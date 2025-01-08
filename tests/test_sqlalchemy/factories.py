from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


class AsyncConnFactory():

    def __init__(self):
        self.async_engine = create_async_engine("sqlite+aiosqlite:///./test.db")
        self.async_session_maker = async_sessionmaker(self.async_engine, expire_on_commit=False, class_=AsyncSession)

    def __call__(self, *args, **kwargs):
        return self.async_session_maker()
