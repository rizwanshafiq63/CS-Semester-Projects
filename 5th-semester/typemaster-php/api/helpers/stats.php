<?php
declare(strict_types=1);

require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/bootstrap.php';

function compute_improvement_percentage(array $results): float
{
    if (count($results) < 2) {
        return 0.0;
    }

    usort($results, static fn(array $a, array $b): int => strcmp((string)$a['created_at'], (string)$b['created_at']));
    $windowSize = min(5, intdiv(count($results), 2));
    if ($windowSize === 0) {
        return 0.0;
    }

    $firstWindow = array_slice($results, 0, $windowSize);
    $lastWindow = array_slice($results, -$windowSize);

    $firstAvg = array_sum(array_map(static fn(array $r): float => (float)$r['wpm'], $firstWindow)) / count($firstWindow);
    $lastAvg = array_sum(array_map(static fn(array $r): float => (float)$r['wpm'], $lastWindow)) / count($lastWindow);

    if ($firstAvg <= 0) {
        return 0.0;
    }

    return round((($lastAvg - $firstAvg) / $firstAvg) * 100, 2);
}

function get_user_stats(int $userId, int $recentLimit = 10): array
{
    $pdo = get_pdo();
    $stmt = $pdo->prepare('SELECT id, user_id, paragraph_id, difficulty, duration, wpm, accuracy, mistakes, chars_typed, time_taken, created_at
                           FROM test_results WHERE user_id = :user_id ORDER BY created_at DESC');
    $stmt->execute(['user_id' => $userId]);
    $results = $stmt->fetchAll();

    $totalTests = count($results);
    $averageWpm = 0.0;
    $bestWpm = 0.0;
    $averageAccuracy = 0.0;
    $totalTime = 0.0;

    if ($totalTests > 0) {
        $wpmValues = array_map(static fn(array $r): float => (float)$r['wpm'], $results);
        $accuracyValues = array_map(static fn(array $r): float => (float)$r['accuracy'], $results);
        $timeValues = array_map(static fn(array $r): float => (float)$r['time_taken'], $results);

        $averageWpm = round(array_sum($wpmValues) / $totalTests, 2);
        $bestWpm = max($wpmValues);
        $averageAccuracy = round(array_sum($accuracyValues) / $totalTests, 2);
        $totalTime = array_sum($timeValues);
    }

    $recent = array_slice($results, 0, $recentLimit);
    $recentTests = array_map(static fn(array $r): array => normalize_result($r), $recent);

    return [
        'totalTests' => $totalTests,
        'averageWpm' => $averageWpm,
        'bestWpm' => $bestWpm,
        'averageAccuracy' => $averageAccuracy,
        'totalTime' => $totalTime,
        'improvementPercentage' => compute_improvement_percentage($results),
        'recentTests' => $recentTests,
    ];
}
