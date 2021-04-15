
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
window.name = 'Window'

window_w = 273
window_h = 200

window.set_size((window_w,window_h),)
window.x = 20
window.y = 20

window.set_style(WidgetStyle(border=(2,(255,255,255)), border_radius=2))

window.set_layout(Layout(Tags.COL, Tags.FIT))

font = pygame.font.Font('font.ttf', 16)

boring_label = Label(None, font, "This is a label")
boring_label.name = 'Boring Label'
boring_label.set_style( WidgetStyle(border=(1,(0,0,0)), border_radius=2) )
boring_label.fluid_size = 1,1
boring_label.margin = 1
window.add_child(boring_label)



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

    any_key = False

    if keys[pygame.K_a]:
        window_w -= 100*deltatime
        any_key = True
    if keys[pygame.K_d]:
        window_w += 100*deltatime
        any_key = True
    if keys[pygame.K_w]:
        window_h -= 100*deltatime
        any_key = True
    if keys[pygame.K_s]:
        window_h += 100*deltatime
        any_key = True
    
    window.size = (int(window_w), int(window_h))

    window_w = max(window.minimum_size[0], window_w)
    window_h = max(window.minimum_size[1], window_h)

    display.fill((20,20,25),)

    window.draw(display)

    pygame.display.flip()


# quit pygame -------------------------------------------------------------- #
pygame.quit()