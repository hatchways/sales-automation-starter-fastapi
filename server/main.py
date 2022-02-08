import sqlalchemy

from dotenv import dotenv_values
from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from api.routers import auth, users, campaigns, prospects


config = dotenv_values(".env")

app = FastAPI(
    title="Sales Automation - Python (FastAPI)",
    description="Sales Automation Work Simulation",
    version="0.0.1",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(campaigns.router)
app.include_router(prospects.router)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(_, exc):
    return JSONResponse({"error": exc.detail}, status_code=exc.status_code)


if __name__ == "__main__":
    import uvicorn
    from api.database import Base

    engine = sqlalchemy.create_engine(config.get("DATABASE_URL"))
    Base.metadata.create_all(engine)

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=3001,
    )
