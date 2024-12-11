from sqlalchemy import BigInteger, String, Date, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True)
    name_and_lastname: Mapped[str] = mapped_column(String(50))
    birthday = mapped_column(Date)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    task: Mapped[str] = mapped_column(String(255))
    deadline: Mapped[str] = mapped_column(String(30))
    status: Mapped[bool] = mapped_column(Boolean, default=False)
    type_task: Mapped[str] = mapped_column(String(30))

    def __iter__(self):
        yield self.id
        yield self.tg_id
        yield self.task
        yield self.deadline
        yield self.status
        yield self.type_task


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
