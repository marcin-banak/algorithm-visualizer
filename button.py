from pygame import *
from CONST import *


class Button:
    def __init__(self, pos, size, text):
        self.text = text
        self.pos = pos
        self.rect = Rect(0, 0, size.x, size.y)
        self.rect.center = Vector2(pos.x + size.x // 2, pos.y + size.y // 2)
        self.state = "normal"
        self.clicked = False

    def update(self, mouse):
        if self.rect.colliderect(mouse.rect):
            if mouse.click_switch:
                if self.state == "normal":
                    self.sound_to_play = "touch"
                self.state = "touched"
            else:
                self.state = "clicked"
            if mouse.click and not self.clicked:
                self.state = "clicked"
                self.clicked = True
                self.sound_to_play = "click"
        elif mouse.click and self.clicked:
            self.state = "normal"
            self.clicked = False