from pkgex.MyInt import MyInt 
import pytest 


class TestMyInt:
    def test_add(self):
        """testing add"""
        a = MyInt(2)
        b = MyInt(3)
        assert a+b == MyInt(5)
        
#pytest -v -m addl test_myint.py
@pytest.mark.addl 
def test_sub(one):
    """Testing sub"""
    a = MyInt(2)
    assert a-one == MyInt(1)
    

def process(a,op,b):
    if op == '+': return a+b 
    if op == '==': return a == b 
    if op == '-' : return a - b 
    
#pytest -v -k "sub" test_myint.py
#pytest -v -k "not sub" test_myint.py
#pytest -v -k "sub and Test" test_myint.py
#pytest -v -k "sub or add" test_myint.py
#pytest --collect-only  test_myint.py
#pytest -v test_myint.py::test_sub
@pytest.mark.parametrize("a,op,b,op2,result",[
    (MyInt(1) , '+' ,MyInt(2), '==', MyInt(3)),
    pytest.param(MyInt(2),'-',MyInt(1),'==',MyInt(1), marks=pytest.mark.addl),
    ],
    ids=["Testing add2", "Testing sub2"]
)
def testMany(a,op,b,op2,result):
    assert process(process(a,op,b),op2,result)
    
    
#pytest -v -s test_myint.py --patch 0  #check conftest.py for actual handling 
#0 for no patch, 1 for patch 

import pkgex.MyInt 
def test_monkey(request, monkeypatch):
    def MyInt(n):
        print("Patching...")
        return 2*n 
    if request.config.getoption("--patch"):
        monkeypatch.setattr(pkgex.MyInt, "MyInt", MyInt)
    a = pkgex.MyInt.MyInt(1)
    assert a+a == pkgex.MyInt.MyInt(2)
    
