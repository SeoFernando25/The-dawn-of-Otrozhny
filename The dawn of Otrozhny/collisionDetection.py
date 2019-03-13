# Basic math functions
# Nothing to look here
import math
import mathHelpers

def pointCircleCollision(point_pos, circle_pos, circle_radius):
    distX, distY = mathHelpers.slope(point_pos, circle_pos) 
    distance = math.hypot(distX, distY)
    return distance <= circle_radius


def polygonPointCollision(vertices, point):
    # I used the even odd rule for polygon collision
    # see: https://en.wikipedia.org/wiki/Even%E2%80%93odd_rule
    collision = False

    nextP = 0

    for current in range(len(vertices)):
        nextP += 1

        if (nextP == len(vertices)):
            nextP = 0

    
        vc = vertices[current]
        vn = vertices[nextP]

       
        if (((vc[1] > point[1] and vn[1] < point[1]) or (vc[1] < point[1] and vn[1] > point[1])) and
            (point[0] < (vn[0]-vc[0])*(point[1]-vc[1]) / (vn[1]-vc[1])+vc[0])):
                collision = not collision
        
    
    return collision