from fastapi import APIRouter


project_router = APIRouter()


@project_router.get("/")
async def root():
    return {"message": "Hello World"}


@project_router.get("/projects")
async def get_projects():
    return {"message": "Hello World"}


@project_router.get("/projects/{project_id}")
async def get_project(project_id: str):
    return {"message": "Hello World"}


@project_router.post("/projects")
async def add_project():
    return {"message": "Hello World"}
