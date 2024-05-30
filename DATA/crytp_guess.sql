
CREATE TABLE IF NOT EXISTS bitcoin_prices (
    date TEXT PRIMARY KEY,
    price REAL
);


INSERT INTO bitcoin_prices (date, price) VALUES ('2023-01-01', 34000.50);
INSERT INTO bitcoin_prices (date, price) VALUES ('2023-01-02', 34500.75);
INSERT INTO bitcoin_prices (date, price) VALUES ('2023-01-03', 35000.20);
