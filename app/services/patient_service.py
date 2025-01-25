import os
import motor.motor_asyncio
from bson.objectid import ObjectId
from pymongo import ReturnDocument


class PatientService:
    def __init__(self):
        MONGO_URL = os.getenv("DATABASE_URL")
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
        self.database = self.client.fastapi
        self.collection = self.database.patients


    def get_collection(self, name):
        return self.database.get_collection(name)

    async def close(self):
        if self.client:
            self.client.close()

    async def create(self, patient_data):
        """
        Create a patient with the `patient_data` object.

        Args:
            patient_data (dict): The patients data to be inserted.

        Returns:
            str: The ID of the inserted patient.
        """
        result = await self.collection.insert_one(patient_data)
        return str(result.inserted_id)

    # Read One: Récupérer un patients par son ID
    async def read_one(self, id):
        """
        Read a patient with the `id` object.

        Args:
            id (str): The patient id to be read.

        Returns:
            _DocumentType: The patient document inserted.
        """
        patient = await self.collection.find_one({"_id": ObjectId(id)})
        return patient
        
    # Read All: Récupérer toutes les consultations
    async def read_all(self, id):
        """
        Read all consultations from a specific kine.

        Args:
            id (str): The patient id from which we retrieve a list of matching consultations.

        Returns:
            List[dict]: A list of consultations.
        """
        pipeline = [
            {
                "$match": {"_id": id}
            },
            {
                "$lookup": {
                    "from": "consultations",
                    "localField": "_id",
                    "foreignField": "patientid",
                    "as": "consultations",
                    "pipeline": [
                        {
                            "$project": {
                                "_id": 1,
                                "date_consultation": 1
                            }
                        }
                    ]
                }
            }
        ]      
        # Exécution de l'agrégation
        async for doc in self.collection.aggregate(pipeline):
            return doc.get("consultations", [])
        return []
    
    # Update: Mettre à jour un kiné par son ID
    async def update(self, id, update_fields):
        """
        Update a patient with the `update_field` object.

        Args:
            id (str): The patient id to be updated.
            update_fields (dict): The patient data to be updated.

        Returns:
            _DocumentType: The patient document updated.
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
        Delete a patients with the `id` object.

        Args:
            id (str): The patient id to be deleted.

        Returns:
            str: The number of deleted patient.
        """
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count  # Nombre de documents supprimés

