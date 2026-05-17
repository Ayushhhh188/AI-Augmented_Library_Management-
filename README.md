# CCL AI-Augmented Library Management System

An AI-powered digital library platform developed for Central Coalfields Limited (CCL) during internship work, designed to modernize document management, intelligent search, and secure access control.

[Python](https://img.shields.io/badge/Python-3.9+-blue.svg) | [Flask](https://img.shields.io/badge/Flask-2.0+-green.svg) | [MongoDB](https://img.shields.io/badge/MongoDB-Atlas-brightgreen.svg) | [Cohere](https://img.shields.io/badge/Cohere-LLM-orange.svg) | [Google OAuth](https://img.shields.io/badge/Google-OAuth2.0-red.svg)

---

## Features

### Authentication & Security
- Google OAuth 2.0 Authentication – Secure login via Google accounts
- Role-Based Access Control (RBAC) – Admin and User roles managed via MongoDB
- Secure OpenID Connect flow with nonce validation

### Document Management
- Single Upload – Quick document addition
- Bulk Upload – Mass document ingestion
- Multi-format Support – PDF, DOC/DOCX, TXT files

### Advanced Search
- Title-based search
- Recent uploads tracking
- Metadata filtering

### AI-Powered Chatbot
- Context-aware document assistance using Cohere LLM
- Document summarization and intelligent querying
- Natural language document interaction

### User Experience
- Responsive UI with modal-based navigation
- MongoDB Atlas integration for seamless data management

---

## Tech Stack

| Category | Technologies |
|----------|-------------|
| Backend | Python, Flask, Authlib |
| Frontend | HTML5, CSS3, JavaScript |
| Database | MongoDB Atlas, PyMongo |
| AI / NLP | Cohere Command-R+ API |
| Authentication | Google OAuth 2.0 |

---

## Authentication Architecture

Google OAuth -> Flask Session -> MongoDB Role Verification

- Google OAuth handles authentication
- MongoDB handles authorization and role management
- Secure OpenID Connect flow with nonce validation

---

## Project Structure
CC_LIBRARY_SYSTEM/
│
├── static/
│   ├── images/
│   ├── uploads/
│   ├── style.css
│   ├── home.css
│   └── stylelogin.css
│
├── templates/
│   ├── home.html
│   ├── index.html
│   ├── login.html
│   ├── search_results.html
│   ├── manage_uploads.html
│   └── admin_users.html
│
├── tests/
│   └── test_app.py
│
├── app.py
├── db.py
├── .env
└── requirements.txt

## Setup Instructions

### 1. Clone Repository
bash
git clone <your-repo-url>
cd CC_LIBRARY_SYSTEM

###2. Install Dependencies
bash

pip install -r requirements.txt

###3. Configure Environment Variables

Create a .env file in the root directory:
env

GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
COHERE_API_KEY=your_cohere_api_key
SECRET_KEY=your_secret_key

###4. Configure Google OAuth

Add the following URIs in Google Cloud Console:
Type	URI
Authorized JavaScript Origins	http://localhost:5000
http://127.0.0.1:5000
Authorized Redirect URIs	http://localhost:5000/auth/callback
http://127.0.0.1:5000/auth/callback
###5. Run Application
bash
python app.py

Access the application at: http://localhost:5000
Admin Access

Admin roles are managed through the MongoDB users collection.

Example user document:
json

{
  "email": "admin@gmail.com",
  "role": "admin"
}

Note: Regular users have "role": "user" or no role field.
AI Chatbot Capabilities

The integrated chatbot can:

    Search documents intelligently

    Answer document-related questions

    Summarize uploaded files

    Retrieve contextual information from stored resources

Project Objective

To create a secure, AI-enhanced digital library system that improves:

    Accessibility – Easy document discovery and retrieval

    Document Organization – Structured storage and metadata management

    Intelligent Knowledge Retrieval – AI-powered search and Q&A for enterprise environments

Future Enhancements

    Admin analytics dashboard

    Semantic vector search

    Cloud document storage (AWS S3 / Azure Blob)

    Mobile-responsive enhancements

    Activity and audit logging

    Enterprise domain restrictions (SSO integration)

Developed By

Ayush Ranjan
Systems Intern - Central Coalfields Limited
License

This project was developed as part of an internship at Central Coalfields Limited (CCL).
