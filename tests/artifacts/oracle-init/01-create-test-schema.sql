-- Oracle Test Database Initialization Script
-- This script creates the test schema and sample data for FLEXT Target Oracle tests

-- Create test tablespace
CREATE TABLESPACE test_data 
DATAFILE '/opt/oracle/oradata/XEPDB1/test_data01.dbf' 
SIZE 100M AUTOEXTEND ON NEXT 10M MAXSIZE 1G;

-- Create test user
CREATE USER target_test_user IDENTIFIED BY test_password
DEFAULT TABLESPACE test_data
TEMPORARY TABLESPACE temp;

-- Grant necessary privileges
GRANT CONNECT, RESOURCE, CREATE SESSION TO target_test_user;
GRANT CREATE TABLE, CREATE VIEW, CREATE SEQUENCE TO target_test_user;
GRANT UNLIMITED TABLESPACE TO target_test_user;

-- Create test schema
CREATE SCHEMA AUTHORIZATION target_test_user;

-- Grant system privileges for testing
GRANT SELECT_CATALOG_ROLE TO target_test_user;
GRANT SELECT ANY DICTIONARY TO target_test_user;

-- Switch to test user context
ALTER SESSION SET CURRENT_SCHEMA=target_test_user;

-- Create test tables
CREATE TABLE test_customers (
    id NUMBER PRIMARY KEY,
    name VARCHAR2(100) NOT NULL,
    email VARCHAR2(255) UNIQUE,
    phone VARCHAR2(20),
    address VARCHAR2(500),
    city VARCHAR2(100),
    country VARCHAR2(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active NUMBER(1) DEFAULT 1,
    metadata CLOB
);

CREATE TABLE test_orders (
    order_id NUMBER PRIMARY KEY,
    customer_id NUMBER NOT NULL,
    order_date DATE DEFAULT SYSDATE,
    total_amount NUMBER(10,2),
    currency VARCHAR2(3) DEFAULT 'USD',
    status VARCHAR2(20) DEFAULT 'PENDING',
    payment_method VARCHAR2(50),
    shipping_address VARCHAR2(500),
    notes CLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES test_customers(id)
);

CREATE TABLE test_order_items (
    item_id NUMBER PRIMARY KEY,
    order_id NUMBER NOT NULL,
    product_name VARCHAR2(200) NOT NULL,
    quantity NUMBER(10,2) DEFAULT 1,
    unit_price NUMBER(10,2),
    total_price NUMBER(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES test_orders(order_id)
);

CREATE TABLE test_products (
    product_id NUMBER PRIMARY KEY,
    name VARCHAR2(200) NOT NULL,
    description CLOB,
    price NUMBER(10,2),
    category VARCHAR2(100),
    is_active NUMBER(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create sequences
CREATE SEQUENCE test_customers_seq START WITH 1000 INCREMENT BY 1;
CREATE SEQUENCE test_orders_seq START WITH 2000 INCREMENT BY 1;
CREATE SEQUENCE test_order_items_seq START WITH 3000 INCREMENT BY 1;
CREATE SEQUENCE test_products_seq START WITH 4000 INCREMENT BY 1;

-- Create triggers for auto-increment
CREATE OR REPLACE TRIGGER test_customers_bi
    BEFORE INSERT ON test_customers
    FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := test_customers_seq.NEXTVAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER test_orders_bi
    BEFORE INSERT ON test_orders
    FOR EACH ROW
BEGIN
    IF :NEW.order_id IS NULL THEN
        :NEW.order_id := test_orders_seq.NEXTVAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER test_order_items_bi
    BEFORE INSERT ON test_order_items
    FOR EACH ROW
BEGIN
    IF :NEW.item_id IS NULL THEN
        :NEW.item_id := test_order_items_seq.NEXTVAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER test_products_bi
    BEFORE INSERT ON test_products
    FOR EACH ROW
BEGIN
    IF :NEW.product_id IS NULL THEN
        :NEW.product_id := test_products_seq.NEXTVAL;
    END IF;
END;
/

-- Create indexes
CREATE INDEX idx_customers_email ON test_customers(email);
CREATE INDEX idx_customers_created_at ON test_customers(created_at);
CREATE INDEX idx_orders_customer_id ON test_orders(customer_id);
CREATE INDEX idx_orders_order_date ON test_orders(order_date);
CREATE INDEX idx_orders_status ON test_orders(status);
CREATE INDEX idx_order_items_order_id ON test_order_items(order_id);
CREATE INDEX idx_products_category ON test_products(category);
CREATE INDEX idx_products_is_active ON test_products(is_active);

-- Insert sample data
INSERT INTO test_customers (name, email, phone, address, city, country, metadata) VALUES
('John Doe', 'john.doe@example.com', '+1-555-0101', '123 Main St', 'New York', 'USA', '{"customer_type": "premium", "signup_source": "web"}'),
('Jane Smith', 'jane.smith@example.com', '+1-555-0102', '456 Oak Ave', 'Los Angeles', 'USA', '{"customer_type": "regular", "signup_source": "mobile"}'),
('Bob Johnson', 'bob.johnson@example.com', '+1-555-0103', '789 Pine Rd', 'Chicago', 'USA', '{"customer_type": "regular", "signup_source": "web"}'),
('Alice Brown', 'alice.brown@example.com', '+1-555-0104', '321 Elm St', 'Houston', 'USA', '{"customer_type": "premium", "signup_source": "referral"}'),
('Charlie Wilson', 'charlie.wilson@example.com', '+1-555-0105', '654 Maple Dr', 'Phoenix', 'USA', '{"customer_type": "regular", "signup_source": "web"}');

INSERT INTO test_products (name, description, price, category) VALUES
('Laptop Computer', 'High-performance laptop with 16GB RAM and 512GB SSD', 999.99, 'Electronics'),
('Wireless Mouse', 'Ergonomic wireless mouse with USB receiver', 29.99, 'Electronics'),
('Office Chair', 'Adjustable ergonomic office chair', 199.99, 'Furniture'),
('Desk Lamp', 'LED desk lamp with adjustable brightness', 49.99, 'Furniture'),
('Coffee Mug', 'Ceramic coffee mug with company logo', 12.99, 'Accessories'),
('Notebook', 'Professional notebook with lined pages', 8.99, 'Accessories'),
('Smartphone', 'Latest model smartphone with 128GB storage', 699.99, 'Electronics'),
('Headphones', 'Noise-cancelling wireless headphones', 149.99, 'Electronics');

INSERT INTO test_orders (customer_id, order_date, total_amount, currency, status, payment_method, shipping_address, notes) VALUES
(1000, SYSDATE-10, 999.99, 'USD', 'COMPLETED', 'CREDIT_CARD', '123 Main St, New York, USA', 'Express shipping requested'),
(1001, SYSDATE-8, 179.98, 'USD', 'SHIPPED', 'PAYPAL', '456 Oak Ave, Los Angeles, USA', 'Gift wrap requested'),
(1002, SYSDATE-5, 62.98, 'USD', 'PENDING', 'CREDIT_CARD', '789 Pine Rd, Chicago, USA', 'Standard shipping'),
(1003, SYSDATE-3, 849.98, 'USD', 'PROCESSING', 'DEBIT_CARD', '321 Elm St, Houston, USA', 'Bulk order discount applied'),
(1004, SYSDATE-1, 21.98, 'USD', 'PENDING', 'CREDIT_CARD', '654 Maple Dr, Phoenix, USA', 'Small order');

INSERT INTO test_order_items (order_id, product_name, quantity, unit_price, total_price) VALUES
(2000, 'Laptop Computer', 1, 999.99, 999.99),
(2001, 'Wireless Mouse', 1, 29.99, 29.99),
(2001, 'Office Chair', 1, 199.99, 199.99),
(2002, 'Desk Lamp', 1, 49.99, 49.99),
(2002, 'Coffee Mug', 1, 12.99, 12.99),
(2003, 'Smartphone', 1, 699.99, 699.99),
(2003, 'Headphones', 1, 149.99, 149.99),
(2004, 'Notebook', 2, 8.99, 17.98),
(2004, 'Coffee Mug', 3, 12.99, 4.99);

COMMIT;

-- Create views for testing
CREATE OR REPLACE VIEW customer_orders AS
SELECT 
    c.id as customer_id,
    c.name as customer_name,
    c.email,
    o.order_id,
    o.order_date,
    o.total_amount,
    o.status,
    o.payment_method
FROM test_customers c
JOIN test_orders o ON c.id = o.customer_id;

CREATE OR REPLACE VIEW order_summary AS
SELECT 
    o.order_id,
    o.customer_id,
    o.order_date,
    o.total_amount,
    o.status,
    COUNT(oi.item_id) as item_count,
    SUM(oi.quantity) as total_quantity
FROM test_orders o
LEFT JOIN test_order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.customer_id, o.order_date, o.total_amount, o.status;

-- Create test procedures
CREATE OR REPLACE PROCEDURE cleanup_test_data AS
BEGIN
    DELETE FROM test_order_items;
    DELETE FROM test_orders;
    DELETE FROM test_customers;
    DELETE FROM test_products;
    
    -- Reset sequences
    EXECUTE IMMEDIATE 'ALTER SEQUENCE test_customers_seq RESTART START WITH 1000';
    EXECUTE IMMEDIATE 'ALTER SEQUENCE test_orders_seq RESTART START WITH 2000';
    EXECUTE IMMEDIATE 'ALTER SEQUENCE test_order_items_seq RESTART START WITH 3000';
    EXECUTE IMMEDIATE 'ALTER SEQUENCE test_products_seq RESTART START WITH 4000';
    
    COMMIT;
END;
/

CREATE OR REPLACE PROCEDURE generate_test_data(p_customer_count IN NUMBER DEFAULT 100) AS
BEGIN
    FOR i IN 1..p_customer_count LOOP
        INSERT INTO test_customers (name, email, phone, city, country) VALUES
        ('Test Customer ' || i, 'test' || i || '@example.com', '+1-555-' || LPAD(i, 4, '0'), 'Test City ' || i, 'USA');
    END LOOP;
    COMMIT;
END;
/

-- Show summary of created objects
SELECT 'Test schema setup completed successfully!' as message FROM dual;
SELECT 'Tables created:' as info FROM dual;
SELECT table_name FROM user_tables WHERE table_name LIKE 'TEST_%' ORDER BY table_name;
SELECT 'Views created:' as info FROM dual;
SELECT view_name FROM user_views ORDER BY view_name;
SELECT 'Sequences created:' as info FROM dual;
SELECT sequence_name FROM user_sequences ORDER BY sequence_name;
SELECT 'Sample data counts:' as info FROM dual;
SELECT 'Customers: ' || COUNT(*) FROM test_customers;
SELECT 'Orders: ' || COUNT(*) FROM test_orders;
SELECT 'Order Items: ' || COUNT(*) FROM test_order_items;
SELECT 'Products: ' || COUNT(*) FROM test_products;
