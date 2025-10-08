from typing import Generic, Type, TypeVar, Optional, List, Any
from sqlmodel import SQLModel, Session, select

ModelT = TypeVar("ModelT", bound=SQLModel)
CreateT = TypeVar("CreateT", bound=SQLModel)
UpdateT = TypeVar("UpdateT", bound=SQLModel)

class Repository(Generic[ModelT, CreateT, UpdateT]):
    def __init__(self, model: Type[ModelT]):
        self.model = model
    # fim_def

    def get(self, session: Session, id: Any) -> Optional[ModelT]:
        return session.get(self.model, id)
    # fim_def

    def list(self, session: Session, offset: int = 0, limit: int = 100) -> List[ModelT]:
        stmt = select(self.model).offset(offset).limit(limit)

        return list(session.exec(stmt))
    # fim_def

    def create(self, session: Session, data: CreateT) -> ModelT:
        obj = self.model.model_validate(data)

        session.add(obj)
        session.commit()
        session.refresh(obj)

        return obj
    # fim_def

    def update(self, session: Session, obj: ModelT, data: UpdateT) -> ModelT:
        data_dict = data.model_dump(exclude_unset=True)

        for k, v in data_dict.items():
            setattr(obj, k, v)
        # fim_for

        session.add(obj)
        session.commit()
        session.refresh(obj)

        return obj
    # fim_def

    def delete(self, session: Session, obj: ModelT) -> None:
        session.delete(obj)
        session.commit()
    # fim_def
# fim_class
