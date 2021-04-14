
# import modules ----------------------------------------------------------- #
import PygameUi
pygame = PygameUi.pygame

Window = PygameUi.Window

Widget = PygameUi.Widget
WidgetLayout = PygameUi.WidgetLayout
WidgetStyle = PygameUi.WidgetStyle

Layout = PygameUi.Layout

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
window.set_style(WidgetStyle(border=(2,(255,255,255)), border_radius=2))

inner_child_1 = Widget(window)
inner_child_1.set_style( WidgetStyle(border=(1,(0,0,0)), border_radius=2) )
inner_child_1.set_fluid_size(1,1)
inner_child_1.style.background = (255,200,200)

inner_child_2 = Widget(window)
inner_child_2.set_style( WidgetStyle(border=(1,(0,0,0)), border_radius=2) )
inner_child_2.set_fluid_size(1,1)
inner_child_2.style.background = (200,255,200)

col_child = Widget(window)
col_child.set_style( WidgetStyle(border=(1,(0,0,0)), border_radius=2) )
col_child.set_fluid_size(1.5,1)
col_child.style.background = (200,200,255)
col_child.set_layout(Layout(Layout.COL, Layout.FIT))
col_child.margin = 5

for i in range(4):
    list_elem = Widget(col_child)
    widget_colour = (225,225,225)
    if i%2 == 0:
        widget_colour = (180,180,180)
    list_elem.set_style(WidgetStyle(background=widget_colour,
                                    border=(2,(50,50,50)),
                                    border_radius=1))
    if i == 2:
        # middle item
        button = Widget(list_elem)
        list_elem.add_child(button)
        button.set_style(WidgetStyle(background=(150,150,220),
                                     border=(3,(0,0,0))))
        button.name = 'blue_button'
        button.margin = (1,1)
        list_elem.set_fluid_size(0,0)
        button.set_minimum_size(50,50)
    
    list_elem.name = f'list_element_{i}'

    list_elem.margin = 1
    col_child.add_child(list_elem)

# window.add_children([inner_child_1, inner_child_2, col_child])

inner_child_1.margin = 1
inner_child_2.margin = 1
col_child.margin = 1

col_child.name='column_widget'

window.add_child(inner_child_1.copy())
# window.add_child(inner_child_1.copy())
# window.add_child(inner_child_1.copy())
# window.add_child(inner_child_1.copy())
# window.add_child(inner_child_2)
window.add_child(col_child)

window.name = 'window'

# window.set_minimum_size( 186, 204 )


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
            if event.key == pygame.K_i:
                print(int(window_w), int(window_h))
                print(button.w, button.h)
            elif event.key == pygame.K_r:
                window_w, window_h = window.get_minimum_size()
            
            if event.key == pygame.K_LEFT:
                button.margin = (button.margin[1]-1, button.margin[0])
            if event.key == pygame.K_RIGHT:
                button.margin = (button.margin[1]+1, button.margin[0])
            
            if event.key == pygame.K_UP:
                button.margin = (button.margin[1], button.margin[0]-1)
            if event.key == pygame.K_DOWN:
                button.margin = (button.margin[1], button.margin[0]+1)
    
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