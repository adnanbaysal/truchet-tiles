* Move common code to a common place
* Add download (svg/png) button to web ui
* Fix linting issues
* Add control to fix the tiling image height and calculate tile edge length using that length and dimension information
* Fix the curved filled tiling bug which draws full circle instead of a circle pie.
* Implement hybrid linear tiling
* Instead of straight lines and arcs, try using 2, 3, ... lines passing on equally spaced points on the arc
* Support animating filled tilings
* Show the 0-1 grid on the right side of the web page
* Support user custom grid: User provide a grid of 0-1s from web-ui and app creates the corresponding tiling
* Support updating the custom grid with click-on-tile
* Support custom grid generation with javascript
* Add hint texts to UI elements