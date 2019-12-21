import MyKeyboard
import tkinter
import math
import random



def F1(a):
    return a*a

def mstr(a):
    a=a*100
    b=int(a)
    if (a-b)>=0.5:
        b=b+1
    b=b/100
    return str(b)

def movePoly(points, dx, dy):
    P = []
    for i in points:
        P.append((i[0]+dx, i[1]+dy))
    return P

def rotate(p, a, x, y):
    P = []
    sin = math.sin(a)
    cos = math.cos(a)
    for i in p:
        tmpx=i[0]-x
        tmpy=i[1]-y
        P.append((cos*tmpx+sin*tmpy+x, -sin*tmpx+cos*tmpy+y))
    return P

def rounding(a):
    if a-int(a)>=0.5:
        return int(a)+1
    else:
        return int(a)

def colorRGB(r, g, b):
  return "#%02X%02X%02X" % (rounding(r), rounding(g), rounding(b))

class Circle():
    def __init__(self, x, y, r, c):
        self.x = x
        self.y = y
        self.r = r
        self.c = c
    def draw(self):
        canv.create_oval(self.x+self.r, self.y+self.r, self.x-self.r, self.y-self.r, fill = self.c, width=0)

def getAngle(dx, dy):
    if dx<0:
        targetAngle=math.atan((-dy)/(max(dx, 0.000000001, key=abs)))+math.pi
    else:
        targetAngle=math.atan((-dy)/(max(dx, 0.000000001, key=abs)))
    return targetAngle

class Bullet():
    def __init__(self, owner):
        global idCounter
        self.id = idCounter
        idCounter += 1
        self.owner = owner
        self.time = 2000
        self.circle = Circle(owner.owner.x+rotate([self.owner.position], self.owner.owner.angle, 0, 0)[0][0]*self.owner.owner.extraSize, owner.owner.y+rotate([self.owner.position], self.owner.owner.angle, 0, 0)[0][1]*self.owner.owner.extraSize, owner.bulletRadius*self.owner.owner.extraSize, colorRGB(self.owner.owner.color[0], self.owner.owner.color[1], self.owner.owner.color[2]))
        n=1000000000
        tmp3 = random.randint(-owner.bulletSpeedY*n, owner.bulletSpeedY*n)/n
        tmp4 = random.randint(0, n)/n
        tmp = math.cos(tmp4*2*math.pi)*tmp3
        tmp2 = math.sin(tmp4*2*math.pi)*tmp3
        self.vx = (math.cos(owner.position[2]+owner.owner.angle)*(owner.bulletSpeedX+tmp2)+math.sin(owner.position[2]+owner.owner.angle)*tmp)*self.owner.owner.extraSize+self.owner.owner.vx
        self.vy = (-math.sin(owner.position[2]+owner.owner.angle)*(owner.bulletSpeedX+tmp2)+math.cos(owner.position[2]+owner.owner.angle)*tmp)*self.owner.owner.extraSize+self.owner.owner.vy
    def move(self):
        global width, heigth
        self.circle.x+=self.vx
        self.circle.y+=self.vy
        if self.circle.x>width-1:
            self.circle.x=0
        if self.circle.x<0:
            self.circle.x=width-1
        if self.circle.y>heigth-1:
            self.circle.y=0
        if self.circle.y<0:
            self.circle.y=heigth-1
    def draw(self):
        self.circle.draw()
    def outside(self):
        global width, heigth
        n = -50
        if self.circle.x<0+n or self.circle.x>width-n or self.circle.y<0+n or self.circle.y>heigth-n:
            return True
        else:
            return False
    def checkHit(self, st2):
        if (self.circle.x-st2.x)**2+(self.circle.y-st2.y)**2<=(self.circle.r+st2.collisionR*st2.extraSize)**2:
            return True
        else:
            return False

class Gun():
    def __init__(self, owner, position):
        global idCounter
        self.id = idCounter
        idCounter += 1
        self.owner = owner
        self.position = position
        self.name = 'Simple Gun'
        self.ReloadingTime = 125*1
        self.Reloading = 0
        self.bulletSpeedX = 50
        self.bulletSpeedY = 2*1
        self.bulletDamage = 10*1
        self.bulletRadius = 5*self.owner.extraSize
        self.bulletCount = 1*1
        self.energyConsumption = 5*1
        self.bullets = []
        exec(position[3])
    def tick(self):
        global FrameTime, keyboard
        self.Reloading += FrameTime
        if self.Reloading > self.ReloadingTime:
            self.Reloading = self.ReloadingTime
        txt = 'if keyboard.key'+self.owner.controls[4]+'''==1:
            self.shoot()'''
        exec(txt)
        self.targeting()
        for i in self.bullets:
            i.move()
            i.time -= FrameTime
            if i.time<0:
                self.bullets.remove(i)
    def shoot(self):
        if self.Reloading==self.ReloadingTime and self.energyConsumption<=self.owner.energy:
            for i in range(0, self.bulletCount):
                self.bullets.append(Bullet(self))
            self.Reloading=0
            self.owner.energy -= self.energyConsumption
    def draw(self):
        #canv.create_oval(self.owner.x+rotate([self.position], self.owner.angle, 0, 0)[0][0]*self.owner.extraSize+10*self.owner.extraSize, self.owner.y+rotate([self.position], self.owner.angle, 0, 0)[0][1]*self.owner.extraSize+10*self.owner.extraSize, self.owner.x+rotate([self.position], self.owner.angle, 0, 0)[0][0]*self.owner.extraSize-10*self.owner.extraSize, self.owner.y+rotate([self.position], self.owner.angle, 0, 0)[0][1]*self.owner.extraSize-10*self.owner.extraSize, fill = colorRGB(self.owner.color[0]/4, self.owner.color[1]/4, self.owner.color[2]/4), width=2*self.owner.extraSize, outline = colorRGB(255, 255, 255))
        x1 = self.owner.x+rotate([self.position], self.owner.angle, 0, 0)[0][0]*self.owner.extraSize
        y1 = self.owner.y+rotate([self.position], self.owner.angle, 0, 0)[0][1]*self.owner.extraSize
        x2 = self.owner.x+rotate([self.position], self.owner.angle, 0, 0)[0][0]*self.owner.extraSize + 30*self.owner.extraSize*math.cos(self.owner.angle)
        y2 = self.owner.y+rotate([self.position], self.owner.angle, 0, 0)[0][1]*self.owner.extraSize - 30*self.owner.extraSize*math.sin(self.owner.angle)
        canv.create_line(x1, y1, x2, y2, width=10*self.owner.extraSize, fill = colorRGB(self.owner.color[0]/4, self.owner.color[1]/4, self.owner.color[2]/4))
        self.drawBullets()
    def drawBullets(self):
        for i in self.bullets:
            i.draw()
    def targeting(self):
        a=0
        a+=1
    def checkHit(self, st2):
        for i in self.bullets:
            a=i.checkHit(st2)
            if a:
                self.bullets.remove(i)
                if st2.shield >= self.bulletDamage:
                    st2.shield-=self.bulletDamage
                else:
                    tmp = self.bulletDamage-st2.shield
                    st2.shield=0
                    st2.hp-=tmp
        if st2.hp<0:
            return True
        else:
            return False

class Starship():
    def __init__(self, color = [150, 150, 150], controls = ['w', 'a', 's', 'd', 'space'], txt = ''):
        global idCounter, width, heigth, FrameTime
        self.id = idCounter
        idCounter += 1
        self.score = 0
        self.hullPoly = [(-30, -30), (-30, 30), (60, 0)]
        self.thrustPoly = [(-30, -10), (-30, 10)]
        self.collisionR = 60
        self.color = color
        self.x = random.randint(0, width-1)
        self.y = random.randint(0, heigth-1)
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.botMode = 0
        n = 1000000000
        self.angle = random.randint(0, rounding(2*math.pi*n))/n
        self.extraSize = 0.25
        self.maxShield = 100
        self.shield = self.maxShield
        self.maxHp = 100
        self.hp =self.maxHp
        self.shieldRegeneration = 0.1*1
        self.hpRegeneration = 0.01
        self.engineForceAcseleration = 0.1
        self.maxForce = 10
        self.control =  0.5
        self.controls = controls
        self.force = 0
        self.mass = 50
        self.maxEnergy = 100
        self.energyRegeneration = 20*FrameTime/1000*1
        self.energy = self.maxEnergy
        self.notCrashed = 1
        # , [40, 0, 0, 'self.bulletDamage=100\nself.energyConsumption=75\nself.ReloadingTime=5000\nself.bulletSpeedY=1']
        self.gunsPositions = [[-20, -30, 0, 'self.bulletSpeedX=35'], [-20, 30, 0, 'self.bulletSpeedX=35']]
        exec(txt)
        self.guns = []
        for i in self.gunsPositions:
            self.guns.append(Gun(self, i))
        self.activeKeys = [0, 0, 0, 0, 0]
    def tick(self):
        self.shield+=self.shieldRegeneration
        if self.shield>self.maxShield:
            self.shield=self.maxShield
        self.hp+=self.hpRegeneration
        if self.hp>self.maxHp:
            self.hp=self.maxHp
        self.energy+=self.energyRegeneration
        if self.energy>self.maxEnergy:
            self.energy=self.maxEnergy
        self.move()
        self.draw()
        for i in self.guns:
            i.tick()
    def draw(self):
        #canv.create_oval(self.x+self.collisionR*self.extraSize, self.y+self.collisionR*self.extraSize, self.x-self.collisionR*self.extraSize, self.y-self.collisionR*self.extraSize, fill = 'grey', width=0)
        tmp = []
        for  i in self.thrustPoly:
            tmp.append((i[0]*self.extraSize, i[1]*self.extraSize))
        tmp.append(((-30-10*(self.force+1))*self.extraSize, random.randint(-5, 5)*self.extraSize))
        tmp2 = []
        for  i in self.hullPoly:
            tmp2.append((i[0]*self.extraSize, i[1]*self.extraSize))
        canv.create_polygon(rotate(movePoly(tmp2, self.x, self.y), self.angle, self.x, self.y), fill = colorRGB(self.color[0]/2, self.color[1]/2, self.color[2]/2), width=2*self.extraSize, outline = colorRGB(255, 255, 255))
        canv.create_polygon(rotate(movePoly(tmp, self.x, self.y), self.angle, self.x, self.y), fill = colorRGB(min((-(self.force/self.maxForce)**2+0.5*self.force/self.maxForce+1), 1)*255, min((-14/3*(self.force/self.maxForce)**2+31/6*self.force/self.maxForce+0), 1)*255, min((-2*(self.force/self.maxForce)**2+3*self.force/self.maxForce+0), 1)*255), width=0)
        for i in self.guns:
            i.draw()
    def move(self):
        global width, heigth
#        if keyboard.key9==1:
#            self.extraSize*=0.99
#        if keyboard.key0==1:
#            self.extraSize/=0.99
        txt = 'if keyboard.key'+self.controls[0]+'''==1:
            self.force+=self.engineForceAcseleration
            if self.force > self.maxForce:
                self.force = self.maxForce'''
        exec(txt)
        txt = 'if keyboard.key'+self.controls[2]+'''==1:
            self.force-=3*self.engineForceAcseleration
            if self.force < 0:
                self.force = 0'''
        exec(txt)
        txt = 'if keyboard.key'+self.controls[1]+'''==1:
            da = (0.5+self.control/2)/5/math.sqrt(1+math.sqrt(((self.vx)**2+(self.vy)**2)))
            self.angle += da
            tmpvx = self.vx
            tmpvy = self.vy
            self.vx = math.cos(da*(0.5+self.control/2))*tmpvx + math.sin(da*(0.5+self.control/2))*tmpvy
            self.vy = -math.sin(da*(0.5+self.control/2))*tmpvx + math.cos(da*(0.5+self.control/2))*tmpvy'''
        exec(txt)
        txt = 'if keyboard.key'+self.controls[3]+'''==1:
            da = (0.5+self.control/2)/5/math.sqrt(1+math.sqrt(((self.vx)**2+(self.vy)**2)))
            self.angle -= da
            tmpvx = self.vx
            tmpvy = self.vy
            self.vx = math.cos(-da*(0.5+self.control/2))*tmpvx + math.sin(-da*(0.5+self.control/2))*tmpvy
            self.vy = -math.sin(-da*(0.5+self.control/2))*tmpvx + math.cos(-da*(0.5+self.control/2))*tmpvy'''
        exec(txt)
        #canv.create_text(width/2-1, 60, text = mstr(math.sqrt((self.vx)**2+(self.vy)**2)), font = 'Verdana 30')
        self.ax = self.force/self.mass*math.cos(self.angle)*self.extraSize
        self.ay = -self.force/self.mass*math.sin(self.angle)*self.extraSize
        self.vx+=self.ax
        self.vy+=self.ay
        t1 = 0.025*self.extraSize
        #t2 = 0.99447
        t2 = 0.99
        self.vx-=min([math.copysign(t1*math.sqrt((self.vx**2)/(self.vx**2+self.vy**2+0.000000001)), self.vx), self.vx], key=F1)
        self.vy-=min([math.copysign(t1*math.sqrt((self.vy**2)/(self.vx**2+self.vy**2+0.000000001)), self.vy), self.vy], key=F1)
        self.vx=self.vx*t2
        self.vy=self.vy*t2
        self.x+=self.vx
        self.y+=self.vy
        if self.angle>2*math.pi:
            self.angle-=2*math.pi
        if self.x>width-1:
            self.x=0
        if self.x<0:
            self.x=width-1
        if self.y>heigth-1:
            self.y=0
        if self.y<0:
            self.y=heigth-1
    def checkHit(self, obj):
        a=0
        if obj.notCrashed:
            for i in self.guns:
                a = a or i.checkHit(obj)
        return a and obj.notCrashed
    def printStats(self, x, y):
        canv.create_text(x, y, text = 'Score = ' + str(self.score), font = 'Verdana 30',  fill  = colorRGB(self.color[0], self.color[1], self.color[2]))
        #canv.create_text(x, y+40, text = 'V = ' + mstr(math.sqrt((self.vx)**2+(self.vy)**2)), font = 'Verdana 20',  fill  = colorRGB(self.color[0], self.color[1], self.color[2]))
        canv.create_text(x, y+70, text = '|'*rounding(20*self.shield/self.maxShield), font = 'Verdana 20',  fill  = colorRGB(0, 0, 255))
        canv.create_text(x, y+100, text = '|'*rounding(20*self.hp/self.maxHp), font = 'Verdana 20',  fill  = colorRGB(255, 0, 0))
        canv.create_text(x, y+130, text = '|'*rounding(20*self.energy/self.maxEnergy), font = 'Verdana 20',  fill  = colorRGB(0, 255, 0))
        for i in range(0, len(self.guns)):
            canv.create_text(x, y+160+i*30, text = '|'*rounding(20*self.guns[i].Reloading/self.guns[i].ReloadingTime), font = 'Verdana 20',  fill  = colorRGB(255, 255, 0))
    def respawn(self):
        self.x = random.randint(0, width-1)
        self.y = random.randint(0, heigth-1)
        self.vx = 0
        self.vy = 0
        n = 1000000000
        self.angle = random.randint(0, rounding(2*math.pi*n))/n
        self.shield = self.maxShield
        self.hp = self.maxHp
        self.energy = self.maxEnergy
        self.notCrashed = 1
        self.force = 0
        for i in self.guns:
            i.bullets = []
            i.Reloading = 0
    def crash(self):
        self.notCrashed = 0
    def privateStats(self):
        stats = []
        
        return stats
    def publicStats(self):
        stats = []
        
        return stats
    def minRange(self, a):
        return math.sqrt((a[0]-self.x)**2+(a[1]-self.y)**2)
    def botMachineGun1(self, target):
        global width, heigth
        # выбор ближайшей точки прицеливания
        targetPoints = [[target.x+width, target.y+heigth],  [target.x, target.y+heigth],  [target.x-width, target.y+heigth],
                        [target.x+width, target.y],  [target.x, target.y],  [target.x-width, target.y],
                        [target.x+width, target.y-heigth],  [target.x, target.y-heigth],  [target.x-width, target.y-heigth]]
        targetPoint = min(targetPoints, key = self.minRange)
        # бот целится в цель
        dx = targetPoint[0]-self.x
        dy = targetPoint[1]-self.y
        targetAngle=0
        dx2 = 0
        dy2 = 0
        l = math.sqrt((dx+dx2)**2+(dy+dy2)**2)
        t = l/self.guns[0].bulletSpeedX/self.extraSize
        prevT=t
        t1 = 0.025*target.extraSize
        t2 = 0.99
        targetA = target.angle*1.0
        targetForce = target.force*1.0
        targetMass = target.mass*1.0
        targetVX = target.vx*1.0
        targetVY = target.vy*1.0
        t0=t
        if self.botMode==0:
            while t0>0:
                tmpt=min(1, t0)
                ax = targetForce/targetMass*math.cos(targetA)*target.extraSize
                ay = -targetForce/targetMass*math.sin(targetA)*target.extraSize
                targetVX+=ax*tmpt
                targetVY+=ay*tmpt
                targetVX-=min([math.copysign(t1*math.sqrt((targetVX**2)/(targetVX**2+targetVY**2+0.000000001)), targetVX), targetVX], key=F1)*tmpt
                targetVY-=min([math.copysign(t1*math.sqrt((targetVY**2)/(targetVX**2+targetVY**2+0.000000001)), targetVY), targetVY], key=F1)*tmpt
                targetVX=targetVX*t2*tmpt
                targetVY=targetVY*t2*tmpt
                dx2+=targetVX*tmpt-self.vx*tmpt
                dy2+=targetVY*tmpt-self.vy*tmpt
                l = math.sqrt((dx+dx2)**2+(dy+dy2)**2)
                t = l/self.guns[0].bulletSpeedX/self.extraSize
                t0+=t-prevT
                prevT=t
                t0-=1
        if dx2==0 and dy2==0:
            dx2+=(targetVX-self.vx)*t
            dy2+=(targetVY-self.vy)*t
        if dx+dx2<0:
            targetAngle=math.atan((-dy-dy2)/(dx+dx2))+math.pi
        else:
            targetAngle=math.atan((-dy-dy2)/(dx+dx2))
        dAngle = targetAngle-self.angle
        if dAngle>2*math.pi:
            dAngle-=2*math.pi
        if abs(dAngle)>math.pi:
            if dAngle>0:
                dAngle=-2*math.pi+dAngle
            else:
                dAngle=2*math.pi-dAngle
        # поворот
        if dAngle>0:
            da = min((0.5+self.control/2)/5/math.sqrt(1+math.sqrt(((self.vx)**2+(self.vy)**2))), abs(dAngle))
            #da = min((0.5+self.control/2)/5/math.sqrt(1+math.sqrt(((self.vx)**2+(self.vy)**2))), 555)
            if self.botMode==1:
                da*=-1
            self.angle += da
            tmpvx = self.vx
            tmpvy = self.vy
            self.vx = math.cos(da*(0.5+self.control/2))*tmpvx + math.sin(da*(0.5+self.control/2))*tmpvy
            self.vy = -math.sin(da*(0.5+self.control/2))*tmpvx + math.cos(da*(0.5+self.control/2))*tmpvy
        else:
            da = min((0.5+self.control/2)/5/math.sqrt(1+math.sqrt(((self.vx)**2+(self.vy)**2))), abs(dAngle))
            #da = min((0.5+self.control/2)/5/math.sqrt(1+math.sqrt(((self.vx)**2+(self.vy)**2))), 555)
            da*=-1
            if self.botMode==1:
                da*=-1
            self.angle += da
            tmpvx = self.vx
            tmpvy = self.vy
            self.vx = math.cos(da*(0.5+self.control/2))*tmpvx + math.sin(da*(0.5+self.control/2))*tmpvy
            self.vy = -math.sin(da*(0.5+self.control/2))*tmpvx + math.cos(da*(0.5+self.control/2))*tmpvy
        # движение 
        self.force+=self.engineForceAcseleration
        if self.force > self.maxForce:
            self.force = self.maxForce
        # переключение стрельбы
        if self.botMode==0:
            for i in self.guns:
                if abs(dAngle)<(target.collisionR*target.extraSize/l):
                    if target.notCrashed:
                        if l/self.guns[0].bulletSpeedX/self.extraSize<2000/FrameTime:
                            i.shoot()
            if self.energy<10:
                self.botMode=1
        if self.botMode==1:
            if self.energy>0.95*self.maxEnergy:
                self.botMode=0
            if self.energy>max(2*(target.hp*1+target.shield*1)/(self.guns[0].bulletDamage*self.guns[0].bulletCount)*self.guns[0].energyConsumption, len(self.guns)*self.guns[0].energyConsumption):
                self.botMode=0
    def botMachineGun2(self, target):
        global width, heigth
        BC=0
        for i in target.guns:
            for j in i.bullets:
                jPoses = [[j.circle.x+width, j.circle.y+heigth],  [j.circle.x, j.circle.y+heigth],  [j.circle.x-width, j.circle.y+heigth],
                        [j.circle.x+width, j.circle.y],  [j.circle.x, j.circle.y],  [j.circle.x-width, j.circle.y],
                        [j.circle.x+width, j.circle.y-heigth],  [j.circle.x, j.circle.y-heigth],  [j.circle.x-width, j.circle.y-heigth]]
                jPos = min(jPoses, key = self.minRange)
                if ((jPos[0]-self.x)**2+(jPos[1]-self.y)**2)<(200)**2:
                    BC+=1
        if BC>5:
            self.botMode = 1
        # выбор ближайшей точки прицеливания
        targetPoints = [[target.x+width, target.y+heigth],  [target.x, target.y+heigth],  [target.x-width, target.y+heigth],
                        [target.x+width, target.y],  [target.x, target.y],  [target.x-width, target.y],
                        [target.x+width, target.y-heigth],  [target.x, target.y-heigth],  [target.x-width, target.y-heigth]]
        targetPoint = min(targetPoints, key = self.minRange)
        # бот целится в цель
        dx = targetPoint[0]-self.x
        dy = targetPoint[1]-self.y
        targetAngle=0
        dx2 = 0
        dy2 = 0
        l = math.sqrt((dx+dx2)**2+(dy+dy2)**2)
        t = l/self.guns[0].bulletSpeedX/self.extraSize
        prevT=t
        t1 = 0.025*target.extraSize
        t2 = 0.99
        targetA = target.angle*1.0
        targetForce = target.force*1.0
        targetMass = target.mass*1.0
        targetVX = target.vx*1.0
        targetVY = target.vy*1.0
        t0=t
        if self.botMode==0:
            while t0>0:
                tmpt=min(1, t0)
                ax = targetForce/targetMass*math.cos(targetA)*target.extraSize
                ay = -targetForce/targetMass*math.sin(targetA)*target.extraSize
                targetVX+=ax*tmpt
                targetVY+=ay*tmpt
                targetVX-=min([math.copysign(t1*math.sqrt((targetVX**2)/(targetVX**2+targetVY**2+0.000000001)), targetVX), targetVX], key=F1)*tmpt
                targetVY-=min([math.copysign(t1*math.sqrt((targetVY**2)/(targetVX**2+targetVY**2+0.000000001)), targetVY), targetVY], key=F1)*tmpt
                targetVX=targetVX*t2*tmpt
                targetVY=targetVY*t2*tmpt
                dx2+=targetVX*tmpt-self.vx*tmpt
                dy2+=targetVY*tmpt-self.vy*tmpt
                l = math.sqrt((dx+dx2)**2+(dy+dy2)**2)
                t = l/self.guns[0].bulletSpeedX/self.extraSize
                t0+=t-prevT
                prevT=t
                t0-=1
        if dx2==0 and dy2==0:
            dx2+=(targetVX-self.vx)*t
            dy2+=(targetVY-self.vy)*t
        if self.botMode==1:
            if len(target.guns[0].bullets)+len(target.guns[1].bullets)>0 and 1:
                dx2=0
                dy2=0
                dx=0
                dy=0
                targX=0
                targY=0
                targVX=0
                targVY=0
                MassK=0
                for i in target.guns:
                    for j in i.bullets:
                        jPoses = [[j.circle.x+width, j.circle.y+heigth],  [j.circle.x, j.circle.y+heigth],  [j.circle.x-width, j.circle.y+heigth],
                        [j.circle.x+width, j.circle.y],  [j.circle.x, j.circle.y],  [j.circle.x-width, j.circle.y],
                        [j.circle.x+width, j.circle.y-heigth],  [j.circle.x, j.circle.y-heigth],  [j.circle.x-width, j.circle.y-heigth]]
                        jPos = min(jPoses, key = self.minRange)
                        jSpeeds = [j.vx,j.vy]
                        m=min([1000000/(math.sqrt((jPos[0]-self.x)**2+(jPos[1]-self.y)**2))**3, 1], key=abs)
                        targVX+=jSpeeds[0]
                        targVY+=jSpeeds[1]
                        targX+=jPos[0]*m
                        targY+=jPos[1]*m
                        MassK+=m
                targX=targX/MassK
                targY=targY/MassK
                if ((self.x-target.x)**2+(self.y-target.y)**2)**(1/2) < 10:
                    dx = -self.vy
                    dy = self.vx
                else:
                    
                
                #dx=-targX+self.x
                #dy=-targY+self.y
                    if targVX!=0 and targVY!=0:
                        dx=(targVY*(math.atan(targY/targX)-math.atan(targVY/targVX))/abs(math.atan(targY/targX)-math.atan(targVY/targVX)))+self.x-targX
                        dy=(-targVX*(math.atan(targY/targX)-math.atan(targVY/targVX))/abs(math.atan(targY/targX)-math.atan(targVY/targVX)))+self.y-targY
                    if dx==0 and dy==0:
                        dx=-targetPoint[0]+self.x                              
                        dy=-targetPoint[1]+self.y
            else:
                dx=-targetPoint[0]+self.x
                dy=-targetPoint[1]+self.y
        if dx+dx2<0:
            targetAngle=math.atan((-dy-dy2)/(dx+dx2))+math.pi
        else:
            targetAngle=math.atan((-dy-dy2)/(dx+dx2))
        dAngle = targetAngle-self.angle
        if dAngle>2*math.pi:
            dAngle-=2*math.pi
        if abs(dAngle)>math.pi:
            if dAngle>0:
                dAngle=-2*math.pi+dAngle
            else:
                dAngle=2*math.pi-dAngle
        # поворот
        if dAngle>0:
            da = min((0.5+self.control/2)/5/math.sqrt(1+math.sqrt(((self.vx)**2+(self.vy)**2))), abs(dAngle))
            #da = min((0.5+self.control/2)/5/math.sqrt(1+math.sqrt(((self.vx)**2+(self.vy)**2))), 555)
            if self.botMode==1:
                da*=-1
            self.angle += da
            tmpvx = self.vx
            tmpvy = self.vy
            self.vx = math.cos(da*(0.5+self.control/2))*tmpvx + math.sin(da*(0.5+self.control/2))*tmpvy
            self.vy = -math.sin(da*(0.5+self.control/2))*tmpvx + math.cos(da*(0.5+self.control/2))*tmpvy
        else:
            da = min((0.5+self.control/2)/5/math.sqrt(1+math.sqrt(((self.vx)**2+(self.vy)**2))), abs(dAngle))
            #da = min((0.5+self.control/2)/5/math.sqrt(1+math.sqrt(((self.vx)**2+(self.vy)**2))), 555)
            da*=-1
            if self.botMode==1:
                da*=-1
            self.angle += da
            tmpvx = self.vx
            tmpvy = self.vy
            self.vx = math.cos(da*(0.5+self.control/2))*tmpvx + math.sin(da*(0.5+self.control/2))*tmpvy
            self.vy = -math.sin(da*(0.5+self.control/2))*tmpvx + math.cos(da*(0.5+self.control/2))*tmpvy
        # движение 
        self.force+=self.engineForceAcseleration
        if self.force > self.maxForce:
            self.force = self.maxForce
        # переключение стрельбы
        if self.botMode==0:
            for i in self.guns:
                if abs(dAngle)<(target.collisionR*target.extraSize/l):
                    if target.notCrashed:
                        if l/self.guns[0].bulletSpeedX/self.extraSize<2000/FrameTime:
                            i.shoot()
            if self.energy<10:
                self.botMode=1
        if self.botMode==1:
            if self.energy>0.95*self.maxEnergy:
                self.botMode=0
            if self.energy>max(2*(target.hp*1+target.shield*1)/(self.guns[0].bulletDamage*self.guns[0].bulletCount)*self.guns[0].energyConsumption, len(self.guns)*self.guns[0].energyConsumption):
                self.botMode=0
        




if __name__=='__main__':
    idCounter = 0
    FrameTime = 16
    
    glob_P=1
    def pause(a):
        global glob_P
        glob_P = 1-glob_P
    
    root = tkinter.Tk()
    width = 1600
    heigth = 850
    WH =  str(width)+'x'+str(heigth)
    root.geometry(WH)
    canv = tkinter.Canvas(root, width=width, height=heigth, bg='black')
    canv.pack()
    keyboard = MyKeyboard.Keyboard(root)
    x=400
    y=300
    r=100
    Starship001 = Starship(color = [255, 0, 0])
#    Starship002 = Starship(color = [0, 255, 0], controls = ['9', 'i', 'o', 'p', 'l'], txt = "self.gunsPositions = [[-20, -30, 0, 'self.bulletSpeedX=20\\nself.bulletSpeedY=5\\nself.bulletCount = 15\\nself.bulletDamage = 1'], [-20, 30, 0, 'self.bulletSpeedX=20\\nself.bulletSpeedY=5\\nself.bulletCount = 15\\nself.bulletDamage = 1']]")
    Starship002 = Starship(color = [0, 255, 0], controls = ['9', 'i', 'o', 'p', 'l'])
    reset =  0
    
    root.bind('<Key-p>', pause)
    
    def draw():
        global x, y, r, FrameTime, reset, glob_P
        canv.delete(tkinter.ALL)
        if glob_P==0:
            Starship002.botMachineGun1(Starship001)
            #Starship001.botMachineGun1(Starship002)
            if  Starship001.notCrashed:
                if Starship001.checkHit(Starship002):
                    Starship002.crash()
                    Starship001.score += 1
            if  Starship002.notCrashed:
                if Starship002.checkHit(Starship001):
                    Starship001.crash()
                    Starship002.score += 1
            if  Starship001.notCrashed:
                Starship001.tick()
            if  Starship002.notCrashed:
                Starship002.tick()
        else:
            if  Starship001.notCrashed:
                Starship001.draw()
            if  Starship002.notCrashed:
                Starship002.draw()
        Starship001.printStats(150, 60)
        Starship002.printStats(width-150, 60)
        if not (Starship001.notCrashed and Starship002.notCrashed):
            reset += 1
        if reset > 1000/FrameTime*5:
            reset = 0
            Starship001.respawn()
            Starship002.respawn()
        #canv.create_oval(x+r, y+r, x-r, y-r, fill = "red", width=0)
#        if keyboard.keyw==1:
#            y-=1
#        if keyboard.keya==1:
#            x-=1
#        if keyboard.keys==1:
#            y+=1
#        if keyboard.keyd==1:
#            x+=1
        root.after(FrameTime, draw)
    draw()
    tkinter.mainloop()
