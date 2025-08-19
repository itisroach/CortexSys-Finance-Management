# Finance Management API

A lightweight and robust API for managing personal and small business finances efficiently. Track income, expenses, budgets, and financial goals securely and in an organized manner.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Technologies Used](#technologies-used)
4. [Installation](#installation)
5. [Usage](#usage)
6. [API Endpoints](#api-endpoints)
7. [Getting Started with Examples](#getting-started-with-examples)
8. [Project Structure](#project-structure)
9. [Database Models](#database-models)

---

## Project Overview

The **Finance Management API** is built using Django REST Framework and PostgreSQL. It allows users to:

* Track personal or business finances.
* Categorize transactions by type (income/expense).
* Manage budgets.
* Generate financial reports.
* Ensure secure user authentication with JWT tokens.

---

## Key Features

* **Transactions**: Create, edit, delete income and expense records.
* **Categories**: Assign categories to transactions.
* **Budgets**: Set budgets with start and end dates; receive a message when exceeded.
* **Reports**: Get a summary of income, expenses, and account balance.
* **Notifications**: Receive in-app notifications when budgets are exceeded.
* **User Authentication**: Register, login, and secure access using JWT.

---

## Technologies Used

* **Backend**: Django, Django REST Framework
* **Database**: PostgreSQL
* **Authentication**: JWT (JSON Web Token)
* **Testing**: pytest
* **Notification**: Firebase Message Service
* **Admin Panel**: Django Admin

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/itisroach/CortexSys-Finance-Management.git
cd CoretxSys-Finance-Management
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a project in firebase and save json file which contains project credentials and save it project folder and add its path to an .env file.

5. Apply migrations:

```bash
python manage.py migrate
```
6. Create a superuser (optional for admin panel):

```bash
python manage.py createsuperuser
```

7. Run the development server:

```bash
python manage.py runserver
```

---

## Usage

* Register a new user via `/api/auth/register/`.
* Login to obtain JWT token via `/api/auth/login/`.
* Use the token to authenticate API requests.
* Use `/api/device-tokens/` to create a device token which receives notifications. 
* Create transactions, budgets, and view or edit or delete them.

---

## API Endpoints

| Method              | Endpoint                    | Description                |
| ------------------- | --------------------------- | -------------------------- |
| POST                | `/api/auth/register/`       | Register new user          |
| POST                | `/api/auth/login/`          | Login and get JWT token    |
| POST                | `/api/auth/refresh/`        | Refresh JWT token          |
| GET/POST            | `/api/transactions/`        | Get or create for transactions      |
| PUT/PATCH/DELETE    | `/api/transactions/{id}/`   | Update or delete for transactions      |
| GET/POST            | `/api/budgets/`             | Get or create for budgets           |
| PUT/PATCH/DELETE    | `/api/budgets/{id}/`        | Update or delete for budgets           |
| GET                 | `/api/transactions/report/` | Get income/expense summary |
| GET/POST            | `/api/device-tokens/`             | Get or create for device tokens           |
| PUT/PATCH/DELETE    | `/api/device-tokens/{id}/`   | Update or delete for device tokens      |

---

## Getting Started with Examples

### Register User

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
-H "Content-Type: application/json" \
-d '{"phone_number": "+989123456789", "name": "John Doe", "password": "strongpassword"}'
```

### Login

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
-H "Content-Type: application/json" \
-d '{"phone_number": "+989123456789", "password": "strongpassword"}'
```

### Create a Budget

```bash
curl -X POST http://127.0.0.1:8000/api/budgets/ \
-H "Authorization: Bearer <your_jwt_token>" \
-H "Content-Type: application/json" \
-d '{"title": "First Budget", "total_amount": 1000, "start_date": "2025-01-01", "end_date": "2025-01-31"}'
```

### Create a Transaction

```bash
curl -X POST http://127.0.0.1:8000/api/transactions/ \
-H "Authorization: Bearer <your_jwt_token>" \
-H "Content-Type: application/json" \
-d '{"title": "Office Supplies", "amount": 100, "type": "expense", "date": "2025-01-05"}'
```

### Get Financial Report

```bash
curl -X GET http://127.0.0.1:8000/api/transactions/report/ \
-H "Authorization: Bearer <your_jwt_token>"
```

### Get Device Token

```bash
curl -X GET http://127.0.0.1:8000/api/device-tokens/ \
-H "Authorization: Bearer <your_jwt_token>"
```

### Create Device Token

```bash
curl -X POST http://127.0.0.1:8000/api/transactions/report/ \
-H "Authorization: Bearer <your_jwt_token>"
-d '{"token": "for_firebase_device_token"}'
```

## Project Structure

```
finance_management/
├── accounts/        # User authentication
├── transactions/    # Income and expense management
├── finance_management/ # Project settings
├── budgets/         # Budget management
├── manage.py
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## Database Models

### User

* Custom user model with phone number, name and password.

### Transaction

* Fields: `title`, `amount`, `type` (income/expense), `date`, `notes`, `user_id`.

### Budget

* Fields: `title`, `total_amount`, `start_date`, `end_date`, `user_id`.
* Validates that `end_date` ≥ `start_date`.

### Device Token

* Fields: `id`, `user`, `token`.
