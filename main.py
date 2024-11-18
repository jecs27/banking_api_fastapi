from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.config.settings import settings
from src.presentation.api.routes import user_routes, auth_routes, account_routes, credit_routes, transaction_routes

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.swagger_ui_parameters = {
    "defaultModelsExpandDepth": -1,
    "displayRequestDuration": True,
    "docExpansion": "none",
    "filter": True,
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix=f"{settings.API_V1_STR}/auth", tags=["authentication"])
app.include_router(user_routes.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(account_routes.router, prefix=f"{settings.API_V1_STR}/accounts", tags=["accounts"])
app.include_router(credit_routes.router, prefix=f"{settings.API_V1_STR}/credits", tags=["credits"])
app.include_router(transaction_routes.router, prefix=f"{settings.API_V1_STR}/transactions", tags=["transactions"])

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}