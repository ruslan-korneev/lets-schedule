# Let's Schedule

Let's Schedule is an open-source API designed for scheduling events, with seamless integration to Google Calendar and additional platforms. Built using Python, FastAPI, SQLAlchemy, and PostgreSQL, this project aims to provide a robust and flexible solution for managing and synchronizing events across various services.

## Getting Started

### Prerequisites

- Python 3.12
- PostgreSQL 17.2

### Installation

1. **Clone the repository:**

   ```bash
   git clone git@github.com:ruslan-korneev/lets-schedule.git
   cd lets-schedule
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```

   or if you are using uv

   ```bash
   uv venv
   ```

3. **Install dependencies:**

   ```bash
   poetry install  # or `uv pip install -r pyproject.toml`
   ```

4. **Set up PostgreSQL:**

   - Create a new PostgreSQL database.
   - Update the database credentials in the `.env` file with your database credentials.

5. **Run database migrations:**

   ```bash
   alembic upgrade head
   ```

6. **Start the server:**

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://0.0.0.0:8000`.

## Usage

- **API Documentation**: Access interactive API documentation at `http://0.0.0.0:8000/api/v1/docs`.
- **Event Management**: Create, update, delete, and list events using the API endpoints.
- **Google Calendar Sync**: Automatically synchronize your events with Google Calendar.

## Contact

For questions or feedback, please contact [admin@ruslan.beer](mailto:admin@ruslan.beer).
