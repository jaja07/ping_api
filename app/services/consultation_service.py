import os
import motor.motor_asyncio
from bson.objectid import ObjectId
from pymongo import ReturnDocument


class ConsultationService:
    def __init__(self):
        MONGO_URL = os.getenv("DATABASE_URL")
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
        self.database = self.client.fastapi
        self.collection = self.database.consultations

    def get_collection(self, name):
        return self.database.get_collection(name)

    async def close(self):
        if self.client:
            self.client.close()

    async def create(self, consultation_data):
        """
        Create a consulation with the `consultation_data` object.

        Args:
            consultation_data (dict): The consultation data to be inserted.

        Returns:
            str: The ID of the inserted consulation.
        """
        result = await self.collection.insert_one(consultation_data)
        return str(result.inserted_id)

    # Read One: Récupérer une consultation par son ID
    async def read_one(self, id):
        """
        Read a consultation with the `id` object.

        Args:
            id (str): The consultation id to be read.

        Returns:
            _DocumentType: The consultation document read.
        """
        consultation = await self.collection.find_one({"_id": ObjectId(id)})
        return consultation
    
    # Update: Mettre à jour une consultation par son ID
    async def update(self, id, update_fields):
        """
        Update a consultation with the `update_field` object.

        Args:
            id (str): The consultation id to be updated.
            update_fields (dict): The consultation data to be updated.

        Returns:
            _DocumentType: The consultation document updated.
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
        Delete a consultations with the `id` object.

        Args:
            id (str): The consultation id to be deleted.

        Returns:
            str: The number of consultation deleted.
        """
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count  # Nombre de documents supprimés

