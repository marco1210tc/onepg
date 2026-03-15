from math import ceil
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, func

from database.datatables import get_session
from database.datatables import Project, ProjectMember, Student, ProjectRank

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("")
def get_projects(
    search: Optional[str] = Query(default=None, max_length=100),
    page: int = Query(default=1, ge=1),
    rows_per_page: int = Query(default=10, ge=1, le=100),
    session: Session = Depends(get_session)
):
    offset = (page - 1) * rows_per_page
    director_role = ProjectRank.DIR

    search_term = search.strip() if search else None

    # -----------------------------
    # QUERY BASE PARA COUNT
    # -----------------------------
    count_statement = select(func.count()).select_from(Project)

    if search_term:
        count_statement = count_statement.where(
            Project.title.ilike(f"%{search_term}%")
        )

    total = session.exec(count_statement).one()

    # -----------------------------
    # QUERY BASE PARA DATA
    # -----------------------------
    statement = (
        select(
            Project,
            Student.firstName,
            Student.middleName,
            Student.lastName
        )
        .select_from(Project)
        .join(
            ProjectMember,
            (ProjectMember.project_id == Project.id) &
            (ProjectMember.rol == director_role),
            isouter=True
        )
        .join(
            Student,
            Student.id == ProjectMember.member_id,
            isouter=True
        )
    )

    if search_term:
        statement = statement.where(
            Project.title.ilike(f"%{search_term}%")
        )

    statement = (
        statement
        .order_by(Project.id.desc())
        .offset(offset)
        .limit(rows_per_page)
    )

    rows = session.exec(statement).all()

    items = []
    for project, first_name, middle_name, last_name in rows:
        director = " ".join(
            part.strip()
            for part in [first_name, middle_name, last_name]
            if part and part.strip()
        ) or None

        items.append({
            "id": project.id,
            "title": project.title,
            "director": director,
            "description": project.description,
            "release_date": project.release_date,
            "season": project.season,
            "image_url": project.image_url,
        })

    total_pages = ceil(total / rows_per_page) if total > 0 else 1

    return {
        "items": items,
        "total": total,
        "page": page,
        "rows_per_page": rows_per_page,
        "total_pages": total_pages
    }