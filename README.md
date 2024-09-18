# Blog Management System

## Overview

This project is a Flask-based web application that supports user authentication, blog management, and more. It utilizes a combination of SQLAlchemy and PyMongo to interact with SQL and MongoDB databases, respectively. The application provides flexibility to switch between these two types of databases based on your needs.

## Setup Instructions

### Prerequisites

- **Python**: Ensure that Python 3.7 or higher is installed on your system.
- **pip**: Make sure `pip` is installed and updated.

### Installation

1. **Clone the Repository**

  - **Clone the repository from GitHub:**

    git clone https://github.com/HassanAbdelhamed22/blog-management-system

    cd blog-management-system

2. **Create a Virtual Environment**

  - **It's a good practice to use a virtual environment to manage dependencies:**

    python -m venv venv

3. **Activate the Virtual Environment**

  - **venv/Scripts/activate**

4. **Install Dependencies**

  - **pip install flask flask-bcrypt flask-injector flask-login flask-pymongo flask-sqlalchemy flask-wtf pymongo sqlalchemy**

5. **Set Up Environment Variables**

  - **Create a .env file in the root directory and add the necessary environment variables. Example:**

    FLASK_APP=app
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    SQLALCHEMY_DATABASE_URI=sqlite:///blog.db
    MONGO_URI=mongodb://localhost:27017/blog

6. **Run the Application**

  - **python main.py**

## Switching Between SQL and MongoDB
This project supports both SQL and MongoDB as database backends. To switch between them, follow these steps:

1. **Configuration**

  - **In the .env file, set the DATABASE_BACKEND variable to specify which database to use:**
    for SQL: DATABASE_BACKEND=sql
    for MongoDB: DATABASE_BACKEND=mongo

2. **Modify Model Layer**

  - **Based on the value of DATABASE_BACKEND, update the model layer in application. The core logic should be in separate classes or modules to support both types of databases.**
  
  - **SQL Model Layer: Implement models using SQLAlchemy.**
  - **MongoDB Model Layer: Implement models using PyMongo.**

3. **Service Layer**  

  - **Modify service classes to accommodate both SQL and MongoDB. For example:**

    from flask import current_app

    class BlogService:

        def __init__(self):

            self.backend = current_app.config    ['DATABASE_BACKEND']

            if self.backend == 'sql':

                from app.services.sql_blog_service import SQLBlogService

                self.blog_service = SQLBlogService()
            elif self.backend == 'mongo':

                from app.services.mongo_blog_service import     MongoBlogService

                self.blog_service = MongoBlogService()

