import math
import random

def sig(a):
    return 1/(1+math.exp(-a))

class Dendrit():
    def __init__(self, Neuron):
        self.weight = random.randint(-1000000000, 1000000000)/100000000
        self.attachedAxon = Neuron.axon
    def act(self):
        return self.weight*self.attachedAxon
    def load(self, data):
        self.weight = float(data)
    def save(self):
        return str(self.weight)

class Neuron():
    def __init__(self, PrevLayer = -1):
        if PrevLayer == -1:
            self.dendrites = -1
        else:
            self.dendrites = []
            for i in PrevLayer.neurons:
                self.dendrites.append(Dendrit(i))
        self.shift = random.randint(-1000000000, 1000000000)/100000000
        self.axon = 0
    def act(self):
        if self.dendrites == -1:
            self.axon = self.axon
        else:
            tmp = self.shift
            for i in self.dendrites:
                tmp += i.act()
            self.axon = sig(tmp)
    def load(self, data):
        tmp = data.split(' ')
        for i in range(0, len(tmp)-1):
            self.dendrites[i].load(tmp[i])
        self.shift = float(tmp[len(tmp)-1])
    def save(self):
        tmp = ""
        for i in self.dendrites:
            tmp += i.save()+" "
        tmp += str(self.shift)
        return tmp

class Layer():
    def __init__(self, size = 1, PrevLayer = -1):
        self.neurons = []
        for i in range(0, size):
            self.neurons.append(Neuron(PrevLayer))
    def act(self):
        for i in self.neurons:
            i.act()
    def load(self, data):
        tmp = data.split(',')
        for i in range(0, len(tmp)-1):
            if tmp[i] != '':
                self.neurons[i].load(tmp[i])
    def save(self):
        txt = ""
        for i in self.neurons:
            txt += i.save()+","
        return txt

class InLayer(Layer):
    def __init__(self, InFunc):
        super().__init__(size = InFunc(-1))
        self.inFunc = InFunc
    def act(self, data):
        tmp = self.inFunc(data)
        for i in range(0, self.inFunc(-1)):
            self.neurons[i].axon = tmp[i]

class MidLayer(Layer):
    def __init__(self, Size, prevLayer):
        super().__init__(size = Size, PrevLayer = prevLayer)
    def act(self):
        super().act()
    def load(self, data):
        super().load(data)
    def save(self):
        return super().save()

class OutLayer(Layer):
    def __init__(self, prevLayer, OutFunc):
        super().__init__(size = OutFunc(-1), PrevLayer = prevLayer)
        self.outFunc = OutFunc
    def act(self):
        super().act()
        tmp = []
        for i in self.neurons:
            tmp.append(i.axon)
        return self.outFunc(tmp)
    def load(self, data):
        super().load(data)
    def save(self):
        return super().save()

class Brain():
    def __init__(self, owner, dataBase, InFunc, MidFunc, OutFunc):
        self.owner = owner
        self.data = []
        self.data.append(self.owner)
        for i in dataBase:
            if i != self.owner:
                self.data.append(i)
        self.In = InLayer(InFunc)
        self.Mid = []
        self.Mid.append(MidLayer(MidFunc(0), self.In))
        for i in range(1, MidFunc(-1)):
            self.Mid.append(MidLayer(MidFunc(i), self.Mid[i-1]))
        self.Out = OutLayer(self.Mid[MidFunc(-1)-1], OutFunc)
        self.res = -1
    def act(self):
        self.In.act(self.data)
        for i in self.Mid:
            i.act()
        self.res = self.Out.act()
    def load(self, data):
        tmp = data.split(sep=';')
        for i in range(0, len(tmp)-1):
            self.Mid[i].load(tmp[i])
        self.Out.load(tmp[len(tmp)-1])
    def save(self):
        txt = ""
        for i in self.Mid:
            txt += i.save()+";"
        txt += self.Out.save()
        return txt
    def show(self):
        for i in self.In.neurons:
            print(i.axon, end=' ')
        print(';')
        for i in self.Mid:
            for j in i.neurons:
                print(j.axon, end=' ')
            print(';')
        for i in self.Out.neurons:
            print(i.axon, end=' ')
        print(';')
        print(self.res, end=' ')
        print(';')





if __name__ == '__main__':
    def inF(a):
        if a == -1:
            return 5
        else:
            return [1, 2, 3, 4, 5]
    
    def midF(a):
        tmp = [8, 10, 8]
        if a == -1:
            return 3
        else:
            return tmp[a]
    
    def outF(a):
        if a == -1:
            return 3
        else:
            tmp = []
            for i in a:
                if i > 0.5:
                    tmp.append(1)
                else:
                    tmp.append(0)
            return tmp
    
    B = Brain(1, [1], inF, midF, outF)
    f = open("brainTest.txt", "r")
    for i in f:
        B.load(i)
    f.close()
    
#    f = open("brainTest1.txt", "w")
#    f.write(B.save()+"\n")
#    f.close()
    
    B.show()
    print()
    n=1
    for i in range(0, n):
        B.act()
    B.show()
        

