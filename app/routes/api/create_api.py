from database import mysql_conn
from fastapi import Depends, HTTPException, Request
from model.table import PreferenceORM, RatingORM
from routes.apihelper import base64_to_uuid, produce_message
from routes.apihelper.create_apihelper import (
    insert_preference_db,
    insert_rating_db,
    re_insert_preference_db,
    re_insert_rating_db,
)
from routes.apihelper.read_apihelper import review_verify_collection
from sqlalchemy.ext.asyncio import AsyncSession


async def register_rating_endpoint(
    request: Request,
    mysql_db: AsyncSession = Depends(mysql_conn.get_db),
):
    if request.state.token and (user_id := base64_to_uuid(request.state.token)):
        result = await review_verify_collection(
            user_id, request.query_params.get("media_id"), "rating"
        )
        if result and result.get("is_delete"):
            print("rating table에 데이터가 있으니 업데이트")
            result = await re_insert_rating_db(
                model_orm=RatingORM(
                    user_id=user_id,
                    media_id=request.query_params.get("media_id"),
                    rating=request.query_params.get("rating"),
                ),
                mysql_db=mysql_db,
            )
        elif not result:
            print("rating table에 데이터가 없으니 새로 생성")
            result = await insert_rating_db(
                model_orm=RatingORM(
                    user_id=user_id,
                    media_id=request.query_params.get("media_id"),
                    rating=request.query_params.get("rating"),
                ),
                mysql_db=mysql_db,
            )
        else:
            raise HTTPException(status_code=400, detail="별점을 중복으로 생성할 수 없습니다.")
        return await produce_message(result)

    else:
        raise HTTPException(status_code=400, detail="jwt 혹은 토큰 없음")


# 새로 선호영화를 추가 하거나 이전에 삭제한 선호영화를 다시 활성화 시키는 api
async def register_preference_endpoint(
    request: Request,
    mysql_db: AsyncSession = Depends(mysql_conn.get_db),
):
    if request.state.token and (user_id := base64_to_uuid(request.state.token)):
        result = await review_verify_collection(
            user_id, request.query_params.get("media_id"), "preference"
        )
        if result:  # 데이터 있으니 업데이트
            print("preference table에 데이터가 있으니 업데이트")
            result = await re_insert_preference_db(
                model_orm=PreferenceORM(
                    user_id=user_id,
                    media_id=request.query_params.get("media_id"),
                ),
                mysql_db=mysql_db,
            )
        else:  # 데이터 없으니 새로 추가
            print("preference table에 데이터가 없으니 새로 생성")
            result = await insert_preference_db(
                model_orm=PreferenceORM(
                    user_id=user_id,
                    media_id=request.query_params.get("media_id"),
                ),
                mysql_db=mysql_db,
            )
        return await produce_message(result)
    else:
        raise HTTPException(status_code=400, detail="jwt 혹은 토큰 없음")
