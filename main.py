import sys
import random


class Clause():
    def __init__(self, literals: list) -> None:
        self.literals = []
        for literal in literals:
            self.literals.append(int(literal))

    def __str__(self) -> str:
        return str(self.literals)


class Interpretation():
    def __init__(self, n_variables) -> None:
        self.interpretation = []
        # Generar interpretacio aleatoria
        for _ in range(n_variables):
            self.interpretation.append(random.choice([False, True]))


class Formula():
    def __init__(self, filename: str) -> None:
        self.clauses = []

        # Obrir arxiu
        with open(filename, "r") as file:
            for line in file:
                if line[0] == "c":
                    # Saltar comentaris
                    continue

                if line[0] == "p":
                    # Parsejar parametres
                    splitted = line.split(" ")
                    self.n_variables = int(splitted[2])
                    self.n_clauses = int(splitted[3])
                    continue

                # Parsejar clausules
                clause = Clause(line.split(" ")[:-1])
                self.clauses.append(clause)


class WalkSat():
    def __init__(self, finelame: str) -> None:
        # Carregar formula
        self.formula = Formula(filename)
        # Generar interpretacio aleatoria
        self.interpretation = Interpretation(self.formula.n_variables)
        pass

    def solve():
        # Pag 27 diapos
        pass


if __name__ == "__main__":
    filename = sys.argv[1]

    WalkSat(filename)
