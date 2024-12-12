A drawsvg and Django based implementation of Truchet tiling defined in [this blog post](https://medium.com/@adbaysal/exploring-truchet-tiles-da61f02981a0).

# How to run
First install dependencies, preferably in a virtual environment. 

Then, run the web server with `python web_ui/manage.py` (or using the `Django` debug config if you are using VS Code). Then for the rectangular tiling, click the `Rectangular Tiling` button on the main page, or open `http://127.0.0.1:8000/rect` in your browser. Use the UI to change the display settings of the tiling.

Some settings will not take affect depending on other settings:

* Invert colors requires Fill to be selected.
* Line width needs Fill to be NOT selected.
* Hybrid fill mode needs both Fill and Curved to be selected.
* Animate needs Fill to be NOT selected (may change in the future).
* Animation mode needs Animate to be selected.