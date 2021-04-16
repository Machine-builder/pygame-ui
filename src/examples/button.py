
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
window.layout_direction = Tags.COL
window.padding = 3
window.style.border_thickness = 3
window.style.border_radius = 2

boring_label = Label(None, font, "This is a label")
boring_label.style.border_thickness = 1
boring_label.style.border_radius = 2
boring_label.fluid_size = 1,0.8
boring_label.margin = 1

container = Container(window)
container.style.background = (160,160,160)
container.style.border_thickness = 1
container.style.border_radius = 2
container.fluid_size = 1,1
container.margin = 1


# create and link buttons to functions ------------------------------------- #

cool_button1 = Label(None, font, "print_test1()")
cool_button1.style.background = (240,240,240)
cool_button1.style.border_thickness = 2
cool_button1.style.border_radius = 2
cool_button1.fluid_size = 3,1
cool_button1.set_fixed_size(
    size = (cool_button1.image_size[0]+6, cool_button1.image_size[1]+6),
    min_margin = (1,1,1,1) # minimum margin of 1px on all sides
)
def print_test1(): print("print_test1() function called")
cool_button1.on_click = print_test1

cool_button2 = Label(None, font, "print_test2()")
cool_button2.style.background = (240,240,240)
cool_button2.style.border_thickness = 2
cool_button2.style.border_radius = 2
cool_button2.fluid_size = 1,1
cool_button2.set_fixed_size(
    size = (cool_button2.image_size[0]+6, cool_button2.image_size[1]+6),
    min_margin = (1,1,1,1) # minimum margin of 1px on all sides
)
def print_test2(): print("print_test2() function called")
cool_button2.on_click = print_test2

cool_button1.style.margin_align = (Tags.CENTER, Tags.CENTER)
cool_button2.style.margin_align = (Tags.CENTER, Tags.CENTER)


# add widgets to main window and align ------------------------------------- #

container.add_child(cool_button1)
container.add_child(cool_button2)
window.add_child(boring_label)
window.add_child(container)

container.align_fluid_children()

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