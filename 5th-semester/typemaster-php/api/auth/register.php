<?php
declare(strict_types=1);

require_once __DIR__ . '/../helpers/bootstrap.php';
require_once __DIR__ . '/../helpers/auth.php';

require_method(['POST']);

$body = get_json_input();
$name = trim((string)($body['name'] ?? ''));
$email = strtolower(trim((string)($body['email'] ?? '')));
$password = (string)($body['password'] ?? '');

if ($name === '' || $email === '' || $password === '') {
    send_error('Name, email, and password are required', 422);
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    send_error('Valid email is required', 422);
}
if (strlen($password) < 8) {
    send_error('Password must be at least 8 characters', 422);
}

$pdo = get_pdo();
$checkStmt = $pdo->prepare('SELECT id FROM users WHERE email = :email LIMIT 1');
$checkStmt->execute(['email' => $email]);
if ($checkStmt->fetch()) {
    send_error('Email is already registered', 409);
}

$passwordHash = password_hash($password, PASSWORD_DEFAULT);
$token = bin2hex(random_bytes(32));

$insertStmt = $pdo->prepare(
    'INSERT INTO users (name, email, password_hash, role, auth_token) VALUES (:name, :email, :password_hash, :role, :auth_token)'
);
$insertStmt->execute([
    'name' => $name,
    'email' => $email,
    'password_hash' => $passwordHash,
    'role' => 'user',
    'auth_token' => $token,
]);

$userId = (int)$pdo->lastInsertId();
$userStmt = $pdo->prepare('SELECT id, name, email, role, created_at, updated_at FROM users WHERE id = :id');
$userStmt->execute(['id' => $userId]);
$user = $userStmt->fetch();

send_success('Registration successful', [
    'token' => $token,
    'user' => to_public_user($user ?: []),
], 201);
