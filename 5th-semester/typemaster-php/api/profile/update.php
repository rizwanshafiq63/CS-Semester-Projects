<?php
declare(strict_types=1);

require_once __DIR__ . '/../helpers/bootstrap.php';
require_once __DIR__ . '/../helpers/auth.php';

require_method(['PUT']);
$user = require_auth();
$body = get_json_input();

$name = trim((string)($body['name'] ?? ''));
if ($name === '') {
    send_error('Name is required', 422);
}
if (strlen($name) < 2 || strlen($name) > 50) {
    send_error('Name must be between 2 and 50 characters', 422);
}

$pdo = get_pdo();
$stmt = $pdo->prepare('UPDATE users SET name = :name, updated_at = NOW() WHERE id = :id');
$stmt->execute([
    'name' => $name,
    'id' => (int)$user['id'],
]);

$userStmt = $pdo->prepare('SELECT id, name, email, role, created_at, updated_at FROM users WHERE id = :id');
$userStmt->execute(['id' => (int)$user['id']]);
$updatedUser = $userStmt->fetch();

send_success('Profile updated', [
    'user' => to_public_user($updatedUser ?: $user),
]);
