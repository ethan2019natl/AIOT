from collections import deque
import time

class Dessert_store:
    def __init__(self, name):
        # 店名
        self.name = name
        # 甜點商品
        self.production_queue = deque()

    def add_order(self, dessert_name):
        # 操作物件屬性: self.屬性 => obj.屬性
        self.production_queue.append(dessert_name)
        print(f"新訂單: {dessert_name} 加入製作清單")   
        #  操作物件方法: self.方法() => obj.方法()
        self.show_queue()

    def make_dessert(self):
        if not self.production_queue:
            print("目前沒有訂單, 甜點師傅休息中...")
            return
        
        current_dessert = self.production_queue.popleft()
        print(f"甜點師傅正在製作{current_dessert}")

        time.sleep(1) #sec秒

        print(f"{current_dessert} 製作完成!客人取餐")
        self.show_queue()

    def show_queue(self):
        if self.production_queue:
            print(f"目前製作清單: {list(self.production_queue)}")
        else:
            print(f"目前製作清單空空如也!")

if __name__ == "__main__":
    my_shop = Dessert_store("幸福甜點屋")
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





