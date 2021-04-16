
# import modules ----------------------------------------------------------- #

import sys
sys.path.append('../')
import PygameUi

pygame = PygameUi.pygame

Tags = PygameUi.widget_tags.Tags

Widget = PygameUi.Widget
Container = PygameUi.Container
Window = PygameUi.Window

Image = PygameUi.Image

pygame.init()

clock = pygame.time.Clock()


# initialise display & ui--------------------------------------------------- #
display = pygame.display.set_mode([640,480])

window = Window()

window_w = 400
window_h = 250

window.set_size((window_w,window_h),)
window.x = 20
window.y = 20

window.style.border_thickness = 1
window.style.border_radius = 2
window.style.padding = 2

image_1 = pygame.image.load('../resources/image_1.png')
image_1.set_colorkey((0,0,0),)

inner_child_1 = Image(image=image_1)

inner_child_1.style.border_thickness = 1
inner_child_1.style.border_radius = 2
inner_child_1.set_fluid_size(1,1)
inner_child_1.margin = 1

window.add_child(inner_child_1)

window.auto_reposition_children = True


# main loop ---------------------------------------------------------------- #
run = True
while run:
    deltatime = clock.tick(60)/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                print(window.get_minimum_size(True))
            elif event.key == pygame.K_r:
                window_w, window_h = window.get_minimum_size()
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        window_w -= 100*deltatime
    if keys[pygame.K_d]:
        window_w += 100*deltatime
    if keys[pygame.K_w]:
        window_h -= 100*deltatime
    if keys[pygame.K_s]:
        window_h += 100*deltatime
    
    window.size = (int(window_w), int(window_h))

    window_w = max(window.minimum_size[0], window_w)
    window_h = max(window.minimum_size[1], window_h)

    display.fill((255,255,255))

    window.draw(display)

    pygame.display.flip()


# quit pygame -------------------------------------------------------------- #
pygame.quit()