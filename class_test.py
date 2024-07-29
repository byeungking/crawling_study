class Person:
    def __init__(self, name, adress, phone, pay):
        self.name = name
        self.adress = adress
        self.phone = phone
        self.pay = pay

    def raise_pay(self):
        self.pay = self.pay*(1+0.1)
        return self.pay

if __name__ == "__main__":
    person = Person('john','서울시','010-1111-2222', 3000)
    print(person.raise_pay())
    print(person.pay)

