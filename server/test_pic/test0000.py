# L = []
# print(id(L))
import sys
def fun1(s=''):
    print(id(s))
    s = 'test'
    print(s)
    print(id(s))

def test(c1):
    print(id(c1))
    c1.update_test()
    print(c1.a)
    print(id(c1))
#不可变实参　是局部变量
class A():
    def __init__(self,a,b):
        self.a = a
        self.b = b
    def update_test(self):
        self.a = 1
a = 1
# print(id(a))
fun1(a)
print(id(a))
#可变和不可变的定义：数据发生改变后地址是否发生改变　地址发生改变为不可变类型　地址不发生改变是可变类型　这都是针对数据本身而不是变量名而言
#数据本身就有
#变量名只是对数据的引用 贴上标签　这就是python内存管理　引用计数　
#可变实参 是全局变量　相当于在程序开始定义了一个列表　总共有两个列表 相当于其实形参也实例化　改变的是实参的值和形参没有关系

def fun(s,l=[]):
    print("实参１",id(l))
    l.append(s)
    print(l)
    print("实参２",id(l))
fun('a')


L =[1,2,3]
print("实参L：",id(L))
fun('b',L)
print("实参L：",id(L))
fun('c')

print(id(L))
obj = A('a','b')
print(id(obj))
print(obj.a)
test(obj)
print(obj.a)
print(sys.getrefcount([1,2,3]))