from bge import logic

def start(cont):
    obj = cont.owner
    scene = obj.scene
    obj['pl'] = [obj for obj in scene.objects if 'jogador' in obj]

def update(cont):
    obj = cont.owner
    track = obj.actuators['track']
    group = obj.groupObject


    if 'orbsPlayer' in group:
        if obj['pl']:
            track.object = obj['pl'][0]
            dis = obj.getDistanceTo(obj['pl'][0])
            if dis <= 5:
                cont.activate(track)
                obj.applyMovement([0,0.1,0], True)

    if 'orbsPorta' in group:
        if obj['pl']:
            pl = obj['pl'][0]
            track.object = pl['objColision']
            dis = obj.getDistanceTo(pl['objColision'])
            cont.activate(track)
            obj.applyMovement([0,0.1,0], True)
            if dis <= 2:
                obj.endObject()


