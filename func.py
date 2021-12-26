def my_func():
    print("Foo")


my_other_func = lambda: print("Bar")

my_arr = [my_func, my_other_func]

for i in range (0, 2):
    my_arr[i]()

# Bots Position
BOT_POS = [(5401, 1530),(3686, 1857),(3733, 2626),(2325, 1814),
           (1718, 1282),(1288, 2418),(1249, 506),(2513,1286)
           ]
print("\n")
for (x,y) in BOT_POS:
    print(x, y)
