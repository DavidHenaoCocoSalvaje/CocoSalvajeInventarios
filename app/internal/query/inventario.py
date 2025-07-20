# app/internal/query/inventario.py
from app.models.inventario import (
    ElementoInventario,
    ElementoCompuestoInventario,
    ElementosPorElementoCompuestoInventario,
    BodegaInventario,
    GrupoInventario,
    PrecioElementoInventario,
    TipoPrecioElementoInventario,
    MovimientoInventario,
    TipoMovimientoInventario,
    EstadoElementoInventario,
)
from app.internal.query.base import BaseQuery


class ElementoInventarioQuery(BaseQuery[ElementoInventario]):
    """Clase de consulta para la entidad ElementoInventario."""

    def __init__(self):
        super().__init__(ElementoInventario)


class ElementoCompuestoInventarioQuery(BaseQuery[ElementoCompuestoInventario]):
    """Clase de consulta para la entidad ElementoCompuestoInventario."""

    def __init__(self):
        super().__init__(ElementoCompuestoInventario)


class ElementosPorElementoCompuestoInventarioQuery(
    BaseQuery[ElementosPorElementoCompuestoInventario]
):
    """Clase de consulta para la entidad ElementosPorElementoCompuestoInventario."""

    def __init__(self):
        super().__init__(ElementosPorElementoCompuestoInventario)


class BodegaInventarioQuery(BaseQuery[BodegaInventario]):
    """Clase de consulta para la entidad BodegaInventario."""

    def __init__(self):
        super().__init__(BodegaInventario)


class GrupoInventarioQuery(BaseQuery[GrupoInventario]):
    """Clase de consulta para la entidad GrupoInventario."""

    def __init__(self):
        super().__init__(GrupoInventario)


class PrecioElementoInventarioQuery(BaseQuery[PrecioElementoInventario]):
    """Clase de consulta para la entidad PrecioElementoInventario."""

    def __init__(self):
        super().__init__(PrecioElementoInventario)


class TipoPrecioElementoInventarioQuery(BaseQuery[TipoPrecioElementoInventario]):
    """Clase de consulta para la entidad TipoPrecioElementoInventario."""

    def __init__(self):
        super().__init__(TipoPrecioElementoInventario)


class MovimientoInventarioQuery(BaseQuery[MovimientoInventario]):
    """Clase de consulta para la entidad MovimientoInventario."""

    def __init__(self):
        super().__init__(MovimientoInventario)


class TipoMovimientoInventarioQuery(BaseQuery[TipoMovimientoInventario]):
    """Clase de consulta para la entidad TipoMovimientoInventario."""

    def __init__(self):
        super().__init__(TipoMovimientoInventario)


class EstadoElementoInventarioQuery(BaseQuery[EstadoElementoInventario]):
    """Clase de consulta para la entidad EstadoElementoInventario."""

    def __init__(self):
        super().__init__(EstadoElementoInventario)


# Opcional: Instancias pre-inicializadas de las clases de consulta,
# siguiendo el patrón de usuario_query en app/internal/query/usuario.py
elemento_inventario_query = ElementoInventarioQuery()
elemento_compuesto_inventario_query = ElementoCompuestoInventarioQuery()
precio_elemento_inventario_query = PrecioElementoInventarioQuery()
tipo_precio_elemento_inventario_query = TipoPrecioElementoInventarioQuery()
movimiento_inventario_query = MovimientoInventarioQuery()
tipo_movimiento_inventario_query = TipoMovimientoInventarioQuery()
estado_elemento_inventario_query = EstadoElementoInventarioQuery()


elemento_inventario_query = ElementoInventarioQuery()
