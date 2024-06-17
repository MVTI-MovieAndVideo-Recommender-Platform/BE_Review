from database import mysql_conn
from fastapi import Depends, HTTPException, Request
from model.table import PreferenceORM, RatingORM
from routes.apihelper import base64_to_uuid, produce_message
from routes.apihelper.delete_apihelpler import delete_preference, delete_rating
from routes.apihelper.read_apihelper import (
    read_user_collection,
    review_verify_collection,
)
from sqlalchemy.ext.asyncio import AsyncSession


async def delete_rating_endpoint(
    request: Request,
    mysql_db: AsyncSession = Depends(mysql_conn.get_db),
):
    if request.state.token and (user_id := base64_to_uuid(request.state.token)):
        if await review_verify_collection(user_id, request.query_params.get("media_id"), "rating"):
            pass
        else:
            raise HTTPException(status_code=400, detail="mongodb에 데이터가 없습니다.")
    else:
        raise HTTPException(status_code=400, detail="jwt 혹은 토큰 없음")

    if (
        request.state.token
        and (user_id := base64_to_uuid(request.state.token))
        and await read_user_collection(user_id)
    ):
        result = await delete_rating(
            model_orm=RatingORM(
                user_id=user_id,
                media_id=request.query_params.get("media_id"),
                rating=0,
                is_delete=False,  # 현재 is_delete 가 False인것을 찾아서 소프트 삭제함
            ),
            mysql_db=mysql_db,
        )
        return await produce_message(result)
    else:
        raise HTTPException(status_code=400, detail="jwt 혹은 토큰 없음")


async def delete_preference_endpoint(
    request: Request,
    mysql_db: AsyncSession = Depends(mysql_conn.get_db),
):
    if request.state.token and (user_id := base64_to_uuid(request.state.token)):
        if await review_verify_collection(
            user_id, request.query_params.get("media_id"), "preference"
        ):
            result = await delete_preference(
                model_orm=PreferenceORM(
                    user_id=user_id,
                    media_id=request.query_params.get("media_id"),
                    is_delete=False,  # 현재 is_delete 가 False인것을 찾아서 소프트 삭제함
                ),
                mysql_db=mysql_db,
            )
            return await produce_message(result)
        else:
            raise HTTPException(status_code=400, detail="mongodb에 데이터가 없습니다.")
    else:
        raise HTTPException(status_code=400, detail="jwt 혹은 토큰 없음")
