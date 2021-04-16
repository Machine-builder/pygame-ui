# pygame-ui
## Introduction & Overview

Here's my attempt at creating a fluid **User Interface** library built for **pygame 2+**

This project is current VERY EARLY in development, so there are probably loads of bugs that you'll experience when messing about with it, so feel free to open an issue or create a PR and fix the bug yourself :)

## How to use
Just download the repo, extract it, and run the test files! - Feel free to look into how they work

**Warning**: Some `test_*.py` files may no longer be functional, as I've done quite a large rewrite of the main `Widget` & `Container` code. I'll try and get all the tests setup properly asap.

**Good Practice**: `test_complex.py` is the most recent of the `test_*.py` files, and it is therefor written the most efficiently and pythonic. I recommend you take a look through it so you can plan out how to setup your own interfaces.

Here's what you _should_ see when you run `test_complex.py`, you can use the WASD keys to resize the Window Widget

![a gif of test_complex.py in action](https://raw.githubusercontent.com/Machine-builder/pygame-ui/main/Gifs/test_complex.gif)

### Further Code Examples
**A window with two stretching widgets, organised in a row**

```python
import PygameUi
Window = PygameUi.Window
Widget = PygameUi.Widget
Layout = PygameUi.Layout
Tags = pygameUi.widget_tags.Tags

# initialise a main window,
# and set its size to 300x200
main_window = Window()
main_window.set_size((300,200),)

# set the layout to be a row,
# and use Layout.FIT to specify
# that child elements should be
# stretched to fit the space

main_window.layout_direction = Tags.ROW

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

# this is NOT all the code required-
# you also need your basic pygame loop
# and event management. If you're not
# sure how that would be setup, I
# recommend you look into some of the
# test files to get a rough idea
```

## Extra Notes
This code is awful, I'm aware.. haha

## License
Please make sure to read the COPYING/LICENSE file before deciding to release your own versions of my code, also feel free to add a PR to change anything or fix anything up
