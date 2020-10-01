from abc import ABCMeta, abstractmethod

class UserException(Exception):
    pass
		
class BankAccount:
    def __init__(self, initAmount=100):
        self.amount = initAmount
    def transact(self, amount):
        if (self.amount + amount <0):
            raise UserException("Not possible")
        self.amount =  self.amount + amount
    def balance(self):  #can get 
        return self.amount


class User(metaclass=ABCMeta):
    how_many_users = 0
    def __init__(self, name, account):
        self.name = name
        self.account = account
        User.how_many_users += 1
    @abstractmethod
    def getCashbackPercentage(self):
        pass
    @classmethod 
    def getCountOfUsers(cls):
        return cls.how_many_users
    def transact(self, amount):
        try:
            self.account.transact(amount)
            #give cashback 
            if amount < 0: #ie debit
                cashback = self.getCashbackPercentage() * abs(amount)
                self.account.transact(cashback)                
        except UserException as e:
            print(str(e), "Name:", self.name, " amount:", amount )
    def __str__(self):
        return "%s with balance %d" % (self.name, self.account.balance())
	#Property notation
    def p_get(self):
        return self.account.balance()
    def p_set(self, val):
        pass
    def p_del(self):
        pass	
    balance = property(p_get, p_set, p_del, None)   #instance.prop


	
class GoldUser(User):
    def getCashbackPercentage(self):
        return 0.05 #5%		

class NormalUser(User):
    def getCashbackPercentage(self):
        return 0.00 		

class SilverUser(User):
    def getCashbackPercentage(self):
        return 0.02 		



if __name__ == '__main__':		
    users = [GoldUser("Gold",  BankAccount(100)),
            NormalUser("Normal",  BankAccount(100)),
            SilverUser("Silver",  BankAccount(100))]            
    for u in users:
        for am in [ 100, -200, 300, -400, 400]:
            u.transact(am)
        print(u)
    print(User.getCountOfUsers())