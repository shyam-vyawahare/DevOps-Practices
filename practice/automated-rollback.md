# Automated Rollback

## 🎯 Objective

Learn how to automatically restore the previous working Docker version when a new deployment fails its health check.

Rollback is a key CI/CD recovery mechanism.

```text
Working Version
      ↓
Deploy New Version
      ↓
Health Check
      ↓
Failed
      ↓
Rollback
      ↓
Restore Working Version
```

---

# 1. What is Rollback?

A rollback means returning an application to a previously known-good version after a failed deployment.

Example:

```text
Version 1.0
   ↓
Working
   ↓
Deploy Version 2.0
   ↓
Application fails
   ↓
Rollback
   ↓
Version 1.0 restored
```

The objective is to reduce application downtime and recover quickly.

---

# 2. Why Rollback Matters

A deployment can fail because of:

- Application bugs
- Incorrect configuration
- Missing environment variables
- Broken dependencies
- Database connection problems
- Incorrect Docker configuration
- Port configuration errors
- Runtime exceptions

Without rollback:

```text
New Version
    ↓
Failure
    ↓
Application remains broken
```

With rollback:

```text
New Version
    ↓
Failure
    ↓
Restore Previous Version
    ↓
Application Available Again
```

---

# 3. Versioned Docker Images

Avoid relying only on the `latest` tag for rollback.

For example:

```text
devops-practice-app:latest
```

does not clearly identify the exact version.

Instead, use immutable tags such as:

```text
devops-practice-app:v1
devops-practice-app:v2
devops-practice-app:v3
```

Git commit SHA tags are also useful:

```text
devops-practice-app:a1b2c3d
```

This makes it possible to identify and restore an exact image.

---

# 4. Current Deployment Strategy

Our current workflow is approximately:

```text
GitHub
   ↓
GitHub Actions
   ↓
Build Docker Image
   ↓
Push to GHCR
   ↓
EC2
   ↓
Pull Image
   ↓
Run Container
   ↓
Health Check
```

We now add:

```text
Health Check
     ↓
 ┌───┴────┐
 ↓        ↓
Pass     Fail
 ↓        ↓
Keep    Rollback
```

---

# 5. Save the Current Version

Before deploying a new version, identify the currently running image.

Run:

```bash
docker inspect   --format='{{.Config.Image}}'   devops-production
```

Example:

```text
ghcr.io/shyam-vyawahare/devops-practice-app:v1
```

Save this value before replacing the container.

---

# 6. Manual Rollback

Suppose the current working version is:

```text
v1
```

and the new deployment is:

```text
v2
```

If `v2` fails, run:

```bash
docker pull ghcr.io/<github-username>/devops-practice-app:v1
```

Remove the failed container:

```bash
docker rm -f devops-production
```

Start the previous version:

```bash
docker run -d   --name devops-production   -p 8080:5000   ghcr.io/<github-username>/devops-practice-app:v1
```

Verify:

```bash
docker ps
```

Then:

```bash
curl --fail http://localhost:8080/health
```

---

# 7. Rollback Flow

```text
Version 1
   ↓
Running Successfully
   ↓
Deploy Version 2
   ↓
Health Check
   ↓
Failed
   ↓
Stop Version 2
   ↓
Start Version 1
   ↓
Health Check
   ↓
Version 1 Healthy
```

---

# 8. Simple Rollback Script

Create a script:

```text
practice/rollback-deployment.sh
```

Example:

```bash
#!/bin/bash

IMAGE_NAME="ghcr.io/<github-username>/devops-practice-app"
PREVIOUS_TAG="${1:-v1}"
CONTAINER_NAME="devops-production"
HOST_PORT="8080"
CONTAINER_PORT="5000"

echo "Starting rollback..."
echo "Previous version: $PREVIOUS_TAG"

echo "Pulling previous image..."
docker pull "$IMAGE_NAME:$PREVIOUS_TAG"

echo "Removing failed deployment..."
docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

echo "Starting previous version..."
docker run -d     --name "$CONTAINER_NAME"     -p "$HOST_PORT:$CONTAINER_PORT"     "$IMAGE_NAME:$PREVIOUS_TAG"

echo "Waiting for application..."
sleep 5

echo "Checking application health..."

if curl --fail --silent http://localhost:$HOST_PORT/health > /dev/null; then
    echo "Rollback successful."
    exit 0
else
    echo "Rollback health check failed."
    docker logs "$CONTAINER_NAME"
    exit 1
fi
```

---

# 9. Run the Rollback Script

Make it executable:

```bash
chmod +x practice/rollback-deployment.sh
```

Run:

```bash
./practice/rollback-deployment.sh v1
```

The argument specifies the version to restore.

---

# 10. Automated Rollback Logic

The deployment process can be represented as:

```text
Save Previous Version
        ↓
Deploy New Version
        ↓
Run Health Check
        ↓
      Healthy?
       /          Yes      No
      ↓        ↓
 Continue    Rollback
              ↓
        Restore Previous
              ↓
        Health Check
              ↓
          Successful?
           /               Yes       No
          ↓         ↓
       Recovery   Critical
       Complete   Failure
```

---

# 11. GitHub Actions Rollback Concept

GitHub Actions can execute rollback commands on EC2.

Example structure:

```yaml
- name: Deploy New Version
  uses: appleboy/ssh-action@v1.2.0
  with:
    host: ${{ secrets.EC2_HOST }}
    username: ${{ secrets.EC2_USERNAME }}
    key: ${{ secrets.EC2_SSH_KEY }}
    script: |
      # Deployment commands
      # Health check commands
      # Rollback commands
```

The exact implementation depends on how versions are tagged and stored.

---

# 12. Deployment with Previous Version Tracking

A simple server-side approach is to store the currently deployed tag.

Example:

```bash
echo "v1" > /opt/devops-current-version
```

Before deploying:

```bash
CURRENT_VERSION=$(cat /opt/devops-current-version)
```

Then deploy the new version.

If successful:

```bash
echo "v2" > /opt/devops-current-version
```

If the deployment fails:

```bash
docker pull "$IMAGE_NAME:$CURRENT_VERSION"
```

and restore that version.

---

# 13. Example Automated Deployment Script

A simplified deployment script:

```bash
#!/bin/bash

IMAGE_NAME="ghcr.io/<github-username>/devops-practice-app"
NEW_VERSION="$1"

CONTAINER_NAME="devops-production"
HOST_PORT="8080"
CONTAINER_PORT="5000"
VERSION_FILE="/opt/devops-current-version"

if [ -z "$NEW_VERSION" ]; then
    echo "Usage: ./deploy.sh <version>"
    exit 1
fi

if [ -f "$VERSION_FILE" ]; then
    PREVIOUS_VERSION=$(cat "$VERSION_FILE")
else
    PREVIOUS_VERSION=""
fi

echo "Previous version: $PREVIOUS_VERSION"
echo "New version: $NEW_VERSION"

echo "Pulling new image..."
docker pull "$IMAGE_NAME:$NEW_VERSION"

echo "Stopping existing container..."
docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

echo "Starting new version..."
docker run -d     --name "$CONTAINER_NAME"     -p "$HOST_PORT:$CONTAINER_PORT"     "$IMAGE_NAME:$NEW_VERSION"

echo "Waiting for startup..."
sleep 5

echo "Running health check..."

if curl --fail --silent http://localhost:$HOST_PORT/health > /dev/null; then

    echo "New version is healthy."

    echo "$NEW_VERSION" > "$VERSION_FILE"

    echo "Deployment successful."
    exit 0

fi

echo "New version failed health check."
echo "Starting rollback..."

if [ -z "$PREVIOUS_VERSION" ]; then
    echo "No previous version available."
    docker logs "$CONTAINER_NAME"
    exit 1
fi

docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

docker pull "$IMAGE_NAME:$PREVIOUS_VERSION"

docker run -d     --name "$CONTAINER_NAME"     -p "$HOST_PORT:$CONTAINER_PORT"     "$IMAGE_NAME:$PREVIOUS_VERSION"

sleep 5

if curl --fail --silent http://localhost:$HOST_PORT/health > /dev/null; then
    echo "Rollback successful."
    echo "$PREVIOUS_VERSION" > "$VERSION_FILE"
    exit 0
fi

echo "Rollback failed."
docker logs "$CONTAINER_NAME"
exit 1
```

---

# 14. Important Rollback Safety

Do not automatically delete the previous image before confirming the new deployment is healthy.

Prefer:

```text
Keep Previous
      ↓
Deploy New
      ↓
Health Check
      ↓
Successful → Previous can eventually be cleaned up
Failed → Previous still available
```

This ensures a known-good image remains available for recovery.

---

# 15. Rollback and Database Changes

Application rollback is easier than database rollback.

For example:

```text
Application v2
    ↓
Database migration
    ↓
Rollback application to v1
```

If the database schema is no longer compatible with v1, simply restoring the old application may not be enough.

Therefore production systems should use carefully designed, backward-compatible database migrations.

---

# 16. Rollback vs Redeployment

### Redeployment

Deploy the same or another version again.

```text
Deployment
   ↓
Problem
   ↓
Deploy again
```

### Rollback

Explicitly restore a known-good previous version.

```text
Version 2
   ↓
Failure
   ↓
Restore Version 1
```

Rollback is specifically about recovery to a previous known-good state.

---

# 17. Rollback vs Fix Forward

Another approach is **fix forward**.

Instead of restoring the old version:

```text
Broken v2
   ↓
Develop v3
   ↓
Deploy v3
```

Rollback:

```text
Broken v2
   ↓
Restore v1
```

The choice depends on the severity of the problem, recovery requirements, and deployment strategy.

---

# 18. Deployment Recovery Architecture

```text
                    GitHub
                       │
                       ↓
                GitHub Actions
                       │
                       ↓
                  Build Image
                       │
                       ↓
                     GHCR
                       │
                       ↓
                    AWS EC2
                       │
                       ↓
               Deploy New Version
                       │
                       ↓
                  Health Check
                       │
              ┌────────┴────────┐
              ↓                 ↓
           Healthy           Unhealthy
              ↓                 ↓
        Keep New Version      Rollback
                                ↓
                         Previous Version
                                ↓
                          Health Check
                                ↓
                          Recovery
```

---

# 19. Practical Rollback Test

To practice rollback safely:

### Step 1

Deploy a known working version:

```bash
docker pull ghcr.io/<github-username>/devops-practice-app:v1
```

### Step 2

Run it:

```bash
docker run -d   --name devops-production   -p 8080:5000   ghcr.io/<github-username>/devops-practice-app:v1
```

### Step 3

Verify:

```bash
curl --fail http://localhost:8080/health
```

### Step 4

Deploy a deliberately broken test version.

For example, use an image that does not start the expected application correctly.

### Step 5

Run the health check.

### Step 6

Trigger rollback.

### Step 7

Verify:

```bash
curl --fail http://localhost:8080/health
```

The previous version should be responding again.

---

# 20. Rollback Checklist

Before implementing automated rollback, verify:

```text
[ ] Images have identifiable versions
[ ] Previous version is known
[ ] Previous image remains available
[ ] New container can be health checked
[ ] Health endpoint exists
[ ] Rollback command is tested
[ ] Previous version can start successfully
[ ] Rollback itself has a health check
[ ] Logs are collected after failure
[ ] Secrets are not stored in scripts
```

---

# 21. Common Rollback Problems

## Previous Image Does Not Exist

Check:

```bash
docker images
```

Or pull it:

```bash
docker pull IMAGE:TAG
```

---

## Wrong Version Tag

List available images:

```bash
docker images --format "{{.Repository}}:{{.Tag}}"
```

---

## Rollback Container Cannot Start

Check:

```bash
docker logs devops-production
```

---

## Health Endpoint Still Fails

Test manually:

```bash
curl -v http://localhost:8080/health
```

---

## Port Already in Use

Check:

```bash
sudo ss -tulpn | grep 8080
```

Or:

```bash
docker ps
```

---

# 22. Production Considerations

A real production rollback system may use:

- Immutable image tags
- Git commit SHA tags
- Deployment history
- Automated health checks
- Load balancers
- Blue-green deployments
- Canary deployments
- Kubernetes
- Infrastructure as Code
- Monitoring and alerting
- Automated incident notifications

The simple Docker rollback in this practical demonstrates the underlying concept.

---

# 23. DevOps Skills Demonstrated

This practical demonstrates:

- CI/CD
- Docker
- GHCR
- AWS EC2
- Shell scripting
- Health checks
- Deployment automation
- Failure detection
- Recovery automation
- Version management
- Incident recovery concepts

---

# 24. Final Deployment Flow

Our deployment system now looks like:

```text
Developer
    ↓
Git Push
    ↓
GitHub Actions
    ↓
Build Docker Image
    ↓
Push Versioned Image to GHCR
    ↓
Deploy to EC2
    ↓
Health Check
    │
    ├── PASS
    │     ↓
    │  Deployment Complete
    │
    └── FAIL
          ↓
      Rollback
          ↓
   Restore Previous Version
          ↓
      Health Check
          ↓
      Recovery Complete
```

---

# 25. Key Commands Cheat Sheet

| Task | Command |
|---|---|
| List containers | `docker ps` |
| List all containers | `docker ps -a` |
| List images | `docker images` |
| Pull version | `docker pull IMAGE:TAG` |
| Run version | `docker run -d ... IMAGE:TAG` |
| Stop container | `docker stop NAME` |
| Remove container | `docker rm -f NAME` |
| View logs | `docker logs NAME` |
| Test health | `curl --fail http://localhost:8080/health` |
| Inspect image | `docker inspect IMAGE` |
| Inspect container | `docker inspect NAME` |
| Check port | `docker port NAME` |

---

# 26. What You Learned

- What rollback means
- Why rollback is important
- Docker image versioning
- Immutable image tags
- Manual rollback
- Automated rollback concepts
- Previous-version tracking
- Health-check-triggered rollback
- Deployment recovery
- Rollback safety
- Database migration considerations
- Rollback vs fix-forward
- CI/CD recovery patterns

---

# 27. Final Architecture

```text
                         GitHub
                            │
                            ↓
                     GitHub Actions
                            │
                            ↓
                    Docker Build
                            │
                            ↓
                          GHCR
                     ┌──────┴──────┐
                     │             │
                  v1 Image       v2 Image
                     │             │
                     │             ↓
                     │       Deploy v2
                     │             │
                     │        Health Check
                     │             │
                     │       ┌─────┴─────┐
                     │       ↓           ↓
                     │    Healthy     Failed
                     │       │           │
                     │       ↓           ↓
                     │    Keep v2     Rollback
                     │                   │
                     └───────────────────┘
                                         ↓
                                    Restore v1
                                         ↓
                                    Health Check
                                         ↓
                                      Recovery
```

---

## 🚀 Next Step

The next deployment strategy to study is **Blue-Green Deployment**.

Instead of replacing the running container directly:

```text
Old Version
    ↓
Stop
    ↓
New Version
```

Blue-Green deployment keeps two environments:

```text
Blue  → Current production
Green → New version
```

The new version is tested before traffic is switched to it.

This provides a foundation for safer deployments and is the next step after basic automated rollback.
