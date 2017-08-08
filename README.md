# contrast_check
----------------
A script that takes a list of colors and displays all the possible combinations of those colors as foregrounds and brackgrounds, and then rates those combinatiosn depending on whether they pass WCAG 2.0 level AA or AAA.

# Usage:
```
python contrast_check.py [filename]
```

The file should be a tab separated file with the first column being the name of the color, and the second column being the RGB values of the color (0-255) separated by commas. For example: 222,173,237.
Example files can be found in the sample folder.
