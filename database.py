import os
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, DateTime, ForeignKey, Boolean, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql import func
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///site.db')

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=True)
    role = Column(String, nullable=True)
    progress = Column(String, default='')

class Sprint(Base):
    __tablename__ = 'sprints'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    status = Column(String, default='Planning')
    goal = Column(String, default='')

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, default='')
    type = Column(String, default='Task')
    priority = Column(String, default='Medium')
    status = Column(String, default='To Do')
    points = Column(Integer, default=0)
    sort_order = Column(Integer, default=0)
    assignee_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    sprint_id = Column(Integer, ForeignKey('sprints.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    assignee = relationship('User')
    sprint = relationship('Sprint')

class ActivityLog(Base):
    __tablename__ = 'activity_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    actor_user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    actor_username = Column(String, nullable=True)
    event_type = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=True)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    message = Column(String, nullable=False)
    is_read = Column(Integer, default=0)  # matching sqlite INTEGER default 0
    created_at = Column(DateTime, default=func.now())

# Initialize the db metadata if it doesn't exist
Base.metadata.create_all(bind=engine)


def _run_migrations():
    inspector = inspect(engine)
    if "tasks" not in inspector.get_table_names():
        return

    task_columns = {column["name"] for column in inspector.get_columns("tasks")}
    with engine.begin() as connection:
        if "sort_order" not in task_columns:
            connection.execute(text("ALTER TABLE tasks ADD COLUMN sort_order INTEGER DEFAULT 0"))
        connection.execute(
            text(
                """
                UPDATE tasks
                SET sort_order = id
                WHERE sort_order IS NULL OR sort_order = 0
                """
            )
        )


_run_migrations()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
