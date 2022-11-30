import numpy as np


class isbwt():
    def __init__(self, s):
        self.s = np.array(list(s))
        self.alphabet, self.counter = np.unique(self.s, return_counts=True)
        self.stypes, self.LMS = self.suffix_types()
        self.SA = self.induce_LMS()

    def suffix_types(self):
        types = np.empty(len(self.s), dtype="|S1")
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
        LMS.reverse()
        return types, LMS

    def get_suffixes(self):
        LMS_suffixes = []
        for i in range(len(self.LMS) - 1):
            LMS_suffixes.append(
                self.s[self.LMS[i]:(self.LMS[i+1] + 1)])
        return LMS_suffixes

    def induce_LMS(self):
        SA = np.ones(len(self.s), dtype=int) * -1
        # place heads on the ends of buckets
        heads = np.cumsum(self.counter) - 1

        # place LMS suffixes in their buckets
        for LMS in self.LMS:
            # get head of letter's bucket
            i = self.alphabet == self.s[LMS]
            SA[heads[i][0]] = LMS
            # move head backwards
            heads[i] -= 1

        # place heads on the beginning of buckets
        heads = np.cumsum(self.counter) - self.counter

        # induce sort L-type LMS-prefixes
        for preffixe in SA:
            if preffixe > 0 and self.stypes[preffixe-1] == b"L":
                i = self.alphabet == self.s[preffixe-1]
                SA[heads[i][0]] = preffixe - 1
                # move head forwards
                heads[i] += 1

        # place heads on the ends of buckets
        heads = np.cumsum(self.counter) - 1

        # induce sort non-size-one LMS-prefixes
        for preffixe in reversed(SA):
            if preffixe > 0 and self.stypes[preffixe-1] == b"S":
                i = self.alphabet == self.s[preffixe-1]
                SA[heads[i][0]] = preffixe - 1
                # move head backwards
                heads[i] -= 1

        return SA


if __name__ == "__main__":
    s = "mmiissiissiippii$"
    b = isbwt(s)
    print(b.stypes)
    print(b.LMS)
    print(b.get_suffixes())
    print(b.SA)
