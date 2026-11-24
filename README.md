# KAVERI AI - Authentication Portal

A secure authentication application built with React, FastAPI, and PostgreSQL.

## Features
- Google OAuth 2.0 login
- Email registration and login
- JWT authentication
- Secure password hashing with Argon2
- Forgot and reset password
- Gmail authorization

## Technology Stack
- React and Vite
- Python and FastAPI
- PostgreSQL and SQLAlchemy
- JWT and Google OAuth 2.0

## Backend Setup
1. Install dependencies: pip install -r requirements.txt
2. Configure backend/.env using backend/.env.example
3. Start: python -m uvicorn app.main:app --reload --port 8000

## Frontend Setup
1. Run npm install
2. Run npm run dev

## API Documentation
http://localhost:8000/docs

## Security
Never commit .env files, OAuth tokens, or credentials. Further security hardening is required before production deployment.
