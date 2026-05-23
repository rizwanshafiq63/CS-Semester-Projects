<?php
declare(strict_types=1);

function send_json(int $statusCode, bool $success, string $message, array $data = []): void
{
    http_response_code($statusCode);
    echo json_encode([
        'success' => $success,
        'message' => $message,
        'data' => $data,
    ]);
    exit;
}

function send_success(string $message, array $data = [], int $statusCode = 200): void
{
    send_json($statusCode, true, $message, $data);
}

function send_error(string $message, int $statusCode = 400): void
{
    send_json($statusCode, false, $message);
}
