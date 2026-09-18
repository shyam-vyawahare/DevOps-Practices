# Docker Health Checks

## 🎯 Objective

Learn how Docker health checks determine whether a containerized application is actually working and how health status can be used in multi-container applications.

---

## 1. What is a Health Check?

A Docker health check is a command that Docker periodically runs inside a container to determine whether the application is functioning correctly.

A container can be:

```text
Running ≠ Healthy
```

For example, a web server process may still be running while the application itself is unable to respond to requests.

Health checks help detect this condition.

---

## 2. Container States

Without a health check, Docker mainly knows whether a container is running:

```text
Created
   ↓
Running
   ↓
Stopped
```

With a health check:

```text
Running
   │
   ├── Healthy
   │
   └── Unhealthy
```

---

## 3. Why Health Checks Matter

Health checks help DevOps teams:

- Detect failed applications
- Improve service reliability
- Monitor application readiness
- Support automated recovery
- Prevent traffic from reaching unhealthy services
- Improve CI/CD deployment validation

---

# 🧪 Hands-On Practice

## 4. Create a Health-Checked Nginx Container

Run:

```bash
docker run -d \
  --name healthy-nginx \
  --health-cmd="curl -f http://localhost/ || exit 1" \
  --health-interval=10s \
  --health-timeout=5s \
  --health-retries=3 \
  nginx
```

Check the container:

```bash
docker ps
```

You should eventually see something similar to:

```text
Up 20 seconds (healthy)
```

---

## 5. Understand the Health Check Options

### `--health-cmd`

Defines the command Docker executes.

```bash
--health-cmd="curl -f http://localhost/ || exit 1"
```

If the command succeeds:

```text
Healthy
```

If it fails:

```text
Unhealthy
```

---

### `--health-interval`

Defines how frequently the check runs.

```bash
--health-interval=10s
```

The check runs approximately every 10 seconds.

---

### `--health-timeout`

Defines how long Docker waits for the check.

```bash
--health-timeout=5s
```

---

### `--health-retries`

Defines how many consecutive failures are allowed before Docker marks the container unhealthy.

```bash
--health-retries=3
```

---

## 6. Inspect Health Status

Run:

```bash
docker inspect --format='{{.State.Health.Status}}' healthy-nginx
```

Expected:

```text
healthy
```

You can also inspect the complete health information:

```bash
docker inspect healthy-nginx
```

Look for:

```text
State
 └── Health
      ├── Status
      ├── FailingStreak
      └── Log
```

---

## 7. View Health Check Logs

Run:

```bash
docker inspect --format='{{json .State.Health}}' healthy-nginx
```

This shows information about previous health-check executions.

---

# 8. Health Checks in Dockerfile

A health check can also be defined directly inside a Dockerfile.

Example:

```dockerfile
FROM nginx:alpine

HEALTHCHECK --interval=30s \
            --timeout=5s \
            --start-period=5s \
            --retries=3 \
            CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1
```

### Important options

```text
--interval
```

Time between checks.

```text
--timeout
```

Maximum time allowed for a check.

```text
--start-period
```

Initial startup period during which failures are ignored.

```text
--retries
```

Number of consecutive failures before the container becomes unhealthy.

---

# 9. Health Checks with Docker Compose

Docker Compose supports health checks directly.

Example:

```yaml
services:

  web:
    image: nginx:alpine
    ports:
      - "8080:80"

    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost/"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 5s
```

Start it:

```bash
docker compose up -d
```

Check:

```bash
docker compose ps
```

The web service should eventually report:

```text
healthy
```

---

# 10. Health Checks in a Multi-Container Application

Consider:

```text
             Web Application
                    │
                    ▼
                 Database
```

The web application should ideally communicate with the database only after the database is ready.

A Compose configuration can define a health check for the database.

Example:

```yaml
services:

  database:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: example

    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    image: nginx:alpine
    depends_on:
      database:
        condition: service_healthy
```

The dependency relationship becomes:

```text
Database
   │
   │ Health Check
   ↓
Healthy
   │
   ↓
Web Application Starts
```

---

# 11. `depends_on` vs Health Check

This is an important distinction.

Basic:

```yaml
depends_on:
  - database
```

This controls **startup order**.

It does not necessarily mean the database is ready to accept connections.

With:

```yaml
depends_on:
  database:
    condition: service_healthy
```

Compose can wait for the database health check to report healthy before starting the dependent service.

---

# 12. Health vs Readiness

These concepts are related but not identical.

### Health

Is the application currently functioning?

```text
Is the service alive and responding?
```

### Readiness

Is the service ready to receive requests?

For example:

```text
Application started
      ↓
Database connected
      ↓
Configuration loaded
      ↓
Dependencies available
      ↓
Ready for traffic
```

Production systems often distinguish between **liveness** and **readiness** checks.

---

# 13. Simulate an Unhealthy Container

Create a container with a deliberately failing health check:

```bash
docker run -d \
  --name unhealthy-demo \
  --health-cmd="exit 1" \
  --health-interval=5s \
  --health-retries=2 \
  nginx
```

Wait several seconds and run:

```bash
docker ps
```

You should eventually see:

```text
Up ... (unhealthy)
```

Check:

```bash
docker inspect --format='{{.State.Health.Status}}' unhealthy-demo
```

Expected:

```text
unhealthy
```

This demonstrates that a running container can still be considered unhealthy.

---

# 14. Clean Up

Remove the containers:

```bash
docker rm -f healthy-nginx unhealthy-demo
```

If you created a Compose application:

```bash
docker compose down
```

---

# 🧪 Practice Tasks

## Task 1

Create an Nginx container with:

```text
interval = 5 seconds
timeout = 3 seconds
retries = 3
```

Verify that it becomes healthy.

---

## Task 2

Create a deliberately failing health check:

```bash
--health-cmd="exit 1"
```

Observe the transition to:

```text
unhealthy
```

---

## Task 3

Modify your previous multi-container application and add:

```yaml
healthcheck:
```

to the Redis service.

---

## Task 4

Configure the Flask service so it depends on Redis being healthy.

---

## Task 5

Run:

```bash
docker compose ps
```

and observe the health status of each service.

---

# 🔑 Key Takeaways

- A running container is not necessarily a healthy container.
- Docker health checks test application functionality.
- Health checks can be defined using `docker run`, Dockerfile, or Compose.
- `interval`, `timeout`, `start_period`, and `retries` control health-check behavior.
- `depends_on` controls service startup dependencies.
- `condition: service_healthy` can wait for a dependency to become healthy.
- Health checks are important for reliable multi-container deployments.

---

# 🚀 DevOps Connection

Health checks connect containerization with automated operations:

```text
Application
     ↓
Docker Container
     ↓
Health Check
     ↓
Healthy / Unhealthy
     ↓
Monitoring
     ↓
Automated Recovery / Deployment Decisions
```

In a production DevOps pipeline:

```text
Code
 ↓
Build
 ↓
Test
 ↓
Docker Image
 ↓
Deploy
 ↓
Health Check
 ↓
Healthy?
 ├── YES → Continue
 └── NO  → Investigate / Rollback
```

Health checks therefore become an important part of **reliable CI/CD and production deployments**.

---

## Next Practice

```text
Docker Health Checks
        ↓
Docker Logging
        ↓
Container Monitoring
        ↓
CI/CD Deployment
```
