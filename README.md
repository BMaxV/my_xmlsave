# my_xmlsave

Save and load simple data types to xml/string and back.

added some new functions to make this usable for just raw strings:

```
from my_save import sxml_main
l = [[(1,2)],[(5,6),(7,8)],[(9,10),(11,12)]]
d = {"eh":l}

my_string = sxml_main.pack(d)
my_d = sxml_main.unpack(my_string)

assert d == my_d

>>>True
```

Is it necessary? I don't know. I haven't found another package
that successfully converts types back and forth.

Json has an issue with strings and numbers I think.

This works for me and for now.
