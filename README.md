\# KAVERI AI – Authentication Portal



A secure authentication portal built using React, FastAPI, and PostgreSQL. The application provides email/password authentication, Google OAuth 2.0 sign-in, JWT-based authentication, and password recovery through email.



\---



\## Project Overview



KAVERI AI is a full-stack authentication application designed to provide users with a secure and user-friendly authentication experience.



The project demonstrates modern web development, backend API development, database integration, authentication, and account recovery.



\### Key Features



\- User registration with email and password.

\- User login with email and password.

\- Google OAuth 2.0 authentication.

\- JWT-based authentication.

\- Secure password hashing.

\- Forgot password functionality.

\- Password reset functionality.

\- Gmail authorization for email services.

\- PostgreSQL database integration.

\- User account management.

\- Logout functionality.

\- React-based responsive user interface.



\---



\## Technology Stack



| Category | Technology |

|---|---|

| Frontend | React.js |

| Frontend Build Tool | Vite |

| Backend | Python |

| Backend Framework | FastAPI |

| Database | PostgreSQL |

| Authentication | JWT |

| Social Login | Google OAuth 2.0 |

| Password Security | Password Hashing |

| Email Integration | Gmail API |

| API Testing | Swagger UI |

| Version Control | Git |

| Source Code Hosting | GitHub |



\---



\## System Architecture



```text

&#x20;                 USER

&#x20;                   |

&#x20;                   v

&#x20;            REACT FRONTEND

&#x20;               App.jsx

&#x20;                   |

&#x20;                   v

&#x20;             FASTAPI BACKEND

&#x20;               main.py

&#x20;                   |

&#x20;         +---------+---------+

&#x20;         |         |         |

&#x20;         v         v         v

&#x20;      EMAIL      GOOGLE     JWT

&#x20;      AUTH       OAUTH      AUTH

&#x20;         |         |         |

&#x20;         +---------+---------+

&#x20;                   |

&#x20;                   v

&#x20;              POSTGRESQL

&#x20;                   |

&#x20;                   v

&#x20;             USER RECORDS

```



\### Application Components



\*\*Frontend\*\*

\- `App.jsx` – Main application interface.

\- `main.jsx` – React application entry point.

\- `App.css` – Application styling.



\*\*Backend\*\*

\- `main.py` – FastAPI application entry point.

\- `security.py` – Password security functions.

\- `jwt.py` – JWT token handling.

\- `google\_auth.py` – Google OAuth authentication.

\- `oauth.py` – OAuth client configuration.

\- `gmail\_auth.py` – Gmail authorization.

\- `email\_auth.py` – Email authentication.

\- `password\_reset.py` – Password recovery functionality.

\- `email\_service.py` – Email service integration.

\- `database.py` – PostgreSQL database connection.

\- `user.py` – User database model.



\---



\## Project Directory Structure



```text

kaveri-ai-authentication-portal/

│

├── backend/

│   ├── app/

│   │   ├── main.py

│   │   ├── security.py

│   │   ├── jwt.py

│   │   ├── database.py

│   │   ├── models/

│   │   ├── routers/

│   │   │   ├── google\_auth.py

│   │   │   ├── email\_auth.py

│   │   │   ├── gmail\_auth.py

│   │   │   └── password\_reset.py

│   │   └── services/

│   │       └── email\_service.py

│   │

│   ├── venv/

│   └── requirements.txt

│

├── frontend/

│   ├── public/

│   ├── src/

│   │   ├── assets/

│   │   │   └── kaveri-ai-logo.png

│   │   ├── App.jsx

│   │   ├── App.css

│   │   └── main.jsx

│   │

│   ├── package.json

│   └── index.html

│

├── .gitignore

└── README.md

```



\*Note: This is a project overview. Some folders and filenames may vary according to the current source code.\*



\---



\## Prerequisites



Install the following tools before running the application:



1\. Python 3.11 or later.

2\. Node.js and npm.

3\. PostgreSQL 16 or later.

4\. Git.

5\. Docker Desktop (optional, for running PostgreSQL in Docker).

6\. Google Cloud account for Google OAuth configuration.



\---



\## Installation and Setup



\### 1. Clone the Repository



```bash

git clone https://github.com/bavajanmasunuri539-hue/-kaveri-ai-authentication-portal.git

```



Navigate into the project:



```bash

cd -kaveri-ai-authentication-portal

```



\### 2. Backend Setup



Navigate to the backend directory:



```powershell

cd backend

```



Create a Python virtual environment:



```powershell

python -m venv venv

```



Activate the environment:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



Install backend dependencies:



```powershell

pip install -r requirements.txt

```



\### 3. PostgreSQL Database Setup



You can use an existing PostgreSQL installation or run PostgreSQL using Docker.



Example Docker command:



```powershell

docker run --name kaveri-postgres -e POSTGRES\_USER=kaveri\_user -e POSTGRES\_PASSWORD=YOUR\_STRONG\_PASSWORD -e POSTGRES\_DB=kaveri\_auth -p 5432:5432 -v kaveri\_postgres\_data:/var/lib/postgresql/data -d postgres:16

```



Replace `YOUR\_STRONG\_PASSWORD` with a strong database password.



Configure the backend database connection using your application's environment configuration.



\### 4. Environment Configuration



Create a `.env` file in the appropriate backend configuration directory.



Configure the required values according to the variable names used by the application.



Typical configuration includes:



```env

DATABASE\_URL=your\_postgresql\_connection\_string

SECRET\_KEY=your\_secure\_random\_secret

GOOGLE\_CLIENT\_ID=your\_google\_client\_id

GOOGLE\_CLIENT\_SECRET=your\_google\_client\_secret

```



Additional Gmail OAuth and email configuration may be required for password recovery.



\*\*Important:\*\* These are example configuration names. Confirm the exact variable names in the backend source code before using them.



Never upload `.env`, OAuth client secrets, Gmail tokens, or database passwords to GitHub.



\### 5. Run the Backend



From the backend directory:



```powershell

.\\venv\\Scripts\\python.exe -m uvicorn app.main:app --reload --port 8000

```



Backend URL:



```text

http://localhost:8000

```



Swagger API documentation:



```text

http://localhost:8000/docs

```



\### 6. Frontend Setup



Open another PowerShell window.



Navigate to the frontend directory:



```powershell

cd C:\\Users\\bavaj\\kaveri-ai-authentication-portal\\frontend

```



Install frontend dependencies:



```powershell

npm install

```



Start the frontend:



```powershell

npm run dev -- --host 127.0.0.1 --port 5176 --strictPort

```



Open the application:



```text

http://127.0.0.1:5176/

```



\---



\## Authentication Workflows



\### 1. Email and Password Authentication



1\. User opens the login page.

2\. User enters an email address and password.

3\. Frontend sends the login request to FastAPI.

4\. Backend validates the user credentials.

5\. Password verification is performed.

6\. The application creates an authentication token when login succeeds.



\### 2. Google OAuth 2.0 Authentication



1\. User selects Continue with Google.

2\. Application redirects the user to Google.

3\. User completes Google authentication.

4\. Google redirects the user to the configured callback.

5\. Backend processes the OAuth response.

6\. The application authenticates the user.



\### 3. Password Recovery



1\. User selects Forgot Password.

2\. User enters their registered email address.

3\. Backend processes the password recovery request.

4\. A password reset email is sent through the configured email service.

5\. User opens the reset link.

6\. User creates a new password.



\---



\## API Endpoints



The following endpoints are implemented in the application.



| Method | Endpoint | Purpose |

|---|---|---|

| GET | `/health` | Health check |

| GET | `/auth/google/login` | Start Google login |

| GET | `/auth/google/callback` | Google OAuth callback |

| GET | `/auth/google/me` | Get authenticated Google user |

| POST | `/auth/google/logout` | Google authentication logout |

| POST | `/auth/email/register` | Register a user |

| POST | `/auth/email/login` | Email/password login |

| GET | `/auth/gmail/login` | Start Gmail authorization |

| GET | `/auth/gmail/callback` | Gmail OAuth callback |

| POST | `/auth/password/forgot` | Request password reset |

| POST | `/auth/password/reset` | Reset password |



Check the FastAPI Swagger documentation for the exact request and response formats.



\---



\## Testing



Test the following application features:



| Test Case | Expected Result |

|---|---|

| User registration | Account is created |

| Valid login | User is authenticated |

| Invalid password | Login is rejected |

| Google login | Google authentication succeeds |

| Forgot password | Recovery request is processed |

| Password reset | Password is updated |

| Logout | User session ends |

| Database connection | Backend connects to PostgreSQL |

| Health check | Backend reports its health |



\---



\## Security Considerations



Security is important for authentication applications.



Recommended production security measures:



\- Use HTTPS.

\- Store secrets in environment variables or a secrets manager.

\- Never commit credentials to GitHub.

\- Use strong password hashing.

\- Protect JWT tokens.

\- Implement token expiration and secure refresh handling.

\- Configure restrictive CORS policies.

\- Protect authentication endpoints against abuse.

\- Apply CSRF protection where applicable.

\- Validate all user inputs.

\- Avoid exposing sensitive error messages.

\- Rotate any credentials that have been exposed.

\- Use secure cookie settings when cookie-based authentication is implemented.



\*\*Note:\*\* This project is a development implementation. Complete a security review before production deployment.



\---



\## Future Enhancements



\- Docker containerization.

\- Docker Compose orchestration.

\- GitHub Actions CI/CD pipeline.

\- AWS deployment.

\- Nginx reverse proxy.

\- HTTPS with SSL certificates.

\- Prometheus monitoring.

\- Grafana dashboards.

\- Automated backend and frontend testing.

\- Role-based access control.

\- Multi-factor authentication.



\---



\## Developer



\*\*Project Name:\*\* KAVERI AI Authentication Portal



\*\*Developer:\*\* Bavajan Masunuri



\*\*GitHub:\*\* \[bavajanmasunuri539-hue](https://github.com/bavajanmasunuri539-hue)



\*\*Repository:\*\* \[KAVERI AI Authentication Portal](https://github.com/bavajanmasunuri539-hue/-kaveri-ai-authentication-portal)



\---



\## License



Choose and add an appropriate open-source license before distributing this project as open source.



\---



\## Acknowledgements



\- React

\- FastAPI

\- PostgreSQL

\- Google OAuth 2.0

\- Gmail API

\- Python

\- Vite

