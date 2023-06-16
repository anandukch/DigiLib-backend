from app.common import BaseCrud
from app.db import Utils
from app.library.schemas import LibConfig


class LibraryCrud(BaseCrud):
    def __init__(self):
        super().__init__(Utils)

    def get_lib_config(self):
        fine_rate = self.db.find_one({"name": "fine_rate"})
        days_of_return = self.db.find_one({"name": "days_of_return"})
        if not fine_rate or not days_of_return:
            return None
        return {
            "fine_rate": fine_rate["value"],
            "days_of_return": days_of_return["value"],
        }

    def add_lib_config(self, payload: LibConfig):
        if not self.get_lib_config():
            self.db.insert_many(
                [
                    {"name": "fine_rate", "value": payload.fine_rate},
                    {"name": "days_of_return", "value": payload.days_of_return},
                ]
            )
        else:
            self.update({"name": "fine_rate"}, {"value": payload.fine_rate})
            self.update({"name": "days_of_return"}, {"value": payload.days_of_return})
        return {
            "fine_rate": payload.fine_rate,
            "days_of_return": payload.days_of_return,
        }


library_crud = LibraryCrud()
