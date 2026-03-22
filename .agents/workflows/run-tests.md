# Run Tests Workflow

Steps to run the full test suite:

1. Ensure all services are running (or at least the database):
   ```bash
   # Option 1: Run tests against a temporary database
   docker compose run --rm vm2-backend pytest tests/ -v
   
   # Option 2: If you have a running database, set environment variables
   # and run tests directly
   MYSQL_HOST=localhost MYSQL_DATABASE=test_db pytest tests/ -v
   ```

2. Run specific test modules:
   ```bash
   # Authentication tests
   docker compose run --rm vm2-backend pytest tests/test_auth.py -v
   
   # Data isolation tests
   docker compose run --rm vm2-backend pytest tests/test_data_isolation.py -v
   
   # Gemini service tests
   docker compose run --rm vm2-backend pytest tests/test_gemini.py -v
   
   # Rsync service tests
   docker compose run --rm vm2-backend pytest tests/test_rsync.py -v
   ```

3. Run tests with coverage:
   ```bash
   docker compose run --rm vm2-backend pytest tests/ --cov=app --cov-report=html
   ```

4. Run specific tests by marker or keyword:
   ```bash
   # Run only unit tests
   docker compose run --rm vm2-backend pytest tests/ -m unit -v
   
   # Run only integration tests
   docker compose run --rm vm2-backend pytest tests/ -m integration -v
   ```

5. Watch for changes and re-run tests (useful during development):
   ```bash
   docker compose run --rm vm2-backend ptw tests/
   ```

Note: Make sure your .env file has appropriate test database credentials if not using the defaults.