import pygame
import pygame.camera
import time

pygame.init()

class Player(object):
    displaysize = (480, 435)
    capturesize = ( 480, 420 )
    mirror = True
    delay = 0
    font = pygame.font.SysFont(None,25)
    text = font.render("Rover: video streaming", True, (255,255,255))
    def __init__(self, **argd):
        self.__dict__.update(**argd)
        super(Player, self).__init__(**argd)
        self.display = pygame.display.set_mode( self.displaysize )
        pygame.camera.init()
        self.camera = X=pygame.camera.Camera("/dev/video0", self.capturesize)
        print pygame.camera.list_cameras()
        self.camera.start()

    def get_and_flip(self):
        snapshot = self.camera.get_image()
        snapshot = pygame.transform.scale(snapshot,(480,420))
        self.display.blit(snapshot,(0,0))
        self.display.blit(self.text, (2,415))
        pygame.display.set_caption("Video")
        pygame.display.update()

    def main(self):
        while 1:
            time.sleep(self.delay)
            self.get_and_flip()
