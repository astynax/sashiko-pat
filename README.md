# Sashiko-Pat

A Sachiko pattern generator.

This app asks you about steps and offsets for both axes of the sqare grid and generates a preview of how the pattern would look like after being stitched.

The "steps" string looks like `FRONT[BACK[FRONT[...]]]` where `FRONT` and `BACK` are digits from 1 to 3. `FRONT` tells how many squares long will be the visible part of the stitch, `BACK` tells how long will be the part that on the other side of the canvas. During the preview generation that sequence of fronts and backs will be repeated again and again, so if the input string will end with `FRONT` this will mean that a single `BACK` will appear in between repeating sub-sequences. Empty "steps" input means "1", i.e. one FRONT followed by one BACK.

The "offsets" string looks like `N[N[...]]` where each `N` is a number from 0 to 3. Each number tells by how many steps the generator should advance the steps sequence at the beginning of the next row. The offset sequence is also being repeated during the rendering. Empty "steps" input means "0", i.e. there will be no offsets and all rows will get exactly the same steps.

Using just a combination of steps and offsets for both axes you may get a pretty interesting patterns, so just try it!

