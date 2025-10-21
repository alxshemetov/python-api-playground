# Toy Testing Example

This project is a simple web API example designed to help you learn and practice testing methods. It includes a Flask
application and a database setup.


## 🏗️ Project Structure

The project follows a structured approach to keep the test code organized and maintainable:
- **`src/app/`**: Contains the Flask web application that serves the REST API endpoints for managing comic artists.

- **`src/api_framework/`**: A custom API testing framework that provides:
  - **`api_client.py`**: Base HTTP client wrapper for making API requests
  - **`models/`**: Pydantic or data class models for request/response validation
  - **`services/`**: High-level service methods that encapsulate API calls

- **`tests/`**: All test code organized by test type:
  - **`functional/artists/`**: Test files for each API endpoint
  - **`functional/helpers/`**: Reusable test utilities and helper functions
  - **`functional/test_data/`**: Test data payloads and fixtures

## 🚀 Getting Started
### Prerequisites

Make sure you have the following software installed on your machine:

*   Python 3.13 or higher
*   Poetry

### Setup

Follow these steps to set up and run the project:

1. **Install Poetry (if not already installed)**
    - Follow the instructions at [https://python-poetry.org/docs/](https://python-poetry.org/docs/)
    - Or use: `curl -sSL https://install.python-poetry.org | python3 -`

2. **Install dependencies**
    - Run the following command to install the required libraries:
      ```bash
      poetry install
      ```
    - This will create a virtual environment and install all dependencies automatically.

3. **Configure environment variables**
    - Create `.env`file using the `.env.example`

4. **Set up the database**
    - Open the `database_creation.py` file.
    - Run the `create_db_table` function to create the necessary database tables:
      ```bash
      poetry run python src/app/database_creation.py
      ```

5. **Run the Flask application**
    - Start the Flask app by running:
      ```bash
      poetry run python src/app/app.py
      ```
   
## 🧪 Running Tests

You can run the API tests using the following Pytest command:
```bash
  poetry run pytest
```
for running tests in parallel:
```bash
  poetry run pytest -n auto
```

## 📊 Test Reports

This project uses Allure to generate detailed and interactive test reports.

### Installing Allure

If you don't have Allure installed, you can find the installation instructions for your operating system in the [official Allure documentation](https://allurereport.org/docs/install/). For macOS and Linux users with Homebrew, it's as simple as:
```bash
brew install allure
```

### Generating the Report

After the tests have run, the Allure results will be available in the `/allure-results` directory. To generate and serve the HTML report, run:

```bash
allure serve allure-results
```

This command will start a local web server and open the report in your default browser.



## 🔌 Endpoints overview

Summary of the API routes implemented in `app.py`. This is intentionally concise — candidates should explore details and
design tests that verify the behaviors below.

- GET `/artists`
    - Returns the list of all artists (JSON list).
    - No input required.

- POST `/artists`
    - Creates a new artist.
    - Expects a JSON body. Keys: `first_name`, `last_name`,`birth_year` .
    - Validation: request must be JSON; required fields must be present and non-empty strings.

- PUT `/artists`
    - Updates an existing artist.
    - Expects a JSON body. Required keys: `user_id`, `first_name`, `last_name`, `birth_year`.
    - Validation: request must be JSON; all required values must be non-empty strings (including `user_id`).

- GET `/artists/<user_id>`
    - Fetch a single artist by `user_id` (path parameter).
    - Validation: `user_id` must be a non-empty string.

- DELETE `/artists/<user_id>`
    - Delete an artist by `user_id` (path parameter).
    - Validation: `user_id` must be a non-empty string.

## 💡 Additional Notes

- Poetry automatically manages the virtual environment for you. All commands should be prefixed with `poetry run`.
- Alternatively, you can activate the Poetry shell with `poetry shell` and then run commands directly without the
  `poetry run` prefix.
- The database file `comic_artist.db` will be created in the project directory after running the `create_db_table`
  function.
- The Flask app will run locally, and you can access it with any method that returns values, there is no UI so a browser
  will be of limited use.

Feel free to explore and modify the project to suit your learning needs.