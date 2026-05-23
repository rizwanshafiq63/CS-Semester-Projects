const User = require("../models/User");
const TestResult = require("../models/TestResult");
const TypingParagraph = require("../models/TypingParagraph");

const getUsers = async (req, res, next) => {
  try {
    const users = await User.find({})
      .select("-password")
      .sort({ createdAt: -1 });
    res.status(200).json({ success: true, count: users.length, users });
  } catch (error) {
    next(error);
  }
};

const getAllResults = async (req, res, next) => {
  try {
    const results = await TestResult.find({})
      .populate("user", "name email role")
      .populate("paragraph", "text difficulty isActive")
      .sort({ createdAt: -1 });
    res.status(200).json({ success: true, count: results.length, results });
  } catch (error) {
    next(error);
  }
};

const getAllParagraphs = async (req, res, next) => {
  try {
    const paragraphs = await TypingParagraph.find({})
      .populate("createdBy", "name email")
      .sort({ createdAt: -1 });
    res.status(200).json({ success: true, count: paragraphs.length, paragraphs });
  } catch (error) {
    next(error);
  }
};

const createParagraph = async (req, res, next) => {
  try {
    const { text, difficulty } = req.body;
    const paragraph = await TypingParagraph.create({
      text: text.trim(),
      difficulty,
      isActive: true,
      createdBy: req.user._id,
    });
    res.status(201).json({ success: true, message: "Paragraph created", paragraph });
  } catch (error) {
    next(error);
  }
};

const updateParagraph = async (req, res, next) => {
  try {
    const updates = {};
    if (req.body.text !== undefined) updates.text = req.body.text.trim();
    if (req.body.difficulty !== undefined) updates.difficulty = req.body.difficulty;
    if (req.body.isActive !== undefined) updates.isActive = req.body.isActive;

    const paragraph = await TypingParagraph.findByIdAndUpdate(req.params.id, updates, {
      new: true,
      runValidators: true,
    });

    if (!paragraph) {
      return res.status(404).json({ success: false, message: "Paragraph not found" });
    }

    res.status(200).json({ success: true, message: "Paragraph updated", paragraph });
  } catch (error) {
    next(error);
  }
};

const disableParagraph = async (req, res, next) => {
  try {
    const paragraph = await TypingParagraph.findByIdAndUpdate(
      req.params.id,
      { isActive: false },
      { new: true }
    );

    if (!paragraph) {
      return res.status(404).json({ success: false, message: "Paragraph not found" });
    }

    res
      .status(200)
      .json({ success: true, message: "Paragraph disabled", paragraph });
  } catch (error) {
    next(error);
  }
};

module.exports = {
  getUsers,
  getAllResults,
  getAllParagraphs,
  createParagraph,
  updateParagraph,
  disableParagraph,
};
