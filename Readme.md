# Digilib - Library Management System

Digilib is a library management system built as a mini-project for our college. It provides a user-friendly interface for students, faculty, and library staff to manage library resources efficiently. This repository contains the backend code for Digilib, built using FastAPI, MongoDB, and integrates with Cloudinary for storing book images.

## Features

- **User Authentication**: Digilib has three main user roles - Admin, Issuer, and User (students and faculty). Each user can register and login to access their specific functionalities.

- **Book Reservation**: Users can reserve a book in advance, even if it is currently out of stock. The system maintains a priority queue for each reserved book, and when the book becomes available, it is automatically issued to the top priority user in the queue.

- **Admin Privileges**: Admin users have special privileges, such as managing books, users, and issuers. They can add new books, update book details, view book borrowing history, and perform other administrative tasks.

- **Book Management**: Users can search for books, view book details, and check their availability status.

- **User Profile**: Users can view and update their profiles, including personal information and borrowing history.

## Tech Stack

- **FastAPI**: FastAPI is used to develop the backend of Digilib, providing a high-performance web framework with automatic validation, serialization, and OpenAPI support.

- **MongoDB**: MongoDB is used as the database to store user information, book details, reservations, and other relevant data.

- **Cloudinary**: Digilib integrates with Cloudinary for storing and managing book images securely in the cloud.

## Installation

1. Clone this repository to your local machine.

```bash
git clone https://github.com/anandukch/DigiLib-backend.git
cd DigiLib-backend
```

2. Create a virtual environment and activate it.

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the dependencies.

```bash
poetry install
```


4. Create a `.env` file in the root directory and add the following environment variables.

```bash
MONGO_URL=<MongoDB connection URI>
```

5. Run the server.

```bash
./run.sh
```

6. Run using Docker.

```bash
docker-compose up
```


## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB](https://www.mongodb.com/)
- [Cloudinary](https://cloudinary.com/)




