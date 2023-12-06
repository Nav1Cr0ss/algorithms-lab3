from lang.create_table import CreateTable
from lang.insert import Insert
from lang.select import Select


class LangCommander:

    @classmethod
    def run_command(cls, stringed_data: str) -> any:
        commands = {
            "insert": Insert,
            "select": Select,
            "create_table": CreateTable,
        }
        try:
            command = stringed_data[:stringed_data.index(" ")]

            ins = commands[command](stringed_data)
            print(ins.exec() or "no result")
        except Exception as exc:
            print(exc)

