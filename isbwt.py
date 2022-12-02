import numpy as np


from memory_profiler import profile


class isbwt:
    def __init__(self, s):
        self.s = np.array(list(s))
        self.stypes = []
        self.LMS = []
        self.transformed = []

    def suffix_types(self):
        self.stypes = np.empty(len(self.s), dtype="|S1")
        self.stypes[-1] = "S"
        i = len(self.s) - 2
        while i >= 0:
            if self.s[i] < self.s[i + 1] or (
                self.s[i] == self.s[i + 1] and self.stypes[i + 1] == b"S"
            ):
                self.stypes[i] = "S"
            else:
                self.stypes[i] = "L"
                if self.stypes[i + 1] == b"S":
                    self.LMS.append(i + 1)
            i -= 1
        self.LMS.reverse()
        return self.stypes, self.LMS

    def get_suffixes(self):
        LMS_suffixes = []
        for i in range(len(self.LMS) - 1):
            LMS_suffixes.append(self.s[self.LMS[i] : (self.LMS[i + 1] + 1)])
        return LMS_suffixes

    def induce_LMS(self):
        alphabet, counter = np.unique(self.s, return_counts=True)

        SA = np.ones(len(self.s), dtype=int) * -1
        # place heads on the ends of buckets
        heads = np.cumsum(counter) - 1

        # place LMS suffixes in their buckets
        for LMS in self.LMS:
            # get head of letter's bucket
            i = alphabet == self.s[LMS]
            SA[heads[i][0]] = LMS
            # move head backwards
            heads[i] -= 1

        # place heads on the beginning of buckets
        heads = np.cumsum(counter) - counter

        # induce sort L-type LMS-prefixes
        for preffixe in SA:
            if preffixe > 0 and self.stypes[preffixe - 1] == b"L":
                i = alphabet == self.s[preffixe - 1]
                SA[heads[i][0]] = preffixe - 1
                # move head forwards
                heads[i] += 1

        # place heads on the ends of buckets
        heads = np.cumsum(counter) - 1

        # induce sort non-size-one LMS-prefixes
        for preffixe in reversed(SA):
            if preffixe > 0 and self.stypes[preffixe - 1] == b"S":
                i = alphabet == self.s[preffixe - 1]
                SA[heads[i][0]] = preffixe - 1
                # move head backwards
                heads[i] -= 1

        return SA

    @profile
    def transform(self):
        SA = self.induce_LMS()
        last_index = list(map(lambda i: (i + len(self.s) - 1) % len(self.s), SA))
        self.transformed = np.array(list(self.s))[last_index]
        return self.transformed


if __name__ == "__main__":
    s = "mmiissiissiippii$"
    b = isbwt(s)
