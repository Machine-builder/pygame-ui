
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
Label = PygameUi.Label

Checks = PygameUi.widget_checks.Checks


# pygame and font init ----------------------------------------------------- #

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
window.padding = 1
window.style.border_thickness = 1
window.style.border_radius = 2

for container_x in range(5):

    new_container = Container(window)
    new_container.layout_direction = Tags.COL
    new_container.fluid_size = 1.75,1
    new_container.margin = 0
    new_container.padding = 0

    for i in range(5):
        # add more widgets to this container column

        list_widget = Container(new_container)
        list_widget.margin = 1
        list_widget.style.border_radius = 2
        list_widget.style.border_colour = (20,20,20)
        list_widget.style.border_thickness = 1
        list_widget.style.background = (140,140,140)

        list_widget.set_hoverable(True)
        hover_style = list_widget.get_style_for(Checks.is_hovered)
        hover_style.background = (180,180,255)
        hover_style.border_colour = (255,255,255)
        hover_style.border_thickness = 2

        new_container.add_child(list_widget)
    
    new_container.style.transparent_background = True
    window.add_child(new_container)

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