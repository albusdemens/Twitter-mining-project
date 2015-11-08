# -*- coding: utf-8 -*-
# This program parses a parenthesized list that describes the [MIME-IMB] body
# structure of an email message and returns the level in the nested list of all
# the plain text parts of the message with its charset.
# More info: http://tools.ietf.org/html/rfc3501#page-75

# Output:
# [['1', 'US-ASCII'], ['2', 'US-ASCII']]
# [['1.1.1', 'iso-8859-1'], ['1.1.2', 'utf-8'], ['1.2', 'ascii'], ['1.6.2', 'None'], ['3.1', 'iso-8859-1']]

# A two part message consisting of a text and a BASE64-encoded 
# text attachment can have a body structure of:
x = ([("TEXT", "PLAIN", ("CHARSET", "US-ASCII"), "NIL", "NIL", "7BIT", 1152, 23),
     ("TEXT", "PLAIN", ("CHARSET", "US-ASCII", "NAME", "cc.diff"),"<9@cac.ny.edu>", "Comp diff", "BASE64", 4554, 73) 
    ], "MIXED")

# A more complex structure
y=( [   ( # Level 1
            (# Level 1.1
                # Level 1.1.1
                ('TEXT', 'PLAIN', ('CHARSET', 'iso-8859-1'), None, None, 'QUOTED-PRINTABLE', 248, 10, None, None, None),
                # Level 1.1.2 
                ('TEXT', 'PLAIN', ('CHARSET', 'utf-8'), None, None, 'QUOTED-PRINTABLE', 248, 10, None, None, None),
                ('TEXT', 'HTML', ('CHARSET', 'iso-8859-1'), None, None, 'QUOTED-PRINTABLE', 3030, 73, None, None, None), 
                'ALTERNATIVE', 
                ('BOUNDARY', '------------Boundary-00=_3D8XBHK0000000000000'), 
                None, 
                None), 
            # Level 1.2
            ('TEXT', 'PLAIN', ('CHARSET', 'ascii'), None, None, 'QUOTED-PRINTABLE', 248, 10, None, None, None),
            # Level 1.3
            ('IMAGE', 'JPEG', ('NAME', '197870_c.jpg'), '<37460F6A-AB8A-41F7-90A5-8715ACB71386>', None, None, None),
            # Level 1.4
            'RELATED',
            # Level 1.5
            ('BOUNDARY', '------------Boundary-00=_3D8X6RO0000000000000','TYPE', 'multipart/alternative'), 
            # Level 1.6
            (   # Level 1.6.1
                ('BOUNDARY', '------------Boundary-00=_3D8X6RO0000000000000'),
                # Level 1.6.2
                ('TEXT', 'PLAIN', ('CHARSET', 'None'), None, None, 'QUOTED-PRINTABLE', 248, 10, None, None, None)
            ),None,None),
        # Level 2 
        ('TEXT', 'HTML', ('NAME', 'MAVICA.HTM'), None, None, 'BASE64', 11214, 145, None, ('ATTACHMENT', None), None), 
        # Level 3
        (   # Level 3.1
            ('TEXT', 'PLAIN', ('CHARSET', 'iso-8859-1'), None, None, 'QUOTED-PRINTABLE', 248, 10, None, None, None),
        ),
        ('IMAGE', 'JPEG', ('NAME', 'MVC-025S.JPG'), None, None, 'BASE64', 103446, None, ('ATTACHMENT', None), None)
    ], 'MIXED', ('BOUNDARY', '------------Boundary-00=_3D8XG6G0000000000000'), None, None)

def inspect_nested_list(lista,index,data,data_aux):
 
    def get_content_chartset(lista):
        for i in lista:
            if type(i)==type(()) and i[0]=='CHARSET':
                return i[1]
                
    def is_a_list(data):
        return type(data) == type(()) 
    
    cont = 1
    for i in lista:
        # i    i[0]
        # (    (   (),()   ),   ()   )
        if is_a_list(i) and is_a_list(i[0]):
            if index=='':
                data, data_aux = inspect_nested_list(i,str(cont)+'.'+str(1),data,data_aux)
            else:
                aux = index[:-1] + str(cont)
                data, data_aux = inspect_nested_list(i,aux+'.'+str(1),data,data_aux) 
            
            if len(index)==1:
                index = ''
        else:
            if is_a_list(i):
                # A final list (eg: ('TEXT', 'PLAIN', ('CHARSET')    
                if i[0]=='TEXT' and i[1]=='PLAIN':
                    #Found it!
                    data.append([index[:-1] + str(cont),get_content_chartset(i)])
                if i[0]=='TEXT' and i[1]=='HTML':
                    data_aux.append([index[:-1] + str(cont),get_content_chartset(i)])
        cont+=1
    return data, data_aux
    
# Testing X
data, data_aux = inspect_nested_list(x[0],'',[],[])
if len(data)==0:
    data =  data_aux
print data

# Testing Y
data, data_aux = inspect_nested_list(y[0],'',[],[])
if len(data)==0:
    data =  data_aux
print data
