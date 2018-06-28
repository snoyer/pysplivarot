import pysplivarot
a = pysplivarot.parse_svgd('M0,0 V2 H2 V0 z')
b = pysplivarot.parse_svgd('M1,1 V3 H3 V1 z')
print(pysplivarot.format_svgd(a + b)) # c = a union b
print(pysplivarot.format_svgd(a - b)) # d = a minus b
print(pysplivarot.format_svgd(a * b)) # d = a inter b
#  _____       _____       _____
# |a  __|__   |c    |__   |d  __|   __
# |__|__| b|  |___     |  |__|     |e_|
#    |_____|      |____|
#
