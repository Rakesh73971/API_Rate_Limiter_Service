# 🚀 API Rate Limiter Service

A production-ready backend system built using FastAPI that provides **JWT authentication, role-based rate limiting, request logging, and Redis-powered request tracking**.

This project simulates how real-world systems protect APIs from abuse and ensure fair usage across users.

---

## 📌 Features

* 🔐 JWT Authentication (Login & Secure APIs)
* ⚡ High-performance Rate Limiting using Redis
* 👥 Role-Based Limits (Free, Premium, Admin)
* 🗄️ PostgreSQL for persistent data storage
* 📊 Automatic Request Logging (Middleware-based)
* 🐳 Dockerized Application (Containerized setup)
* 🔁 CI/CD Pipeline using GitHub Actions
* 📈 Scalable and production-ready architecture

---

## 🏗️ Tech Stack

* **Backend Framework:** FastAPI
* **Database:** PostgreSQL
* **Cache / Rate Limiting:** Redis
* **Authentication:** JWT (OAuth2)
* **ORM:** SQLAlchemy
* **Containerization:** Docker
* **CI/CD:** GitHub Actions

---

## ⚙️ Project Architecture

```
Client Request
      ↓
JWT Authentication
      ↓
Get User Role
      ↓
Fetch Rate Limit Rule (PostgreSQL)
      ↓
Check Counter (Redis)
      ↓
Request Allowed / Blocked
      ↓
Request Logging (PostgreSQL)
```

---

## 🔐 Authentication

* Uses JWT tokens for secure access.
* Users must log in to receive an access token.

### Login Endpoint

```
POST /login
```

---

## 🚦 Rate Limiting

Rate limits are applied based on user roles:

| Role         | Requests | Time Window |
| ------------ | -------- | ----------- |
| free_user    | 10       | 60 sec      |
| premium_user | 100      | 60 sec      |
| admin        | 1000     | 60 sec      |

* Limits are stored in PostgreSQL
* Request counts are tracked in Redis

---

## 📊 Request Logging

* Every request is automatically logged
* Includes:

  * user_id
  * endpoint
  * status (allowed / blocked)
  * timestamp

Logs can be accessed via API (read-only).

---

## 🐳 Docker Setup

### Build and Run

```
docker-compose up --build
```

Services included:

* FastAPI app
* PostgreSQL
* Redis

---

## 🔁 CI/CD Pipeline

* Implemented using GitHub Actions
* Automatically:

  * Installs dependencies
  * Runs tests
  * Builds Docker image

---

## 🧪 API Testing

Use tools like:

* Postman
* Curl
* Swagger UI

Swagger Docs:

```
http://localhost:8000/docs
```

---

## 📈 Future Improvements

* Endpoint-based rate limiting
* Distributed rate limiting (multiple servers)
* API analytics dashboard
* Prometheus + Grafana monitoring

---

## 💡 Learnings

This project helped in understanding:

* Real-world backend system design
* Rate limiting strategies
* Redis for high-speed operations
* JWT authentication flow
* CI/CD and Docker workflows

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork and improve the project.

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 👨‍💻 Author

**Rakesh N**
Aspiring Full Stack Developer 🚀

---
