<?php
declare(strict_types=1);

require_once __DIR__ . '/../helpers/bootstrap.php';
require_once __DIR__ . '/../helpers/auth.php';

require_method(['POST']);

$body = get_json_input();
$email = strtolower(trim((string)($body['email'] ?? '')));
$password = (string)($body['password'] ?? '');

if ($email === '' || $password === '') {
    send_error('Email and password are required', 422);
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    send_error('Valid email is required', 422);
}

$pdo = get_pdo();
$stmt = $pdo->prepare('SELECT id, name, email, password_hash, role, created_at, updated_at FROM users WHERE email = :email LIMIT 1');
$stmt->execute(['email' => $email]);
$user = $stmt->fetch();

if (!$user || !password_verify($password, (string)$user['password_hash'])) {
    send_error('Invalid email or password', 401);
}

$token = bin2hex(random_bytes(32));
$updateStmt = $pdo->prepare('UPDATE users SET auth_token = :auth_token, updated_at = NOW() WHERE id = :id');
$updateStmt->execute([
    'auth_token' => $token,
    'id' => $user['id'],
]);

send_success('Login successful', [
    'token' => $token,
    'user' => to_public_user($user),
]);
