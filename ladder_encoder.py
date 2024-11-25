class LadderEncoder:
    def __init__(self, n: int, width: int):
        self.n = n
        self.width = width
        self.clause = []
        self.number_of_var = n
        self.aux_var = {}

    def __get_axu_var(self, first: int, last: int) -> int:

        if first == last:
            return first

        temp = [i for i in range(first, last + 1)]
        group = tuple(temp)

        if group in self.aux_var:
            return self.aux_var[group]

        self.aux_var[group] = self.number_of_var + 1
        self.number_of_var += 1
        return self.aux_var[group]

    def __generate_window(self, window: int) -> list:
        clauses = []
        if window == 0:
            middle = (window + 1) * self.width

            # First half
            for i in range(middle - 1, middle - self.width + 1, -1):
                aux = self.__get_axu_var(i, middle)
                clauses.append([aux, -self.__get_axu_var(i + 1, middle)])
                clauses.append([aux, -i])
                clauses.append([-i, -self.__get_axu_var(i + 1, middle)])
                clauses.append([i, self.__get_axu_var(i + 1, middle), -aux])

            # Second half
            for i in range(middle + 2, middle + self.width):
                aux = self.__get_axu_var(middle + 1, i)
                clauses.append([aux, -self.__get_axu_var(middle + 1, i - 1)])
                clauses.append([aux, -i])
                clauses.append([-i, -self.__get_axu_var(middle + 1, i - 1)])
                clauses.append([i, self.__get_axu_var(middle + 1, i - 1), - aux])

            for i in range(1, self.width):
                clauses.append(
                    [-self.__get_axu_var(window * self.width + 1 + i, middle),
                     -self.__get_axu_var(middle + 1, middle + i)])

            clauses.append([-(window * self.width + 1), -self.__get_axu_var(window * self.width + 2, middle)])
            clauses.append([-(window * self.width + 1 + 2 * self.width - 1),
                            -self.__get_axu_var(middle + 1, middle + self.width - 1)])

        else:
            middle = (window + 1) * self.width
            # First half
            for i in range(middle - 1, middle - self.width + 1, -1):
                aux = self.__get_axu_var(i, middle)
                clauses.append([aux, -self.__get_axu_var(i + 1, middle)])
                clauses.append([aux, -i])
                clauses.append([i, self.__get_axu_var(i + 1, middle), -aux])

            # Second half
            for i in range(middle + 2, middle + self.width):
                aux = self.__get_axu_var(middle + 1, i)
                clauses.append([aux, -self.__get_axu_var(middle + 1, i - 1)])
                clauses.append([aux, -i])
                clauses.append([-i, -self.__get_axu_var(middle + 1, i - 1)])
                clauses.append([i, self.__get_axu_var(middle + 1, i - 1), - aux])

            for i in range(1, self.width):
                clauses.append(
                    [-self.__get_axu_var(window * self.width + 1 + i, middle),
                     -self.__get_axu_var(middle + 1, middle + i)])

            clauses.append([-(window * self.width + 1 + 2 * self.width - 1),
                            -self.__get_axu_var(middle + 1, middle + self.width - 1)])

        return clauses

    def generate_clause(self) -> list:
        clauses = []
        for window in range(self.n // self.width - 1):
            clauses.extend(self.__generate_window(window))

        return clauses


encoder = LadderEncoder(1000*4, 4)

clauses = encoder.generate_clause()

print(clauses)
print(len(clauses))
print(encoder.number_of_var)