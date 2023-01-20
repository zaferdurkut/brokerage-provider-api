from typing import List, Any

from src.infra.adapter.repository.postgres.repository_config import Base


def convert_sqlalchemy_model_to_dict(model: Base, excluded_columns: List[str] = []):
    generated_dict = {}
    for column in model.__table__.columns:
        if column.name not in excluded_columns:
            generated_dict[column.name] = getattr(model, column.name)

    return generated_dict
