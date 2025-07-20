# app/models/inventario.py
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, CHAR, SMALLINT, DATE


class BodegaInventario(SQLModel):
    __tablename__ = "bodegas_inventario"  # type: ignore
    id: int = Field(primary_key=True, sa_type=SMALLINT)
    nombre: str = Field(max_length=50)
    ubicacion: str = Field(max_length=150)

    # Relationships
    elementos_inventario: list["ElementoInventario"] = Relationship(
        back_populates="bodega_inventario"
    )
    elementos_compuestos_inventario: list["ElementoCompuestoInventario"] = Relationship(
        back_populates="bodega_inventario"
    )


class GrupoInventario(SQLModel):
    __tablename__ = "grupos_inventario"  # type: ignore
    id: int = Field(primary_key=True, sa_type=SMALLINT)
    nombre: str = Field(max_length=50)

    # Relationships
    elementos_inventario: list["ElementoInventario"] = Relationship(
        back_populates="grupo_inventario"
    )
    elementos_compuestos_inventario: list["ElementoCompuestoInventario"] = Relationship(
        back_populates="grupo_inventario"
    )


class UnidadMedida(SQLModel):
    __tablename__ = "unidades_medida"  # type: ignore
    id: int = Field(sa_type=SMALLINT, primary_key=True)
    nombre: str = Field(max_length=50)
    tipo_unidad_medida: str = Field(max_length=50)

    # Relationships
    elementos_inventario_cantidad: list["ElementoInventario"] = Relationship(
        back_populates="unidad_medida_cantidad"
    )
    elementos_inventario_peso: list["ElementoInventario"] = Relationship(
        back_populates="unidad_medida_peso"
    )
    elementos_inventario_volumen: list["ElementoInventario"] = Relationship(
        back_populates="unidad_medida_volumen"
    )
    elementos_compuestos_inventario_cantidad: list["ElementoCompuestoInventario"] = (
        Relationship(back_populates="unidad_medida_cantidad")
    )
    elementos_compuestos_inventario_peso: list["ElementoCompuestoInventario"] = (
        Relationship(back_populates="unidad_medida_peso")
    )
    elementos_compuestos_inventario_volumen: list["ElementoCompuestoInventario"] = (
        Relationship(back_populates="unidad_medida_volumen")
    )


class EstadoElementoInventario(SQLModel):
    __tablename__ = "estados_elemento_inventario"  # type: ignore
    id: int = Field(sa_type=SMALLINT, primary_key=True)
    nombre: str = Field(max_length=50)

    # Relationships
    elementos_inventario: list["ElementoInventario"] = Relationship(
        back_populates="estado_elemento"
    )
    elementos_compuestos_inventario: list["ElementoCompuestoInventario"] = Relationship(
        back_populates="estado_elemento"
    )


class ElementoInventario(SQLModel):
    __tablename__ = "elementos_inventario"  # type: ignore
    id: int = Field(primary_key=True)
    nombre: str = Field(max_length=120)
    bodega_inventario_id: int | None = Field(foreign_key="bodegas_inventario.id")
    grupo_inventario_id: int | None = Field(sa_type=SMALLINT)
    cantidad: int | None = None
    unidad_medida_cantidad_id: str | None = Field(
        max_length=3, foreign_key="unidades_medida.id", default=None
    )
    peso: int | None = None
    unidad_medida_peso_id: str | None = Field(
        max_length=3, foreign_key="unidades_medida.id", default=None
    )
    volumen: int | None = None
    unidad_medida_volumen_id: str | None = Field(
        max_length=3, foreign_key="unidades_medida.id", default=None
    )
    estado_elemento_id: str = Field(foreign_key="estados_elemento_inventario.id")
    created_at: datetime = Field(default=datetime.now)
    usuario_id: int | None = None

    # Relationships
    precios: list["PrecioElementoInventario"] = Relationship(
        back_populates="elementos_inventario"
    )
    elementos_compuestos_inventario: list["ElementosPorElementoCompuestoInventario"] = (
        Relationship(back_populates="elemento_inventario")
    )
    unidad_medida_cantidad: UnidadMedida = Relationship(
        back_populates="elementos_inventario_cantidad"
    )
    unidad_medida_peso: UnidadMedida = Relationship(
        back_populates="elementos_inventario_peso"
    )
    unidad_medida_volumen: UnidadMedida = Relationship(
        back_populates="elementos_inventario_volumen"
    )
    bodega_inventario: BodegaInventario = Relationship(
        back_populates="elementos_inventario"
    )
    grupo_inventario: GrupoInventario = Relationship(
        back_populates="elementos_inventario"
    )
    estado_elemento: EstadoElementoInventario = Relationship(
        back_populates="elementos_inventario"
    )


class ElementoCompuestoInventario(SQLModel):
    __tablename__ = "elementos_inventario"  # type: ignore
    id: int = Field(primary_key=True)
    nombre: str = Field(max_length=120)
    bodega_inventario_id: int | None = Field(foreign_key="bodegas_inventario.id")
    grupo_inventario_id: int | None = None
    cantidad: int | None = None
    unidad_medida_cantidad_id: str | None = Field(
        max_length=3, foreign_key="unidades_medida.id", default=None
    )
    peso: int | None = None
    unidad_medida_peso_id: str | None = Field(
        max_length=3, foreign_key="unidades_medida.id", default=None
    )
    volumen: int | None = None
    unidad_medida_volumen_id: str | None = Field(
        max_length=3, foreign_key="unidades_medida.id", default=None
    )
    estado_elemento_id: str = Field(sa_type=CHAR)
    created_at: datetime = Field(default=datetime.now)
    usuario_id: int | None = None

    # Relationships
    elementos_inventario: list["ElementosPorElementoCompuestoInventario"] = (
        Relationship(back_populates="elemento_compuesto_inventario")
    )
    precios: list["PrecioElementoInventario"] = Relationship(
        back_populates="elementos_inventario"
    )
    unidad_medida_cantidad: UnidadMedida = Relationship(
        back_populates="elementos_compuestos_inventario_cantidad"
    )
    unidad_medida_peso: UnidadMedida = Relationship(
        back_populates="elementos_compuestos_inventario_peso"
    )
    unidad_medida_volumen: UnidadMedida = Relationship(
        back_populates="elementos_compuestos_inventario_volumen"
    )
    bodega_inventario: BodegaInventario = Relationship(
        back_populates="elementos_compuestos_inventario"
    )
    grupo_inventario: GrupoInventario = Relationship(
        back_populates="elementos_compuestos_inventario"
    )
    estado_elemento: EstadoElementoInventario = Relationship(
        back_populates="elementos_compuestos_inventario"
    )


class ElementosPorElementoCompuestoInventario(SQLModel):
    __tablename__ = "elementos_inventario_por_elemento_compuesto"  # type: ignore
    elemento_compuesto_inventario_id: int = Field(foreign_key="elementos_inventario.id")
    elemento_inventario_id: int = Field(foreign_key="elementos_inventario.id")

    # Relationships
    elemento_inventario: ElementoInventario = Relationship(
        back_populates="elementos_por_elemento_compuesto"
    )
    elemento_compuesto_inventario: ElementoCompuestoInventario = Relationship(
        back_populates="elementos_inventario"
    )


class TipoPrecioElementoInventario(SQLModel):
    __tablename__ = "tipos_precio_elemento_inventario"  # type: ignore
    id: int = Field(sa_type=SMALLINT, primary_key=True)
    nombre: str = Field(max_length=50)

    # Relationships
    precios: list["PrecioElementoInventario"] = Relationship(
        back_populates="tipo_precio"
    )


class PrecioElementoInventario(SQLModel):
    __tablename__ = "precios_elemento_inventario"  # type: ignore
    id: int = Field(primary_key=True)
    elemento_inventario_id: int
    precio: float
    tipo_precio_id: int = Field(foreign_key="tipos_precio_elemento_inventario.id")
    fini: datetime = Field(sa_type=DATE)
    ffin: datetime | None = Field(sa_type=DATE, default=None)

    # Relationships
    elementos_inventario: ElementoCompuestoInventario = Relationship(
        back_populates="precios"
    )
    tipo_precio: TipoPrecioElementoInventario = Relationship(back_populates="precios")


class MovimientoInventario(SQLModel):
    __tablename__ = "movimientos_inventario"  # type: ignore
    id: int = Field(primary_key=True)
    nombre: str = Field(max_length=120)
    cantidad: int
    elemento_inventario_id: int | None = Field(
        foreign_key="elementos_inventario.id", default=None
    )
    elemento_compuesto_inventario_id: int | None = None
    created_at: datetime = Field(default=datetime.now)
    usuario_id: int | None = None


class TipoMovimientoInventario(SQLModel):
    __tablename__ = "tipos_movimiento_inventario"  # type: ignore
    id: int = Field(sa_type=SMALLINT, primary_key=True)
    nombre: str = Field(max_length=50)
