# app/routers/inventario.py
from typing import TypeVar
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import SQLModel

# Modelos
from app.models.database import AsyncSessionDep


from app.models.inventario import (
    BodegaInventario,
    GrupoInventario,
    UnidadMedida,
    ElementoInventario,
    ElementoCompuestoInventario,
    ElementosPorElementoCompuestoInventario,
    PrecioElementoInventario,
    TipoPrecioElementoInventario,
    MovimientoInventario,
    TipoMovimientoInventario,
    EstadoElementoInventario,
)

# Base de datos (Repositorio)
from app.internal.query.base import BaseQuery
from app.internal.query.inventario import (
    BodegaInventarioQuery,
    GrupoInventarioQuery,
    ElementoInventarioQuery,
    UnidadMedidaQuery,
    ElementoCompuestoInventarioQuery,
    ElementosPorElementoCompuestoInventarioQuery,
    PrecioElementoInventarioQuery,
    TipoPrecioElementoInventarioQuery,
    MovimientoInventarioQuery,
    TipoMovimientoInventarioQuery,
    EstadoElementoInventarioQuery,
)
from .auth import validar_access_token

router = APIRouter(
    prefix="/inventario",
    tags=["Inventario"],
    responses={404: {"description": "No encontrado"}},
    dependencies=[Depends(validar_access_token)],
)

# Define un TypeVar para los modelos de SQLModel
ModelType = TypeVar("ModelType", bound=SQLModel)
QueryType = TypeVar("QueryType", bound=BaseQuery)


def create_crud_routes(
    model: type[ModelType],
    query_class: type[BaseQuery[ModelType]],
    name: str,
    id_type: type = int,  # Tipo de dato para el ID (int o str)
):
    """
    Crea rutas CRUD genéricas para un modelo dado.

    Args:
        model (type[ModelType]): La clase del modelo SQLModel.
        query_class (type[BaseQuery[ModelType]]): La clase de consulta correspondiente al modelo.
        name (str): El nombre singular del recurso (ej. "bodega_inventario").
        id_type (type): El tipo de dato del ID (int o str), por defecto int.
    """

    # POST - Crear un nuevo recurso
    @router.post(
        f"/{name}",
        response_model=model,
        status_code=status.HTTP_201_CREATED,
        response_model_exclude_unset=True,
        response_model_exclude_none=True,
        summary=f"Crear un nuevo {name.replace('_', ' ')}",
        description=f"Crea un nuevo {name.replace('_', ' ')} con los datos proporcionados.",
    )
    async def create_resource(
        resource: model,  # type: ignore
        session: AsyncSessionDep,
    ):
        """Crea un nuevo recurso."""
        query = query_class()  # type: ignore
        await query.create(session, resource)
        return resource

    # GET - Obtener lista de recursos
    @router.get(
        f"/{name}s",  # Plural para la lista (ej. /bodegas_inventario)
        response_model=list[model],
        response_model_exclude_none=True,
        summary=f"Obtener lista de {name.replace('_', ' ')}s",
        description=f"Obtiene una lista paginada de {name.replace('_', ' ')}s.",
    )
    async def get_resources(
        session: AsyncSessionDep,
        skip: int = 0,
        limit: int = 100,
    ):
        """Obtiene una lista de recursos."""
        query = query_class()  # type: ignore
        resources = await query.get_list(session=session, skip=skip, limit=limit)
        return resources

    # GET - Obtener un recurso por ID
    @router.get(
        f"/{name}/{{{name}_id}}",
        response_model=model,
        summary=f"Obtener un {name.replace('_', ' ')} por ID",
        description=f"Obtiene los detalles de un {name.replace('_', ' ')} específico mediante su ID.",
        response_model_exclude_none=True,
    )
    async def get_resource(
        session: AsyncSessionDep,
        resource_id: id_type,  # Usa el tipo de ID dinámicamente # type: ignore
    ):
        """Obtiene un recurso por ID."""
        query = query_class()  # type: ignore
        db_resource = await query.get(session, resource_id)
        if db_resource is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{model.__name__} con ID {resource_id} no encontrado",
            )
        return db_resource

    # PUT - Actualizar un recurso
    @router.put(
        f"/{name}/{{{name}_id}}",
        response_model=model,
        summary=f"Actualizar un {name.replace('_', ' ')}",
    )
    async def update_resource(
        session: AsyncSessionDep,
        resource_id: id_type,  # Usa el tipo de ID dinámicamente # type: ignore
        resource: model,  # type: ignore
    ):
        """Actualiza un recurso."""
        query = query_class()  # type: ignore
        updated_resource = await query.update(session, resource_id, resource)
        if updated_resource is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{model.__name__} no encontrado",
            )
        return updated_resource

    # DELETE - Eliminar un recurso
    @router.delete(
        f"/{name}/{{{name}_id}}",
        response_model=model,
        summary=f"Eliminar un {name.replace('_', ' ')}",
    )
    async def delete_resource(
        session: AsyncSessionDep,
        resource_id: id_type,  # Usa el tipo de ID dinámicamente # type: ignore
    ):
        """Elimina un recurso."""
        query = query_class()  # type: ignore
        deleted_resource = await query.delete(session, resource_id)
        if deleted_resource is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{model.__name__} no encontrado",
            )
        return deleted_resource


# Llamadas a la función genérica para cada modelo de inventario
create_crud_routes(BodegaInventario, BodegaInventarioQuery, "bodega_inventario")
create_crud_routes(GrupoInventario, GrupoInventarioQuery, "grupo_inventario")
create_crud_routes(ElementoInventario, ElementoInventarioQuery, "elemento_inventario")
create_crud_routes(
    ElementoCompuestoInventario,
    ElementoCompuestoInventarioQuery,
    "elemento_compuesto_inventario",
)
create_crud_routes(
    ElementosPorElementoCompuestoInventario,
    ElementosPorElementoCompuestoInventarioQuery,
    "elementos_por_elemento_compuesto_inventario",
)
create_crud_routes(
    PrecioElementoInventario,
    PrecioElementoInventarioQuery,
    "precio_elemento_inventario",
)
create_crud_routes(
    TipoPrecioElementoInventario,
    TipoPrecioElementoInventarioQuery,
    "tipo_precio_elemento_inventario",
)
create_crud_routes(
    MovimientoInventario, MovimientoInventarioQuery, "movimiento_inventario"
)
create_crud_routes(
    TipoMovimientoInventario,
    TipoMovimientoInventarioQuery,
    "tipo_movimiento_inventario",
    id_type=int,
)  # Asegúrate de que el tipo de ID sea correcto
create_crud_routes(
    EstadoElementoInventario,
    EstadoElementoInventarioQuery,
    "estado_elemento_inventario",
)
create_crud_routes(UnidadMedida, UnidadMedidaQuery, "unidad_medida")
