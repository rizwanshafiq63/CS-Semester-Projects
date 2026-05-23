const requireAdmin = (req, res, next) => {
  if (!req.user || req.user.role !== "admin") {
    res.status(403);
    return next(new Error("Access denied: admin only"));
  }
  next();
};

module.exports = { requireAdmin };
