import logging
from typing import Dict

# from cachetools import LFUCache
from sqlalchemy import select, delete

from .settings import session
from .utils import inject_connection

logger = logging.getLogger(__name__)


# READ / GET
@inject_connection
async def get_object(model, filters, conn=None):
    """Get object from db"""
    key = f"{model.__name__}{filters}"
    query = select(model).filter_by(**filters)
    logger.debug(f"{__name__}.get_obj: query = {query}")
    async with conn:
        result = await conn.execute(query)
    logger.debug(f"{__name__}.get_obj: result = {result}")
    obj = result.scalars().first()
    logger.debug(f"{__name__}.get_obj: obj = {obj}")
    return obj


@inject_connection
async def get_all(model, conn=None):
    """Get objects from db"""
    query = select(model)
    async with conn:
        result = await conn.execute(query)
    logger.debug(f"{__name__}.get_all: result = {result}")
    objects = result.scalars().all()
    logger.debug(f"{__name__}.get_all: obj = {objects}")
    return objects


@inject_connection
async def get_all_with_filter(model, filters: dict, conn=None):
    """Get objects from db"""
    query = select(model).filter_by(**filters)
    async with conn:
        result = await conn.execute(query)
    logger.debug(f"{__name__}.get_all: result = {result}")
    objects = result.scalars().all()
    logger.debug(f"{__name__}.get_all: obj = {objects}")
    return objects


@inject_connection
async def get_objects(model, filters: Dict, limit=10, per_page=10, conn=None):
    """Get objects from db"""
    query = select(model).filter_by(**filters).limit(limit).offset(per_page)
    logger.debug(f"{__name__}.get_objects: query = {query}")
    async with conn:
        result = await conn.execute(query)
    logger.debug(f"{__name__}.get_objects: result = {result}")
    objects = result.scalars().all()
    logger.debug(f"{__name__}.get_objects: obj = {objects}")
    return objects


async def get_or_create_object(model, params, conn=None):
    """Get object from db or create new one"""
    key = f"{model.__name__}{params}"
    obj = await get_object(model, params, conn=conn)
    if not obj:
        obj = await create_object(model, params, conn=conn)
    return obj


# CREATE
@inject_connection
async def create_object(model, params, conn=None):
    """Create object in db"""
    logger.debug(f"{__name__}.create_obj: model = {model}, params = {params}")
    new_obj = model(**params)
    async with conn:
        conn.add(new_obj)
        await conn.commit()
    return new_obj


@inject_connection
async def bulk_create(objects, conn=None):
    for obj in objects:
        await create_object(obj, conn=conn)


# UPDATE
@inject_connection
async def update_object(obj, params, conn=None):
    """
    Soft Update object in db.
    If attribute not exists in model`s fields, then skip field without error
    """
    avaliable_fields = obj.__class__.__table__.columns.keys()
    for key, value in params.items():
        if key in avaliable_fields:
            setattr(obj, key, value)
    async with conn:
        await conn.commit()
        conn.refresh(obj)
    return obj


@inject_connection
async def update_or_error(obj, params, conn=None):
    """
    Soft Update object in db.
    If attribute not exists in model`s fields, then skip field without error
    """
    avaliable_fields = obj.__class__.__table__.columns.keys()
    for key, value in params.items():
        if key in avaliable_fields:
            setattr(obj, key, value)
        else:
            raise AttributeError(f"Attribute {key} not exists in {obj.__class__.__name__}")
    async with conn:
        await conn.commit()
        conn.refresh(obj)
    return obj


@inject_connection
async def update_object_by_id(model, id: int, params, conn=None):
    obj = await get_object(model, id=id)
    updated_obj = await update_object(obj, params, conn=conn)
    return updated_obj


def bulk_update():
    pass


@inject_connection
async def update_or_create_object(model, filters, params, conn=None):
    obj = await get_or_create_object(model, filters, conn=conn)
    return await update_object(obj, params, conn=conn)


# DELETE
@inject_connection
async def delete_object(obj, conn=None):
    model = obj.__class__
    id_ = obj.id
    return await delete_object_by_id(model, id_, conn=conn)


@inject_connection
async def delete_object_by_id(model, id_: int, conn=None):
    query = delete(model).where(model.id == id_)
    async with conn:
        await conn.execute(query)
        await conn.commit()
    logger.debug(f"{__name__}.delete_object_by_id: model = {model}, id = {id_}")
    return True


@inject_connection
async def bulk_delete(objects, conn=None):
    for obj in objects:
        await delete_object(obj, conn=conn)
    return True


@inject_connection
async def bulk_delete_by_id(model, ids, conn=None):
    for id_ in ids:
        await delete_object_by_id(model, id_, conn=conn)
    return True

