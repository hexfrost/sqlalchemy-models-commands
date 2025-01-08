from typing import Dict, List

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession


# READ / GET


async def get_object(model, filters: dict, conn: AsyncSession = None) -> object:
    """Get object from db"""
    query = select(model).filter_by(**filters)
    async with conn:
        result = await conn.execute(query)
    obj = result.scalars().first()
    return obj


async def get_all(model, conn: AsyncSession = None) -> List[object]:
    """Get objects from db"""
    query = select(model)
    async with conn:
        result = await conn.execute(query)
    objects = result.scalars().all()
    return objects


async def get_all_with_filter(model, filters: dict, conn: AsyncSession = None) -> List[object]:
    """Get objects from db"""
    query = select(model).filter_by(**filters)
    async with conn:
        result = await conn.execute(query)
    objects = result.scalars().all()
    return objects


async def get_objects(
    model, filters: Dict, limit: int = 10, offset: int = 10, conn: AsyncSession = None
) -> List[object]:
    """Get objects from db"""
    query = select(model).filter_by(**filters).limit(limit).offset(offset)
    async with conn:
        result = await conn.execute(query)
    objects = result.scalars().all()
    return objects


async def get_or_create_object(model, params: dict, conn: AsyncSession = None) -> object:
    """Get object from db or create new one"""
    obj = await get_object(model, params, conn=conn)
    if not obj:
        obj = await create_object(model, params, conn=conn)
    return obj


# CREATE


async def create_object(model, params, conn: AsyncSession = None) -> object:
    """Create object in db"""
    new_obj = model(**params)
    async with conn:
        conn.add(new_obj)
        await conn.commit()
    return new_obj


async def bulk_create(model, data: List[Dict], conn: AsyncSession = None) -> List[object]:
    """Bulk create objects in db"""
    return [await create_object(model, params, conn=conn) for params in data]


# UPDATE


async def update_object(obj, params, conn: AsyncSession = None) -> object:
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


async def update_or_error(obj, params, conn: AsyncSession = None) -> object:
    """
    Soft Update object in db.
    If attribute not exists in model`s fields, then skip field without error
    """
    avaliable_fields = obj.__class__.__table__.columns.keys()
    for key, value in params.items():
        if key not in avaliable_fields:
            raise AttributeError(f"Attribute {key} not exists in {obj.__class__.__name__}")
    obj = await update_object(obj, params, conn=conn)
    return obj


async def update_object_by_id(model, id: int, params, conn: AsyncSession = None) -> object:
    """Update object in db by id"""
    obj = await get_object(model, dict(id=id), conn=conn)
    updated_obj = await update_object(obj, params, conn=conn)
    return updated_obj


# async def bulk_update(objects, params, conn: AsyncSession = None) -> List[object]:
#     """Bulk update objects in db"""
#     updated_objects = []
#     for obj in objects:
#         updated_obj = await update_object(obj, params, conn=conn)
#         updated_objects.append(updated_obj)
#     return updated_objects


async def update_or_create_object(model, filters, params, conn: AsyncSession = None) -> object:
    obj = await get_or_create_object(model, filters, conn=conn)
    return await update_object(obj, params, conn=conn)


# DELETE


async def delete_object(obj, conn: AsyncSession = None) -> bool:
    model = obj.__class__
    id_ = obj.id
    return await delete_object_by_id(model, id_, conn=conn)


async def delete_object_by_id(model, id_: int, conn: AsyncSession = None) -> bool:
    query = delete(model).where(model.id == id_)
    async with conn:
        await conn.execute(query)
        await conn.commit()
    return True


async def bulk_delete(objects, conn: AsyncSession = None) -> bool:
    for obj in objects:
        await delete_object(obj, conn=conn)
    return True


async def bulk_delete_by_id(model, ids, conn: AsyncSession = None) -> bool:
    for id_ in ids:
        await delete_object_by_id(model, id_, conn=conn)
    return True
