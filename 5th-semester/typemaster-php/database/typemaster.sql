CREATE DATABASE IF NOT EXISTS typemaster CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE typemaster;

DROP TABLE IF EXISTS test_results;
DROP TABLE IF EXISTS typing_paragraphs;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') NOT NULL DEFAULT 'user',
    auth_token VARCHAR(128) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_auth_token (auth_token),
    INDEX idx_users_role (role)
);

CREATE TABLE typing_paragraphs (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    difficulty ENUM('easy', 'medium', 'hard') NOT NULL DEFAULT 'medium',
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_by INT UNSIGNED NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_paragraph_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_paragraphs_difficulty_active (difficulty, is_active)
);

CREATE TABLE test_results (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    paragraph_id INT UNSIGNED NOT NULL,
    difficulty ENUM('easy', 'medium', 'hard') NOT NULL,
    duration INT NOT NULL,
    wpm DECIMAL(8,2) NOT NULL,
    accuracy DECIMAL(5,2) NOT NULL,
    mistakes INT NOT NULL DEFAULT 0,
    chars_typed INT NOT NULL DEFAULT 0,
    time_taken DECIMAL(8,2) NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_results_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_results_paragraph FOREIGN KEY (paragraph_id) REFERENCES typing_paragraphs(id) ON DELETE CASCADE,
    INDEX idx_results_user_created (user_id, created_at),
    INDEX idx_results_filters (difficulty, duration, created_at),
    INDEX idx_results_ranking (wpm, accuracy)
);

INSERT INTO users (name, email, password_hash, role)
VALUES
('Admin User', 'admin@typemaster.com', '$2b$10$uFRw24Bq169f8HQa/s5KqezxZ5hfxtejAeH2FFDdM4jD3v0HgiFl6', 'admin'),
('Demo User', 'demo@example.com', '$2b$10$B2nwITqEHh.ho51qv3ft6uVxE/gMH4eU3m9wgDYdELERMobMAO9p6', 'user');

INSERT INTO typing_paragraphs (text, difficulty, is_active, created_by) VALUES
('Typing daily helps build strong muscle memory and improves your keyboard confidence.', 'easy', 1, 1),
('Short practice sessions can still produce steady progress when done with focus.', 'easy', 1, 1),
('Keep your eyes on the screen and let your fingers learn each key naturally.', 'easy', 1, 1),
('A calm rhythm often gives better speed than rushing and making many mistakes.', 'easy', 1, 1),
('Measure your words per minute and aim for small improvements each week.', 'easy', 1, 1),

('Consistent typing habits improve both speed and precision during timed assessments.', 'medium', 1, 1),
('When accuracy stays high, your average words per minute will rise over multiple tests.', 'medium', 1, 1),
('Good posture, balanced breathing, and clear focus can reduce typing fatigue significantly.', 'medium', 1, 1),
('Switching between practice modes challenges your adaptability and strengthens muscle memory.', 'medium', 1, 1),
('Track your performance trends to identify weak letter patterns and correct them early.', 'medium', 1, 1),

('Although rapid typing appears chaotic, disciplined finger placement creates surprisingly stable results over long durations.', 'hard', 1, 1),
('Advanced typists maintain concentration under pressure by balancing speed, precision, and efficient correction strategies.', 'hard', 1, 1),
('Complex passages with punctuation demand controlled rhythm; otherwise, small errors quickly lower overall accuracy metrics.', 'hard', 1, 1),
('Performance plateaus often break only after focused drills that target stubborn key transitions and uncommon word patterns.', 'hard', 1, 1),
('Mastery in typing grows from deliberate repetition, reflective review, and continuous adaptation to increasingly difficult text.', 'hard', 1, 1);
