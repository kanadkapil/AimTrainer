import pygame
import sys
from .settings import *
from .input import InputHandler
from src.ui.menu import Button
from src.ui.hud import HUD


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

        self.running = True
        self.state = "MENU"  # MENU, PLAYING, GAMEOVER
        self.mode = None

        self.input_handler = InputHandler()
        self.hud = HUD()

        # Menu Buttons
        self.play_btn = Button(
            SCREEN_WIDTH // 2 - 100,
            SCREEN_HEIGHT // 2 - 25,
            200,
            50,
            "Play Flick Mode",
            self.font,
            GRAY,
            GREEN,
            self.start_game,
        )
        self.quit_btn = Button(
            SCREEN_WIDTH // 2 - 100,
            SCREEN_HEIGHT // 2 + 50,
            200,
            50,
            "Quit",
            self.font,
            GRAY,
            RED,
            self.quit_game,
        )

    def quit_game(self):
        self.running = False

    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        events = self.input_handler.process_input()
        if self.input_handler.quit_game:
            self.running = False

        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == "PLAYING":
                        self.state = "MENU"
                        self.mode = None  # Reset mode?
                    else:
                        self.running = False

            if self.state == "MENU":
                self.play_btn.handle_event(event)
                self.quit_btn.handle_event(event)

            elif self.state == "PLAYING":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.mode:
                        hit = self.mode.handle_click(event.pos)

    def start_game(self):
        from src.gameplay.modes import FlickMode

        self.mode = FlickMode()
        self.state = "PLAYING"

    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.state == "MENU":
            self.play_btn.update(mouse_pos)
            self.quit_btn.update(mouse_pos)
        elif self.state == "PLAYING":
            if self.mode:
                self.mode.update()

    def draw(self):
        self.screen.fill(BG_COLOR)

        if self.state == "MENU":
            self.draw_text("Aim Trainer", SCREEN_WIDTH // 2, 100, 50)
            self.play_btn.draw(self.screen)
            self.quit_btn.draw(self.screen)
        elif self.state == "PLAYING":
            if self.mode:
                self.mode.draw(self.screen)
            self.hud.draw(self.screen, self.mode.score if self.mode else 0)
        elif self.state == "GAMEOVER":
            self.draw_text("Game Over", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        pygame.display.flip()

    def draw_text(self, text, x, y, size=30, color=WHITE):
        # Override default font for custom size if needed, or just use default
        font = pygame.font.SysFont("Arial", size)
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(x, y))
        self.screen.blit(surface, rect)
