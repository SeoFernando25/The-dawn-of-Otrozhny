# Just placed some draw functions here because 
# otherwise it would become messy
import textDraw
import renderer
import colors
import entities

def render_tutorial_tab_1():
    textDraw.message_display_MB(
                renderer.SCREEN,
                "Enemy Status",
                renderer.SCREEN_WIDTH//1.5, renderer.VIEWPORT_Y_OFFSET * 1.5,
                20, color=colors.RED)

    row = 0
    textDraw.message_display_L(
        renderer.SCREEN,
        "Enemy status refers to various states of alert that",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 1
    textDraw.message_display_L(
        renderer.SCREEN,
        "affect the behaviour of enemy soldiers.",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 2
    textDraw.message_display_L(
        renderer.SCREEN,
        "NORMAL",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12, entities.EnemyStatus.Normal.value[1])

    textDraw.message_display_L(
        renderer.SCREEN,
        "While in Normal mode, enemy soldiers will ",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)

    row += 1

    textDraw.message_display_L(
        renderer.SCREEN,
        "follow a set patrol route.",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)

    row += 2

    textDraw.message_display_L(
        renderer.SCREEN,
        "Alert",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12, entities.EnemyStatus.Alert.value[1])

    textDraw.message_display_L(
        renderer.SCREEN,
        "This is the state in which the player has",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    
    row += 1
    
    textDraw.message_display_L(
        renderer.SCREEN,
        "been discovered by enemy soldiers. ",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 1
    textDraw.message_display_L(
        renderer.SCREEN,
        "enemy soldiers call for backup and attack.",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)

    row += 2

    textDraw.message_display_L(
        renderer.SCREEN,
        "Evasion",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12, entities.EnemyStatus.Evasion.value[1])

    textDraw.message_display_L(
        renderer.SCREEN,
        "Enemy soldiers will search the area",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)

    row += 1

    textDraw.message_display_L(
        renderer.SCREEN,
        "they last found the player",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)

    row += 2

    textDraw.message_display_L(
        renderer.SCREEN,
        "Caution",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12, entities.EnemyStatus.Caution.value[1])


    textDraw.message_display_L(
        renderer.SCREEN,
        "Enemy soldiers will search the vicinity",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)

    row += 1

    textDraw.message_display_L(
        renderer.SCREEN,
        "after losing sight of the player",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)


def render_tutorial_tab_2():
    textDraw.message_display_MB(
                renderer.SCREEN,
                "Map Editor",
                renderer.SCREEN_WIDTH//1.5, renderer.VIEWPORT_Y_OFFSET * 1.5,
                20, color=colors.RED)

    row = 0
    textDraw.message_display_L(
        renderer.SCREEN,
        "You can create and edit you levels in the level",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 1
    textDraw.message_display_L(
        renderer.SCREEN,
        "editor. You can share maps through the maps folder.",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 2


    textDraw.message_display_L(
        renderer.SCREEN,
        "NAV",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12, colors.YELLOW)

    textDraw.message_display_L(
        renderer.SCREEN,
        "You can edit and change node conections.",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)

    row += 1

    textDraw.message_display_L(
        renderer.SCREEN,
        "Making soldiers follow a set patrol route.",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)

    row += 2

    textDraw.message_display_L(
        renderer.SCREEN,
        "Draw",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12, colors.YELLOW)

    textDraw.message_display_L(
        renderer.SCREEN,
        "In draw mode you can add and remove",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    
    row += 1
    
    textDraw.message_display_L(
        renderer.SCREEN,
        "walls, as well as enemies and nodes",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)

    row += 2

    textDraw.message_display_L(
        renderer.SCREEN,
        "Wall",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12, colors.YELLOW)

    textDraw.message_display_L(
        renderer.SCREEN,
        "You can paint walls and add keys to them",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)

    row += 2

    textDraw.message_display_L(
        renderer.SCREEN,
        "Options",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12, colors.YELLOW)


    textDraw.message_display_L(
        renderer.SCREEN,
        "You can edit the settings of your map ",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)

    row += 1

    textDraw.message_display_L(
        renderer.SCREEN,
        "such as width and height",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)

def render_tutorial_tab_3():
    textDraw.message_display_MB(
                renderer.SCREEN,
                "Items and Objects",
                renderer.SCREEN_WIDTH//1.5, renderer.VIEWPORT_Y_OFFSET * 1.5,
                20, color=colors.RED)

    row = 0
    textDraw.message_display_L(
        renderer.SCREEN,
        "While on missions, you may find a variety of ",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 1
    textDraw.message_display_L(
        renderer.SCREEN,
        "items and obstacles",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 2


    textDraw.message_display_L(
        renderer.SCREEN,
        "Keys",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12, colors.YELLOW)

    textDraw.message_display_L(
        renderer.SCREEN,
        "Keys can open gates and allow you to",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)

    row += 1

    textDraw.message_display_L(
        renderer.SCREEN,
        "pass through before locked areas.",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)

    row += 2

    textDraw.message_display_L(
        renderer.SCREEN,
        "Gates",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12, colors.YELLOW)

    textDraw.message_display_L(
        renderer.SCREEN,
        "Gates block your path and may restrict",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    
    row += 1
    
    textDraw.message_display_L(
        renderer.SCREEN,
        "your way to an advantage point",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)

    row += 2

    textDraw.message_display_L(
        renderer.SCREEN,
        "Stars",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12, colors.YELLOW)

    textDraw.message_display_L(
        renderer.SCREEN,
        "Are collectables scattered around the",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)

    row += 1

    textDraw.message_display_L(
        renderer.SCREEN,
        "map. You need to collect all of them to",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)

    row += 1

    textDraw.message_display_L(
        renderer.SCREEN,
        "complete a mission",
        renderer.VIEWPORT_X_OFFSET * 10, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)

def render_tutorial_tab_4():
    textDraw.message_display_MB(
                renderer.SCREEN,
                "Briefing",
                renderer.SCREEN_WIDTH//1.5, renderer.VIEWPORT_Y_OFFSET * 1.5,
                20, color=colors.RED)

    row = 0
    textDraw.message_display_L(
        renderer.SCREEN,
        "JULY 2019: The human species is on the edge of",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 1
    textDraw.message_display_L(
        renderer.SCREEN,
        "extinction. ",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 2
    textDraw.message_display_L(
        renderer.SCREEN,
        "A geneticaly modified creature created by Kephart",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 1
    textDraw.message_display_L(
        renderer.SCREEN,
        "corporations of Keter class named by SPC-610 was",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 1
    textDraw.message_display_L(
        renderer.SCREEN,
        "recently denounced uncontained of level Red after",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 1
    textDraw.message_display_L(
        renderer.SCREEN,
        "members from Area-683 lost direct contact to",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 1
    textDraw.message_display_L(
        renderer.SCREEN,
        "I DATA EXPUNGED I . Locals from Otrozhny in the ",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 1
    textDraw.message_display_L(
        renderer.SCREEN,
        "Russia Confederation also recently reported ",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 1
    textDraw.message_display_L(
        renderer.SCREEN,
        "anomalous sounds comming from Area-683.",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 2
    textDraw.message_display_L(
        renderer.SCREEN,
        "Fortunately, one of the officers was able to",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 1
    textDraw.message_display_L(
        renderer.SCREEN,
        "contact HQ via a 2000 MK VI Transreciever.",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 1
    textDraw.message_display_L(
        renderer.SCREEN,
        "More details will be availible ASAP",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 1
    textDraw.message_display_L(
        renderer.SCREEN,
        "I End of transmission I",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)

def render_tutorial_tab_5():
    textDraw.message_display_MB(
                renderer.SCREEN,
                "Unauthorized",
                renderer.SCREEN_WIDTH//1.5, renderer.VIEWPORT_Y_OFFSET * 1.5,
                20, color=colors.RED)

    row = 0
    textDraw.message_display_L(
        renderer.SCREEN,
        "Error 401 - Unauthorized",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12, colors.RED)
    row += 2
    textDraw.message_display_L(
        renderer.SCREEN,
        "You do not have permission to view this directory",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12, color=colors.RED)
    row += 2
    textDraw.message_display_L(
        renderer.SCREEN,
        "olssv, ty ztpao",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 1
    textDraw.message_display_L(
        renderer.SCREEN,
        "pm fvb hyl zllpun aopz tlzzhnl jvunyhabshapvuz.",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 1
    textDraw.message_display_L(
        renderer.SCREEN,
        "bumvyabuhalsf, aol zavyf pz zapss pujvtwslal ",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 1
    textDraw.message_display_L(
        renderer.SCREEN,
        "huk pa thf ulcly dpss p zhk ltvqp p . wslhzl ",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
    row += 1
    textDraw.message_display_L(
        renderer.SCREEN,
        "jvtl ihjr shaly.",
        renderer.VIEWPORT_X_OFFSET, renderer.VIEWPORT_Y_OFFSET * 2 + 20 * row,
        12)
   



 

