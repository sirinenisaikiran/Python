from userh import *
import pytest

class TestUser:
    def test_gold(self, amounts):
        u = GoldUser("Gold",  BankAccount(100))
        for am in amounts:
            u.transact(am)
        assert u.balance == 710

@pytest.mark.addl     
def test_normal(normal, amounts):   
    for am in amounts:
            normal.transact(am)
    assert normal.balance == 700

@pytest.mark.addl     
def test_silver(silver, amounts):   
    for am in amounts:
            silver.transact(am)
    assert silver.balance == 704