const { body, param } = require("express-validator");

const createParagraphValidator = [
  body("text").trim().notEmpty().withMessage("Paragraph text is required"),
  body("difficulty")
    .isIn(["easy", "medium", "hard"])
    .withMessage("Difficulty must be easy, medium, or hard"),
];

const updateParagraphValidator = [
  param("id").isMongoId().withMessage("Invalid paragraph id"),
  body("text")
    .optional()
    .trim()
    .notEmpty()
    .withMessage("Text cannot be empty when provided"),
  body("difficulty")
    .optional()
    .isIn(["easy", "medium", "hard"])
    .withMessage("Difficulty must be easy, medium, or hard"),
  body("isActive")
    .optional()
    .isBoolean()
    .withMessage("isActive must be true or false"),
];

const paragraphIdParamValidator = [
  param("id").isMongoId().withMessage("Invalid paragraph id"),
];

module.exports = {
  createParagraphValidator,
  updateParagraphValidator,
  paragraphIdParamValidator,
};
