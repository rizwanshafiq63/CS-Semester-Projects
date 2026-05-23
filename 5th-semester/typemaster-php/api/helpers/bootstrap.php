<?php
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Headers: Content-Type, Authorization');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

require_once __DIR__ . '/response.php';
require_once __DIR__ . '/../config/database.php';

set_exception_handler(static function (Throwable $e): void {
    send_error('Server error: ' . $e->getMessage(), 500);
});

function require_method(array $allowedMethods): void
{
    $method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
    if (!in_array($method, $allowedMethods, true)) {
        send_error('Method not allowed', 405);
    }
}

function get_json_input(): array
{
    $raw = file_get_contents('php://input');
    if ($raw === false || trim($raw) === '') {
        return [];
    }

    $decoded = json_decode($raw, true);
    if (!is_array($decoded)) {
        send_error('Invalid JSON body', 400);
    }
    return $decoded;
}

function normalize_paragraph(array $row): array
{
    return [
        'id' => (int)($row['id'] ?? 0),
        '_id' => (int)($row['id'] ?? 0),
        'text' => $row['text'] ?? '',
        'difficulty' => $row['difficulty'] ?? 'medium',
        'isActive' => (bool)($row['is_active'] ?? 0),
        'createdAt' => $row['created_at'] ?? null,
        'updatedAt' => $row['updated_at'] ?? null,
    ];
}

function normalize_result(array $row): array
{
    return [
        'id' => (int)($row['id'] ?? 0),
        '_id' => (int)($row['id'] ?? 0),
        'userId' => (int)($row['user_id'] ?? 0),
        'paragraph' => isset($row['paragraph_id']) ? (int)$row['paragraph_id'] : null,
        'difficulty' => $row['difficulty'] ?? 'medium',
        'duration' => (int)($row['duration'] ?? 0),
        'wpm' => (float)($row['wpm'] ?? 0),
        'accuracy' => (float)($row['accuracy'] ?? 0),
        'mistakes' => (int)($row['mistakes'] ?? 0),
        'charsTyped' => (int)($row['chars_typed'] ?? 0),
        'timeTaken' => (float)($row['time_taken'] ?? 0),
        'createdAt' => $row['created_at'] ?? null,
    ];
}
