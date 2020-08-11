INSERT INTO hrapp_training_program
(name, description, start_date, end_date, max_attendees)
VALUES
('OSHA Regulations', 'New procedures to follow safety guidelines', '2020-010-09', '2021-04-05', 25);

INSERT INTO hrapp_training_program
(name, description, start_date, end_date, max_attendees)
VALUES
('Coloring by Numbers', 'Come color dawg!', '2020-11-09', '2022-04-05', 10);

INSERT INTO hrapp_training_program
(name, description, start_date, end_date, max_attendees)
VALUES
('Forklift Maintenance', 'Come repair a forklist, dawg!', '2012-03-09', '2014-04-05', 10);

INSERT INTO hrapp_training_program
(name, description, start_date, end_date, max_attendees)
VALUES
('New thing', 'Come learn this new thing, dawg!', '2021-03-09', '2023-04-05', 10);

DELETE FROM hrapp_training_program
WHERE name LIKE '%OSHA%';

INSERT INTO hrapp_employee_training_program
(training_program_id, employee_id)
VALUES
(12, 2);
