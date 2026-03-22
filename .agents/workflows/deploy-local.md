# Deploy Local Workflow

Steps to build and run the full stack locally via Docker Compose:

1. Copy `.env.example` to `.env` and fill in your values:
   ```bash
   cp .env.example .env
   # Edit .env with your GEMINI_API_KEY and other configuration
   ```

2. Build and start all services:
   ```bash
   docker compose up --build -d
   ```

3. Verify services are running:
   ```bash
   docker compose ps
   ```

4. Access the application:
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:8000
   - MySQL: localhost:3306 (internal network only)

5. To stop and remove containers:
   ```bash
   docker compose down
   ```

6. To rebuild after making changes:
   ```bash
   docker compose up --build -d
   ```

7. View logs for a specific service:
   ```bash
   docker compose logs -f vm2-backend
   ```

8. Execute commands inside a container:
   ```bash
   docker compose exec vm2-backend bash
   ```