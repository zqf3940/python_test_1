# coding = UTF-8

class Robot:
    population = 0
    def __init__(self,name):
        self.name = name
        print("(initializing {})".format(self.name))
        Robot.population += 1

    def die(self):
        print("{} is being destroyed!".format(self.name))

        Robot.population -= 1

        if Robot.population == 0:
            print("{} was the last one.".format(self.name))
        else:
            print("there are still{:d} robots working.".format(Robot.population))

    def say_hi(self):
        print("greetings, my masters call me {}".format(self.name))

    @classmethod
    def how_many(cls):
        print("we have {:d} robots.".format(cls.population))

droid1 = Robot("R2-D2")
droid1.say_hi()
Robot.how_many()

droid2 = Robot("C-3Po")
droid2.say_hi()
Robot.how_many()

print("\nRobot can do some work here.\n")
print("Robote have finished their work. so let's destroy them.")

droid1.die()
droid2.die()

Robot.how_many()