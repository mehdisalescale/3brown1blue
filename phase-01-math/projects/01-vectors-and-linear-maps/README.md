# 01.01 — vectors-and-linear-maps

NumPy matrix ops + animated 2D/3D linear transformations (3B1B-style).

## What

A NumPy-only walkthrough of 2D linear maps — rotation, shear, scale, projection, reflection — visualized as continuous animations that morph the basis vectors and a dense grid of points under the chosen matrix. Optional 3D extension at the end.

## Why

Grant's *Essence of Linear Algebra* frames every matrix as a transformation of space. The intuition I want as muscle memory: see a 2×2 matrix, see what it does to î and ĵ, see what happens to a point cloud. If I can build that visualization from scratch, the picture is mine, not borrowed.

## References

_(append resources here as you actually use them — specific 3B1B chapters, blog posts, Stack Exchange answers. Don't pre-list things you haven't read yet.)_

## Success criteria

- Given any 2×2 matrix, I can predict — before running the code — where (1, 0), (0, 1), and one off-axis point land.
- The notebook produces an animated visualization for at least three transformations (e.g. rotation, shear, projection).
- I can explain — without notes — why `det(A) = 0` collapses 2D to a line, and what an eigenvector "means" geometrically (eigenvectors are stretched, not rotated).
- The notebook runs end-to-end on a fresh kernel without errors.

## Run it

```bash
uv run --package phase-01-math jupyter lab projects/01-vectors-and-linear-maps/notes.ipynb
```

## Notes

_(short, post-hoc. What surprised you, what tripped you up. Fill in when the project is done.)_

## Posts

_(blog posts that draw on this project — link them here as they're written.)_
