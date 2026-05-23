<?php
declare(strict_types=1);

require_once __DIR__ . '/../helpers/bootstrap.php';
require_once __DIR__ . '/../helpers/auth.php';

require_method(['GET']);
$user = require_auth();

$pdo = get_pdo();
$stmt = $pdo->prepare('SELECT id, user_id, paragraph_id, difficulty, duration, wpm, accuracy, mistakes, chars_typed, time_taken, created_at
                       FROM test_results
                       WHERE user_id = :user_id
                       ORDER BY created_at DESC');
$stmt->execute(['user_id' => (int)$user['id']]);
$rows = $stmt->fetchAll();

$results = array_map(static fn(array $row): array => normalize_result($row), $rows);

send_success('Test history fetched', [
    'count' => count($results),
    'results' => $results,
]);
