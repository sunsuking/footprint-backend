from fastapi import APIRouter, Depends
from api import database, models
from sqlalchemy.orm import Session
from api.schemas import diary_sc
from sqlalchemy import and_

router = APIRouter(
    prefix = "/diary",
    tags = ["Diary"],
    responses = {404: {"description": "Not Found"}},
)

get_db = database.get_db

@router.post("/post")
def postDiary(visit_id: int, user_id: str, diary: diary_sc.Diary, db: Session=Depends(get_db)):
    db_diary = models.Diary(
        user_id=user_id, 
        visit_id=visit_id, 
        content=diary.content, 
        photo=diary.photo, 
        visible=diary.visible)
        
    db.add(db_diary)
    db.commit()
    db.refresh(db_diary)
    return {
        "status": "OK",
        "result": db_diary
    }

@router.get("/read")
def readDiary(visit_id: int, user_id: str, db: Session=Depends(get_db)):
    result = db.query(models.Diary).filter(
        and_(models.Diary.visit_id == visit_id, models.Diary.user_id == user_id)).first()

    if result is None:
        raise HTTPException(status_code=404, detail="해당하는 Diary가 없습니다.")

    return {
        "status": "OK",
        "data": result
    }