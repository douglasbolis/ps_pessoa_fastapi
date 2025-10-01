from app.controller.generic import create_crud_router
from app.model.models import Locador 
from app.model.dto import LocadorCreate, LocadorUpdate, LocadorRead

router = create_crud_router(
    model=Locador,
    create_schema=LocadorCreate,
    update_schema=LocadorUpdate,
    read_schema=LocadorRead,
    prefix="/locadores",
    tags=["locadores"],
)
