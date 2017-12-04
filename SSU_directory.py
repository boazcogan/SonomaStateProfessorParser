import ProfessorParser


def main():
    # I recommend not exceeding 10 threads, 6 is the number of threads chosen after optimization testing.
    a = ProfessorParser.ProfessorParser(6)
    a.spawnThreads()
    a.timeIt()

if __name__ == "__main__":
    main()
