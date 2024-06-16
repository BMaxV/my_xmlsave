import re
int_characters = re.compile("[0-9]*")

class Scope:
    def __init__(self,tag,start):
        self.tag=tag
        self.start=start
        self.end=None
        self.contents=[]
        
    def convert(self,lines,level=0):
        
        data=[]
        if self.tag=="dict":
            data={}
            
        if len(self.contents)!=0:
            for scope in self.contents:
                
                r_data=scope.convert(lines,level=level+1)
                
                if self.tag=="dict":
                    thiskey=str(scope.tag)
                    match=int_characters.match(scope.tag)
                    if len(scope.tag) == match.span()[1]-match.span()[0]:
                        thiskey=int(thiskey)
                    data[thiskey]=r_data[0]
                    
                else:
                    data.append(r_data)
                        
        elif self.tag in ["int","float","bool","str","none"]:
            data_line, data = self.convert_simple_data_line(lines)
            
        else:
            data = {self.tag: lines[self.start:self.end]}
            
        if self.tag == "tuple":
            data = tuple(data)

        if type(data) == list:
            if len(data) == 0:
                print("no data converted")
                raise
        return data

    def convert_simple_data_line(self, lines):
        data_line = lines[self.start+1]
        data_line = data_line.strip()

        if self.tag == "int":
            data = int(data_line)

        elif self.tag == "float":
            data = float(data_line)

        elif self.tag == "bool":
            if data_line == "True":
                data = True
            elif data_line == "False":
                data = False

        elif self.tag == "str":
            data = data_line

        elif self.tag == "none":
            data = None
        return data_line, data 


def data_crawl(lines, data, level=0):
    """insert
    data into lines
    """
    level_space = " "*level*2
    ls = level_space

    # this is a bit hacky.
    if "Vector" in type(data).__name__:
        data = tuple(data)

    if type(data) == tuple:
        lines.append(ls+"<tuple>")
        for el in data:
            data_crawl(lines, el, level+1)
        lines.append(ls+"</tuple>")

    elif type(data) == list:
        lines.append(ls+"<list>")
        for el in data:
            data_crawl(lines, el, level+1)
        lines.append(ls+"</list>")

    elif type(data) == dict:
        lines.append("<dict>")
        for key in data:

            # this assembles tags from data

            if type(key) == int:
                # convert ints to strings
                tagkey = str(key)
            elif type(key) not in [str]:
                # else raise a type error
                raise TypeError
            tagkey = str(key)

            lines.append(ls+"<"+tagkey+">")
            data_crawl(lines, data[key], level+1)
            lines.append(ls+"</"+tagkey+">")
        lines.append("</dict>")

    elif type(data) == int:
        lines.append(ls+"<int>")
        lines.append(ls+str(data))
        lines.append(ls+"</int>")

    elif type(data) == float:
        lines.append(ls+"<float>")
        lines.append(ls+str(data))
        lines.append(ls+"</float>")

    elif type(data) == str:
        lines.append(ls+"<str>")
        data = data.replace("<", "tagopen")
        data = data.replace("/>", "tagclose")
        lines.append(ls+data)
        lines.append(ls+"</str>")

    elif type(data) == bool:
        lines.append(ls+"<bool>")
        lines.append(ls+str(data))
        lines.append(ls+"</bool>")
        
    elif data == None:
        lines.append(ls+"<none>")
        lines.append(ls+"None")
        lines.append(ls+"</none>")

    else:
        print("error")
        print("data type", type(data))
        print("data instance", data)
        raise TypeError


def is_tag(string):
    string = string.strip()

    if "<" in string and ">" in string:
        if "</" in string:
            return string[2:-1], "end"
        else:
            return string[1:-1], "start"

    return False, False


def tag_in_line(string):

    string = str(string)
    string = string.strip()
    elements = []

    c = 0
    while True:
        start = string.find("<")
        end = string.find(">")
        if start != -1 and end != -1:
            # there is a tag here.
            s1, tag = string[:start], string[start:end+1]
            elements.append(s1)
            elements.append(tag)
            string = str(string[end+1:])

        elif c == 1000:
            break
        c += 1
    s2 = string[end+1:]
    elements.append(s2)
    while "" in elements:
        elements.remove("")
    return elements


def data_unpack(lines, end_tag=None, is_dict=False):
    """
    explore the data and convert to python dict or list
    """

    data = []
    scopes_stack = []
    c = 0
    m = len(lines)
    while c < m:
        line = lines[c]

        # I'm assuming a tag per line,
        # that's not accurate.
        # if tag in line

        elements = tag_in_line(line)
        # split the line by the tag, put it back in the list.
        if len(elements) > 1:
            lines = lines[:c]+elements+lines[c+1:]
            
            m += len(elements)-1
            continue
        c += 1

    current_scope = None
    c = 0
    while c < m:
        line = lines[c]
        tag = is_tag(line)
        
        if tag[0]:
            handle_start(tag,scopes_stack,current_scope,c)
            handle_end(tag,current_scope,scopes_stack,c)
            
            if c == m - 1:
                break
            
            current_scope = get_current_scope(scopes_stack,current_scope)
        
        c += 1

    if current_scope != None:
        ob = current_scope.convert(lines)
        return ob, c

def get_current_scope(scopes_stack,current_scope):

    if len(scopes_stack) > 0:
        current_scope = scopes_stack[-1]
    else:

        # actually, it just breaks here.
        # it needs to check if the current line was
        # the last line.
        # if it is, I can just break.
        # if it's not, I shouldn't do that.
        # I should instead create a masterscope
        # probably as list type.
        
        new_scope = Scope("list", None)
        new_scope.contents.append(current_scope)
        current_scope = new_scope
        scopes_stack.insert(0, new_scope)
    return current_scope

def handle_start(tag,scopes_stack,current_scope,c):
    if tag[1] == "start":
        S = Scope(tag[0], c)
        scopes_stack.append(S)
        if current_scope != None:
            current_scope.contents.append(S)
    
def handle_end(tag,current_scope,scopes_stack,c):
    if tag[1] == "end":
        if tag[0] == current_scope.tag:
            current_scope.end = c
            scopes_stack.pop(-1)

def sxml_append(fn, data, lines=None, mode="a"):
    if lines == None:
        lines = []
    data_crawl(lines, data)

    with open(fn, mode) as f:
        for line in lines:
            f.write(line+"\n")

def write(fn, data):

    preamble_lines = []
    preamble_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    preamble_lines.append('<!DOCTYPE language>')

    sxml_append(fn, data, lines=preamble_lines, mode="w")

def read(fn):
    with open(fn, "r") as f:
        lines = f.readlines()
    
    if "<?" in lines[0]:
        lines.pop(0)
    if "<!" in lines[0]:
        lines.pop(0)

    data, c = data_unpack(lines)

    try:
        if len(data) == 1:
            data = data[0]

    except KeyError:
        pass

    return data

def pack(data):
    my_lines = []
    data_crawl(my_lines, data)
    return "\n".join(my_lines)


def unpack(string):
    lines = string.split("\n")
    my_data_object = data_unpack(lines)
    my_data_object = my_data_object[0]
    return my_data_object

