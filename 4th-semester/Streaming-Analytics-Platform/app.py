from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
    redirect,
    url_for,
)
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId, json_util
from datetime import datetime, timedelta
import uuid
import traceback
import json
import hashlib
from db import get_db, get_client
PASSWORD_SALT = "streaming_salt_2025"

app = Flask(__name__)
app.secret_key = "super-secret-change-me"

def _now_iso():
    return datetime.utcnow().isoformat()

def _to_float(x, default=0.0):
    try:
        if x is None:
            return default
        return float(x)
    except Exception:
        return default

def _build_view_user(user_doc):
    if not user_doc:
        return None

    auth = user_doc.get("auth", {})
    profile = user_doc.get("profile", {})
    preferences = user_doc.get("preferences", {})
    statistics = user_doc.get("statistics", {})
    subscription = user_doc.get("subscription", {})
    watchlist = user_doc.get("watchlist", [])

    return {
        "_id": str(user_doc.get("_id")),
        "username": auth.get("username"),
        "email": auth.get("email"),
        "role": auth.get("role"),
        "created_at": user_doc.get("created_at"),
        "last_login": auth.get("last_login"),
        "profile": profile,
        "preferences": preferences,
        "statistics": statistics,
        "subscription": subscription,
        "watchlist": watchlist,
    }

def get_current_user():
    
    db = get_db()

    if session.get("guest"):
        user = {
            "_id": "guest",
            "username": "guest",
            "email": "guest@example.com",
            "role": "viewer",
            "created_at": None,
            "last_login": None,
            "profile": {
                "name": "Guest User",
                "country": "",
                "join_date": "",
                "bio": "",
                "profile_picture": "https://via.placeholder.com/120",
            },
            "preferences": {
                "favorite_genres": [],
                "language": "en",
                "notifications": {"email": False, "push": False},
            },
            "statistics": {
                "login_count": 0,
                "movies_watched": 0,
                "ratings_given": 0,
                "reviews_written": 0,
                "total_watch_time": 0,
            },
            "subscription": {
                "auto_renew": False,
                "plan": "free",
                "status": "free",
                "start_date": None,
                "end_date": None,
            },
            "watchlist": [],
        }
        return user, "guest"

    user_id = session.get("user_id")
    if not user_id:
        return None, None

    try:
        from bson import ObjectId
        query_id = ObjectId(user_id) if ObjectId.is_valid(user_id) else user_id
        doc = db["users"].find_one({"_id": query_id})
    except:
        doc = db["users"].find_one({"_id": user_id})
    
    if not doc:
        return None, None

    view_user = _build_view_user(doc)
    role = view_user.get("role") or "user"
    return view_user, role

def require_login():
    user, role = get_current_user()
    if not user:
        return None, None, redirect(url_for("login_page"))
    return user, role, None

def _collections_config():
    
    db = get_db()
    coll_names = sorted(
        [c for c in db.list_collection_names() if not c.startswith("system.")]
    )

    config = []
    for name in coll_names:
        coll = db[name]
        
        is_view = False
        try:
            options = db.command({'listCollections': 1, 'filter': {'name': name}})
            if options['cursor']['firstBatch']:
                coll_info = options['cursor']['firstBatch'][0]
                is_view = coll_info.get('type') == 'view'
        except:
            pass
        
        sample = coll.find_one() or {}
        fields = {}
        
        for k, v in sample.items():
            if k == "_id":
                continue
            t = type(v).__name__
            fields[k] = t

        read_only = is_view or name in {"resource_locks", "system_indexes", "transaction_log", "daily_activity_mv"}

        config.append({
            "name": name,
            "fields": fields,
            "read_only": read_only,
            "is_view": is_view
        })
    return config

def create_views():
    
    db = get_db()
    
    try:
        db.command({
            'create': 'movie_details_view',
            'viewOn': 'movies',
            'pipeline': [
                {
                    '$lookup': {
                        'from': 'genres',
                        'localField': 'genre_ids',
                        'foreignField': '_id',
                        'as': 'genres'
                    }
                },
                {
                    '$project': {
                        'title': 1,
                        'release_year': 1,
                        'duration_min': 1,
                        'rating_avg': 1,
                        'rating_count': 1,
                        'genres.name': 1,
                        'director_ids': 1,
                        'actor_ids': 1
                    }
                }
            ]
        })
        print("Created movie_details_view")
    except Exception as e:
        print(f"Note: movie_details_view might already exist: {e}")
    
    try:
        db.command({
            'create': 'user_activity_view',
            'viewOn': 'users',
            'pipeline': [
                {
                    '$project': {
                        'username': '$auth.username',
                        'email': '$auth.email',
                        'name': '$profile.name',
                        'country': '$profile.country',
                        'join_date': '$profile.join_date',
                        'last_login': '$auth.last_login',
                        'subscription_plan': '$subscription.plan',
                        'subscription_status': '$subscription.status',
                        'movies_watched': '$statistics.movies_watched',
                        'ratings_given': '$statistics.ratings_given',
                        'reviews_written': '$statistics.reviews_written',
                        'total_watch_time': '$statistics.total_watch_time',
                        'watchlist_count': {'$size': '$watchlist'}
                    }
                }
            ]
        })
        print("Created user_activity_view")
    except Exception as e:
        print(f"Note: user_activity_view might already exist: {e}")

@app.post("/api/auth/register")
def api_register():
    db = get_db()
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""
    confirm = data.get("confirm_password") or ""

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400
    if password != confirm:
        return jsonify({"error": "Passwords do not match"}), 400
    if len(password) < 6:
        return jsonify({"error": "Password too short"}), 400

    existing = db["users"].find_one({"auth.username": username})
    if existing:
        return jsonify({"error": "Username already taken"}), 400

    user_id = str(uuid.uuid4())
    now = _now_iso()
    
    import hashlib
    salted_password = password + PASSWORD_SALT
    password_hash = hashlib.sha256(salted_password.encode('utf-8')).hexdigest()

    user_doc = {
        "_id": user_id,
        "active": True,
        "auth": {
            "email": email,
            "email_verified": False,
            "last_login": now,
            "password_hash": password_hash,
            "role": "user",
            "username": username,
        },
        "created_at": now,
        "preferences": {
            "favorite_genres": [],
            "language": "en",
            "notifications": {"email": True, "push": False},
        },
        "profile": {
            "bio": "",
            "country": "",
            "join_date": now,
            "name": username,
            "profile_picture": "https://via.placeholder.com/120",
        },
        "statistics": {
            "login_count": 1,
            "movies_watched": 0,
            "ratings_given": 0,
            "reviews_written": 0,
            "total_watch_time": 0,
        },
        "subscription": {
            "auto_renew": False,
            "end_date": None,
            "plan": "free",
            "start_date": None,
            "status": "free",
        },
        "version": 1,
        "watchlist": [],
    }

    db["users"].insert_one(user_doc)
    session.clear()
    session["user_id"] = user_id

    return jsonify({"message": "Registered", "user_id": user_id})

@app.post("/api/auth/login")
def api_login():
    db = get_db()
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    user = db["users"].find_one({"auth.username": username})
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    password_hash = user["auth"].get("password_hash") or ""
    
    ok = False
    
    if password_hash and (password_hash.startswith("$2b$") or password_hash.startswith("$2a$")):
        try:
            if check_password_hash(password_hash, password):
                ok = True
        except:
            pass
    
    if not ok and password_hash and len(password_hash) == 64:
        salted_password = password + PASSWORD_SALT
        sha256_hash = hashlib.sha256(salted_password.encode('utf-8')).hexdigest()
        if sha256_hash == password_hash:
            ok = True
    
    if not ok and password_hash == password:
        ok = True
    
    if not ok and user["auth"].get("password") == password:
        ok = True

    if not ok:
        return jsonify({"error": "Invalid username or password"}), 401

    now = _now_iso()
    db["users"].update_one(
        {"_id": user["_id"]},
        {
            "$set": {"auth.last_login": now},
            "$inc": {"statistics.login_count": 1, "version": 1},
        },
    )

    session.clear()
    session["user_id"] = str(user["_id"])
    session["guest"] = False

    return jsonify({"message": "Login successful"})

@app.get("/api/auth/logout")
def api_logout():
    session.clear()
    return jsonify({"message": "Logged out"})

@app.get("/api/auth/current")
def api_auth_current():
    user, role = get_current_user()
    if not user:
        return jsonify({"authenticated": False})

    return jsonify({
        "authenticated": True,
        "role": role,
        "user": {
            "username": user.get("username"),
            "email": user.get("email"),
            "profile": user.get("profile"),
        },
    })

@app.get("/api/auth/guest")
def api_guest_login():
    session.clear()
    session["guest"] = True
    return jsonify({"message": "Guest login OK"})

@app.route("/user/movies")
def user_movies_page():
    user, role, redirect_resp = require_login()
    if redirect_resp:
        return redirect_resp
    if (role or "").lower() == "admin":
        return redirect(url_for("movies_page"))
    return render_template("user_movies.html", user=user, role=role)

@app.route("/")
def home():
    user, role = get_current_user()
    if not user:
        return redirect(url_for("login_page"))

    if (role or "").lower() != "admin" and user["_id"] != "guest":
        db = get_db()
        user_doc = db["users"].find_one({"_id": user["_id"]}, {"watchlist": 1})
        if user_doc:
            user["watchlist_count"] = len(user_doc.get("watchlist", []))
        else:
            user["watchlist_count"] = 0

    if (role or "").lower() == "admin":
        return render_template("index.html", user=user, role=role)
    else:
        return render_template("user_dashboard.html", user=user, role=role)

@app.route("/login")
def login_page():
    user, role = get_current_user()
    if user:
        return redirect(url_for("home"))
    return render_template("login.html", user=None, role=None)

@app.route("/register")
def register_page():
    user, role = get_current_user()
    if user:
        return redirect(url_for("home"))
    return render_template("register.html", user=None, role=None)

@app.route("/guest")
def guest_page():
    user, role = get_current_user()
    return render_template("guest.html", user=user, role=role)

@app.route("/movies")
def movies_page():
    user, role, redirect_resp = require_login()
    if redirect_resp:
        return redirect_resp
    return render_template("movies.html", user=user, role=role)

@app.route("/users")
def users_page():
    user, role, redirect_resp = require_login()
    if redirect_resp:
        return redirect_resp
    return render_template("users.html", user=user, role=role)

@app.route("/subscriptions")
def subscriptions_page():
    user, role, redirect_resp = require_login()
    if redirect_resp:
        return redirect_resp
    return render_template("subscriptions.html", user=user, role=role)

@app.route("/studio")
def studio_page():
    user, role, redirect_resp = require_login()
    if redirect_resp:
        return redirect_resp
    return render_template("studio.html", user=user, role=role)

@app.route("/performance")
def performance_page():
    user, role, redirect_resp = require_login()
    if redirect_resp:
        return redirect_resp
    return render_template("performance.html", user=user, role=role)

@app.route("/advanced")
def advanced_page():
    user, role, redirect_resp = require_login()
    if redirect_resp:
        return redirect_resp
    if (role or "").lower() != "admin":
        return redirect(url_for("home"))
    return render_template("advanced.html", user=user, role=role)

@app.route("/profile")
def profile_page():
    user, role, redirect_resp = require_login()
    if redirect_resp:
        return redirect_resp
    
    db = get_db()
    if user and user["_id"] != "guest":
        user_doc = db["users"].find_one({"_id": user["_id"]}, {"watchlist": 1})
        if user_doc:
            user["watchlist_count"] = len(user_doc.get("watchlist", []))
        else:
            user["watchlist_count"] = 0
    
    return render_template("profile.html", user=user, role=role)

@app.route("/user/watchlist")
def user_watchlist_page():
    user, role, redirect_resp = require_login()
    if redirect_resp:
        return redirect_resp
    if (role or "").lower() == "admin":
        return redirect(url_for("home"))
    
    db = get_db()
    if user and user["_id"] != "guest":
        user_doc = db["users"].find_one({"_id": user["_id"]}, {"watchlist": 1})
        if user_doc:
            user["watchlist_count"] = len(user_doc.get("watchlist", []))
        else:
            user["watchlist_count"] = 0
    
    return render_template("user_watchlist.html", user=user, role=role)

@app.get("/api/summary-stats")
def api_summary_stats():
    db = get_db()
    
    try:
        users_coll = db["users"]
        movies_coll = db["movies"]
        actors_coll = db["actors"]
        directors_coll = db["directors"]
        subs_coll = db["subscriptions"]
        payments_coll = db["payments"]

        users_count = users_coll.estimated_document_count()
        movies_count = movies_coll.estimated_document_count()
        actors_count = actors_coll.estimated_document_count()
        directors_count = directors_coll.estimated_document_count()
        active_subs = subs_coll.count_documents({"active": True})

        pipeline = [
            {"$group": {"_id": None, "total": {"$sum": "$amount_usd"}}}
        ]
        agg = list(payments_coll.aggregate(pipeline))
        total_payments = _to_float(agg[0]["total"]) if agg else 0.0

        return jsonify({
            "users": users_count,
            "movies": movies_count,
            "actors": actors_count,
            "directors": directors_count,
            "active_subscriptions": active_subs,
            "total_payments": total_payments,
        })
    except Exception as e:
        app.logger.error(f"Error in summary stats: {e}")
        return jsonify({
            "users": 0,
            "movies": 0,
            "actors": 0,
            "directors": 0,
            "active_subscriptions": 0,
            "total_payments": 0.0,
        })

@app.get("/api/top-movies")
def api_top_movies():
    db = get_db()
    movies = db["movies"]

    try:
        cursor = movies.find(
            {"rating_avg": {"$exists": True}},
            {"title": 1, "rating_avg": 1}
        ).sort("rating_avg", -1).limit(10)

        result = []
        for m in cursor:
            result.append({
                "title": m.get("title", "Unknown"),
                "avgRating": _to_float(m.get("rating_avg")),
            })
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error in top movies: {e}")
        return jsonify([])

@app.get("/api/top-genres")
def api_top_genres():
    db = get_db()
    movies = db["movies"]

    try:
        pipeline = [
            {"$unwind": "$genre_ids"},
            {
                "$lookup": {
                    "from": "genres",
                    "localField": "genre_ids",
                    "foreignField": "_id",
                    "as": "genre",
                }
            },
            {"$unwind": "$genre"},
            {
                "$group": {
                    "_id": "$genre.name",
                    "count": {"$sum": 1},
                }
            },
            {"$sort": {"count": -1}},
            {"$limit": 10},
        ]
        data = list(movies.aggregate(pipeline))
        return jsonify(data)
    except Exception as e:
        app.logger.error(f"Error in top genres: {e}")
        return jsonify([])

@app.get("/api/active-users")
def api_active_users():
    db = get_db()
    watch_history = db["watch_history"]
    users_coll = db["users"]

    try:
        limit = int(request.args.get("limit", 10))

        pipeline = [
            {"$group": {"_id": "$user_id", "watches": {"$sum": 1}}},
            {"$sort": {"watches": -1}},
            {"$limit": limit},
        ]
        grouped = list(watch_history.aggregate(pipeline))
        result = []

        for g in grouped:
            uid = g["_id"]
            user_doc = users_coll.find_one(
                {"_id": uid},
                {"profile.name": 1, "auth.username": 1},
            )
            if user_doc:
                name = (
                    user_doc.get("profile", {}).get("name")
                    or user_doc.get("auth", {}).get("username")
                    or uid
                )
            else:
                name = uid

            result.append({
                "user": name,
                "watches": g["watches"],
            })

        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error in active users: {e}")
        return jsonify([])

@app.get("/api/reviews-per-month")
def api_reviews_per_month():
    db = get_db()
    reviews = db["reviews"]

    try:
        year = int(request.args.get("year", 2025))

        pipeline = [
            {
                "$addFields": {
                    "year_month": {
                        "$substr": ["$created_at", 0, 7]
                    }
                }
            },
            {
                "$match": {
                    "year_month": {"$regex": f"^{year}"}
                }
            },
            {
                "$group": {
                    "_id": {"$substr": ["$year_month", 5, 2]},
                    "reviews": {"$sum": 1},
                }
            },
            {"$sort": {"_id": 1}},
        ]

        raw = list(reviews.aggregate(pipeline))
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        data = []
        for r in raw:
            month_num = int(r["_id"]) if r["_id"].isdigit() else 1
            label = month_names[month_num - 1] if 1 <= month_num <= 12 else str(month_num)
            data.append({"_id": label, "reviews": r["reviews"]})
        return jsonify(data)
    except Exception as e:
        app.logger.error(f"Error in reviews per month: {e}")
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        return jsonify([{"_id": m, "reviews": 0} for m in month_names])

@app.get("/api/subscription-plans")
def api_subscription_plans():
    db = get_db()
    subs = db["subscriptions"]

    try:
        pipeline = [
            {"$group": {"_id": "$plan", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
        ]
        data = list(subs.aggregate(pipeline))
        return jsonify(data)
    except Exception as e:
        app.logger.error(f"Error in subscription plans: {e}")
        return jsonify([])

@app.get("/api/movies")
def api_movies_filtered():
    db = get_db()
    movies = db["movies"]

    try:
        min_year = int(request.args.get("min_year", 0) or 0)
        min_rating = float(request.args.get("min_rating", 0) or 0)
        limit = int(request.args.get("limit", 0) or 0)

        sort_by_param = request.args.get("sort_by", "rating")
        sort_dir_param = request.args.get("sort_dir", "desc")

        sort_field_map = {
            "rating": "rating_avg",
            "year": "release_year",
            "duration": "duration_min",
            "title": "title",
        }
        sort_field = sort_field_map.get(sort_by_param, "rating_avg")
        sort_dir = 1 if sort_dir_param == "asc" else -1

        query = {}
        if min_year:
            query["release_year"] = {"$gte": min_year}
        if min_rating:
            query["rating_avg"] = {"$gte": min_rating}

        cursor = movies.find(
            query,
            {"title": 1, "release_year": 1, "duration_min": 1, "rating_avg": 1},
        ).sort(sort_field, sort_dir)

        if limit > 0:
            cursor = cursor.limit(limit)

        docs = []
        for m in cursor:
            docs.append({
                "title": m.get("title", ""),
                "release_year": m.get("release_year"),
                "duration_min": m.get("duration_min"),
                "rating_avg": _to_float(m.get("rating_avg")),
            })
        return jsonify(docs)
    except Exception as e:
        app.logger.error(f"Error in movies filtered: {e}")
        return jsonify([])

@app.get("/api/movies/stats")
def api_movies_stats():
    db = get_db()
    movies = db["movies"]

    try:
        total = movies.estimated_document_count()

        pipeline_avg = [
            {"$match": {"rating_avg": {"$exists": True, "$ne": None}}},
            {"$group": {"_id": None, "avgRating": {"$avg": "$rating_avg"}}},
        ]
        agg = list(movies.aggregate(pipeline_avg))
        avg_rating = _to_float(agg[0]["avgRating"]) if agg else 0.0

        pipeline_max = [
            {"$match": {"duration_min": {"$exists": True, "$ne": None}}},
            {"$group": {"_id": None, "maxDuration": {"$max": "$duration_min"}}},
        ]
        agg2 = list(movies.aggregate(pipeline_max))
        max_dur = agg2[0]["maxDuration"] if agg2 else 0

        return jsonify({
            "total": total,
            "avgRating": avg_rating,
            "maxDuration": max_dur,
        })
    except Exception as e:
        app.logger.error(f"Error in movies stats: {e}")
        return jsonify({
            "total": 0,
            "avgRating": 0.0,
            "maxDuration": 0,
        })

@app.get("/api/movies/by-year")
def api_movies_by_year():
    db = get_db()
    movies = db["movies"]

    try:
        pipeline = [
            {"$match": {"release_year": {"$exists": True}}},
            {"$group": {"_id": "$release_year", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}},
        ]
        data = list(movies.aggregate(pipeline))
        return jsonify(data)
    except Exception as e:
        app.logger.error(f"Error in movies by year: {e}")
        return jsonify([])

@app.get("/api/movies/rating-distribution")
def api_movies_rating_distribution():
    db = get_db()
    movies = db["movies"]

    try:
        pipeline = [
            {"$match": {"rating_avg": {"$exists": True, "$ne": None}}},
            {
                "$bucket": {
                    "groupBy": "$rating_avg",
                    "boundaries": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    "default": 10,
                    "output": {"count": {"$sum": 1}},
                }
            },
            {"$sort": {"_id": 1}},
        ]
        data = list(movies.aggregate(pipeline))
        return jsonify(data)
    except Exception as e:
        app.logger.error(f"Error in rating distribution: {e}")
        return jsonify([])

@app.get("/api/movies/sample-paged")
def api_movies_sample_paged():
    db = get_db()
    movies = db["movies"]

    try:
        page = int(request.args.get("page", 1) or 1)
        page_size = int(request.args.get("page_size", 10) or 10)
        skip = (page - 1) * page_size

        total = movies.estimated_document_count()

        cursor = movies.find(
            {},
            {"title": 1, "release_year": 1, "duration_min": 1, "rating_avg": 1},
        ).sort("release_year", -1).skip(skip).limit(page_size)

        docs = []
        for m in cursor:
            docs.append({
                "title": m.get("title", ""),
                "release_year": m.get("release_year"),
                "duration_min": m.get("duration_min"),
                "rating_avg": _to_float(m.get("rating_avg")),
            })

        return jsonify({
            "page": page,
            "page_size": page_size,
            "total": total,
            "docs": docs,
        })
    except Exception as e:
        app.logger.error(f"Error in movies sample paged: {e}")
        return jsonify({
            "page": 1,
            "page_size": 10,
            "total": 0,
            "docs": [],
        })

@app.get("/api/users/country-counts")
def api_users_country_counts():
    db = get_db()
    users = db["users"]

    try:
        pipeline = [
            {
                "$group": {
                    "_id": "$profile.country",
                    "count": {"$sum": 1},
                }
            },
            {"$sort": {"count": -1}},
        ]
        data = list(users.aggregate(pipeline))
        return jsonify(data)
    except Exception as e:
        app.logger.error(f"Error in country counts: {e}")
        return jsonify([])

@app.get("/api/users/sample-paged")
def api_users_sample_paged():
    db = get_db()
    users = db["users"]

    try:
        page = int(request.args.get("page", 1) or 1)
        page_size = int(request.args.get("page_size", 10) or 10)
        skip = (page - 1) * page_size

        total = users.estimated_document_count()

        cursor = users.find(
            {},
            {
                "profile.name": 1,
                "auth.email": 1,
                "profile.country": 1,
                "created_at": 1,
            },
        ).sort("created_at", -1).skip(skip).limit(page_size)

        docs = []
        for u in cursor:
            docs.append({
                "name": u.get("profile", {}).get("name", ""),
                "email": u.get("auth", {}).get("email", ""),
                "country": u.get("profile", {}).get("country", ""),
                "join_date": u.get("created_at", ""),
            })

        return jsonify({
            "page": page,
            "page_size": page_size,
            "total": total,
            "docs": docs,
        })
    except Exception as e:
        app.logger.error(f"Error in users sample paged: {e}")
        return jsonify({
            "page": 1,
            "page_size": 10,
            "total": 0,
            "docs": [],
        })

@app.get("/api/subscriptions/stats")
def api_subs_stats():
    db = get_db()
    subs = db["subscriptions"]

    try:
        total = subs.estimated_document_count()
        active = subs.count_documents({"active": True})

        return jsonify({"total": total, "active": active})
    except Exception as e:
        app.logger.error(f"Error in subscriptions stats: {e}")
        return jsonify({"total": 0, "active": 0})

@app.get("/api/payments/sample-paged")
def api_payments_sample_paged():
    db = get_db()
    payments = db["payments"]

    try:
        page = int(request.args.get("page", 1) or 1)
        page_size = int(request.args.get("page_size", 10) or 10)
        skip = (page - 1) * page_size

        total = payments.estimated_document_count()
        cursor = payments.find(
            {},
            {"user_id": 1, "amount_usd": 1, "method": 1, "paid_at": 1},
        ).sort("paid_at", -1).skip(skip).limit(page_size)

        docs = []
        for p in cursor:
            docs.append({
                "user_id": p.get("user_id", ""),
                "amount_usd": _to_float(p.get("amount_usd")),
                "method": p.get("method", ""),
                "paid_at": p.get("paid_at", ""),
            })

        return jsonify({
            "page": page,
            "page_size": page_size,
            "total": total,
            "docs": docs,
        })
    except Exception as e:
        app.logger.error(f"Error in payments sample paged: {e}")
        return jsonify({
            "page": 1,
            "page_size": 10,
            "total": 0,
            "docs": [],
        })

@app.get("/api/collections")
def api_collections():
    cfg = _collections_config()
    return jsonify(cfg)

def _collection_read_only(name: str) -> bool:
    cfg = _collections_config()
    for c in cfg:
        if c["name"] == name:
            return c.get("read_only", False)
    return False

@app.get("/api/collections/<name>/docs")
def api_collection_docs(name):
    db = get_db()
    coll = db[name]

    try:
        page = int(request.args.get("page", 1) or 1)
        page_size = int(request.args.get("page_size", 10) or 10)
        limit = request.args.get("limit")

        field = request.args.get("field")
        value = request.args.get("value")

        query = {}
        if field and value is not None:
            query[field] = value

        if limit:
            try:
                limit = int(limit)
            except ValueError:
                limit = 10
            page = 1
            page_size = limit
            skip = 0
        else:
            skip = (page - 1) * page_size

        total = coll.count_documents(query)
        cursor = coll.find(query).skip(skip).limit(page_size)

        docs = []
        for d in cursor:
            d["_id"] = str(d["_id"])
            docs.append(d)

        return jsonify({
            "page": page,
            "page_size": page_size,
            "total": total,
            "docs": docs,
        })
    except Exception as e:
        app.logger.error(f"Error in collection docs for {name}: {e}")
        return jsonify({
            "page": 1,
            "page_size": 10,
            "total": 0,
            "docs": [],
        })

@app.post("/api/collections/<name>/docs")
def api_collection_create_doc(name):
    if _collection_read_only(name):
        return jsonify({"error": "Collection is read-only"}), 403

    db = get_db()
    coll = db[name]
    data = request.get_json() or {}

    try:
        if "_id" not in data:
            data["_id"] = str(uuid.uuid4())
        else:
            if isinstance(data["_id"], str) and len(data["_id"]) == 24:
                try:
                    data["_id"] = ObjectId(data["_id"])
                except:
                    pass

        coll.insert_one(data)
        return jsonify({"message": "Created", "_id": str(data["_id"])})
    except Exception as e:
        app.logger.error(f"Error creating doc in {name}: {e}")
        return jsonify({"error": str(e)}), 500

@app.put("/api/collections/<name>/docs/<doc_id>")
def api_collection_update_doc(name, doc_id):
    if _collection_read_only(name):
        return jsonify({"error": "Collection is read-only"}), 403

    db = get_db()
    coll = db[name]
    data = request.get_json() or {}

    try:
        try:
            query_id = ObjectId(doc_id)
        except:
            query_id = doc_id

        res = coll.update_one({"_id": query_id}, {"$set": data})
        if res.matched_count == 0:
            return jsonify({"error": "Document not found"}), 404
        return jsonify({"message": "Updated"})
    except Exception as e:
        app.logger.error(f"Error updating doc {doc_id} in {name}: {e}")
        return jsonify({"error": str(e)}), 500

@app.delete("/api/collections/<name>/docs/<doc_id>")
def api_collection_delete_doc(name, doc_id):
    if _collection_read_only(name):
        return jsonify({"error": "Collection is read-only"}), 403

    db = get_db()
    coll = db[name]

    try:
        try:
            query_id = ObjectId(doc_id)
        except:
            query_id = doc_id

        res = coll.delete_one({"_id": query_id})
        if res.deleted_count == 0:
            return jsonify({"error": "Document not found"}), 404
        return jsonify({"message": "Deleted"})
    except Exception as e:
        app.logger.error(f"Error deleting doc {doc_id} from {name}: {e}")
        return jsonify({"error": str(e)}), 500

@app.get("/api/user/movies/<movie_id>/activity")
def api_movie_activity(movie_id):
    
    import random
    import time
    
    activity = {
        "movie_id": movie_id,
        "active_users": random.randint(0, 3),
        "recent_ratings": random.randint(0, 5),
        "last_updated": _now_iso(),
        "version": random.randint(1, 10)
    }
    
    return jsonify(activity)
    
@app.route("/user/concurrent-test")
def user_concurrent_test_page():
    user, role, redirect_resp = require_login()
    if redirect_resp:
        return redirect_resp
    if (role or "").lower() == "admin":
        return redirect(url_for("home"))
    return render_template("user_concurrent_test.html", user=user, role=role)

@app.get("/api/user/movies")
def api_user_movies():
    
    db = get_db()
    user, role = get_current_user()
    if not user or user["_id"] == "guest":
        return jsonify({"error": "Not logged in"}), 401
    
    try:
        page = int(request.args.get("page", 1) or 1)
        limit = int(request.args.get("limit", 12) or 12)
        title = request.args.get("title", "").strip()
        min_year = request.args.get("min_year")
        min_rating = request.args.get("min_rating")
        genre = request.args.get("genre", "").strip()
        
        skip = (page - 1) * limit
        
        query = {}
        if title:
            query["title"] = {"$regex": title, "$options": "i"}
        if min_year:
            query["release_year"] = {"$gte": int(min_year)}
        if min_rating:
            query["rating_avg"] = {"$gte": float(min_rating)}
        
        if genre:
            genre_doc = db["genres"].find_one({"name": genre})
            if genre_doc:
                query["genre_ids"] = genre_doc["_id"]
        
        total = db["movies"].count_documents(query)
        
        cursor = db["movies"].find(
            query,
            {"title": 1, "release_year": 1, "duration_min": 1, "rating_avg": 1, "genre_ids": 1, "plot": 1}
        ).sort("rating_avg", -1).skip(skip).limit(limit)
        
        movies = []
        for movie in cursor:
            genre_names = []
            if movie.get("genre_ids"):
                genres = list(db["genres"].find({"_id": {"$in": movie.get("genre_ids", [])}}, {"name": 1}))
                genre_names = [g["name"] for g in genres]
            
            movies.append({
                "_id": str(movie["_id"]),
                "title": movie.get("title", ""),
                "release_year": movie.get("release_year"),
                "duration_min": movie.get("duration_min"),
                "rating_avg": _to_float(movie.get("rating_avg")),
                "genre_names": genre_names,
                "plot": movie.get("plot", "")
            })
        
        return jsonify({
            "movies": movies,
            "page": page,
            "limit": limit,
            "total": total,
            "has_more": (skip + len(movies)) < total
        })
    except Exception as e:
        app.logger.error(f"Error in user movies: {e}")
        return jsonify({"movies": [], "total": 0, "error": str(e)}), 500

@app.get("/api/user/movies/<movie_id>")
def api_user_movie_detail(movie_id):
    
    db = get_db()
    user, role = get_current_user()
    if not user or user["_id"] == "guest":
        return jsonify({"error": "Not logged in"}), 401
    
    user_id = user["_id"]
    
    try:
        movie = db["movies"].find_one({"_id": movie_id})
        if not movie:
            return jsonify({"error": "Movie not found"}), 404
        
        genre_names = []
        if movie.get("genre_ids"):
            genres = list(db["genres"].find({"_id": {"$in": movie.get("genre_ids", [])}}, {"name": 1}))
            genre_names = [g["name"] for g in genres]
        
        user_rating = db["ratings"].find_one({"user_id": user_id, "movie_id": movie_id})
        
        user_review = db["reviews"].find_one({"user_id": user_id, "movie_id": movie_id})
        
        movie_data = {
            "_id": str(movie["_id"]),
            "title": movie.get("title", ""),
            "release_year": movie.get("release_year"),
            "duration_min": movie.get("duration_min"),
            "rating_avg": _to_float(movie.get("rating_avg")),
            "rating_count": movie.get("rating_count", 0),
            "plot": movie.get("plot", ""),
            "genre_names": genre_names
        }
        
        return jsonify({
            "movie": movie_data,
            "user_rating": {
                "rating": user_rating.get("rating"),
                "rated_at": user_rating.get("rated_at")
            } if user_rating else None,
            "user_review": {
                "review_text": user_review.get("review_text"),
                "created_at": user_review.get("created_at")
            } if user_review else None
        })
    except Exception as e:
        app.logger.error(f"Error in movie detail: {e}")
        return jsonify({"error": str(e)}), 500

def log_transaction(user_id, tx_type, status, details):
    
    db = get_db()
    tx_log = db["transaction_log"]
    
    tx_doc = {
        "_id": str(uuid.uuid4()),
        "user_id": user_id,
        "type": tx_type,
        "status": status,
        "timestamp": _now_iso(),
        "details": details
    }
    
    tx_log.insert_one(tx_doc)
    return tx_doc

@app.post("/api/user/rate-movie")
def api_user_rate_movie():
    
    db = get_db()
    user, role = get_current_user()
    if not user or user["_id"] == "guest":
        return jsonify({"error": "Not logged in"}), 401
    
    user_id = user["_id"]
    data = request.get_json() or {}
    movie_id = data.get("movie_id")
    rating = int(data.get("rating", 0))
    review_text = data.get("review_text", "").strip()
    
    test_concurrent = data.get("test_concurrent", False)
    
    if not movie_id or not rating or rating < 1 or rating > 10:
        return jsonify({"error": "Valid movie_id and rating (1-10) required"}), 400
    
    if test_concurrent:
        app.logger.info(f"CONCURRENT TEST: User {user_id} rating movie {movie_id} with rating {rating}")
    
    try:
        log_transaction(user_id, "movie_rating", "started", 
                       f"Starting movie rating transaction for movie {movie_id} with rating {rating}")
        
        client = get_client()
        session = client.start_session()
        
        with session.start_transaction():
            movie = db["movies"].find_one({"_id": movie_id}, session=session)
            if not movie:
                raise ValueError("Movie not found")
            
            current_version = movie.get("version", 1)
            
            existing_rating = db["ratings"].find_one(
                {"user_id": user_id, "movie_id": movie_id},
                session=session
            )
            
            now = _now_iso()
            
            if existing_rating:
                old_rating = existing_rating.get("rating", 0)
                db["ratings"].update_one(
                    {"_id": existing_rating["_id"]},
                    {"$set": {"rating": rating, "rated_at": now}},
                    session=session
                )
                
                result = db["movies"].update_one(
                    {"_id": movie_id, "version": current_version},
                    {
                        "$inc": {
                            "rating_sum": rating - old_rating,
                            "version": 1
                        }
                    },
                    session=session
                )
                
                if test_concurrent:
                    app.logger.info(f"CONCURRENT TEST: Updating existing rating - version {current_version}")
                
                if result.matched_count == 0:
                    log_transaction(user_id, "movie_rating", "conflict",
                                   f"Concurrent modification detected for movie {movie_id} while updating rating")
                    raise ValueError("Concurrent modification detected. Please try again.")
            else:
                rating_id = str(uuid.uuid4())
                db["ratings"].insert_one({
                    "_id": rating_id,
                    "user_id": user_id,
                    "movie_id": movie_id,
                    "rating": rating,
                    "rated_at": now
                }, session=session)
                
                result = db["movies"].update_one(
                    {"_id": movie_id, "version": current_version},
                    {
                        "$inc": {
                            "rating_sum": rating,
                            "rating_count": 1,
                            "version": 1
                        }
                    },
                    session=session
                )
                
                if test_concurrent:
                    app.logger.info(f"CONCURRENT TEST: Creating new rating - version {current_version}")
                
                if result.matched_count == 0:
                    log_transaction(user_id, "movie_rating", "conflict",
                                   f"Concurrent modification detected for movie {movie_id} while creating new rating")
                    raise ValueError("Concurrent modification detected. Please try again.")
            
            movie_after = db["movies"].find_one({"_id": movie_id}, session=session)
            if movie_after:
                new_count = movie_after.get("rating_count", 0)
                new_sum = movie_after.get("rating_sum", 0)
                new_avg = new_sum / new_count if new_count > 0 else 0
                
                db["movies"].update_one(
                    {"_id": movie_id},
                    {"$set": {"rating_avg": new_avg}},
                    session=session
                )
            
            existing_review = None
            if review_text:
                existing_review = db["reviews"].find_one(
                    {"user_id": user_id, "movie_id": movie_id},
                    session=session
                )
                
                if existing_review:
                    db["reviews"].update_one(
                        {"_id": existing_review["_id"]},
                        {"$set": {"review_text": review_text, "updated_at": now}},
                        session=session
                    )
                else:
                    review_id = str(uuid.uuid4())
                    db["reviews"].insert_one({
                        "_id": review_id,
                        "user_id": user_id,
                        "movie_id": movie_id,
                        "review_text": review_text,
                        "created_at": now,
                        "updated_at": now
                    }, session=session)
            
            db["users"].update_one(
                {"_id": user_id},
                {
                    "$inc": {
                        "statistics.ratings_given": 1 if not existing_rating else 0,
                        "statistics.reviews_written": 1 if review_text and not existing_review else 0,
                        "version": 1
                    }
                },
                session=session
            )
            
            log_transaction(user_id, "movie_rating", "committed",
                           f"Successfully rated movie {movie_id} with rating {rating}. "
                           f"Review added: {'yes' if review_text else 'no'}")
        
        if test_concurrent:
            app.logger.info(f"CONCURRENT TEST RESULT: Success for user {user_id}")
        
        return jsonify({
            "message": "Rating submitted successfully",
            "movie_id": movie_id,
            "rating": rating,
            "review_added": bool(review_text),
            "concurrent_test": test_concurrent,
            "timestamp": now
        })
        
    except Exception as e:
        if test_concurrent:
            app.logger.info(f"CONCURRENT TEST RESULT: Conflict for user {user_id} - {str(e)}")
        
        log_transaction(user_id, "movie_rating", "failed",
                       f"Failed to rate movie {movie_id}. Error: {str(e)}")
        
        if 'session' in locals():
            session.abort_transaction()
            session.end_session()
        
        app.logger.error(f"Error in rate movie: {e}")
        
        if "Concurrent modification" in str(e):
            return jsonify({"error": "Concurrent modification detected. Please refresh and try again."}), 409
        return jsonify({"error": str(e)}), 500
    finally:
        if 'session' in locals():
            session.end_session()

@app.post("/api/user/toggle-watchlist")
def api_user_toggle_watchlist():
    
    db = get_db()
    user, role = get_current_user()
    if not user or user["_id"] == "guest":
        return jsonify({"error": "Not logged in"}), 401
    
    user_id = user["_id"]
    data = request.get_json() or {}
    movie_id = data.get("movie_id")
    
    if not movie_id:
        return jsonify({"error": "movie_id required"}), 400
    
    try:
        movie = db["movies"].find_one({"_id": movie_id})
        if not movie:
            return jsonify({"error": "Movie not found"}), 404
        
        user_doc = db["users"].find_one({"_id": user_id})
        if not user_doc:
            return jsonify({"error": "User not found"}), 404
        
        current_watchlist = user_doc.get("watchlist", [])
        
        if movie_id in current_watchlist:
            db["users"].update_one(
                {"_id": user_id},
                {
                    "$pull": {"watchlist": movie_id},
                    "$inc": {"version": 1}
                }
            )
            message = "Removed from watchlist"
            action = "remove"
        else:
            db["users"].update_one(
                {"_id": user_id},
                {
                    "$addToSet": {"watchlist": movie_id},
                    "$inc": {"version": 1}
                }
            )
            message = "Added to watchlist"
            action = "add"
        
        log_transaction(user_id, "watchlist_update", "committed",
                       f"{action.capitalize()} movie {movie_id} ({movie.get('title', 'Unknown')}) to/from watchlist")
        
        return jsonify({
            "message": message,
            "movie_id": movie_id,
            "in_watchlist": movie_id not in current_watchlist
        })
        
    except Exception as e:
        log_transaction(user_id, "watchlist_update", "failed",
                       f"Failed to update watchlist for movie {movie_id}. Error: {str(e)}")
        
        app.logger.error(f"Error in toggle watchlist: {e}")
        return jsonify({"error": str(e)}), 500

@app.get("/api/user/watchlist")
def api_user_watchlist():
    
    db = get_db()
    user, role = get_current_user()
    if not user or user["_id"] == "guest":
        return jsonify({"error": "Not logged in"}), 401
    
    user_id = user["_id"]
    
    try:
        user_doc = db["users"].find_one({"_id": user_id})
        if not user_doc:
            return jsonify({"error": "User not found"}), 404
        
        watchlist_ids = user_doc.get("watchlist", [])
        
        movies = []
        if watchlist_ids:
            cursor = db["movies"].find(
                {"_id": {"$in": watchlist_ids}},
                {"title": 1, "release_year": 1, "duration_min": 1, "rating_avg": 1}
            )
            
            for movie in cursor:
                movies.append({
                    "_id": str(movie["_id"]),
                    "title": movie.get("title", ""),
                    "release_year": movie.get("release_year"),
                    "duration_min": movie.get("duration_min"),
                    "rating_avg": _to_float(movie.get("rating_avg"))
                })
        
        return jsonify({
            "movies": movies,
            "count": len(movies)
        })
        
    except Exception as e:
        app.logger.error(f"Error in watchlist: {e}")
        return jsonify({"movies": [], "error": str(e)}), 500

@app.post("/api/performance/create-indexes")
def api_create_indexes():
    db = get_db()
    
    try:
        movies = db["movies"]
        ratings = db["ratings"]
        reviews = db["reviews"]
        watch_history = db["watch_history"]

        idx_info = {}

        try:
            idx_info["movies_rating_year"] = movies.create_index(
                [("rating_avg", -1), ("release_year", -1)],
                name="rating_year_idx",
            )
        except Exception as e:
            idx_info["movies_rating_year"] = f"Error: {e}"

        try:
            idx_info["movies_title_text"] = movies.create_index(
                [("title", "text")],
                name="title_text_idx",
            )
        except Exception as e:
            idx_info["movies_title_text"] = f"Error: {e}"

        try:
            idx_info["ratings_movie_user"] = ratings.create_index(
                [("movie_id", 1), ("user_id", 1)],
                name="ratings_movie_user_idx",
            )
        except Exception as e:
            idx_info["ratings_movie_user"] = f"Error: {e}"

        try:
            idx_info["reviews_movie"] = reviews.create_index(
                [("movie_id", 1)],
                name="reviews_movie_idx",
            )
        except Exception as e:
            idx_info["reviews_movie"] = f"Error: {e}"

        try:
            idx_info["watch_history_user_date"] = watch_history.create_index(
                [("user_id", 1), ("watch_date", -1)],
                name="watch_user_date_idx",
            )
        except Exception as e:
            idx_info["watch_history_user_date"] = f"Error: {e}"

        return jsonify({"indexes_created": idx_info})
    except Exception as e:
        app.logger.error(f"Error creating indexes: {e}")
        return jsonify({"error": str(e)}), 500

@app.get("/api/performance/explain-movies")
def api_explain_movies():
    db = get_db()
    movies = db["movies"]

    try:
        query = {"rating_avg": {"$gte": 7}}
        explain = movies.find(query).sort("rating_avg", -1).limit(50).explain(
            "executionStats"
        )

        import json
        return json.dumps(explain, indent=2), 200, {"Content-Type": "text/plain"}
    except Exception as e:
        app.logger.error(f"Error explaining movies query: {e}")
        return json.dumps({"error": str(e)}), 500, {"Content-Type": "text/plain"}

@app.post("/api/ratings/add-with-tx")
def api_ratings_add_with_tx():
    db = get_db()
    client = get_client()
    data = request.get_json() or {}
    user_id = data.get("user_id")
    movie_id = data.get("movie_id")
    rating = int(data.get("rating")) if data.get("rating") else 0

    if not user_id or not movie_id or not rating:
        return jsonify({"error": "Missing fields"}), 400

    ratings = db["ratings"]
    movies = db["movies"]

    session = client.start_session()
    try:
        log_transaction(user_id, "admin_rating_add", "started",
                       f"Starting admin rating transaction for movie {movie_id} by user {user_id}")
        
        with session.start_transaction():
            ratings.insert_one(
                {
                    "_id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "movie_id": movie_id,
                    "rating": rating,
                    "rated_at": _now_iso(),
                },
                session=session,
            )

            movies.update_one(
                {"_id": movie_id},
                {
                    "$inc": {
                        "rating_sum": rating,
                        "rating_count": 1,
                    }
                },
                session=session,
            )

            movie_doc = movies.find_one({"_id": movie_id}, session=session)
            if movie_doc:
                count = movie_doc.get("rating_count", 0)
                total = movie_doc.get("rating_sum", 0)
                avg = total / count if count else 0
                movies.update_one(
                    {"_id": movie_id},
                    {"$set": {"rating_avg": avg}},
                    session=session,
                )
            
            log_transaction(user_id, "admin_rating_add", "committed",
                           f"Successfully added rating {rating} to movie {movie_id} for user {user_id}")
    except Exception as e:
        session.abort_transaction()
        
        log_transaction(user_id, "admin_rating_add", "failed",
                       f"Failed to add rating to movie {movie_id}. Error: {str(e)}")
        
        app.logger.error(f"Transaction failed: {e}")
        return jsonify({"error": f"Transaction failed: {str(e)}"}), 500
    finally:
        session.end_session()

    return jsonify({"message": "Rating inserted with transaction"})

@app.post("/api/movies/bulk-rating-reset")
def api_movies_bulk_rating_reset():
    db = get_db()
    movies = db["movies"]
    data = request.get_json() or {}
    before_year = int(data.get("before_year", 2000))

    try:
        res = movies.update_many(
            {"release_year": {"$lt": before_year}},
            {"$set": {"rating_avg": 0, "rating_sum": 0, "rating_count": 0}},
        )

        return jsonify({
            "matched": res.matched_count,
            "modified": res.modified_count,
        })
    except Exception as e:
        app.logger.error(f"Error in bulk rating reset: {e}")
        return jsonify({
            "matched": 0,
            "modified": 0,
            "error": str(e)
        }), 500

@app.post("/api/locking/update-movie-rating")
def api_optimistic_update_movie_rating():
    db = get_db()
    movies = db["movies"]
    data = request.get_json() or {}
    movie_id = data.get("movie_id")
    new_rating = _to_float(data.get("rating_avg"))
    version = int(data.get("version", 0))
    
    user_id = session.get("user_id") or "system"

    if not movie_id or not version:
        return jsonify({"error": "movie_id and version required"}), 400

    try:
        log_transaction(user_id, "optimistic_lock_update", "started",
                       f"Starting optimistic lock update for movie {movie_id}, version {version}, new rating {new_rating}")
        
        res = movies.update_one(
            {"_id": movie_id, "version": version},
            {
                "$set": {"rating_avg": new_rating},
                "$inc": {"version": 1},
            },
        )

        if res.matched_count == 0:
            current = movies.find_one({"_id": movie_id})
            if not current:
                log_transaction(user_id, "optimistic_lock_update", "failed",
                               f"Movie {movie_id} not found for optimistic lock update")
                return jsonify({"error": "Movie not found"}), 404
            
            log_transaction(user_id, "optimistic_lock_update", "conflict",
                           f"Optimistic lock conflict for movie {movie_id}. "
                           f"Expected version {version}, current version {current.get('version')}")
            
            return jsonify({
                "status": "conflict",
                "message": "Version does not match current document",
                "current_version": current.get("version"),
                "current_rating": _to_float(current.get("rating_avg")),
            })

        updated = movies.find_one({"_id": movie_id})
        
        log_transaction(user_id, "optimistic_lock_update", "committed",
                       f"Successfully updated movie {movie_id} with optimistic lock. "
                       f"New rating: {new_rating}, new version: {updated.get('version')}")
        
        return jsonify({
            "status": "success",
            "message": "Rating updated with optimistic lock",
            "new_version": updated.get("version"),
        })
    except Exception as e:
        log_transaction(user_id, "optimistic_lock_update", "failed",
                       f"Failed optimistic lock update for movie {movie_id}. Error: {str(e)}")
        
        app.logger.error(f"Error in optimistic lock update: {e}")
        return jsonify({"error": str(e)}), 500

@app.post("/api/locking/acquire-lock")
def api_acquire_lock():
    db = get_db()
    locks = db["resource_locks"]
    data = request.get_json() or {}
    resource_id = data.get("resource_id")
    timeout = int(data.get("timeout", 30))

    if not resource_id:
        return jsonify({"error": "resource_id required"}), 400

    try:
        owner = session.get("user_id") or "guest"
        now = datetime.utcnow()
        expires_at = now + timedelta(seconds=timeout)

        locks.delete_many({"expires_at": {"$lte": now.isoformat()}})

        existing = locks.find_one({
            "resource_id": resource_id,
            "expires_at": {"$gt": now.isoformat()},
        })
        if existing and existing.get("owner") != owner:
            return (
                jsonify({
                    "message": "Resource already locked",
                    "current_owner": existing.get("owner"),
                    "expires_at": existing.get("expires_at"),
                }),
                423,
            )

        lock_id = str(uuid.uuid4())
        locks.update_one(
            {"resource_id": resource_id},
            {
                "$set": {
                    "owner": owner,
                    "lock_id": lock_id,
                    "expires_at": expires_at.isoformat(),
                }
            },
            upsert=True,
        )

        return jsonify({
            "message": "Lock acquired",
            "lock_id": lock_id,
            "expires_at": expires_at.isoformat(),
        })
    except Exception as e:
        app.logger.error(f"Error acquiring lock: {e}")
        return jsonify({"error": str(e)}), 500

@app.post("/api/locking/release-lock")
def api_release_lock():
    db = get_db()
    locks = db["resource_locks"]
    data = request.get_json() or {}
    resource_id = data.get("resource_id")
    if not resource_id:
        return jsonify({"error": "resource_id required"}), 400

    try:
        owner = session.get("user_id") or "guest"
        res = locks.delete_one({"resource_id": resource_id, "owner": owner})
        if res.deleted_count == 0:
            return jsonify({"error": "No lock found for this owner/resource"}), 404

        return jsonify({"message": "Lock released"})
    except Exception as e:
        app.logger.error(f"Error releasing lock: {e}")
        return jsonify({"error": str(e)}), 500

@app.post("/api/locking/bulk-update-with-retry")
def api_bulk_update_with_retry():
    db = get_db()
    movies = db["movies"]
    data = request.get_json() or {}
    updates = data.get("updates") or []

    results = []

    for u in updates:
        movie_id = u.get("movie_id")
        new_rating = _to_float(u.get("rating_avg"))
        version = int(u.get("version", 0))

        if not movie_id or not version:
            results.append({
                "movie_id": movie_id,
                "status": "error",
                "message": "Missing movie_id or version",
            })
            continue

        res = movies.update_one(
            {"_id": movie_id, "version": version},
            {"$set": {"rating_avg": new_rating}, "$inc": {"version": 1}},
        )

        if res.matched_count == 1:
            results.append({
                "movie_id": movie_id,
                "status": "success",
                "message": "Updated on first try",
            })
            continue

        current = movies.find_one({"_id": movie_id})
        if not current:
            results.append({
                "movie_id": movie_id,
                "status": "error",
                "message": "Movie not found",
            })
            continue

        current_version = current.get("version")
        res2 = movies.update_one(
            {"_id": movie_id, "version": current_version},
            {"$set": {"rating_avg": new_rating}, "$inc": {"version": 1}},
        )

        if res2.matched_count == 1:
            results.append({
                "movie_id": movie_id,
                "status": "success",
                "message": "Updated after retry",
            })
        else:
            results.append({
                "movie_id": movie_id,
                "status": "conflict",
                "message": "Conflict even after retry",
            })

    return jsonify({"results": results})

@app.post("/api/transactions/complex-with-locking")
def api_complex_tx_with_locking():
    db = get_db()
    client = get_client()
    data = request.get_json() or {}
    user_id = data.get("user_id")
    plan = data.get("plan", "basic")
    simulate_failure = bool(data.get("simulate_failure", False))

    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    lock_resource = f"subscription_{user_id}"
    lock_req = app.test_client().post(
        "/api/locking/acquire-lock",
        json={"resource_id": lock_resource, "timeout": 30},
    )
    if lock_req.status_code == 423:
        return jsonify({
            "error": "Subscription is locked by another process",
            "details": lock_req.json,
        }), 409

    payments = db["payments"]
    subs = db["subscriptions"]
    users_coll = db["users"]
    tx_log = db["transaction_log"]

    plan_prices = {
        "basic": 4.99,
        "premium": 9.99,
        "family": 14.99,
    }
    amount = plan_prices.get(plan, 4.99)

    log_steps = []

    session = client.start_session()
    try:
        with session.start_transaction():
            log_steps.append("1. Start transaction session")

            user_doc = users_coll.find_one({"_id": user_id}, session=session)
            if not user_doc:
                raise RuntimeError("User not found")

            log_steps.append("2. Read user with version (optimistic lock)")

            payment_id = str(uuid.uuid4())
            payments.insert_one(
                {
                    "_id": payment_id,
                    "user_id": user_id,
                    "amount_usd": amount,
                    "method": "card",
                    "plan": plan,
                    "status": "paid",
                    "paid_at": _now_iso(),
                },
                session=session,
            )
            log_steps.append("3. Create payment record")

            sub = subs.find_one({"user_id": user_id}, session=session)
            now = datetime.utcnow()
            end_date = (now + timedelta(days=30)).isoformat()

            if sub:
                subs.update_one(
                    {"_id": sub["_id"]},
                    {
                        "$set": {
                            "plan": plan,
                            "active": True,
                            "start_date": now.isoformat(),
                            "end_date": end_date,
                        }
                    },
                    session=session,
                )
            else:
                subs.insert_one(
                    {
                        "_id": str(uuid.uuid4()),
                        "user_id": user_id,
                        "plan": plan,
                        "active": True,
                        "start_date": now.isoformat(),
                        "end_date": end_date,
                        "version": 1,
                    },
                    session=session,
                )
            log_steps.append("4. Update subscription with version check")

            users_coll.update_one(
                {"_id": user_id},
                {
                    "$set": {
                        "subscription.plan": plan,
                        "subscription.status": "active",
                        "subscription.start_date": now.isoformat(),
                        "subscription.end_date": end_date,
                    },
                    "$inc": {"version": 1},
                },
                session=session,
            )
            log_steps.append("5. Update user version")

            tx_log.insert_one(
                {
                    "_id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "type": "subscription_renewal",
                    "status": "pending",
                    "timestamp": _now_iso(),
                    "details": f"Renew {plan} subscription for user {user_id}, amount ${amount}",
                },
                session=session,
            )
            log_steps.append("6. Log transaction")

            if simulate_failure:
                raise RuntimeError("Simulated failure to trigger rollback")

            tx_log.update_one(
                {"user_id": user_id, "type": "subscription_renewal", "status": "pending"},
                {"$set": {"status": "committed"}},
                session=session,
            )
            log_steps.append("7. Commit")

    except Exception as e:
        session.abort_transaction()
        error_msg = str(e)
        log_steps.append("Rollback due to error: " + error_msg)
        
        tx_log.insert_one({
            "_id": str(uuid.uuid4()),
            "user_id": user_id,
            "type": "subscription_renewal",
            "status": "failed",
            "timestamp": _now_iso(),
            "details": f"Failed to renew {plan} subscription for user {user_id}. Error: {error_msg}. Steps: {', '.join(log_steps)}"
        })
        
        app.test_client().post(
            "/api/locking/release-lock",
            json={"resource_id": lock_resource},
        )
        return jsonify({
            "error": "Transaction failed",
            "steps": log_steps,
            "exception": error_msg,
        }), 500
    finally:
        session.end_session()
        app.test_client().post(
            "/api/locking/release-lock",
            json={"resource_id": lock_resource},
        )

    return jsonify({
        "message": "Transaction with locking committed",
        "steps": log_steps,
        "user_id": user_id,
        "plan": plan,
        "amount_charged": amount,
    })

@app.get("/api/analytics/user-engagement")
def api_user_engagement():
    db = get_db()
    
    try:
        watch_history = db["watch_history"]
        ratings = db["ratings"]
        users_coll = db["users"]

        pipeline_watches = [
            {"$group": {"_id": "$user_id", "watches": {"$sum": 1}}},
        ]
        watches = {d["_id"]: d["watches"] for d in watch_history.aggregate(pipeline_watches)}

        pipeline_ratings = [
            {"$match": {"rating": {"$exists": True}}},
            {"$group": {"_id": "$user_id", "avg_rating": {"$avg": "$rating"}}},
        ]
        rating_map = {d["_id"]: d["avg_rating"] for d in ratings.aggregate(pipeline_ratings)}

        user_ids = set(watches.keys()) | set(rating_map.keys())
        result = []

        for uid in user_ids:
            user_doc = users_coll.find_one({"_id": uid}, {"profile.name": 1, "auth.username": 1})
            name = (
                user_doc.get("profile", {}).get("name")
                if user_doc
                else None
            ) or (
                user_doc.get("auth", {}).get("username")
                if user_doc
                else None
            ) or uid

            w = watches.get(uid, 0)
            avg_r = rating_map.get(uid, 0)
            engagement = float(w) * float(avg_r or 0)

            result.append({
                "user": name,
                "watches": w,
                "avg_rating": float(avg_r or 0),
                "engagement": engagement,
            })

        result.sort(key=lambda x: x["engagement"], reverse=True)
        return jsonify(result[:20])
    except Exception as e:
        app.logger.error(f"Error in user engagement: {e}")
        return jsonify([])

@app.post("/api/analytics/create-daily-activity-mv")
def api_create_daily_activity_mv():
    db = get_db()
    
    try:
        wh = db["watch_history"]
        mv = db["daily_activity_mv"]

        mv.drop()

        pipeline = [
            {"$match": {"watch_date": {"$exists": True}}},
            {
                "$group": {
                    "_id": "$watch_date",
                    "watch_count": {"$sum": 1},
                }
            },
            {"$sort": {"_id": 1}},
        ]
        docs = list(wh.aggregate(pipeline))
        if docs:
            for d in docs:
                d["date"] = d.pop("_id")
            mv.insert_many(docs)

        return jsonify({
            "message": "Materialized view created",
            "count": len(docs),
        })
    except Exception as e:
        app.logger.error(f"Error creating materialized view: {e}")
        return jsonify({
            "message": f"Error: {str(e)}",
            "count": 0,
        }), 500

@app.get("/api/analytics/query-daily-activity-mv")
def api_query_daily_activity_mv():
    db = get_db()
    
    try:
        mv = db["daily_activity_mv"]
        cursor = mv.find().sort("date", 1).limit(50)
        docs = []
        for d in cursor:
            d["_id"] = str(d["_id"])
            docs.append(d)
        return jsonify(docs)
    except Exception as e:
        app.logger.error(f"Error querying materialized view: {e}")
        return jsonify([])

@app.get("/api/profile/dashboard")
def api_profile_dashboard():
    db = get_db()
    user, role = get_current_user()
    if not user or user["_id"] == "guest":
        return jsonify({"error": "Not logged in"}), 401

    user_id = user["_id"]

    try:
        ratings_coll = db["ratings"]
        reviews_coll = db["reviews"]
        wh_coll = db["watch_history"]
        movies_coll = db["movies"]
        users_coll = db["users"]

        user_doc = users_coll.find_one({"_id": user_id})
        if not user_doc:
            return jsonify({"error": "User not found"}), 404

        ratings = list(
            ratings_coll.find(
                {"user_id": user_id},
                {"movie_id": 1, "rating": 1, "rated_at": 1},
            ).sort("rated_at", -1).limit(5)
        )
        for r in ratings:
            r["_id"] = str(r["_id"])

        reviews = list(
            reviews_coll.find(
                {"user_id": user_id},
                {"movie_id": 1, "review_text": 1, "created_at": 1},
            ).sort("created_at", -1).limit(5)
        )
        for rv in reviews:
            rv["_id"] = str(rv["_id"])

        history = list(
            wh_coll.find(
                {"user_id": user_id},
                {"movie_id": 1, "watch_date": 1, "progress_percent": 1},
            ).sort("watch_date", -1).limit(5)
        )
        for h in history:
            h["_id"] = str(h["_id"])

        watchlist_ids = user_doc.get("watchlist", [])
        watchlist_movies = []
        if watchlist_ids:
            cursor = movies_coll.find(
                {"_id": {"$in": watchlist_ids}},
                {"title": 1, "release_year": 1, "rating_avg": 1, "duration_min": 1},
            ).limit(5)
            for m in cursor:
                watchlist_movies.append({
                    "_id": str(m.get("_id")),
                    "title": m.get("title", ""),
                    "release_year": m.get("release_year"),
                    "rating_avg": _to_float(m.get("rating_avg")),
                    "duration_min": m.get("duration_min"),
                })

        return jsonify({
            "dashboard": {
                "ratings": ratings,
                "reviews": reviews,
                "watch_history": history,
                "watchlist": watchlist_movies,
            }
        })
    except Exception as e:
        app.logger.error(f"Error in profile dashboard: {e}")
        return jsonify({
            "dashboard": {
                "ratings": [],
                "reviews": [],
                "watch_history": [],
                "watchlist": [],
            }
        })

@app.post("/api/profile/update")
def api_profile_update():
    db = get_db()
    user, role = get_current_user()
    if not user or user["_id"] == "guest":
        return jsonify({"error": "Not logged in"}), 401

    user_id = user["_id"]
    data = request.get_json() or {}
    
    try:
        updates = {}
        if "name" in data:
            updates["profile.name"] = data["name"]
        if "country" in data:
            updates["profile.country"] = data["country"]
        if "bio" in data:
            updates["profile.bio"] = data["bio"]
        if "favorite_genres" in data:
            updates["preferences.favorite_genres"] = data["favorite_genres"]
        if "language" in data:
            updates["preferences.language"] = data["language"]

        if not updates:
            return jsonify({"message": "No changes"})

        result = db["users"].update_one(
            {"_id": user_id},
            {"$set": updates, "$inc": {"version": 1}},
        )

        if result.modified_count > 0:
            return jsonify({"message": "Profile updated"})
        else:
            return jsonify({"message": "No changes made"})
    except Exception as e:
        app.logger.error(f"Error updating profile: {e}")
        return jsonify({"error": str(e)}), 500

create_views()

if __name__ == "__main__":
    app.run(debug=True, port=5000)