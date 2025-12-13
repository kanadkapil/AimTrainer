import pygame


class InputHandler:
    def __init__(self):
        self.mouse_pos = (0, 0)
        self.mouse_clicked = False
        self.quit_game = False

    def process_input(self):
        self.mouse_clicked = False
        self.quit_game = False

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.quit_game = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.mouse_clicked = True

        self.mouse_pos = pygame.mouse.get_pos()
        return events
