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

    def __str__(self) -> str:
        output = "s "
        for i, literal in enumerate(self.interpretation):
            if literal:
                output += str(i+1)
            else:
                output += str(-(i+1))

            output += " "
        return output


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

    def count_satisfied_literals(self, interpretation: Interpretation):
        # Comptem el numero de literals satisfacibles, utilitzat nomes en una estructura de dades
        count = 0
        for literal in self.literals:
            if interpretation.check(literal):
                count += 1

        return count

    def __str__(self) -> str:
        return str(self.literals)


class Formula():
    def __init__(self, filename: str) -> None:
        self.clauses = []

        # Obrir arxiu
        with open(filename, "r") as file:
            actual_clause = 0

            for line in file:
                if line[0] == "c":
                    # Saltar comentaris
                    continue

                if line[0] == "p":
                    # Parsejar parametres
                    splitted = line.split(" ")
                    self.n_variables = int(splitted[2])
                    self.n_clauses = int(splitted[3])
                    # La posició 0 no s'utilitza i cada posició conté una llista de clausules on apareix el literal
                    self.literals_map = [[]
                                         for i in range(0, 1 + self.n_variables * 2)]
                    continue

                # Parsejar clausules
                clause = Clause(line.split(" ")[:-1])

                for literal in clause.literals:
                    self.literals_map[literal].append(actual_clause)

                self.clauses.append(clause)
                actual_clause += 1

    def populate_satisfied_clauses_arr(self, interpretation: Interpretation):
        # Cada posicio representa una clausula i conte el nombre de literals satisfetes
        self.satisfied_clauses_arr = []
        self.unsat_count = 0

        for clause in self.clauses:
            count = clause.count_satisfied_literals(interpretation)
            if count == 0:
                self.unsat_count += 1
            self.satisfied_clauses_arr.append(count)

    def get_unsatisfied_clause(self, interpretation: Interpretation):
        # Si tenim 0 al contador retornem directament None
        if self.unsat_count == 0:
            return None

        # Mira si exesteix una clausula que no es satifacible
        #! Poser seria mes eficiet fer anar un contador per el index encomptes del enumerate
        for index, count in enumerate(self.satisfied_clauses_arr):
            if count == 0:
                return self.clauses[index].literals

        return None

    def satisfied_clauses(self, interpretation: Interpretation):
        # Cada posicio representa una clausula i conte el nombre de literals satisfetes
        for i, clause in enumerate(self.clauses):
            for literal in clause.literals:
                if interpretation.check(literal):
                    self.satisfied_clauses_arr[i] += 1

        # print(self.satisfied_clauses_arr)

    def update_satisfied_clauses(self, interpretation: Interpretation, literal):
        # Actualitza el nombre de clausules satisfetes per cada literal

        for index in self.literals_map[literal]:
            clause = self.clauses[index]
            sat_count = clause.count_satisfied_literals(interpretation)
            self.satisfied_clauses_arr[index] = sat_count
            if self.satisfied_clauses_arr[index] == 0 and sat_count != 0:
                self.unsat_count -= 1

            if self.satisfied_clauses_arr[index] != 0 and sat_count == 0:
                self.unsat_count += 1

    def count_unsatisfied_clauses(self, interpretation: Interpretation, literal):
        counter = self.unsat_count
        # Conta quantes clausules es falsifiquen
        for index in self.literals_map[literal]:
            clause = self.clauses[index]
            sat_count = clause.count_satisfied_literals(interpretation)
            if sat_count == 0:
                counter += 1

        return counter

    def __str__(self) -> str:
        output = "Variables: %i Clauses: %i\n" % (
            self.n_variables, self.n_clauses)
        for clause in self.clauses:
            output += str(clause) + "\n"
        return output


class WalkSat():
    def __init__(self, formula: Formula, max_tries: int = 1000, max_flips: int = 100, w: float = 0.8):
        self.max_tries = max_tries
        self.max_flips = max_flips

        self.w = w

        self.formula = formula

        # Generar interpretacio aleatoria
        # self.interpretation = Interpretation(self.formula.n_variables)

    def solve(self):
        for r in range(1, self.max_tries):
            self.interpretation = Interpretation(self.formula.n_variables)
            self.formula.populate_satisfied_clauses_arr(self.interpretation)
            for f in range(1, self.max_flips):
                # Mirar si hi ha una clausula que no satisfa la interpretacio
                unsatisfied_clause = self.formula.get_unsatisfied_clause(
                    self.interpretation)

                # Mirar si la interpretacio satisfa la formula
                if not unsatisfied_clause:
                    return self.interpretation

                # Per cada literal dins la clausula insatisfeta, en calculem el broken
                literal_min = None
                broken_min = 999999
                for literal in unsatisfied_clause:
                    broken = self.broken(literal)
                    if broken < broken_min:
                        broken_min = broken
                        literal_min = literal

                # Si el broken es mes gran que 0 i amb certa probabilitat, canviarem un literal aleaotoriament
                if broken_min > 0 and random.random() < self.w:
                    literal_to_flip = random.choice(unsatisfied_clause)
                else:
                    literal_to_flip = literal_min

                self.interpretation.flip(abs(literal_to_flip))
                self.formula.update_satisfied_clauses(
                    self.interpretation, literal_to_flip)
            # print("Max Flips reached " + str(r))
        return None

    def broken(self, literal):
        # Canviar variable i contar quantes clausules no satisfa
        new_interpretation = self.interpretation.copy()
        new_interpretation.flip(abs(literal))

        return self.formula.count_unsatisfied_clauses(new_interpretation, literal)


if __name__ == "__main__":
    filename = sys.argv[1]
    formula = Formula(filename)
    # print(str(formula))
    # test_interpretation = Interpretation()
    # test_interpretation.interpretation = [
    #     False, False, False, False, True, True, True, False, False, True]
    # print(formula.get_unsatisfied_clause(test_interpretation))
    model = WalkSat(formula)
    sol = model.solve()
    if sol:
        print(sol)
    else:
        print("UNSAT", file=sys.stderr)
