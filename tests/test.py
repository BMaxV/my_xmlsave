from my_save import sxml_main
import unittest


class TestMySave:
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


if __name__ == "__main__":
    unittest.main()
