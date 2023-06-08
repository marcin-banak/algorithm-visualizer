import copy
from math import ceil

from pygame import *
from CONST import *
from mouse import *
from pole import *
from button import *

class Main:
    def __init__(self):
        init()
        self.screen = display.set_mode(SCREEN_SIZE)
        self.draw_screen = Surface(DRAW_SCREEN_SIZE)
        self.font = pygame.font.Font("font.ttf", BUTTON_FONT_SIZE)
        display.set_caption("Algorithm visualizer")

        self.poles = []
        self.ended = None
        self.algorithm = None
        self.algorithm_generator = None

        self.buttons = []
        self.init_menu()

        self.scene = self.menu
        self.mouse = Mouse()
        self.is_running = True
        self.clock = time.Clock()
        self.last_update = time.get_ticks()
        self.dt = 1

        while self.is_running:
            self.check_events()
            self.scene()
            self.display_update()
        quit()

    def check_events(self):
        self.mouse.update(SCREEN_SIZE)
        for e in event.get():
            if e.type == QUIT:
                self.is_running = False

    def display_update(self):
        self.dt = self.clock.tick(FPS) * 60 / 1000
        self.screen.blit(pygame.transform.scale(self.draw_screen, SCREEN_SIZE), (0, 0))
        display.update()

    def init_menu(self):
        self.poles = []
        self.algorithm_generator = None
        self.ended = False
        self.scene = self.menu
        self.buttons.append(Button(Vector2(BUTTONS_HORIZONTAL_DISTANCE + 80, BUTTONS_VERTICAL_DISTANCE), BUTTON_SIZE, "Bubble sort"))
        self.buttons.append(Button(Vector2(BUTTONS_HORIZONTAL_DISTANCE + 80, BUTTONS_VERTICAL_DISTANCE + BUTTONS_INTERVAL), BUTTON_SIZE, "Select sort"))
        self.buttons.append(Button(Vector2(BUTTONS_HORIZONTAL_DISTANCE + 80, BUTTONS_VERTICAL_DISTANCE + 2 * BUTTONS_INTERVAL), BUTTON_SIZE, "Insert sort"))

    def menu(self):
        for button in self.buttons:
            button.update(self.mouse)
            if button.clicked:
                if button.text == "Bubble sort":
                    self.algorithm = self.bubbleSort
                elif button.text == "Select sort":
                    self.algorithm = self.selectionSort
                elif button.text == "Insert sort":
                    self.algorithm = self.insertionSort
                self.init_program()
        self.draw_menu()

    def draw_menu(self):
        self.draw_screen.fill(BLACK)
        for button in self.buttons:
            draw.rect(self.draw_screen, GREY, (button.pos.x, button.pos.y, BUTTON_SIZE.x, BUTTON_SIZE.y))
            self.draw_screen.blit(self.font.render(button.text, True, BLACK), Vector2(button.pos.x + 20, button.pos.y + (BUTTON_SIZE.y - BUTTON_FONT_SIZE) // 2))
        self.display_update()

    def init_program(self):
        self.poles = self.init_poles()
        self.algorithm_generator = self.algorithm()
        self.ended = False
        self.buttons = []
        self.scene = self.program

    def program(self):
        if (time.get_ticks() - self.last_update) / 1000 > ALGORITHMS_ANIMATION_SPEED:
            if self.ended:
                self.init_menu()
            else:
                self.generate()
            self.last_update = time.get_ticks()
        self.draw_program()

    def draw_program(self):
        self.draw_screen.fill(BLACK)
        for pole in self.poles:
            if pole.state == 0:
                draw.rect(self.draw_screen, WHITE, (pole.pos.x, pole.pos.y - (pole.val * POLE_SCALAR), POLES_WIDTH, pole.val * POLE_SCALAR))
            elif pole.state == 1:
                draw.rect(self.draw_screen, RED, (pole.pos.x, pole.pos.y - (pole.val * POLE_SCALAR), POLES_WIDTH, pole.val * POLE_SCALAR))
            else:
                draw.rect(self.draw_screen, YELLOW, (pole.pos.x, pole.pos.y - (pole.val * POLE_SCALAR), POLES_WIDTH, pole.val * POLE_SCALAR))
        self.display_update()

    def init_poles(self):
        poles = []
        for i in range(ceil((WIDTH_D - 2 * POLES_HORIZONTAL_DISTANCE) / (POLES_WIDTH + POLES_INTERVAL))):
            poles.append(Pole(Vector2(POLES_HORIZONTAL_DISTANCE + (POLES_WIDTH + POLES_INTERVAL) * i, HEIGHT_D - POLES_VERTICAL_DISTANCE)))
        poles[0].state = 1
        return poles

    def generate(self):
        try:
            next(self.algorithm_generator)
        except StopIteration:
            self.ended = True

    def bubbleSort(self):
        for i in range(len(self.poles) - 1):
            for j in range(len(self.poles) - i - 1):
                if j > 0:
                    self.poles[j - 1].state = 0
                if self.poles[j].val > self.poles[j + 1].val:
                    self.poles[j].val, self.poles[j + 1].val = self.poles[j + 1].val, self.poles[j].val
                    self.poles[j].state, self.poles[j + 1].state = 1, 2
                else:
                    self.poles[j].state, self.poles[j + 1].state = 1, 2
                self.draw_program()
                yield True
            self.poles[len(self.poles) - i - 1].state = 0
            self.poles[len(self.poles) - i - 2].state = 0

    def selectionSort(self):
        for i in range(len(self.poles)):
            min_index = i
            self.poles[min_index].state = 1
            for j in range(i + 1, len(self.poles)):
                self.poles[j - 1].state = 0
                if self.poles[min_index].val > self.poles[j].val:
                    self.poles[min_index].state = 0
                    min_index = j
                self.poles[j].state = 2
                self.poles[min_index].state = 1
                self.draw_program()
                yield
            (self.poles[i].val, self.poles[min_index].val) = (self.poles[min_index].val, self.poles[i].val)
            self.poles[min_index].state = 0
            self.poles[len(self.poles) - 1].state = 0

    def insertionSort(self):
        for i in range(1, len(self.poles)):
            self.poles[i - 1].state = 0
            key = self.poles[i].val
            j = i - 1
            while j >= 0 and key < self.poles[j].val:
                self.poles[j + 1].val = self.poles[j].val
                j -= 1
                self.poles[j + 2].state = 0
                self.poles[j + 1].state = 1
                self.poles[j].state = 2
                self.draw_program()
                yield
            self.poles[j + 1].val = key
            self.poles[j].state = 0
            self.poles[j + 1].state = 0


if __name__ == "__main__":
    Main()