from userh import * 
import pytest 

@pytest.fixture(scope='module')
def silver(request):
    a = SilverUser("Gold",  BankAccount(100))
    yield a
    print("shutdown code")
  
@pytest.fixture(scope='module')
def amounts(request):
    a = [ 100, -200, 300, -400, 400]
    yield a

@pytest.fixture(scope='module')
def normal(request):
    a = NormalUser("Gold",  BankAccount(100))
    yield a