from sqlmodel import Session, select
from database.datatables import Project, Ally, Achievement, Post, Student, InfoFellow
from constants import FellowRank

def get_projects(session: Session):
  projects = session.exec(
      select(Project).order_by(Project.id.desc())
  ).all()

  return [
    {
      "id": project.id,
      "title": project.title,
      "description": project.description,
      "release_date": project.release_date,
      "season": project.season,
      "image_url": project.image_url,
    }
    for project in projects
  ]

def get_allies(session: Session):
  allies = session.exec(
      select(Ally).order_by(Ally.id.desc())
  ).all()

  return [
    {
      "id": ally.id,
      "name": ally.name,
      "url": ally.url,
      "image_url": ally.image_url,
      "is_active": ally.is_active,
    }
    for ally in allies
  ]

def get_achievements(session: Session):
  achievements = session.exec(
      select(Achievement).order_by(Achievement.id.desc())
  ).all()

  return [
    {
      "id": achievement.id,
      "name": achievement.title,
      "url": achievement.description,
      "image_url": achievement.publish_date,
      "is_active": achievement.image_url,
    }
    for achievement in achievements
  ]
  
def get_posts(session: Session):
  posts = session.exec(
      select(Post).order_by(Post.id.desc())
  ).all()

  return [
    {
      "id": post.id,
      "name": post.title,
      "url": post.description,
      "image_url": post.publish_date,
      "is_active": post.image_url,
    }
    for post in posts
  ]
  
def get_directors(session: Session):
  statement = (
    select(Student, InfoFellow)
    .join(InfoFellow)
    .where(
        InfoFellow.fellow_rank.in_([
            FellowRank.DIRECTOR,
            FellowRank.VI_PRE,
            FellowRank.PRE
        ])
    )
    .order_by(InfoFellow.fellow_rank)
  )

  results = session.exec(statement).all()

  return [
      {
          "id": student.id,
          "name": f"{student.firstName} {student.middleName or ''} {student.lastName}".strip(),
          "rank": info.fellow_rank,
          "url": student.urlProfile,
          "is_active": info.isActive,
      }
      for student, info in results
  ]

def build_home_data(session: Session):
  return {
    "projects": get_projects(session),
    "allies": get_allies(session),
    "achievements": get_achievements(session),
    "posts": get_posts(session),
    "directors": get_directors(session),
  }