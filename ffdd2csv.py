import struct
import datetime
import pickle
import csv

EPOCH = datetime.datetime(1903, 12, 31, 20, 0, 0)

class FileParser:

    def __init__(self, fname):
        self.f = open(fname, "rb")

    def close(self):
        self.f.close()

    def get_int(self):
        n = struct.unpack(">I", self.read(4))[0]
        return n

    def get_double(self):
        n = struct.unpack(">d", self.read(8))[0]
        return n

    def get_string(self, n):
        s = self.read(n).decode("utf-8")
        return s

    def get_n_floats(self, n):
        s = struct.unpack(">"+"f"*n, self.read(n*4))
        return list(s)

    def get_n_ints(self, n):
        s = struct.unpack(">"+"I"*n, self.read(n*4))
        return list(s)
    
    def skip(self, n):
        self.read(n)

    def read(self, n):
        res = self.f.read(n)
        if res == b'':
            raise EOFError
        return res
            

    def parse_content(self):
        data = []
        while True:
            try:
                anim_data = self.parse_animal()
            except EOFError:
                self.close()
                break
            data.append(anim_data)
        return data

    def parse_animal(self):
        len_animal = self.get_int()
        i1 = self.get_int()
        i2 = self.get_int()
        dtime = self.get_double()
        time = EPOCH + datetime.timedelta(0, dtime)
        i3 = self.get_int()
        name = self.get_string(self.get_int())
        l_content = self.get_int()
        n_trunk = self.get_int()
        l_trunk = self.get_int()
        if n_trunk == 3:
            timestamp = self.get_n_floats(l_trunk)
            stimuli = [int(x) for x in self.get_n_floats(l_trunk)]
            data = self.get_n_floats(l_trunk)
            n_left = self.get_int()
            self.get_n_ints(n_left)
            if timestamp[0] == -1.:
                timestamp=timestamp[1:]
                ref = data[0]
                data = data[1:]
                stimuli = stimuli[1:]
            else:
                ref = 0
            return {"name": name,
                    "time": time,
                    "timestamp": timestamp,
                    "stimuli": stimuli,
                    "reference": ref,
                    "motion_index": data}
        else:
            raise Exception("Unexpected trunk number: {}".format(n_trunk))


def export_csv(data, fname):
    with open(fname, "w") as outf:
        fo = csv.writer(outf)
        fo.writerow(["Name", data["name"]])
        fo.writerow(["Time", data["time"]])
        fo.writerow(["Reference", data["reference"]])
        fo.writerow([])
        fo.writerow([])
        title = ["Timestamp", "Stimuli", "Motion_Index"]
        fo.writerow(title)
        for l in zip(*[data[t.lower()] for t in title]):
            fo.writerow(l)
    


if __name__ == "__main__":
    import sys
    import os
    fi = sys.argv[1]
    fo = sys.argv[2]
    p = FileParser(fi)
    res = p.parse_content()
    if fo[-4:] == ".pkl":
        pickle.dump(res, open(fo, "wb"))
    elif os.path.isdir(fo):
        for i, d in enumerate(res):
            fname = os.path.join(fo, "{}.csv".format(i))
            export_csv(d, fname)
    
    else:
        raise Exception("Unknown export format")
        



