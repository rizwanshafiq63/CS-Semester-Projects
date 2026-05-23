const TestResult = require("../models/TestResult");

const buildLeaderboardPipeline = (filters = {}) => {
  const match = {};
  if (filters.difficulty) match.difficulty = filters.difficulty;
  if (filters.duration) match.duration = Number(filters.duration);
  if (filters.createdAt) match.createdAt = filters.createdAt;

  return [
    { $match: match },
    { $sort: { wpm: -1, accuracy: -1, createdAt: 1 } },
    {
      $group: {
        _id: "$user",
        bestWpm: { $first: "$wpm" },
        bestAccuracy: { $first: "$accuracy" },
        testsTaken: { $sum: 1 },
      },
    },
    {
      $lookup: {
        from: "users",
        localField: "_id",
        foreignField: "_id",
        as: "user",
      },
    },
    { $unwind: "$user" },
    {
      $project: {
        _id: 0,
        userId: "$user._id",
        name: "$user.name",
        bestWpm: 1,
        bestAccuracy: 1,
        testsTaken: 1,
      },
    },
    { $sort: { bestWpm: -1, bestAccuracy: -1, name: 1 } },
  ];
};

const getLeaderboard = async (req, res, next) => {
  try {
    const now = new Date();
    const timeFilter = req.query.time || "all";
    let createdAt;

    if (timeFilter === "today") {
      const startOfDay = new Date(now);
      startOfDay.setHours(0, 0, 0, 0);
      createdAt = { $gte: startOfDay };
    } else if (timeFilter === "week") {
      const weekAgo = new Date(now);
      weekAgo.setDate(weekAgo.getDate() - 7);
      createdAt = { $gte: weekAgo };
    } else if (timeFilter === "month") {
      const monthAgo = new Date(now);
      monthAgo.setDate(monthAgo.getDate() - 30);
      createdAt = { $gte: monthAgo };
    }

    const entries = await TestResult.aggregate(
      buildLeaderboardPipeline({
        difficulty: req.query.difficulty,
        duration: req.query.duration,
        createdAt,
      })
    );

    const leaderboard = entries.map((entry, index) => ({
      rank: index + 1,
      name: entry.name,
      bestWpm: entry.bestWpm,
      bestAccuracy: Number(entry.bestAccuracy.toFixed(2)),
      testsTaken: entry.testsTaken,
    }));

    res.status(200).json({ success: true, count: leaderboard.length, leaderboard });
  } catch (error) {
    next(error);
  }
};

const getMyLeaderboardRank = async (req, res, next) => {
  try {
    const entries = await TestResult.aggregate(buildLeaderboardPipeline({}));
    const meIndex = entries.findIndex(
      (entry) => String(entry.userId) === String(req.user._id)
    );

    if (meIndex === -1) {
      return res.status(200).json({
        success: true,
        rank: null,
        message: "No test results yet for current user",
      });
    }

    const me = entries[meIndex];
    res.status(200).json({
      success: true,
      rank: meIndex + 1,
      bestWpm: me.bestWpm,
      bestAccuracy: Number(me.bestAccuracy.toFixed(2)),
      testsTaken: me.testsTaken,
    });
  } catch (error) {
    next(error);
  }
};

module.exports = { getLeaderboard, getMyLeaderboardRank };
