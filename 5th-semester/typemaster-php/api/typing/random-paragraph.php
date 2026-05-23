<?php
declare(strict_types=1);

require_once __DIR__ . '/../helpers/bootstrap.php';

require_method(['GET']);

$difficulty = strtolower(trim((string)($_GET['difficulty'] ?? '')));
if ($difficulty !== '' && !in_array($difficulty, ['easy', 'medium', 'hard'], true)) {
    send_error('Difficulty must be easy, medium, or hard', 422);
}

$pdo = get_pdo();
$sql = 'SELECT id, text, difficulty, is_active, created_at, updated_at
        FROM typing_paragraphs
        WHERE is_active = 1';
$params = [];

if ($difficulty !== '') {
    $sql .= ' AND difficulty = :difficulty';
    $params['difficulty'] = $difficulty;
}

$sql .= ' ORDER BY RAND() LIMIT 1';
$stmt = $pdo->prepare($sql);
$stmt->execute($params);
$paragraph = $stmt->fetch();

if (!$paragraph) {
    send_error('No active paragraph found', 404);
}

send_success('Random paragraph fetched', [
    'paragraph' => normalize_paragraph($paragraph),
]);
