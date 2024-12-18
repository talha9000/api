from fastapi import APIRouter
from fastapi import FastAPI,Request,APIRouter,HTTPException,Response
from fastapi.requests import Request
from App.read_env import env_data
from App.connect_db import MongoDBConnection

uri=""
Mongoconnect=None
async def on_startup():
    global uri,Mongoconnect
    print("Application is starting up...")
    try:
 
        if not env_data:
            raise ValueError("ERror no env data found")
        uri=f"mongodb://{env_data['usrname']}:{env_data['passwd']}@{env_data['url']}:{env_data['port']}"
        Mongoconnect=MongoDBConnection(uri,'datanal')
        await Mongoconnect.connect()
    except Exception as e:
        return f"Error during startup: {e}"

async def on_shutdown():
    print("Application is shutting down...")
    Mongoconnect.close()
router=APIRouter(on_startup=[on_startup] ,on_shutdown=[on_shutdown])

@router.get("/conect_mongo")
async def get_uri():
    #Mongoconnect.connect()
    collect=await Mongoconnect.delete_collection("harami")
    print(collect)