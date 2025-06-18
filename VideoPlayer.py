import pygame, cv2, numpy as np

class VideoPlayer :
    def __init__(self, path, size, screen):
        self.cap = cv2.VideoCapture(path)
        self.size = (int(size[0]), int(size[1]))
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.fps = int( self.cap.get( cv2.CAP_PROP_FPS ) )
        if self.fps == 0:
            self.fps = 120

    def play(self):

        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, self.size)
        frame_surface = pygame.surfarray.make_surface(np.rot90(frame))
        self.screen.blit(frame_surface, (0, 0))

        self.clock.tick(self.fps)

    def restart(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def release(self):
        self.cap.release()