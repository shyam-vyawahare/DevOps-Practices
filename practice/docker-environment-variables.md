# Docker Environment Variables & Secrets

## 🎯 Objective

Learn how to pass configuration values to Docker containers using environment variables and understand how to handle sensitive information securely.

---

## 1. What are Environment Variables?

Environment variables are key-value pairs used to provide configuration to an application without hardcoding values inside the source code.

Example:

```text
APP_ENV=production
PORT=5000
DB_HOST=database
```

Instead of writing these values directly into application code, Docker can provide them when the container starts.

---

## 2. Why Use Environment Variables?

They help to:

- Keep configuration separate from code
- Change settings without rebuilding the image
- Support different environments
- Avoid hardcoding configuration
- Simplify CI/CD deployments

Example:

```text
Development → DB_HOST=localhost
Production  → DB_HOST=production-db
```

The same application image can be used in both environments.

---

## 3. Using `-e` with Docker

Environment variables can be passed using the `-e` option.

```bash
docker run -d \
  --name env-demo \
  -e APP_ENV=development \
  -e APP_VERSION=1.0 \
  nginx
```

Check the variables:

```bash
docker exec env-demo printenv APP_ENV
```

Output:

```text
development
```

Check another variable:

```bash
docker exec env-demo printenv APP_VERSION
```

Output:

```text
1.0
```

---

## 4. View All Environment Variables

Run:

```bash
docker exec env-demo env
```

or:

```bash
docker exec env-demo printenv
```

This displays the environment variables available inside the container.

---

## 5. Using an `.env` File

Instead of specifying every variable using `-e`, create an `.env` file.

Example:

```env
APP_ENV=development
APP_VERSION=1.0
APP_PORT=5000
```

Run:

```bash
docker run -d \
  --name env-demo \
  --env-file .env \
  nginx
```

Check:

```bash
docker exec env-demo printenv APP_ENV
```

---

## 6. Environment Variables with Docker Compose

Docker Compose makes environment configuration easier.

Example:

```yaml
services:

  app:
    image: nginx
    environment:
      APP_ENV: production
      APP_VERSION: "1.0"
```

The variables are available inside the container.

---

## 7. Using a `.env` File with Compose

Create:

```text
.env
```

Example:

```env
APP_ENV=production
APP_VERSION=1.0
```

Compose file:

```yaml
services:

  app:
    image: nginx
    environment:
      APP_ENV: ${APP_ENV}
      APP_VERSION: ${APP_VERSION}
```

Docker Compose substitutes the values from `.env`.

---

## 8. Environment Variables vs Secrets

Environment variables are useful for normal configuration.

Examples:

```text
APP_ENV=production
PORT=5000
LOG_LEVEL=info
```

However, sensitive information requires additional care.

Examples:

```text
Database passwords
API keys
Access tokens
Private credentials
```

Do not commit sensitive values to GitHub.

Bad practice:

```yaml
environment:
  DB_PASSWORD: my-secret-password
```

Better practice is to use a secret-management mechanism appropriate to the deployment environment.

---

## 9. Docker Secrets

Docker Swarm provides a secrets mechanism for securely supplying sensitive data to services.

Example:

```bash
echo "my-db-password" | docker secret create db_password -
```

List secrets:

```bash
docker secret ls
```

Secrets are exposed to an authorized service rather than being placed directly in the image.

> Note: Docker Secrets are primarily associated with Docker Swarm. For modern deployments, platforms such as Kubernetes and cloud providers also provide dedicated secret-management solutions.

---

## 10. Important Security Rules

### Never commit secrets

Avoid:

```text
.env
```

when it contains passwords, API keys, or tokens.

Add it to `.gitignore`:

```gitignore
.env
```

### Use a template instead

Create:

```text
.env.example
```

Example:

```env
APP_ENV=development
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
```

The template documents the required variables without exposing real credentials.

---

## 11. Environment-Specific Configuration

A common DevOps workflow is:

```text
                 Same Docker Image
                        │
             ┌──────────┼──────────┐
             ↓          ↓          ↓
        Development   Testing   Production
             │          │          │
             ↓          ↓          ↓
          .env-dev   .env-test  Secure Config
```

This allows the application image to remain unchanged while its configuration changes between environments.

---

# 🧪 Hands-On Practice

## Task 1 — Run a Container

```bash
docker run -d \
  --name devops-env \
  -e APP_NAME=DevOpsPractice \
  -e APP_ENV=development \
  -e APP_VERSION=1.0 \
  alpine \
  sh -c "while true; do sleep 3600; done"
```

---

## Task 2 — Read Variables

```bash
docker exec devops-env printenv APP_NAME
```

```bash
docker exec devops-env printenv APP_ENV
```

```bash
docker exec devops-env printenv APP_VERSION
```

Expected output:

```text
DevOpsPractice
development
1.0
```

---

## Task 3 — Create an `.env` File

Create:

```text
.env
```

Add:

```env
APP_NAME=DevOpsPractice
APP_ENV=testing
APP_VERSION=2.0
```

---

## Task 4 — Run Using `.env`

Remove the previous container:

```bash
docker rm -f devops-env
```

Run:

```bash
docker run -d \
  --name devops-env \
  --env-file .env \
  alpine \
  sh -c "while true; do sleep 3600; done"
```

Check:

```bash
docker exec devops-env printenv APP_ENV
```

Expected:

```text
testing
```

---

## Task 5 — Protect the `.env` File

Add the following to `.gitignore`:

```gitignore
.env
```

Create:

```text
.env.example
```

Add:

```env
APP_NAME=DevOpsPractice
APP_ENV=development
APP_VERSION=1.0
```

The `.env.example` file can be committed because it contains no real secrets.

---

## Task 6 — Clean Up

```bash
docker rm -f devops-env
```

---

# 🔑 Key Takeaways

- Environment variables provide external configuration to containers.
- `docker run -e` passes variables directly.
- `--env-file` loads variables from a file.
- Docker Compose supports environment variables and `.env` files.
- Never hardcode passwords, API keys, or tokens in source code.
- Do not commit real `.env` files containing secrets.
- Use `.env.example` to document required configuration.
- Use dedicated secret-management mechanisms for sensitive production credentials.

---

## 🚀 DevOps Connection

Environment management is essential for building reliable CI/CD pipelines.

```text
Application Code
       │
       ▼
Docker Image
       │
       ├── Development Configuration
       │
       ├── Testing Configuration
       │
       └── Production Configuration
                    │
                    ▼
             Secure Secrets
                    │
                    ▼
                Deployment
```

The same Docker image can therefore move through different environments while receiving environment-specific configuration.

## Next Practice

```text
Environment Variables & Secrets
             ↓
Dockerized Multi-Container Application
             ↓
Advanced Docker Compose
             ↓
CI/CD Deployment
             ↓
AWS
```
