# Docker Multi-Container Application

## 🎯 Objective

Build and understand a multi-container application using Docker Compose, where an application container communicates with a separate database container.

---

## 1. What is a Multi-Container Application?

A multi-container application divides an application into multiple services, with each service running in its own container.

For example:

```text
             User
              │
              ▼
       ┌─────────────┐
       │ Web / API   │
       │ Container   │
       └──────┬──────┘
              │
        Docker Network
              │
              ▼
       ┌─────────────┐
       │ Database    │
       │ Container   │
       └─────────────┘
```

Each container has a specific responsibility.

---

## 2. Why Use Multiple Containers?

Multi-container architecture provides:

- Separation of responsibilities
- Independent scaling
- Easier maintenance
- Better isolation
- Easier development and testing
- Independent service deployment

A typical application may contain:

```text
Frontend
Backend API
Database
Cache
Reverse Proxy
```

Each can run as a separate container.

---

## 3. Docker Compose

Docker Compose is used to define and run multiple Docker containers using a YAML configuration file.

Instead of running many commands manually:

```bash
docker run ...
docker run ...
docker network create ...
docker volume create ...
```

we can define the entire application in:

```text
docker-compose.yml
```

and start it with:

```bash
docker compose up
```

---

# 🧪 Hands-On Project

We will create a simple:

```text
Python API + Redis
```

application.

Architecture:

```text
                 Client
                   │
                   │ HTTP :5000
                   ▼
            ┌─────────────┐
            │ Flask API   │
            │ Container   │
            └──────┬──────┘
                   │
             Docker Network
                   │
                   ▼
            ┌─────────────┐
            │ Redis       │
            │ Container   │
            └─────────────┘
```

The Flask application will communicate with Redis using the service name:

```text
redis
```

---

## 4. Project Structure

Create:

```text
practice/docker-multi-container/
├── app/
│   ├── app.py
│   └── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# 5. Create the Flask Application

Create:

```text
app/app.py
```

```python
from flask import Flask
import os
import redis

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "redis")
redis_client = redis.Redis(
    host=redis_host,
    port=6379,
    decode_responses=True
)


@app.route("/")
def home():
    visits = redis_client.incr("visits")

    return {
        "message": "Docker Multi-Container App",
        "visits": visits
    }


@app.route("/health")
def health():
    return {
        "status": "healthy"
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

# 6. Create Requirements File

Create:

```text
app/requirements.txt
```

```text
Flask==3.1.0
redis==5.2.1
```

---

# 7. Create the Dockerfile

Create:

```text
Dockerfile
```

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 5000

CMD ["python", "app.py"]
```

---

# 8. Create Docker Compose File

Create:

```text
docker-compose.yml
```

```yaml
services:

  web:
    build: .
    container_name: flask-api
    ports:
      - "5000:5000"
    environment:
      REDIS_HOST: redis
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    container_name: redis-db
```

---

# 9. Understand the Compose File

### Web Service

```yaml
web:
  build: .
```

Builds the Flask application using the Dockerfile.

---

### Port Mapping

```yaml
ports:
  - "5000:5000"
```

This maps:

```text
Host :5000
     ↓
Container :5000
```

You can access the application through:

```text
http://localhost:5000
```

---

### Environment Variable

```yaml
environment:
  REDIS_HOST: redis
```

The Flask application knows that the Redis service is available at:

```text
redis
```

Docker Compose provides internal DNS for service names.

---

### depends_on

```yaml
depends_on:
  - redis
```

This tells Compose to start the Redis service before the web service.

> Note: `depends_on` controls startup order but does not guarantee that Redis is fully ready to accept connections.

---

# 10. Start the Application

From the project directory:

```bash
docker compose up --build
```

Compose will:

1. Build the Flask image.
2. Pull the Redis image.
3. Create a Docker network.
4. Start Redis.
5. Start Flask.

---

# 11. Test the Application

Open:

```text
http://localhost:5000
```

Example response:

```json
{
  "message": "Docker Multi-Container App",
  "visits": 1
}
```

Refresh the page.

The value should increase:

```json
{
  "message": "Docker Multi-Container App",
  "visits": 2
}
```

This happens because Redis stores the visit counter.

---

# 12. Test the Health Endpoint

Open:

```text
http://localhost:5000/health
```

Expected:

```json
{
  "status": "healthy"
}
```

---

# 13. Check Running Containers

Open another terminal:

```bash
docker compose ps
```

You should see two services:

```text
flask-api
redis-db
```

---

# 14. View Logs

View all logs:

```bash
docker compose logs
```

View only the web service:

```bash
docker compose logs web
```

View Redis logs:

```bash
docker compose logs redis
```

Follow logs continuously:

```bash
docker compose logs -f
```

---

# 15. Check the Network

List Docker networks:

```bash
docker network ls
```

Inspect the Compose network:

```bash
docker network inspect docker-multi-container_default
```

You should find both containers connected to the same network.

```text
flask-api
    │
    │ Docker Network
    │
redis-db
```

---

# 16. Test Redis Directly

Open a Redis shell:

```bash
docker compose exec redis redis-cli
```

Check the stored value:

```text
GET visits
```

Example:

```text
"5"
```

Exit:

```text
exit
```

---

# 17. Stop the Application

Press:

```text
CTRL + C
```

Or use:

```bash
docker compose down
```

This stops and removes the containers and Compose network.

---

# 18. Start Again

Run:

```bash
docker compose up
```

The application will start again.

Because Redis in this example does not have a persistent volume, its stored visit counter is not guaranteed to survive removal and recreation of the Redis container.

---

# 19. Add Persistent Redis Storage

Modify the Redis service:

```yaml
  redis:
    image: redis:7-alpine
    container_name: redis-db
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes

volumes:
  redis-data:
```

Now the architecture becomes:

```text
             Flask
               │
               ▼
          Docker Network
               │
               ▼
             Redis
               │
               ▼
          Redis Volume
               │
               ▼
        Persistent Data
```

Start again:

```bash
docker compose up --build
```

---

# 20. Stop and Remove Containers

```bash
docker compose down
```

The named volume remains unless explicitly removed.

Check:

```bash
docker volume ls
```

---

# 21. Remove Everything Including Volumes

```bash
docker compose down -v
```

> ⚠️ Be careful with `-v`. It removes the Compose-managed volumes and can permanently delete stored application data.

---

# 🔑 Key Concepts Learned

### Service

A logical component defined in `docker-compose.yml`.

Example:

```yaml
web:
redis:
```

### Container

The running instance of a service.

```text
web → flask-api
redis → redis-db
```

### Network

Allows services to communicate.

```text
web → redis
```

### Volume

Provides persistent storage.

```text
redis → redis-data
```

### Environment Variable

Provides configuration to the application.

```text
REDIS_HOST=redis
```

---

# 🧠 DevOps Architecture

This practice combines several Docker concepts:

```text
                 Docker Compose
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
     Services       Network        Volumes
        │              │              │
        ↓              ↓              ↓
      Flask  ──────→  Redis  ─────→ Persistent
       API          Communication      Data
        │
        ↓
     Port 5000
        │
        ↓
      User
```

---

# 📝 Practice Tasks

After completing the basic application, try these modifications:

### Task 1

Change:

```text
"message": "Docker Multi-Container App"
```

to your own message.

### Task 2

Add an endpoint:

```text
/info
```

that returns:

```json
{
  "application": "DevOps Practice",
  "version": "1.0"
}
```

### Task 3

Add an environment variable:

```text
APP_VERSION=1.0
```

and return it from `/info`.

### Task 4

Add a Redis health check to the Compose file.

### Task 5

Add a second Flask instance and experiment with scaling:

```bash
docker compose up --scale web=2
```

Observe how the services behave when multiple application containers are running.

---

# 🚀 DevOps Connection

Multi-container applications are commonly used with:

```text
Docker
   ↓
Docker Compose
   ↓
CI/CD Pipeline
   ↓
Container Registry
   ↓
Cloud Deployment
   ↓
Kubernetes
```

Understanding how containers communicate, store data, and receive configuration is essential before moving to container orchestration.

---

## Next Practice

The next topic will build on this application:

```text
Multi-Container Application
          ↓
Docker Health Checks
          ↓
Service Dependency Management
          ↓
Advanced Docker Compose
          ↓
CI/CD
```
