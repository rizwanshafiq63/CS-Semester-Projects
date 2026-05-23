const { query } = require("express-validator");

const difficultyQueryValidator = [
  query("difficulty")
    .optional()
    .isIn(["easy", "medium", "hard"])
    .withMessage("Difficulty must be easy, medium, or hard"),
];

module.exports = { difficultyQueryValidator };
