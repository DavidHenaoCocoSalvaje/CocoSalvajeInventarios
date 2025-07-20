# app/routers/inventario.py

from fastapi import APIRouter, HTTPException, status

# Modelos
from app.models.database import AsyncSessionDep
from app.models.inventario import (
    ElementoInventario,
    ElementoCompuestoInventario,
    PrecioElementoInventario,
    TipoPrecioElementoInventario,
    MovimientoInventario,
    TipoMovimientoInventario,
    EstadoElementoInventario,
)

# Base de datos (Repositorio)
from app.internal.query.inventario import (
    ElementoInventarioQuery,
    ElementoCompuestoInventarioQuery,
    PrecioElementoInventarioQuery,
    TipoPrecioElementoInventarioQuery,
    MovimientoInventarioQuery,
    TipoMovimientoInventarioQuery,
    EstadoElementoInventarioQuery,
)

router = APIRouter(
    prefix="/inventario",
    tags=["Inventario"],
    responses={404: {"description": "No encontrado"}},
)

router.post(
    "/elemento_inventario",
    response_model=ElementoInventario,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
    summary="Crear un nuevo elemento de inventario",
    description="Crea un nuevo elemento de inventario con los datos proporcionados.",
)


async def crear_elemento_inventario(
    elemento: ElementoInventario,
    session: AsyncSessionDep,
):
    """Crea un nuevo elemento de inventario."""
    query = ElementoInventarioQuery()
    await query.create(session, elemento)
    return elemento


@router.get(
    "/elementos_inventario",
    response_model=list[ElementoInventario],
    response_model_exclude_none=True,
    summary="Obtener lista de elementos de inventario",
    description="Obtiene una lista paginada de elementos de inventario.",
)
async def get_elementos_inventario(
    session: AsyncSessionDep,
    skip: int = 0,
    limit: int = 100,
):
    """Obtiene una lista de elementos de inventario."""
    query = ElementoInventarioQuery()
    elementos = await query.get_list(session=session, skip=skip, limit=limit)
    return elementos


@router.get(
    "/elemento_inventario/{elemento_id}",
    response_model=ElementoInventario,
    summary="Obtener un elemento de inventario por ID",
    description="Obtiene los detalles de un elemento de inventario específico mediante su ID.",
    response_model_exclude_none=True,
)
async def get_elemento_inventario(
    session: AsyncSessionDep,
    elemento_id: int,
):
    """Obtiene un elemento de inventario por ID."""
    query = ElementoInventarioQuery()
    db_elemento = await query.get(session, elemento_id)
    if db_elemento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ElementoInventario con ID {elemento_id} no encontrado",
        )
    return db_elemento


@router.put(
    "/elemento_inventario/{elemento_id}",
    response_model=ElementoInventario,
    summary="Actualizar un elemento de inventario",
)
async def actualizar_elemento_inventario(
    session: AsyncSessionDep,
    elemento_id: int,
    elemento: ElementoInventario,
):
    """Actualiza un elemento de inventario."""
    query = ElementoInventarioQuery()
    elemento_actualizado = await query.update(session, elemento_id, elemento)
    if elemento_actualizado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ElementoInventario no encontrado",
        )
    return elemento_actualizado


@router.delete(
    "/elemento_inventario/{elemento_id}",
    response_model=ElementoInventario,
    summary="Eliminar un elemento de inventario",
)
async def eliminar_elemento_inventario(
    session: AsyncSessionDep,
    elemento_id: int,
):
    """Elimina un elemento de inventario."""
    query = ElementoInventarioQuery()
    elemento_eliminado = await query.delete(session, elemento_id)
    if elemento_eliminado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ElementoInventario no encontrado",
        )
    return elemento_eliminado


@router.post(
    "/elemento_compuesto_inventario",
    response_model=ElementoCompuestoInventario,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
    summary="Crear un nuevo elemento compuesto de inventario",
    description="Crea un nuevo elemento compuesto de inventario con los datos proporcionados.",
)
async def crear_elemento_compuesto_inventario(
    elemento_compuesto: ElementoCompuestoInventario,
    session: AsyncSessionDep,
):
    """Crea un nuevo elemento compuesto de inventario."""
    query = ElementoCompuestoInventarioQuery()
    await query.create(session, elemento_compuesto)
    return elemento_compuesto


@router.get(
    "/elementos_compuestos_inventario",
    response_model=list[ElementoCompuestoInventario],
    response_model_exclude_none=True,
    summary="Obtener lista de elementos compuestos de inventario",
    description="Obtiene una lista paginada de elementos compuestos de inventario.",
)
async def get_elementos_compuestos_inventario(
    session: AsyncSessionDep,
    skip: int = 0,
    limit: int = 100,
):
    """Obtiene una lista de elementos compuestos de inventario."""
    query = ElementoCompuestoInventarioQuery()
    elementos_compuestos = await query.get_list(session=session, skip=skip, limit=limit)
    return elementos_compuestos


@router.get(
    "/elemento_compuesto_inventario/{elemento_compuesto_id}",
    response_model=ElementoCompuestoInventario,
    summary="Obtener un elemento compuesto de inventario por ID",
    description="Obtiene los detalles de un elemento compuesto de inventario específico mediante su ID.",
    response_model_exclude_none=True,
)
async def get_elemento_compuesto_inventario(
    session: AsyncSessionDep,
    elemento_compuesto_id: int,
):
    """Obtiene un elemento compuesto de inventario por ID."""
    query = ElementoCompuestoInventarioQuery()
    db_elemento_compuesto = await query.get(session, elemento_compuesto_id)
    if db_elemento_compuesto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ElementoCompuestoInventario con ID {elemento_compuesto_id} no encontrado",
        )
    return db_elemento_compuesto


@router.put(
    "/elemento_compuesto_inventario/{elemento_compuesto_id}",
    response_model=ElementoCompuestoInventario,
    summary="Actualizar un elemento compuesto de inventario",
)
async def actualizar_elemento_compuesto_inventario(
    session: AsyncSessionDep,
    elemento_compuesto_id: int,
    elemento_compuesto: ElementoCompuestoInventario,
):
    """Actualiza un elemento compuesto de inventario."""
    query = ElementoCompuestoInventarioQuery()
    elemento_compuesto_actualizado = await query.update(
        session, elemento_compuesto_id, elemento_compuesto
    )
    if elemento_compuesto_actualizado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ElementoCompuestoInventario no encontrado",
        )
    return elemento_compuesto_actualizado


@router.delete(
    "/elemento_compuesto_inventario/{elemento_compuesto_id}",
    response_model=ElementoCompuestoInventario,
    summary="Eliminar un elemento compuesto de inventario",
)
async def eliminar_elemento_compuesto_inventario(
    session: AsyncSessionDep,
    elemento_compuesto_id: int,
):
    """Elimina un elemento compuesto de inventario."""
    query = ElementoCompuestoInventarioQuery()
    elemento_compuesto_eliminado = await query.delete(session, elemento_compuesto_id)
    if elemento_compuesto_eliminado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ElementoCompuestoInventario no encontrado",
        )
    return elemento_compuesto_eliminado


@router.post(
    "/precio_elemento_inventario",
    response_model=PrecioElementoInventario,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
    summary="Crear un nuevo precio de elemento de inventario",
    description="Crea un nuevo precio de elemento de inventario con los datos proporcionados.",
)
async def crear_precio_elemento_inventario(
    precio_elemento: PrecioElementoInventario,
    session: AsyncSessionDep,
):
    """Crea un nuevo precio de elemento de inventario."""
    query = PrecioElementoInventarioQuery()
    await query.create(session, precio_elemento)
    return precio_elemento


@router.get(
    "/precios_elementos_inventario",
    response_model=list[PrecioElementoInventario],
    response_model_exclude_none=True,
    summary="Obtener lista de precios de elementos de inventario",
    description="Obtiene una lista paginada de precios de elementos de inventario.",
)
async def get_precios_elementos_inventario(
    session: AsyncSessionDep,
    skip: int = 0,
    limit: int = 100,
):
    """Obtiene una lista de precios de elementos de inventario."""
    query = PrecioElementoInventarioQuery()
    precios_elementos = await query.get_list(session=session, skip=skip, limit=limit)
    return precios_elementos


@router.get(
    "/precio_elemento_inventario/{precio_elemento_id}",
    response_model=PrecioElementoInventario,
    summary="Obtener un precio de elemento de inventario por ID",
    description="Obtiene los detalles de un precio de elemento de inventario específico mediante su ID.",
    response_model_exclude_none=True,
)
async def get_precio_elemento_inventario(
    session: AsyncSessionDep,
    precio_elemento_id: int,
):
    """Obtiene un precio de elemento de inventario por ID."""
    query = PrecioElementoInventarioQuery()
    db_precio_elemento = await query.get(session, precio_elemento_id)
    if db_precio_elemento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"PrecioElementoInventario con ID {precio_elemento_id} no encontrado",
        )
    return db_precio_elemento


@router.put(
    "/precio_elemento_inventario/{precio_elemento_id}",
    response_model=PrecioElementoInventario,
    summary="Actualizar un precio de elemento de inventario",
)
async def actualizar_precio_elemento_inventario(
    session: AsyncSessionDep,
    precio_elemento_id: int,
    precio_elemento: PrecioElementoInventario,
):
    """Actualiza un precio de elemento de inventario."""
    query = PrecioElementoInventarioQuery()
    precio_elemento_actualizado = await query.update(
        session, precio_elemento_id, precio_elemento
    )
    if precio_elemento_actualizado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PrecioElementoInventario no encontrado",
        )
    return precio_elemento_actualizado


@router.delete(
    "/precio_elemento_inventario/{precio_elemento_id}",
    response_model=PrecioElementoInventario,
    summary="Eliminar un precio de elemento de inventario",
)
async def eliminar_precio_elemento_inventario(
    session: AsyncSessionDep,
    precio_elemento_id: int,
):
    """Elimina un precio de elemento de inventario."""
    query = PrecioElementoInventarioQuery()
    precio_elemento_eliminado = await query.delete(session, precio_elemento_id)
    if precio_elemento_eliminado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PrecioElementoInventario no encontrado",
        )
    return precio_elemento_eliminado


@router.post(
    "/tipo_precio_elemento_inventario",
    response_model=TipoPrecioElementoInventario,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
    summary="Crear un nuevo tipo de precio de elemento de inventario",
    description="Crea un nuevo tipo de precio de elemento de inventario con los datos proporcionados.",
)
async def crear_tipo_precio_elemento_inventario(
    tipo_precio_elemento: TipoPrecioElementoInventario,
    session: AsyncSessionDep,
):
    """Crea un nuevo tipo de precio de elemento de inventario."""
    query = TipoPrecioElementoInventarioQuery()
    await query.create(session, tipo_precio_elemento)
    return tipo_precio_elemento


@router.get(
    "/tipos_precios_elementos_inventario",
    response_model=list[TipoPrecioElementoInventario],
    response_model_exclude_none=True,
    summary="Obtener lista de tipos de precios de elementos de inventario",
    description="Obtiene una lista paginada de tipos de precios de elementos de inventario.",
)
async def get_tipos_precios_elementos_inventario(
    session: AsyncSessionDep,
    skip: int = 0,
    limit: int = 100,
):
    """Obtiene una lista de tipos de precios de elementos de inventario."""
    query = TipoPrecioElementoInventarioQuery()
    tipos_precios_elementos = await query.get_list(
        session=session, skip=skip, limit=limit
    )
    return tipos_precios_elementos


@router.get(
    "/tipo_precio_elemento_inventario/{tipo_precio_elemento_id}",
    response_model=TipoPrecioElementoInventario,
    summary="Obtener un tipo de precio de elemento de inventario por ID",
    description="Obtiene los detalles de un tipo de precio de elemento de inventario específico mediante su ID.",
    response_model_exclude_none=True,
)
async def get_tipo_precio_elemento_inventario(
    session: AsyncSessionDep,
    tipo_precio_elemento_id: int,
):
    """Obtiene un tipo de precio de elemento de inventario por ID."""
    query = TipoPrecioElementoInventarioQuery()
    db_tipo_precio_elemento = await query.get(session, tipo_precio_elemento_id)
    if db_tipo_precio_elemento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TipoPrecioElementoInventario con ID {tipo_precio_elemento_id} no encontrado",
        )
    return db_tipo_precio_elemento


@router.put(
    "/tipo_precio_elemento_inventario/{tipo_precio_elemento_id}",
    response_model=TipoPrecioElementoInventario,
    summary="Actualizar un tipo de precio de elemento de inventario",
)
async def actualizar_tipo_precio_elemento_inventario(
    session: AsyncSessionDep,
    tipo_precio_elemento_id: int,
    tipo_precio_elemento: TipoPrecioElementoInventario,
):
    """Actualiza un tipo de precio de elemento de inventario."""
    query = TipoPrecioElementoInventarioQuery()
    tipo_precio_elemento_actualizado = await query.update(
        session, tipo_precio_elemento_id, tipo_precio_elemento
    )
    if tipo_precio_elemento_actualizado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="TipoPrecioElementoInventario no encontrado",
        )
    return tipo_precio_elemento_actualizado


@router.delete(
    "/tipo_precio_elemento_inventario/{tipo_precio_elemento_id}",
    response_model=TipoPrecioElementoInventario,
    summary="Eliminar un tipo de precio de elemento de inventario",
)
async def eliminar_tipo_precio_elemento_inventario(
    session: AsyncSessionDep,
    tipo_precio_elemento_id: int,
):
    """Elimina un tipo de precio de elemento de inventario."""
    query = TipoPrecioElementoInventarioQuery()
    tipo_precio_elemento_eliminado = await query.delete(
        session, tipo_precio_elemento_id
    )
    if tipo_precio_elemento_eliminado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="TipoPrecioElementoInventario no encontrado",
        )
    return tipo_precio_elemento_eliminado


@router.post(
    "/movimiento_inventario",
    response_model=MovimientoInventario,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
    summary="Crear un nuevo movimiento de inventario",
    description="Crea un nuevo movimiento de inventario con los datos proporcionados.",
)
async def crear_movimiento_inventario(
    movimiento: MovimientoInventario,
    session: AsyncSessionDep,
):
    """Crea un nuevo movimiento de inventario."""
    query = MovimientoInventarioQuery()
    await query.create(session, movimiento)
    return movimiento


@router.get(
    "/movimientos_inventario",
    response_model=list[MovimientoInventario],
    response_model_exclude_none=True,
    summary="Obtener lista de movimientos de inventario",
    description="Obtiene una lista paginada de movimientos de inventario.",
)
async def get_movimientos_inventario(
    session: AsyncSessionDep,
    skip: int = 0,
    limit: int = 100,
):
    """Obtiene una lista de movimientos de inventario."""
    query = MovimientoInventarioQuery()
    movimientos = await query.get_list(session=session, skip=skip, limit=limit)
    return movimientos


@router.get(
    "/movimiento_inventario/{movimiento_id}",
    response_model=MovimientoInventario,
    summary="Obtener un movimiento de inventario por ID",
    description="Obtiene los detalles de un movimiento de inventario específico mediante su ID.",
    response_model_exclude_none=True,
)
async def get_movimiento_inventario(
    session: AsyncSessionDep,
    movimiento_id: int,
):
    """Obtiene un movimiento de inventario por ID."""
    query = MovimientoInventarioQuery()
    db_movimiento = await query.get(session, movimiento_id)
    if db_movimiento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MovimientoInventario con ID {movimiento_id} no encontrado",
        )
    return db_movimiento


@router.put(
    "/movimiento_inventario/{movimiento_id}",
    response_model=MovimientoInventario,
    summary="Actualizar un movimiento de inventario",
)
async def actualizar_movimiento_inventario(
    session: AsyncSessionDep,
    movimiento_id: int,
    movimiento: MovimientoInventario,
):
    """Actualiza un movimiento de inventario."""
    query = MovimientoInventarioQuery()
    movimiento_actualizado = await query.update(session, movimiento_id, movimiento)
    if movimiento_actualizado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MovimientoInventario no encontrado",
        )
    return movimiento_actualizado


@router.delete(
    "/movimiento_inventario/{movimiento_id}",
    response_model=MovimientoInventario,
    summary="Eliminar un movimiento de inventario",
)
async def eliminar_movimiento_inventario(
    session: AsyncSessionDep,
    movimiento_id: int,
):
    """Elimina un movimiento de inventario."""
    query = MovimientoInventarioQuery()
    movimiento_eliminado = await query.delete(session, movimiento_id)
    if movimiento_eliminado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MovimientoInventario no encontrado",
        )
    return movimiento_eliminado


@router.post(
    "/tipo_movimiento_inventario",
    response_model=TipoMovimientoInventario,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
    summary="Crear un nuevo tipo de movimiento de inventario",
    description="Crea un nuevo tipo de movimiento de inventario con los datos proporcionados.",
)
async def crear_tipo_movimiento_inventario(
    tipo_movimiento: TipoMovimientoInventario,
    session: AsyncSessionDep,
):
    """Crea un nuevo tipo de movimiento de inventario."""
    query = TipoMovimientoInventarioQuery()
    await query.create(session, tipo_movimiento)
    return tipo_movimiento


@router.get(
    "/tipos_movimientos_inventario",
    response_model=list[TipoMovimientoInventario],
    response_model_exclude_none=True,
    summary="Obtener lista de tipos de movimientos de inventario",
    description="Obtiene una lista paginada de tipos de movimientos de inventario.",
)
async def get_tipos_movimientos_inventario(
    session: AsyncSessionDep,
    skip: int = 0,
    limit: int = 100,
):
    """Obtiene una lista de tipos de movimientos de inventario."""
    query = TipoMovimientoInventarioQuery()
    tipos_movimientos = await query.get_list(session=session, skip=skip, limit=limit)
    return tipos_movimientos


@router.get(
    "/tipo_movimiento_inventario/{tipo_movimiento_id}",
    response_model=TipoMovimientoInventario,
    summary="Obtener un tipo de movimiento de inventario por ID",
    description="Obtiene los detalles de un tipo de movimiento de inventario específico mediante su ID.",
    response_model_exclude_none=True,
)
async def get_tipo_movimiento_inventario(
    session: AsyncSessionDep,
    tipo_movimiento_id: str,
):
    """Obtiene un tipo de movimiento de inventario por ID."""
    query = TipoMovimientoInventarioQuery()
    db_tipo_movimiento = await query.get(session, tipo_movimiento_id)
    if db_tipo_movimiento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TipoMovimientoInventario con ID {tipo_movimiento_id} no encontrado",
        )
    return db_tipo_movimiento


@router.put(
    "/tipo_movimiento_inventario/{tipo_movimiento_id}",
    response_model=TipoMovimientoInventario,
    summary="Actualizar un tipo de movimiento de inventario",
)
async def actualizar_tipo_movimiento_inventario(
    session: AsyncSessionDep,
    tipo_movimiento_id: str,
    tipo_movimiento: TipoMovimientoInventario,
):
    """Actualiza un tipo de movimiento de inventario."""
    query = TipoMovimientoInventarioQuery()
    tipo_movimiento_actualizado = await query.update(
        session, tipo_movimiento_id, tipo_movimiento
    )
    if tipo_movimiento_actualizado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="TipoMovimientoInventario no encontrado",
        )
    return tipo_movimiento_actualizado


@router.delete(
    "/tipo_movimiento_inventario/{tipo_movimiento_id}",
    response_model=TipoMovimientoInventario,
    summary="Eliminar un tipo de movimiento de inventario",
)
async def eliminar_tipo_movimiento_inventario(
    session: AsyncSessionDep,
    tipo_movimiento_id: str,
):
    """Elimina un tipo de movimiento de inventario."""
    query = TipoMovimientoInventarioQuery()
    tipo_movimiento_eliminado = await query.delete(session, tipo_movimiento_id)
    if tipo_movimiento_eliminado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="TipoMovimientoInventario no encontrado",
        )
    return tipo_movimiento_eliminado


@router.post(
    "/estado_elemento_inventario",
    response_model=EstadoElementoInventario,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
    summary="Crear un nuevo estado de elemento de inventario",
    description="Crea un nuevo estado de elemento de inventario con los datos proporcionados.",
)
async def crear_estado_elemento_inventario(
    estado_elemento: EstadoElementoInventario,
    session: AsyncSessionDep,
):
    """Crea un nuevo estado de elemento de inventario."""
    query = EstadoElementoInventarioQuery()
    await query.create(session, estado_elemento)
    return estado_elemento


@router.get(
    "/estados_elementos_inventario",
    response_model=list[EstadoElementoInventario],
    response_model_exclude_none=True,
    summary="Obtener lista de estados de elementos de inventario",
    description="Obtiene una lista paginada de estados de elementos de inventario.",
)
async def get_estados_elementos_inventario(
    session: AsyncSessionDep,
    skip: int = 0,
    limit: int = 100,
):
    """Obtiene una lista de estados de elementos de inventario."""
    query = EstadoElementoInventarioQuery()
    estados_elementos = await query.get_list(session=session, skip=skip, limit=limit)
    return estados_elementos


@router.get(
    "/estado_elemento_inventario/{estado_elemento_id}",
    response_model=EstadoElementoInventario,
    summary="Obtener un estado de elemento de inventario por ID",
    description="Obtiene los detalles de un estado de elemento de inventario específico mediante su ID.",
    response_model_exclude_none=True,
)
async def get_estado_elemento_inventario(
    session: AsyncSessionDep,
    estado_elemento_id: int,
):
    """Obtiene un estado de elemento de inventario por ID."""
    query = EstadoElementoInventarioQuery()
    db_estado_elemento = await query.get(session, estado_elemento_id)
    if db_estado_elemento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"EstadoElementoInventario con ID {estado_elemento_id} no encontrado",
        )
    return db_estado_elemento


@router.put(
    "/estado_elemento_inventario/{estado_elemento_id}",
    response_model=EstadoElementoInventario,
    summary="Actualizar un estado de elemento de inventario",
)
async def actualizar_estado_elemento_inventario(
    session: AsyncSessionDep,
    estado_elemento_id: int,
    estado_elemento: EstadoElementoInventario,
):
    """Actualiza un estado de elemento de inventario."""
    query = EstadoElementoInventarioQuery()
    estado_elemento_actualizado = await query.update(
        session, estado_elemento_id, estado_elemento
    )
    if estado_elemento_actualizado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="EstadoElementoInventario no encontrado",
        )
    return estado_elemento_actualizado


@router.delete(
    "/estado_elemento_inventario/{estado_elemento_id}",
    response_model=EstadoElementoInventario,
    summary="Eliminar un estado de elemento de inventario",
)
async def eliminar_estado_elemento_inventario(
    session: AsyncSessionDep,
    estado_elemento_id: int,
):
    """Elimina un estado de elemento de inventario."""
    query = EstadoElementoInventarioQuery()
    estado_elemento_eliminado = await query.delete(session, estado_elemento_id)
    if estado_elemento_eliminado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="EstadoElementoInventario no encontrado",
        )
    return estado_elemento_eliminado
