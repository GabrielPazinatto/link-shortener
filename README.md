# Full-Stack URL Shortener

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100-green?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-Next.js-black?logo=nextdotjs&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-DB-blue?logo=postgresql&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-black?logo=typescript&logoColor=white)

This is a full-stack URL shortener application built as a portfolio project, demonstrating a modern web architecture with a clear separation of concerns. The backend is a robust RESTful API built with **FastAPI**, and the frontend is a dynamic, reactive Single-Page Application (SPA) built with **React (Next.js)** and **TypeScript**.


![alt text](./images/user_page.png)

## Key Features

* **Full User Authentication:** Secure user registration and login system.
* **JWT (OAuth2) Security:** All user-specific actions are protected. Passwords are never stored in plain text, using `bcrypt` for hashing.
* **URL Management (CRUD):**
    * Authenticated users can create new shortened URLs.
    * List all URLs owned by the logged-in user.
    * Delete individual URLs.
    * Delete multiple URLs in a single batch request.
* **Public Redirects:** A root-level endpoint (`/{short_url}`) that redirects to the original long URL. Currently, a second domain (shortify.rf.gd) is being used to process the redirects.
* **Data Validation:** `Pydantic` models on the backend ensure all API inputs and outputs are type-safe and valid.
* **Reactive UI:** A responsive SPA frontend that manages user state (via Context and `localStorage`) without page reloads.

## Tech Stack

The project is cleanly separated into two main components: `backend` and `frontend`.

### Backend (Python 🐍)

* **Framework:** [**FastAPI**](https://fastapi.tiangolo.com/)
* **Database:** [**PostgreSQL**](https://www.postgresql.org/)
* **ORM:** [**SQLAlchemy**](https://www.sqlalchemy.org/)
* **Data Validation:** [**Pydantic**](https://docs.pydantic.dev/latest/)
* **Authentication:** [**python-jose**](https://github.com/mpdavis/python-jose) (for JWTs) & [**bcrypt**](https://pypi.org/project/bcrypt/) (for hashing)
* **Server:** [**Uvicorn**](https://www.uvicorn.org/) (ASGI)
* **Dependencies:** `python-dotenv`, `psycopg2-binary`

### Frontend (React ⚛️)

* **Framework:** [**React (Next.js)**](https://nextjs.org/)
* **Language:** [**TypeScript**](https://www.typescriptlang.org/)
* **Styling:** [**Tailwind CSS**](https://tailwindcss.com/)
* **State Management:** React Hooks (`useState`, `useContext`) & `localStorage`
* **API Communication:** `fetch` API

## Project Architecture

The application follows a standard monorepo pattern with a decoupled backend and frontend. The frontend (Next.js) is purely a client that consumes the FastAPI backend.


```text
/
├── backend/
|   |   
│   ├── main.py              # Main FastAPI app (CORS, routers, /token, /{short_url})
│   ├── api/
│   │   ├── routers/
│   │   │   ├── users.py     # Endpoints for /users/*
│   │   │   └── urls.py      # Endpoints for /urls/*
│   │   └── auth.py          # Authentication logic (JWT, get_current_user)
│   ├── database/
│   │   ├── connection.py    # SQLAlchemy session setup
│   │   ├── functions.py     # All CRUD/service logic
│   │   ├── models.py        # SQLAlchemy table models
│   │   └── schemas.py       # Pydantic data schemas
│   └── utils.py             # Utility functions (password hashing)
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── views/       # UI Components (LoginView, UserView, etc.)
│   │   ├── app/
│   │   │   ├── layout.tsx   # Global layout (fonts, theme)
│   │   │   └── page.tsx     # Main SPA logic (view router)
│   │   └── ...
└── README.md

```


## API Endpoints

All endpoints are prefixed with `/api`. Endpoints marked as **Authenticated** require a valid JWT `Bearer` token in the `Authorization` header.

### Authentication & User Management

| Method | Path | Description | Authentication |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/users/` | Registers a new user. | None |
| `POST` | `/api/token` | Authenticates a user (using form-data) and returns a JWT. | None |
| `GET` | `/api/users/me/urls` | Gets a list of all URLs for the current user. | **Authenticated** |
| `DELETE` | `/api/users/me` | Deletes the current user's account and all their URLs. | **Authenticated** |
---

### URL Management

| Method | Path | Description | Authentication |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/urls/` | Creates a new short URL. Expects a JSON body: `{"url": "..."}`. | **Authenticated** |
| `DELETE` | `/api/urls/` | Deletes one or more short URLs. Expects a JSON body with a list of strings: `["url1", "url2"]`. | **Authenticated** |

---

### Redirect & Health Check

| Method | Path | Description | Authentication |
| :--- | :--- | :--- | :--- |
| `HEAD` | `/api/{short_url}` | Checks if a short URL exists and returns redirect headers (e.g., `Location`). | None |
| `GET` | `/api/hello` | A simple health-check endpoint to confirm the API is running. | None |

## Database Schema

The application uses a PostgreSQL database with two main tables, `users` and `urls`. The relationship is a one-to-many: one user can own many URLs.



### Users Table (`users`)

Stores user account information and credentials.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | SERIAL | **PRIMARY KEY** | Unique identifier for the user. |
| `username` | VARCHAR(20) | **NOT NULL**, **UNIQUE** | The user's public-facing name. |
| `password` | VARCHAR(255) | **NOT NULL** | The user's hashed password (using bcrypt). |

### URLs Table (`urls`)

Stores the shortened URLs and their original destinations, linked to a user.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | SERIAL | **PRIMARY KEY** | Unique identifier for the URL record. |
| `owner_id` | INTEGER | **FOREIGN KEY** (references `users.id`), **ON DELETE CASCADE** | Links the URL to its owner in the `users` table. If the user is deleted, their URLs are also deleted. |
| `url` | TEXT | **NOT NULL** | The original, long URL that the user wants to shorten. |
| `short_url` | TEXT | **NOT NULL**, **UNIQUE** | The generated 6-character unique short string. |

## Frontend Architecture

The frontend is a **Single-Page Application (SPA)** built with **React** and **TypeScript**, using a component-based architecture. A central "view router" (`page.tsx`) manages the application's state and decides which of the four main "views" (components) to display.


This approach avoids full page reloads, creating a fast, modern user experience.

The frontend was mainly built using [lovable](https://lovable.dev/), but the integration with the backend was done manually.

### Component Breakdown

| Component | File | Responsibility |
| :--- | :--- | :--- |
| **View Router** | `page.tsx` | The main page of the app. It holds the `view` state (`"home"`, `"login"`, `"register"`, `"user"`) and renders the appropriate component based on that state. It's the "brain" of the frontend. |
| **Home View** | `home-view.tsx` | The primary landing page for all users. It provides simple navigation, with buttons to log in, register, or go to the user page (if already logged in). |
| **Register View** | `register-view.tsx` | Handles new user registration. It provides a form for `username`, `password`, and `confirmPassword`, performs client-side validation (e.g., password match), and calls the `POST /api/users/` backend endpoint. |
| **Login View** | `login-view.tsx` | Handles user authentication. It provides a form for `username` and `password` and calls the `POST /api/token` endpoint. On success, it saves the received `accessToken` to `localStorage` and calls the `onLoginSuccess` prop to update the main app state. |
| **User View** | `user-view.tsx` | The main user dashboard (the "logged-in" page). This is the most complex component. It uses the `accessToken` from `localStorage` to: <br/> 1. Fetch all user URLs (`GET /api/users/me/urls`). <br/> 2. Create new short URLs (`POST /api/urls/`). <br/> 3. Delete one or more URLs (`DELETE /api/urls/`). <br/> 4. Handle logout (by clearing `localStorage`). |