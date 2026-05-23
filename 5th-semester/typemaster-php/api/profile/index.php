<?php
declare(strict_types=1);

require_once __DIR__ . '/../helpers/bootstrap.php';
require_once __DIR__ . '/../helpers/auth.php';
require_once __DIR__ . '/../helpers/stats.php';

require_method(['GET']);
$user = require_auth();

$stats = get_user_stats((int)$user['id'], 10);
send_success('Profile fetched', [
    'user' => to_public_user($user),
    'stats' => [
        'totalTests' => $stats['totalTests'],
        'averageWpm' => $stats['averageWpm'],
        'bestWpm' => $stats['bestWpm'],
        'averageAccuracy' => $stats['averageAccuracy'],
        'totalTime' => $stats['totalTime'],
        'improvementPercentage' => $stats['improvementPercentage'],
    ],
]);
