import sys
import random
from copy import copy


class Interpretation():
    def __init__(self, n_variables=0) -> None:
        self.interpretation = []

        # Generar interpretacio aleatoria
        for _ in range(n_variables):
            self.interpretation.append(random.choice([False, True]))

    def check(self, literal):
        literal_bool = literal > 0
        return self.interpretation[abs(literal)-1] == literal_bool

    def flip(self, literal):
        # Canviar de signe el literal
        self.interpretation[abs(literal)-1] = -literal

    def copy(self):
        new_interpretation = Interpretation()

        new_interpretation.interpretation = copy(self.interpretation)

        return new_interpretation


class Clause():
    def __init__(self, literals: list) -> None:
        self.literals = []
        for literal in literals:
            self.literals.append(int(literal))

    def satisfied(self, interpretation: Interpretation):
        # Mirar si un literal es compleix
        for literal in self.literals:
            if interpretation.check(literal):
                return True

        return False

    def __str__(self) -> str:
        return str(self.literals)


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

    def get_unsatisfied_clause(self, interpretation: Interpretation):
        # Mira si exesteix una clausula que no es satifacible
        for clause in self.clauses:
            if not clause.satisfied(interpretation):
                return clause

        return None

    def __str__(self) -> str:
        output = "Variables: %i Clauses: %i\n" % (
            self.n_variables, self.n_clauses)
        for clause in self.clauses:
            output += str(clause) + "\n"
        return output


class WalkSat():
    def __init__(self, formula: Formula, max_tries: int = 1000, max_flips: int = 1000):
        self.max_tries = max_tries
        self.max_flips = max_flips

        self.formula = formula

        # Generar interpretacio aleatoria
        self.interpretation = Interpretation(self.formula.n_variables)

    def solve(self):
        for _ in range(1, self.max_tries):
            for _ in range(1, self.max_flips):
                # Mirar si hi ha una clausula que no satisfa la interpretacio
                unsatisfied_clause = self.formula.get_unsatisfied_clause(
                    self.interpretation)

                # Mirar si la interpretacio satisfa la formula
                if not unsatisfied_clause:
                    return self.interpretation

        pass

    def broken(self, litral):
        # Canviar variable i contar quantes clausules no satisfa
        new_interpretation = self.interpretation.copy()

        pass


if __name__ == "__main__":
    filename = sys.argv[1]
    formula = Formula(filename)
    print(str(formula))
    test_interpretation = Interpretation()
    test_interpretation.interpretation = [
        False, False, False, False, False, False, False, False, False, True]
    print(formula.get_unsatisfied_clause(test_interpretation))
    WalkSat(formula)
