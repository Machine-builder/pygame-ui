
# import modules ----------------------------------------------------------- #

import sys
sys.path.append('../')
import PygameUi

pygame = PygameUi.pygame

Tags = PygameUi.widget_tags.Tags

Widget = PygameUi.Widget
Window = PygameUi.Window


pygame.init()
font = pygame.font.Font('../resources/font.ttf', 16)

clock = pygame.time.Clock()


# initialise display & ui--------------------------------------------------- #

display = pygame.display.set_mode([640,480])

window = Window()

window_w = 280
window_h = 200

window.size = (window_w,window_h)
window.position = (20,20)
window.layout_direction = Tags.ROW
window.padding = 3
window.style.border_thickness = 3
window.style.border_radius = 2

widget_1 = Widget(window)
widget_1.style.background = (200,150,150)
widget_1.style.border_thickness = 1
widget_1.style.border_radius = 2
widget_1.fluid_size = 1.4,1
widget_1.margin = 1

widget_2 = Widget(window)
widget_2.style.background = (150,200,150)
widget_2.style.border_thickness = 1
widget_2.style.border_radius = 2
widget_2.fluid_size = 1,1
widget_2.margin = 1

widget_3 = Widget(window)
widget_3.style.background = (150,150,200)
widget_3.style.border_thickness = 1
widget_3.style.border_radius = 2
widget_3.fluid_size = 1.8,1
widget_3.margin = 1

window.add_child(widget_1)
window.add_child(widget_2)
window.add_child(widget_3)

# allows any change in size, style, or whatever
# to reposition the widget's children, and their children too
window.auto_reposition_children = True


# main loop ---------------------------------------------------------------- #

run = True
while run:
    deltatime = clock.tick(60)/1000

    pygame_events = pygame.event.get()
    for event in pygame_events:
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                print(window.get_minimum_size(True))
            elif event.key == pygame.K_r:
                window_w, window_h = window.get_minimum_size()
    
    window.process_events(pygame_events)
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        window_w -= 100*deltatime
    if keys[pygame.K_d]:
        window_w += 100*deltatime
    if keys[pygame.K_w]:
        window_h -= 100*deltatime
    if keys[pygame.K_s]:
        window_h += 100*deltatime
    
    window.size = (int(window_w),int(window_h))

    window_w = max(window.minimum_size[0], window_w)
    window_h = max(window.minimum_size[1], window_h)

    display.fill((255,255,255),)

    window.draw(display)

    pygame.display.flip()


# quit pygame -------------------------------------------------------------- #

pygame.quit()