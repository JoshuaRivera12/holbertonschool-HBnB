# HBnB – Authentication & Database Integration

Welcome to **Part 3** of the **HBnB Project**!

In this phase, we’ll enhance the backend by introducing:

- 🔐 **User Authentication**
- 🛂 **Role-Based Access Control**
- 🗄️ **Persistent Storage** using **SQLite** and **SQLAlchemy**
- 🚀 **Production-Ready Setup** with **MySQL**

This stage focuses on improving security, enabling persistence, and preparing the backend for scalable deployment.

---

## 🧱 Project Overview

This part of the project gradually builds a secure, database-driven backend that’s suitable for real-world applications.

---

## ✅ Goals

- Secure password storage in the `User` model using `bcrypt`
- Implement JWT-based authentication
- Restrict access through role-based authorization
- Use SQLite for development storage
- Define data models with SQLAlchemy ORM
- Configure MySQL for production use
- Visualize the database schema using Mermaid.js

---

## 🧩 Tasks

### 1. Enhance the User Model
- Hash passwords using `bcrypt`
- Update registration logic to store hashed credentials

### 2. Add JWT Authentication
- Create login routes that issue JWT tokens
- Protect endpoints by requiring a valid token

### 3. Implement Role-Based Authorization
- Define user roles such as `admin` and `user`
- Restrict sensitive routes based on role permissions

### 4. Set Up SQLite for Development
- Replace in-memory storage with SQLite
- Use environment variables to toggle between development and production databases

### 5. Use SQLAlchemy for ORM
- Map and create models: `User`, `Place`, `Review`, `Amenity`
- Establish relationships between models

### 6. Configure MySQL for Production
- Set up SQLAlchemy to connect to a MySQL database
- Dynamically switch databases using environment configs

### 7. Visualize with Mermaid.js
- Design and maintain an Entity Relationship Diagram (ERD)
- Use Mermaid.js to keep your schema visualization up to date

---

## 🛠️ Technologies Used

- Python + Flask
- SQLAlchemy
- SQLite / MySQL
- bcrypt
- JWT (via PyJWT)
- Mermaid.js

---

## 📈 Example: Mermaid.js ER Diagram

```mermaid
erDiagram
    USER ||--o{ PLACE : owns
    USER ||--o{ REVIEW : writes
    PLACE ||--o{ REVIEW : has
    PLACE ||--o{ AMENITY : offers

    USER {
        string id PK
        string email
        string password
    }

    PLACE {
        string id PK
        string name
        string description
        string user_id FK
    }

    REVIEW {
        string id PK
        string text
        string user_id FK
        string place_id FK
    }

    AMENITY {
        string id PK
        string name
    }

