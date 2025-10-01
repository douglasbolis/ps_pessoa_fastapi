from typing import Optional, List
from datetime import datetime
from sqlmodel import Field
from app.model.models import PessoaBase, LocadorBase, LocatarioBase, EnderecoBase, CarroBase, SeguroBase, LocacaoBase

# ====================================================================
#                           ENDERECO
# ====================================================================

class EnderecoCreate(EnderecoBase):
    pass

class EnderecoPublic(EnderecoBase):
    id: int
    pessoa_id: Optional[int] = None
    model_config = {"from_attributes": True}

# ====================================================================
#                          PESSOA
# ====================================================================

class PessoaRead(PessoaBase):
    id: int
    model_config = {"from_attributes": True}

# ====================================================================
#                          LOCADOR
# ====================================================================

class LocadorRead(LocadorBase):
    id: int

class LocadorCreate(LocadorBase):
    endereco: Optional[EnderecoCreate] = None

class LocadorPublic(LocadorBase):
    id: int
    endereco: Optional[EnderecoPublic] = None
    model_config = {"from_attributes": True}

class LocadorUpdate(LocadorBase):
    nome: Optional[str] = Field(default=None)
    cpf: Optional[str] = Field(default=None)
    telefone: Optional[str] = Field(default=None)
    salario: Optional[float] = Field(default=None, ge=0)
    endereco: Optional[EnderecoCreate] = None

# ====================================================================
#                          LOCATARIO
# ====================================================================

class LocatarioCreate(LocatarioBase):
    endereco: Optional[EnderecoCreate] = None

class LocatarioPublic(LocatarioBase):
    id: int
    endereco: Optional[EnderecoPublic] = None
    model_config = {"from_attributes": True}

class LocatarioUpdate(LocatarioBase):
    nome: Optional[str] = Field(default=None)
    cpf: Optional[str] = Field(default=None)
    telefone: Optional[str] = Field(default=None)
    cnh: Optional[str] = Field(default=None)
    endereco: Optional[EnderecoCreate] = None

# ====================================================================
#                            CARRO
# ====================================================================

class CarroCreate(CarroBase):
    pass

class CarroPublic(CarroBase):
    id: int
    model_config = {"from_attributes": True}

class CarroUpdate(CarroBase):
    modelo: Optional[str] = Field(default=None)
    ano: Optional[int] = Field(default=None)
    placa: Optional[str] = Field(default=None)
    cor: Optional[str] = Field(default=None)

# ====================================================================
#                            SEGURO
# ====================================================================

class SeguroCreate(SeguroBase):
    pass

class SeguroPublic(SeguroBase):
    id: int
    model_config = {"from_attributes": True}

class SeguroUpdate(SeguroBase):
    nome: Optional[str] = Field(default=None)
    categoria: Optional[str] = Field(default=None)
    cobertura: Optional[str] = Field(default=None)
    valor: Optional[float] = Field(default=None, ge=0)

# ====================================================================
#                            LOCACAO
# ====================================================================

class LocacaoCreate(LocacaoBase):
    carro_id: int
    locador_id: int
    locatario_id: int
    seguro_id: Optional[int] = None

class LocacaoPublic(LocacaoBase):
    id: int
    carro_id: int
    locador_id: int
    locatario_id: int
    seguro_id: Optional[int] = None
    model_config = {"from_attributes": True}

class LocacaoUpdate(LocacaoBase):
    data_inicial: Optional[datetime] = Field(default=None)
    data_final: Optional[datetime] = Field(default=None)
    valor_total: Optional[float] = Field(default=None, ge=0)
    carro_id: Optional[int] = Field(default=None)
    locador_id: Optional[int] = Field(default=None)
    locatario_id: Optional[int] = Field(default=None)
    seguro_id: Optional[int] = Field(default=None)

# Locação com Relacionamentos
class LocacaoReadWithDetails(LocacaoPublic):
    carro: CarroPublic
    locador: LocadorPublic
    locatario: LocatarioPublic
    seguro: Optional[SeguroPublic] = None
    model_config = {"from_attributes": True}
