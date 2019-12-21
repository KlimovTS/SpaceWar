import StarshipBrain
import game



POPULATION_SIZE = 10
PUBLIC_STATS_LEN = 232
PRIVATE_STATS_LEN = 232



def intRescale(start, end, number, sections):
    tmp = start - end
    tmp = tmp / sections
    tmp = tmp * number
    tmp = tmp + end
    return game.rounding(tmp)

# конвертер базы данных во вход нейросети
def InFunc(a):
        if a == -1:
            global POPULATION_SIZE, PUBLIC_STATS_LEN, PRIVATE_STATS_LEN
            inputSize = (POPULATION_SIZE-1) * PUBLIC_STATS_LEN + PRIVATE_STATS_LEN
            return inputSize
        else:
            inputList = []
            for i in a:
                if i == a[0]:
                    inputList.extend(i.privateStats())
                else:
                    inputList.extend(i.publicStats())
            return inputList

# кол-во слоёв и их размеры - готово
def MidFunc(a):
    tmp = [2*InFunc(-1), 2*InFunc(-1), 2*InFunc(-1), InFunc(-1), intRescale(InFunc(-1), OutFunc(-1), 1, 4), intRescale(InFunc(-1), OutFunc(-1), 2, 4), intRescale(InFunc(-1), OutFunc(-1), 3, 4)]
    if a == -1:
        return len(tmp)
    else:
        return tmp[a]

# конвертер из нейросети на управление
def OutFunc(a):
    if a == -1:
        return 5
    else:
        tmp = []
        for i in a:
            if i > 0.5:
                tmp.append(1)
            else:
                tmp.append(0)
        return tmp

class SmartStarship():
    def __init__(self, starship, starships):
        self.starship = starship
        self.brain = StarshipBrain.Brain(self.starship, starships, InFunc, MidFunc, OutFunc)
    def tick(self):
        self.brain.act()
        if self.brain.res[0]:
            self.starship.pressW()
        else:
            self.starship.releaseW()
        if self.brain.res[1]:
            self.starship.pressA()
        else:
            self.starship.releaseA()
        if self.brain.res[2]:
            self.starship.pressS()
        else:
            self.starship.releaseS()
        if self.brain.res[3]:
            self.starship.pressD()
        else:
            self.starship.releaseD()
        if self.brain.res[4]:
            self.starship.pressSpace()
        else:
            self.starship.releaseSpace()
