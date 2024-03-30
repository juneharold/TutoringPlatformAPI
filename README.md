# Tutor-Tutee Meeting API

## Description

The Tutor-Tutee Meeting API is a Flask-based RESTful API designed to facilitate 1:1 meeting arrangements between tutors and tutees. It supports managing availability for tutors, class bookings for tutees, and handles various class-related operations. This project aims to simplify the scheduling process for educational sessions, making it easier for tutors to open their availability and for tutees to find and register for classes.

## Features

- **Tutor Availability Management**: Tutors can create, update, and delete their available times.
- **Class Registration**: Tutees can search for available classes based on time slots or tutor availability and register for classes.
- **Flexible Scheduling**: Supports 30-minute and 60-minute classes, ensuring that each class starts only at the beginning of the hour or half-hour.
- **Persistent Storage**: Uses SQLAlchemy with SQLite for data persistence, ensuring data is saved across service restarts.

## Endpoints

### Tutor Availability
- `POST /api/add_time`: Add availability for a tutor.
- `DELETE /api/delete_time`: Remove a specific availability slot for a tutor.

### Tutee Search Classes
- `GET /api/find_classes`: Find possible times to have classes for a specified time period.
- `GET /api/find_tutors`: Find available tutors in a specific day of week and time of day.

### Register and View Classes
- `PUT /api/register_class`: Register for a class.
- `GET /api/view_registered_class`: View registered classes.

## Installation

Ensure you have Python 3 and pip installed on your system.

1. Clone the repository:
```bash
git clone https://github.com/juneharold/TutoringPlatformAPI.git
```

2. Navigate to the project directory:
```bash
cd TutoringPlatformAPI
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## How To Run

From the root directory of the project, run the following command:

```bash
python3 app.py
```

This will start the Flask application on `http://127.0.0.1:5000/`.

## How To Test

The project includes automated test scripts for testing all the API endpoints. Make sure to have **curl and jq** installed. The test cases have to be run in order for the code to output correctly. To run these tests:

```bash
cd tests
./run_all_tests.sh
```

Ensure you have granted execution permissions to the test scripts:

```bash
chmod +x ./testcase_scripts/*.sh
chmod +x run_all_tests.sh
```


