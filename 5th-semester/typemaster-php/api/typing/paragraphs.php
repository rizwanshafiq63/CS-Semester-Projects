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

$sql .= ' ORDER BY created_at DESC';
$stmt = $pdo->prepare($sql);
$stmt->execute($params);
$rows = $stmt->fetchAll();

$paragraphs = array_map(static fn(array $row): array => normalize_paragraph($row), $rows);

send_success('Paragraph list fetched', [
    'count' => count($paragraphs),
    'paragraphs' => $paragraphs,
]);
