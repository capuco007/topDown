import bge
from collections import OrderedDict

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
        self.life = 5
        self.isMov = True

        self.goupEnemy = self.object.groupObject

    def damage(self,object):
        if 'bulet' in object:
            self.life -= 1
            object.endObject()



    def atack(self):

        self.dis = self.object.getDistanceTo(self.player[0])

        if 'enemy_1' in self.goupEnemy:
            if self.dis < 5:
                if self.timeShot == 0:
                    self.scene.addObject('bulet_enemy',self.spw_enemy,100)
                    self.timeShot = 100
                self.isMov = False
            else:
                self.isMov = True


        if 'enemy_2' in self.goupEnemy:
            if self.dis < 5:
                if self.timeShot == 0:
                    self.scene.addObject('bulet_enemy',self.spw_enemy,100)
                    self.timeShot = 10
                self.isMov = False
            else:
                self.isMov = True

    def update(self):
        scnL = bge.logic.getSceneList()

        if not 'hud_wepon' in scnL:

            self.object['isMov'] = self.isMov
            self.atack()
            
            if self.life <= 0:
                self.scene.addObject('orbs_group',self.object, 0)
                self.object.endObject()
        
            if self.timeShot >0:
                self.timeShot -= 1
       