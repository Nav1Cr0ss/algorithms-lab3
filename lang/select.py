from typing import Optional
from lang._base import BaseCommand


class Select(BaseCommand):

    def __init__(self, stringed_data: str):
        mapped_q = self.deconstruct(stringed_data)

        self.columns: list = mapped_q["select"]
        self.table_name: str = mapped_q["from"]
        self.obj_id: int = mapped_q["where"]

    def exec(self) -> any:
        return self.fs.read(self.table_name, self.obj_id, self.columns)


    @classmethod
    def sql_select(cls, command: str) -> list:
        args = cls.find.between(command, "select", "from")
        return args.split(",")

    @classmethod
    def sql_from(cls, command: str) -> str:
        table_name = cls.find.between(command, "from", "where")
        return table_name

    @classmethod
    def sql_where(cls, command: str) -> int:
        return int(cls.find.right(command, "where"))

    @classmethod
    def deconstruct(cls, stringed_data: str, mapper: Optional[dict[str, callable]] = None) -> dict:
        commands_mapper = {
            "select": cls.sql_select,
            "from": cls.sql_from,
            "where": cls.sql_where,
        }
        return super().deconstruct(stringed_data, commands_mapper)
