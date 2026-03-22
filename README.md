# OpenSpec Multi-VM Docker Project

This project consists of three interconnected Docker containers simulating a network infrastructure:

1. **VM1-Login** (nginx:alpine) - Web login interface on port 8080
2. **VM2-Backend** (python:3.11-slim) - FastAPI backend service on port 8000  
3. **VM3-Storage** (mysql:5.7) - Database and rsync storage service on ports 3306 (MySQL) and 873 (rsync)

## Prerequisites

- Docker Desktop installed and running
- Git (optional, for cloning)
- Minimum 4GB RAM recommended

## Getting Started

### 1. Clone or download the project
```bash
# If you don't have the project files yet:
git clone <repository-url>
cd Openspec
# Otherwise, navigate to the project directory
```

### 2. Build and start all services
```bash
# Using the classic Docker build method (recommended for Windows)
DOCKER_BUILDKIT=0 docker-compose up -d --build

# Alternative standard command (may work on some systems):
# docker-compose up -d --build
```

### 3. Verify services are running
```bash
docker ps
```

You should see three containers running:
- openspec-vm1-login-1 (nginx)
- openspec-vm2-backend-1 (uvicorn/FastAPI)
- openspec-vm3-storage-1 (MySQL + rsync)

## Service Access

### VM1-Login (Web Interface)
- URL: http://localhost:8080
- Technology: Nginx serving static files
- Purpose: User login interface

### VM2-Backend (API Service)
- URL: http://localhost:8000
- Technology: FastAPI/Python 3.11
- API Documentation: http://localhost:8000/docs
- Purpose: Business logic and data processing

### VM3-Storage (Database & File Sync)
- MySQL: localhost:3306 (username: app_user, password: apppassword, database: company_data)
- RSYNC: localhost:873 (username: app_user, password: rsyncpassword123)
- Purpose: Data storage and file synchronization

## Environment Variables

All services use environment variables defined in the `.env` file:

```
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=company_data
MYSQL_USER=app_user
MYSQL_PASSWORD=apppassword
GEMINI_API_KEY=AIzaSyD_SD9sjhST2IxhfY8UUdYmvuVRR7NVvkk
JWT_SECRET_KEY=supersecretkey
RSYNC_PASSWORD=rsyncpassword123
```

## Service Details

### VM3-Storage (MySQL + RSYNC)
- Based on mysql:5.7 (Oracle Linux 7.9)
- Uses yum package manager
- Includes rsync for file synchronization
- Custom startup script launches both rsync daemon and MySQL server
- Initializes database with schema and seed data from `/docker-entrypoint-initdb.d/`

### VM2-Backend (FastAPI)
- Based on python:3.11-slim (Debian-based)
- Uses apt package manager
- Installs Python dependencies from requirements.txt
- Runs Uvicorn server on port 8000
- Connects to MySQL database at vm3-storage:3306

### VM1-Login (Nginx)
- Based on nginx:alpine (Alpine Linux)
- Serves static files from ./vm1-login/public/
- Custom nginx configuration in ./vm1-login/nginx.conf
- Runs on port 80

## Troubleshooting

### Common Issues

1. **"Failed to create pid file" errors in rsync**
   - This is usually harmless and occurs when the rsync pid file already exists
   - The startup script now cleans up the pid file before starting rsync

2. **Database connection failures**
   - Ensure VM3-storage is fully started (MySQL initialization can take 30-60 seconds)
   - Check logs: `docker logs openspec-vm3-storage-1`
   - Verify MySQL is ready: `docker exec openspec-vm3-storage-1 mysqladmin ping -h localhost -u root -prootpassword`

3. **Port conflicts**
   - Make sure ports 8080, 8000, 3306, and 873 are not already in use
   - Check with: `netstat -ano | findstr :8080` (Windows) or `lsof -i :8080` (Mac/Linux)

### Viewing Logs
```bash
# View logs for a specific service
docker logs openspec-vm3-storage-1
docker logs openspec-vm2-backend-1
docker logs openspec-vm1-login-1

# Follow logs in real-time
docker logs -f openspec-vm3-storage-1
```

### Stopping and Cleaning Up
```bash
# Stop all containers
docker-compose down

# Stop containers and remove volumes (including database data)
docker-compose down -v

# Remove all images (use with caution)
docker-compose down --rmi all
```

## Development Notes

### Making Changes
1. Modify source code in the respective VM directories
2. Rebuild and restart:
   ```bash
   DOCKER_BUILDKIT=0 docker-compose up -d --build
   ```
3. For code-only changes in VM2-backend, you can often just restart:
   ```bash
   docker-compose restart vm2-backend
   ```

### Database Persistence
- MySQL data is persisted in the `./vm3-storage/` directory
- To reset the database completely, remove the directory and restart:
  ```bash
  docker-compose down -v
  rm -rf vm3-storage/*
  docker-compose up -d
  ```

## Project Structure
```
Openspec/
├── docker-compose.yml          # Container orchestration
├── .env                        # Environment variables
├── README.md                   # This file
├── vm1-login/                  # Nginx web server
│   ├── Dockerfile
│   ├── nginx.conf
│   └── public/                 # Static web files
├── vm2-backend/                # Python/FastAPI backend
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/                    # Application code
└── vm3-storage/                # MySQL + RSYNC storage
    ├── Dockerfile
    ├── entrypoint.sh           # Startup script
    ├── rsync_setup.sh
    ├── startup.sh              # Alternative startup approach
    └── init/                   # Database initialization scripts
```

## Security Note
⚠️ This project uses default passwords for simplicity. In production environments:
- Use strong, unique passwords
- Consider using Docker secrets or a secret management system
- Limit network exposure
- Regularly update dependencies

---

**The project is now ready to use!** Access the login interface at http://localhost:8080 and the API documentation at http://localhost:8000/docs.