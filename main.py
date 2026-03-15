from contextlib import asynccontextmanager
from fastapi import FastAPI
from database.datatables import create_db_and_tables, get_session
from database.seeders.studentSeeder import seed_students
from database.seeders.infofellowSeeder import seed_info_fellows
from database.seeders.projectSeeder import seed_projects
from modules.auth.auth_controller import router as auth_router
from modules.project_controller import router as project_router
from modules.controllers.home_controller import router as home_router

from sqlmodel import Session, select
from database.datatables import Student


session = next(get_session())


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ Solo se ejecuta una vez al iniciar
    create_db_and_tables()
    with next(get_session()) as session:
        seed_students(session)
        seed_info_fellows(session)
        seed_projects(session)

    yield  # La app corre aquí
    # Aquí puedes poner lógica de cierre si la necesitas


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    students = session.exec(select(Student)).all()
    return {"students": students}


app.include_router(auth_router)
app.include_router(project_router)
app.include_router(home_router)