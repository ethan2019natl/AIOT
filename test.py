import dessert_store
from dessert_store import Dessert_store

# my_shop = dessert_store.Dessert_store("法式甜點屋")
my_shop = Dessert_store("法式甜點屋")
print(my_shop.name)

my_shop.add_order("草莓蛋糕")
my_shop.add_order("巧克力千層")
my_shop.add_order("焦糖烤布雷")

my_shop.make_dessert()
my_shop.make_dessert()

my_shop.add_order("焦糖烤布雷")

my_shop.make_dessert()
my_shop.make_dessert()
my_shop.make_dessert()