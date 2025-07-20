# app/models/usuario.py
from sqlmodel import Field, Relationship, SQLModel


class UsuarioBase(SQLModel):
    username: str = Field(max_length=50, unique=True)
    contacto_id: int | None = None


class UsuarioCreate(UsuarioBase):
    password: str = Field(min_length=8, max_length=120)


# Solo el modelo de tabla
class UsuarioDB(UsuarioCreate, table=True):
    __tablename__ = "usuarios"  # type: ignore
    id: int = Field(primary_key=True)

    # Relationships
    # Un usuario puede tener múltiples elementos de inventario creados
    elementos_inventario: list["ElementoInventario"] = Relationship(  # type: ignore  # noqa: F821
        back_populates="usuario"
    )
    # Un usuario puede tener múltiples elementos compuestos de inventario creados
    elementos_compuestos_inventario: list["ElementoCompuestoInventario"] = Relationship(  # type: ignore  # noqa: F821
        back_populates="usuario"
    )
    # Un usuario puede realizar múltiples movimientos de inventario
    movimientos_inventario: list["MovimientoInventario"] = Relationship(  # type: ignore  # noqa: F821
        back_populates="usuario"
    )

    # back_populates indica que si algo cambia en este modelo, debe cambiar en el otro también.
    # https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/create-and-update-relationships/#create-a-team-with-heroes


# https://fastapi.tiangolo.com/es/tutorial/sql-databases/?h=sqlmodel#crear-multiples-modelos
