# pygame-ui
## Introduction & Overview

Here's my attempt at creating a fluid **User Interface** library built for **pygame 2+**

This project is current VERY EARLY in development, so there are probably loads of bugs that you'll experience when messing about with it, so feel free to open an issue or create a PR and fix the bug yourself :)

## How to use
Just take a look in the repo and try out some of the example files - I suggest you look into how they work to get an idea of how you'd setup your own uis :)

**Warning**: Some `examples/*.py` files may no longer be functional, as I've done quite a large rewrite of the main `Widget` & `Container` code. I'll try and get all the tests setup properly asap.

**Good Practice**: `examples/complex.py` is the most recent of the `examples/*.py` files, and it is therefor written the most efficiently and pythonic. I recommend you take a look through it so you can plan out how to setup your own interfaces.

Here's what you _should_ see when you run `examples/complex.py`, you can use the WASD keys to resize the Window Widget

![a gif of examples/complex.py in action](https://raw.githubusercontent.com/Machine-builder/pygame-ui/main/src/gifs/test_complex.gif)

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
main_window.size = (300,200)
main_window.layout_direction = Tags.ROW

# create two child widgets,
# and set their fluid sizes to
# have the same priority - so
# they take up the same amount
# of space

child_left = Widget()
child_left.fluid_size = (1,1)
child_right = Widget()
child_right.fluid_size = (1,1)

main_window.add_children([child_left, child_right])

# this is NOT all the code required-
# you also need your basic pygame loop
# and event management. If you're not
# sure how that would be setup, I
# recommend you look into some of the
# example files to get a rough idea
```

## License
Please make sure to read the LICENSE file before deciding to release your own versions of my code, also feel free to add a PR to change anything or fix anything up
