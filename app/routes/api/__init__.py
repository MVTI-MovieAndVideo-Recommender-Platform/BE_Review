from fastapi.routing import APIRoute
from routes.api.create_api import register_preference_endpoint, register_rating_endpoint
from routes.api.delete_api import delete_preference_endpoint, delete_rating_endpoint
from routes.api.update_api import update_rating_endpoint

rating_post_route = APIRoute(path="/rating", endpoint=register_rating_endpoint, methods=["POST"])

rating_update_route = APIRoute(
    path="/editrating", endpoint=update_rating_endpoint, methods=["PATCH"]
)

rating_delete_route = APIRoute(
    path="/deleterating", endpoint=delete_rating_endpoint, methods=["Delete"]
)

preference_post_route = APIRoute(
    path="/preference", endpoint=register_preference_endpoint, methods=["POST"]
)
preference_delete_route = APIRoute(
    path="/deletepreference", endpoint=delete_preference_endpoint, methods=["delete"]
)
