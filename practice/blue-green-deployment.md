# Blue-Green Deployment

## 🎯 Objective

Learn how to deploy a new application version alongside the current version, verify it independently, and switch production traffic only after the new version is healthy.

Blue-Green deployment uses two environments:

```text
BLUE  → Current production version
GREEN → New version being tested
```

After Green is verified, traffic is switched from Blue to Green.

---

## 1. What is Blue-Green Deployment?

A Blue-Green deployment maintains two application environments.

```text
BLUE
Version 1
Production
```

and:

```text
GREEN
Version 2
Testing
```

After successful testing:

```text
Production Traffic
        ↓
      GREEN
     Version 2
```

Blue can remain available for rollback.

---

## 2. Why Use Blue-Green Deployment?

Traditional deployment may look like:

```text
Stop Version 1
      ↓
Start Version 2
      ↓
Application transition
```

Blue-Green:

```text
Version 1 → Blue
Version 2 → Green
      ↓
Test Green
      ↓
Switch Traffic
```

Benefits:

- Reduced deployment downtime
- Safer deployments
- Fast rollback
- Independent testing
- Clear separation between versions
- Easier recovery from failed releases

---

## 3. Basic Architecture

```text
                    Users
                      │
                      ↓
                Reverse Proxy
                  /       \
                 /         \
                ↓           ↓
             BLUE         GREEN
           Version 1      Version 2
                │           │
                └─────┬─────┘
                      │
              One receives traffic
```

Nginx can be used as the reverse proxy.

---

## 4. Blue and Green

### Blue

Blue is the current production environment.

```text
Blue → v1
Status → Production
```

### Green

Green contains the new release.

```text
Green → v2
Status → Testing
```

After switching:

```text
Blue  → v1 → Standby
Green → v2 → Production
```

---

## 5. Docker Example

Run Blue:

```bash
docker run -d   --name app-blue   -p 5001:5000   ghcr.io/<github-username>/devops-practice-app:v1
```

Run Green:

```bash
docker run -d   --name app-green   -p 5002:5000   ghcr.io/<github-username>/devops-practice-app:v2
```

Architecture:

```text
EC2
 │
 ├── Port 5001 → Blue → v1
 │
 └── Port 5002 → Green → v2
```

---

## 6. Test Blue

```bash
curl http://localhost:5001/health
```

Expected:

```json
{
  "status": "healthy"
}
```

---

## 7. Test Green

```bash
curl http://localhost:5002/health
```

Expected:

```json
{
  "status": "healthy"
}
```

Green should pass health checks before receiving production traffic.

---

## 8. Why Separate Ports?

Both containers cannot normally bind to the same host port.

Incorrect:

```text
Blue  → 8080
Green → 8080
```

Correct:

```text
Blue  → 5001
Green → 5002
```

Nginx can expose a single public port:

```text
Public :8080
      ↓
    Nginx
   /     \
5001     5002
Blue     Green
```

---

## 9. Nginx Reverse Proxy

Example configuration:

```nginx
events {}

http {
    upstream application {
        server 127.0.0.1:5001;
    }

    server {
        listen 8080;

        location / {
            proxy_pass http://application;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
```

Initially:

```text
Nginx → Blue :5001
```

---

## 10. Install Nginx on Ubuntu

```bash
sudo apt update
sudo apt install nginx -y
```

Check:

```bash
sudo systemctl status nginx
```

Start:

```bash
sudo systemctl start nginx
```

Enable at boot:

```bash
sudo systemctl enable nginx
```

---

## 11. Validate Nginx

Always test the configuration before reloading:

```bash
sudo nginx -t
```

Expected:

```text
syntax is ok
test is successful
```

Reload:

```bash
sudo systemctl reload nginx
```

---

## 12. Switching Traffic

Suppose:

```text
Blue  → v1
Green → v2
```

Green has passed its health checks.

Change:

```nginx
upstream application {
    server 127.0.0.1:5001;
}
```

to:

```nginx
upstream application {
    server 127.0.0.1:5002;
}
```

Validate:

```bash
sudo nginx -t
```

Reload:

```bash
sudo systemctl reload nginx
```

Traffic now goes:

```text
Nginx → Green → v2
```

---

## 13. Traffic Switch

### Before

```text
Users
  ↓
Nginx
  ↓
Blue
v1
```

Green:

```text
Green
v2
↓
Testing
```

### After

```text
Users
  ↓
Nginx
  ↓
Green
v2
```

Blue remains available:

```text
Blue
v1
↓
Standby
```

---

## 14. Rollback

If Green becomes unhealthy after the switch, point Nginx back to Blue.

```nginx
upstream application {
    server 127.0.0.1:5001;
}
```

Validate:

```bash
sudo nginx -t
```

Reload:

```bash
sudo systemctl reload nginx
```

Traffic returns to:

```text
Nginx → Blue → v1
```

---

## 15. Rollback Flow

```text
Blue v1
   ↓
Production

Green v2
   ↓
Testing
   ↓
Health Check
   ↓
PASS
   ↓
Traffic → Green

Later:

Green v2
   ↓
Problem
   ↓
Traffic → Blue
   ↓
Blue v1 restored
```

---

## 16. Complete Docker Setup

Start Blue:

```bash
docker run -d   --name app-blue   -p 5001:5000   ghcr.io/<github-username>/devops-practice-app:v1
```

Start Green:

```bash
docker run -d   --name app-green   -p 5002:5000   ghcr.io/<github-username>/devops-practice-app:v2
```

Check:

```bash
docker ps
```

Test Blue:

```bash
curl --fail http://localhost:5001/health
```

Test Green:

```bash
curl --fail http://localhost:5002/health
```

---

## 17. Blue-Green Deployment Script

Example:

```bash
#!/bin/bash

IMAGE_NAME="ghcr.io/<github-username>/devops-practice-app"
NEW_VERSION="$1"

if [ -z "$NEW_VERSION" ]; then
    echo "Usage: ./blue-green-deploy.sh <version>"
    exit 1
fi

echo "Deploying version: $NEW_VERSION"

docker pull "$IMAGE_NAME:$NEW_VERSION"

docker rm -f app-green 2>/dev/null || true

docker run -d     --name app-green     -p 5002:5000     "$IMAGE_NAME:$NEW_VERSION"

echo "Waiting for Green application..."
sleep 5

echo "Checking Green health..."

if curl --fail --silent http://localhost:5002/health > /dev/null; then
    echo "Green environment is healthy."
else
    echo "Green environment failed health check."
    docker logs app-green
    docker rm -f app-green
    exit 1
fi

echo "Green deployment is ready for traffic switch."
```

---

## 18. Blue-Green vs Automated Rollback

Automated rollback:

```text
Stop Old
   ↓
Start New
   ↓
Health Check
   ↓
Failure
   ↓
Restore Old
```

Blue-Green:

```text
Old Running
   ↓
Start New Separately
   ↓
Health Check
   ↓
Switch Traffic
```

The old version can remain running while the new version is tested.

---

## 19. Deployment Process

A complete Blue-Green deployment can follow:

```text
1. Blue is production
        ↓
2. Deploy Green
        ↓
3. Start Green
        ↓
4. Run health checks
        ↓
5. Run application tests
        ↓
6. Switch traffic
        ↓
7. Monitor Green
        ↓
8. Keep Blue temporarily
        ↓
9. Remove Blue after verification
```

---

## 20. Health Checks Before Switching

Do not switch traffic just because the container started.

Check:

```bash
docker ps
```

Then:

```bash
curl --fail http://localhost:5002/health
```

Also inspect logs:

```bash
docker logs app-green
```

Only switch traffic after Green has been verified.

---

## 21. Application Testing

Health checks verify basic availability.

Additional tests can verify functionality:

```bash
curl --fail http://localhost:5002/
```

API example:

```bash
curl --fail http://localhost:5002/api/status
```

The exact tests depend on the application.

---

## 22. Nginx Blue-Green Configuration

A simple configuration can define both environments:

```nginx
events {}

http {

    upstream blue {
        server 127.0.0.1:5001;
    }

    upstream green {
        server 127.0.0.1:5002;
    }

    server {
        listen 8080;

        location / {
            proxy_pass http://blue;

            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
```

Initially:

```text
proxy_pass http://blue;
```

Switch to:

```text
proxy_pass http://green;
```

Then:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

## 23. GitHub Actions Integration

A CI/CD pipeline can automate:

```text
Git Push
   ↓
GitHub Actions
   ↓
Build Docker Image
   ↓
Push to GHCR
   ↓
SSH to EC2
   ↓
Start Green
   ↓
Health Check Green
   ↓
Switch Nginx
   ↓
Verify Production
   ↓
Keep / Remove Blue
```

Conceptual workflow:

```yaml
- name: Deploy Green
  run: |
    # Pull new image
    # Start Green container

- name: Check Green
  run: |
    # Test Green health endpoint

- name: Switch Traffic
  run: |
    # Update Nginx configuration
    # Validate Nginx
    # Reload Nginx

- name: Verify Production
  run: |
    # Test production endpoint
```

Adapt the commands to the actual EC2 and Nginx configuration.

---

## 24. Blue-Green Advantages

Blue-Green deployment can provide:

- Reduced deployment downtime
- Fast rollback
- Independent testing
- Clear version separation
- Controlled production switches
- Easier recovery from failed releases

---

## 25. Production Considerations

Blue-Green deployment requires additional resources because both versions may run simultaneously.

Consider:

- CPU usage
- Memory usage
- Container storage
- Database compatibility
- Configuration compatibility
- Secrets and environment variables
- Monitoring
- Logging
- Traffic switching
- Rollback strategy

Database migrations require special attention because the old and new application versions may temporarily coexist.

---

## 26. Blue-Green vs Traditional Deployment

| Feature | Traditional | Blue-Green |
|---|---|---|
| Two versions running | Usually no | Yes |
| Independent pre-production testing | Limited | Yes |
| Rollback mechanism | Deployment dependent | Traffic switch |
| Deployment complexity | Lower | Higher |
| Resource usage | Lower | Higher |
| Traffic switching | Replacement | Controlled switch |
| Downtime | May occur | Can be minimized |

---

## 27. Troubleshooting

### Green container does not start

```bash
docker ps -a
```

Then:

```bash
docker logs app-green
```

---

### Green health check fails

```bash
curl -v http://localhost:5002/health
```

Check logs:

```bash
docker logs app-green
```

---

### Nginx configuration error

```bash
sudo nginx -t
```

Do not reload until the configuration passes validation.

---

### Traffic still reaches Blue

Inspect the complete configuration:

```bash
sudo nginx -T
```

Check that the active `proxy_pass` points to Green.

Then:

```bash
sudo systemctl reload nginx
```

---

### Port conflict

```bash
sudo ss -tulpn | grep -E '5001|5002|8080'
```

Also:

```bash
docker ps
```

---

## 28. Security Considerations

Internal application ports should not be unnecessarily exposed to the internet.

For example:

```text
5001 → Blue
5002 → Green
```

can remain accessible only from the local server.

The reverse proxy can expose the public application through:

```text
80
443
```

or another intended public port.

---

## 29. Practical Checklist

Before switching traffic:

```text
[ ] New Docker image pulled
[ ] Green container started
[ ] Green container is running
[ ] Green health check passes
[ ] Green application tests pass
[ ] Nginx configuration validated
[ ] Traffic switch performed
[ ] Production endpoint tested
[ ] Logs monitored
[ ] Blue kept available for rollback
```

---

## 30. Complete Architecture

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
                            │
                            ↓
                         AWS EC2
                            │
                ┌───────────┴───────────┐
                ↓                       ↓
             BLUE                    GREEN
              v1                       v2
                │                       │
                │                  Health Check
                │                       │
                │                  Application Test
                │                       │
                │                       ↓
                │                    Ready
                │                       │
                └───────────────┬───────┘
                                ↓
                         Nginx Traffic Switch
                                ↓
                              GREEN
                               v2
                                │
                                ↓
                           Production
```

---

## 31. Final Deployment Flow

```text
Blue v1
  │
  └── Production
        ↓
Deploy Green v2
        ↓
Health Check
        ↓
   ┌────┴────┐
   ↓         ↓
 PASS       FAIL
   ↓         ↓
Switch      Remove
Traffic     Green
   ↓
Green v2
Production
   ↓
Monitor
   ↓
Problem?
   ↓
Switch back to Blue
```

---

## 32. What You Learned

- Blue-Green deployment
- Active and standby environments
- Running multiple Docker versions
- Port-based application separation
- Nginx reverse proxy
- Traffic switching
- Pre-production health checks
- Fast rollback
- CI/CD Blue-Green concepts
- Production considerations
- Troubleshooting deployment issues

---

## 🚀 Next Step

The next deployment strategy is **Canary Deployment**.

Instead of switching all traffic at once:

```text
100% → Old Version
```

traffic can gradually move to the new version:

```text
90% → Old Version
10% → New Version
```

Then:

```text
50% → Old Version
50% → New Version
```

Eventually:

```text
0% → Old Version
100% → New Version
```

This introduces gradual traffic rollout and controlled exposure of a new release.
