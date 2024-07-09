import pygame
import sys


class Visualizer:
    def __init__(self, size, tile_size=100, background_color=(0, 0, 0), tile_color=(255, 255, 255), tile_text_color=(0, 0, 0), font_size=36):
        self.size = size
        self.tile_size = tile_size
        self.grid_size = size * tile_size
        self.background_color = background_color
        self.tile_color = tile_color
        self.tile_text_color = tile_text_color
        self.font_size = font_size
        self.border = 2
        self.font = pygame.font.SysFont("Consolas", font_size)
        self.screen = pygame.display.set_mode((self.grid_size, self.grid_size))
        pygame.display.set_caption("n-puzzle")

    def draw_tile(self, number, position):
        if number == 0:
            return
        x, y = position
        rect = pygame.Rect(x * self.tile_size + self.border // 2, y * self.tile_size + self.border // 2, self.tile_size - self.border, self.tile_size - self.border)
        pygame.draw.rect(self.screen, self.tile_color, rect, border_radius=20)
        text = self.font.render(str(number), True, self.tile_text_color)
        text_rect = text.get_rect(center=rect.center)
        self.screen.blit(text, text_rect)

    def draw_board(self, board):
        self.screen.fill(self.background_color)
        for i, number in enumerate(board):
            y, x = divmod(i, self.size)
            self.draw_tile(number, (x, y))
        pygame.display.flip()

    def apply_move(self, board, move):
        empty = board.index(0)
        y, x = divmod(empty, self.size)
        new_y = y + (1 if move == 'v' else -1 if move == '^' else 0)
        new_x = x + (1 if move == '>' else -1 if move == '<' else 0)
        if 0 <= new_x < self.size and 0 <= new_y < self.size:
            new_index = new_y * self.size + new_x
            board[empty], board[new_index] = board[new_index], board[empty]

    def start(self, puzzle, solution):
        clock = pygame.time.Clock()
        move_index = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            if move_index < len(solution):
                self.apply_move(puzzle, solution[move_index])
                move_index += 1

            self.draw_board(puzzle)
            clock.tick(5)


def start(puzzle, size, solution):
    visu = Visualizer(size, background_color=(93, 115, 126), tile_text_color=(218, 255, 239), tile_color=(100, 182, 172))
    visu.start(puzzle, solution)


pygame.init()
