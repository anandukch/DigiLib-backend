from fastapi import APIRouter
from app.projects.crud import projectCrud

from app.serializers.projects import projectSerializer, projectsSerializer


project_router = APIRouter()


@project_router.get("/")
async def get_projects():
    return projectsSerializer(projectCrud.get_all())


@project_router.get("/{project_id}")
async def get_project(project_id: str):
    return projectSerializer(projectCrud.get(project_id))


@project_router.post("/") 
async def add_project():
    return {"message": "Hello World"}


