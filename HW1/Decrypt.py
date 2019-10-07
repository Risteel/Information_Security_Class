import sys


class Decrypt:
    @staticmethod
    def caesar(key, text):
        k = 26 - int(key) #shift
        # ord(ch) -> get char's ascii code
        # ord(t) - ord('A') -> let the value of 't' in [0, 25]
        # + k -> shift k
        # % 26 -> let the value in [0, 25]
        # chr(value + ord('A')) -> move value to ascii code of uppercase and convert to char
        return ''.join([chr((ord(t) - ord('A') + k) % 26 + ord('A')) for t in text]).lower()

    @staticmethod
    def playfair(key, text):
        def inSameRow(a, b):
            """
            Check a and b in Same Row
            """
            return a // 5 == b // 5

        def inSameCol(a, b):
            """
            Check a and b in Same Column
            """
            return a % 5 == b % 5

        def deRow(a, b):
            """
            Decrypt a and b
            """
            return [a + (4 if a % 5 == 0 else -1), b + (4 if b % 5 == 0 else -1)]

        def deCol(a, b):
            """
            Decrypt a and b
            """
            return [a + (20 if a // 5 == 0 else -5), b + (20 if b // 5 == 0 else -5)]

        def deRect(a, b):
            """
            Decrypt a and b
            """
            return [a // 5 * 5 + b % 5, b // 5 * 5 + a % 5]
        key = key.upper()
        # make table
        alphabet = [chr(i + ord('A')) for i in range(26)]
        sub = ('J', 'I')
        alphabet.remove(sub[0])
        uniqueKey = dict.fromkeys(alphabet, -1)
        key_id = 0
        for k in key:
            if k == sub[0]:
                k = sub[1]
            if uniqueKey[k] == -1:
                uniqueKey[k] = key_id
                key_id += 1
        for k in alphabet:
            if uniqueKey[k] == -1:
                uniqueKey[k] = key_id
                key_id += 1
        uniqueId = {}
        for k, v in uniqueKey.items():
            uniqueId[v] = k
        result = ''
        for i in range(0, len(text), 2):
            t1, t2 = text[i:i+2]
            id1 = uniqueKey[t1]
            id2 = uniqueKey[t2]
            if inSameRow(id1, id2):
                id1, id2 = deRow(id1, id2)
            elif inSameCol(id1, id2):
                id1, id2 = deCol(id1, id2)
            else:
                id1, id2 = deRect(id1, id2)
            result += uniqueId[id1] + uniqueId[id2]
        return result.lower()

    @staticmethod
    def vernam(key, text):
        text = text.upper()
        key = key.upper()
        r = ''
        for k, v in enumerate(text):
            ch = chr(((ord(v) - ord('A')) ^ (ord(key[k]) - ord('A'))) + ord('A'))
            key += ch
            r += ch
        return r.lower()

    @staticmethod
    def row(key, text):
        # char buffer
        t = [''] * len(text)
        # key and value map
        d = {}
        # rows count
        r = len(text) // len(key) + (0 if len(text) % len(key) == 0 else 1)
        # make map
        for i, j in enumerate(key):
            d[int(j)] = i
        # text index
        tid = 0
        for k in sorted(d.keys()):
            for i in range(r):
                # place position
                v = len(key) * i + d[k]
                # overflow
                if v >= len(text):
                    break
                t[v] = text[tid]
                tid += 1
        return ''.join(t).lower()

    @staticmethod
    def rail_fence(key, text):
        key = int(key)
        r = [''] * len(text)
        step = []
        # m -> move distance
        m, st, t = key * 2 - 2, 0, 0
        for d in range(m, -1, -2):
            # d -> move down distance
            # u -> move up distance
            # v -> plaintext char position
            u, v = m - d, st
            while v < len(text):
                if d != 0:
                    r[v] = text[t]
                    t += 1
                    v += d
                if v < len(text) and u != 0:
                    r[v] = text[t]
                    t += 1
                    v += u
            st += 1
        return ''.join(r).lower()
        

method = sys.argv[1]
key = sys.argv[2]
cipher = sys.argv[3]
sys.stdout.write(getattr(Decrypt, method)(key, cipher))
