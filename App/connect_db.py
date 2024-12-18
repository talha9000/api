from motor.motor_asyncio import AsyncIOMotorClient
from typing import List


class MongoDBError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
# MongoDB connection class
class MongoDBConnection:
    def __init__(self, uri: str, db_name: str):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None

    async def connect(self):
        try:
            """Establish connection to MongoDB"""
            self.client = AsyncIOMotorClient(self.uri)
            self.db = self.client[self.db_name]
            print(f"Connected to MongoDB database: {self.db_name}")
        except Exception as e:
            raise MongoDBError(f"ERROR CONNECT TO DB DUE TO {e}")
    async def close(self):
        try:
            """Close MongoDB connection"""
            self.client.close()
            print("MongoDB connection closed")
        except Exception as e:
            raise MongoDBError(f"ERROR CLOSE TO DB DUE TO {e}")
        
        
    async def get_collection(self, collection_name: str):
        try:
            """Retrieve a collection from the database"""
            if self.db is None:
                raise Exception("Not connected to the database")
            return self.db[collection_name]
        except Exception as e:
            raise MongoDBError(f"error get collectio due to  {e}")
        
    async def get_all_collections(self):
        try:
            """Retrieve all collections from the database"""
            if self.db is None:
                raise Exception("Not connected to the database")
            
            # Get the collection names from the database
            collection_names = await self.db.list_collection_names()
            return collection_names
        except Exception as e:
            raise MongoDBError(f"Error getting collections: {e}")
        
    async def create_collection(self, collection_name: str):
        try:
            """Create a new collection in the database"""
            if self.db is None:
                raise Exception("Not connected to the database")
            if collection_name in await self.db.list_collection_names():
                raise Exception(f"Collection '{collection_name}' already exists")
            await self.db.create_collection(collection_name)
            print(f"Collection '{collection_name}' created successfully.")
        except Exception as e:
            raise MongoDBError(f"error create scollectio due to  {e}")
            
    async def delete_collection(self, collection_name: str):
        try:
            """Delete a collection from the database"""
            if self.db is None:
                raise Exception("Not connected to the database")
            if collection_name not in await self.db.list_collection_names():
                raise Exception(f"Collection '{collection_name}' does not exist")
            await self.db.drop_collection(collection_name)
            print(f"Collection '{collection_name}' deleted successfully.")
        except Exception as e:
            raise MongoDBError(f"error delete collectio due to  {e}")
    # CRUD Operations
    async def insert_one(self, collection_name: str, document: dict):
        try:
            """Insert a single document into a collection"""
            collection = await self.get_collection(collection_name)
            result = await collection.insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
           raise MongoDBError(f"error insert_one collectio due to  {e}")
            
    async def insert_many(self, collection_name: str, documents: List[dict]):
        try:
            """Insert multiple documents into a collection"""
            collection = await self.get_collection(collection_name)
            result = await collection.insert_many(documents)
            return [str(id) for id in result.inserted_ids]
        except Exception as e:
           raise MongoDBError(f"error insert_many collectio due to  {e}")
            
    async def find_one(self, collection_name: str, query: dict):
        try:
            """Find a single document based on the query"""
            collection = await self.get_collection(collection_name)
            document = await collection.find_one(query)
            return document
        except Exception as e:
           raise MongoDBError(f"error find collectio due to  {e}")
            
    async def find_many(self, collection_name: str, query: dict = {}, limit: int = 10):
        try:
            """Find many documents based on the query"""
            collection = await self.get_collection(collection_name)
            documents = await collection.find(query).limit(limit).to_list(length=limit)
            return documents
        except Exception as e:
            raise MongoDBError(f"error find many collectio due to  {e}")
    async def update_one(self, collection_name: str, query: dict, update_data: dict):
        try:
            """Update a single document based on the query"""
            collection = await self.get_collection(collection_name)
            result = await collection.update_one(query, {'$set': update_data})
            return result.modified_count
        except Exception as e:
            raise MongoDBError(f"error update one collectio due to  {e}")
    async def delete_one(self, collection_name: str, query: dict):
        try:
            """Delete a single document based on the query"""
            collection = await self.get_collection(collection_name)
            result = await collection.delete_one(query)
            return result.deleted_count
        except Exception as e:
            raise MongoDBError(f"error delete one collectio due to  {e}")
    async def delete_many(self, collection_name: str, query: dict):
        try:
            """Delete many documents based on the query"""
            collection = await self.get_collection(collection_name)
            result = await collection.delete_many(query)
            return result.deleted_count
        except Exception as e:
            raise MongoDBError(f"error delete_many collectio due to  {e}")