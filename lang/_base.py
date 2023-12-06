from typing import Optional

from file_system.crud import CRUD


class String:
    @classmethod
    def between(cls, command: str, start: str, finish: str) -> str:
        between_str = ((command.split(start))[1].split(finish)[0]).strip()
        return between_str

    @classmethod
    def right(cls, command: str, word: str) -> str:
        values_i = command.rfind(word)
        text = command[values_i + len(word):].strip()
        return text


class BaseCommand:
    fs = CRUD
    find = String

    @classmethod
    def deconstruct(cls, stringed_data: str, mapper: Optional[dict[str, callable]] = None) -> dict:
        query = {}
        if not mapper:
            return query

        for i in stringed_data.split(" "):
            try:
                query[i] = mapper[i](stringed_data)
            except KeyError:
                pass
        return query

    @classmethod
    def exec(cls):
        raise NotImplementedError
