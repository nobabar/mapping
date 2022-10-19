import numpy as np


class sabwt():
    def __init__(self, s):
        self.s = np.array(list(s))
        self.stypes, self.stypes_substrings = self.suffix_types()

    def suffix_types(self):
        types = np.empty(len(self.s), dtype="|S2")
        types[-1] = "S"
        stypes_index = []
        i = len(self.s) - 2
        while i >= 0:
            if self.s[i] < self.s[i+1] or (self.s[i] == self.s[i+1] and types[i+1] == b"S"):
                types[i] = "S"
            else:
                types[i] = "L"
                if types[i+1] == b"S":
                    types[i+1] = "S*"
                    stypes_index.append(i+1)
            i -= 1
        stypes_index.sort()
        stypes_substrings = []
        for i in range(len(stypes_index) - 1):
            stypes_substrings.append(
                self.s[stypes_index[i]:(stypes_index[i+1] + 1)])
        return types, stypes_substrings

    def induce(self):
        for i in range(len(self.stypes_substrings)):
            u = reversed(self.stypes_substrings[i])
            c = u.pop()


if __name__ == "__main__":
    s = "mmississiippii$"
    b = sabwt(s)
    print(b.stypes)
    print(b.stypes_substrings)
