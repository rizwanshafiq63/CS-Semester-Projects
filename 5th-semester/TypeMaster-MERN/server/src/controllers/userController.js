const User = require("../models/User");
const { getUserStats } = require("../services/statsService");

const getProfile = async (req, res, next) => {
  try {
    const user = await User.findById(req.user._id).select("-password");
    const stats = await getUserStats(req.user._id, 10);

    res.status(200).json({
      success: true,
      user,
      stats: {
        totalTests: stats.totalTests,
        averageWpm: stats.averageWpm,
        bestWpm: stats.bestWpm,
        averageAccuracy: stats.averageAccuracy,
        totalTime: stats.totalTime,
        improvementPercentage: stats.improvementPercentage,
      },
    });
  } catch (error) {
    next(error);
  }
};

const updateProfile = async (req, res, next) => {
  try {
    const { name } = req.body;
    const updated = await User.findByIdAndUpdate(
      req.user._id,
      { name: name.trim() },
      { new: true, runValidators: true }
    ).select("-password");

    res.status(200).json({
      success: true,
      message: "Profile updated",
      user: updated,
    });
  } catch (error) {
    next(error);
  }
};

module.exports = { getProfile, updateProfile };
