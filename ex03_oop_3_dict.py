# 115.08.03 練習 oop (物件導向程式設計)
# 物件功能的操作-dictionary-字典 (由key和value組成的集合)

d = {'name':"peter","age":10,"email":"peter@sdf.com"}
# 讀取資料
print(d['name'])
print(d.get('name'))
# 新增資料
d['phoem'] = "0980123456"
d.setdefault('blood','B')
print(d)

#移除
del d['blood']
print(d)

# 新增多筆資料
d1 = {'height':160, 'weight':65}
d.update(d1)
print(d)

d2 = {**d, **d1}
print(d2)

d["hight"] = 200
d3 = d1 | d | d2  # |符號(or)可以用來合併dict，注意key值不能重複，若有相同值會覆蓋前值
print(f"d3={d3}")

#取所有鍵值
print(d.keys())

# 取所有變數值
print(d.values())

# 取所有鍵和值 (通常會拿來 for 迴圈使用)
print(d.items())
print(list(d.items()))    #前面加上list()可以轉成list模式


