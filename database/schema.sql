-- ============================================================
-- Smart Agro AI-Powered Agriculture Management System
-- MySQL Database Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS smart_agro_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE smart_agro_db;

-- ============================================================
-- Table: users (core authentication table)
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    email           VARCHAR(120) UNIQUE NOT NULL,
    password_hash   VARCHAR(256) NOT NULL,
    role            ENUM('admin', 'farmer', 'expert', 'bank') NOT NULL,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_email (email),
    INDEX idx_users_role  (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Table: farmer_profiles
-- ============================================================
CREATE TABLE IF NOT EXISTS farmer_profiles (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL UNIQUE,
    farm_name       VARCHAR(100),
    farm_location   VARCHAR(200),
    farm_size       DECIMAL(10, 2) COMMENT 'in acres',
    soil_type       ENUM('Sandy', 'Loamy', 'Clay', 'Silt', 'Peaty', 'Chalky', 'Sandy Loam') DEFAULT 'Loamy',
    phone           VARCHAR(15),
    aadhaar         VARCHAR(12),
    address         TEXT,
    profile_image   VARCHAR(256),
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_farmer_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Table: expert_profiles
-- ============================================================
CREATE TABLE IF NOT EXISTS expert_profiles (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    user_id             INT NOT NULL UNIQUE,
    specialization      VARCHAR(100),
    qualification       VARCHAR(150),
    experience_years    INT DEFAULT 0,
    bio                 TEXT,
    phone               VARCHAR(15),
    profile_image       VARCHAR(256),
    is_available        BOOLEAN DEFAULT TRUE,
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_expert_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Table: bank_profiles
-- ============================================================
CREATE TABLE IF NOT EXISTS bank_profiles (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL UNIQUE,
    bank_name       VARCHAR(100),
    branch_name     VARCHAR(100),
    ifsc_code       VARCHAR(11),
    address         TEXT,
    phone           VARCHAR(15),
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_bank_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Table: crops
-- ============================================================
CREATE TABLE IF NOT EXISTS crops (
    id                      INT AUTO_INCREMENT PRIMARY KEY,
    farmer_id               INT NOT NULL,
    name                    VARCHAR(100) NOT NULL,
    variety                 VARCHAR(100),
    area_acres              DECIMAL(10, 2),
    planting_date           DATE,
    expected_harvest_date   DATE,
    actual_harvest_date     DATE,
    status                  ENUM('growing', 'harvested', 'failed') DEFAULT 'growing',
    image_url               VARCHAR(256),
    description             TEXT,
    created_at              DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at              DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES farmer_profiles(id) ON DELETE CASCADE,
    INDEX idx_crop_farmer   (farmer_id),
    INDEX idx_crop_status   (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Table: crop_prices
-- ============================================================
CREATE TABLE IF NOT EXISTS crop_prices (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    crop_name       VARCHAR(100) NOT NULL,
    variety         VARCHAR(100),
    price_per_kg    DECIMAL(10, 2) NOT NULL,
    market_name     VARCHAR(150),
    state           VARCHAR(100),
    date            DATE NOT NULL DEFAULT (CURRENT_DATE),
    updated_by      INT COMMENT 'FK to users.id (admin user)',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_crop_price_name (crop_name),
    INDEX idx_crop_price_date (date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Table: loans
-- ============================================================
CREATE TABLE IF NOT EXISTS loans (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    loan_reference      VARCHAR(20) UNIQUE,
    farmer_id           INT NOT NULL,
    bank_id             INT,
    amount              DECIMAL(15, 2) NOT NULL,
    purpose             ENUM('Agriculture', 'Equipment', 'Seeds', 'Irrigation', 'Other') NOT NULL,
    description         TEXT,
    status              ENUM('pending', 'approved', 'rejected', 'disbursed') DEFAULT 'pending',
    interest_rate       DECIMAL(5, 2) COMMENT 'Annual % rate',
    tenure_months       INT COMMENT 'Repayment tenure in months',
    applied_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    reviewed_at         DATETIME,
    remarks             TEXT COMMENT 'Bank officer remarks',
    documents           JSON COMMENT 'Array of document file paths',
    FOREIGN KEY (farmer_id) REFERENCES farmer_profiles(id) ON DELETE CASCADE,
    FOREIGN KEY (bank_id)   REFERENCES bank_profiles(id) ON DELETE SET NULL,
    INDEX idx_loan_farmer   (farmer_id),
    INDEX idx_loan_status   (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Table: complaints
-- ============================================================
CREATE TABLE IF NOT EXISTS complaints (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    farmer_id       INT NOT NULL,
    subject         VARCHAR(200) NOT NULL,
    description     TEXT NOT NULL,
    category        ENUM('crop', 'loan', 'weather', 'pest', 'market', 'other') DEFAULT 'other',
    status          ENUM('open', 'in_progress', 'resolved', 'closed') DEFAULT 'open',
    priority        ENUM('low', 'medium', 'high') DEFAULT 'medium',
    admin_reply     TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES farmer_profiles(id) ON DELETE CASCADE,
    INDEX idx_complaint_farmer  (farmer_id),
    INDEX idx_complaint_status  (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Table: notifications
-- ============================================================
CREATE TABLE IF NOT EXISTS notifications (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    title       VARCHAR(200) NOT NULL,
    message     TEXT NOT NULL,
    type        ENUM('info', 'success', 'warning', 'error') DEFAULT 'info',
    is_read     BOOLEAN DEFAULT FALSE,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_notif_user    (user_id),
    INDEX idx_notif_read    (is_read)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Table: disease_predictions
-- ============================================================
CREATE TABLE IF NOT EXISTS disease_predictions (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    farmer_id           INT NOT NULL,
    crop_id             INT,
    image_url           VARCHAR(256) NOT NULL,
    disease_name        VARCHAR(200) NOT NULL,
    confidence_score    DECIMAL(5, 4) COMMENT '0.0000 to 1.0000',
    severity            ENUM('healthy', 'low', 'medium', 'high') DEFAULT 'medium',
    treatment_suggestion TEXT,
    prevention_tips     TEXT,
    predicted_at        DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES farmer_profiles(id) ON DELETE CASCADE,
    FOREIGN KEY (crop_id)   REFERENCES crops(id) ON DELETE SET NULL,
    INDEX idx_disease_farmer (farmer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Table: recommendations
-- ============================================================
CREATE TABLE IF NOT EXISTS recommendations (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    farmer_id   INT NOT NULL,
    type        ENUM('crop', 'fertilizer', 'yield') NOT NULL,
    input_data  JSON NOT NULL COMMENT 'Input parameters as JSON',
    result      JSON NOT NULL COMMENT 'AI result as JSON',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES farmer_profiles(id) ON DELETE CASCADE,
    INDEX idx_rec_farmer (farmer_id),
    INDEX idx_rec_type   (type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Table: queries (farmer to expert Q&A)
-- ============================================================
CREATE TABLE IF NOT EXISTS queries (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    farmer_id       INT NOT NULL,
    expert_id       INT,
    subject         VARCHAR(200) NOT NULL,
    question        TEXT NOT NULL,
    answer          TEXT,
    status          ENUM('open', 'answered', 'closed') DEFAULT 'open',
    category        ENUM('disease', 'fertilizer', 'pesticide', 'irrigation', 'general') DEFAULT 'general',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    answered_at     DATETIME,
    FOREIGN KEY (farmer_id) REFERENCES farmer_profiles(id) ON DELETE CASCADE,
    FOREIGN KEY (expert_id) REFERENCES expert_profiles(id) ON DELETE SET NULL,
    INDEX idx_query_farmer  (farmer_id),
    INDEX idx_query_expert  (expert_id),
    INDEX idx_query_status  (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Seed Data — Demo Users
-- ============================================================
-- Passwords are all: Password@123 (hashed with werkzeug pbkdf2:sha256)
-- NOTE: These hashes are generated by werkzeug.security.generate_password_hash('Password@123')
-- You should regenerate these using the seed_data.py script for security.
-- For demo purposes only:

INSERT INTO users (name, email, password_hash, role, is_active) VALUES
('Admin User',          'admin@smartagro.com',  'pbkdf2:sha256:260000$demo$adminhash',  'admin',  TRUE),
('Rajesh Kumar',        'farmer@smartagro.com', 'pbkdf2:sha256:260000$demo$farmerhash', 'farmer', TRUE),
('Dr. Priya Sharma',    'expert@smartagro.com', 'pbkdf2:sha256:260000$demo$experthash', 'expert', TRUE),
('SBI Bank Officer',    'bank@smartagro.com',   'pbkdf2:sha256:260000$demo$bankhash',   'bank',   TRUE);

-- NOTE: Use seed_data.py to properly seed with real password hashes!

-- ============================================================
-- Seed Data — Crop Prices
-- ============================================================
INSERT INTO crop_prices (crop_name, variety, price_per_kg, market_name, state, date) VALUES
('Rice',        'Basmati',      45.50,  'Azadpur Mandi',    'Delhi',        CURRENT_DATE),
('Rice',        'Sona Masuri',  38.00,  'Kurnool Market',   'Andhra Pradesh', CURRENT_DATE),
('Wheat',       'Sharbati',     28.00,  'Khanna Mandi',     'Punjab',       CURRENT_DATE),
('Wheat',       'HD-2967',      25.50,  'Karnal Mandi',     'Haryana',      CURRENT_DATE),
('Corn',        'Yellow Corn',  18.00,  'Davangere Market', 'Karnataka',    CURRENT_DATE),
('Cotton',      'BT Cotton',    62.00,  'Yavatmal Mandi',   'Maharashtra',  CURRENT_DATE),
('Sugarcane',   'Co-86032',     3.50,   'Kolhapur Market',  'Maharashtra',  CURRENT_DATE),
('Tomato',      'Hybrid',       15.00,  'Nashik Mandi',     'Maharashtra',  CURRENT_DATE),
('Onion',       'Red Onion',    22.00,  'Lasalgaon Mandi',  'Maharashtra',  CURRENT_DATE),
('Potato',      'Kufri Jyoti',  12.00,  'Agra Mandi',       'Uttar Pradesh', CURRENT_DATE),
('Soybean',     'JS-335',       44.00,  'Indore Mandi',     'Madhya Pradesh', CURRENT_DATE),
('Groundnut',   'TMV-2',        55.00,  'Gondal Mandi',     'Gujarat',      CURRENT_DATE),
('Mustard',     'Pusa Bold',    52.00,  'Bharatpur Mandi',  'Rajasthan',    CURRENT_DATE),
('Turmeric',    'Salem',        115.00, 'Erode Market',     'Tamil Nadu',   CURRENT_DATE),
('Chilli',      'Guntur',       95.00,  'Guntur Mandi',     'Andhra Pradesh', CURRENT_DATE);
