from typing import Optional
from lang._base import BaseCommand


class CreateTable(BaseCommand):

    def __init__(self, stringed_data: str):
        mapped_q = self.deconstruct(stringed_data)

        self.table_name: str = mapped_q["create_table"]
        self.table_columns: list = mapped_q["columns"]

    def exec(self) -> any:
        self.fs.create_index(self.table_name)
        return self.fs.create_table(self.table_name, self.table_columns)

    @classmethod
    def sql_create_table(cls, command: str) -> str:
        table_name = cls.find.between(command, "create_table", "columns")
        return table_name

    @classmethod
    def sql_columns(cls, command: str) -> list:
        columns = cls.find.right(command, "columns")
        return columns.split(",")

    @classmethod
    def deconstruct(cls, stringed_data: str, mapper: Optional[dict[str, callable]] = None) -> dict:
        commands_mapper = {
            "create_table": cls.sql_create_table,
            "columns": cls.sql_columns,
        }
        return super().deconstruct(stringed_data, commands_mapper)