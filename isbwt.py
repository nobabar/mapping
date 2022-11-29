import numpy as np


class sabwt():
    def __init__(self, s):
        self.s = np.array(list(s))
        self.stypes, self.LMS, self.LMS_substrings = self.suffix_types()

    def suffix_types(self):
        types = np.empty(len(self.s), dtype="|S2")
        types[-1] = "S"
        LMS = []
        i = len(self.s) - 2
        while i >= 0:
            if self.s[i] < self.s[i+1] or (self.s[i] == self.s[i+1] and types[i+1] == b"S"):
                types[i] = "S"
            else:
                types[i] = "L"
                if types[i+1] == b"S":
                    LMS.append(i+1)
            i -= 1
        LMS.sort()
        LMS_substrings = []
        for i in range(len(LMS) - 1):
            LMS_substrings.append(
                self.s[LMS[i]:(LMS[i+1] + 1)])
        return types, LMS, LMS_substrings

    def induce(self):
        for i in range(len(self.LMS_substrings)):
            u = reversed(self.LMS_substrings[i])
            c = u.pop()


if __name__ == "__main__":
    s = "mmiissiissiippii$"
    b = sabwt(s)
    print(b.stypes)
    print(b.LMS)
    print(b.LMS_substrings)
