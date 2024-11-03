A pygame based implementation of Truchet tiling defined in [this blog post](https://medium.com/@adbaysal/exploring-truchet-tiles-da61f02981a0).

## How to use
First install dependencies, preferably in a virtual environment.

### Rectangular Tiling
Run rectangular/main.py. This will open a pygame screen. Use the following keys to alter the tiling:

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

### Hexagonal Tiling
To be implemented ...