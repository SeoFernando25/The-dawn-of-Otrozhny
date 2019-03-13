import textDraw
import pygame

def truncline(text, maxwidth, font):
    text = str(text)
    real = len(text)
    stext = text
    l = font.size(text)[0]
    cut = 0
    a = 0
    done = 1
    old = None
    while l > maxwidth:
        a = a + 1
        n = text.rsplit(None, a)[0]
        if stext == n:
            cut += 1
            stext = n[:-cut]
        else:
            stext = n
        l = font.size(stext)[0]
        real = len(stext)
        done = 0
    return real, done, stext


def wrapline(text, pixelMaxwidth, size):
    done = 0
    wrapped = []
    for f, f_size in textDraw.font_cache:
        if f_size == size:
            font = f
    else:
        font = pygame.font.Font(textDraw.FONT_PATH, size)
    while not done:
        nl, done, stext = truncline(text, pixelMaxwidth, font)
        wrapped.append(stext.strip())
        text = text[nl:]
    return wrapped

#Demo of text wrapping
if __name__ == "__main__":  
    import ui
    import colors   
    import pygame
    
    pygame.init()
    screen = pygame.display.set_mode( (300,200))
    hudb = ui.HudButton( 300, 200)
    hudb.set_text("THIS IS A TEST OF A REALLY BIG SENTENCE BEING WRAPPED")
    clock = pygame.time.Clock()
    import textDraw
    while 1:
        pygame.event.pump()
        screen.fill(colors.WHITE)
        hudb.set_active(True)
        screen.blit(hudb, (0,0))
        pygame.display.flip()
        clock.tick(10)
