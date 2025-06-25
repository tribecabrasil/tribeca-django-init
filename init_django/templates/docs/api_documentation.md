# Project API Documentation

This document details the main endpoints and flows of the project's REST API, enabling programmatic integration with the core functionalities of the system.

## Authentication
- Supports session (cookie-based) authentication and Firebase integration.
- Endpoints for login, logout, registration, and password recovery.

## Main Endpoints

### Users
- `POST /accounts/register/`: User registration
- `POST /accounts/login/`: User login
- `POST /accounts/logout/`: User logout
- `POST /accounts/verify/`: Email/token verification
- `POST /accounts/password/reset/`: Password reset request

### Anamnesis
- `GET /accounts/leads-anamnese/`: List anamnesis records
- `GET /accounts/lead-anamnese/<id>/`: Retrieve a specific anamnesis
- `POST /website/anamnese/`: Submit a new anamnesis
- `POST /website/openai-validate-anamnese/`: Validate anamnesis via OpenAI

### Contact
- `POST /website/contact/`: Send a contact message

### Webhooks
- `POST /website/receive-anamnese-webhook/`: Receive external anamnesis data

## Request Examples
