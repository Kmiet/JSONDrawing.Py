# JSONDrawing.Py
Drawing figures with Python using PyGame. All the data has to be predefined in JSON file as shown in example below.
## Tech
| Library | Link |
| ------ | ------ |
| PyGame | [PyGame] |

#
#### Installation

According to [PyGame wiki] download library using PIP:
```sh
$ python3 -m pip install -U pygame --user
```
#
#### Usage example:
#
```sh
$ python main.py <INPUT_FILE.JSON> [-o OUTPUT_FILE.PNG]
```

#### JSON file example:
#
```json
{
    "Figures": [
        {"type": "point", "x": 1, "y": 0},
        {"type": "polygon", "points": [[2,5], [3,14], [5,18], [11,18], [3,39]], "color": "blue"},
        {"type": "rectangle", "x": 100, "y": 50, "width": 200, "height": 50},
        {"type": "square", "x": 150, "y": 100, "size": 80, "color": "(255,255,255)"},
        {"type": "circle", "x": 800, "y": 600, "radius": 40, "color": "#abcdef"}
    ],
    "Screen": {"width": 800, "height": 600, "bg_color": "black", "fg_color": "red"},
    "Palette": {"red": "#ff0000", "blue": "#0000ff", "black": "#000000"}
}
```
#


   [PyGame wiki]: <https://www.pygame.org/wiki/GettingStarted>
   [PyGame]: <https://www.pygame.org/>
   