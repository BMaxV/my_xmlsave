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
    
    
    def test_html_object_split(self):
        
        # so I'm assuming that the thing is split like this:
        # how beautiful soup would do it.
        # in emergencies I could also write something that would do it.
        # but I guess in reality, I would put a linebreak after 
        # every > and be done with it.
        
        s = """<p>
hello
    <a href="yo">
    that
    </a>
there
</p>

"""
        lines = s.split("\n")
        lines, m = sxml_main.tag_split(lines)
       
        current_scope, c = sxml_main.create_nested_scopes(lines, m)
        
        current_scope=current_scope.contents[0]
        # print("")
        # for mybool,line,level in sxml_main.scope_line_recursion(current_scope,lines):
            # if mybool:
                # print("    scoped"+" "*level+line)
            # else:
                # print("not scoped"+" "*level+line)
        s = """<p>
hello
<a href="yo">
that
</a>
there

<ul>
<div>
<li>
<a href="this">
lol
</a>
</li>
</div>
<li>
that
</li>
</ul>

<div>
aaay
<p>
lamo
</p>
is this working
<p>
he
</p>
thought
</div>

"""
        lines = s.split("\n")
        lines, m = sxml_main.tag_split(lines)
       
        current_scope, c = sxml_main.create_nested_scopes(lines, m)
        
        current_scope.end =len(lines)
        outputs =[]
        for my_tuple in sxml_main.scope_line_recursion(current_scope,lines):
            mybool,line,level = my_tuple
            #if mybool:
            #    print("    scoped"+"-"*level*2+line,level)
            #else:
            #    print("not scoped"+"-"*level*2+line,level)
            outputs.append(my_tuple)
        
        assert len(lines) == len(outputs)
        
        assert outputs[0]==outputs[0]
        assert outputs[8]==outputs[8]
        assert outputs[13]==outputs[13]
        assert outputs[25]==outputs[25]
        
        return
        p1,p2,p3 = r
        assert p1 == "hello"
        assert p2 == '<a href="yo">that</a>'
        assert p3 == "there"

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
    
def test_diskcache():
    import time
    import diskcache
    
    from diskcache import Cache
    
    my_data = sxml_main.read("my_test_file.xml")
    t0=time.time()
    cache = Cache()
    
    cache["hellotest"] = my_data
    my_data2 = cache["hellotest"]
    t1=time.time()
    print("diskcache test",t1-t0)
    assert my_data == my_data2

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
def test_single():
    mytest=TestMySave()
    mytest.test_html_object_split()

if __name__ == "__main__":
    unittest.main()
    #test_single()
    #test_diskcache()
    #test_pickle()
