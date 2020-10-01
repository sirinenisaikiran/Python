import pytest 
from pkgex.MyInt import MyInt 

@pytest.fixture(scope="module")
def one(request):
    a = MyInt(1)
    yield a 
    print("shutdown here")
    
    
def pytest_addoption(parser):
    parser.addoption("--patch", action="store", type="int", default=1)
