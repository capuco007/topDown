from operator import add
import bge
from collections import OrderedDict
import random

class Enemy(bge.types.KX_PythonComponent):
    # Put your arguments here of the format ("key", default_value).
    # These values are exposed to the UI.
    args = OrderedDict([
    ])

    def start(self, args):
        self.scene = self.object.scene
        self.timeShot = 0
        self.player = [obj for obj in self.scene.objects if 'jogador' in obj]
        self.spw_enemy = self.object.childrenRecursive.get('spw_enemy')
        self.object.collisionCallbacks.append(self.damage)
        self.goupEnemy = self.object.groupObject
        self.life = self.goupEnemy['life']
        self.isMov = True
        Steering = self.object.actuators['Steering']
        Steering.velocity = self.object.groupObject['speed']
        

        

    def damage(self,object):
        if 'bulet' in object:
            self.life -= 1
            self.scene.addObject('',self.object,100)
            object.endObject()




    def atack(self):

        self.dis = self.object.getDistanceTo(self.player[0])
        
        if  self.goupEnemy['type'] == 1:
            if self.dis < 5:
                if self.timeShot == 0:
                    self.scene.addObject('bulet_enemy',self.spw_enemy,100)
                    self.timeShot = 100
            if self.dis < 3:
                self.isMov = False
            else:
                self.isMov = True


        if  self.goupEnemy['type'] == 2:
            if self.dis < 10:
                if self.timeShot == 0:
                    self.scene.addObject('bulet_enemy',self.spw_enemy,100)
                    self.timeShot = 90
            if self.dis < 1:
                self.isMov = False
            else:
                self.isMov = True

    def update(self):
        scnL = bge.logic.getSceneList()

        if not 'hud_wepon' in scnL:

            self.object['isMov'] = self.isMov
            self.atack()
            
            if self.life <= 0:
                iten = random.randint(0,100)
                
                if iten<30:
                    listIten=['life','municao']
                    addIten =random.choice(listIten)
                    self.scene.addObject(addIten,self.object, 0)
                    print(addIten['life'])
                self.scene.addObject('orbs_group',self.object, 0)
                self.object.endObject()
        
            if self.timeShot >0:
                self.timeShot -= 1
       