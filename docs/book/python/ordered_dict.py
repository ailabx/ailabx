dict1 = {}
dict1['a'] = 'a'
dict1['c'] = 'c'
dict1['b'] = 'b'
print(dict1)

dict2 = {}
dict2['a'] = 'a'
dict2['b'] = 'b'
dict2['c'] = 'c'
print(dict2)
print(dict2 == dict1)


from collections import OrderedDict
dict_ordered1= OrderedDict()
dict_ordered1['a'] = 'a'
dict_ordered1['c'] = 'c'
dict_ordered1['b'] = 'b'
print(dict_ordered1)

dict_ordered2= OrderedDict()
dict_ordered2['a'] = 'a'
dict_ordered2['b'] = 'b'
dict_ordered2['c'] = 'c'
print(dict_ordered2)

print(dict_ordered1 == dict_ordered2)