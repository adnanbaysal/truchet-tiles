A drawsvg and Django based implementation of Truchet tiling defined in [this blog post](https://medium.com/@adbaysal/exploring-truchet-tiles-da61f02981a0).

# How to run
First install dependencies, preferably in a virtual environment. 

## How to run with Django
Run the web server with `python web_ui/manage.py` (or using the `Django` debug config if you are using VS Code). Then for the rectangular tiling, click the `Rectangular Tiling` button on the main page, or open `http://127.0.0.1:8000/rect` in your browser. Use the UI to change the display settings of the tiling.

Some settings will not take affect depending on other settings:

* Invert colors requires Fill to be selected.
* Line width needs Fill to be NOT selected.
* Hybrid fill mode needs both Fill and Curved to be selected.
* Animate needs Fill to be NOT selected (may change in the future).
* Animation mode needs Animate to be selected.

## How to run with Pygame (unix only)
### Rectangular tiling
Run `python pygame_ui/rectangular.py`, or use the `Pygame Rectangular` debug config if you are using VS Code. This will open a pygame screen. Use the following keys to alter the tiling:

* **UP-DOWN Arrows:** Change the function being shown
* **LEFT-RIGHT Arrows:** Regenerate an image in the random function mode.
* **F:** Switch between Filled and linear versions.
* **G:** Switch between showig and not showing grid lines.
* **I:** Invert the colors in filled version.
* **A:** Switch between axis Aligned and 45 degrees rotaded versions.
* **W:** Increase the width of the line in linear version.
* **S:** Decrease the width of the line in linear version.
* **P:** Print the current image on pygame screen to a file.
* **C:** Switch between Curved and Straight lines mode
* **H:** Cycle through 3 modes of Hybrid fill for curved and filled tiling
* **M:** Turn on/off SVG animation (not visible in Pygame screen)
* **N:** Cycle through 3 animation methods (all tiles at once, row by row, tile by tile)

Note that animation will not play in Pygame, but key `P` will save the SVG with animation.

### Hexagonal tiling
Run `python pygame_ui/hexagonal.py`, or use the `Pygame Hexagonal` debug config if you are using VS Code. This will open a pygame screen. Use the following keys to alter the tiling:

* **UP-DOWN Arrows:** Change the function being shown
* **LEFT-RIGHT Arrows:** Regenerate an image in the random function mode.
* **F:** Switch between Filled and linear versions.
* **G:** Switch between showig and not showing grid lines.
* **I:** Invert the colors in filled version.
* **O:** Switch between pointy-top and flat-top hexagon modes.
* **W:** Increase the width of the line in linear version.
* **S:** Decrease the width of the line in linear version.
* **P:** Print the current image on pygame screen to a file.
* **C:** Switch between three connector types: straight, curved and two lines
* **H:** Cycle through 3 modes of Hybrid fill for curved and filled tiling
* **M:** Turn on/off SVG animation (not visible in Pygame screen)
* **N:** Cycle through 3 animation methods (all tiles at once, ring by ring, tile by tile)

Note that animation will not play in Pygame, but key `P` will save the SVG with animation.
