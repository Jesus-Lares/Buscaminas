import pygame
import sys

width=400
height=400

def main():
    pygame.init()
    pygame.display.set_mode((width,height))
    pygame.display.set_caption("Buscaminas")

    clock = pygame.time.Clock()

    openInterface = True

    while openInterface:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.flip()
    

if __name__ == "__main__":
    main()