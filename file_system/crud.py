import json
from typing import Optional

from file_system.index import Index


class CRUD:
    index = Index
    DB_SOURCE = "db/tables"

    @classmethod
    def get_full_table_name(cls, table_name: str) -> str:
        return f"{cls.DB_SOURCE}/{table_name}"

    @classmethod
    def create_index(cls, table_name: str) -> None:
        cls.index.create_index(table_name)

    @classmethod
    def create_table(cls, table_name: str, obj_columns: list) -> None:
        with open(cls.get_full_table_name(table_name), "w") as f:
            f.write(f'{"___".join(obj_columns)}\n')

    @classmethod
    def read(cls, table_name: str, obj_id: int, columns: list) -> Optional[str]:

        obj_index = cls.index.get_index(table_name, obj_id)
        if not obj_index:
            return

        with open(cls.get_full_table_name(table_name), "r") as f:
            lines = f.readlines()
            labels = lines[0].replace("\n", "").split("___")

            res = {}
            obj = lines[obj_index].replace("\n", "").split("___")

            column_indexes = cls.index.get_column_indexes(columns, labels)
            for index in column_indexes:
                res[labels[index]] = obj[index]

            return json.dumps(res)

    @classmethod
    def count(cls, table_name: str) -> int:
        with open(cls.index.get_full_index_name(table_name), "r") as f:
            return len(f.readlines())

    @classmethod
    def write(cls, table_name: str, data: list):
        with open(cls.get_full_table_name(table_name), "a") as f:
            f.write(f'{"___".join(data)}\n')

        cls.index.update_index(table_name, data[0], cls.count(table_name))

