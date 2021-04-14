# pygame-ui
My attempt at creating a fluid ui library built for pygame

# how-to-use
Just download the code, and run the test files - feel free to take a look at how they work!

Basic examples:

## A window with two stretching widgets in a row
```python
import PygameUi
Window = PygameUi.Window
Widget = PygameUi.Widget
Layout = PygameUi.Layout

# initialise a main window,
# and set its size to 300x200
main_window = Window()
main_window.set_size((300,200),)

# set the layout to be a row,
# and use Layout.FIT to specify
# that child elements should be
# stretched to fit the space
window_layout = Layout(Layout.ROW, Layout.FIT)
main_window.set_layout(window_layout)

# create a widget for the left
# and right side, and set them
# both to be fluid, and take up
# the same amount of space
child_left = Widget()
child_left.set_fluid_size(1,1)

child_right = Widget()
child_right.set_fluid_size(1,1)

# experiment with changing child_left's
# first value in .set_fluid_size()
# and see how that affects it!

main_window.add_children([child_left,
                          child_right])
```

# extra-notes
This code is awful, I'm aware - but I'd appreciate it if you don't go steal it and claim it as your own :P

# license
Please make sure to read the COPYING file before deciding to release your own versions of my code,
also feel free to add a PR to change anything or fix anything up
