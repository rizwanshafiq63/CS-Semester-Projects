const express = require("express");
const { protect } = require("../middleware/authMiddleware");
const validateRequest = require("../middleware/validateRequest");
const { createResultValidator } = require("../validators/resultValidators");
const { createResult, getMyResults, getMyStats } = require("../controllers/resultController");

const router = express.Router();

router.use(protect);

router.post("/", createResultValidator, validateRequest, createResult);
router.get("/me", getMyResults);
router.get("/me/stats", getMyStats);

module.exports = router;
