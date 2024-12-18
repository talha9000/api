from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from Route.main_route import router
from fastapi.responses import *
origins = [
    "http://localhost",  # Allow specific domains
    "http://localhost:3000",  # Example: frontend running on a different port
 
]

app=FastAPI(title="Data cleansing API",description="Data cleansing for further visualisiation")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows access from these origins
    allow_credentials=True,  # Allow credentials such as cookies to be sent
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(router=router)