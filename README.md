# 🤖 GitHub Copilot × FastAPI

<p align="center">
  <strong>A hands-on GitHub Copilot project for building a simple FastAPI Activity Signup API.</strong>
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green?style=for-the-badge)
![GitHub Copilot](https://img.shields.io/badge/GitHub%20Copilot-AI-purple?style=for-the-badge)

</p>

---

## 🎥 Demo

<p align="center">

<!-- Replace with your demo GIF/video -->
<a href="YOUR_VIDEO_LINK">
  <img src="https://img.shields.io/badge/▶%20Watch%20Demo-Video-red?style=for-the-badge">
</a>

</p>

## ⚡ Project

A simple **FastAPI-based Activities API** where users can:

- 📋 View available activities
- 📝 Sign up for an activity
- ✅ Validate email
- 🚫 Prevent duplicate signup
- 👥 Check activity capacity

All data is stored **in memory**.

## 🔄 Flow

```mermaid
flowchart TD
    A[👤 User] --> B[FastAPI Server]

    B --> C{Request Type}

    C -->|GET| D[GET /activities]
    C -->|POST| E[POST /activities/name/signup]

    D --> F[📋 Activity List]

    E --> G[Validate Email]
    G --> H{Already Registered?}

    H -->|Yes| I[❌ Duplicate Signup]
    H -->|No| J{Capacity Available?}

    J -->|No| K[❌ Activity Full]
    J -->|Yes| L[✅ Add Participant]

    L --> M[🎉 Signup Success]
```

## 🏗️ Architecture

```text
            ┌─────────────────────┐
            │       User          │
            └─────────┬───────────┘
                      │
                      ▼
            ┌─────────────────────┐
            │     FastAPI App     │
            └─────────┬───────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
   GET /activities      POST /activities/{name}/signup
          │                       │
          ▼                       ▼
   Activity Data           Validation Logic
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
                  Email        Capacity      Duplicate
                  Check          Check          Check
                    │             │             │
                    └─────────────┴─────────────┘
                                  │
                                  ▼
                         ✅ Signup Response
```

## 🧠 API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/activities` | List activities |
| `POST` | `/activities/{activity_name}/signup` | Register student |

## 🛠️ Stack

```text
Python
FastAPI
Uvicorn
GitHub Copilot
GitHub Actions
In-Memory Data
```

## 📁 Structure

```text
skills-getting-started-with-github-copilot/
│
├── .devcontainer/
├── .github/
├── .vscode/
├── docs/
├── src/
│   ├── app.py
│   └── README.md
│
├── requirements.txt
├── LICENSE
└── README.md
```

## 🚀 Run

```bash
pip install -r requirements.txt
cd src
python app.py
```

Open:

```text
http://localhost:8000/docs
```

## 🤖 Copilot Learning

This project demonstrates how GitHub Copilot can help with:

```text
Prompt
  ↓
Code Generation
  ↓
API Logic
  ↓
Validation
  ↓
Testing
  ↓
Working FastAPI App
```

## 🎯 Highlights

**FastAPI • GitHub Copilot • REST API • Validation • API Documentation • GitHub Actions**

---

<p align="center">

### 💻 Built with GitHub Copilot + FastAPI

**Learn → Build → Test → Improve**

</p>
