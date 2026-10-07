from abc import ABC, abstractmethod


class Pet(ABC):

    @abstractmethod
    def express(self):
        pass

    @abstractmethod
    def getName(self):
        pass

    @abstractmethod
    def getAge(self):
        pass

    @abstractmethod
    def getAgeInHumanYears(self):
        pass

class Animal(Pet):

    def __init__(self, name, age):
        self._name = name
        self._age = age

    def happyBirthday(self):
        self._age += 1

    @abstractmethod
    def express(self):
        pass

    @abstractmethod
    def getAgeInHumanYears(self):
        pass

    def getName(self):
        return self._name

    def getAge(self):
        return self._age

class Parrot(Animal):

    def __init__(self, name, age):
        super().__init__(name, age)

    def getAgeInHumanYears(self):
        return self.getAge() * 5

    def express(self):
        print(f'{self.getName()}: "Hello!"')
        print(r"""
   \
   (o>
\\_//)
 \_/_)
  _|_
""")

class Turtle(Animal):

    def __init__(self, name, age):
        super().__init__(name, age)

    def getAgeInHumanYears(self):
        if self.getAge() <= 0:
            return 0

        return 15 + (self.getAge() - 1) * 2

    def express(self):
        print(r"""
  _____     ____
 /      \  |  o |
|        |/ ___\|
|_________/
|_|_| |_|_|
""")

class Person:

    def __init__(self, name, pet=None):
        self._name = name
        self._pet = pet

    def setPet(self, pet):
        self._pet = pet

    def getPetInfo(self):
        print("--------------------")

        if self._pet is None:
            print(f"{self._name} has no pet yet")
            print("--------------------")
            return

        print(f"Pet for {self._name} is named {self._pet.getName()}")
        print(
            f"Age: {self._pet.getAge()} year(s), "
            f"about {self._pet.getAgeInHumanYears()} human years"
        )
        print("And it expresses itself like this:")

        self._pet.express()

        print("--------------------")

if __name__ == "__main__":

    kesha = Parrot("Kesha", 2)
    zavala = Turtle("Zavala", 4)

    kesha.happyBirthday()

    jack = Person("Jack", kesha)
    john = Person("John")

    jack.getPetInfo()
    john.getPetInfo()

    john.setPet(zavala)
    john.getPetInfo()

