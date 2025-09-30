from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

# ====================================================================
#               ENDERECO (Dado Composto de PESSOA)
# ====================================================================

class EnderecoBase(SQLModel):
    logradouro: str = Field(max_length=255)
    numero: Optional[str] = Field(default=None, max_length=20)
    cep: str = Field(max_length=9)
    bairro: str = Field(max_length=100)
    cidade: str = Field(max_length=100)
    estado: str = Field(max_length=2)
    complemento: Optional[str] = Field(default=None, max_length=255)

class Endereco(EnderecoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Relacionamento de volta para a Pessoa
    pessoa_id: Optional[int] = Field(default=None, foreign_key="pessoa.id")

# ====================================================================
#                           PESSOA (BASE)
# ====================================================================

class PessoaBase(SQLModel):
    nome: str = Field(min_length=2, max_length=120)
    cpf: str = Field(min_length=11, max_length=14, unique=True, index=True)
    telefone: Optional[str] = Field(default=None, max_length=20)

class Pessoa(PessoaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    # Relacionamento 1-1 com Endereço (back_populates opcional)
    endereco: Optional[Endereco] = Relationship()

    # Relação de volta (back_populates) para as Locações como locador e locatário
    locacoes_locador: List["Locacao"] = Relationship(back_populates="locador")
    locacoes_locatario: List["Locacao"] = Relationship(back_populates="locatario")

# ====================================================================
#                             LOCADOR
# ====================================================================

class LocadorBase(PessoaBase): # Herda atributos de PessoaBase
    salario: Optional[float] = Field(default=None, ge=0)

class Locador(LocadorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, foreign_key="pessoa.id")

# ====================================================================
#                            LOCATARIO
# ====================================================================

class LocatarioBase(PessoaBase): # Herda atributos de PessoaBase
    cnh: str = Field(min_length=10, max_length=30, unique=True, index=True)

class Locatario(LocatarioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, foreign_key="pessoa.id")

# ====================================================================
#                              CARRO
# ====================================================================

class CarroBase(SQLModel):
    modelo: str = Field(max_length=150)
    ano: int = Field(ge=1900, le=2100) # Assumindo um range razoável
    placa: str = Field(min_length=7, max_length=10, unique=True, index=True)
    cor: Optional[str] = Field(default=None, max_length=50)

class Carro(CarroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Relação 1-* com Locação
    locacoes: List["Locacao"] = Relationship(back_populates="carro")

# ====================================================================
#                              SEGURO
# ====================================================================

class CategoriaSeguro(str, Enum):
    BASICO = "Básico"
    INTERMEDIARIO = "Intermediário"
    COMPLETO = "Completo"

class SeguroBase(SQLModel):
    nome: str = Field(max_length=100)
    categoria: CategoriaSeguro
    cobertura: Optional[str] = Field(default=None, max_length=500)
    valor: float = Field(ge=0)

class Seguro(SeguroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Relação 1-* com Locação
    locacoes: List["Locacao"] = Relationship(back_populates="seguro")

# ====================================================================
#                             LOCACAO
# ====================================================================

class LocacaoBase(SQLModel):
    data_inicial: datetime = Field()
    data_final: datetime = Field()
    valor_total: Optional[float] = Field(default=None, ge=0)

class Locacao(LocacaoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Chaves Estrangeiras (Foreign Keys)
    carro_id: int = Field(foreign_key="carro.id")
    locador_id: int = Field(foreign_key="locador.id")
    locatario_id: int = Field(foreign_key="locatario.id")
    seguro_id: Optional[int] = Field(default=None, foreign_key="seguro.id")

    # Relacionamentos (Relationships)
    carro: Carro = Relationship(back_populates="locacoes")
    locador: Locador = Relationship(back_populates="locacoes_locador")
    locatario: Locatario = Relationship(back_populates="locacoes_locatario")
    seguro: Optional[Seguro] = Relationship(back_populates="locacoes")
