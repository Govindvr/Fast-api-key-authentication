# Fast-api-key-authentication
REST API using FastAPI for a key based authentication using psql database.

Python version used : `3.10.6`

## Setup
1. Clone the repository
2. Create a virtual environment
3. Install the requirements
4. Create a `.env` and add the following variables
```bash
DATABASE_URL=<postgresql://username:password@host/name>

```

To install the required packages
```bash
pip  install -r requirements.txt
```
To Run the app
```bash
python app/main.py
```

The app will be availiable on http://localhost:8000/

## API Endpoints
1. POST /register - Registers a new user with the specified data.
2. POST /user/authenticate - Authenticates the user with the specified data.
3. GET /user - Returns the user data.
