# Let's Schedule

Let's Schedule is an open-source API designed for scheduling events, with seamless integration to Google Calendar and additional platforms. Built using Python, FastAPI, SQLAlchemy, and PostgreSQL, this project aims to provide a robust and flexible solution for managing and synchronizing events across various services.

## Features

- **FastAPI**: Leverage the speed and simplicity of FastAPI for building the API.
- **SQLAlchemy**: Use SQLAlchemy for ORM capabilities, making database interactions intuitive and efficient.
- **PostgreSQL**: Utilize PostgreSQL for a reliable and powerful database solution.
- **Google Calendar Integration**: Connect and synchronize with Google Calendar for seamless event management.
- **Extensible Architecture**: Easily add more integrations and features to suit your needs.
- **RESTful API**: Designed with RESTful principles for easy integration and use.

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- Google Cloud account for API integration

### Installation

1. **Clone the repository:**

   ```bash
   git clone git@github.com:ruslan-korneev/lets-schedule.git
   cd lets-schedule
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python3.13 -m venv .venv
   source .venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   poetry install
   ```

4. **Set up PostgreSQL:**

   - Create a new PostgreSQL database.
   - Update the `DATABASE_URL` in the `.env` file with your database credentials.

5. **Set up Google Calendar API:**

   - Follow [Google Calendar API Quickstart](https://developers.google.com/calendar/quickstart/python) to obtain your credentials.
   - Save the `credentials.json` file to the project root.

6. **Run database migrations:**

   ```bash
   alembic upgrade head
   ```

7. **Start the server:**

   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at `http://localhost:8000`.

## Usage

- **API Documentation**: Access interactive API documentation at `http://localhost:8000/docs`.
- **Event Management**: Create, update, delete, and list events using the API endpoints.
- **Google Calendar Sync**: Automatically synchronize your events with Google Calendar.

## Configuration

Configuration is managed via environment variables. Refer to the `.env.example` file for a list of configurable options.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For questions or feedback, please contact [admin@ruslan.beer](mailto:admin@ruslan.beer).
