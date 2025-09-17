# 🕷️ Oculum ASM 

A modular, extensible, and Dockerized reconnaissance automation framework built for offensive security operations.

## 🚀 Overview

**ReconOrchestrator** is an asset discovery and reconnaissance automation tool built with:

- **Flask** for API interaction  
- **Celery** for distributed task queueing  
- **Redis** as the broker  
- **MongoDB** for persistent storage  
- **Docker** for containerized deployment

The tool supports modular integration of recon utilities with a task-based workflow engine. Initially, it supports **subdomain enumeration**, but it's designed to scale to include:

- Port scanning  
- Vulnerability scanning  
- OSINT gathering  
- Screenshot capture  
- GF pattern-based endpoint filtering  
- GPT-generated report generation (PDF)

---

## 🔧 Features

- Subdomain Enumeration (via `assetfinder`, `subfinder`, etc.)  (Available)
- Wayback URL collection & Spidering  
- HTTP Probing (live detection)  
- Port Scanning (optional)  
- Directory/File Fuzzing  
- Screenshot Capture  
- OSINT (Emails, Leaks, Employees)  
- Pattern-based Endpoint Filtering (GF patterns)  
- Vulnerability Scanning via:
  - Nuclei  
  - CRLFuzz  
  - Dalfox  
  - Misconfigured S3 Scanner  
- GPT-based Report Generation

---

## 📦 Deployment

### Prerequisites

- Docker  
- Docker Compose

### Quick Start

```bash
git clone https://github.com/aaryanbhujang/pyasm.git
cd pyasm
cp .env.example .env
docker-compose up --build
