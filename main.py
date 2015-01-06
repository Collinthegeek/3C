import pygame
import math
import time
import os
import rendermodule
from pygame.locals import *
from map1 import map1
import dumbmenu as dm

try:
    import android
except ImportError:
    android = None

red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255

sprite_positions = [
    #(20.5, 11.5, 0),
]


def load_image(image, darken, colorKey = None):
    ret = []
    if colorKey is not None:
        image.set_colorkey(colorKey)
    if darken:
        image.set_alpha(127)
    for i in range(image.get_width()):
        s = pygame.Surface((1, image.get_height())).convert()
        s.blit(image, (- i, 0))
        if colorKey is not None:
            s.set_colorkey(colorKey)
        ret.append(s)
    return ret


def main():

    t = time.clock()
    oldTime = 0.
    pygame.mixer.init()
    sound = 0
    sstate = "On"
    gunsound = pygame.mixer.Sound(os.path.join('sound', 'gun.wav'))
    pygame.init()
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    map = map1
    Fullscreen = True
    f = pygame.font.SysFont(pygame.font.get_default_font(), 50)
    wm = rendermodule.WorldManager(map, sprite_positions, 22, 11.5, -1, 0, 0, .66)
    gun = pygame.image.load("img/gun.png")
    gun = pygame.transform.scale2x(gun)
    gun = pygame.transform.scale2x(gun)
    ret = pygame.image.load("img/ret.png")
    ret = pygame.transform.scale2x(ret)
    ret = pygame.transform.scale2x(ret)
    pygame.event.set_grab(True)
    pygame.display.set_caption("Collin's Game")

    # Android version coming soon... maybe!
    if android:
        android.init()
        android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)


        pygame.key.set_repeat(500,30)

    while(True):
        clock.tick(60)
        
        # Android-specific:
        if android:
            if android.check_pause():
                android.wait_for_resume()

        wm.draw(screen)

        frameTime = float(clock.get_time()) / 1000.0  # frameTime is the time this frame has taken, in seconds
        t = time.clock()
        if sound == 0:
            sstate = "On"
        if sound == 1:
            sstate = "Muted"
        fps = clock.get_fps()
        text = f.render(str(fps), False, (255, 255, 0))
        screen.blit(text, text.get_rect(), text.get_rect())
        screen.blit(gun, (screen.get_width()/2 - gun.get_width()/2, screen.get_height()-gun.get_height()))
        screen.blit(ret, (screen.get_width()/2 - ret.get_width()/2, screen.get_height()/2 - ret.get_height()/2 ))
        gun = pygame.image.load("img/gun.png")
        gun = pygame.transform.scale2x(gun)
        gun = pygame.transform.scale2x(gun)
        if sound > 1:
            sound = 0
        pygame.display.flip()

        moveSpeed = frameTime * 2.0
        rotSpeed = frameTime * 2.0


        look_x, look_y = pygame.mouse.get_rel()

        for event in pygame.event.get(): 
            if event.type == QUIT: 
                return 
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:

                    screen.fill(blue)
                    pygame.display.update()
                    pygame.key.set_repeat(500,30)

                    choose = dm.dumbmenu(screen, [
                        'Resume',
                        'Options',
                        'Help',
                        'Quit Game'], 64,64,None,32,1.4,green,red)

                    if choose == 0:
                        print "You choose 'Start Game'."
                    elif choose == 1:

                        screen.fill(blue)
                        pygame.display.update()
                        pygame.key.set_repeat(500,30)

                        choose = dm.dumbmenu(screen, [
                            'Full-Screen',
                            'TexturePacks',
                            'Back'], 64,64,None,32,1.4,green,red)

                        if choose == 0:
                            if Fullscreen == True:
                                screen = pygame.display.set_mode(size)
                                Fullscreen = False
                            else:
                                screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                                Fullscreen = True
                        elif choose == 1:
                            print "You choose 'TexturePacks'."
                        elif choose == 2:
                            break

                    elif choose == 2:
                        print "You choose 'Manual'."
                    elif choose == 3:
                        return

                elif event.key == K_m:
                    sound = sound + 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gun = pygame.image.load("img/gun2.png")
                gun = pygame.transform.scale2x(gun)
                gun = pygame.transform.scale2x(gun)
                if sound == 0:
                    gunsound.play()
        
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            # move forward if no wall in front of you
            moveX = wm.camera.x + wm.camera.dirx * moveSpeed
            if(map[int(moveX)][int(wm.camera.y)]==0 and map[int(moveX + 0.1)][int(wm.camera.y)]==0):wm.camera.x += wm.camera.dirx * moveSpeed
            moveY = wm.camera.y + wm.camera.diry * moveSpeed
            if(map[int(wm.camera.x)][int(moveY)]==0 and map[int(wm.camera.x)][int(moveY + 0.1)]==0):wm.camera.y += wm.camera.diry * moveSpeed
        if keys[K_s]:
            # move backwards if no wall behind you
            if(map[int(wm.camera.x - wm.camera.dirx * moveSpeed)][int(wm.camera.y)] == 0):wm.camera.x -= wm.camera.dirx * moveSpeed
            if(map[int(wm.camera.x)][int(wm.camera.y - wm.camera.diry * moveSpeed)] == 0):wm.camera.y -= wm.camera.diry * moveSpeed
        if (look_x > 0.5 and not keys[K_DOWN]) or (keys[K_LEFT] and keys[K_DOWN]):
            # rotate to the right
            # both camera direction and camera plane must be rotated
            oldDirX = wm.camera.dirx
            wm.camera.dirx = wm.camera.dirx * math.cos(- rotSpeed) - wm.camera.diry * math.sin(- rotSpeed)
            wm.camera.diry = oldDirX * math.sin(- rotSpeed) + wm.camera.diry * math.cos(- rotSpeed)
            oldPlaneX = wm.camera.planex
            wm.camera.planex = wm.camera.planex * math.cos(- rotSpeed) - wm.camera.planey * math.sin(- rotSpeed)
            wm.camera.planey = oldPlaneX * math.sin(- rotSpeed) + wm.camera.planey * math.cos(- rotSpeed)
        if (look_x < -0.5 and not keys[K_DOWN]) or (keys[K_RIGHT] and keys[K_DOWN]): 
            # rotate to the left
            # both camera direction and camera plane must be rotated
            oldDirX = wm.camera.dirx
            wm.camera.dirx = wm.camera.dirx * math.cos(rotSpeed) - wm.camera.diry * math.sin(rotSpeed)
            wm.camera.diry = oldDirX * math.sin(rotSpeed) + wm.camera.diry * math.cos(rotSpeed)
            oldPlaneX = wm.camera.planex
            wm.camera.planex = wm.camera.planex * math.cos(rotSpeed) - wm.camera.planey * math.sin(rotSpeed)
            wm.camera.planey = oldPlaneX * math.sin(rotSpeed) + wm.camera.planey * math.cos(rotSpeed)

if __name__ == '__main__':   
    main()

