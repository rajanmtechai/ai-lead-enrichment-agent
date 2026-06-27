from hashlib import sha256

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

from app.core.config import settings


class EmbeddingService:
    collection_name = "company_profiles"

    def __init__(self) -> None:
        self.client = QdrantClient(url=settings.qdrant_url)

    def vectorize(self, text: str) -> list[float]:
        digest = sha256(text.encode()).digest()
        return [round(byte / 255, 6) for byte in digest[:8]]

    def ensure_collection(self) -> None:
        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            try:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=qmodels.VectorParams(size=8, distance=qmodels.Distance.COSINE),
                )
            except Exception:
                return

    def upsert_company(self, company_id: int, content: str) -> str:
        try:
            self.ensure_collection()
            vector = self.vectorize(content)
            point_id = str(company_id)
            self.client.upsert(
                collection_name=self.collection_name,
                points=[qmodels.PointStruct(id=point_id, vector=vector, payload={"company_id": company_id, "content": content})],
            )
            return point_id
        except Exception:
            return f"fallback-{company_id}"