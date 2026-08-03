# Unfoldr
# AI Developer Onboarding Assistant

## Overview

AI Developer Onboarding Assistant is an AI-powered platform that helps organizations automate the onboarding process for developers by analyzing software repositories and generating intelligent insights.

Instead of spending days manually understanding a new codebase, developers can upload a project repository and receive automatically generated documentation, architecture insights, technology detection, dependency analysis, and AI-powered answers about the project.

The platform is designed using industry-standard software architecture and modern backend engineering practices. It combines traditional backend development with Generative AI and Retrieval-Augmented Generation (RAG) to create an intelligent developer assistant.

---

# Problem Statement

When a new developer joins a team, they usually spend several days or even weeks trying to understand:

* Project structure
* Technologies used
* Frameworks
* Dependencies
* Coding standards
* APIs
* Database schema
* Business logic
* Folder organization

This manual onboarding process is time-consuming, inconsistent, and expensive.

AI Developer Onboarding Assistant aims to automate this entire process using Artificial Intelligence.

---

# Solution

The platform allows users to upload a software repository, automatically analyzes the project, generates documentation, builds a searchable knowledge base, and enables developers to ask AI-powered questions about the codebase.

---

# Key Features

## Repository Management

* Upload repository ZIP files
* Automatic repository extraction
* Repository metadata storage
* Repository status tracking
* Repository listing
* Repository details

---

## Repository Analysis

* Programming language detection
* Framework detection
* Dependency detection
* Package manager detection
* Repository structure analysis
* Source code scanning

---

## Architecture Analysis

* Folder structure analysis
* Layer detection
* API discovery
* Model detection
* Service detection
* Repository pattern detection
* Database relationship analysis

---

## Documentation Generation

Automatically generate:

* Project Overview
* Architecture Documentation
* API Documentation
* Database Documentation
* Folder Documentation
* Setup Guide
* Developer Onboarding Guide

---

## AI Features

* Repository Q&A
* Retrieval-Augmented Generation (RAG)
* Semantic Search
* AI Chat Assistant
* Code Explanation
* File Explanation
* Function Explanation
* Architecture Explanation

---

## Future Features

* User Authentication
* Team Management
* Multiple Repository Support
* Background Processing
* Repository Versioning
* Code Quality Reports
* Security Analysis
* Monitoring Dashboard

---

# System Architecture

The project follows a layered architecture.

```
                Client
                   │
                   ▼
              FastAPI Router
                   │
                   ▼
            Service Layer
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
Repository Layer      Storage Service
        │                     │
        ▼                     ▼
 PostgreSQL Database      File System
```

Future AI Architecture:

```
Repository Upload
        │
        ▼
Repository Scanner
        │
        ▼
Dependency Analyzer
        │
        ▼
Architecture Analyzer
        │
        ▼
Documentation Generator
        │
        ▼
Chunk Generator
        │
        ▼
Embedding Generator
        │
        ▼
ChromaDB Vector Store
        │
        ▼
Gemini / OpenAI
        │
        ▼
AI Response
```

---

# Technology Stack

## Backend

* Python 3.12
* FastAPI
* SQLAlchemy 2.0
* Pydantic

## Database

* PostgreSQL

## File Storage

* Local Storage

## Containerization

* Docker
* Docker Compose

## AI (Planned)

* Gemini API
* OpenAI API
* ChromaDB

## Future Technologies

* Redis
* Celery / Background Workers
* GitHub Actions
* Kubernetes
* Nginx
* Cloud Deployment

---

# Project Structure

```
app/
│
├── api/
│   └── v1/
│
├── core/
│
├── db/
│
├── models/
│
├── repositories/
│
├── schemas/
│
├── services/
│
├── analyzers/
│
├── documentation/
│
├── ai/
│
└── main.py

storage/
│
└── repositories_collection/
```

---

# Application Workflow

## Repository Upload

```
User Uploads ZIP
        │
        ▼
Generate Repository ID
        │
        ▼
Create Database Record
        │
        ▼
Create Storage Directory
        │
        ▼
Save ZIP
        │
        ▼
Extract Repository
        │
        ▼
Update Repository Status
```

---

## Repository Analysis Workflow

```
Repository
     │
     ▼
Scan Files
     │
     ▼
Detect Technologies
     │
     ▼
Analyze Dependencies
     │
     ▼
Analyze Architecture
     │
     ▼
Store Results
```

---

## AI Workflow

```
Repository
      │
      ▼
Extract Source Code
      │
      ▼
Chunk Source Code
      │
      ▼
Generate Embeddings
      │
      ▼
Store in ChromaDB
      │
      ▼
User Question
      │
      ▼
Similarity Search
      │
      ▼
Relevant Context
      │
      ▼
Gemini/OpenAI
      │
      ▼
AI Response
```

---

# Current Features

* Repository CRUD APIs
* Repository metadata storage
* ZIP upload preparation
* Repository directory creation
* ZIP extraction
* SQLAlchemy ORM
* PostgreSQL integration
* Clean Layered Architecture
* Storage Service

---

# Database Design

## repositories

| Column        | Description                  |
| ------------- | ---------------------------- |
| id            | Repository UUID              |
| name          | Repository Name              |
| original_name | Original Uploaded Filename   |
| storage_path  | Repository Storage Path      |
| status        | Repository Processing Status |
| created_at    | Created Timestamp            |
| updated_at    | Updated Timestamp            |

---

# Storage Structure

```
storage/
└── repositories_collection/
    └── <repository_id>/
        ├── source.zip
        └── extracted/
```

---

# Design Principles

* Clean Architecture
* Layered Architecture
* Separation of Concerns
* Repository Pattern
* Service Layer Pattern
* Single Responsibility Principle
* Dependency Injection
* Scalable Project Structure

---

# Future Roadmap

## Phase 1

* Repository CRUD
* ZIP Upload
* Storage Management

## Phase 2

* Repository Scanner
* Language Detection
* Framework Detection
* Dependency Analysis

## Phase 3

* Architecture Analysis
* Documentation Generator
* API Documentation
* Database Documentation

## Phase 4

* Code Chunking
* Embedding Generation
* ChromaDB Integration
* AI Repository Chat
* Retrieval-Augmented Generation (RAG)

## Phase 5

* Authentication
* Redis Caching
* Background Jobs
* GitHub Actions CI/CD
* Docker Compose
* Cloud Deployment
* Monitoring & Logging
* Kubernetes (Learning & Scaling)

---

# Future Improvements

* Multi-user authentication
* Repository sharing
* Team workspaces
* Code visualization
* Repository comparison
* Automated changelog generation
* Code quality analysis
* Security vulnerability scanning
* Performance analysis
* AI-generated onboarding tutorials

---

# Installation

```bash
git clone <repository-url>

cd ai-developer-onboarding-assistant

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

docker compose up -d

uvicorn app.main:app --reload
```


# Future Deployment Architecture

```
GitHub
    │
    ▼
GitHub Actions
    │
    ▼
Docker Build
    │
    ▼
Cloud Deployment
    │
    ▼
Nginx
    │
    ▼
FastAPI
    │
    ├──────────────┐
    ▼              ▼
PostgreSQL      Redis
    │
    ▼
ChromaDB
```

---

