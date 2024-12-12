* Add controls for line color, fill color, bg color, grid line color, grid line width and stroke
* Remove color inversion since color choices can do it 
* Add download (svg/png) button to web ui
* Implement hybrid linear tiling
* Support animating filled tilings
* Show the 0-1 grid on the right side of the web page
* Support user custom grid: User provide a grid of 0-1s from web-ui and app creates the corresponding tiling
* Support updating the custom grid with click-on-tile
* Support custom grid generation with javascript
* Fix the curved filled tiling bug which draws full circle instead of a circle pie.
* Add hint texts to UI elements
* Seperate interface used by pygame by deriving a class from the draw class
  