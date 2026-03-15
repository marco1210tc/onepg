from sqlmodel import Session, select
from database.datatables import Project

def seed_projects(session: Session):
    # Check if there are any projects in the database
    existing = session.exec(select(Project)).first()
    if existing:
        return

    projects = [
        Project(
            title="SEDITALKS",
            description="Description de seditalks",
            release_date="2025-05-18",
            season="2025-I",
            image_url="fotos_logos/SEDITALKS.png",
        ),
        Project(
            title="SediPatitas",
            description="Proyecto SediPatitas",
            release_date="2025-05-18",
            season="2025-I",
            image_url="fotos_logos/SediPatitas.png",
        ),
        Project(
            title="Amigos de la Tecnología",
            description="Proyecto Amigos de la Tecnología",
            release_date="2025-05-18",
            season="2025-I",
            image_url="fotos_logos/Amigos de la Tecnología.png",
        ),
        Project(
            title="NAVISEDIPRO 9.0",
            description="Proyecto NAVISEDIPRO 9.0",
            release_date="2025-10-22",
            season="2025-II",
            image_url="fotos_logos/NAVISEDIPRO 9.0.png",
        ),
        Project(
            title="Gestión de Proyectos 360",
            description="Proyecto Gestión de Proyectos 360",
            release_date="2025-10-22",
            season="2025-II",
            image_url="fotos_logos/Gestión de Proyectos 360.png",
        ),
        Project(
            title="CHEQUEATE UNT",
            description="Proyecto CHEQUEATE UNT",
            release_date="2025-10-22",
            season="2025-II",
            image_url="fotos_logos/CHEQUEATE UNT.png",
        ),
    ]

    session.add_all(projects)
    session.commit()