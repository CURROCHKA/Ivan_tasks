# import pygame
#
# pygame.init()
# screen = pygame.display.set_mode((300, 200))
# running = True
#
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_a and event.mod & pygame.KMOD_CTRL:
#                 print("Pressed: Ctrl + A")
#
# pygame.quit()

l = [[0] * 10 for _ in range(10)]
print(l)
del l[0][1:4]
print(l)