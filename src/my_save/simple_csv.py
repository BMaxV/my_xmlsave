

def my_writer(fn, input_dict):
    headers = []
    for key in input_dict:
        headers = list(input_dict[key].keys())
        break

    s = ";"+";".join(headers) + "\n"
    for key in input_dict:
        my_list = []

        for subkey in headers:
            my_list.append(str(input_dict[key][subkey]))
       
        line = f"{key};"+";".join(my_list)+"\n"
        s += line
    with open(fn, "w") as f:
        f.write(s)


def my_reader(fn):
    with open(fn, "r") as f:
        t = f.read()
    my_dict = {}
    t = t.split("\n")
    headers = t.pop(0)

    headers = headers.split(";")
    headers = headers[1:]
    my_dict = {}
    for line in t:
        line = line.split(";")
        name = line[0]
        if name == "":
            break
        line = line[1:]
        my_dict[name] = {}
        c = 0
        m = len(headers)
        if len(line) == 0:
            break
        while c < m:
            # do I assume these are numbers?
            try:
                my_dict[name][headers[c]] = float(line[c])
            except:
                my_dict[name][headers[c]] = line[c]
            c += 1
    return my_dict


def test():
    my_dict = {"jack": {"age": 25, "fav color": "blue"},
               "bob": {"age": 60, "fav color": "red"}, }

    fn = "justtestthis.csv"
    my_writer(fn, my_dict)

    my_dict2 = my_reader(fn)
    
    print(my_dict)
    print(my_dict2)
    
    assert my_dict == my_dict2

    my_dict2 = my_reader("moa.csv")
    print(my_dict2)
if __name__ == "__main__":
    test()
