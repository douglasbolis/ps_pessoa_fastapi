from fastapi import HTTPException
from sqlmodel import Session
from controller.generic import create_crud_router, Hooks
from model.models import Endereco, Pessoa
from model.dto import EnderecoCreate, EnderecoUpdate, EnderecoRead

class EnderecoHooks(Hooks[Endereco, EnderecoCreate, EnderecoUpdate]):
    def pre_create(self, payload: EnderecoCreate, session: Session) -> None:
        pessoa_id = getattr(payload, "pessoa_id", None)

        if pessoa_id is None or pessoa_id <= 0 or not session.get(Pessoa, pessoa_id):
            raise HTTPException(400, "pessoa_id inválido")
        # fim_if
    # fim_pre_create

router = create_crud_router(
    model=Endereco,
    create_schema=EnderecoCreate,
    update_schema=EnderecoUpdate,
    read_schema=EnderecoRead,
    prefix="/enderecos",
    tags=["enderecos"],
    hooks=EnderecoHooks(),
)