# Practical 9 – CI/CD with GitHub Actions

This practical introduces **Continuous Integration (CI)** using GitHub Actions.
It automates the Docker image build process whenever code is pushed to the repository.

This is the first step toward real-world deployment pipelines used in industry.

---

## 🎯 Objectives

- Understand CI/CD fundamentals
- Learn GitHub Actions workflow structure
- Automate Docker image builds
- Remove manual build steps from development

---

## 🧠 Key Concepts

- CI vs CD
- Workflow triggers
- Jobs and steps
- Runners (ubuntu-latest)
- Automation mindset

---

## 📁 Files in This Practical

- `docker-ci.yml` – GitHub Actions workflow file

---

## ⚙️ Workflow Overview

1. Developer pushes code to GitHub
2. GitHub Actions workflow is triggered
3. Repository code is checked out
4. Docker image is built automatically

---

## ▶️ How to Use

1. Place the workflow file inside:
