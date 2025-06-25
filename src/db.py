import os
import uuid
from typing import List, Dict

from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct, VectorParams, Distance, NamedVector, QueryResponse

VECTOR_SIZE = 1536

class Database:
    _client: QdrantClient

    def __init__(self, host: str, port: int):
        self.__collection_name = 'movies'
        self.__client = QdrantClient(host=host, port=port)

        self._create_collection()

    def _create_collection(self):
        collection_name = self.__collection_name

        if not self.__client.collection_exists(collection_name):
            self.__client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=VECTOR_SIZE,
                    distance=models.Distance.COSINE
                )
            )

    def insert(self, vec: List[float], payload: Dict):
        point_id = str(uuid.uuid4())

        self.__client.upsert(
            collection_name=self.__collection_name,
            points=[
                models.PointStruct(
                    id=point_id,
                    vector=vec,
                    payload=payload
                )
            ]
        )

    def find(self, vector: List[float], limit: int) -> QueryResponse:
         return self.__client.query_points(
            collection_name=self.__collection_name,
            query=vector,
            limit=limit,
            score_threshold=0.7
        )
