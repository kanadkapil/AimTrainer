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
        self.state = "MENU"  # MENU, PLAYING, PAUSED, GAMEOVER
        self.mode = None

        self.input_handler = InputHandler()
        self.hud = HUD()

        # Menu Buttons
        self.btn_flick = Button(
            SCREEN_WIDTH // 2 - 100,
            200,
            200,
            50,
            "Flick Mode",
            self.font,
            GRAY,
            GREEN,
            self.start_flick,
        )
        self.btn_survival = Button(
            SCREEN_WIDTH // 2 - 100,
            270,
            200,
            50,
            "Survival Mode",
            self.font,
            GRAY,
            RED,
            self.start_survival,
        )
        self.btn_quit = Button(
            SCREEN_WIDTH // 2 - 100,
            340,
            200,
            50,
            "Quit",
            self.font,
            GRAY,
            RED,
            self.quit_game,
        )

        # Game Over Buttons
        self.btn_restart = Button(
            SCREEN_WIDTH // 2 - 100,
            SCREEN_HEIGHT // 2 + 20,
            200,
            50,
            "Restart",
            self.font,
            GRAY,
            GREEN,
            self.restart_game,
        )
        self.btn_menu = Button(
            SCREEN_WIDTH // 2 - 100,
            SCREEN_HEIGHT // 2 + 90,
            200,
            50,
            "Main Menu",
            self.font,
            GRAY,
            BLUE,
            self.return_to_menu,
        )

    def quit_game(self):
        self.running = False

    def start_flick(self):
        from src.gameplay.modes import FlickMode

        self.mode = FlickMode()
        self.state = "PLAYING"

    def start_survival(self):
        from src.gameplay.modes import SurvivalMode

        self.mode = SurvivalMode()
        self.state = "PLAYING"

    def restart_game(self):
        if isinstance(self.mode, type(self.mode)):
            # Re-instantiate current mode class
            # Check type and re-create
            from src.gameplay.modes import FlickMode, SurvivalMode

            if isinstance(self.mode, FlickMode):
                self.start_flick()
            elif isinstance(self.mode, SurvivalMode):
                self.start_survival()

    def return_to_menu(self):
        self.state = "MENU"
        self.mode = None

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

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == "PLAYING":
                        self.state = "PAUSED"
                    elif self.state == "PAUSED":
                        self.state = "PLAYING"

            if self.state == "MENU":
                self.btn_flick.handle_event(event)
                self.btn_survival.handle_event(event)
                self.btn_quit.handle_event(event)
            elif self.state == "GAMEOVER":
                self.btn_restart.handle_event(event)
                self.btn_menu.handle_event(event)
            elif self.state == "PAUSED":
                # Simple pause handling, maybe add Resume button later or just ESC to resume
                pass

            elif self.state == "PLAYING":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.mode:
                        self.mode.handle_click(event.pos)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.state == "MENU":
            self.btn_flick.update(mouse_pos)
            self.btn_survival.update(mouse_pos)
            self.btn_quit.update(mouse_pos)
        elif self.state == "PLAYING":
            if self.mode:
                self.mode.update()
                if self.mode.game_over:
                    self.state = "GAMEOVER"
        elif self.state == "GAMEOVER":
            self.btn_restart.update(mouse_pos)
            self.btn_menu.update(mouse_pos)

    def draw(self):
        self.screen.fill(BG_COLOR)

        if self.state == "MENU":
            self.draw_text("Aim Trainer", SCREEN_WIDTH // 2, 100, 50)
            self.btn_flick.draw(self.screen)
            self.btn_survival.draw(self.screen)
            self.btn_quit.draw(self.screen)

        elif self.state == "PLAYING":
            if self.mode:
                self.mode.draw(self.screen)
                self.hud.draw(self.screen, self.mode.score, self.mode.lives)

        elif self.state == "PAUSED":
            # Draw game freeze frame
            if self.mode:
                self.mode.draw(self.screen)

            # Overlay
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            s.set_alpha(128)
            s.fill(BLACK)
            self.screen.blit(s, (0, 0))
            self.draw_text("PAUSED", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        elif self.state == "GAMEOVER":
            if self.mode:
                self.mode.draw(self.screen)  # Draw background still

            # Overlay
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            s.set_alpha(200)
            s.fill(BLACK)
            self.screen.blit(s, (0, 0))

            self.draw_text(
                "GAME OVER",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 50,
                size=50,
                color=RED,
            )
            score = self.mode.score if self.mode else 0
            self.draw_text(
                f"Final Score: {score}", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, size=30
            )

            self.btn_restart.draw(self.screen)
            self.btn_menu.draw(self.screen)

        pygame.display.flip()

    def draw_text(self, text, x, y, size=30, color=WHITE):
        font = pygame.font.SysFont("Arial", size)
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(x, y))
        self.screen.blit(surface, rect)
