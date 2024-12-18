import os
from dotenv import load_dotenv

 
load_dotenv(interpolate=True, verbose=True, override=True)
 
try:
    env_data = {
        "url": os.getenv("mongo_url"),
        "usrname":os.getenv("username"),
        "passwd":os.getenv("password"),
        "port":os.getenv("port"),
        # argon 2
         "timecost":os.getenv("timecost"),
             "memorycost":os.getenv("memorycost"),
                 "pararellism":os.getenv("pararellism"),
                     "salt_length":os.getenv("salt_length"),
                               "hash_length":os.getenv("hash_length"),
    }   

    # Check if any required environment variable is missing or empty
    for k, v in env_data.items():  # Use .items() to correctly unpack the dictionary
        if not v:
            raise ValueError(f"Value for {k} is missing or empty")

except ValueError as e:
    print(f"Error loading environment data: {e}")
    raise BaseException(f"Error loading data from environment: {e}")  # Raise with BaseException

 
 