from lang._commander import LangCommander


def server():
    while True:
        if raw_command := input("naviSql : "):
            LangCommander.run_command(raw_command)


def main():
    server()


if __name__ == '__main__':
    main()
