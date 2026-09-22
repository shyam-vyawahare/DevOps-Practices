# AWS EC2 + Docker Deployment

## 🎯 Objective

Deploy a Dockerized application on an AWS EC2 instance.

This practical connects the DevOps workflow learned so far:

```text
Developer
   ↓
GitHub
   ↓
GitHub Actions
   ↓
Docker Image
   ↓
GitHub Container Registry (GHCR)
   ↓
AWS EC2
   ↓
Running Docker Container
   ↓
Public Application
```

---

# 1. What is AWS EC2?

**Amazon EC2 (Elastic Compute Cloud)** provides virtual servers in the AWS cloud.

An EC2 instance can be used to:

- Host web applications
- Run Docker containers
- Run APIs
- Host databases
- Run backend services
- Build CI/CD deployment environments

For this practical, EC2 will act as our deployment server.

---

# 2. Prerequisites

Before starting, make sure you have:

- AWS account
- GitHub account
- Docker image published to GHCR
- SSH client
- Existing Docker application
- Basic Linux commands knowledge

Our previous Docker image is:

```text
ghcr.io/<github-username>/devops-practice-app:latest
```

Replace `<github-username>` with your GitHub username.

---

# 3. Create an EC2 Instance

Open the AWS Management Console.

Navigate to:

```text
EC2 → Instances → Launch Instance
```

Recommended configuration for practice:

```text
Name:
DevOps-Practice-Server

AMI:
Ubuntu Server 24.04 LTS

Instance Type:
t2.micro
```

If `t2.micro` is unavailable for your account/region, select an appropriate small instance available to you.

---

# 4. Create an SSH Key Pair

During instance creation, create or select a key pair.

Example:

```text
devops-practice-key
```

Download the `.pem` file.

Example:

```text
devops-practice-key.pem
```

Keep this file secure.

Never upload the private key to GitHub.

---

# 5. Configure Security Group

The EC2 Security Group works like a cloud firewall.

Allow:

| Type | Port | Source | Purpose |
|---|---:|---|---|
| SSH | 22 | My IP | Server access |
| HTTP | 80 | 0.0.0.0/0 | Web traffic |
| Custom TCP | 8080 | 0.0.0.0/0 | Practice application |

For better security, restrict SSH access to your own IP whenever possible.

---

# 6. Connect to EC2 Using SSH

After launching the instance, copy its public IP.

Example:

```text
13.234.56.78
```

On Linux/macOS:

```bash
chmod 400 devops-practice-key.pem
```

Connect:

```bash
ssh -i devops-practice-key.pem ubuntu@<EC2-PUBLIC-IP>
```

Example:

```bash
ssh -i devops-practice-key.pem ubuntu@13.234.56.78
```

You should now be inside the EC2 server.

---

# 7. Update the Server

Run:

```bash
sudo apt update
```

Then:

```bash
sudo apt upgrade -y
```

---

# 8. Install Docker

Install Docker:

```bash
sudo apt install docker.io -y
```

Check the installation:

```bash
docker --version
```

Example output:

```text
Docker version 28.x.x
```

---

# 9. Start Docker

Start the Docker service:

```bash
sudo systemctl start docker
```

Enable Docker at system startup:

```bash
sudo systemctl enable docker
```

Check the service:

```bash
sudo systemctl status docker
```

---

# 10. Allow the Ubuntu User to Run Docker

By default, Docker may require `sudo`.

Add the current user to the Docker group:

```bash
sudo usermod -aG docker $USER
```

Apply the group change by logging out and reconnecting:

```bash
exit
```

Reconnect:

```bash
ssh -i devops-practice-key.pem ubuntu@<EC2-PUBLIC-IP>
```

Test:

```bash
docker ps
```

If Docker works without `sudo`, the setup is complete.

---

# 11. Login to GitHub Container Registry

If the GHCR package is public, Docker can pull it directly.

For example:

```bash
docker pull ghcr.io/<github-username>/devops-practice-app:latest
```

If the package is private, authenticate first:

```bash
echo "<GITHUB_TOKEN>" | docker login ghcr.io -u <github-username> --password-stdin
```

A GitHub token used for a private GHCR package should have the appropriate package read permission.

Never commit the token to GitHub.

---

# 12. Pull the Docker Image

Pull the image:

```bash
docker pull ghcr.io/<github-username>/devops-practice-app:latest
```

Check downloaded images:

```bash
docker images
```

You should see something similar to:

```text
REPOSITORY                                  TAG       IMAGE ID
ghcr.io/<github-username>/devops-practice-app latest  XXXXXXXX
```

---

# 13. Run the Application

Run the container:

```bash
docker run -d   --name devops-production   -p 8080:5000   ghcr.io/<github-username>/devops-practice-app:latest
```

Explanation:

```text
-d
```

Runs the container in detached mode.

```text
--name devops-production
```

Assigns a name to the container.

```text
-p 8080:5000
```

Maps:

```text
EC2 Port 8080 → Container Port 5000
```

---

# 14. Check Running Containers

Run:

```bash
docker ps
```

Example:

```text
CONTAINER ID   IMAGE                                      PORTS
xxxxxxxx       ghcr.io/user/devops-practice-app:latest   0.0.0.0:8080->5000/tcp
```

---

# 15. Check Application Logs

Run:

```bash
docker logs devops-production
```

For live logs:

```bash
docker logs -f devops-production
```

Press:

```text
Ctrl + C
```

to stop following the logs.

The container itself will continue running.

---

# 16. Test the Application from EC2

Inside the EC2 server:

```bash
curl http://localhost:8080/
```

If the application is working, you should receive the application's response.

---

# 17. Access the Application from Your Browser

Open:

```text
http://<EC2-PUBLIC-IP>:8080
```

Example:

```text
http://13.234.56.78:8080
```

If the application loads, your Docker application is now running on AWS EC2.

---

# 18. Important Port Mapping

The complete request flow is:

```text
Browser
   │
   │ HTTP :8080
   ↓
AWS EC2
   │
   │ Docker port mapping
   │ 8080 → 5000
   ↓
Docker Container
   │
   │ Flask application
   ↓
Port 5000
```

---

# 19. Check Container Details

Inspect the container:

```bash
docker inspect devops-production
```

Check its processes:

```bash
docker top devops-production
```

Check resource usage:

```bash
docker stats devops-production
```

---

# 20. Restart the Application

Stop the container:

```bash
docker stop devops-production
```

Start it again:

```bash
docker start devops-production
```

Check:

```bash
docker ps
```

---

# 21. Remove the Container

Stop and remove:

```bash
docker rm -f devops-production
```

Verify:

```bash
docker ps
```

---

# 22. Deploying a New Version

Suppose a new Docker image has been published to GHCR.

First pull the latest image:

```bash
docker pull ghcr.io/<github-username>/devops-practice-app:latest
```

Remove the old container:

```bash
docker rm -f devops-production
```

Run the new version:

```bash
docker run -d   --name devops-production   -p 8080:5000   ghcr.io/<github-username>/devops-practice-app:latest
```

Verify:

```bash
docker ps
```

Check logs:

```bash
docker logs devops-production
```

---

# 23. Complete Manual Deployment

The complete deployment process can be summarized as:

```bash
# Connect to EC2
ssh -i devops-practice-key.pem ubuntu@<EC2-PUBLIC-IP>

# Pull latest image
docker pull ghcr.io/<github-username>/devops-practice-app:latest

# Remove old container
docker rm -f devops-production 2>/dev/null || true

# Start new container
docker run -d   --name devops-production   -p 8080:5000   ghcr.io/<github-username>/devops-practice-app:latest

# Verify
docker ps

# Check logs
docker logs devops-production
```

---

# 24. Deployment Architecture

```text
                    GitHub
                       │
                       │ Push Code
                       ↓
              GitHub Actions
                       │
                       │ Build
                       ↓
                  Docker Image
                       │
                       │ Push
                       ↓
                     GHCR
                       │
                       │ Pull
                       ↓
                 AWS EC2 Server
                       │
                       │ docker run
                       ↓
               Docker Container
                       │
                       ↓
                Flask Application
                       │
                       ↓
                Public HTTP Request
```

---

# 25. DevOps Concepts Demonstrated

This practical demonstrates several important DevOps concepts.

### Infrastructure

AWS EC2 provides the virtual server.

### Containerization

Docker packages the application and its dependencies.

### Container Registry

GHCR stores the Docker image.

### Continuous Integration

GitHub Actions can build and test the application.

### Continuous Delivery

The built image is made available for deployment.

### Deployment

The Docker image is deployed to an EC2 server.

### Monitoring

Docker commands such as:

```bash
docker ps
docker logs
docker stats
```

help inspect the running application.

---

# 26. Troubleshooting

## Problem: SSH Permission Denied

Check the key permissions:

```bash
chmod 400 devops-practice-key.pem
```

Verify the username:

```text
Ubuntu AMI → ubuntu
Amazon Linux → ec2-user
```

---

## Problem: Docker Permission Denied

Try:

```bash
sudo docker ps
```

If that works, add the user to the Docker group:

```bash
sudo usermod -aG docker $USER
```

Then reconnect to the server.

---

## Problem: Browser Cannot Connect

Check:

```bash
docker ps
```

Make sure the container exposes:

```text
0.0.0.0:8080->5000/tcp
```

Then check the EC2 Security Group.

Port `8080` must be allowed if you are accessing the application directly through that port.

---

## Problem: Container Exits Immediately

Check:

```bash
docker ps -a
```

Then:

```bash
docker logs devops-production
```

The logs usually provide the reason for the failure.

---

## Problem: Image Cannot Be Pulled

Check the image name:

```bash
docker pull ghcr.io/<github-username>/devops-practice-app:latest
```

If the package is private, authenticate with GHCR first.

---

# 27. Security Best Practices

Do not expose SSH to the entire internet unless necessary.

Prefer:

```text
SSH → My IP
```

instead of:

```text
SSH → 0.0.0.0/0
```

Never commit:

```text
.pem files
GitHub tokens
AWS access keys
passwords
API keys
.env files containing secrets
```

Add sensitive files to `.gitignore`.

---

# 28. Cleanup

When the practical is finished, stop the container:

```bash
docker stop devops-production
```

Remove it:

```bash
docker rm devops-production
```

If the EC2 instance is no longer needed, stop or terminate it from:

```text
AWS Console
→ EC2
→ Instances
```

Terminating an instance permanently removes that instance's ephemeral resources.

---

# 29. Key Commands Cheat Sheet

| Task | Command |
|---|---|
| Connect to EC2 | `ssh -i key.pem ubuntu@IP` |
| Update Ubuntu | `sudo apt update` |
| Install Docker | `sudo apt install docker.io -y` |
| Docker version | `docker --version` |
| Start Docker | `sudo systemctl start docker` |
| Docker status | `sudo systemctl status docker` |
| List containers | `docker ps` |
| All containers | `docker ps -a` |
| List images | `docker images` |
| Pull image | `docker pull IMAGE` |
| Run container | `docker run -d ...` |
| Stop container | `docker stop NAME` |
| Start container | `docker start NAME` |
| Remove container | `docker rm NAME` |
| Force remove | `docker rm -f NAME` |
| Container logs | `docker logs NAME` |
| Live logs | `docker logs -f NAME` |
| Container stats | `docker stats NAME` |
| Test HTTP endpoint | `curl http://localhost:8080/` |

---

# 30. Final DevOps Workflow

After completing this practical, the deployment lifecycle becomes:

```text
1. Developer writes code
        ↓
2. Push code to GitHub
        ↓
3. GitHub Actions runs
        ↓
4. Docker image is built
        ↓
5. Image is pushed to GHCR
        ↓
6. EC2 pulls the image
        ↓
7. Docker container starts
        ↓
8. Application becomes accessible
        ↓
9. Logs and resources are monitored
```

This is a simplified real-world container deployment workflow.

---

## 🧠 What You Learned

- AWS EC2
- SSH
- Linux server administration
- AWS Security Groups
- Docker installation on Linux
- Docker image deployment
- GitHub Container Registry
- Docker port mapping
- Container logs
- Container lifecycle management
- Manual application deployment
- Cloud-based DevOps workflow

---

## 🚀 Next Step

The next level is to remove the manual deployment steps.

Instead of:

```text
GitHub
   ↓
GHCR
   ↓
SSH into EC2
   ↓
docker pull
   ↓
docker run
```

we can build:

```text
GitHub
   ↓
GitHub Actions
   ↓
Build Docker Image
   ↓
Push to GHCR
   ↓
Deploy Automatically
   ↓
AWS EC2
```

That will introduce **automated CI/CD deployment to AWS EC2**.
