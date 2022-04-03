from bge import logic
import bge

def start(cont):
    obj = cont.owner
    scene = obj.scene
    obj['navList'] = [obj for obj in scene.objects if 'navmesh' in obj]
    obj['playerList'] = [obj for obj in scene.objects if 'jogador' in obj]
    obj['nav'] = None
   
        
    for n in obj['navList']:
        if n['LVL'] == obj.groupObject['LVL']:
            obj['nav'] = n
            
            

def track(cont):
    
    own = cont.owner
    scene = own.scene
    Steering = cont.actuators['Steering']
    TrackTo = cont.actuators['TrackTo']
    nav = own['nav']
    player = own['playerList'][0]
    dis = own.getDistanceTo(player)
    scnL = [s.name for s in bge.logic.getSceneList()]
    TrackTo.object = player

    if player['LVL'] == own.groupObject['LVL'] and nav and dis < 15 and own['isMov'] == True:
        Steering.target = player
        Steering.navmesh = nav
        cont.activate(Steering)
        cont.activate(TrackTo)
        
    elif dis <3:
        cont.deactivate(Steering)   
    else:
        cont.deactivate(Steering)

    

    