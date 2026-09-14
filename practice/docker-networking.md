# Docker Networking

## 🎯 Objective

Understand Docker networking and learn how multiple containers communicate with each other using Docker networks.

---

## 1. What is Docker Networking?

Docker networking allows containers to communicate with:

- Other containers
- The host machine
- External networks / the Internet

By default, Docker provides networking so that containers can communicate while remaining isolated from the host and other networks.

---

## 2. Types of Docker Networks

Docker commonly provides these network drivers:

| Network | Description |
|---|---|
| `bridge` | Default network for containers on a single Docker host |
| `host` | Container shares the host's network stack |
| `none` | Disables networking for the container |
| `overlay` | Connects containers across multiple Docker hosts |
| `macvlan` | Gives containers their own MAC address on the network |

For normal local development, the **bridge** network is most commonly used.

---

## 3. View Existing Networks

List all Docker networks:

```bash
docker network ls
```

Example:

```text
NETWORK ID     NAME      DRIVER    SCOPE
abc123         bridge    bridge    local
def456         host      host      local
ghi789         none      null      local
```

Inspect the default bridge network:

```bash
docker network inspect bridge
```

---

## 4. Create a Custom Network

Create a custom bridge network:

```bash
docker network create devops-network
```

Verify it:

```bash
docker network ls
```

---

## 5. Run Containers on the Network

Run a container connected to the custom network:

```bash
docker run -d --name web-server --network devops-network nginx
```

Run another container on the same network:

```bash
docker run -it --name test-client --network devops-network alpine sh
```

Inside the Alpine container, install networking tools:

```bash
apk add --no-cache curl
```

Now communicate with the Nginx container using its container name:

```bash
curl http://web-server
```

The request should return the Nginx welcome page.

---

## 6. Container-to-Container Communication

One of the major advantages of a custom Docker network is **DNS-based container discovery**.

For example:

```text
test-client
     |
     | HTTP request
     ↓
web-server
     |
     ↓
   Nginx
```

The client does not need to know the IP address of `web-server`.

It can simply use:

```text
http://web-server
```

Docker's internal DNS resolves the container name to the correct IP address.

---

## 7. Connect an Existing Container

A running container can be connected to a network:

```bash
docker network connect devops-network existing-container
```

Check the network:

```bash
docker network inspect devops-network
```

---

## 8. Disconnect a Container

Remove a container from the network:

```bash
docker network disconnect devops-network existing-container
```

---

## 9. Docker Compose Networking

Docker Compose automatically creates a network for services defined in a Compose file.

Example:

```yaml
services:

  web:
    image: nginx
    ports:
      - "8080:80"

  client:
    image: alpine
    command: ["sh", "-c", "sleep 3600"]
```

Both services can communicate using their service names.

For example:

```text
client → web:80
```

The `client` container can access the Nginx service using:

```bash
curl http://web
```

No IP address is required.

---

## 10. Port Mapping vs Container Networking

These two concepts are different.

### Port Mapping

```yaml
ports:
  - "8080:80"
```

This allows:

```text
Host Machine
     |
   :8080
     ↓
Container :80
```

It is mainly used to expose a container service to the host or external clients.

### Container Networking

```text
Container A
     |
     | Docker Network
     ↓
Container B
```

Containers on the same Docker network can communicate internally without publishing their ports to the host.

---

## 11. Practical Example: Web + Database

A typical application may contain:

```text
                 Host Machine
                      |
                   :8080
                      |
                      ↓
              ┌─────────────┐
              │ Web/API     │
              │ Container   │
              └──────┬──────┘
                     |
             Docker Network
                     |
                     ↓
              ┌─────────────┐
              │ Database    │
              │ Container   │
              └─────────────┘
```

The web application can communicate with the database using the database's service/container name.

For example:

```text
DB_HOST=database
DB_PORT=5432
```

The database does not need to expose port `5432` to the host if only the application needs to access it.

---

## 12. Useful Commands

### List networks

```bash
docker network ls
```

### Inspect a network

```bash
docker network inspect devops-network
```

### Create a network

```bash
docker network create devops-network
```

### Connect container

```bash
docker network connect devops-network container-name
```

### Disconnect container

```bash
docker network disconnect devops-network container-name
```

### Remove network

```bash
docker network rm devops-network
```

---

## 🧪 Hands-On Practice

### Step 1 — Create the network

```bash
docker network create devops-network
```

### Step 2 — Start Nginx

```bash
docker run -d \
  --name web-server \
  --network devops-network \
  nginx
```

### Step 3 — Start an Alpine client

```bash
docker run -it \
  --name test-client \
  --network devops-network \
  alpine sh
```

### Step 4 — Install curl

Inside the Alpine container:

```bash
apk add --no-cache curl
```

### Step 5 — Test communication

```bash
curl http://web-server
```

You should receive the Nginx HTML response.

### Step 6 — Exit the container

```bash
exit
```

### Step 7 — Clean up

```bash
docker rm -f web-server test-client
docker network rm devops-network
```

---

## 🔑 Key Takeaways

- Docker networking enables communication between containers.
- `bridge` is the most commonly used network for local containers.
- Custom networks provide better container isolation and communication.
- Containers on the same custom network can communicate using container/service names.
- Docker Compose automatically creates a network for its services.
- Port mapping exposes container services to the host.
- Internal container communication does not necessarily require port publishing.
- Docker networking is essential for multi-container and microservice applications.

---

## 🚀 Next Step

Docker networking provides the foundation for running applications consisting of multiple services.

Next, we can build on this concept with:

```text
Docker Networking
       ↓
Docker Volumes
       ↓
Environment Variables & Secrets
       ↓
Multi-Container Application
       ↓
CI/CD Deployment
```
