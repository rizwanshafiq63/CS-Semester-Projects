const express = require("express");
const { protect } = require("../middleware/authMiddleware");
const { requireAdmin } = require("../middleware/roleMiddleware");
const validateRequest = require("../middleware/validateRequest");
const {
  createParagraphValidator,
  updateParagraphValidator,
  paragraphIdParamValidator,
} = require("../validators/adminValidators");
const {
  getUsers,
  getAllResults,
  getAllParagraphs,
  createParagraph,
  updateParagraph,
  disableParagraph,
} = require("../controllers/adminController");

const router = express.Router();

router.use(protect, requireAdmin);

router.get("/users", getUsers);
router.get("/results", getAllResults);
router.get("/paragraphs", getAllParagraphs);
router.post("/paragraphs", createParagraphValidator, validateRequest, createParagraph);
router.put("/paragraphs/:id", updateParagraphValidator, validateRequest, updateParagraph);
router.delete(
  "/paragraphs/:id",
  paragraphIdParamValidator,
  validateRequest,
  disableParagraph
);

module.exports = router;
