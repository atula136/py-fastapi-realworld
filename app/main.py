from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.datastructures import URL
from starlette.middleware.base import BaseHTTPMiddleware
from app.api.routes import todo, user, profile
from app.db.base import init_db

init_db()
app = FastAPI()

class TrailingSlashMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if path != "/" and not path.endswith("/") and "api" not in path:  # Skip API paths
            request.scope["path"] = path + "/"
        response = await call_next(request)
        return response

app.add_middleware(TrailingSlashMiddleware)

"""
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.datastructures import URL

curl -L -X POST http://127.0.0.1:8000/todos -d '{"title": "Test Post", "description": "This is a test."}' -H "Content-Type: application/json"
The -L flag makes curl follow the redirect and display the final response
"""
# @app.middleware("http")
# async def add_trailing_slash(request: Request, call_next):
#     path = request.url.path
#     if path != "/" and not path.endswith("/"):
#         # Redirect to the same path but with a trailing slash
#         url = URL(
#             f"{request.url.scheme}://{request.url.hostname}"
#             f"{':' + str(request.url.port) if request.url.port else ''}{path}/"
#         )
#         if request.url.query:
#             url = url.include_query_params(request.url.query)
#         print("NEIT", url, sep=" ")
#         return RedirectResponse(url=str(url))
#     response = await call_next(request)
#     return response

app.include_router(todo.router)
app.include_router(user.router, prefix="/api/users", tags=["users"])
app.include_router(profile.router, prefix="/api", tags=["profiles"])

for route in app.router.routes:
    print(route.path)