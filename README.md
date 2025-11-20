# Finance Tracker

A personal finance tracking application designed to help you manage your finances effectively.

## Tech Stack

### Backend
- **Framework:** FastAPI
- **Database ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Database Driver:** asyncpg
- **Package Manager:** Poetry

### Frontend
- **Library:** React
- **Build Tool:** Vite
- **Styling:** TailwindCSS
- **Language:** TypeScript

## Prerequisites

- Python >= 3.13
- Node.js (Latest LTS recommended)
- PostgreSQL

## Installation

### Backend Setup

1.  Navigate to the project root directory.
2.  Install dependencies using Poetry:

    ```bash
    poetry install
    ```

3.  Create a `.env` file in the root directory and configure your environment variables (e.g., `DATABASE_URL`).

### Frontend Setup

1.  Navigate to the `frontend` directory:

    ```bash
    cd frontend
    ```

2.  Install dependencies:

    ```bash
    npm install
    ```

## Database Setup

Run database migrations to set up the schema:

```bash
poetry run alembic upgrade head
```

## Running the Application

### Backend

Start the FastAPI server:

```bash
poetry run uvicorn src.finance_tracker.app:app --reload
```

The API will be available at `http://localhost:8000`.

### Frontend

Start the React development server:

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`.

## API Documentation

Once the backend is running, you can access the interactive API documentation at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/finance_tracker

# Frontend API URL (used by Vite)
VITE_API_BASE_URL=http://localhost:8000
```

Replace `username` and `password` with your PostgreSQL credentials.

