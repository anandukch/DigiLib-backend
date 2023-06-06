from app.common import BaseCrud
from app.db import Projects


class ProjectCrud(BaseCrud):
    def __init__(self, db):
        super().__init__(db)
    
projectCrud=ProjectCrud(Projects)
