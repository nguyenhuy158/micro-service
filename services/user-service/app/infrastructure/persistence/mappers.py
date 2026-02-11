from app.domain.entities.user import UserEntity
from app.infrastructure.persistence.models.user import User


def orm_to_entity(user: User) -> UserEntity:
    return UserEntity.model_validate(user)


def entity_to_dict(entity: UserEntity) -> dict:
    return entity.model_dump(exclude_none=True)
