# FastAPI Banking Application System

## Overview
A RESTful API built with FastAPI for managing user credit applications. The system allows users to register, login, apply for credit, and manage their credit applications.

## User Guide

### Objective
This API provides a complete credit application system where users can:
- Register and manage their accounts
- Banking operations (deposits, withdrawals, transfers)
- Credit management
- Real-time notifications
- Track application status
- View credit details and payment information
- Secure authentication

### Authentication

All endpoints except registration and login require authentication using JWT tokens. Include the token in the Authorization header:

Authorization: Bearer <tu_token_de_acceso>


### Core Features

1. **User Management**
   - Registration: `POST /api/v1/users/`
   - Profile management: `GET /api/v1/users/me`
   - Profile updates: `PUT /api/v1/users/`

2. **Account Operations**
   - Create account: `POST /api/v1/accounts/`
   - View accounts: `GET /api/v1/accounts/`
   - Check balance: `GET /api/v1/accounts/{account_id}/balance`

3. **Transactions**
   - Deposit: `POST /api/v1/transactions/{account_id}/deposit`
   - Withdrawal: `POST /api/v1/transactions/{account_id}/withdrawal`
   - Transfer: `POST /api/v1/transactions/{account_id}/transfer`
   - Transaction history: `GET /api/v1/transactions/{account_id}/history`

4. **Credit Management**
   - Apply for credit: `POST /api/v1/credits/`
   - View credits: `GET /api/v1/credits/`
   - Credit status: `GET /api/v1/credits/{credit_id}`

5. **Notifications**
   - View notifications: `GET /api/v1/notifications/`
   - Mark as read: `POST /api/v1/notifications/{notification_id}/read`
   - Mark all as read: `POST /api/v1/notifications/read-all`


## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

### Installation Steps

1. Clone the repository:
```bash
git clone <https://github.com/jecs27/banking_api_fastapi.git>
cd banking-api
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

5. Initialize the database:
```bash
alembic upgrade head
```

6. Run the application:
```bash
uvicorn main:app --reload
```

## Project Architecture

### Project Structure

```
src/
├── application/       # Application business logic
│   └── services/      # Business services
├── domain/            # Domain models and business rules
├── infrastructure/    # External concerns
│   ├── config/        # Configuration
│   ├── models/        # Database models
│   └── repositories/  # Data access
└── presentation/      # API interface
    ├── api/           # API routes
    └── schemas/       # Data transfer objects
```


### Architecture Explanation

This project follows Clean Architecture principles with a focus on:

1. **Separation of Concerns**: Clear boundaries between layers
2. **Dependency Inversion**: Core business logic doesn't depend on external frameworks
3. **Domain-Driven Design**: Business logic organized around domain models
4. **Repository Pattern**: Abstraction of data persistence
5. **Service Layer**: Orchestration of business operations

### API Flow Diagram

``` mermaid
graph TD
A[Client] -->|HTTP Request| B[FastAPI Routes]
B -->|DTO Validation| C[Services Layer]
C -->|Business Logic| D[Repositories]
D -->|Data Access| E[Database]
C -->|Events| F[Notification Service]
F -->|Email/Push| G[External Services]
```

## Security Features

- JWT-based authentication
- Password hashing using bcrypt
- Role-based access control
- Request validation
- CORS protection
- Rate limiting

## Contributing

Please fork the repository and submit your pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.