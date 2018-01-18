bri = set(['brazil', 'russia', 'india'])
print('india' in bri)
print('usa' in bri)
bric = bri.copy()
bric.add('china')
print(bric.issuperset(bri))
bri.remove('russia')
print(bri & bric)

print('simple assignment')
shoplist = ['apple', 'mange', 'carrot', 'banana']
mylist = shoplist

del shoplist[0]

print('shoplist is', shoplist)
print('mylist is', mylist)

print('copy by making a full slice')

mylist = shoplist[:]

del mylist[0]

print('shoplist is', shoplist)
print('mylist is', mylist)