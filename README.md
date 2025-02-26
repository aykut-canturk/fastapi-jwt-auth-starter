# FastAPI JWT Auth Starter 🚀

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
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
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

## Running the Tests

To run the tests, use the following command:

```bash
python -m unittest discover -s tests
```

Make sure you have `unittest` installed. It is included in the Python standard library, so no additional installation is required.

## Project Structure

```
fastapi-jwt-auth-starter/
├── app/                    # Application source code
│   ├── config.py
│   ├── models/             # Data models
│   ├── routes/             # API routes
│   ├── schemas/            # Request/response schemas
│   ├── security.py
│   ├── services/           # Business logic
│   └── utils/              # Utility functions
├── data/                   # Database and other data files
├── logs/                   # Application log files
├── tests/                  # Test files
├── run.py                  # Application entry point
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── .gitignore              # Files to be ignored by Git
├── LICENSE                 # License information
└── README.md               # Project documentation
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License.
