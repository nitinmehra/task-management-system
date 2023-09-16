# Task-Management-System Readme

Welcome to the [Project Name] project!

## Prerequisites

Before you begin, make sure you have the following installed on your system:

- Python ([Download Python](https://www.python.org/downloads/))
- PostgreSQL ([Download PostgreSQL](https://www.postgresql.org/download/))
- Git ([Download Git](https://git-scm.com/downloads))

## Setup

Follow these steps to set up your project:

### 1. Clone the Repository

Clone this Git repository to your local machine:

```bash
git clone https://github.com/nitinmehra/task-management-system.git
cd your-repo

### 2. Create a Virtual Environment

python -m venv venv
source venv/bin/activate 

### 3. Install Project Requirements

pip install -r requirements.txt

### 4. Set Up PostgreSQL

Install PostgreSQL (if not already installed)

Create a Database and User
```bash
    psql -U postgres

    CREATE DATABASE task_management_system;
    CREATE USER root WITH PASSWORD 'root';
    GRANT ALL PRIVILEGES ON DATABASE task_management_system TO root;

Exit the PostgreSQL shell:
```bash
    \q

### 5. Run Migrations
```bash
    python manage.py migrate

### 6. Start the Development Server
```bash
    python manage.py runserver

Your project should now be running at http://localhost:8000.

## Usage
A postman collection is added in repository
--User API's
-create user
-login user and get token for authentication
--Task API's
-create Task
-update Task
-view Task
-list Task
-Delete Task

### swagger documentation 
url: http://localhost:8000/swagger/




