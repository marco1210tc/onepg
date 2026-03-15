from fastapi import APIRouter, Depends
from typing import Annotated
from sqlmodel import Session

from database.datatables import get_session
from modules.services.home_service import build_home_data

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter()


@router.get("/home")
async def get_home(session: SessionDep):
    return build_home_data(session)