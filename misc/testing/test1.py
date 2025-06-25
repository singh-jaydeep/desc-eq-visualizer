from dataclasses import dataclass, field

@dataclass
class test_class:
    attr1 = [1,2]
    attr2 = [3,4]
    attr3 = [attr1, attr2]



p = test_class()
print(p.attr3)
