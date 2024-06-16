from my_save import sxml_main
import unittest


class TestMySave(unittest.TestCase):
    def test4(self):
        l = [[(1, 2)], [(5, 6), (7, 8)], [(9, 10), (11, 12)]]
        d = {"eh": l}

        my_string = sxml_main.pack(d)
        my_d = sxml_main.unpack(my_string)

        assert d == my_d

    def test3(self):
        l = [[(1, 2)], [(5, 6), (7, 8)], [(9, 10), (11, 12)]]
        d = {"eh": l}
        sxml_main.write("test2.xml", d)
        d2 = sxml_main.read("test2.xml")

        assert d == d2

    def test2(self):
        l = [((1, 2), (3, 4)), ((5, 6), (7, 8)), [(9, 10), (11, 12)]]
        d = {"eh": l}
        sxml_main.write("test2.xml", d)
        d2 = sxml_main.read("test2.xml")

        assert d == d2

    def test(self):
        d = {"hello": 1,
             "there": "obi wan",
             "nice": 3.141,
             "eh": [1, 2, 3],
             "muh": (1, 2, 3),
             "bug": None,
             }
        sxml_main.write("test1.xml", d)
        d2 = sxml_main.read("test1.xml")

        assert d == d2

    def test_dict_int_keys(self):
        d = {1: "hello"}  # "1":"hello"}
        sxml_main.write("int_dict_key.xml", d)
        new_d = sxml_main.read("int_dict_key.xml")

        assert d == new_d
    def test_dict_int_keys(self):
        d = {"questtasks":[
                ("WalkTask", ((0,-2,0),) , ),          # this can coincide with the location I purposefully place some stuff at.
                ("GetTask", ("Axe",)     , ), 
                ("WalkTask", ((-3,3,0),) ,  ), 
                ("HarvestTask",("Wood",) , ),
                ("WalkTask", ((0,-3,0),) ,  ), 
                ("GetTask", ("Tent",),      ),             
                ("PlaceBlueprintTask",("Tent",),    {"vuid":True} ),   # set a thing for a virtual uid, create one from the task or plan step or whatever, and save it.
                ("PlaceBlueprintTask",("campfire",),{"vuid":True} ),# then reference it later.
                ("BuildTask",("Tent",),{"vuid":True} ),
                ("BuildTask",("campfire",),{"vuid":True} ),  # "1":"hello"}
            ]}
        sxml_main.write("quests.xml", d)
        new_d = sxml_main.read("quests.xml")

        assert d == new_d


def test_benchmark():
    import time
    
    t0=time.time()
    d=sxml_main.read("my_test_file.xml")
    sxml_main.write("test_bench_big.xml", d)
    t1=time.time()
    print("me",t1-t0)

def test_pickle():
    import time
    import pickle
    
    d=sxml_main.read("my_test_file.xml")
    t0=time.time()
    with open("pickletest.db","ab") as f:
        pickle.dump(d,f)
    with open("pickletest.db","rb") as f:
        my_data = pickle.load(f)
    t1=time.time()
    print("pickle test",t1-t0)
    assert my_data == d

def test_pandas1():
    import time
    import pandas as pd

    d=sxml_main.read("my_test_file.xml")
    t0=time.time()
    df = pd.DataFrame.from_dict(d)
    df.to_csv("this_test.csv")
    my_data = pd.read_csv("this_test.csv")
    my_data = my_data.to_dict()
    t1=time.time()
    assert my_data == d
    print("pandas csv",t1-t0)


if __name__ == "__main__":
    unittest.main()
    test_pickle()
    test_benchmark()
