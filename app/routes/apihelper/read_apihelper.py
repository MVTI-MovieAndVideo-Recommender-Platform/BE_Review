import uuid

from database import mongo_conn
from fastapi import HTTPException
from routes.apihelper import uuid_to_base64


# preference collection에 데이터가 존재하는지 확인
async def preference_verify_collection(user_id: str, media_id: str) -> bool:
    return (
        result
        if (
            result := await mongo_conn.review["preference"].find_one(
                {"user_id": user_id, "media_id": int(media_id)}
            )
        )
        else False
    )


# rating collection에 데이터가 존재하는지 확인
async def review_verify_collection(user_id: str, media_id: str, table: str) -> bool | dict:
    return (
        result
        if (
            result := await mongo_conn.review[table].find_one(
                {"user_id": user_id, "media_id": int(media_id)}
            )
        )
        else False
    )


# 유저가 특정 미디어에 별점을 남겼는지 확인하는 함수
async def user_rating_media_verify_collection(user_id, media_id) -> bool:
    return await mongo_conn.review["rating"].find_one({"user_id": user_id, "media_id": media_id})
    if result and result["is_delete"]:
        return 1
    elif not result["is_delete"]:
        return 1
    else:
        False

    return (
        True
        if await mongo_conn.review["rating"].find_one(
            {"user_id": user_id, "media_id": media_id, "is_delete": False}
        )
        else False
    )


async def read_auth_collection(user_id: str) -> dict | None:
    return await mongo_conn.member["auth"].find_one({"_id": uuid_to_base64(uuid.UUID(user_id))})


async def read_user_collection(user_id: str) -> dict | None:
    result = await mongo_conn.member["user"].find_one({"_id": user_id})
    if await mongo_conn.member["user"].find_one({"_id": user_id}) and (
        result := await mongo_conn.review["preference"].find_one({"user_id": user_id})
    ):
        print(result)
    return await mongo_conn.member["user"].find_one({"_id": user_id})


async def check_preference_collection(user_id: str) -> bool:
    if await mongo_conn.member["user"].find_one({"_id": user_id}):
        if result := await mongo_conn.review["preference"].find_one(
            {"user_id": user_id}
        ) and not result.get(
            "is_delete"
        ):  # 비활성화 됐을 경우
            return False
        else:  # 소프트 삭제된 경우
            return True
    else:
        raise HTTPException(status_code=400, detail="회원 정보가 없음")

    print(await mongo_conn.review["preference"].find_one({"user_id": user_id}))
    if await mongo_conn.member["user"].find_one({"_id": user_id}) and (
        result := await mongo_conn.review["preference"].find_one({"user_id": user_id})
    ):
        print("check_preference_collection", result)
        if result == None:  # 새로 생성
            return True
        elif result.get("is_delete") == True:  # 업데이트
            return False
