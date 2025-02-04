import os
import motor.motor_asyncio
from bson.objectid import ObjectId
from pymongo import ReturnDocument
from fastapi import HTTPException
from passlib.hash import bcrypt

class KineService:
    def __init__(self):
        MONGO_URL = os.getenv("DATABASE_URL")
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
        self.database = self.client.fastapi
        self.collection = self.database.kine


    def get_collection(self, name):
        return self.database.get_collection(name)

    async def close(self):
        if self.client:
            self.client.close()

    async def create(self, kine_data):
        """
        Create a kine with the `kine_data` object.

        Args:
            kine_data (dict): The kine data to be inserted.

        Returns:
            str: The ID of the inserted kine.
        """
        try:
            result = await self.collection.insert_one(kine_data)
            return str(result.inserted_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        

    # Read One: Récupérer un kine par son ID
    async def read_one(self, id):
        """
        Read a kine with the `kine_id` object.

        Args:
            id (str): The kine id to be read.

        Returns:
            _DocumentType: The kine document inserted.
        """
        kine = await self.collection.find_one({"_id": ObjectId(id)})
        return kine
    
    # Read : Récupérer un kine par son email et son mot de passe
    async def read(self, email: str, password: str):
        """
        Read a kine with his email and password.

        Args:
            email (str): The kine email.
            password (str): The kine password.

        Returns:
            _DocumentType: The kine document inserted.
        """
        kine = await self.collection.find_one({"email": email})     
        # Vérifier si le mot de passe correspond (en supposant que le mot de passe est haché)
        if kine and bcrypt.verify(password, kine["mdp"]):
            return kine
        else:
            return None
    
    # Read All: Récupérer tous les patients
    async def read_all(self, id):
        """
        Read all patients from a specific kine.

        Args:
            id (str): The kine id from which we retrieve a list of matching patients.

        Returns:
            List[dict]: A list of patients.
        """
        pipeline = [
            {
                "$match": {"_id": ObjectId(id)}
            },
            {
                '$project': {
                    '_id': {'$toString': '$_id'}
                }
            },
            {
                "$lookup": {
                    "from": "patients",
                    "localField": "_id",
                    "foreignField": "kineid",
                    "as": "patients",
                    "pipeline": [
                        {
                            "$project": {
                                "_id": 1,
                                "nom": 1,
                                "prenom": 1
                            }
                        }
                    ]
                }
            }
        ]      
        # Exécution de l'agrégation
        async for doc in self.collection.aggregate(pipeline): # doc est un dictionnaire
            return doc.get("patients", [])
        return []
    
    # Update: Mettre à jour un kiné par son ID
    async def update(self, id, update_fields):
        """
        Update a kine with the `update_field` object.

        Args:
            id (str): The kine id to be updated.
            update_fields (dict): The kine data to be updated.

        Returns:
            _DocumentType: The kine document updated.
        """
        update_result = await self.collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": update_fields},
            return_document=ReturnDocument.AFTER,
        )
        return update_result 

    # Delete: Supprimer un document par son ID
    async def delete(self, id):
        """
        Delete a kine with the `kine_id` object.

        Args:
            kine_id (str): The kine id to be deleted.

        Returns:
            str: The ID of the deleted kine.
        """
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count  # Nombre de documents supprimés

