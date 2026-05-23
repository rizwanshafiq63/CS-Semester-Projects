const dotenv = require("dotenv");
const bcrypt = require("bcryptjs");
const connectDB = require("../config/db");
const User = require("../models/User");
const TypingParagraph = require("../models/TypingParagraph");

dotenv.config();

const paragraphs = [
  // Easy (5)
  {
    text: "The quick brown fox jumps over the lazy dog and runs into the green forest.",
    difficulty: "easy",
  },
  {
    text: "Typing every day helps build speed, rhythm, and confidence in your keyboard skills.",
    difficulty: "easy",
  },
  {
    text: "Practice slowly at first and then increase your pace when your accuracy improves.",
    difficulty: "easy",
  },
  {
    text: "Good posture and relaxed hands can reduce mistakes and make typing feel smoother.",
    difficulty: "easy",
  },
  {
    text: "Small daily sessions are better than one long session because consistency builds habits.",
    difficulty: "easy",
  },
  // Medium (5)
  {
    text: "Modern web applications rely on clean architecture, reusable components, and consistent APIs for maintainable growth.",
    difficulty: "medium",
  },
  {
    text: "When measuring typing performance, you should balance speed with precision because mistakes reduce communication quality.",
    difficulty: "medium",
  },
  {
    text: "A focused typist keeps their eyes on the screen, uses all fingers, and avoids rushing difficult word patterns.",
    difficulty: "medium",
  },
  {
    text: "Learning keyboard shortcuts can improve productivity dramatically by reducing repetitive mouse movements during daily tasks.",
    difficulty: "medium",
  },
  {
    text: "Reliable systems include input validation, graceful error handling, and clear feedback for both users and administrators.",
    difficulty: "medium",
  },
  // Hard (5)
  {
    text: "Sustainable software engineering demands thoughtful trade-offs, especially when balancing performance, readability, security constraints, and long-term maintainability across distributed teams.",
    difficulty: "hard",
  },
  {
    text: "Effective typing under pressure requires cognitive discipline: you must preserve accuracy while processing punctuation, capitalization, and shifting sentence structure in real time.",
    difficulty: "hard",
  },
  {
    text: "Data-driven products evolve quickly, so developers must design robust APIs, enforce schema integrity, and continuously monitor edge-case behavior under unpredictable workloads.",
    difficulty: "hard",
  },
  {
    text: "As asynchronous systems scale, debugging race conditions becomes increasingly complex because failures may emerge only when timing interactions align in rare sequences.",
    difficulty: "hard",
  },
  {
    text: "Mastery in technical communication comes from clarity, precision, and context: each sentence should convey intent without ambiguity or unnecessary verbosity.",
    difficulty: "hard",
  },
];

const seed = async () => {
  try {
    await connectDB();

    const adminEmail = "admin@typemaster.com";
    const demoEmail = "demo@example.com";

    let admin = await User.findOne({ email: adminEmail });
    if (!admin) {
      admin = await User.create({
        name: "TypeMaster Admin",
        email: adminEmail,
        password: await bcrypt.hash("Admin1234", 10),
        role: "admin",
      });
      console.log("Admin user created.");
    } else {
      console.log("Admin user already exists.");
    }

    let demo = await User.findOne({ email: demoEmail });
    if (!demo) {
      await User.create({
        name: "Demo User",
        email: demoEmail,
        password: await bcrypt.hash("Demo1234", 10),
        role: "user",
      });
      console.log("Demo user created.");
    } else {
      console.log("Demo user already exists.");
    }

    await TypingParagraph.deleteMany({});
    const docs = paragraphs.map((p) => ({ ...p, isActive: true, createdBy: admin._id }));
    await TypingParagraph.insertMany(docs);
    console.log(`Seeded ${docs.length} typing paragraphs.`);

    process.exit(0);
  } catch (error) {
    console.error("Seed failed:", error);
    process.exit(1);
  }
};

seed();
