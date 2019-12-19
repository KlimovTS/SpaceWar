import tkinter

def KeyboardKeys():
    keys = []
    for i in range(48, 58):
        keys.append(chr(i))
    for i in range(97, 123):
        keys.append(chr(i))
#    anotherKeys = ['-', '=', '[', ']', ';', '\'', '\\', ',', '.', '/', 'space']
    anotherKeys = ['space', 'Up', 'Down', 'Right', 'Left']
    for i in anotherKeys:
        keys.append(i)
    return keys

def Null():
    return -1

class Keyboard():
    def __init__(self, root):
        for i in KeyboardKeys():
            self.key=1
            text = 'self.key'+i+'=0'
            exec(text)
        for i in KeyboardKeys():
            txt1='root.bind(\'<KeyPress-'+i+'>\', self.press'+i+')'
            txt2='root.bind(\'<KeyRelease-'+i+'>\', self.release'+i+')'
            exec(txt1)
            exec(txt2)
    for i in KeyboardKeys():
        txt1='def press'+i+'(self, a):\n self.key'+i+'=1'
        txt2='def release'+i+'(self, a):\n self.key'+i+'=0'
        exec(txt1)
        exec(txt2)
    def show(self):
        s = []
        for i in KeyboardKeys():
            txt = 's.append((i+\'=\'+str(self.key'+i+')))'
            exec(txt)
        print(s)

if __name__=='__main__':
    root = tkinter.Tk()
    width = 800
    heigth = 600
    WH =  str(width)+'x'+str(heigth)
    root.geometry(WH)
    a = Keyboard(root)
    tkinter.mainloop()
    a.show()