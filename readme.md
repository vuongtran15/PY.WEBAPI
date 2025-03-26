# Python Web API Project

This repository contains a Python-based Web API project.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd PY.WEBAPI
   ```

2. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

### Development Mode

To run the application in development mode:

```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

The API will be accessible at `http://127.0.0.1:5000/` by default.

### Production Mode

For production deployment, it's recommended to use a WSGI server like Gunicorn:

```bash
gunicorn app:app
```

## API Documentation

The API documentation is available at `/docs` or `/redoc` endpoints when the server is running.

## Project Structure

```
PY.WEBAPI/
├── app.py          # Main application entry point
├── api/            # API routes and controllers
├── models/         # Data models
├── services/       # Business logic
├── config/         # Configuration files
├── tests/          # Test cases
└── requirements.txt # Project dependencies
```

## Running Tests

```bash
pytest
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
DEBUG=True
DATABASE_URL=sqlite:///database.db
SECRET_KEY=your_secret_key
```

## License

[MIT](LICENSE)
