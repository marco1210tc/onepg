import os
from sqlmodel import SQLModel, Field, create_engine, Session, Relationship
from dotenv import load_dotenv
from constants import FellowArea, FellowRank, ProjectRank
from typing import List, Optional

load_dotenv()


class Post(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    publish_date: str
    short_description: str
    long_description: str
    image_url: str = Field(default=None, nullable=True)


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str


class Ally(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    url: str
    image_url: str = Field(default=None, nullable=True)
    is_active: bool


class Achievement(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    publish_date: str
    image_url: str = Field(default=None, nullable=True)


# --- TABLAS CON RELACIONES ---


class ProjectMember(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    member_id: int = Field(foreign_key="student.id")
    rol: ProjectRank  # Asegúrate de tener este tipo definido

    # Relaciones hacia las tablas principales
    project: "Project" = Relationship(back_populates="project_members")
    student: "Student" = Relationship(back_populates="project_members")


class Project(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    release_date: str
    season: str
    image_url: str = Field(default=None, nullable=True)

    # Relación: Un proyecto tiene múltiples miembros
    project_members: List["ProjectMember"] = Relationship(back_populates="project")


class InfoFellow(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    fellow_code: str = Field(default=None, nullable=True)
    area: FellowArea
    fellow_rank: FellowRank
    isActive: bool = Field(default=True)
    idStudent: int = Field(foreign_key="student.id", ondelete="CASCADE")

    # Relación de vuelta hacia el estudiante
    student: "Student" = Relationship(back_populates="info_fellow")


class Student(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    firstName: str
    middleName: str = Field(default=None, nullable=True)
    lastName: str
    studentCode: str
    career: str = Field(default=None, nullable=True)
    urlProfile: str = Field(default=None, nullable=True)

    # Relación Uno a Uno con InfoFellow (uselist=False evita que devuelva una lista)
    info_fellow: Optional["InfoFellow"] = Relationship(
        back_populates="student", sa_relationship_kwargs={"uselist": False}
    )

    # Relación: Un estudiante puede ser miembro de múltiples proyectos
    project_members: List["ProjectMember"] = Relationship(back_populates="student")


engine = create_engine(
    os.environ["DB_URI"],  # ← rompe si no existe
    connect_args={"options": "-c lc_messages=en_US.UTF-8"},
    )


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
