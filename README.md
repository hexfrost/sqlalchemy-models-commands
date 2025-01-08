[![Maintainability](https://api.codeclimate.com/v1/badges/d33ecb2661fb7aedf516/maintainability)](https://codeclimate.com/github/hexfrost/sqlalchemy-models-commands/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/d33ecb2661fb7aedf516/test_coverage)](https://codeclimate.com/github/hexfrost/sqlalchemy-models-commands/test_coverage)
[![flake8](https://github.com/hexfrost/simplecrud/actions/workflows/linter.yml/badge.svg?branch=staging)](https://github.com/hexfrost/simplecrud/actions/workflows/linter.yml)

***
# SimpleCRUD
[![PyPI Downloads](https://static.pepy.tech/badge/hexfrost-simplecrud)](https://pepy.tech/projects/hexfrost-simplecrud)

SimpleCRUD is a library that provides a simple way to create CRUD commands for SQLAlchemy models.


## Installation

```bash
pip install hexfrost-simplecrud
```
```
poetry add hexfrost-simplecrud
```

***

## Usage

1. Create a model
2. Create a sessionmaker from SQLAlchemy
4. Import CRUD functions
5. Use CRUD functions and enjoy

### Example usage

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from simplecrud import get_all, create_obj, update_obj, delete_object

engine = create_async_engine("sqlite+aiosqlite:///test.db", echo=True)
session = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

# Create a model
class ExampleModel(DeclarativeBase):
    __tablename__ = "example_model"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)


async def example_func():

    # Create a model
    new_model = await create_object(model, name="test", description="test", conn=session())

    # Get all models
    all_objs = await get_all(model, conn=session())

    # Update a model
    updated_obj = await update_object(model, name="test2", description="test2", conn=session())

    # Delete a model
    await delete_object(model, name="test2", description="test2", conn=session())

```

### Avaliable functions:
- `get_object` - get a single object
- `get_all` - get all objects
- `get_all_with_filter` - get all objects with filter
- `get_objects` - get all objects with filter, limit and offset
- `get_or_create_object` - get or create an object
- `create_object` - create an object
- `bulk_create` - create multiple objects
- `update_object` - update an object
- `update_or_error` - update an object or raise an error
- `update_object_by_id` - update an object by id
- `update_or_create_object` - update or create an object
- `delete_object` - delete an object
- `delete_object_by_id` - delete an object by id
- `bulk_delete` - bulk delete objects
- `bulk_delete_by_id` - bulk delete objects by id

***

## Contributing

This project is open for contributions. Feel free to open an issue or create a pull request.

***

## License

```GNU GENERAL PUBLIC LICENSE Version 3```

