from fastapi import HTTPException
from model.table import PreferenceORM, RatingORM
from routes.apihelper import message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def insert_preference_db(model_orm: PreferenceORM, mysql_db: AsyncSession):
    mysql_db.add(model_orm)
    await mysql_db.commit()
    result = await get_preference(model_orm, mysql_db)
    return message("insert", "preference", result)


async def re_insert_preference_db(model_orm: PreferenceORM, mysql_db: AsyncSession):
    if result := (
        await mysql_db.execute(
            select(PreferenceORM).filter_by(
                user_id=model_orm.user_id,
                media_id=model_orm.media_id,
                is_delete=True,
            )
        )
    ).scalar_one_or_none():
        result.is_delete = False
        await mysql_db.commit()
        print(f"user_id {model_orm.user_id} is re create")
    else:
        raise HTTPException(status_code=400, detail=f"Mysql에 데이터가 존재하지 않습니다")
    update_time = (
        await mysql_db.execute(
            select(PreferenceORM).filter_by(user_id=model_orm.user_id, media_id=model_orm.media_id)
        )
    ).scalar_one_or_none()
    return message("update", "preference", update_time)


async def insert_rating_db(model_orm: RatingORM, mysql_db: AsyncSession):
    mysql_db.add(model_orm)
    await mysql_db.commit()
    result = await get_rating(model_orm, mysql_db)
    return message("insert", "rating", result)


async def re_insert_rating_db(model_orm: RatingORM, mysql_db: AsyncSession):
    if result := (
        await mysql_db.execute(
            select(RatingORM).filter_by(
                user_id=model_orm.user_id,
                media_id=model_orm.media_id,
                is_delete=True,
            )
        )
    ).scalar_one_or_none():
        result.rating = model_orm.rating
        result.is_delete = False
        await mysql_db.commit()
        print(f"user_id {model_orm.user_id} is re create")
    else:
        raise HTTPException(status_code=400, detail=f"Mysql에 데이터가 존재하지 않습니다")
    update_time = (
        await mysql_db.execute(
            select(PreferenceORM).filter_by(user_id=model_orm.user_id, media_id=model_orm.media_id)
        )
    ).scalar_one_or_none()
    return message("update", "rating", update_time)


async def get_rating(rating_model: RatingORM, mysql_db: AsyncSession):
    query = select(RatingORM).where(
        RatingORM.user_id == rating_model.user_id, RatingORM.media_id == rating_model.media_id
    )
    return (await mysql_db.execute(query)).scalar_one_or_none()


async def get_preference(preference_model: PreferenceORM, mysql_db: AsyncSession):
    query = select(PreferenceORM).where(
        PreferenceORM.user_id == preference_model.user_id,
        PreferenceORM.media_id == preference_model.media_id,
    )
    return (await mysql_db.execute(query)).scalar_one_or_none()
