# app/models/usuario.py
from sqlmodel import Field, SQLModel


# Solo el modelo de tabla
class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"  # type: ignore

    id: int = Field(primary_key=True)
    primer_nombre: str = Field(max_length=25)
    # Usar default=None para atributos opcionales
    segundo_nombre: str | None = None
    primer_apellido: str = Field(max_length=25)
    segundo_apellido: str | None = None
    sexo: str = Field(include=["F", "M"], default=None)