# Deployment Health Check

## 🎯 Objective

Learn how to verify that an application is actually working after deployment.

A successful deployment does not always mean a successful application.

```text
Docker image built successfully
        ↓
Container started successfully
        ↓
Application crashed
        ↓
Deployment is technically complete
BUT
Application is unavailable
```

Health checks help detect this problem automatically.

---

# 1. What is a Deployment Health Check?

A deployment health check verifies that the deployed application is responding correctly.

A basic health check can test:

- Is the container running?
- Is the application listening on the expected port?
- Is the HTTP endpoint reachable?
- Is the server returning a successful HTTP status?
- Is the application responding within a reasonable time?
- Is the application marked healthy by Docker?

Typical flow:

```text
Deployment
    ↓
Start Container
    ↓
Wait for Application
    ↓
Send Health Request
    ↓
Check Response
    ↓
Healthy → Continue
Unhealthy → Fail Deployment
```

---

# 2. Why Health Checks Matter

Consider this deployment:

```text
GitHub
   ↓
GitHub Actions
   ↓
Docker Build
   ↓
GHCR
   ↓
EC2
   ↓
docker run
```

If `docker run` succeeds, GitHub Actions may report success.

But the application could still be:

- Crashing after startup
- Listening on the wrong port
- Returning HTTP 500
- Missing an environment variable
- Unable to connect to a dependency
- Starting too slowly

A health check gives the deployment pipeline another verification layer.

---

# 3. Basic HTTP Health Check

The simplest health check uses `curl`.

```bash
curl --fail http://localhost:8080/
```

The `--fail` option causes `curl` to return a failure status for HTTP errors such as:

```text
400
404
500
```

A successful response allows the command to continue.

---

# 4. Check the HTTP Status Code

You can explicitly inspect the HTTP status:

```bash
curl -o /dev/null -s -w "%{http_code}" http://localhost:8080/
```

Example output:

```text
200
```

A common interpretation is:

```text
200 → Application responded successfully
404 → Requested endpoint does not exist
500 → Application/server error
```

The exact acceptable status codes depend on the application.

---

# 5. Health Endpoint

A dedicated health endpoint is better than testing an arbitrary page.

For example:

```text
GET /health
```

Expected response:

```json
{
  "status": "healthy"
}
```

The deployment system can then test:

```bash
curl --fail http://localhost:8080/health
```

---

# 6. Example Flask Health Endpoint

A Flask application can provide a simple health endpoint:

```python
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/")
def home():
    return "DevOps Practice Application"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

The important part is:

```python
@app.route("/health")
def health():
    return jsonify({"status": "healthy"})
```

The application now provides a dedicated endpoint for automated health checks.

---

# 7. Test Health Endpoint Locally

If the application is running locally on port `5000`:

```bash
curl --fail http://localhost:5000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

---

# 8. Test Health Endpoint in Docker

If the container is mapped like this:

```text
Host:      8080
Container: 5000
```

Run:

```bash
curl --fail http://localhost:8080/health
```

Expected:

```json
{
  "status": "healthy"
}
```

---

# 9. Docker Healthcheck

Docker can also monitor application health directly.

Example:

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD curl --fail http://localhost:5000/health || exit 1
```

This tells Docker:

```text
Every 30 seconds
       ↓
Run health check
       ↓
Wait maximum 5 seconds
       ↓
Allow 10 seconds startup time
       ↓
Retry 3 times if necessary
```

---

# 10. Important Docker Healthcheck Requirement

The container must contain the command used by the health check.

For example, if using:

```dockerfile
CMD curl --fail http://localhost:5000/health || exit 1
```

the image needs `curl`.

For an Ubuntu-based image:

```dockerfile
RUN apt-get update && apt-get install -y curl
```

For Alpine:

```dockerfile
RUN apk add --no-cache curl
```

Always clean up package caches where appropriate for production images.

---

# 11. Check Docker Health Status

Run:

```bash
docker ps
```

A healthy container may show:

```text
Up 2 minutes (healthy)
```

Inspect health information:

```bash
docker inspect --format='{{json .State.Health}}' devops-production
```

A simpler status check:

```bash
docker inspect --format='{{.State.Health.Status}}' devops-production
```

Possible result:

```text
healthy
```

or:

```text
unhealthy
```

---

# 12. Example Unhealthy Container

If the application is not responding correctly, Docker may report:

```text
unhealthy
```

Check logs:

```bash
docker logs devops-production
```

Check the health status:

```bash
docker inspect --format='{{.State.Health.Status}}' devops-production
```

This helps identify deployment problems.

---

# 13. Deployment Health Check on EC2

After deploying:

```bash
docker run -d   --name devops-production   -p 8080:5000   ghcr.io/<github-username>/devops-practice-app:latest
```

Wait a few seconds:

```bash
sleep 5
```

Then test:

```bash
curl --fail http://localhost:8080/health
```

If the command succeeds:

```text
Deployment health check passed.
```

If it fails:

```text
Deployment health check failed.
```

---

# 14. Health Check Script

A simple health-check script can be:

```bash
#!/bin/bash

URL="http://localhost:8080/health"

echo "Checking application health..."

if curl --fail --silent --show-error "$URL"; then
    echo ""
    echo "Application is healthy."
    exit 0
else
    echo ""
    echo "Application health check failed."
    exit 1
fi
```

Save it as:

```text
practice/check-deployment-health.sh
```

Make it executable:

```bash
chmod +x practice/check-deployment-health.sh
```

Run:

```bash
./practice/check-deployment-health.sh
```

---

# 15. Health Check with Retry

Applications sometimes need time to start.

Instead of checking only once, retry several times.

```bash
#!/bin/bash

URL="http://localhost:8080/health"
MAX_RETRIES=10

echo "Waiting for application..."

for i in $(seq 1 $MAX_RETRIES); do
    if curl --fail --silent "$URL" > /dev/null; then
        echo "Application is healthy."
        exit 0
    fi

    echo "Attempt $i/$MAX_RETRIES failed."
    sleep 3
done

echo "Application failed health check."
exit 1
```

This gives the application multiple opportunities to start successfully.

---

# 16. Why Retry Logic Matters

Without retry:

```text
Container starts
      ↓
Health check immediately
      ↓
Application still starting
      ↓
FAIL
```

With retry:

```text
Container starts
      ↓
Health check
      ↓
Not ready
      ↓
Wait
      ↓
Health check
      ↓
Ready
      ↓
SUCCESS
```

---

# 17. GitHub Actions Health Check

A deployment workflow can run a health check after deployment.

```yaml
- name: Verify Deployment
  uses: appleboy/ssh-action@v1.2.0
  with:
    host: ${{ secrets.EC2_HOST }}
    username: ${{ secrets.EC2_USERNAME }}
    key: ${{ secrets.EC2_SSH_KEY }}
    script: |
      echo "Checking application health..."

      for i in {1..10}; do
        if curl --fail --silent http://localhost:8080/health > /dev/null; then
          echo "Application is healthy."
          exit 0
        fi

        echo "Health check attempt $i failed."
        sleep 3
      done

      echo "Application failed health check."
      exit 1
```

If the health check fails, the GitHub Actions job fails.

---

# 18. Deployment Success Criteria

A deployment should ideally pass several checks:

```text
✓ Docker image pulled
✓ Container started
✓ Container is running
✓ Application port is available
✓ Health endpoint responds
✓ HTTP status is successful
```

Only after these checks should the deployment be considered successful.

---

# 19. Health Check Architecture

```text
                 GitHub Actions
                       │
                       │ Deploy
                       ↓
                  AWS EC2
                       │
                       ↓
                Docker Container
                       │
                       ↓
               Flask Application
                       │
                       ↓
                  /health
                       │
                       ↓
                 HTTP 200 OK
                       │
                       ↓
               Deployment Passed
```

If `/health` fails:

```text
/health
   ↓
HTTP Error / Timeout
   ↓
Health Check Failed
   ↓
GitHub Actions Job Failed
```

---

# 20. Container Health vs Application Health

These are related but different.

### Container Health

Checks whether the containerized service is responding as expected.

Example:

```text
Docker HEALTHCHECK
```

### Application Health

Checks whether the actual application is functioning.

Example:

```text
GET /health
```

A container can be running while the application inside it is broken.

Therefore:

```text
Running ≠ Healthy
```

---

# 21. Readiness and Liveness

In larger systems, health checks are often divided into:

### Liveness

Answers:

> Is the application process alive?

Example:

```text
GET /health/live
```

### Readiness

Answers:

> Is the application ready to receive traffic?

Example:

```text
GET /health/ready
```

Example:

```text
/health/live
    ↓
Process is alive

/health/ready
    ↓
Application + required dependencies are ready
```

These concepts become especially important with Kubernetes.

---

# 22. Health Check and Dependencies

A production application may depend on:

```text
Application
    ├── Database
    ├── Redis
    ├── External API
    └── File Storage
```

A readiness check may verify that required dependencies are available.

For example:

```text
Database reachable?
Redis reachable?
Required configuration present?
Application initialized?
```

Do not make health endpoints unnecessarily expensive.

---

# 23. Security Considerations

Health endpoints should not expose sensitive information.

Avoid responses such as:

```json
{
  "database_password": "...",
  "api_key": "...",
  "internal_ip": "...",
  "secret": "..."
}
```

Prefer a simple response:

```json
{
  "status": "healthy"
}
```

Detailed diagnostics should be protected and controlled.

---

# 24. Troubleshooting Health Check Failures

## Check container status

```bash
docker ps -a
```

## Check logs

```bash
docker logs devops-production
```

## Check port mapping

```bash
docker port devops-production
```

## Test locally

```bash
curl http://localhost:8080/health
```

## Check Docker health

```bash
docker inspect --format='{{.State.Health.Status}}' devops-production
```

## Check listening ports

```bash
sudo ss -tulpn
```

---

# 25. Common Problems

### Wrong Port

Application listens on:

```text
5000
```

but container is started incorrectly.

Correct:

```bash
-p 8080:5000
```

---

### Wrong Endpoint

Workflow checks:

```text
/health
```

but application only provides:

```text
/
```

Make sure the endpoint exists.

---

### Application Starts Slowly

Use retry logic:

```bash
for i in {1..10}; do
    ...
    sleep 3
done
```

---

### Application Crashes

Check:

```bash
docker logs devops-production
```

---

### Security Group Problem

If checking from an external machine, verify that the required EC2 port is allowed.

For an internal EC2 health check using:

```bash
curl http://localhost:8080/health
```

the request does not need to travel through the public internet.

---

# 26. Practical Deployment Sequence

Use this sequence after deploying a new image:

```bash
docker pull ghcr.io/<github-username>/devops-practice-app:latest

docker rm -f devops-production 2>/dev/null || true

docker run -d   --name devops-production   -p 8080:5000   ghcr.io/<github-username>/devops-practice-app:latest

sleep 5

curl --fail http://localhost:8080/health
```

If the final command succeeds:

```text
Deployment verified.
```

---

# 27. CI/CD Verification Flow

Our pipeline now becomes:

```text
Developer
    ↓
Git Push
    ↓
GitHub Actions
    ↓
Build Docker Image
    ↓
Push Image to GHCR
    ↓
Deploy to EC2
    ↓
Start Container
    ↓
Health Check
    ↓
Healthy?
   /  Yes  No
  ↓    ↓
Success  Fail
```

---

# 28. Deployment Failure Handling

If the health check fails, the pipeline should not report a successful deployment.

Instead:

```text
Health Check Failed
        ↓
Deployment Job Fails
        ↓
Logs Collected
        ↓
Developer Investigates
```

A later improvement can automatically restore the previous known-good version.

That concept is called **rollback**.

---

# 29. Practical Checklist

Before considering a deployment complete:

```text
[ ] EC2 instance is running
[ ] Docker service is running
[ ] Latest image pulled
[ ] Container started
[ ] Container is running
[ ] Port mapping is correct
[ ] Application is responding
[ ] /health endpoint returns success
[ ] Docker health status is healthy, if configured
[ ] Deployment workflow reports success
[ ] Logs show no startup errors
```

---

# 30. Final DevOps Workflow

After adding deployment health checks:

```text
                    GitHub
                       │
                       ↓
                GitHub Actions
                       │
                       ↓
                Build Docker Image
                       │
                       ↓
                     GHCR
                       │
                       ↓
                   AWS EC2
                       │
                       ↓
                Docker Container
                       │
                       ↓
                Application Start
                       │
                       ↓
                 Health Check
                       │
                ┌──────┴──────┐
                ↓             ↓
             Healthy       Unhealthy
                ↓             ↓
          Deployment OK   Deployment Failed
```

---

## 🧠 What You Learned

- Deployment health checks
- HTTP health endpoints
- `curl --fail`
- HTTP status verification
- Docker `HEALTHCHECK`
- Container health status
- Retry logic
- Liveness vs readiness
- CI/CD deployment verification
- Health-check troubleshooting
- Deployment failure handling
- Rollback concept

---

## 🚀 Next Step

The next practical can implement **automated rollback**.

Instead of:

```text
New Version
    ↓
Deployment
    ↓
Health Check Failed
    ↓
❌ Application stays broken
```

we can build:

```text
Old Version
    ↓
Deploy New Version
    ↓
Health Check
    ↓
Failed
    ↓
Remove New Version
    ↓
Restore Old Version
    ↓
Application Back Online
```

This introduces an important real-world **CI/CD deployment recovery pattern**.
