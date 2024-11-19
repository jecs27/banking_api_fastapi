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
graph TB
    subgraph Client Layer
        A[Web Client]
        B[Mobile Client]
    end

    subgraph API Gateway
        C[FastAPI Routes]
        D[Authentication Middleware]
        E[Request Validation]
    end

    subgraph Application Layer
        F[Services]
        subgraph Services
            F1[Account Service]
            F2[Transaction Service]
            F3[Credit Service]
            F4[Payment Service]
            F5[Notification Service]
            F6[Auth Service]
        end
    end

    subgraph Domain Layer
        G[Domain Models]
        subgraph Models
            G1[Account]
            G2[Transaction]
            G3[Credit]
            G4[Payment]
            G5[User]
        end
    end

    subgraph Infrastructure Layer
        H[Repositories]
        I[Database]
        J[External Services]
        subgraph Repositories
            H1[Account Repository]
            H2[Transaction Repository]
            H3[Credit Repository]
            H4[User Repository]
        end
        subgraph External
            J1[Email Service]
            J2[Payment Gateway]
        end
    end

    %% Client to API Gateway
    A --> |HTTP Request| C
    B --> |HTTP Request| C
    
    %% API Gateway Flow
    C --> D
    D --> E
    E --> F
    
    %% Service Layer Interactions
    F1 --> H1
    F2 --> H2
    F3 --> H3
    F4 --> H2
    F5 --> J1
    F6 --> H4
    
    %% Repository to Database
    H --> I
    
    %% Domain Model Relations
    G1 --> G2
    G1 --> G3
    G3 --> G4
    G5 --> G1

    %% External Service Integration
    F5 --> J1
    F4 --> J2

    %% Color coding
    classDef gateway fill:#f9f,stroke:#333,stroke-width:2px
    classDef service fill:#bbf,stroke:#333,stroke-width:2px
    classDef repository fill:#bfb,stroke:#333,stroke-width:2px
    classDef model fill:#fbb,stroke:#333,stroke-width:2px
    classDef external fill:#fff,stroke:#333,stroke-width:2px

    class C,D,E gateway
    class F1,F2,F3,F4,F5,F6 service
    class H1,H2,H3,H4 repository
    class G1,G2,G3,G4,G5 model
    class J1,J2 external
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