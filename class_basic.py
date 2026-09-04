class Phone:
    def __init__(self, color):
        # 定義屬性
        self.size = "6.2\""
        self.brand = "apple"
        self.os = "ios"
        self.color = color

    def call(self, phone_num):
        print(f"dial : {phone_num}")

    def send_text(self, msg):
        print(f"send: {msg}")

    def play_music(self, music):
        print(f"play: {music}")


# 產生真實的手機物件
myPhone = Phone(color="white")
print(myPhone)

print(f"myPhone.color: {myPhone.color}")
print(f"myPhone.size: {myPhone.size}")
myPhone.play_music("生日快樂")