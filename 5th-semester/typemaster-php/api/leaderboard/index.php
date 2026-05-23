<?php
declare(strict_types=1);

require_once __DIR__ . '/../helpers/bootstrap.php';

require_method(['GET']);

$difficulty = strtolower(trim((string)($_GET['difficulty'] ?? '')));
$duration = (int)($_GET['duration'] ?? 0);
$time = strtolower(trim((string)($_GET['time'] ?? 'all')));
$page = max(1, (int)($_GET['page'] ?? 1));
$limit = max(1, min(100, (int)($_GET['limit'] ?? 100)));

if ($difficulty !== '' && !in_array($difficulty, ['easy', 'medium', 'hard'], true)) {
    send_error('Difficulty must be easy, medium, or hard', 422);
}
if ($duration !== 0 && !in_array($duration, [30, 60, 120], true)) {
    send_error('Duration must be 30, 60, or 120', 422);
}
if (!in_array($time, ['all', 'today', 'week', 'month'], true)) {
    send_error('Time must be all, today, week, or month', 422);
}

$params = [];
$whereParts = ['1=1'];

if ($difficulty !== '') {
    $whereParts[] = 'tr.difficulty = :difficulty';
    $params['difficulty'] = $difficulty;
}
if ($duration !== 0) {
    $whereParts[] = 'tr.duration = :duration';
    $params['duration'] = $duration;
}
if ($time !== 'all') {
    if ($time === 'today') {
        $whereParts[] = 'tr.created_at >= CURDATE()';
    } elseif ($time === 'week') {
        $whereParts[] = 'tr.created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)';
    } else {
        $whereParts[] = 'tr.created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)';
    }
}

$whereSql = implode(' AND ', $whereParts);
$pdo = get_pdo();

$sql = "SELECT tr.user_id, u.name, tr.wpm, tr.accuracy
        FROM test_results tr
        INNER JOIN users u ON u.id = tr.user_id
        WHERE {$whereSql}
        ORDER BY tr.user_id ASC, tr.wpm DESC, tr.accuracy DESC, tr.created_at ASC";

$stmt = $pdo->prepare($sql);
$stmt->execute($params);
$rows = $stmt->fetchAll();

$byUser = [];
foreach ($rows as $row) {
    $userId = (int)$row['user_id'];
    if (!isset($byUser[$userId])) {
        $byUser[$userId] = [
            'userId' => $userId,
            'name' => $row['name'],
            'bestWpm' => (float)$row['wpm'],
            'bestAccuracy' => round((float)$row['accuracy'], 2),
            'testsTaken' => 0,
        ];
    }
    $byUser[$userId]['testsTaken']++;
}

$all = array_values($byUser);
usort($all, static function (array $a, array $b): int {
    if ($a['bestWpm'] !== $b['bestWpm']) {
        return $b['bestWpm'] <=> $a['bestWpm'];
    }
    if ($a['bestAccuracy'] !== $b['bestAccuracy']) {
        return $b['bestAccuracy'] <=> $a['bestAccuracy'];
    }
    return strcmp($a['name'], $b['name']);
});
foreach ($all as $index => $entry) {
    $all[$index]['rank'] = $index + 1;
}

$total = count($all);
$offset = ($page - 1) * $limit;
$leaderboard = array_slice($all, $offset, $limit);

send_success('Leaderboard fetched', [
    'count' => count($leaderboard),
    'total' => $total,
    'page' => $page,
    'limit' => $limit,
    'leaderboard' => $leaderboard,
]);
