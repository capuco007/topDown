from this import d
import bge
from collections import OrderedDict
from mathutils import Vector
GD = bge.logic.globalDict
import random
class Player(bge.types.KX_PythonComponent):
    # Put your arguments here of the format ("key", default_value).
    # These values are exposed to the UI.
    args = OrderedDict([
    ])

    

    
    # Roda apenas uma ver no game !!
    def start(self, args):
        # pegando a cena atual
        self.scene = self.object.scene
        # spaw
        self.spw = self.scene.objects['spw']
        
        # Pegando as teclas
        self.tc = bge.logic.keyboard.inputs
        # Pegando o Mouse
        self.ms = bge.logic.mouse.inputs
        # Velocidade para se mover
        self.speed = 0.1
        # Pegando a fisica Character do object
        self.char = bge.constraints.getCharacter(self.object) 
        # tempo de disparo
        self.timeShot = 0
        self.life = 100
        self.hitDamage = None
        self.timeDamage =0
       
        self.dorObject = None
        self.dorOpening = 0
        self.orbs = 0
        self.gropuDor = None
        self.object.collisionCallbacks.append(self.onCollision)
        self.timeOrbs = 0
        self.hud = 0
        self.gun = []
        GD = bge.logic.globalDict
        GD['gunColected'] = []
        GD['gunList'] = []
        GD['equiped'] = None
        self.scnL = bge.logic.getSceneList()
        self.PlayMeshArm = self.object.childrenRecursive.get('PlayMeshArm')
        self.timeDash = 0
        self.energy = 100
        self.decarga = 80
        self.municao = 100
    # Roda em todos os frames no jogo

    def onCollision(self,object):
        GD = bge.logic.globalDict
        if 'life' in object:
            if self.life < 100:
                self.life += random.randint(0,25)
                object.endObject()
        if 'municao' in object:
            if self.municao < 300:
                self.municao += random.randint(0,75)
                object.endObject()

        if 'espinho' in object:
            self.hitDamage = object
            self.life -= 1

        if 'ground' in object:
            self.object['LVL'] = object.groupObject['LVL']
            
            

        if 'bulet_enemy' in object:
            object.endObject()
            if self.life >0:
                self.life -= 1

        if 'orbes' in object and self.timeOrbs == 0:
             self.object['orbs'] += 1
             self.timeOrbs = 5

        if 'guns' in object:
            if self.tc[bge.events.EKEY].activated:
                if  len( GD['gunColected']) <=3:
                    if not object.groupObject['gun'] in GD['gunColected']:
                        GD['gunColected'].append(object.groupObject['gun'])
                        GD['equiped'] = object.groupObject['gun']
                        object.endObject()
                else:
                    if GD['equiped']:
                        if not object['gun'] in GD['gunColected']:
                            #self.scene.addObject()
                            if str(GD['equiped']) in  GD['gunColected']:
                                GD['gunColected'].remove(GD['equiped'])
                                GD['gunColected'].append(object['gun'])
                                GD['equiped'] = object['gun']
                                object.endObject(str(GD['equiped']),self.spw,0)
                                         
    def move(self):
        if self.timeDamage>0:
            self.timeDamage -=1
        y = self.tc[bge.events.WKEY].active - self.tc[bge.events.SKEY].active
        x = self.tc[bge.events.DKEY].active - self.tc[bge.events.AKEY].active

        if self.hitDamage and self.timeDamage == 0:
            self.timeDamage = 10
            dir = self.object.worldPosition - self.hitDamage.worldPosition
            self.char.walkDirection =  Vector(dir *1).normalized()*self.speed
           
            dir = None
        if self.timeDamage<3:
            self.hitDamage = None
        
        if not self.hitDamage:
     
            self.char.walkDirection = Vector([x, y, 0]).normalized()*self.speed
     
    def shoot(self):
        
        if  GD['equiped'] != None and self.municao >0:
            if self.ms[bge.events.LEFTMOUSE].active:
                if 'pistola' in GD['equiped']:
                    if self.timeShot == 0:
                        self.timeShot = 20
                        self.scene.addObject('ball',self.spw, 100)
                        self.municao -= 1
                if 'metra' in GD['equiped']:
                    if self.timeShot == 0:
                        self.timeShot = 8
                        self.scene.addObject('ball',self.spw, 100)
                        self.municao -= 1
                else:
                    pass
                
    def tradeGun(self):
        GD = bge.logic.globalDict

    def sceneGame(self):
        #bge.logic.addScene('hud_wepon',1)
        scnL = bge.logic.getSceneList()
        

        if self.tc[bge.events.QKEY].active and  self.hud <3 :   
            
                self.hud +=1
        else:
            if self.hud >0:
                self.hud -= 1

        if self.hud == 2:
            if not 'hud_wepon' in scnL:
                bge.logic.addScene('hud_wepon',1)
                bge.logic.setTimeScale(0.05)
                bge.logic.sendMessage('activeFilter')
           
        if self.hud == 1:
            
            for scn in scnL:
                if scn.name == 'hud_wepon':
                    scn.end()
                    bge.logic.setTimeScale(1.0)
                    bge.logic.sendMessage('deactiveFilter')
                    break

    def dash(self):
        
       
        if self.energy < 100:
            self.energy += 1
        
        if self.timeDash == 0:
            self.speed = 0.15
            
            if self.tc[bge.events.SPACEKEY].activated and  self.energy >= self.decarga:
                self.timeDash = 5
                
        if self.timeDash == 5:
            if self.energy >= self.decarga:
                    self.energy -= self.decarga

        if self.timeDash >0:
            self.speed = 0.6
            self.timeDash -= 1
               
    def update(self):
        if self.municao > 300:
            self.municao = 300
        if self.life > 100:
            self.life = 100
        print(self.life)
        if  GD['equiped'] != None:
            self.PlayMeshArm.visible = True
            self.PlayMeshArm.replaceMesh(GD['equiped']) 
        if GD['equiped'] == None:
            self.PlayMeshArm.visible = False
            self.PlayMeshArm.replaceMesh('macakinha') 
        if not 'hud_wepon' in self.scnL:

            self.tradeGun()
            self.move()
            self.shoot()
            self.dash()
        else:
            self.char.walkDirection = Vector([0, 0, 0])
        self.sceneGame()
       

        
        if self.timeOrbs >0:
            self.timeOrbs -=1
        
        # Diminuir falor
        if self.timeShot > 0:
            self.timeShot -= 1

def dors(cont):
        
        obj = cont.owner
        kb = bge.logic.keyboard.inputs
        colision = cont.sensors['Collision']
        scene = obj.scene
        player = scene.objects['player']
        
        if player['time_spw']>0:
            player['time_spw'] -= 1
       
        if colision.positive :
            spw_pl = player.childrenRecursive.get('spw_p')
            dor = colision.hitObject
            group = dor.groupObject
           
            if group['active'] == False and kb[bge.events.EKEY].active and  player['orbs'] >0 :
               
                if player['time_spw'] ==0:
                    if player['orbs'] >0:
                        player['orbs'] -= 1
                    scene.addObject('orbs_group_port',spw_pl, 0)
                    player['time_spw'] = 20
                    if group['orbs'] >0:
                        print(group['orbs'],player['orbs'])
                        group['orbs'] -= 1


                if  group['timeInject'] >0:
                    group['timeInject'] -= 1


                if group['orbs'] <= player['orbs'] and group['timeInject'] == 0:
                    
                   
                    
                    group['timeInject'] = 20

                    if group['orbs'] == 0:
                        if group['active'] == False:
                            group['active'] = True



            if group['active']:

                if group['time'] <20:
                    group['time'] += 1
                    
                    


                for DR in dor.childrenRecursive:
                    if 'DR' in DR:
                        DR.playAction('porta_r',group['time'],group['time'], play_mode = 1)

                for DL in dor.childrenRecursive:
                    if 'DL' in DL:
                        DL.playAction('porta_l',group['time'],group['time'], play_mode = 1)
            
            obj['objColision'] = dor
        else:
            pass
            #obj['objColision'] = None