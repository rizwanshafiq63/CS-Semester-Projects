<?php
declare(strict_types=1);

require_once __DIR__ . '/../helpers/bootstrap.php';
require_once __DIR__ . '/../helpers/auth.php';

require_method(['GET']);

$user = require_auth();
send_success('Current user fetched', ['user' => to_public_user($user)]);
