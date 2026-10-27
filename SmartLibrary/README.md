# 📚 Smart Library Management System

A robust, enterprise-grade, console-based Library Management and Inventory Control System built in **Python** and backed by **MySQL**. The system incorporates strict database transaction isolation, role-based access control (RBAC), secure cryptographic password hashing, and complete financial and inventory auditing.

---

## 🚀 Key Features

* **Role-Based Access Control (RBAC):** Supports distinct system roles with strictly enforced permission boundaries (`Admin`, `Finance Manager`, and `Customer`).
* **Secure Authentication:** Utilizes **Argon2** password hashing (`auth.py`) for state-of-the-art credential security and verification.
* **Advanced Inventory & Stock Management:** 
  * Real-time tracking of book quantities (Total, Available, and Borrowed).
  * Atomic transactions with row-level locking (`FOR UPDATE`) to prevent race conditions during concurrent borrowing, purchasing, and sales.
* **Borrowing & Return Lifecycle:** Automated due date calculation (14-day default), partial returns support, and fine-grained quantity tracking.
* **Financial Auditing & Reporting:** Dedicated services for generating real-time sales reports, purchase histories, inventory valuations, and gross profit analytics restricted strictly to authorized financial roles.
* **Robust Error Handling & Rollbacks:** Comprehensive exception handling and transaction rollbacks (`connection.rollback()`) to maintain database integrity upon failure.

---

## 🛠️ Technology Stack

* **Language:** Python 3.x
* **Database:** MySQL (Relational Database Management System)
* **Database Connectivity:** `mysql-connector-python`
* **Security/Hashing:** `argon2-cffi`
* **Testing & Validation:** Python standard libraries (`unittest.mock`, custom automated test suites)

---

## 📂 Project Architecture

The project follows a clean, modular, and separation-of-concerns architecture:

```text
Smart_Library/
│
├── database/               # Database connectivity & data access layer
│   ├── connection.py       # MySQL database connection handler
│   ├── book_repository.py  # Book data access operations[cite: 6]
│   ├── borrow_repository.py# Borrow records data access[cite: 7]
│   ├── purchase_repository.py# Purchase transactions data access[cite: 10]
│   ├── sale_repository.py  # Sales transactions data access[cite: 11]
│   ├── user_repository.py  # User management data access[cite: 12]
│   └── library.sql         # Complete database schema & relational constraints
│
├── models/                 # Object-Oriented Domain Entities
│   ├── book.py             # Book entity definition[cite: 13]
│   ├── borrow.py           # Borrow entity & date logic[cite: 14]
│   └── user.py             # User entity definition[cite: 15]
│
├── services/               # Core Business Logic & Security
│   ├── auth.py             # Argon2 password hashing & verification[cite: 16]
│   ├── library.py          # Central business controller & transaction engine[cite: 17]
│   ├── report_access.py    # RBAC rules for financial reporting[cite: 18]
│   └── report_service.py   # Financial analytics & report aggregators[cite: 19]
│
├── main.py                 # Application entry point & CLI interface[cite: 20]
├── requirements.txt        # External Python dependencies
├── test_borrow_return.py   # Borrow/Return lifecycle tests[cite: 21]
├── test_connection.py      # DB connection verification[cite: 22]
├── test_purchase_sale.py   # Purchase & Sales stock flow tests[cite: 23]
├── test_report_access.py   # RBAC permission checks[cite: 24]
├── test_report_service.py  # Analytics report verification[cite: 25]
├── test_sale_rollback.py   # Transaction rollback validation[cite: 26]
└── test_user_flow.py       # User registration & auth flow[cite: 27]
```

---

## 📊 Database Schema Overview

The relational database (`smart_library`) consists of 5 core tables structured with strict foreign key constraints and cascade rules:
1. **`users`**: Stores user profiles, hashed credentials, contact info, and roles.
2. **`books`**: Tracks book metadata, pricing metrics, and inventory counts.
3. **`borrows`**: Manages book lending records, quantities, due dates, and return timestamps.
4. **`purchases`**: Records administrative acquisition of stock items and unit costs.
5. **`sales`**: Logs customer retail purchases and cost-of-goods-sold metrics.

---

## ⚙️ Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/smart-library.git
   cd smart-library
   ```

2. **Install Dependencies:**
   ```bash
   pip install mysql-connector-python argon2-cffi
   ```

3. **Configure Database:**
   * Import the `library.sql` script into your local MySQL server.
   * Update your database credentials in `database/connection.py` if necessary (host, user, password).

4. **Run the Application:**
   ```bash
   python main.py
   ```

---

## 🧪 Running Tests

The project includes an extensive suite of integration and transaction integrity tests:
```bash
python -m unittest discover tests
# Or run individual test scripts:
python test_borrow_return.py
python test_sale_rollback.py
```

---

## 💡 Engineering Highlights
* **ACID Compliance & Concurrency Control:** Implemented database-level row locking (`FOR UPDATE`) inside Python transaction blocks (`try-except-rollback-commit`) to guarantee zero stock discrepancies under high concurrency.
* **Separation of Concerns:** Isolated data access logic (`repositories`) completely from business rules (`services`) and domain objects (`models`), ensuring high maintainability and testability.

---

## 👤 Author
**Amna Al-Hassan**  
*Computer Engineering Graduate | Systems & Hardware-Software Co-Design Researcher*