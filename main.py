import os
from configs import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from questionnaire_service.routes import router as router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Asuta API",
    description="API for Asuta Training Form",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    redoc_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

# Enable CORS to allow requests from your React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*', "http://localhost:3000", "https://questionnaire.trainings.admin101.asuta.or.tz", "http://13.61.150.92"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api/v1", tags=["questionnaire"])


if __name__ == "__main__":
    import uvicorn
    
   
    
    uvicorn.run(app="main:app", host="0.0.0.0", port= settings.PORT)
