# AI練習03：輸入與型別轉換
# 利用input函數輸入數值，並儲存到變數str_age中
# 將str_age轉換為整數並儲存到變數age中，再印出age的值

keyin_age = input("請輸入年齡: ")
age = int(keyin_age)
print(f"你的年齡是: {age}")

#str_age = input("請輸入年齡：")
#print(f"你的年齡是：{str_age}")


# 實作小練習：成績計算機
# 請利用 input() 讓使用者輸入「數學分數」和「英文分數」
# 假設分數都是整數，請將輸入的文字轉型成 int
# 最後計算總分與平均，並用 print() 印出來
# 例如：
# 輸入：數學: 90
# 輸入：英文: 80
# 輸出：總分: 170, 平均: 85.0

score_math = input("請輸入數學分數: ")
score_english = input("請輸入英文分數: ")
score_total = int(score_math) + int(score_english)
score_average = score_total / 2
print(f"數學成績: {score_math}，英文成績: {score_english}，總分: {score_total}，平均: {score_average}")
