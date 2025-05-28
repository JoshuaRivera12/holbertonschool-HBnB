# HBnB Evolution - Technical Documentation

## Part 1: Context and Objective

This document outlines the architecture and business logic design for a simplified AirBnB-like application called **HBnB Evolution**. It covers core components, their interactions, and technical diagrams using UML to guide implementation.

---

## 📌 Problem Description

### Main Functionalities

- **User Management**  
  Register, update, delete, and identify users (admin or regular).

- **Place Management**  
  Create, update, delete, list places. Each place includes title, description, price, location, and amenities.

- **Review Management**  
  Add and manage reviews with ratings and comments tied to places and users.

- **Amenity Management**  
  Maintain amenities that can be attached to places.

---

## 📋 Business Rules & Requirements

### User
- Fields: `first_name`, `last_name`, `email`, `password`, `is_admin`
- Actions: Register, Update, Delete

### Place
- Fields: `title`, `description`, `price`, `latitude`, `longitude`
- Owned by a User
- Linked with multiple amenities
- Actions: CRUD

### Review
- Fields: `rating`, `comment`
- Linked to a User and a Place
- Actions: CRUD (by Place)

### Amenity
- Fields: `name`, `description`
- Linked to many Places
- Actions: CRUD

### Common to All
- Unique ID
- `created_at`, `updated_at` timestamps

---

## 🏗 Architecture and Layers

```mermaid
graph TD
  A[Presentation Layer<br>API/Services] --> B[Business Logic Layer<br>Models & Rules]
  B --> C[Persistence Layer<br>Database Access]

  A -.->|Facade Pattern| B
  B -->|ORM / Queries| C

