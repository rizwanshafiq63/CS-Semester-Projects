<?php
declare(strict_types=1);

require_once __DIR__ . '/../helpers/bootstrap.php';
require_once __DIR__ . '/../helpers/auth.php';

require_method(['POST', 'DELETE']);
require_admin();

$body = get_json_input();
$id = (int)($body['id'] ?? ($_GET['id'] ?? 0));
if ($id <= 0) {
    send_error('Invalid paragraph id', 422);
}

$pdo = get_pdo();
$stmt = $pdo->prepare('UPDATE typing_paragraphs SET is_active = 0, updated_at = NOW() WHERE id = :id');
$stmt->execute(['id' => $id]);

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

send_success('Paragraph disabled', [
    'paragraph' => normalize_paragraph($paragraph ?: []),
]);
