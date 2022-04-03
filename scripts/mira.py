from bge import logic
import bge


def mouse(cont):
    obj = cont.owner
    scene = obj.scene
    mira = [obj for obj in scene.objects if 'mira' in obj]
    eixoMira = scene.objects['eixo-mira']
    mouse = cont.sensors['Mouse']
    scnL = bge.logic.getSceneList()

    if not 'hud_wepon' in scnL:
        if mouse.positive:
            position = mouse.hitPosition
            mira[0].worldPosition.x = position[0]
            mira[0].worldPosition.y = position[1]
        
       
       