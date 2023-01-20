from sqlalchemy.orm import make_transient

from src.infra.adapter.repository.postgres.entity.base_entity import BaseEntity
from src.infra.adapter.repository.postgres.repository_manager import RepositoryManager


class BaseRepository:
    @staticmethod
    def delete_hard(entity, entity_id: int):
        with RepositoryManager() as repository_manager:
            retrieved_entity = (
                repository_manager.query(entity).filter(entity.id == entity_id).first()
            )

            if retrieved_entity is None:
                return

            repository_manager.delete(retrieved_entity)
            repository_manager.commit()

    @staticmethod
    def rollback_delete(
        entity,
        entity_id: int,
        existing_entity_model,
    ):
        with RepositoryManager() as repository_manager:
            retrieved_entity = (
                repository_manager.query(entity).filter(entity.id == entity_id).first()
            )

            retrieved_entity.deleted = False
            retrieved_entity.updated_at = existing_entity_model.updated_at
            retrieved_entity.updated_by = existing_entity_model.updated_by

            repository_manager.merge(retrieved_entity)
            repository_manager.commit()

    @staticmethod
    def duplicate_single_entity(repository_manager, entity: BaseEntity, user_id: str):
        repository_manager.expunge(entity)
        make_transient(entity)

        entity.id = None
        entity.created_at = None
        entity.updated_at = None
        entity.created_by = user_id
        entity.updated_by = None

        repository_manager.add(entity)
        repository_manager.flush()
