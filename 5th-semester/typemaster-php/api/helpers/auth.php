<?php
declare(strict_types=1);

require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/response.php';

function get_bearer_token(): ?string
{
    $headers = function_exists('getallheaders') ? getallheaders() : [];
    $authHeader = $headers['Authorization'] ?? $headers['authorization'] ?? '';

    if (!$authHeader && isset($_SERVER['HTTP_AUTHORIZATION'])) {
        $authHeader = $_SERVER['HTTP_AUTHORIZATION'];
    }

    if (!preg_match('/Bearer\s+(.+)/i', (string)$authHeader, $matches)) {
        return null;
    }

    return trim($matches[1]);
}

function require_auth(): array
{
    $token = get_bearer_token();
    if (!$token) {
        send_error('Unauthorized: token missing', 401);
    }

    $pdo = get_pdo();
    $stmt = $pdo->prepare('SELECT id, name, email, role, created_at, updated_at FROM users WHERE auth_token = :token LIMIT 1');
    $stmt->execute(['token' => $token]);
    $user = $stmt->fetch();

    if (!$user) {
        send_error('Unauthorized: invalid token', 401);
    }

    return $user;
}

function require_admin(): array
{
    $user = require_auth();
    if (($user['role'] ?? 'user') !== 'admin') {
        send_error('Forbidden: admin access required', 403);
    }
    return $user;
}

function to_public_user(array $user): array
{
    return [
        'id' => (int)($user['id'] ?? 0),
        '_id' => (int)($user['id'] ?? 0),
        'name' => $user['name'] ?? '',
        'email' => $user['email'] ?? '',
        'role' => $user['role'] ?? 'user',
        'createdAt' => $user['created_at'] ?? null,
        'updatedAt' => $user['updated_at'] ?? null,
    ];
}
