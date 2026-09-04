import my_package.str_tool
import my_package.math.math_tool

my_package.str_tool.split()
print(my_package.math.math_tool.PI)
my_package.math.math_tool.sub()

from my_package import str_tool, math

str_tool.split()
math.math_tool.sub()

from my_package.math.math_tool import PI
from my_package.str_tool import split

split()
print(PI)