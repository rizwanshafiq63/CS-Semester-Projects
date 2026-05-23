<?php
declare(strict_types=1);

require_once __DIR__ . '/../helpers/bootstrap.php';
require_once __DIR__ . '/../helpers/auth.php';

require_method(['POST', 'PUT']);
require_admin();
$body = get_json_input();

$id = (int)($body['id'] ?? ($_GET['id'] ?? 0));
if ($id <= 0) {
    send_error('Invalid paragraph id', 422);
}

$updates = [];
$params = ['id' => $id];

if (array_key_exists('text', $body)) {
    $text = trim((string)$body['text']);
    if ($text === '') {
        send_error('Text cannot be empty when provided', 422);
    }
    $updates[] = 'text = :text';
    $params['text'] = $text;
}

if (array_key_exists('difficulty', $body)) {
    $difficulty = strtolower(trim((string)$body['difficulty']));
    if (!in_array($difficulty, ['easy', 'medium', 'hard'], true)) {
        send_error('Difficulty must be easy, medium, or hard', 422);
    }
    $updates[] = 'difficulty = :difficulty';
    $params['difficulty'] = $difficulty;
}

if (array_key_exists('isActive', $body)) {
    $updates[] = 'is_active = :is_active';
    $params['is_active'] = $body['isActive'] ? 1 : 0;
}

if (empty($updates)) {
    send_error('No valid fields to update', 422);
}

$updates[] = 'updated_at = NOW()';
$sql = 'UPDATE typing_paragraphs SET ' . implode(', ', $updates) . ' WHERE id = :id';

$pdo = get_pdo();
$stmt = $pdo->prepare($sql);
$stmt->execute($params);

if ($stmt->rowCount() === 0) {
    $existsStmt = $pdo->prepare('SELECT id FROM typing_paragraphs WHERE id = :id');
    $existsStmt->execute(['id' => $id]);
    if (!$existsStmt->fetch()) {
        send_error('Paragraph not found', 404);
    }
}

$itemStmt = $pdo->prepare('SELECT id, text, difficulty, is_active, created_at, updated_at FROM typing_paragraphs WHERE id = :id');
$itemStmt->execute(['id' => $id]);
$paragraph = $itemStmt->fetch();

send_success('Paragraph updated', [
    'paragraph' => normalize_paragraph($paragraph ?: []),
]);
