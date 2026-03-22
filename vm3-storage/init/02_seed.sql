-- Insert sample companies
INSERT INTO companies (name) VALUES 
('Acme Corporation'),
('Globex Inc.'),
('Initech'),
('Widget Works'),
('Gadget Galaxy');

-- Insert sample users
-- Passwords are hashed (password: password123)
INSERT INTO users (username, password_hash, company_id) VALUES 
('john_doe', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.B6qy/G', 1),
('jane_smith', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.B6qy/G', 2),
('bob_johnson', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.B6qy/G', 3),
('alice_wilson', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.B6qy/G', 4),
('tom_hank', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.B6qy/G', 5);

-- Insert sample company data
INSERT INTO company_data (company_id, data_key, data_value) VALUES 
(1, 'revenue_2023', '1000000'),
(1, 'employees', '150'),
(1, 'industry', 'Manufacturing'),
(2, 'revenue_2023', '2500000'),
(2, 'employees', '300'),
(2, 'industry', 'Technology'),
(3, 'revenue_2023', '750000'),
(3, 'employees', '75'),
(3, 'industry', 'Services'),
(4, 'revenue_2023', '500000'),
(4, 'employees', '50'),
(4, 'industry', 'Retail'),
(5, 'revenue_2023', '1200000'),
(5, 'employees', '200'),
(5, 'industry', 'Finance');