INSERT INTO items (name, description, price) VALUES
    ('Coffee', 'Locally sourced whole coffee beans.', 4.49),
    ('Green Tea', 'Premium imported Japanese green tea leaves.', 5.99),
    ('Flour', 'Italian Farina 00 flour.', 7.99),
    ('Sugar', 'Sugar of unknown origins.', 2.29),
    ('Eggs', 'Extra large eggs from the local farm.', 4.99);

INSERT INTO shipments (item_id, quantity, time_created) VALUES
    (1, 10, '2020-01-01 00:00:00'),
    (2, 20, '2020-01-01 00:00:00'),
    (3, 30, '2020-01-01 00:00:00'),
    (4, 40, '2020-01-01 00:00:00'),
    (5, 50, '2020-01-01 00:00:00');

INSERT INTO inventory (item_id, quantity) VALUES
    (1, 10),
    (2, 20),
    (3, 30),
    (4, 40),
    (5, 50);