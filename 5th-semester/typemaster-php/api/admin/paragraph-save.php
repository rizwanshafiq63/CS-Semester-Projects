<?php
declare(strict_types=1);

require_once __DIR__ . '/../helpers/bootstrap.php';
require_once __DIR__ . '/../helpers/auth.php';

require_method(['POST']);
$user = require_admin();
$body = get_json_input();

$text = trim((string)($body['text'] ?? ''));
$difficulty = strtolower(trim((string)($body['difficulty'] ?? '')));

if ($text === '') {
    send_error('Paragraph text is required', 422);
}
if (!in_array($difficulty, ['easy', 'medium', 'hard'], true)) {
    send_error('Difficulty must be easy, medium, or hard', 422);
}

$pdo = get_pdo();
$stmt = $pdo->prepare('INSERT INTO typing_paragraphs (text, difficulty, is_active, created_by) VALUES (:text, :difficulty, 1, :created_by)');
$stmt->execute([
    'text' => $text,
    'difficulty' => $difficulty,
    'created_by' => (int)$user['id'],
]);

$id = (int)$pdo->lastInsertId();
$itemStmt = $pdo->prepare('SELECT id, text, difficulty, is_active, created_at, updated_at FROM typing_paragraphs WHERE id = :id');
$itemStmt->execute(['id' => $id]);
$paragraph = $itemStmt->fetch();

send_success('Paragraph created', [
    'paragraph' => normalize_paragraph($paragraph ?: []),
], 201);
