from typing import Optional
from lang._base import BaseCommand


class Insert(BaseCommand):

    def __init__(self, stringed_data: str):
        mapped_q = self.deconstruct(stringed_data)

        self.table_name = mapped_q["insert"]
        self.obj_data = mapped_q["values"]

    def exec(self) -> any:
        return self.fs.write(self.table_name, self.obj_data)

    @classmethod
    def sql_insert(cls, command: str) -> str:
        table_name = cls.find.between(command, "insert", "values")
        return table_name

    @classmethod
    def sql_values(cls, command: str) -> list:
        values = cls.find.right(command, "values")
        return values.split(",")

    @classmethod
    def deconstruct(cls, stringed_data: str, mapper: Optional[dict[str, callable]] = None) -> dict:
        commands_mapper = {
            "insert": cls.sql_insert,
            "values": cls.sql_values,
        }
        return super().deconstruct(stringed_data, commands_mapper)
