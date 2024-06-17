from database import mysql_conn
from fastapi import Depends, HTTPException, Request
from model.table import RatingORM
from routes.apihelper import base64_to_uuid, produce_message
from routes.apihelper.read_apihelper import review_verify_collection
from routes.apihelper.update_apihelpler import update_rating
from sqlalchemy.ext.asyncio import AsyncSession


async def update_rating_endpoint(
    request: Request,
    mysql_db: AsyncSession = Depends(mysql_conn.get_db),
):
    if request.state.token and (user_id := base64_to_uuid(request.state.token)):
        if await review_verify_collection(user_id, request.query_params.get("media_id"), "rating"):
            result = await update_rating(
                model_orm=RatingORM(
                    user_id=user_id,
                    media_id=request.query_params.get("media_id"),
                    rating=request.query_params.get("rating"),
                ),
                mysql_db=mysql_db,
            )
            return await produce_message(result)
        else:
            raise HTTPException(status_code=400, detail="mongodb에 데이터가 없습니다.")
    else:
        raise HTTPException(status_code=400, detail="jwt 혹은 토큰 없음")
