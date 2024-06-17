from fastapi import HTTPException
from model.table import RatingORM
from routes.apihelper import message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


def check_and_assign(rating: float) -> float:
    # 소수점이 0.5 단위인지 확인
    if rating * 10 % 5 != 0:
        raise ValueError("a는 0.5 단위로 입력되어야 합니다")

    # 범위와 조건에 따른 처리
    return (
        rating
        if 0 < rating <= 5
        else (
            5
            if rating > 5
            else (lambda: (_ for _ in ()).throw(ValueError("a는 0보다 커야 합니다")))()
        )
    )


async def update_rating(model_orm: RatingORM, mysql_db: AsyncSession):
    if result := (
        await mysql_db.execute(
            select(RatingORM).filter_by(
                user_id=model_orm.user_id,
                media_id=model_orm.media_id,
            )
        )
    ).scalar_one_or_none():
        try:
            # model_orm.rating = check_and_assign(float(model_orm.rating))
            result.rating = check_and_assign(float(model_orm.rating))
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        # result.rating = model_orm.rating
        await mysql_db.commit()
        print(
            f"{model_orm.user_id}가 {model_orm.media_id}를 {model_orm.rating}점으로 변경하였습니다"
        )
    else:
        raise HTTPException(status_code=400, detail=f"Mysql에 데이터가 존재하지 않습니다")
    update_time = (
        await mysql_db.execute(
            select(RatingORM).filter_by(user_id=model_orm.user_id, media_id=model_orm.media_id)
        )
    ).scalar_one_or_none()
    return message("update", "rating", update_time)
