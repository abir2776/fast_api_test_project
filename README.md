# 🚀 fast_api_test_project

This is a Python-based project built with FastAPI. You can run it either using a virtual environment or with Docker.

---

## 📦 Requirements

- Python 3.10+
- pip
- Docker & Docker Compose (if using Docker)

---

## 🧪 Running the Project without Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/abir2776/fast_api_test_project.git
   cd fast_api_test_project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the server**
   ```bash
   uvicorn app.main:app --reload
   ```

---

## 🐳 Running the Project with Docker

1. **Run the following command**
   ```bash
   sudo docker compose up --build
   ```

---

## 🌐 Access the API

Once running, the API will be available at:
```
http://localhost:8000
```

You can view the interactive Swagger documentation at:
```
http://localhost:8000/news
```

---

## 📁 Project Structure

```
.
├── app/
│   └── auth.py
    └── database.py
    └── deps.py
    └── main.py
    └── models.py
    └── routes.py
    └── schemas.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```