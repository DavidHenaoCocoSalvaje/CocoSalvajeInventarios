# app/internal/query/inventario.py
import app.models.inventario as inv
from app.internal.query.base import BaseQuery


class ElementoInventarioQuery(BaseQuery[inv.ElementoInventario]):
    """Repositorio para la entidad Usuario"""

    def __init__(self):
        super().__init__(inv.ElementoInventario)


elemento_inventario_query = ElementoInventarioQuery()
