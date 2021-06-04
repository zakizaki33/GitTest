import time
time.sleep(1)
print("foo")
print("bar")
print("ふがふが")
time.sleep(1)


# selfの理解を進める
# https://www.sejuku.net/blog/64106
class className():
    # pass  # Do nothing.
    # initialize
    strC = "YamaYama"  # クラス変数

    def __init__(self1):
        print(self1.strC)   # インスタンス変数strCの誕生
        self1.strC = "TakaTaka"
        print(self1.strC)
        strC = "123456"     # クラス変数の書き換え
        print(self1.strC)   # インスタンス変数の書き換えが優先される
        print(strC)


instance = className()
