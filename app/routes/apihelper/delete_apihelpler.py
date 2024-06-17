from fastapi import HTTPException
from model.table import PreferenceORM, RatingORM
from routes.apihelper import message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# preference 소프트 삭제
async def delete_preference(model_orm: PreferenceORM, mysql_db: AsyncSession):
    if result := (
        await mysql_db.execute(
            select(PreferenceORM).filter_by(
                user_id=model_orm.user_id,
                media_id=model_orm.media_id,
                is_delete=model_orm.is_delete,
            )
        )
    ).scalar_one_or_none():
        result.is_delete = not model_orm.is_delete
        await mysql_db.commit()
        print(f"user_id {model_orm.user_id}'s preference media is delete")
    else:
        raise HTTPException(status_code=400, detail=f"Mysql에 데이터가 존재하지 않습니다")
    update_time = (
        await mysql_db.execute(
            select(PreferenceORM).filter_by(user_id=model_orm.user_id, media_id=model_orm.media_id)
        )
    ).scalar_one_or_none()
    return message("delete", "preference", update_time)


# rating 소프트 삭제
async def delete_rating(model_orm: RatingORM, mysql_db: AsyncSession):
    if result := (
        await mysql_db.execute(
            select(RatingORM).filter_by(
                user_id=model_orm.user_id,
                media_id=model_orm.media_id,
                is_delete=model_orm.is_delete,
            )
        )
    ).scalar_one_or_none():
        result.is_delete = not model_orm.is_delete
        result.rating = 0
        await mysql_db.commit()
        print(f"user_id {model_orm.user_id}'s rating media is delete")
    else:
        raise HTTPException(status_code=400, detail=f"Mysql에 데이터가 존재하지 않습니다")
    update_time = (
        await mysql_db.execute(
            select(RatingORM).filter_by(user_id=model_orm.user_id, media_id=model_orm.media_id)
        )
    ).scalar_one_or_none()
    return message("delete", "rating", update_time)
