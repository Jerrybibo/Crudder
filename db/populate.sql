INSERT INTO items (name, description, price) VALUES
    ('Coffee', 'Locally sourced whole coffee beans.', 4.49),
    ('Green Tea', 'Premium imported Japanese green tea leaves.', 5.99),
    ('Flour', 'Italian Farina 00 flour.', 7.99),
    ('Sugar', 'Sugar of unknown origins.', 2.29),
    ('Eggs', 'Extra large eggs from the local farm.', 4.99);

INSERT INTO shipments (item_id, quantity, time_created) VALUES
    (2, -40, '2022-02-01 10:00:00'),
    (1, -10, '2022-02-01 13:00:00'),
    (3, -100, '2022-02-04 14:00:00'),
    (3, 30, '2022-02-05 08:30:00'),
    (4, -100, '2022-02-05 09:00:00'),
    (5, -4, '2022-02-07 15:00:00');

INSERT INTO inventory (item_id, quantity) VALUES
    (1, 15),
    (2, 50),
    (3, 120),
    (4, 100),
    (5, 6);