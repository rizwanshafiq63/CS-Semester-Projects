const TestResult = require("../models/TestResult");
const TypingParagraph = require("../models/TypingParagraph");
const { getUserStats } = require("../services/statsService");

const createResult = async (req, res, next) => {
  try {
    const { paragraph, difficulty, duration, wpm, accuracy, mistakes, charsTyped, timeTaken } =
      req.body;

    const paragraphDoc = await TypingParagraph.findOne({
      _id: paragraph,
      isActive: true,
    });
    if (!paragraphDoc) {
      return res
        .status(400)
        .json({ success: false, message: "Paragraph is invalid or inactive" });
    }

    const result = await TestResult.create({
      user: req.user._id,
      paragraph,
      difficulty,
      duration,
      wpm,
      accuracy,
      mistakes,
      charsTyped,
      timeTaken,
    });

    res.status(201).json({ success: true, message: "Result saved", result });
  } catch (error) {
    next(error);
  }
};

const getMyResults = async (req, res, next) => {
  try {
    const results = await TestResult.find({ user: req.user._id })
      .populate("paragraph", "text difficulty")
      .sort({ createdAt: -1 });

    res.status(200).json({ success: true, count: results.length, results });
  } catch (error) {
    next(error);
  }
};

const getMyStats = async (req, res, next) => {
  try {
    const stats = await getUserStats(req.user._id, 10);
    res.status(200).json({ success: true, ...stats });
  } catch (error) {
    next(error);
  }
};

module.exports = { createResult, getMyResults, getMyStats };
