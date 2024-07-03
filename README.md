# Project Name

Brief description of your project.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [API Endpoints](#api-endpoints)
4. [Testing](#testing)
5. [Contributing](#contributing)
6. [License](#license)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/NagahShinawy/walzay.git
   cd payment
   ```

2. **Set up the environment:**

   - Create a virtual environment (optional but recommended):

     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```

   - Install dependencies:

     ```bash
     pip install -r requirements.txt
     ```

3. **Set up the database:**

   - Ensure PostgreSQL is installed and configured.
   - Create a `.env` file with necessary environment variables (database credentials, etc.).

4. **Run migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Load initial data (if any):**

   ```bash
   python manage.py loaddata initial_data.json
   ```

6. **Start the development server:**

   ```bash
   python manage.py runserver
   ```

   The development server will start at `http://localhost:8000`.

## Usage

Explain how to use your project once it's set up. Include any specific instructions or steps necessary to interact with the application.

## CashCollector Endpoints

1. **Task List API:**

   - **Endpoint:** `/api/cashcollector/tasks/`
   - **Method:** GET
   - **Description:** Retrieves a list of tasks completed by the CashCollector.


2. **Next Task API:**

   - **Endpoint:** `/api/cashcollector/next_task/`
   - **Method:** GET
   - **Description:** Retrieves the next task that the CashCollector should perform.


3. **Status API:**

   - **Endpoint:** `/api/cashcollector/status/`
   - **Method:** GET
   - **Description:** Checks whether the CashCollector is frozen or not.


4. **Collect Amount API:**

   - **Endpoint:** `/api/cashcollector/collect/`
   - **Method:** POST
   - **Description:** Records the amount collected by the CashCollector for a task.


5. **Pay Amount API:**

   - **Endpoint:** `/api/cashcollector/pay/`
   - **Method:** POST
   - **Description:** Records the amount delivered to the Manager by the CashCollector.



## Accounts Endpoints

1. **User Login API:**

   - **Endpoint:** `/api/auth/login/`
   - **Method:** POST
   - **Description:** Authenticates and logs in a user, returning an authentication token.


2**User Resister API:**

   - **Endpoint:** `/api/auth/resister/`
   - **Method:** POST
   - **Description:** Registers a new user


3**User List API:**

   - **Endpoint:** `/api/auth/resister/`
   - **Method:** POST
   - **Description:** Retrieves a list of all users.




## Testing

Explain how to run tests for your application.

```bash
python manage.py test
```

## Contributing

Explain how others can contribute to your project.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

