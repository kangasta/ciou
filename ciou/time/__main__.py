if __name__ == "__main__":
    from queue import Queue

    from ._ticker import Ticker

    ticks = Queue()
    ticker = Ticker(1, ticks)
    ticker.start()

    while True:
        try:
            print(ticks.get())
        except KeyboardInterrupt:
            ticker.stop()
            break
