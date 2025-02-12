# FastAPI JWT Auth Starter

This project is a starter template for building a FastAPI application with JWT-based authentication.

## Features

- FastAPI framework
- JWT authentication
- User registration and login
- Protected routes

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/aykut-canturk/fastapi-jwt-auth-starter.git
    cd fastapi-jwt-auth-starter
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running with Uvicorn

1. Run the application:
    ```bash
    uvicorn run:app --reload
    ```

2. Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the Swagger UI.

### Running with Docker

1. Ensure you have Docker and Docker Compose installed on your machine.

2. Run the Docker Compose application:
    ```bash
    docker compose up -d
    ```

3. Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the Swagger UI.

## Project Structure

```
/fastapi-jwt-auth-starter/
├── app
│   ├── config.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── database.py
│   │   └── user.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── user.py
│   ├── schemas
│   │   ├── base.py
│   │   └── user.py
│   ├── security.py
│   ├── services
│   │   ├── base.py
│   │   └── user.py
│   └── utils
│       ├── crypto.py
│       ├── exception.py
│       ├── logger.py
│       └── starter.py
├── data
│   └── database.db
├── docker-compose.yml
├── logs
│   └── application.log
├── requirements.txt
└── run.py
├── .gitignore
├── requirements.txt
├── Dockerfile
├── LICENSE
├── README.md

```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License.
