from proxypool.scheduler import Schduler


def main():
    try:
        scheduler = Schduler()
        scheduler.run()
    except:
        main()


if __name__ == '__main__':
    main()
