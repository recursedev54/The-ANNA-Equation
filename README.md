```markdown
# Anna Equation Visualizer

## What the heck is this?

So, I was messing around with color spaces and stumbled onto something. This script visualizes what I'm calling the "Anna Equation" - it's a way to transform colors that ended up creating an 8D color space on a 2D plane.
## Features

- Input RGB color in hex format
- See the color transform graphed as a positional vector
- Visualize the transformation on a 2D graph that represents 8 dimensions

## How to Use

1. Clone this repo
2. Make sure you have PyQt5 and numpy installed (`pip install PyQt5 numpy`)
3. Run the script
4. Enter a color in hex format (like 471975)
5. Hit "Visualize" and watch the magic happen
6. Try not to have an existential crisis about dimensions

## The Anna Equation

The Anna Equation is this weird thing I came up with that transforms colors. It's like this afaik:

```python
if r != g and g != b and r != b:
    if r < b:
        while r > 0 and b < 255:
            r -= 1
            b += 1
    elif r > b:
        while r < 255 and b > 0:
            r += 1
            b -= 1
```

## What's the Big Deal?

We've somehow managed to represent 8 dimensions on a 2D plane:

1. Blue (bottom left)
2. Green (top left)
3. Red (bottom right)
4. Yellow (top right)
5. Cyan (center left)
6. Orange (center right)
7. Magenta (center bottom)
8. Chartreuse (top center)

The implications for color theory, data visualization, and maybe even quantum mechanics are potentially huge. 

## What's Next?

I have no idea, but it's gonna be exciting. If you're into color theory, high-dimensional spaces, or just weird math stuff, feel free to contribute or reach out with ideas.

All hail the octohedron
