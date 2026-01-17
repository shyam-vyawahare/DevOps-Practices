# Practical 10 – Deploying Dockerized App on AWS EC2

This practical focuses on deploying a **Dockerized Python application**
on a real cloud server using **AWS EC2**.

This marks the transition from local development to **real-world cloud deployment**.

---

## 🎯 Objectives

- Understand cloud virtual machines
- Deploy containers on AWS EC2
- Learn basic production deployment flow
- Bridge local Docker → cloud infrastructure

---

## 🧠 Key Concepts

- EC2 instances
- SSH access
- Security Groups
- Linux server environment
- Running containers in production

---

## 📁 Files in This Practical

- `ec2_commands.md` – Common commands used on EC2 instance
- `README.md` – Deployment explanation

---

## 🚀 Deployment Flow

1. Launch an EC2 instance (Ubuntu)
2. Connect using SSH
3. Install Docker on EC2
4. Pull Docker image
5. Run container and expose port

---

## 🛠️ Basic Commands (Reference)

```bash
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker

docker pull <image-name>
docker run -d -p 80:5000 <image-name>
