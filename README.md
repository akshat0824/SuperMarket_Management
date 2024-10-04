# Supermarket Management System

## Overview

The **Supermarket Management System** is a web application built using Flask, designed to manage products and customers in a supermarket setting. It allows users to register, log in, manage product and customer information, and perform sales transactions. The application also includes search functionality for easy retrieval of products and customers.

## Features

- User registration and login
- Product management (add, delete, search)
- Customer management (add, delete, search)
- Record sales transactions
- Responsive design with Bootstrap

## Technologies Used

- **Backend**: Flask
- **Database**: SQLite (via SQLAlchemy)
- **Frontend**: HTML, CSS (Bootstrap)
- **User Authentication**: Flask-Login
- **Email Integration**: Flask-Mail (not implemented yet)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/akshat0824/SuperMarket_Management.git
   cd SuperMarket_Management
   
  
2.Create a virtual environment:
   ```bash
  python -m venv venv
  ```
3.Activate the virtual environment:
  On Windows:
  ```bash
  venv\Scripts\activate
  ```
  4.On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```
  5.Install the required packages:
  ```bash
  pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF Flask-Mail itsdangerous
  ```

  6.Initialize the database:
  You may need to create the database tables by running a script or using the Flask shell.
  ```bash
   python
   From app import app,db
   with app.app_context():
   Db.create_all()
  ```   

  Usage
  Start the application:
  ```bash
  python app.py
  ```
  Open your web browser and navigate to http://127.0.0.1:5000/.
  Register a new user account or log in with an existing account.
  Use the dashboard to manage products and customers.
  Perform sales transactions as needed.
  
  Future Enhancements
  Implement email integration for password recovery and username retrieval.
  Add user roles (admin, staff) for better access control.
  Improve UI/UX with more advanced frontend frameworks.
  Implement unit tests for better code reliability.
  
  Contributing
  Contributions are welcome! Please feel free to submit a pull request or open an issue for any improvements or bugs you find.
  
