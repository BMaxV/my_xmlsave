from Sxml import sxml_main

def test_dict_int_keys():
    d={1:"hello"}#"1":"hello"}
    sxml_main.write("int_dict_key.xml",d)
    new_d=sxml_main.read("int_dict_key.xml")
    
    assert d == new_d

def test_all():
    sxml_main.test()
    sxml_main.test2()
    sxml_main.test3()
    

if __name__=="__main__":
    test_all()
    #test_dict_int_keys()
