# app/models/inventario.py
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, SMALLINT, DATE


class BodegaInventario(SQLModel, table=True):
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


class GrupoInventario(SQLModel, table=True):
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


class UnidadMedida(SQLModel, table=True):
    __tablename__ = "unidades_medida"  # type: ignore
    # Cambiado a str para coincidir con las FKs que usan max_length=3
    id: str = Field(primary_key=True, max_length=3)
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


class EstadoElementoInventario(SQLModel, table=True):
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


class ElementoInventario(SQLModel, table=True):
    __tablename__ = "elementos_inventario"  # type: ignore
    id: int = Field(primary_key=True)
    nombre: str = Field(max_length=120)
    bodega_inventario_id: int | None = Field(foreign_key="bodegas_inventario.id")
    # Añadida clave foránea
    grupo_inventario_id: int | None = Field(foreign_key="grupos_inventario.id")
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
    # Corregido tipo a int y añadida clave foránea
    estado_elemento_id: int = Field(foreign_key="estados_elemento_inventario.id")
    created_at: datetime = Field(default=datetime.now)
    # Añadida clave foránea
    usuario_id: int | None = Field(foreign_key="usuarios.id", default=None)

    # Relationships
    precios: list["PrecioElementoInventario"] = Relationship(
        back_populates="elemento_inventario"
    )
    elementos_compuestos_inventario: list["ElementosPorElementoCompuestoInventario"] = (
        Relationship(back_populates="elemento_inventario")
    )
    unidad_medida_cantidad: "UnidadMedida" = Relationship(  # Usar cadena
        back_populates="elementos_inventario_cantidad"
    )
    unidad_medida_peso: "UnidadMedida" = Relationship(  # Usar cadena
        back_populates="elementos_inventario_peso"
    )
    unidad_medida_volumen: "UnidadMedida" = Relationship(  # Usar cadena
        back_populates="elementos_inventario_volumen"
    )
    bodega_inventario: "BodegaInventario" = Relationship(  # Usar cadena
        back_populates="elementos_inventario"
    )
    grupo_inventario: "GrupoInventario" = Relationship(  # Usar cadena
        back_populates="elementos_inventario"
    )
    estado_elemento: "EstadoElementoInventario" = Relationship(  # Usar cadena
        back_populates="elementos_inventario"
    )
    # Relación con UsuarioDB
    usuario: "UsuarioDB" = Relationship(back_populates="elementos_inventario")  # type: ignore # noqa: F821
    # Relación con MovimientoInventario
    movimientos_inventario: list["MovimientoInventario"] = Relationship(
        back_populates="elemento_inventario"
    )


class ElementoCompuestoInventario(SQLModel, table=True):
    # Nombre de tabla corregido para evitar conflictos
    __tablename__ = "elementos_compuestos_inventario"  # type: ignore
    id: int = Field(primary_key=True)
    nombre: str = Field(max_length=120)
    bodega_inventario_id: int | None = Field(foreign_key="bodegas_inventario.id")
    # Añadida clave foránea
    grupo_inventario_id: int | None = Field(
        foreign_key="grupos_inventario.id", default=None
    )
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
    # Corregido tipo a int y añadida clave foránea
    estado_elemento_id: int = Field(foreign_key="estados_elemento_inventario.id")
    created_at: datetime = Field(default=datetime.now)
    # Añadida clave foránea
    usuario_id: int | None = Field(foreign_key="usuarios.id", default=None)

    # Relationships
    elementos_inventario: list["ElementosPorElementoCompuestoInventario"] = (
        Relationship(back_populates="elemento_compuesto_inventario")
    )
    # Eliminada relación 'precios' que no corresponde a este modelo
    unidad_medida_cantidad: "UnidadMedida" = Relationship(  # Usar cadena
        back_populates="elementos_compuestos_inventario_cantidad"
    )
    unidad_medida_peso: "UnidadMedida" = Relationship(  # Usar cadena
        back_populates="elementos_compuestos_inventario_peso"
    )
    unidad_medida_volumen: "UnidadMedida" = Relationship(  # Usar cadena
        back_populates="elementos_compuestos_inventario_volumen"
    )
    bodega_inventario: "BodegaInventario" = Relationship(  # Usar cadena
        back_populates="elementos_compuestos_inventario"
    )
    grupo_inventario: "GrupoInventario" = Relationship(  # Usar cadena
        back_populates="elementos_compuestos_inventario"
    )
    estado_elemento: "EstadoElementoInventario" = Relationship(  # Usar cadena
        back_populates="elementos_compuestos_inventario"
    )
    # Relación con UsuarioDB
    usuario: "UsuarioDB" = Relationship(  # type: ignore  # noqa: F821
        back_populates="elementos_compuestos_inventario"
    )
    # Relación con MovimientoInventario
    movimientos_inventario: list["MovimientoInventario"] = Relationship(
        back_populates="elemento_compuesto_inventario"
    )


class ElementosPorElementoCompuestoInventario(SQLModel, table=True):
    __tablename__ = "elementos_inventario_por_elemento_compuesto"  # type: ignore
    # Añadidos primary_key para la tabla de enlace
    elemento_compuesto_inventario_id: int = Field(
        foreign_key="elementos_compuestos_inventario.id", primary_key=True
    )
    elemento_inventario_id: int = Field(
        foreign_key="elementos_inventario.id", primary_key=True
    )

    # Relationships
    elemento_inventario: "ElementoInventario" = Relationship(  # Usar cadena
        back_populates="elementos_compuestos_inventario"
    )
    elemento_compuesto_inventario: "ElementoCompuestoInventario" = (
        Relationship(  # Usar cadena
            back_populates="elementos_inventario"
        )
    )


class TipoPrecioElementoInventario(SQLModel, table=True):
    __tablename__ = "tipos_precio_elemento_inventario"  # type: ignore
    id: int = Field(sa_type=SMALLINT, primary_key=True)
    nombre: str = Field(max_length=50)

    # Relationships
    precios: list["PrecioElementoInventario"] = Relationship(
        back_populates="tipo_precio"
    )


class PrecioElementoInventario(SQLModel, table=True):
    __tablename__ = "precios_elemento_inventario"  # type: ignore
    id: int = Field(primary_key=True)
    # Añadida clave foránea
    elemento_inventario_id: int = Field(foreign_key="elementos_inventario.id")
    precio: float
    tipo_precio_id: int = Field(foreign_key="tipos_precio_elemento_inventario.id")
    fini: datetime = Field(sa_type=DATE)
    ffin: datetime | None = Field(sa_type=DATE, default=None)

    # Relationships
    # Corregida la relación para que apunte a ElementoInventario
    elemento_inventario: "ElementoInventario" = Relationship(back_populates="precios")
    tipo_precio: "TipoPrecioElementoInventario" = Relationship(back_populates="precios")


class MovimientoInventario(SQLModel, table=True):
    __tablename__ = "movimientos_inventario"  # type: ignore
    id: int = Field(primary_key=True)
    nombre: str = Field(max_length=120)
    cantidad: int
    elemento_inventario_id: int | None = Field(
        foreign_key="elementos_inventario.id", default=None
    )
    # Añadida clave foránea
    elemento_compuesto_inventario_id: int | None = Field(
        foreign_key="elementos_compuestos_inventario.id", default=None
    )
    # Añadido campo y clave foránea para el tipo de movimiento
    tipo_movimiento_id: int = Field(foreign_key="tipos_movimiento_inventario.id")
    created_at: datetime = Field(default=datetime.now)
    # Añadida clave foránea
    usuario_id: int | None = Field(foreign_key="usuarios.id", default=None)

    # Relationships
    elemento_inventario: "ElementoInventario" = Relationship(  # Usar cadena
        back_populates="movimientos_inventario"
    )
    elemento_compuesto_inventario: "ElementoCompuestoInventario" = (
        Relationship(  # Usar cadena
            back_populates="movimientos_inventario"
        )
    )
    tipo_movimiento: "TipoMovimientoInventario" = Relationship(  # Usar cadena
        back_populates="movimientos_inventario"
    )
    usuario: "UsuarioDB" = Relationship(back_populates="movimientos_inventario")  # type: ignore  # noqa: F821


class TipoMovimientoInventario(SQLModel, table=True):
    __tablename__ = "tipos_movimiento_inventario"  # type: ignore
    id: int = Field(sa_type=SMALLINT, primary_key=True)
    nombre: str = Field(max_length=50)

    # Relationships
    movimientos_inventario: list["MovimientoInventario"] = Relationship(
        back_populates="tipo_movimiento"
    )
