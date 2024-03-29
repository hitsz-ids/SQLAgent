from bson.objectid import ObjectId

from sql_agent.db.repositories.types import KnowledgeEmbeddingRecord

SYNC_EMBEDDING_COLLECTION = "sync_knowledge"


class KnowledgeSyncRepository:
    def __init__(self, storage):
        self.storage = storage

    def insert(self, embedding_record: KnowledgeEmbeddingRecord) -> KnowledgeEmbeddingRecord:
        embedding_record_dict = embedding_record.dict(exclude={"id"})
        embedding_record.id = str(
            self.storage.insert_one(SYNC_EMBEDDING_COLLECTION, embedding_record_dict)
        )
        return embedding_record

    def find_one(self, query: dict) -> KnowledgeEmbeddingRecord | None:
        row = self.storage.find_one(SYNC_EMBEDDING_COLLECTION, query)
        if not row:
            return None
        row["id"] = str(row["_id"])
        return KnowledgeEmbeddingRecord(**row)

    def find_by_id(self, id: str) -> KnowledgeEmbeddingRecord | None:
        row = self.storage.find_one(SYNC_EMBEDDING_COLLECTION, {"_id": ObjectId(id)})
        if not row:
            return None
        row["id"] = str(row["_id"])
        return KnowledgeEmbeddingRecord(**row)

    def update(self, embedding_record: KnowledgeEmbeddingRecord) -> KnowledgeEmbeddingRecord:
        embedding_record_dict = embedding_record.dict(exclude={"id"})
        self.storage.update_or_create(
            SYNC_EMBEDDING_COLLECTION,
            {"_id": ObjectId(embedding_record.id)},
            embedding_record_dict,
        )
        return embedding_record
