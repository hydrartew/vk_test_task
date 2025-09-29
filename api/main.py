import uvicorn
from fastapi import FastAPI

from api.routers import get_top_users


app = FastAPI(
    title='API for VK test task',
    version='v1',
    openapi_url='/vk-test-task.json'
)

app.include_router(get_top_users.router)


def main():
    uvicorn.run("api.main:app", host="0.0.0.0", reload=True)


if __name__ == '__main__':
    main()
