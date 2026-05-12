# Task Manager

A specialized web application for managing workflows, organizing tasks, and tracking progress within a collaborative environment. This project focuses on a clean implementation of task assignment, status tracking, and categorization using a relational database.

## Project Overview

Task Manager is a multi-user platform designed to streamline internal project coordination. It allows for the creation of tasks, assignment of responsible parties, and the categorization of work items through a flexible system of statuses and labels.

The application supports public user registration, enabling anyone to create an account and begin managing their own tasks or collaborating with others.

## Main Features

### User Authentication and Management
* **Registration and Profiles:** Full support for user sign-up and profile management.
* **Security:** Secure login and logout functionality to protect user data and task privacy.
* **Account Control:** Users can modify their data or delete their accounts, provided they are not currently linked to active tasks.

### Task Control
* **Full CRUD Operations:** Comprehensive ability to create, view, edit, and remove tasks.
* **Responsibility Tracking:** Each task is linked to an Author (creator) and an Executor (assigned user).
* **Deletion Protection:** A safety mechanism ensures that only the creator of a task has the authority to delete it.

### Status and Label System
* **Custom Statuses:** The ability to define the lifecycle of a task (e.g., Planned, In Progress, Under Review, Completed).
* **Many-to-Many Labeling:** Tasks can be tagged with multiple labels for better organization and grouping across different projects or themes.

## Database Setup

To populate the database with initial data, run:

```bash
python manage.py loaddata data.json
```

## Credentials

You can use the following credentials to access the admin panel or test the application. Note that the password is the same for all pre-configured users in the system:

* **Username:** admin
* **Password:** RpfpQ87$

## Tech Stack

* **Language:** Python 3.14
* **Framework:** Django 6.0.5
* **Database:** SQLite
* **Frontend:** Django Templates with Bootstrap integration

## Author

**Artem Radkevych**