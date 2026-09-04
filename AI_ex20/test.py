# 對照AI範例用的空白練習檔案
# 只看題目在此區作答，不要看AI的答案

# AI_ex01:輸出字串
# 試著利用print函數在螢幕上輸出文字"Hello World"


print("Hello, World!")

print("Hello","World")

print("Hello"+"World")




# AI_ex02:變數指派
# 試著宣告兩個整數變數a和b，並分別指定值為10和20
# 將a和b相加的結果儲存到變數sum_ab中
# 印出sum_ab的值

a = 10
b = 20
sum_ab = a + b

print("a=",a,"b=",b,"加總=",sum_ab)
print(f"a={a}, b={b}, 加總={sum_ab}")


# AI_ex03:輸入與型別轉換
# 利用input函數輸入數值，並儲存到變數str_age中
# 將str_age轉換為整數並儲存到變數age中，再印出age的值

keyin_age = input("請輸入年齡：")
age = int(keyin_age)
print(f"你的年齡是{age}")

# AI_ex04:整數除法與求餘數
# 試著宣告一個整數變數，並分別使用 "//"、"%" 運算子計算其平方根的整數部分以及餘數
# 將結果分別儲存到 sqrt_ab 和 remainder 兩個變數中，並輸出其值

ex04_keyin_num = int(input("請輸入一個整數："))
ex04_sqrt_ab = ex04_keyin_num // 2
ex04_remainder = ex04_keyin_num % 2
print(f"平方根的整數部分為：{ex04_sqrt_ab}")
print(f"餘數為：{ex04_remainder}")

# AI_ex05:條件判斷 (if-elif-else)
# 提示入一個整數，再輸出判斷是奇數、偶數或0

ex05_keyin_num = int(input("請輸入一個整數："))
if ex05_keyin_num == 0:
    print("你輸入的是0")
elif ex05_keyin_num % 2 == 0:
    print("你輸入的是偶數")
else:
    print("你輸入的是奇數")


# AI_ex06:成績統計
# 提示輸入整數分數，分別為國文、英文、數學
# 分數範圍為0~100，若分數大於100或小於0，則輸出“輸入錯誤”
# 若輸入正確則輸出"總分"、"平均"、"最高分"、"最低分" 

# 輸入
ex06_score_chinese = int(input("請輸入國文分數："))
ex06_score_english = int(input("請輸入英文分數："))
ex06_score_math = int(input("請輸入數學分數："))

# 判斷是否輸入錯誤
if ex06_score_chinese > 100 or ex06_score_chinese < 0 or ex06_score_english > 100 or ex06_score_english < 0 or ex06_score_math > 100 or ex06_score_math < 0:
    print("輸入錯誤")
    

# 總分、平均、最高分、最低分
ex06_score_total = ex06_score_chinese + ex06_score_english + ex06_score_math
ex06_score_average = ex06_score_total / 3
ex06_score_max = max(ex06_score_chinese, ex06_score_english, ex06_score_math)
ex06_score_min = min(ex06_score_chinese, ex06_score_english, ex06_score_math)

# 輸出
print(f"總分：{ex06_score_total}")
print(f"平均：{ex06_score_average:.2}")
print(f"最高分：{ex06_score_max}")
print(f"最低分：{ex06_score_min}")


