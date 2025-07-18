# 🕷️ pyASM 

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

## 🧱 Architecture

The system architecture follows an asynchronous pipeline:

1. User initiates a scan via a REST API.  
2. Flask API normalizes and validates input.  
3. A task workflow is constructed dynamically based on available modules.  
4. Celery processes the task chain.  
5. MongoDB stores results.  
6. User polls the API for real-time progress or results.

All services are containerized using Docker and orchestrated via `docker-compose`.

---

## 🔧 Features

- Subdomain Enumeration (via `assetfinder`, `subfinder`, etc.)  
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
