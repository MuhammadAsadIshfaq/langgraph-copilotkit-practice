from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import enum
from datetime import datetime

class TaskStatus(str, enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class Priority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class Role(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "User"
    
    id = Column(String, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    name = Column(String)
    password = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False, default=Role.USER)
    createdAt = Column(DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationship with tasks
    tasks = relationship("Task", back_populates="assignee")

class Task(Base):
    __tablename__ = "Task"
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.TODO)
    assigneeId = Column(String, ForeignKey("User.id", onupdate="CASCADE", ondelete="SET NULL"))
    createdAt = Column(DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = Column(DateTime, nullable=False, default=datetime.utcnow)
    priority = Column(Enum(Priority), nullable=False, default=Priority.MEDIUM)
    
    # Relationship with user
    assignee = relationship("User", back_populates="tasks")