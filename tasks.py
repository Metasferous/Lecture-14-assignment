"""
 1. Create a class Product with properties
 name, price, and quantity.

 Create a child class Book that inherits from Product
 and adds a property author
 and a method called read that prints information about the book.
"""


class Product:
    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity


class Book(Product):
    def __init__(self, name: str, price: float, quantity: int, author: str):
        super().__init__(name, price, quantity)
        self.author = author

    def read(self):
        print(f'Book : {self.name}',
              f'\nWritten by : {self.author}',
              f'\nPrice : {self.price}',
              f'\n{self.quantity} unit(s) in stock')


book = Book('I see you`re into darkness', 490., 42, 'Illarion Pavliuk')

book.read()

print('\n\n')

"""
 2. Create a class Restaurant with properties
 name, cuisine, and menu.

 The menu property should be a dictionary
 with keys being the dish name
 and values being the price.

 Create a child class FastFood that inherits from Restaurant
 and adds
 a property drive_thru
 (a boolean indicating whether the restaurant has a drive-thru or not)

 and a method called order which takes in the dish name and quantity
 and returns the total cost of the order.

 The method should also update the menu dictionary
 to subtract the ordered quantity from the available quantity.

 If the dish is not available
 or if the requested quantity is greater than the available quantity,
 the method should return
 a message indicating that the order cannot be fulfilled.

 Example of usage:
 class Restaurant:
    # your code here
    pass

 class FastFood(Restaurant):
    # your code here
    pass

 menu =  {
    'burger': {'price': 5, 'quantity': 10},
    'pizza': {'price': 10, 'quantity': 20},
    'drink': {'price': 1, 'quantity': 15}
 }

 mc = FastFood('McDonalds', 'Fast Food', menu, True)

 print(mc.order('burger', 5)) # 25
 print(mc.order('burger', 15)) # Requested quantity not available
 print(mc.order('soup', 5)) # Dish not available
"""


class Restauraunt:
    def __init__(self, name: str, cuisine: str, menu: dict):
        self.name = name
        self.cuisine = cuisine
        self.menu = menu


class FastFood(Restauraunt):
    def __init__(self, name: str, cuisine: str, menu: dict, drive_thru: bool):
        super().__init__(name, cuisine, menu)
        self.drive_thru = drive_thru

    def order(self, dish_name: str, quantity: int):
        if dish_name not in self.menu:
            raise KeyError('No such item in menu')
        else:
            if self.menu[dish_name]['quantity'] < quantity:
                raise ValueError(f'Insufficient amount of item(s) in stock: {self.menu[dish_name]["quantity"]}')
            else:
                self.menu[dish_name]['quantity'] -= quantity
                return self.menu[dish_name]['price'] * quantity


menu = {
    'burger': {'price': 5, 'quantity': 10},
    'pizza': {'price': 10, 'quantity': 20},
    'drink': {'price': 1, 'quantity': 15}
 }

mc = FastFood('McDonalds', 'Fast Food', menu, True)

try:
    print(mc.order('burger', 5))  # 25
except Exception as err:
    print(err)

try:
    print(mc.order('burger', 15))  # Requested quantity not available
except Exception as err:
    print(err)

try:
    print(mc.order('soup', 5))  # Dish not available
except Exception as err:
    print(err)

print('\n\n')


"""
 3. (Optional) A Bank
    a) Using the Account class as a base class,
    write two derived classes called SavingsAccount and CurrentAccount.

    A SavingsAccount object,
    in addition to the attributes of an Account object,
    should have an interest attribute
    and a method which adds interest to the account.

    A CurrentAccount object,
    in addition to the attributes of an Account object,
    should have an overdraft limit attribute.

    b) Now create a Bank class,
    an object of which contains an array of Account objects.

    Accounts in the array could be instances of the Account class,
    the SavingsAccount class, or the CurrentAccount class.

    Create some test accounts (some of each type).

    c) Write an update method in the Bank class.
    It iterates through each account,
    updating it in the following ways:

    Savings accounts get interest added
    (via the method you already wrote);

    CurrentAccounts get a letter sent if they are in overdraft.
    (use print to 'send' the letter).

    d)The Bank class requires methods for
    opening
    and closing accounts,
    and for paying a dividend into each account.
"""


class Account:
    def __init__(self, balance, account_number):
        self._balance = balance
        self._account_number = account_number

    @classmethod
    def create_account(cls, account_number):
        return cls(0.0, account_number)

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
        else:
            raise ValueError('Amount must be positive')

    def withdraw(self, amount):
        if amount > 0:
            self._balance -= amount
        else:
            raise ValueError('Amount must be positive')

    def get_balance(self):
        return self._balance

    def get_account_number(self):
        return self._account_number

    def __str__(self):
        return f'Account number: {self._account_number}, balance: {self._balance}'


class SavingsAccount(Account):
    def __init__(self, balance, account_number, interest: float):
        super().__init__(balance, account_number)
        self.interest = interest

    def add_interest(self):
        self._balance += self._balance * self.interest

    @classmethod
    def create_account(cls, account_number):
        return cls(0.0, account_number, 0.02)


class CurrentAccount(Account):
    def __init__(self, balance, account_number, overdraft_limit):
        super().__init__(balance, account_number)
        self._overdraft_limit = overdraft_limit

    @classmethod
    def create_account(cls, account_number):
        return cls(0.0, account_number, 0.)

    def get_limit(self):
        return self._overdraft_limit


ACCOUNT_TYPES = {'account': Account, 'savings': SavingsAccount, 'current': CurrentAccount}


class Bank:
    def __init__(self, accounts: list[Account]):
        self._accounts = accounts

    def update(self):
        for acc in self._accounts:
            if isinstance(acc, SavingsAccount):
                acc.add_interest()
            elif isinstance(acc, CurrentAccount):
                if acc._balance < 0:
                    print(f'Account {acc.get_account_number()} is in overdraft by ' +
                          f'{-acc.get_balance()}, ' +
                          f'remaining limit is {acc.get_limit() + acc.get_balance()}')

    def open_account(self, account_type: str, account_number):
        account_type = account_type.lower()
        if account_type in ACCOUNT_TYPES:
            if account_number not in self.get_account_numbers():
                self._accounts.append(ACCOUNT_TYPES[account_type].create_account(account_number))
            else:
                raise ValueError('Given account number is already used')
        else:
            raise KeyError('Non-existing account type')

    def get_account_numbers(self):
        return {acc.get_account_number() for acc in self._accounts}

    def close_account(self, account_number):
        acc = [acc for acc in self._accounts if acc.get_account_number() == account_number]
        self._accounts.remove(*acc)

    def pay_dividends(self, amount):
        for acc in self._accounts:
            acc.deposit(amount)


try:
    acc_1 = Account(500., 1)
    acc_2 = Account.create_account(2)
    s_acc_1 = SavingsAccount(100., 3, 0.05)
    s_acc_2 = SavingsAccount.create_account(4)
    c_acc_1 = CurrentAccount(-10., 5, 3000.)
    c_acc_2 = CurrentAccount.create_account(6)

    bank = Bank([acc_1, acc_2, s_acc_1, s_acc_2, c_acc_1, c_acc_2])

    for acc in bank._accounts:
        print(acc)
    print('\n')

    bank.update()

    bank.open_account('savings', 8)

    for acc in bank._accounts:
        print(acc)
    print('\n')

    bank.close_account(8)

    for acc in bank._accounts:
        print(acc)
    print('\n')

    bank.pay_dividends(200.)

    for acc in bank._accounts:
        print(acc)
    print('\n')

    bank.update()
except Exception as err:
    print(err)
