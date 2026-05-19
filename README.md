# Cobra Kai Banking

Cobra Kai Banking is a full-stack web application built with Django that simulates a modern online banking system. This project demonstrates user authentication, account management, financial transactions, and a clean, branded user interface.

---

## Overview

Cobra Kai Banking allows users to:
- Register and log in securely
- Create a personal bank account
- Deposit and withdraw funds
- Track account balances in real time
- View transaction history

This project was designed to simulate how a real banking system manages users, accounts, and financial activity while showcasing full-stack development skills.

---

## Tech Stack

- **Backend:** Django (Python)
- **Database:** SQLite (development)
- **Frontend:** HTML, CSS (custom styling)
- **Authentication:** Django built-in auth system

---

## Features

### User Authentication
- Secure registration and login
- Session-based authentication
- Logout functionality

### Bank Account Management
- One account per user
- Unique account numbers
- Account type support, such as checking or savings

### Transactions
- Deposit funds
- Withdraw funds with validation
- Automatic balance updates
- Transaction history tracking

### Dashboard
- Displays account information
- Shows current balance
- Lists transaction history in real time

---

## Project Structure

```text
CobraKaiBanking/
|- app/
|  |- models.py
|  |- views.py
|  |- urls.py
|  |- templates/
|  |- static/
|- cobrakaibanking/
|- manage.py
|- db.sqlite3
```

---

## Installation & Setup

1. Clone the repository:

```bash
git clone https://github.com/haley09/cobra-kai-banking.git
cd cobra-kai-banking
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the environment:

```bash
venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install django whitenoise
```

5. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Start the server:

```bash
python manage.py runserver
```

7. Open in browser:

```text
http://127.0.0.1:8000
```

---

## How to Use

1. Register a new account
2. Log in
3. Create a bank account
4. Deposit funds
5. Withdraw funds
6. View transaction history on the dashboard

---

## Purpose

This project was built as a portfolio piece to demonstrate:
- Full-stack web development
- Database design and relationships
- Backend logic and validation
- User authentication systems
- Clean UI integration with backend functionality

---

## Future Improvements

- Improved UI/UX design
- Multiple account types per user
- Interest calculation automation
- API integration
- Deployment on Render, Railway, or AWS

---

## Author

Haley Abel  
Informatics Student - Indiana University Indianapolis
