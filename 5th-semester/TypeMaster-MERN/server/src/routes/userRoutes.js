const express = require("express");
const { protect } = require("../middleware/authMiddleware");
const validateRequest = require("../middleware/validateRequest");
const { updateProfileValidator } = require("../validators/userValidators");
const { getProfile, updateProfile } = require("../controllers/userController");

const router = express.Router();

router.use(protect);

router.get("/profile", getProfile);
router.put("/profile", updateProfileValidator, validateRequest, updateProfile);

module.exports = router;
