# All entities (not to be mistaken by the actual map)
# are defined here in this file
# PS: Good luck finding what is what

import math
import pygame.constants as pyConst
import pygame
import levelData
import renderer
import collisionDetection
import mathHelpers
import enum
import os
import gameIO
import pathFinding

#Base class for everything 
class Entity():
    def __init__(self, start_pos):
        self.px = start_pos[0]
        self.py = start_pos[1]

    def update(self, dt, events):
        pass

    def get_pos(self):
        return (self.px, self.py)

# An entity with an "agent_pack" which is a
# way to group everything related to an object
# to a folder name in the Assets folder 
class SpriteEntity(Entity):
    def __init__(self, start_pos, agent_pack_name="Default"):
        super().__init__(start_pos)
        # We only store the name because pickle cant
        # store surfaces and sound classes
        self.agent_pack_name = agent_pack_name
    
    def get_sprite(self, camObj):
        return gameIO.get_sprite(self.agent_pack_name, 0)

# An entity with a camera
# everything derived froom this class
# can be considered playerish
class Agent(SpriteEntity):
    def __init__(self, start_pos, fov, moveSpeed, fovDepth):
        super().__init__(start_pos)
        # Everything has health but only the player actualy uses it
        # HMMMMMMMMMMMMMMMM
        self.health = 100
        self.entitiesInSight = []

        # I could use "player.instance in entitiesInSight" but whatever
        self.canSeePlayer = False

        # "A ray" that store rays (pun intended) so they can be drawn 
        # on screen. You can spectate enemies!
        self.rayDistanceTable = {}
        self.FOV = fov * (math.pi/180)
        self.FOVDepth = fovDepth
        self.angleY = 0
        self.moveSpeed = moveSpeed

        self.dirX = -1
        self.dirY = 0

        self.planeX = 0
        self.planeY = 0.66

    def update(self, dt, events):
        renderer.generate_distance_table(self)
        return super().update(dt, events)

    def move(self, dirX, dirY, deltaTime):
        # I splitted movemnt in two so the player
        # can slide walls
        nexPosX = self.px + dirX
        nexPosY = self.py + dirY
        # Move X

        if (nexPosX < 0 or nexPosX > levelData.Level.currentMap.level_width):
            self.px += dirX
        elif self.py < 0 or self.py > levelData.Level.currentMap.level_height:
            self.px += dirX
        elif levelData.Level.currentMap.grid[int(nexPosX)][int(self.py)] == 0:
            self.px += dirX

        # Move Y

        if nexPosY < 0 or nexPosY > levelData.Level.currentMap.level_height:
            self.py += dirY
        elif (self.px < 0 or self.px > levelData.Level.currentMap.level_width):
            self.py += dirY
        elif levelData.Level.currentMap.grid[int(self.px)][int(nexPosY)] == 0:
            self.py += dirY

    def move_to(self, target, deltaTime):
        angle = math.atan2(self.dirY, self.dirX)
        self.look_at(target, deltaTime * 2)
        dirX = math.cos(angle) * self.moveSpeed * deltaTime
        dirY = math.sin(angle) * self.moveSpeed * deltaTime
        self.move(dirX, dirY, deltaTime)

    def rotate(self, amount):
        #Rotating the player and its projection plane
        oldDirX = self.dirX
        self.dirX =  self.dirX * math.cos(amount) - self.dirY * math.sin(amount)
        self.dirY = oldDirX  * math.sin(amount) + self.dirY * math.cos(amount)

        oldPlaneX = self.planeX
        self.planeX = self.planeX * math.cos(amount) -  self.planeY * math.sin(amount)
        self.planeY = oldPlaneX * math.sin(amount) + self.planeY * math.cos(amount)

    def look_at(self, target, deltaTime):

        dx, dy = mathHelpers.slope(self.get_pos(), target.get_pos())
        # Finds out whats the target angle to the target
        theta = math.atan2(dy, dx)
        angle = math.atan2(self.dirY, self.dirX)
        targetAngle = theta
        targetAngle = math.degrees(targetAngle)
        # Good old stack exchange :)
        # https://math.stackexchange.com/a/2898118
        shortest_angle=((((targetAngle - math.degrees(angle)) % 360) + 540) % 360) - 180
        self.rotate(math.radians(shortest_angle) * deltaTime )


class EnemyStatus(enum.Enum):
    import colors
    Normal = ("Normal", colors.GREEN, 0)
    Alert = ("Alert", colors.RED, 10)
    Evasion = ("Evasion", colors.YELLOW, 20)
    Caution = ("Caution", colors.MAROON, 30)


# My failed attempt to have 8 directional sprites
# the is still some remainings of my attempt in the 
# SpriteAgent class

# class AngleDirection(enum.Enum):
#     back = 4
#     backDiag = 3
#     side = 2
#     fronDiag = 1
#     front = 0

# I created this class by accident
# all Agents already have sprites
class SpriteAgent(Agent):
    def __init__(self, start_pos, fov, moveSpeed, fovDepth, agent_pack):
        super().__init__(start_pos, fov, moveSpeed, fovDepth)
        # Five sprites from 0 to 180 in steps of 45
        self.agent_pack_name = agent_pack

    
    def get_sprite(self, camObj):
        angle = math.atan2(self.dirY, self.dirX)
        camObjAngle =math.atan2(camObj.dirY, camObj.dirX)

        camPos = camObj.get_pos()
        dx, dy = mathHelpers.slope(camPos, self.get_pos())
        camAngleToSprite = (math.atan2(dy, dx))
        angleCamDelta = mathHelpers.fixed_angle(camAngleToSprite + angle)

        curr = gameIO.get_sprite(self.agent_pack_name, 0)

        if math.degrees(angleCamDelta) < 180:
            curr = pygame.transform.flip(curr, True, False)

        return curr

# The player is a singleton
# You can actually see yourself
# if you change the "draw_first_person(player_instance)"
# to levelData.current_map.grid_entities[some_number]
class Player(SpriteAgent):
    instance = None

    def __init__(self, start_pos):
        super().__init__(start_pos, 90, 2, renderer.DEPTH,
                         "enemyIdle")

        Player.instance = self
        self.mouseEnable = False
        self.cameraYawSens = 2
        self.cameraPitchSens = 360
        self.keys = 0

    def update(self, dt, events):
        get_input(self, dt, events)
        return super().update(dt, events)
        
class Enemy(SpriteAgent):
    enemy_status = EnemyStatus.Normal
    enemy_status_time_left = 0

    def __init__(self, start_pos, patrolPoint=None):
        super().__init__(start_pos, 90, 2, 6,
                         "Droog")

        self.patrolPoint = patrolPoint
        self.target = self.patrolPoint

        self.pathFindingNodesTarget = self.target
        self.pathFindingNodes = None

        self.timeGuarded = 0
        self.pathFindingComplete = False
        self.originalFov = self.FOV
        self.originalFovDepth = self.FOVDepth
        self.lastPathFindingPoint = None
        self.cameraYawSens = 4

    # Base enemy behaviour
    # It stills needs some tweaking
    def update(self, dt, events):
        super().update(dt, events)
        # Status time will lower faster if there is more enemies
        # PS: Its a feature
        Enemy.enemy_status_time_left -= dt
        if Enemy.enemy_status_time_left < 0:
            Enemy.enemy_status_time_left = 0
            if Enemy.enemy_status == EnemyStatus.Alert:
                Enemy.enemy_status = EnemyStatus.Evasion
            elif Enemy.enemy_status == EnemyStatus.Evasion:
                Enemy.enemy_status = EnemyStatus.Caution
            elif Enemy.enemy_status == EnemyStatus.Caution:
                Enemy.enemy_status = EnemyStatus.Normal

            if Enemy.enemy_status != EnemyStatus.Normal:
                Enemy.reset_enemy_status_time()

        if Enemy.enemy_status == EnemyStatus.Normal:
            self.change_target(self.patrolPoint)

        if Player.instance in [x[0] for x in self.entitiesInSight]:
            self.canSeePlayer = True
            Enemy.change_enemy_status(EnemyStatus.Alert)
        else:
            self.canSeePlayer = False

        if self.canSeePlayer or Enemy.enemy_status == EnemyStatus.Alert:
            self.change_target(Player.instance)

        if Enemy.enemy_status == EnemyStatus.Evasion:
            if self.pathFindingNodesTarget != Player.instance:
                self.change_target(Player.instance)
            if self.pathFindingComplete:
                # pick random point on the map
                while len(self.pathFindingNodes) == 0:
                    random_pos = Entity(
                        levelData.Level.currentMap.pick_random_point())

                    self.change_target(random_pos)

        if Enemy.enemy_status == EnemyStatus.Caution:
            if self.pathFindingComplete:
                # pick random point on the map
                random_pos = Entity(
                    levelData.Level.currentMap.pick_random_point())
                dx, dy = mathHelpers.slope(
                    self.get_pos(), random_pos.get_pos())
                targetDistance = math.hypot(dx, dy)
                if len(self.pathFindingNodes) == 0 or targetDistance < 1:
                    while len(self.pathFindingNodes) == 0 and targetDistance < 1:
                        random_pos = Entity(
                            levelData.Level.currentMap.pick_random_point())
                        dx, dy = mathHelpers.slope(
                            self.get_pos(), random_pos.get_pos())
                        targetDistance = math.hypot(dx, dy)

                self.change_target(random_pos)

        if (Enemy.enemy_status == EnemyStatus.Evasion or
                Enemy.enemy_status == EnemyStatus.Alert or
                Enemy.enemy_status == EnemyStatus.Caution):
            self.FOV = self.originalFov * 1.5
            self.FOVDepth = self.originalFovDepth * 1.5
        else:
            self.FOV = self.originalFov
            self.FOVDepth = self.originalFovDepth

        if self.target is not None:
            dx, dy = mathHelpers.slope(self.get_pos(), self.target.get_pos())
            targetDistance = math.hypot(dx, dy)
            if self.pathFindingNodes is not None and len(self.pathFindingNodes) > 0:
                nextStep = self.pathFindingNodes[0]
                
                nextPathNodeDistance = mathHelpers.distance_to(self.get_pos(), nextStep)
                adjustedNextStep = (nextStep[0]+0.5, nextStep[1]+0.5)
                self.move_to(Entity(adjustedNextStep), dt)
                if nextPathNodeDistance < 0.1:
                    self.pathFindingNodes.pop(0)    
            else:
                self.pathFindingComplete = True
                if targetDistance > 0.5:
                    self.move_to(self.target, dt)

            if isinstance(self.target, Node) and targetDistance < 0.5:
                self.timeGuarded += dt
                self.rotate(math.radians(36) * dt)

                if self.timeGuarded > 1:
                    self.change_patrol_point()

    def change_target(self, target):
        if target != None:
            self.target = target
            x, y = target.get_pos()
            x = int(x)
            y = int(y)
            my_pos = (int(self.px), int(self.py))
            self.lastPathFindingPoint = target.get_pos()
            self.pathFindingComplete = False
            self.pathFindingNodesTarget = target
            self.pathFindingNodes = pathFinding.go_to(my_pos, (x, y))
            self.pathFindingNodes.pop(0)

    def change_patrol_point(self):
        self.patrolPoint = self.target.pick_random_node()
        self.timeGuarded = 0
        self.change_target(self.patrolPoint)

    @staticmethod
    def change_enemy_status(status):
        Enemy.enemy_status = status
        Enemy.enemy_status_time_left = Enemy.enemy_status.value[2]

    @staticmethod
    def reset_enemy_status_time():
        Enemy.enemy_status_time_left = Enemy.enemy_status.value[2]


class Node(Entity):
    """
    Nodes are points on the map were enemies depend on
    to patrol. They are like bus stops for them
    """

    def __init__(self, start_pos):
        super().__init__(start_pos)
        self.behaviour = None
        self.destination_point = 0
        self.nodes = []

    def join_node(self, nextNode):
        if nextNode not in self.nodes:
            self.nodes.append(nextNode)
        if self not in nextNode.nodes:
            nextNode.nodes.append(self)

    def remove_node(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
            node.remove_node(self)


    # If biased the last node on the list will 
    # get an advantage to be picked
    # so the enemy will be less probable to run
    # in circles between two nodes
    def pick_random_node(self, biased=False):
        import random
        node_list = self.nodes.copy()

        if biased:  
            for x in range(int( len(self.nodes)*0.5 ) ):
                node_list.append( node_list[-1] )


        if len(node_list) > 0:
            node_pos = random.randint(0, len(node_list) - 1)
            return node_list[node_pos]
        else:
            return self

# tbh I don't know why I created this class
# this is a basically an enemy that produces
# sounds.
class Monster(Enemy):
    def __init__(self, start_pos, patrolPoint=None):
        super().__init__(start_pos, patrolPoint=patrolPoint)
        self.sound = None
        self.channel = None
    def update(self, dt, events):
        import os
        super().update(dt, events)
        if self.channel == None:
            self.channel = pygame.mixer.find_channel(True)

        
        if self.target is not None:
            dist_to_player = mathHelpers.distance_to(self.get_pos(), Player.instance.get_pos())
            if isinstance(self.target, Player) and dist_to_player < 3 and self.canSeePlayer:
                self.attack(self.target, dt)
            if isinstance(self.target, Player) and dist_to_player < 3 and not self.canSeePlayer:
                self.look_at(self.target, dt)
        if dist_to_player < 5:
            self.play_sound(dist_to_player, Enemy.enemy_status.name)
        

        
    
    def play_sound(self, distance, flag, force=False):
        volume = mathHelpers.translate(distance, 0, 5, 2, 0.5 )
        self.sound = gameIO.get_audio(self.agent_pack_name, flag )
        if not self.channel.get_busy(): # Do not play two sounds at the same time
            if self.sound != None:
                self.channel.play(self.sound)
                self.channel.set_volume(volume, volume)
        else:
            if force:
                self.sound.play()
    
    def attack(self, target, dt):
        import random
        self.look_at(self.target, dt * 2)
        self.target.health -= dt * 30
        self.target.look_at(self, dt)
        self.target.angleY +=  dt * random.randint(-400, 400)
        self.target.rotate(dt * random.randint(-3, 3))
        dist_to_player = mathHelpers.distance_to(self.get_pos(), Player.instance.get_pos())
        self.play_sound(dist_to_player, "Attack", True)
        
class Collectible(SpriteEntity):
    def __init__(self, start_pos):
        super().__init__(start_pos, "Collectible")
        self.collected = False
    def update(self, dt, events):
        if not self.collected:
            dist = mathHelpers.distance_to(self.get_pos(), Player.instance.get_pos())
            if dist < 0.5:
                levelData.Level.currentMap.num_of_collected += 1
                self.collected = True
                self.agent_pack_name = ""


class Gate(SpriteEntity):
    def __init__(self, start_pos):
        super().__init__(start_pos, "Gate")
        self.open = False #Depends on a key class to be opened

    def update(self, dt, events):
        if not self.open:
            dist = mathHelpers.distance_to(self.get_pos(), Player.instance.get_pos())
            if not self.open:
                if dist < 0.5:
                    if Player.instance.keys > 0:
                        Player.instance.keys -= 1
                        self.open= True
                        self.agent_pack_name = ""
                elif dist < 1 and Player.instance.keys == 0:
                    Player.instance.move(-Player.instance.dirX * 0.5, -Player.instance.dirY * 0.5, dt)

class Key(SpriteEntity):
    def __init__(self, start_pos):
        super().__init__(start_pos, "Key")
        self.collected = False

    def update(self, dt, events):
        if not self.collected:
            dist = mathHelpers.distance_to(self.get_pos(), Player.instance.get_pos())
            if dist < 0.5:
                Player.instance.keys += 1
                self.collected = True
                self.agent_pack_name = ""

# I was using this test global var to tweak some values while I played. 
testGlobalVar = 0
def get_input(entity, dt, events):
    global testGlobalVar
    deltaTime = dt

    kb = pygame.key.get_pressed()
    for event in events:
        if event.type == pyConst.KEYDOWN:
            if event.key == pyConst.K_ESCAPE:
                pygame.mouse.set_pos(
                    [renderer.SCREEN_WIDTH//2,
                        renderer.SCREEN_HEIGHT//2])
                entity.mouseEnable = not entity.mouseEnable
 
    pygame.mouse.set_visible(not entity.mouseEnable)
    pygame.event.set_grab(entity.mouseEnable)
    if entity.mouseEnable:

        mouse_pos = pygame.mouse.get_pos()
        pygame.mouse.set_pos(
            [renderer.SCREEN_WIDTH//2,
                renderer.SCREEN_HEIGHT//2])
        mouseDeltaX =  (mouse_pos[0] - renderer.SCREEN_WIDTH//2)
        mouseDeltaY =  (mouse_pos[1] - renderer.SCREEN_HEIGHT//2)
        entity.rotate(-entity.cameraYawSens * 0.05 * deltaTime * mouseDeltaX)

        entity.angleY -= 0.05 * deltaTime * entity.cameraPitchSens * mouseDeltaY
    

    if kb[pyConst.K_LEFT]:
        entity.rotate(entity.cameraYawSens * deltaTime)


    if kb[pyConst.K_RIGHT]:
        entity.rotate(-entity.cameraYawSens * deltaTime)

    if kb[pyConst.K_UP]:
        entity.angleY += entity.cameraPitchSens * deltaTime

    if kb[pyConst.K_DOWN]:
        entity.angleY -= entity.cameraPitchSens * deltaTime

    newPx = 0
    newPy = 0
    angle = math.atan2(-entity.dirY, entity.dirX)

    entity.angleY = mathHelpers.clamp(
        entity.angleY, -renderer.VIEWPORT_HEIGHT, renderer.VIEWPORT_HEIGHT)

    if kb[pyConst.K_d]:
        newPx -= math.sin(angle) * 2 * deltaTime
        newPy -= math.cos(angle) * 2 * deltaTime

        

    if kb[pyConst.K_a]:
        newPx += math.sin(angle) * entity.moveSpeed * deltaTime
        newPy += math.cos(angle) * entity.moveSpeed * deltaTime
        
    if kb[pyConst.K_w]:
        newPx += math.cos(angle) * entity.moveSpeed * deltaTime
        newPy -= math.sin(angle) * entity.moveSpeed * deltaTime 

    if kb[pyConst.K_s]:
        newPx -= math.cos(angle) * entity.moveSpeed * deltaTime
        newPy += math.sin(angle) * entity.moveSpeed * deltaTime

        
        

    #Used for prototyping purposes see line: 468
    if kb[pyConst.K_n]:
        testGlobalVar -= 1 * deltaTime
        print(testGlobalVar)

    if kb[pyConst.K_m]:
        testGlobalVar += 1 * deltaTime
        print(testGlobalVar)

    entity.move(newPx, newPy, deltaTime)