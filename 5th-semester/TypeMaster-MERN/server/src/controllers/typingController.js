const TypingParagraph = require("../models/TypingParagraph");

const getParagraphs = async (req, res, next) => {
  try {
    const filter = { isActive: true };
    if (req.query.difficulty) {
      filter.difficulty = req.query.difficulty;
    }

    const paragraphs = await TypingParagraph.find(filter)
      .select("_id text difficulty isActive createdAt")
      .sort({ createdAt: -1 });

    res.status(200).json({ success: true, count: paragraphs.length, paragraphs });
  } catch (error) {
    next(error);
  }
};

const getRandomParagraph = async (req, res, next) => {
  try {
    const match = { isActive: true };
    if (req.query.difficulty) {
      match.difficulty = req.query.difficulty;
    }

    const random = await TypingParagraph.aggregate([
      { $match: match },
      { $sample: { size: 1 } },
      { $project: { _id: 1, text: 1, difficulty: 1, isActive: 1, createdAt: 1 } },
    ]);

    if (!random.length) {
      return res
        .status(404)
        .json({ success: false, message: "No active paragraph found" });
    }

    res.status(200).json({ success: true, paragraph: random[0] });
  } catch (error) {
    next(error);
  }
};

module.exports = { getParagraphs, getRandomParagraph };
