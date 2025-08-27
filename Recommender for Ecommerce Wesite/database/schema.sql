CREATE DATABASE IF NOT EXISTS BookStore
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

-- Chọn database để sử dụng
USE BookStore;

-- ========================
-- 1. Bảng tác giả
-- ========================
CREATE TABLE IF NOT EXISTS author (
    AuthorID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Bio TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ========================
-- 2. Bảng nhà xuất bản
-- ========================
CREATE TABLE IF NOT EXISTS publisher (
    PublisherID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Address VARCHAR(255),
    Phone VARCHAR(20)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ========================
-- 3. Bảng thể loại
-- ========================
CREATE TABLE IF NOT EXISTS category (
    CategoryID INT AUTO_INCREMENT PRIMARY KEY,
    CategoryName VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ========================
-- 4. Bảng sách
-- ========================
CREATE TABLE IF NOT EXISTS book (
    BookID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    AuthorID INT,
    PublisherID INT,
    ISBN VARCHAR(20) UNIQUE,
    Year INT,
    Price DECIMAL(10,2) NOT NULL,
    Stock INT NOT NULL,
    CategoryID INT,
    Description TEXT,
    ImageURL VARCHAR(500),
    FOREIGN KEY (AuthorID) REFERENCES author(AuthorID),
    FOREIGN KEY (PublisherID) REFERENCES publisher(PublisherID),
    FOREIGN KEY (CategoryID) REFERENCES category(CategoryID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ========================
-- 5. Bảng khách hàng
-- ========================
CREATE TABLE IF NOT EXISTS customer (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    FullName VARCHAR(255) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Phone VARCHAR(20),
    Address VARCHAR(255),
    PasswordHash VARCHAR(255) NOT NULL,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ========================
-- 6. Bảng đơn hàng
-- ========================
CREATE TABLE IF NOT EXISTS orders (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    OrderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    TotalAmount DECIMAL(10,2) NOT NULL,
    Status VARCHAR(50) DEFAULT 'Pending', -- Pending, Paid, Shipped, Cancelled
    FOREIGN KEY (CustomerID) REFERENCES customer(CustomerID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ========================
-- 7. Bảng chi tiết đơn hàng
-- ========================
CREATE TABLE IF NOT EXISTS orderdetail (
    OrderDetailID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT NOT NULL,
    BookID INT NOT NULL,
    Quantity INT NOT NULL,
    Price DECIMAL(10,2) NOT NULL, -- Giá tại thời điểm đặt
    FOREIGN KEY (OrderID) REFERENCES orders(OrderID),
    FOREIGN KEY (BookID) REFERENCES book(BookID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ========================
-- 8. Bảng thanh toán
-- ========================
CREATE TABLE IF NOT EXISTS payment (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT NOT NULL,
    PaymentDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    Amount DECIMAL(10,2) NOT NULL,
    Method VARCHAR(50),   -- Ví dụ: CreditCard, COD, Momo, VNPay
    Status VARCHAR(50),   -- Paid, Pending, Failed
    FOREIGN KEY (OrderID) REFERENCES orders(OrderID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ========================
-- 9. Bảng hoạt động người dùng (cho recommendation system)
-- ========================
CREATE TABLE IF NOT EXISTS useractivity (
    ActivityID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    BookID INT NOT NULL,
    Action ENUM('view', 'add_to_cart', 'checkout', 'purchase') NOT NULL,
    ActivityTime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    SessionID VARCHAR(50),
    FOREIGN KEY (CustomerID) REFERENCES customer(CustomerID),
    FOREIGN KEY (BookID) REFERENCES book(BookID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
