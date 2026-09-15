# Sashiko-Pat

A [Sashiko](https://en.wikipedia.org/wiki/Sashiko) pattern generator.

This app asks you about steps and offsets for both axes of the square
grid and generates a preview of what the pattern would look like after
being stitched.

The "steps" string looks like `FRONT[BACK[FRONT[...]]]` where `FRONT`
and `BACK` are digits from 1 to 3. `FRONT` tells how many squares long
the visible part of the stitch will be, and `BACK` tells how long
the part on the other side of the canvas will be. During the preview
generation that sequence of fronts and backs will be repeated again
and again, so if the input string ends with `FRONT` this will mean
that a single `BACK` will appear in between repeating
sub-sequences. Empty "steps" input means "1", i.e. one FRONT followed
by one BACK.

The "offsets" string looks like `N[N[...]]` where each `N` is a number
from 0 to 3. Each number tells by how many steps the generator should
advance the steps sequence at the beginning of the next row. The
offset sequence is also repeated during the rendering. Empty
"offsets" input means "0", i.e. there will be no offsets and all rows
will get exactly the same steps.

Using just a combination of steps and offsets for both axes you may
get pretty interesting patterns, so just try it!

Here is an example of a pattern from the Sashiko Wikipedia article
([this picture](https://en.wikipedia.org/wiki/Sashiko#/media/File:MET_RT792C.jpg)):

```text
X steps [1]:  
X offsets [0]: 101
Y steps [1]: 
Y offsets [0]: 111110
┌─  ┌─  ┌─   ─┐  ─┐  ─┐ ┌─  ┌─  ┌─   ─┐  ─┐  ─┐ ┌─  ┌─  ┌─   ─┐  ─┐  ─┐ ┌─  ┌─
│   │   │     │   │   │ │   │   │     │   │   │ │   │   │     │   │   │ │   │ 
  ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ 
  │   │   │ │   │   │     │   │   │ │   │   │     │   │   │ │   │   │     │   
  └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ 
│   │   │     │   │   │ │   │   │     │   │   │ │   │   │     │   │   │ │   │ 
└─┐ └─┐ └─┐ ┌─┘ ┌─┘ ┌─┘ └─┐ └─┐ └─┐ ┌─┘ ┌─┘ ┌─┘ └─┐ └─┐ └─┐ ┌─┘ ┌─┘ ┌─┘ └─┐ └─
  │   │   │ │   │   │     │   │   │ │   │   │     │   │   │ │   │   │     │   
  └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ 
│   │   │     │   │   │ │   │   │     │   │   │ │   │   │     │   │   │ │   │ 
  ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ 
  │   │   │ │   │   │     │   │   │ │   │   │     │   │   │ │   │   │     │   
┌─┘ ┌─┘ ┌─┘ └─┐ └─┐ └─┐ ┌─┘ ┌─┘ ┌─┘ └─┐ └─┐ └─┐ ┌─┘ ┌─┘ ┌─┘ └─┐ └─┐ └─┐ ┌─┘ ┌─
│   │   │     │   │   │ │   │   │     │   │   │ │   │   │     │   │   │ │   │ 
  ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ 
  │   │   │ │   │   │     │   │   │ │   │   │     │   │   │ │   │   │     │   
  └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ 
│   │   │     │   │   │ │   │   │     │   │   │ │   │   │     │   │   │ │   │ 
└─┐ └─┐ └─┐ ┌─┘ ┌─┘ ┌─┘ └─┐ └─┐ └─┐ ┌─┘ ┌─┘ ┌─┘ └─┐ └─┐ └─┐ ┌─┘ ┌─┘ ┌─┘ └─┐ └─
  │   │   │ │   │   │     │   │   │ │   │   │     │   │   │ │   │   │     │   
  └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ 
│   │   │     │   │   │ │   │   │     │   │   │ │   │   │     │   │   │ │   │ 
  ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ 
  │   │   │ │   │   │     │   │   │ │   │   │     │   │   │ │   │   │     │   
┌─┘ ┌─┘ ┌─┘ └─┐ └─┐ └─┐ ┌─┘ ┌─┘ ┌─┘ └─┐ └─┐ └─┐ ┌─┘ ┌─┘ ┌─┘ └─┐ └─┐ └─┐ ┌─┘ ┌─
│   │   │     │   │   │ │   │   │     │   │   │ │   │   │     │   │   │ │   │ 
  ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ 
  │   │   │ │   │   │     │   │   │ │   │   │     │   │   │ │   │   │     │   
  └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ 
│   │   │     │   │   │ │   │   │     │   │   │ │   │   │     │   │   │ │   │ 
└─┐ └─┐ └─┐ ┌─┘ ┌─┘ ┌─┘ └─┐ └─┐ └─┐ ┌─┘ ┌─┘ ┌─┘ └─┐ └─┐ └─┐ ┌─┘ ┌─┘ ┌─┘ └─┐ └─
  │   │   │ │   │   │     │   │   │ │   │   │     │   │   │ │   │   │     │   
  └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ └─┐ └─┘ ┌─┘ ┌─┘ ┌─┐ └─┐ 
```
