class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def eat(self):
        print(f"{self.name} is eating!")

    def sleep(self):
        print(f"{self.name} is sleeping!")


class Chiken(Animal):
    def __init__(self, name, age, color):
        # 初始化父類的屬性
        super().__init__(name, age)
        # 初始化自己的屬性
        self.color = color

    def lay_egg(self):
        print(f"{self.name} is laying an egg!")

    def sleep(self):
        print(f"{self.name} is sleeping with 咖咖咖 的聲音!")

class Rabbit(Animal):
    def __init__(self, name, age, weight):
        # 初始化父類的屬性
        super().__init__(name, age)
        # 初始化自己的屬性
        self.weight = weight

    def jump(self):
        print(f"{self.name} is jump!")

c1 = Chiken('chicken', 2, "white")
c1.eat()
c1.sleep()
print(c1.name)

c1 = Rabbit('Rabbit', 2, 10)
c1.sleep()

