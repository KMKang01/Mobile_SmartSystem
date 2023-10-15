print('딕셔너리')
print('---------------------------')

dictionary = {'jmlee':88, 'kitae':98, 'ihjung':99}

print(dictionary)
print(dictionary.keys())
print(list(dictionary.keys()))

dictionary['ihjung']=dictionary['kitae']
print(dictionary)

print(dictionary.values())
print(list(dictionary.values()))

value = dictionary.get('hyhwang')
print(value)
