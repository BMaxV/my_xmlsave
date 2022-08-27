import random
import re

int_characters=re.compile("[0-9]*")

class Scope:
    def __init__(self,tag,start):
        self.tag=tag
        self.start=start
        self.end=None
        self.contents=[]
        
    def convert(self,lines,verbose=False,level=0):
        if verbose:
            print("entering verbose")
        data=[]
        if self.tag=="dict":
            data={}
        if verbose:
            print("weird?")
            print(self.contents)
            print(self.tag)
            
        if len(self.contents)!=0:
            if verbose:
                print("Hellooooo")
            for scope in self.contents:
                
                if verbose:
                    print(" "*level+"this convert1")
                    print(scope.start,scope.end)
                    if scope.end-scope.start < 1000:
                        print(lines[scope.start:scope.end])
                    
                r_data=scope.convert(lines,level=level+1,verbose=verbose)
                
                if verbose:
                    print(r_data)
                if self.tag=="dict":
                    thiskey=str(scope.tag)
                    match=int_characters.match(scope.tag)
                    print(scope.tag,len(scope.tag),match.string,match.endpos , match.start(),match.endpos - match.start())
                    if len(scope.tag) == match.span()[1]-match.span()[0]:
                        thiskey=int(thiskey)
                    data[thiskey]=r_data[0]
                    
                else:
                    data.append(r_data)
                        
        elif self.tag in ["int","float","bool","str","none"]:
            
            data_line=lines[self.start+1]
            data_line=data_line.strip()
            
            if verbose:
                print("is tagged, but no content?",data_line)
            if self.tag=="int":
                data=int(data_line)
            if self.tag=="float":
                data=float(data_line)
            if self.tag=="bool":
                data=bool(data_line)
            if self.tag=="str":
                data=data_line
            if self.tag=="none":
                data=None
        
        
        else:
            
            data={self.tag:lines[self.start:self.end]}
            if verbose:
                print("no contents?!")
                
        if self.tag=="tuple":
            data=tuple(data)
        
        if verbose:
            print("data in convert",data)
            
        if type(data)==list:
            if len(data)==0 and verbose:
                print("no data converted")
                raise
        return data
        

def data_crawl(lines,data,level=0):
    """insert
    data into lines
    """
    level_space=" "*level*2
    ls=level_space
    
    #this is a bit hacky.
    if "Vector" in type(data).__name__:
        data=tuple(data)
    
    if type(data)==tuple:
        
        lines.append(ls+"<tuple>")
        for el in data:
            data_crawl(lines,el,level+1)
        lines.append(ls+"</tuple>")
    
    elif type(data)==list:
        lines.append(ls+"<list>")
        for el in data:
            data_crawl(lines,el,level+1)
        lines.append(ls+"</list>")
    
    elif type(data)==dict:
        lines.append("<dict>")
        for key in data:
            
            #this assembles tags from data
            
            if type(key)==int:
                #convert ints to strings
                tagkey=str(key)
            elif type(key) not in [str]:
                #else raise a type error
                raise TypeError
            tagkey=str(key)
                
            lines.append(ls+"<"+tagkey+">")
            data_crawl(lines,data[key],level+1)
            lines.append(ls+"</"+tagkey+">")
        lines.append("</dict>")
    
    elif type(data)==int:
        lines.append(ls+"<int>")
        lines.append(ls+str(data))
        lines.append(ls+"</int>")
    
    elif type(data)==float:
        lines.append(ls+"<float>")
        lines.append(ls+str(data))
        lines.append(ls+"</float>")
    
    elif type(data)==str:
        lines.append(ls+"<str>")
        #make sure t
        data=data.replace("<","tagopen")
        data=data.replace("/>","tagclose")
        lines.append(ls+data)
        lines.append(ls+"</str>")
    
    elif type(data)==bool:
        lines.append(ls+"<bool>")
        lines.append(ls+str(data))
        lines.append(ls+"</bool>")
    elif data==None:
        lines.append(ls+"<none>")
        lines.append(ls+"None")
        lines.append(ls+"</none>")
    
    else:
        print("error")
        print("data type",type(data))
        print("data instance",data)
        raise TypeError

def is_tag(string):
    string=string.strip()
    
    if "<" in string and ">" in string:
        if "</" in string:
            return string[2:-1],"end"
        else:
            return string[1:-1],"start"
    
    return False,False

def tag_in_line(string):
    
    string=str(string)
    string=string.strip()
    elements=[]
    
    c=0
    while True:
        start=string.find("<")
        end=string.find(">")
        if start!=-1 and end!=-1:
            #there is a tag here.
            s1, tag = string[:start], string[start:end+1]
            elements.append(s1)
            elements.append(tag)
            string=str(string[end+1:])
            
        elif c==1000:
            break
        c+=1
    s2=string[end+1:]
    elements.append(s2)
    while "" in elements:
        elements.remove("")
    return elements


def data_unpack(lines, end_tag=None, is_dict=False, verbose=False):
    """recursively explore the data and convert to python dict or
    list"""
    
    #ok there is an issue. I think I am assuming there is a top level thing.
    #or that there is only one anyway
    
    local_id=random.random()
    start_stack=[]
    end_stack=[]
    
    #input()
    #tracks data based on index in tag list
    
    data=[]
    data_d={}
    c=0
    m=len(lines)
    tags=[]
    tag_stack=[]
    scopes_stack=[]
    
    if verbose:
        print("yo, verbose")
    
    while c < m:
        line=lines[c]
        
        if verbose and c%100==0:
            print(c,"/",m)
            #print(line)
            #input("ok?")
        #I'm assuming a tag per line,
        #that's not accurate.
        #if tag in line
        
        elements=tag_in_line(line)
        #split the line by the tag, put it back in the list.
        if len(elements)>1:
            lines=lines[:c]+elements+lines[c+1:]
            #if verbose:
                #print(lines)
                #input("ok?")
            m+=len(elements)-1
            continue
        c+=1
        
    if verbose:
        print("line iteration done")
        print("lines now",len(lines))
    current_scope=None
    c=0
    while c < m:
        if verbose and c%100==0:
            print(c,"/",m)
        line=lines[c]
        tag = is_tag(line)
        if tag[0]:
            if verbose:
                print("tag",tag)
            if tag[1]=="start":
                S=Scope(tag[0],c)
                scopes_stack.append(S)
                if current_scope!=None:
                    current_scope.contents.append(S)
                current_scope=S
            
            if tag[1]=="end":
                if tag[0]==current_scope.tag:
                    current_scope.end=c
                    scopes_stack.pop(-1)
                    if len(scopes_stack)>0:
                        current_scope=scopes_stack[-1]
                    else:
                        
                        #actually, it just breaks here.
                        #it needs to check if the current line was 
                        #the last line.
                        #if it is, I can just break.
                        #if it's not, I shouldn't do that.
                        #I should instead create a masterscope
                        #probably as list type.
                        if c == m -1 :
                            
                            break
                        else:
                            eh=Scope("list",None)
                            eh.contents.append(current_scope)
                            current_scope=eh
                            scopes_stack.insert(0,eh)
        c+=1
        
    if verbose:
        print("this section")
        
    if current_scope!=None:
        print("that convert2, verbose")
        print("start",current_scope.start)
        print("end",current_scope.end)
        ob=current_scope.convert(lines,verbose=verbose)
        if verbose:
            print("that convert2 output")
            for xl in ob:
                print(xl)
            print(ob,c)
        return ob,c
    else:
        if verbose:
            print("current scope is none?")

def sxml_append(fn,data,lines=None,mode="a"):
    if lines==None:
        lines=[]
    data_crawl(lines,data)
    
    with open(fn,mode) as f:
        for line in lines:
            f.write(line+"\n")
    
    
def write(fn,data):
    
    preamble_lines=[]
    preamble_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    preamble_lines.append('<!DOCTYPE language>')
    
    sxml_append(fn,data,lines=preamble_lines,mode="w")
    
    #I want to take either lists,tuples or
    #dicts
    
    #ok I want to write
    #string
    #int,float
    #bool
    #None?
        
def read(fn,verbose=False):
    with open(fn,"r") as f:
        lines=f.readlines()
    #why this?
    #lines=lines[2:]
    #while True:
    if "<?" in lines[0]:
        lines.pop(0)
    if "<!" in lines[0]:
        lines.pop(0)
    
    if verbose:
        print(lines[:100])
    #ok if there are multiple objects in the same file...
    #what do I do then?
    data,c = data_unpack(lines,verbose=verbose)
    
    if verbose:
        print("unpacked")
        print(data,c)
            
            
    try:
        #...why?
        if len(data)==1:
            data=data[0]
        
    except KeyError:
        pass
    
    return data


def pack(data):
    my_lines=[]
    data_crawl(my_lines,data)
    return "\n".join(my_lines)
    
def unpack(string):
    lines=string.split("\n")
    my_data_object=data_unpack(lines)
    my_data_object=my_data_object[0]
    return my_data_object

def test4():
    l=[[(1,2)],[(5,6),(7,8)],[(9,10),(11,12)]]
    d={"eh":l}
    
    my_string=pack(d)
    my_d=unpack(my_string)
    
    assert d==my_d
    print(d)
    print(my_d)
    print(d==my_d)
    
def test3():
    print("new test")
    print("")
    print("")
    l=[[(1,2)],[(5,6),(7,8)],[(9,10),(11,12)]]
    d={"eh":l}
    write("test2.xml",d)
    d2=read("test2.xml")
    
    print("in",d)
    print("out",d2)
    print(d==d2)
    assert d==d2

def test2():
    print("new test")
    print("")
    print("")
    l=[((1,2),(3,4)),((5,6),(7,8)),[(9,10),(11,12)]]
    d={"eh":l}
    write("test2.xml",d)
    d2=read("test2.xml")
    
    print("in",d)
    print("out",d2)
    print()
    
    assert d==d2

def test():
    d={"hello":1,
    "there":"obi wan",
    "nice":3.141,
    "eh":[1,2,3],
    "muh":(1,2,3),
    "bug":None,
    }
    print("in",d)
    write("test1.xml",d)
    d2=read("test1.xml")
    
    print("out",d2)
    print(d==d2)
    
    assert d==d2
    
    #s=json.dumps(d,indent=4)
    #with open("test.txt","w") as f:
    #    f.write(s)
     #d==d2
    
if __name__=="__main__":
    test4()
    
    #l=["hello",",","there"]
    #l2=["1","2","3"]
    
   # line_insert(l,1,l2)
