import rules as rules
import polyline as polyline

# a = rules.Rules("sample/GRADA3.rul")
# a.parse()
# print(a)

p = polyline.Polyline("sample/GRADA3.dxf")
p.parse()
print(p)