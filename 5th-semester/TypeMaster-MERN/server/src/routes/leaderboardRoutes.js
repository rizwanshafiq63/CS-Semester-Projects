const express = require("express");
const { protect } = require("../middleware/authMiddleware");
const validateRequest = require("../middleware/validateRequest");
const { leaderboardFilterValidator } = require("../validators/resultValidators");
const {
  getLeaderboard,
  getMyLeaderboardRank,
} = require("../controllers/leaderboardController");

const router = express.Router();

router.get("/", leaderboardFilterValidator, validateRequest, getLeaderboard);
router.get("/me", protect, getMyLeaderboardRank);

module.exports = router;
