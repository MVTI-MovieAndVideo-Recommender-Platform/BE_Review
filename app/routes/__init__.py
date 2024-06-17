from fastapi import APIRouter
from routes.api import (
    preference_delete_route,
    preference_post_route,
    rating_delete_route,
    rating_post_route,
    rating_update_route,
)

router = APIRouter(tags=["Rating"])

router.routes.append(rating_post_route)
router.routes.append(rating_update_route)
router.routes.append(rating_delete_route)
router.routes.append(preference_post_route)
router.routes.append(preference_delete_route)
