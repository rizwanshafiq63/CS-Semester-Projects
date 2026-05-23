const { body, query } = require("express-validator");

const createResultValidator = [
  body("paragraph").isMongoId().withMessage("Valid paragraph id is required"),
  body("difficulty")
    .isIn(["easy", "medium", "hard"])
    .withMessage("Difficulty must be easy, medium, or hard"),
  body("duration")
    .isInt({ min: 30, max: 120 })
    .custom((value) => [30, 60, 120].includes(Number(value)))
    .withMessage("Duration must be 30, 60, or 120"),
  body("wpm").isFloat({ min: 0 }).withMessage("WPM must be >= 0"),
  body("accuracy")
    .isFloat({ min: 0, max: 100 })
    .withMessage("Accuracy must be between 0 and 100"),
  body("mistakes").isInt({ min: 0 }).withMessage("Mistakes must be >= 0"),
  body("charsTyped").isInt({ min: 0 }).withMessage("charsTyped must be >= 0"),
  body("timeTaken").isFloat({ min: 0 }).withMessage("timeTaken must be >= 0"),
];

const leaderboardFilterValidator = [
  query("difficulty")
    .optional()
    .isIn(["easy", "medium", "hard"])
    .withMessage("Difficulty must be easy, medium, or hard"),
  query("duration")
    .optional()
    .isInt()
    .custom((value) => [30, 60, 120].includes(Number(value)))
    .withMessage("Duration must be 30, 60, or 120"),
  query("time")
    .optional()
    .isIn(["all", "today", "week", "month"])
    .withMessage("Time must be all, today, week, or month"),
];

module.exports = { createResultValidator, leaderboardFilterValidator };
