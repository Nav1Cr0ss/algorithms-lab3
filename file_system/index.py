import re
from bisect import bisect_left


class Index:
    DB_SOURCE = "db/indexes"

    @classmethod
    def get_full_index_name(cls, table_name: str) -> str:
        return f"{cls.DB_SOURCE}/{table_name}"

    @classmethod
    def create_index(cls, table_name: str) -> None:
        with open(cls.get_full_index_name(table_name), "w") as f:
            pass

    @classmethod
    def get_column_indexes(cls, selected: list, full: list) -> list:
        res = []
        for i_f, val_f in enumerate(full):
            for val_s in selected:
                if val_f == val_s:
                    res.append(i_f)
        return res

    @classmethod
    def get_index(cls, table_name: str, obj_id: int) -> int:
        with open(cls.get_full_index_name(table_name), "r") as f:
            index = cls.binary_search(f.readlines(), obj_id) + 1
            return index

    @classmethod
    def update_index(cls, table_name: str, obj_id: int, last_el: int):

        with open(cls.get_full_index_name(table_name), "r+") as f:
            data = f.read().splitlines()
            data.append(f"{obj_id}___{last_el}")
            data.sort(key=lambda s: int(re.search(r'\d+', s).group()))
            f.seek(0)
            f.writelines([line + "\n" for line in data])

    @classmethod
    def binary_search(cls, obj_list: list, obj_id: int) -> int:
        i = bisect_left([obj.split("___")[0] for obj in obj_list], str(obj_id))
        if i != len(obj_list) and obj_list[i].startswith(str(obj_id)):
            result = re.search('___(.*)\n', obj_list[i])
            return int(result.group(1))
        else:
            return -1