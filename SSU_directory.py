import ProfessorParser


def main():
    a = ProfessorParser.ProfessorParser(6)
    a.spawnThreads()
    a.timeIt()

if __name__ == "__main__":
    main()