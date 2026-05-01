-- Data for Book Tracker Database
USE book_tracker
-- 1. Insert Publishers
INSERT INTO publisher (name, website, country) VALUES 
('Penguin Press', 'https://www.penguin.com', 'USA'),
('Random House', 'https://www.randomhousebooks.com', 'USA'),
('Little, Brown and Company', 'https://www.littlebrown.com', 'USA'),
('Crown Publishing Group', 'https://www.penguinrandomhouse.com', 'USA'),
('Portfolio', 'https://www.penguin.com/portfolio', 'USA'),
('HarperCollins', 'https://www.harpercollins.com', 'USA'),
('Simon & Schuster', 'https://www.simonandschuster.com', 'USA'),
('W. W. Norton & Company', 'https://www.wwnorton.com', 'USA'),
('Riverhead Books', 'https://www.penguin.com', 'USA'),
('Viking', 'https://www.penguin.com', 'USA'),
('Ballantine Books', 'https://www.penguinrandomhouse.com', 'USA'),
('Basic Books', 'https://www.basicbooks.com', 'USA'),
('Knopf', 'https://www.penguinrandomhouse.com', 'USA'),
('Bloomsbury', 'https://www.bloomsbury.com', 'UK'),
('Pan Macmillan', 'https://www.panmacmillan.com', 'UK');

-- 2. Insert Authors
INSERT INTO author (first_name, last_name, bio, field_of_expertise, credentials) VALUES 
('Simon', 'Sinek', 'Optimist and author of Start With Why.', 'Leadership', 'Motivational Speaker, Author'),
('Brené', 'Brown', 'Research professor on courage and vulnerability.', 'Psychology', 'PhD, LMSW, Professor at University of Houston'),
('Malcolm', 'Gladwell', 'Journalist and researcher on social dynamics.', 'Sociology', 'Staff writer at The New Yorker'),
('Tim', 'Ferriss', 'Entrepreneur and lifestyle designer.', 'Productivity', 'Author of The 4-Hour Workweek'),
('Carol', 'Dweck', 'Psychologist known for growth mindset research.', 'Psychology', 'Professor of Psychology at Stanford'),
('Ryan', 'Holiday', 'Writer on stoicism and marketing.', 'Philosophy', 'Former Director of Marketing at American Apparel'),
('Nassim', 'Taleb', 'Scholar and risk analyst.', 'Economics/Philosophy', 'Former options trader'),
('Gretchen', 'Rubin', 'Author on habits and happiness.', 'Personal Development', 'Yale Law graduate'),
('Charles', 'Duhigg', 'Pulitzer Prize-winning reporter on habits.', 'Personal Development', 'New York Times reporter'),
('Oliver', 'Burkeman', 'Journalist on productivity and time.', 'Productivity', 'The Guardian columnist'),
('Mark', 'Manson', 'Blogger and author on self-help.', 'Personal Development', 'Blogger'),
('Angela', 'Duckworth', 'Academic on grit and perseverance.', 'Psychology', 'Professor of Psychology at UPenn'),
('Daniel', 'Pink', 'Author on work, management, and behavior.', 'Business Strategy', 'Former speechwriter for Al Gore'),
('Mihaly', 'Csikszentmihalyi', 'Psychologist who defined Flow.', 'Psychology', 'Former head of Dept. of Psychology at UChicago'),
('David', 'Epstein', 'Journalist on performance and specialization.', 'Performance Science', 'Investigative reporter');

-- 3. Insert Categories
INSERT INTO category (name, description) VALUES 
('Leadership', 'Building teams and inspiring action'),
('Sociology', 'Study of social behavior and society'),
('Philosophy', 'Fundamental nature of knowledge and reality'),
('Stoicism', 'Practical ancient Greek philosophy'),
('Economics', 'Production, consumption, and transfer of wealth'),
('Habits', 'Science of behavioral change'),
('Happiness', 'Study of well-being and satisfaction'),
('Mindset', 'Psychological frameworks for success'),
('Creativity', 'Generating new ideas and artistic work'),
('Communication', 'Interpersonal skills and influence'),
('Time Management', 'Optimizing daily schedules'),
('Self-Help', 'Personal growth and life advice'),
('Performance', 'Reaching peak potential'),
('Work Culture', 'Management and workplace dynamics'),
('Decision Making', 'The science of choices');

-- 4. Insert Books
INSERT INTO book (title, publisher_id, page_count, word_count, read_time_hours, depth_level, approval_rating, description) VALUES 
('Start With Why', 1, 256, 65000, 5.0, 'moderate', 8.9, 'Why some people and organizations are more innovative.'),
('Daring Greatly', 2, 304, 75000, 6.0, 'in-depth', 9.2, 'How the courage to be vulnerable transforms the way we live.'),
('Outliers', 3, 304, 72000, 6.0, 'moderate', 9.0, 'The story of success and why some people achieve more.'),
('The 4-Hour Workweek', 4, 308, 85000, 7.0, 'broad', 8.5, 'Forget the old concept of retirement.'),
('Mindset', 5, 320, 80000, 6.5, 'in-depth', 9.3, 'The new psychology of success.'),
('The Obstacle Is the Way', 6, 201, 50000, 4.0, 'broad', 8.8, 'The timeless art of turning trials into triumph.'),
('The Black Swan', 7, 400, 110000, 9.0, 'in-depth', 9.1, 'The impact of the highly improbable.'),
('The Happiness Project', 8, 368, 90000, 7.5, 'broad', 8.4, 'Why I spent a year trying to sing in the morning.'),
('The Power of Habit', 9, 371, 95000, 8.0, 'in-depth', 9.4, 'Why we do what we do in life and business.'),
('Four Thousand Weeks', 10, 288, 70000, 5.5, 'moderate', 9.0, 'Time management for mortals.'),
('The Subtle Art of Not Giving a F*ck', 11, 224, 55000, 4.5, 'broad', 8.7, 'A counterintuitive approach to living a good life.'),
('Grit', 12, 352, 85000, 7.0, 'in-depth', 9.1, 'The power of passion and perseverance.'),
('Drive', 13, 272, 68000, 5.5, 'moderate', 8.9, 'The surprising truth about what motivates us.'),
('Flow', 14, 336, 82000, 6.5, 'in-depth', 9.2, 'The psychology of optimal experience.'),
('Range', 15, 352, 88000, 7.0, 'moderate', 9.0, 'Why generalists triumph in a specialized world.');

-- 5. Insert Book-Author Relationships
INSERT INTO book_author (book_id, author_id) VALUES 
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15);

-- 6. Insert Book-Category Relationships
INSERT INTO book_category (book_id, category_id) VALUES 
(1, 1), (2, 8), (3, 2), (4, 11), (5, 8), (6, 4), (7, 5), (8, 7), (9, 6), (10, 11), (11, 12), (12, 8), (13, 14), (14, 8), (15, 13);