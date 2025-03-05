// Тестовые данные для проверки работы
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    amount NUMERIC(10, 2) NOT NULL
);
INSERT INTO orders (customer_id, order_date, amount) 
VALUES
    (1, '2023-01-10', 100.00),
    (1, '2023-02-15', 200.00),
    (2, '2023-03-20', 150.00),
    (2, '2023-04-25', 150.00),
    (2, '2022-05-30', 300.00),
    (3, '2023-06-05', 500.00),
    (4, '2024-07-10', 200.00),
    (4, '2024-08-15', 200.00),
    (5, '2023-09-20', 500.00),
    (6, '2023-10-25', 600.00);
// Найти общую сумму заказов для каждого клиента.
SELECT customer_id, sum(amount) as total_amount
FROM orders
GROUP BY customer_id;
// Найти клиента с максимальной суммой заказов.
WITH customer_total_amount AS (
    SELECT customer_id, sum(amount) as total_amount
    FROM orders
    GROUP BY customer_id
) SELECT * FROM customer_total_amount
WHERE total_amount = (SELECT max(total_amount) FROM customer_total_amount);
// Найти количество заказов, сделанных в 2023 году. 
SELECT count(*) as orders
FROM orders
WHERE extract(YEAR FROM order_date) = 2023;
// Найти среднюю сумму заказа для каждого клиента.  
SELECT customer_id, round(avg(amount), 2) AS average_amount
FROM orders
GROUP BY customer_id
ORDER BY customer_id;
