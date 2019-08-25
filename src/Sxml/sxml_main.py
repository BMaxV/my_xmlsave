
def data_crawl(lines,data,level=0):
    
    level_space=" "*level*2
    ls=level_space
    
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
            if type(key)!=str:
                raise TypeError
            lines.append(ls+"<"+key+">")
            data_crawl(lines,data[key],level+1)
            lines.append(ls+"</"+key+">")
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
        raise TypeError

def is_tag(string):
    string=string.strip()
    if "<" in string and ">" in string:
        if "</" in string:
            return string[2:-1],"end"
        else:
            return string[1:-1],"start"
    
    return False,False

def data_unpack(lines,end_tag=None,is_dict=False):
    start_stack=[]
    end_stack=[]
    
    #input()
    #tracks data based on index in tag list
    
    data=[]
    data_d={}
    c=0
    m=len(lines)
    while c < m:
        line=lines[c]
        
        tag = is_tag(line)
        
        #it's a tag
        if tag[0]:
            if tag[1]=="start":
                start_stack.append((tag[0],c))
                
                if tag[0] in ["tuple","list","dict"]:
                    #print("enter recursion")
                    datai,cx=data_unpack(lines[c+1:],tag[0])
                    #print("returned",datai)
                    if tag[0]=="tuple":
                        data.append(tuple(datai))
                    else:
                        data.append(datai)
                    c+=cx
                
                elif tag[0] in ["int","float","bool","str","none"]:
                    data_line=lines[c+1]
                    data_line=data_line.strip()
                    if tag[0]=="int":
                        data.append(int(data_line))
                    if tag[0]=="float":
                        data.append(float(data_line))
                    if tag[0]=="bool":
                        data.append(bool(data_line))
                    if tag[0]=="str":
                        data.append(data_line)
                    if tag[0]=="none":
                        print("YOOO")
                        data.append(None)
                    c+=1
                else:
                    #it's a dict key
                    datai,cx=data_unpack(lines[c+1:],tag[0],is_dict=True)
                    data_d[tag[0]]=datai
                    #print("data_d",data_d)      
                    c+=cx             
                    
            if tag[1]=="end":
                if tag[0]==end_tag:
                    #print("endtag",end_tag)
                    #print("ret1")
                    if end_tag=="dict":
                        return data_d,c
                    else:
                        if len(data)==1:
                            data=data[0]
                        return data,c                    
        
        c+=1
        continue
        
    if is_dict:
        #print("ret2")
        return data_d,c
    else:
        #print("ret3")
        return data,c
    
def write(fn,data):
    
    lines=[]
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<!DOCTYPE language>')
    
    data_crawl(lines,data)
    
    with open(fn,"w") as f:
        for line in lines:
            f.write(line+"\n")
        
    
    #I want to take either lists,tuples or
    #dicts
    
    #ok I want to write
    #string
    #int,float
    #bool
    #None?
        
def read(fn):
    with open(fn,"r") as f:
        lines=f.readlines()
    
    lines=lines[2:]
    data,c = data_unpack(lines)
    data=data[0]
    #print("end of read")
    #print(data)
    return data

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
     #d==d2
    
if __name__=="__main__":
    test()
    
