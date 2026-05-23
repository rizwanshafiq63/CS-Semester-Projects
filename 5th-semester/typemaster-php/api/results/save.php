<?php
declare(strict_types=1);

require_once __DIR__ . '/../helpers/bootstrap.php';
require_once __DIR__ . '/../helpers/auth.php';

require_method(['POST']);
$user = require_auth();

$body = get_json_input();
$paragraphId = (int)($body['paragraph'] ?? 0);
$difficulty = strtolower(trim((string)($body['difficulty'] ?? '')));
$duration = (int)($body['duration'] ?? 0);
$wpm = (float)($body['wpm'] ?? 0);
$accuracy = (float)($body['accuracy'] ?? 0);
$mistakes = (int)($body['mistakes'] ?? 0);
$charsTyped = (int)($body['charsTyped'] ?? 0);
$timeTaken = (float)($body['timeTaken'] ?? 0);

if ($paragraphId <= 0) {
    send_error('Valid paragraph id is required', 422);
}
if (!in_array($difficulty, ['easy', 'medium', 'hard'], true)) {
    send_error('Difficulty must be easy, medium, or hard', 422);
}
if (!in_array($duration, [30, 60, 120], true)) {
    send_error('Duration must be 30, 60, or 120', 422);
}
if ($wpm < 0 || $accuracy < 0 || $accuracy > 100 || $mistakes < 0 || $charsTyped < 0 || $timeTaken < 0) {
    send_error('Invalid typing result values', 422);
}

$pdo = get_pdo();
$paragraphStmt = $pdo->prepare('SELECT id FROM typing_paragraphs WHERE id = :id AND is_active = 1 LIMIT 1');
$paragraphStmt->execute(['id' => $paragraphId]);
if (!$paragraphStmt->fetch()) {
    send_error('Paragraph is invalid or inactive', 400);
}

$insertStmt = $pdo->prepare(
    'INSERT INTO test_results (user_id, paragraph_id, difficulty, duration, wpm, accuracy, mistakes, chars_typed, time_taken)
     VALUES (:user_id, :paragraph_id, :difficulty, :duration, :wpm, :accuracy, :mistakes, :chars_typed, :time_taken)'
);
$insertStmt->execute([
    'user_id' => (int)$user['id'],
    'paragraph_id' => $paragraphId,
    'difficulty' => $difficulty,
    'duration' => $duration,
    'wpm' => $wpm,
    'accuracy' => $accuracy,
    'mistakes' => $mistakes,
    'chars_typed' => $charsTyped,
    'time_taken' => $timeTaken,
]);

$resultId = (int)$pdo->lastInsertId();
$resultStmt = $pdo->prepare('SELECT * FROM test_results WHERE id = :id');
$resultStmt->execute(['id' => $resultId]);
$result = $resultStmt->fetch();

send_success('Result saved', [
    'result' => normalize_result($result ?: []),
], 201);
