<?php
declare(strict_types=1);

require_once __DIR__ . '/../helpers/bootstrap.php';
require_once __DIR__ . '/../helpers/auth.php';

require_method(['GET']);
require_admin();

$search = trim((string)($_GET['search'] ?? ''));
$difficulty = strtolower(trim((string)($_GET['difficulty'] ?? '')));
$status = strtolower(trim((string)($_GET['status'] ?? '')));
$page = max(1, (int)($_GET['page'] ?? 1));
$limit = max(1, min(100, (int)($_GET['limit'] ?? 10)));

if ($difficulty !== '' && $difficulty !== 'all' && !in_array($difficulty, ['easy', 'medium', 'hard'], true)) {
    send_error('Difficulty must be easy, medium, hard, or all', 422);
}
if ($status !== '' && $status !== 'all' && !in_array($status, ['active', 'inactive'], true)) {
    send_error('Status must be active, inactive, or all', 422);
}

$whereParts = ['1=1'];
$params = [];

if ($search !== '') {
    $whereParts[] = 'text LIKE :search';
    $params['search'] = '%' . $search . '%';
}
if ($difficulty !== '' && $difficulty !== 'all') {
    $whereParts[] = 'difficulty = :difficulty';
    $params['difficulty'] = $difficulty;
}
if ($status !== '' && $status !== 'all') {
    $whereParts[] = $status === 'active' ? 'is_active = 1' : 'is_active = 0';
}

$whereSql = implode(' AND ', $whereParts);
$pdo = get_pdo();

$countStmt = $pdo->prepare("SELECT COUNT(*) FROM typing_paragraphs WHERE {$whereSql}");
$countStmt->execute($params);
$total = (int)$countStmt->fetchColumn();

$offset = ($page - 1) * $limit;
$listSql = "SELECT id, text, difficulty, is_active, created_by, created_at, updated_at
            FROM typing_paragraphs
            WHERE {$whereSql}
            ORDER BY created_at DESC
            LIMIT :limit OFFSET :offset";
$listStmt = $pdo->prepare($listSql);
foreach ($params as $key => $value) {
    $listStmt->bindValue(':' . $key, $value);
}
$listStmt->bindValue(':limit', $limit, PDO::PARAM_INT);
$listStmt->bindValue(':offset', $offset, PDO::PARAM_INT);
$listStmt->execute();
$rows = $listStmt->fetchAll();

$paragraphs = array_map(static fn(array $row): array => normalize_paragraph($row), $rows);

send_success('Paragraphs fetched', [
    'paragraphs' => $paragraphs,
    'count' => count($paragraphs),
    'total' => $total,
    'page' => $page,
    'limit' => $limit,
]);
