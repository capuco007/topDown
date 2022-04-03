from this import d
import bge
from collections import OrderedDict
from mathutils import Vector
GD = bge.logic.globalDict
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
    # Roda em todos os frames no jogo
    def onCollision(self,object):
        GD = bge.logic.globalDict

        if 'ground' in object:
            self.object['LVL'] = object.groupObject['LVL']
            
            

        if 'bulet_enemy' in object:
            object.endObject()
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
                else:
                    if GD['equiped']:
                        if not object['gun'] in GD['gunColected']:
                            if str(GD['equiped']) in  GD['gunColected']:
                                GD['gunColected'].remove(GD['equiped'])
                                GD['gunColected'].append(object['gun'])
                                GD['equiped'] = object['gun']

                
        
    def move(self):
        
        y = self.tc[bge.events.WKEY].active - self.tc[bge.events.SKEY].active
        x = self.tc[bge.events.DKEY].active - self.tc[bge.events.AKEY].active
        
        
        self.char.walkDirection = Vector([x, y, 0]).normalized()*self.speed
     
    def shoot(self):
        
        if  GD['equiped'] != None:
            if self.ms[bge.events.LEFTMOUSE].active:
                if 'pistola' in GD['equiped']:
                    if self.timeShot == 0:
                        self.timeShot = 10
                        self.scene.addObject('ball',self.spw, 100)
                if 'metra' in GD['equiped']:
                    if self.timeShot == 0:
                        self.timeShot = 1
                        self.scene.addObject('ball',self.spw, 100)
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

               
    def update(self):
        if not 'hud_wepon' in self.scnL:

            self.tradeGun()
            self.move()
            self.shoot()
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
        colision = cont.sensors['Collision']
        scene = obj.scene
        player = scene.objects['player']
        if player['time_spw']>0:
            player['time_spw'] -= 1

        if colision.positive:
            spw_pl = player.childrenRecursive.get('spw_p')
            dor = colision.hitObject
            group = dor.groupObject
           
            if group['active'] == False:
                if player['orbs'] >0 and player['time_spw'] ==0:
                    scene.addObject('orbs_group_port',spw_pl, 0)
                    player['time_spw'] = 30


                if  group['timeInject'] >0:
                    group['timeInject'] -= 1


                if group['orbs'] <= player['orbs'] and group['timeInject'] == 0:
                    
                    if group['orbs'] >0:
                        print(group['orbs'],player['orbs'])
                        group['orbs'] -= 1
                    if player['orbs'] >0:
                        player['orbs'] -= 1
                    group['timeInject'] = 50

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