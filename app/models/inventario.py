# app/models/usuario.py
from datetime import datetime
from sqlmodel import Field, SQLModel, CHAR, SMALLINT


class ElementoInventario(SQLModel):
    __tablename__ = "elementos_inventario"  # type: ignore
    id: int = Field(primary_key=True)
    nombre: str = Field(max_length=120)
    cantidad: int
    estado_elemento_id: str = Field(sa_type=CHAR)
    created_at: datetime = Field(default_factory=datetime.now)
    usuario_id: int | None = None


class ElementoCompuestoInventario(SQLModel):
    __tablename__ = "elementos_compuestos_inventario"  # type: ignore
    id: int = Field(primary_key=True)
    nombre: str = Field(max_length=120)
    cantidad: int
    estado_elemento_id: str = Field(sa_type=CHAR)
    created_at: datetime = Field(default_factory=datetime.now)
    usuario_id: int | None = None


class ElementosPorElementoCompuestoInventario(SQLModel):
    __tablename__ = "elementos_inventario_por_elemento_compuesto"  # type: ignore
    elemento_compuesto_inventario_id: int
    elemento_inventario_id: int


class PrecioElementoInventario(SQLModel):
    __tablename__ = "precios_elemento_inventario"  # type: ignore
    id: int = Field(primary_key=True)
    elemento_inventario_id: int
    precio: float


class TipoPrecioElementoInventario(SQLModel):
    __tablename__ = "tipos_precio_elemento_inventario"  # type: ignore
    id: int = Field(sa_type=SMALLINT, primary_key=True)
    nombre: str = Field(max_length=50)


class MovimientoInventario(SQLModel):
    __tablename__ = "movimientos_inventario"  # type: ignore
    id: int = Field(primary_key=True)
    nombre: str = Field(max_length=120)
    cantidad: int
    created_at: datetime = Field(default_factory=datetime.now)
    usuario_id: int | None = None


class TipoMovimientoInventario(SQLModel):
    __tablename__ = "tipos_movimiento_inventario"  # type: ignore
    id: str = Field(sa_type=CHAR, primary_key=True)
    nombre: str = Field(max_length=50)


class EstadoElementoInventario(SQLModel):
    __tablename__ = "estados_elemento_inventario"  # type: ignore
    id: int = Field(primary_key=True)
    nombre: str = Field(max_length=50)
