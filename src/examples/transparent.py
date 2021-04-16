
# import modules ----------------------------------------------------------- #

import sys
sys.path.append('../')
import PygameUi

pygame = PygameUi.pygame

Tags = PygameUi.widget_tags.Tags

Widget = PygameUi.Widget
Container = PygameUi.Container
Window = PygameUi.Window

ImageWidget = PygameUi.ImageWidget
Label = PygameUi.Label


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
window.padding = 3

container_1 = Container(window)
container_1.style.background = (200,150,150)
container_1.style.border_thickness = 1
container_1.style.border_radius = 2
container_1.fluid_size = 1,1
container_1.margin = 1

container_2 = Container(window)
container_2.style.background = (150,200,150)
container_2.style.border_thickness = 1
container_2.style.border_radius = 2
container_2.fluid_size = 1,1
container_2.margin = 1

container_3 = Container(window)
container_3.layout_direction = Tags.COL
container_3.fluid_size = 1.75,1
container_3.margin = 1
container_3.padding = 3
container_3.style.background = (150,150,200)

for i in range(5):
    # add more widgets to this last container
    list_widget = Container(container_3)
    list_widget.margin = 2
    list_widget.style.border_radius = 4
    list_widget.style.border_colour = (20,20,20)
    list_widget.style.border_thickness = 1
    list_widget.style.background = (180,180,180) if (
        i%2 == 0) else (220,220,220)
    container_3.add_child(list_widget)

extra_widget = Widget(container_3.child_at(2))
extra_widget.margin = 3
extra_widget.style.background = (190,190,230)
extra_widget.style.border_thickness = 1
extra_widget.style.border_radius = 2

container_3.child_at(2).style.border_thickness = 0
container_3.child_at(2).style.padding = 35
container_3.child_at(2).add_child(extra_widget)
container_3.child_at(2).name = 'debug'
container_3.child_at(2).reposition_children()
container_3.child_at(2).name = 'widget'
container_3.align_fluid_children()

print(container_3.child_at(2).style.padding)

window.add_child(container_1)
window.add_child(container_2)
window.add_child(container_3)

window.run_functions_on_children(
    function=lambda widget: widget.style.set_transparent_background(True),
    all_children=True
)
window.style.transparent_background = True

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