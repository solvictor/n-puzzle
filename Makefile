NAME = n-puzzle
PROJECT_NAME = n-puzzle

# Utils
ERASE_L = \033[K
CURS_UP = \033[A
SAVE_CURS_POS = \033[s
LOAD_CURS_SAVE = \033[u
BOLD = \033[1m
BLINK = \033[5m

# Reset
NC = \033[0m

# Colors
YELLOW = \033[0;33m
GREEN = \033[0;32m
BLUE = \033[0;34m
RED = \033[0;31m
PURPLE = \033[0;35m
CYAN = \033[0;36m
BLACK = \033[0;30
WHITE = \033[0;37m

# Colors
BYELLOW = \033[1;33m
BGREEN = \033[1;32m
BBLUE = \033[1;34m
BRED = \033[1;31m
BPURPLE = \033[1;35m
BCYAN = \033[1;36m
BBLACK = \033[1;30m
BWHITE = \033[1;37m

# Bg colors
GREEN_BG = \033[48;5;2m

help:
	@python3 sources/n-puzzle.py -h

clean:
	@find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	@echo "[🧼] $(BYELLOW)Cache $(YELLOW)files have been cleaned from $(PROJECT_NAME) ✔️$(NC)\n"
