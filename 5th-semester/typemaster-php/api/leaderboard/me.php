<?php
declare(strict_types=1);

require_once __DIR__ . '/../helpers/bootstrap.php';
require_once __DIR__ . '/../helpers/auth.php';

require_method(['GET']);
$user = require_auth();

$pdo = get_pdo();
$stmt = $pdo->query('SELECT tr.user_id, u.name, tr.wpm, tr.accuracy
                     FROM test_results tr
                     INNER JOIN users u ON u.id = tr.user_id
                     ORDER BY tr.user_id ASC, tr.wpm DESC, tr.accuracy DESC, tr.created_at ASC');
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

$leaderboard = array_values($byUser);
usort($leaderboard, static function (array $a, array $b): int {
    if ($a['bestWpm'] !== $b['bestWpm']) {
        return $b['bestWpm'] <=> $a['bestWpm'];
    }
    if ($a['bestAccuracy'] !== $b['bestAccuracy']) {
        return $b['bestAccuracy'] <=> $a['bestAccuracy'];
    }
    return strcmp($a['name'], $b['name']);
});
foreach ($leaderboard as $index => $entry) {
    $leaderboard[$index]['rank'] = $index + 1;
}

$me = null;
foreach ($leaderboard as $entry) {
    if ((int)$entry['userId'] === (int)$user['id']) {
        $me = $entry;
    }
}

if ($me === null) {
    send_success('No test results yet for current user', [
        'rank' => null,
    ]);
}

send_success('Current leaderboard rank fetched', [
    'rank' => $me['rank'],
    'bestWpm' => $me['bestWpm'],
    'bestAccuracy' => $me['bestAccuracy'],
    'testsTaken' => $me['testsTaken'],
]);
