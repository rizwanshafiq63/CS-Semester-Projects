const express = require("express");
const { getParagraphs, getRandomParagraph } = require("../controllers/typingController");
const { difficultyQueryValidator } = require("../validators/typingValidators");
const validateRequest = require("../middleware/validateRequest");

const router = express.Router();

router.get("/paragraphs/random", difficultyQueryValidator, validateRequest, getRandomParagraph);
router.get("/paragraphs", difficultyQueryValidator, validateRequest, getParagraphs);

module.exports = router;
