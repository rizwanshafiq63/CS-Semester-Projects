const mongoose = require("mongoose");

const testResultSchema = new mongoose.Schema(
  {
    user: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      required: true,
    },
    paragraph: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "TypingParagraph",
      required: true,
    },
    difficulty: {
      type: String,
      enum: ["easy", "medium", "hard"],
      required: true,
    },
    duration: {
      type: Number,
      enum: [30, 60, 120],
      required: true,
    },
    wpm: {
      type: Number,
      required: true,
      min: 0,
    },
    accuracy: {
      type: Number,
      required: true,
      min: 0,
      max: 100,
    },
    mistakes: {
      type: Number,
      required: true,
      min: 0,
    },
    charsTyped: {
      type: Number,
      required: true,
      min: 0,
    },
    timeTaken: {
      type: Number,
      required: true,
      min: 0,
    },
  },
  { timestamps: true }
);

module.exports = mongoose.model("TestResult", testResultSchema);
