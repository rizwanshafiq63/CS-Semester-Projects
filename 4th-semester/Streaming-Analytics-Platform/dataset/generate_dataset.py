# generate_dataset.py
import json
import random
from datetime import datetime, timedelta
from bson import ObjectId
import hashlib

# ================= CONFIGURATION =================
NUM_USERS = 300
NUM_MOVIES = 150
NUM_ACTORS = 200
NUM_DIRECTORS = 50
NUM_GENRES = 15
MAX_RATINGS_PER_USER = 30
MAX_REVIEWS_PER_USER = 10
MAX_WATCH_HISTORY_PER_USER = 50

# ================= HELPER FUNCTIONS =================
def generate_id(prefix):
    return f"{prefix}_{str(ObjectId())[:8]}"

def hash_password(password):
    return hashlib.sha256((password + "streaming_salt_2025").encode()).hexdigest()

def random_date(start_year=2018, end_year=2024):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return f"{year}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}Z"

def random_subscription_plan():
    plans = ["free", "basic", "premium", "family"]
    weights = [0.3, 0.25, 0.35, 0.1]  # 30% free, 25% basic, 35% premium, 10% family
    return random.choices(plans, weights=weights)[0]

# ================= GENERATE GENRES =================
def generate_genres():
    genres_list = [
        "Action", "Adventure", "Animation", "Comedy", "Crime",
        "Documentary", "Drama", "Family", "Fantasy", "History",
        "Horror", "Music", "Mystery", "Romance", "Sci-Fi",
        "Thriller", "War", "Western"
    ]
    genres = []
    for i, name in enumerate(random.sample(genres_list, NUM_GENRES)):
        genres.append({
            "_id": f"genre_{i+1:03d}",
            "name": name
        })
    return genres

# ================= GENERATE ACTORS =================
def generate_actors():
    first_names = ["James", "Emma", "Michael", "Sophia", "William", "Olivia", 
                   "Alexander", "Ava", "Daniel", "Mia", "Matthew", "Isabella",
                   "David", "Charlotte", "Joseph", "Amelia", "Christopher", "Harper",
                   "Andrew", "Evelyn", "Joshua", "Abigail", "Ryan", "Emily"]
    
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
                  "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez",
                  "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore"]
    
    nationalities = ["USA", "UK", "Canada", "Australia", "France", "Germany", 
                     "Italy", "Spain", "Japan", "South Korea", "India", "Mexico"]
    
    actors = []
    for i in range(NUM_ACTORS):
        birth_year = random.randint(1950, 2005)
        actors.append({
            "_id": f"actor_{i+1:03d}",
            "name": f"{random.choice(first_names)} {random.choice(last_names)}",
            "birth_year": birth_year,
            "nationality": random.choice(nationalities)
        })
    return actors

# ================= GENERATE DIRECTORS =================
def generate_directors():
    first_names = ["Steven", "Christopher", "Quentin", "Martin", "James",
                   "David", "Peter", "Ridley", "Tim", "Wes", "Guillermo",
                   "Denis", "Bong", "Greta", "Ava", "Jordan", "Ryan"]
    
    last_names = ["Spielberg", "Nolan", "Tarantino", "Scorsese", "Cameron",
                  "Fincher", "Jackson", "Scott", "Burton", "Anderson",
                  "del Toro", "Villeneuve", "Joon-ho", "Gerwig", "DuVernay",
                  "Peele", "Coogler"]
    
    directors = []
    for i in range(NUM_DIRECTORS):
        birth_year = random.randint(1940, 1985)
        directors.append({
            "_id": f"director_{i+1:03d}",
            "name": f"{random.choice(first_names)} {random.choice(last_names)}",
            "birth_year": birth_year,
            "nationality": random.choice(["USA", "UK", "Canada", "France", "Japan"])
        })
    return directors

# ================= GENERATE USERS =================
def generate_users(genres):
    countries = ["USA", "UK", "Canada", "Australia", "Germany", "France", 
                 "Japan", "South Korea", "India", "Brazil", "Mexico", 
                 "Spain", "Italy", "Pakistan", "UAE", "Singapore"]
    
    users = []
    
    # Create admin users
    admin_users = [
        {
            "_id": "user_admin001",
            "auth": {
                "username": "admin",
                "email": "admin@streaming.com",
                "password_hash": hash_password("admin123"),
                "role": "admin",
                "email_verified": True,
                "last_login": random_date(2024, 2024)
            },
            "profile": {
                "name": "System Administrator",
                "country": "USA",
                "join_date": "2020-01-01",
                "profile_picture": "https://ui-avatars.com/api/?name=Admin&background=0D8ABC&color=fff",
                "bio": "System administrator with full access"
            },
            "subscription": {
                "plan": "premium",
                "status": "active",
                "start_date": "2020-01-01",
                "end_date": "2030-01-01",
                "auto_renew": True
            },
            "preferences": {
                "favorite_genres": random.sample([g["name"] for g in genres], 3),
                "language": "en",
                "notifications": {"email": True, "push": True}
            },
            "statistics": {
                "total_watch_time": random.randint(5000, 15000),
                "movies_watched": random.randint(200, 500),
                "ratings_given": random.randint(150, 400),
                "reviews_written": random.randint(50, 100),
                "login_count": random.randint(100, 300)
            },
            "watchlist": [],
            "version": 1,
            "created_at": "2020-01-01T00:00:00Z",
            "active": True
        }
    ]
    
    # Create test users
    test_users = [
        {
            "_id": "user_test001",
            "auth": {
                "username": "testuser",
                "email": "test@streaming.com",
                "password_hash": hash_password("test123"),
                "role": "user",
                "email_verified": True,
                "last_login": random_date(2024, 2024)
            },
            "profile": {
                "name": "Test User",
                "country": "UK",
                "join_date": "2022-03-15",
                "profile_picture": "https://ui-avatars.com/api/?name=Test+User&background=10B981&color=fff",
                "bio": "Regular user for testing"
            },
            "subscription": {
                "plan": "premium",
                "status": "active",
                "start_date": "2022-03-15",
                "end_date": "2025-03-15",
                "auto_renew": True
            },
            "preferences": {
                "favorite_genres": ["Action", "Sci-Fi", "Drama"],
                "language": "en",
                "notifications": {"email": True, "push": False}
            },
            "statistics": {
                "total_watch_time": random.randint(1000, 3000),
                "movies_watched": random.randint(50, 150),
                "ratings_given": random.randint(30, 100),
                "reviews_written": random.randint(10, 30),
                "login_count": random.randint(50, 150)
            },
            "watchlist": [],
            "version": 1,
            "created_at": "2022-03-15T00:00:00Z",
            "active": True
        }
    ]
    
    # Generate regular users
    regular_users = []
    for i in range(NUM_USERS - 2):  # -2 for admin and test user
        user_id = f"user_{i+1:04d}"
        username = f"user{i+1}"
        plan = random_subscription_plan()
        join_date = random_date(2019, 2024)
        
        # Calculate end date for active subscriptions
        if plan != "free" and random.random() > 0.3:  # 70% active
            status = "active"
            start_date = random_date(int(join_date[:4]), 2024)
            end_date = (datetime.strptime(start_date[:10], "%Y-%m-%d") + 
                       timedelta(days=365)).strftime("%Y-%m-%d")
            auto_renew = random.choice([True, False])
        else:
            status = "free" if plan == "free" else random.choice(["cancelled", "expired"])
            start_date = random_date(int(join_date[:4]), 2024) if plan != "free" else None
            end_date = (datetime.strptime(start_date[:10], "%Y-%m-%d") + 
                       timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d") if start_date else None
            auto_renew = False
        
        user = {
            "_id": user_id,
            "auth": {
                "username": username,
                "email": f"{username}@example.com",
                "password_hash": hash_password("password123"),
                "role": "user",
                "email_verified": random.choice([True, True, True, False]),  # 75% verified
                "last_login": random_date(2024, 2024) if random.random() > 0.2 else None
            },
            "profile": {
                "name": f"User {i+1}",
                "country": random.choice(countries),
                "join_date": join_date[:10],
                "profile_picture": f"https://ui-avatars.com/api/?name=User+{i+1}&background=random&color=fff",
                "bio": random.choice([
                    "Movie enthusiast",
                    "Casual viewer",
                    "Film critic",
                    "Binge watcher",
                    "Documentary lover",
                    "Action movie fan",
                    ""
                ])
            },
            "subscription": {
                "plan": plan,
                "status": status,
                "start_date": start_date,
                "end_date": end_date,
                "auto_renew": auto_renew
            },
            "preferences": {
                "favorite_genres": random.sample([g["name"] for g in genres], random.randint(1, 4)),
                "language": random.choice(["en", "es", "fr", "de", "ja", "ko"]),
                "notifications": {
                    "email": random.choice([True, False]),
                    "push": random.choice([True, False])
                }
            },
            "statistics": {
                "total_watch_time": random.randint(0, 5000),
                "movies_watched": random.randint(0, 200),
                "ratings_given": random.randint(0, 150),
                "reviews_written": random.randint(0, 50),
                "login_count": random.randint(1, 100)
            },
            "watchlist": [],
            "version": 1,
            "created_at": join_date,
            "active": random.choice([True, True, True, False])  # 75% active
        }
        
        # Adjust statistics based on subscription
        if plan == "premium" or plan == "family":
            user["statistics"]["total_watch_time"] = random.randint(1000, 10000)
            user["statistics"]["movies_watched"] = random.randint(50, 300)
        elif plan == "basic":
            user["statistics"]["total_watch_time"] = random.randint(100, 2000)
            user["statistics"]["movies_watched"] = random.randint(10, 100)
        
        regular_users.append(user)
    
    return admin_users + test_users + regular_users

# ================= GENERATE MOVIES =================
def generate_movies(actors, directors, genres):
    movie_titles = [
        "The Last Horizon", "Echoes of Time", "Shadow Realm", "Neon Dreams",
        "Arctic Fury", "Digital Ghost", "Crimson Tide", "Solar Flare",
        "Midnight Run", "Golden Hour", "Silent Echo", "Frozen Heart",
        "Desert Rose", "Ocean's Whisper", "Mountain Peak", "City Lights",
        "Country Road", "Island Mystery", "Forest Spirit", "River Flow"
    ]
    
    prefixes = ["The", "A", "My", "Our", "Your", "Their", "His", "Her"]
    suffixes = ["Story", "Journey", "Adventure", "Mystery", "Secret", "Promise",
                "Legacy", "Dream", "Nightmare", "Hope", "Fear", "Love", "Hate"]
    
    movies = []
    for i in range(NUM_MOVIES):
        # Generate creative title
        if random.random() > 0.5:
            title = f"{random.choice(prefixes)} {random.choice(movie_titles)}"
        else:
            title = f"{random.choice(movie_titles)}: {random.choice(suffixes)}"
        
        release_year = random.randint(2000, 2024)
        duration = random.randint(75, 180)  # 1.25 to 3 hours
        
        # Select random actors (2-5 per movie)
        num_actors = random.randint(2, 5)
        movie_actors = random.sample([a["_id"] for a in actors], num_actors)
        
        # Select random genres (1-3 per movie)
        num_genres = random.randint(1, 3)
        movie_genres = random.sample([g["_id"] for g in genres], num_genres)
        
        # Select director
        director = random.choice([d["_id"] for d in directors])
        
        # Calculate rating (higher for newer/bigger movies)
        base_rating = random.uniform(3.0, 9.0)
        if release_year > 2020:
            base_rating += random.uniform(0.5, 1.5)
        if duration > 150:  # Epic movies
            base_rating += random.uniform(0.2, 0.8)
        
        rating_avg = round(min(10.0, max(1.0, base_rating)), 1)
        
        movies.append({
            "_id": f"movie_{i+1:03d}",
            "title": title,
            "release_year": release_year,
            "duration_min": duration,
            "rating_avg": rating_avg,
            "director_id": director,
            "actor_ids": movie_actors,
            "genre_ids": movie_genres,
            "rating_sum": 0,
            "rating_count": 0,
            "version": 1
        })
    
    return movies

# ================= GENERATE RATINGS =================
def generate_ratings(users, movies):
    ratings = []
    rating_id = 1
    
    for user in users:
        if user["auth"]["role"] == "admin":
            continue  # Admin doesn't rate movies
        
        user_id = user["_id"]
        num_ratings = random.randint(0, MAX_RATINGS_PER_USER)
        
        # Users with premium watch more
        if user["subscription"]["plan"] in ["premium", "family"]:
            num_ratings = random.randint(10, MAX_RATINGS_PER_USER)
        elif user["subscription"]["plan"] == "basic":
            num_ratings = random.randint(5, 15)
        
        rated_movies = random.sample(movies, min(num_ratings, len(movies)))
        
        for movie in rated_movies:
            # Rating influenced by subscription and movie quality
            base_rating = random.randint(1, 10)
            
            # Premium users tend to rate higher (happy customers)
            if user["subscription"]["plan"] in ["premium", "family"]:
                base_rating = random.randint(6, 10)
            
            # Adjust based on movie rating
            movie_quality = movie["rating_avg"] / 10
            adjusted_rating = int(base_rating * (0.7 + 0.6 * movie_quality))
            final_rating = max(1, min(10, adjusted_rating))
            
            ratings.append({
                "_id": f"rating_{rating_id:04d}",
                "user_id": user_id,
                "movie_id": movie["_id"],
                "rating": final_rating,
                "rated_at": random_date(2020, 2024)
            })
            rating_id += 1
    
    return ratings

# ================= GENERATE REVIEWS =================
def generate_reviews(users, ratings):
    reviews = []
    review_id = 1
    
    # Convert ratings to dict for easy lookup
    ratings_by_user_movie = {}
    for rating in ratings:
        key = f"{rating['user_id']}_{rating['movie_id']}"
        ratings_by_user_movie[key] = rating
    
    for user in users:
        if user["auth"]["role"] == "admin":
            continue
        
        user_id = user["_id"]
        num_reviews = random.randint(0, MAX_REVIEWS_PER_USER)
        
        # More active users write more reviews
        if user["statistics"]["movies_watched"] > 50:
            num_reviews = random.randint(5, MAX_REVIEWS_PER_USER)
        
        # Find movies this user rated
        user_ratings = [r for r in ratings if r["user_id"] == user_id]
        review_candidates = random.sample(user_ratings, min(num_reviews, len(user_ratings)))
        
        review_templates = [
            "Absolutely loved this movie! The cinematography was breathtaking.",
            "Good movie but could have been better. The plot felt rushed.",
            "One of the best films I've seen this year. Highly recommend!",
            "Disappointing. The trailer was better than the actual movie.",
            "A masterpiece! Every actor delivered an outstanding performance.",
            "Not my cup of tea. Found it quite boring to be honest.",
            "Great family movie. My kids loved it!",
            "The special effects were amazing but the story was weak.",
            "An emotional rollercoaster. Brought me to tears.",
            "Funny and entertaining. Perfect for a movie night.",
            "Too long and dragged out. Could have been 30 minutes shorter.",
            "A must-watch for all movie lovers!",
            "The director did an amazing job with this one.",
            "Expected more based on the hype. It was just okay.",
            "The soundtrack alone is worth watching the movie for."
        ]
        
        for rating in review_candidates:
            if random.random() > 0.3:  # 70% of ratings have reviews
                reviews.append({
                    "_id": f"review_{review_id:04d}",
                    "user_id": user_id,
                    "movie_id": rating["movie_id"],
                    "review_text": random.choice(review_templates),
                    "created_at": rating["rated_at"],
                    "helpful_votes": random.randint(0, 50)
                })
                review_id += 1
    
    return reviews

# ================= GENERATE WATCH HISTORY =================
def generate_watch_history(users, movies):
    watch_history = []
    history_id = 1
    
    for user in users:
        user_id = user["_id"]
        
        # Determine how many movies watched based on statistics
        movies_watched = user["statistics"]["movies_watched"]
        if movies_watched == 0:
            continue
        
        # Select movies to add to watch history
        num_to_watch = min(movies_watched, MAX_WATCH_HISTORY_PER_USER)
        watched_movies = random.sample(movies, min(num_to_watch, len(movies)))
        
        for movie in watched_movies:
            # More complete watches for better rated movies
            if movie["rating_avg"] > 7.0:
                progress = random.randint(90, 100)
            else:
                progress = random.randint(30, 100)
            
            # Premium users watch more completely
            if user["subscription"]["plan"] in ["premium", "family"]:
                progress = random.randint(80, 100)
            
            watch_date = random_date(2020, 2024)
            
            watch_history.append({
                "_id": f"watch_{history_id:05d}",
                "user_id": user_id,
                "movie_id": movie["_id"],
                "progress_percent": progress,
                "watch_date": watch_date
            })
            history_id += 1
    
    return watch_history

# ================= GENERATE RECOMMENDATIONS =================
def generate_recommendations(users, movies):
    recommendations = []
    
    for user in users:
        if user["auth"]["role"] == "admin":
            continue
        
        user_id = user["_id"]
        
        # Generate recommendations based on favorite genres
        favorite_genres = user["preferences"]["favorite_genres"]
        
        # Find movies in favorite genres
        recommended_movies = []
        for movie in movies:
            # Check if movie matches user's preferences
            if random.random() > 0.7:  # 30% chance
                recommended_movies.append(movie["_id"])
            
            if len(recommended_movies) >= 10:
                break
        
        if recommended_movies:
            recommendations.append({
                "_id": f"rec_{user_id}",
                "user_id": user_id,
                "recommended_movies": recommended_movies
            })
    
    return recommendations

# ================= GENERATE SUBSCRIPTIONS =================
def generate_subscriptions(users):
    subscriptions = []
    
    for user in users:
        sub = user["subscription"]
        if sub["plan"] == "free":
            continue
        
        subscriptions.append({
            "_id": f"sub_{user['_id']}",
            "user_id": user["_id"],
            "plan": sub["plan"],
            "active": sub["status"] == "active",
            "start_date": sub["start_date"],
            "end_date": sub["end_date"],
            "version": 1
        })
    
    return subscriptions

# ================= GENERATE PAYMENTS =================
def generate_payments(users):
    payments = []
    payment_id = 1
    
    plan_prices = {
        "basic": 4.99,
        "premium": 9.99,
        "family": 14.99
    }
    
    for user in users:
        user_id = user["_id"]
        plan = user["subscription"]["plan"]
        
        if plan == "free":
            continue
        
        # Generate 1-12 payments per user
        num_payments = random.randint(1, 12)
        price = plan_prices.get(plan, 9.99)
        
        payment_date = user["profile"]["join_date"] + "T00:00:00Z"
        base_date = datetime.strptime(payment_date[:10], "%Y-%m-%d")
        
        for i in range(num_payments):
            payment_date = (base_date + timedelta(days=i*30)).strftime("%Y-%m-%dT%H:%M:%SZ")
            
            payments.append({
                "_id": f"payment_{payment_id:04d}",
                "user_id": user_id,
                "amount_usd": price,
                "method": random.choice(["credit_card", "paypal", "google_pay", "apple_pay"]),
                "paid_at": payment_date,
                "status": random.choice(["completed", "completed", "completed", "failed", "refunded"]),
                "plan": plan
            })
            payment_id += 1
    
    return payments

# ================= GENERATE DEVICES =================
def generate_devices(users):
    devices = []
    device_id = 1
    
    device_types = ["smartphone", "tablet", "desktop", "smart_tv", "laptop"]
    os_versions = {
        "smartphone": ["iOS 16", "iOS 17", "Android 13", "Android 14"],
        "tablet": ["iPadOS 16", "iPadOS 17", "Android 13", "Android 14"],
        "desktop": ["Windows 11", "Windows 10", "macOS Ventura", "macOS Sonoma"],
        "smart_tv": ["webOS 22", "Tizen 7", "Android TV 11", "Roku OS 12"],
        "laptop": ["Windows 11", "macOS Sonoma", "Chrome OS", "Ubuntu 22.04"]
    }
    
    for user in users:
        user_id = user["_id"]
        
        # 1-3 devices per user
        num_devices = random.randint(1, 3)
        
        for _ in range(num_devices):
            device_type = random.choice(device_types)
            
            devices.append({
                "_id": f"device_{device_id:04d}",
                "user_id": user_id,
                "device_type": device_type,
                "os_version": random.choice(os_versions[device_type]),
                "last_active": random_date(2024, 2024)
            })
            device_id += 1
    
    return devices

# ================= MAIN GENERATION FUNCTION =================
def generate_complete_dataset():
    print("🎬 Generating Streaming Platform Dataset...")
    
    # Generate base collections
    print("1. Generating genres...")
    genres = generate_genres()
    
    print("2. Generating actors...")
    actors = generate_actors()
    
    print("3. Generating directors...")
    directors = generate_directors()
    
    print("4. Generating users (unified)...")
    users = generate_users(genres)
    
    print("5. Generating movies...")
    movies = generate_movies(actors, directors, genres)
    
    print("6. Generating ratings...")
    ratings = generate_ratings(users, movies)
    
    print("7. Generating reviews...")
    reviews = generate_reviews(users, ratings)
    
    print("8. Generating watch history...")
    watch_history = generate_watch_history(users, movies)
    
    print("9. Generating recommendations...")
    recommendations = generate_recommendations(users, movies)
    
    print("10. Generating subscriptions...")
    subscriptions = generate_subscriptions(users)
    
    print("11. Generating payments...")
    payments = generate_payments(users)
    
    print("12. Generating devices...")
    devices = generate_devices(users)
    
    # Update movies with actual rating statistics
    print("13. Calculating movie statistics...")
    for movie in movies:
        movie_ratings = [r for r in ratings if r["movie_id"] == movie["_id"]]
        if movie_ratings:
            rating_sum = sum(r["rating"] for r in movie_ratings)
            rating_count = len(movie_ratings)
            movie["rating_sum"] = rating_sum
            movie["rating_count"] = rating_count
            movie["rating_avg"] = round(rating_sum / rating_count, 1)
    
    # Update user watchlists
    print("14. Creating user watchlists...")
    for user in users:
        if user["auth"]["role"] != "admin" and random.random() > 0.3:
            num_watchlist = random.randint(1, 10)
            watchlist_movies = random.sample(movies, min(num_watchlist, len(movies)))
            user["watchlist"] = [m["_id"] for m in watchlist_movies]
    
    # Create transaction log for demonstrations
    print("15. Creating transaction log...")
    transaction_log = []
    for i in range(100):
        transaction_log.append({
            "_id": f"tx_{i+1:04d}",
            "type": random.choice(["subscription", "rating", "payment", "watch", "login"]),
            "user_id": random.choice([u["_id"] for u in users if u["auth"]["role"] != "admin"]),
            "timestamp": random_date(2024, 2024),
            "status": random.choice(["success", "failed", "pending"]),
            "details": f"Transaction {i+1}"
        })
    
    # Create resource_locks for pessimistic locking demo
    print("16. Creating resource locks...")
    resource_locks = []
    
    # Create indexes collection for performance demo
    print("17. Creating system indexes...")
    system_indexes = []
    
    # ================= SAVE ALL COLLECTIONS =================
    dataset = {
        "genres": genres,
        "actors": actors,
        "directors": directors,
        "users": users,  # Unified users collection
        "movies": movies,
        "ratings": ratings,
        "reviews": reviews,
        "watch_history": watch_history,
        "recommendations": recommendations,
        "subscriptions": subscriptions,
        "payments": payments,
        "devices": devices,
        "transaction_log": transaction_log,
        "resource_locks": resource_locks,
        "system_indexes": system_indexes
    }
    
    # Save to individual JSON files
    for collection_name, data in dataset.items():
        filename = f"{collection_name}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  ✅ Saved {len(data)} documents to {filename}")
    
    # Create a single import script
    create_import_script(dataset)
    
    print("\n" + "="*60)
    print("🎉 DATASET GENERATION COMPLETE!")
    print("="*60)
    print(f"Total Users: {len(users)} (including {sum(1 for u in users if u['auth']['role'] == 'admin')} admin)")
    print(f"Total Movies: {len(movies)}")
    print(f"Total Ratings: {len(ratings)}")
    print(f"Total Reviews: {len(reviews)}")
    print(f"Total Payments: {len(payments)}")
    print(f"Total Subscriptions: {len(subscriptions)}")
    print("\n✨ Dataset ready for MongoDB import!")
    
    return dataset

def create_import_script(dataset):
    """Create MongoDB import scripts"""
    
    # Create mongoimport commands
    commands = []
    for collection_name, data in dataset.items():
        filename = f"{collection_name}.json"
        command = f"mongoimport --uri \"mongodb+srv://streaming_admin:adb123@cluster0.36uks1x.mongodb.net/streaming\" --collection {collection_name} --file {filename} --jsonArray"
        commands.append(command)
    
    # Save to script file
    with open("import_to_mongodb.sh", "w") as f:
        f.write("#!/bin/bash\n\n")
        f.write("# MongoDB Import Script for Streaming Platform\n")
        f.write("# Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
        
        for command in commands:
            f.write(command + "\n")
    
    # Also create Python import script
    python_script = """import pymongo
import json
from bson import json_util

# Connect to MongoDB
try:
    client = pymongo.MongoClient("mongodb+srv://<username>:<password>@<cluster-url>/streaming?retryWrites=true&w=majority")
except Exception as e:
    print("MongoDB connection failed. Please replace the MongoClient URI on line 767 of generate_dataset.py with your actual credentials.")
    print(f"Error: {e}")
db = client["streaming"]

# Import all collections
collections = [
    "genres", "actors", "directors", "users", "movies", 
    "ratings", "reviews", "watch_history", "recommendations",
    "subscriptions", "payments", "devices", "transaction_log",
    "resource_locks", "system_indexes"
]

for collection_name in collections:
    print(f"Importing {collection_name}...")
    with open(f"{collection_name}.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if data:  # Only insert if there's data
        db[collection_name].insert_many(data)
        print(f"  ✅ Imported {len(data)} documents")
    else:
        print(f"  ⚠️  No data for {collection_name}")

print("\\n🎉 All collections imported successfully!")
print(f"Database: {db.name}")
print(f"Collections: {db.list_collection_names()}")
"""
    
    with open("import_to_mongodb.py", "w") as f:
        f.write(python_script)
    
    print("\n📦 Import scripts created:")
    print("  - import_to_mongodb.sh (mongoimport commands)")
    print("  - import_to_mongodb.py (Python script)")
    print("\nTo import, run:")
    print("  python import_to_mongodb.py")

# ================= EXECUTE =================
if __name__ == "__main__":
    print("="*60)
    print("STREAMING PLATFORM DATASET GENERATOR")
    print("Advanced Database Systems - Spring 2025")
    print("="*60)
    
    dataset = generate_complete_dataset()
    
    # Show sample data
    print("\n📊 SAMPLE DATA:")
    print("-" * 40)
    
    # Show sample user
    sample_user = dataset["users"][0]
    print(f"👤 Sample User: {sample_user['auth']['username']}")
    print(f"   Role: {sample_user['auth']['role']}")
    print(f"   Plan: {sample_user['subscription']['plan']}")
    print(f"   Country: {sample_user['profile']['country']}")
    print(f"   Watchlist: {len(sample_user['watchlist'])} movies")
    
    # Show sample movie
    sample_movie = dataset["movies"][0]
    print(f"\n🎬 Sample Movie: {sample_movie['title']}")
    print(f"   Year: {sample_movie['release_year']}")
    print(f"   Rating: {sample_movie['rating_avg']}/10")
    print(f"   Duration: {sample_movie['duration_min']} mins")
    
    print("\n🚀 Ready for implementation!")