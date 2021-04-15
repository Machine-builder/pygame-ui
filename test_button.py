
# import modules ----------------------------------------------------------- #
import PygameUi
pygame = PygameUi.pygame

Tags = PygameUi.widget_tags.Tags
Window = PygameUi.Window

Widget = PygameUi.Widget
Container = PygameUi.Container

WidgetLayout = PygameUi.WidgetLayout
WidgetStyle = PygameUi.WidgetStyle
ImageWidget = PygameUi.ImageWidget
Label = PygameUi.Label

Layout = PygameUi.Layout

pygame.init()

clock = pygame.time.Clock()


# initialise display & ui--------------------------------------------------- #
display = pygame.display.set_mode([640,480])

window = Window()

window_w = 273
window_h = 200

window.set_size((window_w,window_h),)
window.x = 20
window.y = 20

window.set_style(WidgetStyle(border=(2,(255,255,255)), border_radius=2))

window.set_layout(Layout(Tags.COL, Tags.FIT))

font = pygame.font.Font('font.ttf', 16)

boring_label = Label(None, font, "This is a label")
boring_label.set_style( WidgetStyle(border=(1,(0,0,0)), border_radius=2) )
boring_label.fluid_size = 1,0.8
boring_label.margin = 1
window.add_child(boring_label)

container = Container(window)
container.set_style( WidgetStyle(background=(160,160,160), border=(1,(0,0,0)), border_radius=2) )
container.fluid_size = 1,1
container.margin = 1
window.add_child(container)

cool_button = Label(None, font, "This one is a button! - say Hi")
cool_button.set_style( WidgetStyle(background=(240,240,240), border=(1,(0,0,0)), border_radius=2) )
cool_button.fluid_size = 3,1
cool_button.set_fixed_size(
    size = (cool_button.image_size[0]+6, cool_button.image_size[1]+6),
    min_margin = (1,1,1,1) # minimum margin of 1px on all sides
)
def print_test(): print("print_test() function called: Hi")
cool_button.on_click = print_test

cool_button2 = Label(None, font, "Button: Hey")
cool_button2.set_style( WidgetStyle(background=(240,240,240), border=(1,(0,0,0)), border_radius=2) )
cool_button2.fluid_size = 1,1
cool_button2.set_fixed_size(
    size = (cool_button2.image_size[0]+6, cool_button2.image_size[1]+6),
    min_margin = (1,1,1,1) # minimum margin of 1px on all sides
)
def print_test2(): print("print_test() function called: Hey")
cool_button2.on_click = print_test2

cool_button.wlayout.margin_align = (Tags.CENTER, Tags.CENTER)
cool_button2.wlayout.margin_align = (Tags.CENTER, Tags.CENTER)

container.add_child(cool_button)
container.add_child(cool_button2)

container.align_fluid_children()



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
                print(cool_button.size)
    
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
    
    window.w = int(window_w)
    window.h = int(window_h)

    window_w = max(window.minimum_size[0], window_w)
    window_h = max(window.minimum_size[1], window_h)

    display.fill((20,20,25),)

    window.draw(display)

    pygame.display.flip()


# quit pygame -------------------------------------------------------------- #
pygame.quit()