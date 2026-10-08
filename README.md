# DevTrack

DevTrack is a minimalistic backend for tracking engineering bugs, setting priorities, and updating statuses – akin to a stripped-down GitHub Issues system.

## Project Structure
- Built with Django
- Relies on JSON files (`reporters.json`, `issues.json`) instead of a traditional database to persist data.
- Object-Oriented implementations for data models.

## How to run the project
1. Ensure you have Python installed.
2. Install Django via pip (it's recommended to do this in a virtual environment):
   ```
   pip install django
   ```
3. Run the development server (make sure you are in the root directory where `manage.py` is present):
   ```
   python manage.py runserver
   ```
4. Access the API at `http://127.0.0.1:8000/api/`

## API Endpoints

### 1. Reporter Endpoints
- **Create a Reporter**
  - **POST** `/api/reporters/`
  - Body (JSON): `{"id": 1, "name": "John Doe", "email": "johndoe@example.com", "team": "backend"}`
  - Creates a new reporter and stores them in `reporters.json`.

- **Get All Reporters**
  - **GET** `/api/reporters/`
  - Returns a list of all reporters.

- **Get a Reporter by ID**
  - **GET** `/api/reporters/?id=1`
  - Returns the specific reporter matching the given ID or 404 if not found.

### 2. Issue Endpoints
- **Create an Issue**
  - **POST** `/api/issues/`
  - Body (JSON): `{"id": 1, "title": "Login button not working", "description": "Broken on mobile", "status": "open", "priority": "critical", "reporter_id": 1}`
  - Instantiates the correct issue type based on priority (e.g. CriticalIssue vs LowPriorityIssue) and returns an enriched message if successful.

- **Get All Issues**
  - **GET** `/api/issues/`
  - Returns a full list of issues currently tracked.

- **Get a Single Issue by ID**
  - **GET** `/api/issues/?id=1`
  - Retrieves a specific issue mapping to the given ID.

- **Get All Issues Filtered by Status**
  - **GET** `/api/issues/?status=open`
  - Returns only those issues that possess the queried status such as "open" or "resolved".

## Design Decision
**Why JSON instead of DB models?**
As stated in the requirements, I selected a standard JSON-file based storage in `reporters.json` and `issues.json` utilizing abstract classes rather than `django.db.models.Model`. The choice ensures this backend acts strictly based on the requested OOP behavior (validating via custom abstract classes, polymorphic classes like `CriticalIssue`) without relying on Django’s built-in ORM.
This prevents the tight coupling often seen with Active Record pattern in Django models and cleanly separates the domain behavior from the storage implementation (file persistence).
