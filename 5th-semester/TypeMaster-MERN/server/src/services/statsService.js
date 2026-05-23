const TestResult = require("../models/TestResult");

const computeImprovementPercentage = (results) => {
  if (!results || results.length < 2) return 0;

  const chronological = [...results].sort(
    (a, b) => new Date(a.createdAt) - new Date(b.createdAt)
  );
  const windowSize = Math.min(5, Math.floor(chronological.length / 2));
  if (windowSize === 0) return 0;

  const firstWindow = chronological.slice(0, windowSize);
  const lastWindow = chronological.slice(-windowSize);

  const firstAvg =
    firstWindow.reduce((sum, item) => sum + item.wpm, 0) / firstWindow.length;
  const lastAvg =
    lastWindow.reduce((sum, item) => sum + item.wpm, 0) / lastWindow.length;

  if (firstAvg === 0) return 0;
  return Number((((lastAvg - firstAvg) / firstAvg) * 100).toFixed(2));
};

const getUserStats = async (userId, recentLimit = 10) => {
  const results = await TestResult.find({ user: userId }).sort({ createdAt: -1 });

  const totalTests = results.length;
  const averageWpm = totalTests
    ? Number((results.reduce((sum, item) => sum + item.wpm, 0) / totalTests).toFixed(2))
    : 0;
  const bestWpm = totalTests ? Math.max(...results.map((item) => item.wpm)) : 0;
  const averageAccuracy = totalTests
    ? Number(
        (
          results.reduce((sum, item) => sum + item.accuracy, 0) / totalTests
        ).toFixed(2)
      )
    : 0;
  const totalTime = results.reduce((sum, item) => sum + item.timeTaken, 0);
  const improvementPercentage = computeImprovementPercentage(results);

  return {
    totalTests,
    averageWpm,
    bestWpm,
    averageAccuracy,
    totalTime,
    improvementPercentage,
    recentTests: results.slice(0, recentLimit),
  };
};

module.exports = { getUserStats };
