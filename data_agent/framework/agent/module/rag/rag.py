from abc import ABC, abstractmethod

from data_agent.framework.agent.context import Context
from data_agent.framework.agent.module.loader import Loader
from data_agent.framework.agent.module.rag import RagKey
from data_agent.framework.agent.module.rag.embedding.embedding_model import (
    EmbeddingModel,
)
from data_agent.framework.agent.module.rag.schema_linking.schema_linking import (
    SchemaLinking,
)


class Rag(Loader, ABC):
    def __init__(self, context: Context):
        super().__init__(context)
        super().load(RagKey.EMBEDDING, self.init_embedding())
        super().load(
            RagKey.SCHEMA_LINKING, self.init_schema_linking(), model=self.get_embedding_model()
        )

    @abstractmethod
    def init_embedding(self) -> type[EmbeddingModel]:
        pass

    @abstractmethod
    def init_schema_linking(self) -> type[SchemaLinking]:
        pass

    def get_embedding_model(self) -> EmbeddingModel:
        return super().get_immediate(RagKey.EMBEDDING, EmbeddingModel)

    def get_schema_linking(self) -> SchemaLinking:
        return super().get_immediate(RagKey.SCHEMA_LINKING, SchemaLinking)