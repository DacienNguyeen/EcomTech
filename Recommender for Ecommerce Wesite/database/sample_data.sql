-- Sample data for BookStore database
USE BookStore;

INSERT INTO author (Name, Bio) VALUES
('Nguyễn Nhật Ánh', 'Nhà văn chuyên viết sách thiếu nhi nổi tiếng.'),
('J.K. Rowling', 'Tác giả bộ truyện Harry Potter.'),
('Harper Lee', 'Tác giả của To Kill a Mockingbird.'),
('George Orwell', 'Tác giả 1984 và Animal Farm.'),
('Paulo Coelho', 'Tác giả The Alchemist.');

INSERT INTO publisher (Name, Address, Phone) VALUES
('NXB Trẻ', 'TP.HCM', '0281234567'),
('NXB Kim Đồng', 'Hà Nội', '0242345678'),
('Bloomsbury', 'London, UK', '+442012345678'),
('HarperCollins', 'New York, USA', '+12129876543'),
('Penguin Random House', 'London, UK', '+442076543210');

INSERT INTO category (CategoryName) VALUES
('Thiếu nhi'),
('Tiểu thuyết'),
('Kinh điển'),
('Fantasy'),
('Self-help');

INSERT INTO book (Title, AuthorID, PublisherID, ISBN, Year, Price, Stock, CategoryID, Description, ImageURL) VALUES
('Cho tôi xin một vé đi tuổi thơ', 1, 1, '9786042023456', 2010, 45000, 100, 1, 'Một trong những tác phẩm nổi bật của Nguyễn Nhật Ánh.', 'image1.jpg'),
('Harry Potter and the Philosopher''s Stone', 2, 3, '9780747532743', 1997, 120000, 200, 4, 'Tập đầu tiên trong series Harry Potter.', 'image2.jpg'),
('To Kill a Mockingbird', 3, 4, '9780061120084', 1960, 90000, 50, 3, 'Tiểu thuyết kinh điển của Harper Lee.', 'image3.jpg'),
('1984', 4, 5, '9780451524935', 1949, 85000, 70, 3, 'Tác phẩm phản địa đàng nổi tiếng.', 'image4.jpg'),
('The Alchemist', 5, 4, '9780061122415', 1988, 95000, 120, 5, 'Cuốn sách truyền cảm hứng toàn cầu.', 'image5.jpg');

INSERT INTO customer (FullName, Email, Phone, Address, PasswordHash) VALUES
('Nguyễn Văn A', 'vana@example.com', '0909123456', 'Hà Nội', 'hashedpw1'),
('Trần Thị B', 'thib@example.com', '0909765432', 'TP.HCM', 'hashedpw2'),
('Lê Văn C', 'vanc@example.com', '0912123456', 'Đà Nẵng', 'hashedpw3'),
('Phạm Thị D', 'thid@example.com', '0912345678', 'Huế', 'hashedpw4'),
('Hoàng Văn E', 'vane@example.com', '0923456789', 'Cần Thơ', 'hashedpw5');

INSERT INTO orders (CustomerID, TotalAmount, Status) VALUES
(1, 45000, 'Paid'),
(2, 120000, 'Pending'),
(3, 175000, 'Shipped'),
(4, 85000, 'Cancelled'),
(5, 95000, 'Paid');

INSERT INTO orderdetail (OrderID, BookID, Quantity, Price) VALUES
(1, 1, 1, 45000),
(2, 2, 1, 120000),
(3, 2, 1, 120000),
(3, 3, 1, 55000),
(4, 4, 1, 85000),
(5, 5, 1, 95000);

INSERT INTO payment (OrderID, Amount, Method, Status) VALUES
(1, 45000, 'Momo', 'Paid'),
(2, 120000, 'COD', 'Pending'),
(3, 175000, 'CreditCard', 'Paid'),
(4, 85000, 'VNPay', 'Failed'),
(5, 95000, 'Momo', 'Paid');

INSERT INTO useractivity (CustomerID, BookID, Action, ActivityTime, SessionID)
VALUES
(1, 1, 'view',      '2025-08-25 09:15:00', 'S1'),
(1, 2, 'view',      '2025-08-25 09:17:00', 'S1'),
(1, 1, 'add_to_cart','2025-08-25 09:20:00', 'S1'),
(2, 3, 'view',      '2025-08-25 10:05:00', 'S2'),
(2, 3, 'add_to_cart','2025-08-25 10:10:00', 'S2'),
(2, 3, 'checkout',  '2025-08-25 10:12:00', 'S2'),
(2, 3, 'purchase',  '2025-08-25 10:13:00', 'S2'),
(3, 4, 'view',      '2025-08-25 11:30:00', 'S3'),
(3, 5, 'view',      '2025-08-25 11:35:00', 'S3'),
(3, 4, 'add_to_cart','2025-08-25 11:40:00', 'S3');
