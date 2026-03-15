from sqlmodel import Session, select
from database.datatables import  ProjectMember
from constants import Roles

def seed_info_fellows(session: Session):
 
    existing = session.exec(select(ProjectMember)).first()

    if existing:
        return
    
    projectmembers = [
     #   ProjectMember(
     #       project_id=1,
     #       student_id=1    
     #   )
    ]

    session.add_all(projectmembers)
    session.commit()