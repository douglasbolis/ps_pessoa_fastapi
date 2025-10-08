from typing import Any, Callable, Generic, Optional, Type, TypeVar
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import SQLModel, Session
from util.database import get_session
from repository.base import Repository
from service.base import Service

ModelT = TypeVar("ModelT", bound=SQLModel)
CreateT = TypeVar("CreateT", bound=SQLModel)
UpdateT = TypeVar("UpdateT", bound=SQLModel)
ReadT   = TypeVar("ReadT", bound=SQLModel)

class Hooks(Generic[ModelT, CreateT, UpdateT]):
    """
    Pontos de extensão opcionais para regras específicas.
    """
    #
    def pre_create(self, payload: CreateT, session: Session) -> None: ...
    def pre_update(self, payload: UpdateT, session: Session, obj: ModelT) -> None: ...
    def pre_delete(self, session: Session, obj: ModelT) -> None: ...
# fim_class

def create_crud_router(
    *,
    model: Type[ModelT],
    create_schema: Type[CreateT],
    update_schema: Type[UpdateT],
    read_schema: Type[ReadT],
    prefix: str,
    tags: list[str],
    hooks: Optional[Hooks[ModelT, CreateT, UpdateT]] = None,
    page_size_limit: int = 200
) -> APIRouter:
    """
    Cria os endpoints(CRUDL): POST /, GET /, GET /{id}, PATCH /{id}, DELETE /{id}
    """
    router = APIRouter(prefix=prefix, tags=tags)

    # Repository instance
    repo: Repository[ModelT, CreateT, UpdateT] = Repository(model)
    # Service instance
    service: Service[ModelT, CreateT, UpdateT] = Service(repo)
    # Hooks instance
    _hooks = hooks or Hooks()

    """
    Endpoint to create a new object
    """
    @router.post("/", response_model=read_schema, status_code=201)
    def create_item(payload: create_schema, session: Session = Depends(get_session)): # type: ignore
        if hasattr(_hooks, "pre_create") and callable(_hooks.pre_create):
            _hooks.pre_create(payload, session)
        # fim_if

        return service.create(session, payload)
    # fim_def

    """
    Endpoint to get all objects
    """
    @router.get("/", response_model=list[read_schema])
    def list_items(session: Session = Depends(get_session), offset: int = 0, limit: int = Query(100, le=page_size_limit)):
        return service.list(session, offset, limit)
    # fim_def

    """
    Endpoint to get a specific object
    """
    @router.get("/{item_id}", response_model=read_schema)
    def get_item(item_id: int, session: Session = Depends(get_session)):
        obj = service.get(session, item_id)

        if not obj:
            raise HTTPException(404, "Not found")
        # fim_if

        return obj
    # fim_def

    """
    Endpoint to update a specific object
    """
    @router.patch("/{item_id}", response_model=read_schema)
    def update_item(item_id: int, payload: update_schema, session: Session = Depends(get_session)): # type: ignore
        obj = service.get(session, item_id)

        if not obj:
            raise HTTPException(404, "Not found")
        # fim_if

        if hasattr(_hooks, "pre_update") and callable(_hooks.pre_update):
            _hooks.pre_update(payload, session, obj)
        # fim_if

        try:
            return service.update(session, item_id, payload)
        except ValueError:
            raise HTTPException(404, "Not found")
        # fim_try
    # fim_def

    """
    Endpoint to delete a specific object
    """
    @router.delete("/{item_id}", status_code=204)
    def delete_item(item_id: int, session: Session = Depends(get_session)):
        obj = service.get(session, item_id)

        if not obj:
            raise HTTPException(404, "Not found")
        # fim_if

        if hasattr(_hooks, "pre_delete") and callable(_hooks.pre_delete):
            _hooks.pre_delete(session, obj)
        # fim_if

        try:
            service.delete(session, item_id)
        except ValueError:
            raise HTTPException(404, "Not found")
        # fim_try
    # fim_def

    return router
# fim_def
