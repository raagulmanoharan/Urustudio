# Uru Studio — Artisanal Wedding Return Gifts

A responsive marketing website built with plain HTML, CSS, and JavaScript — no build step required.

## Run locally

Just open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Structure

```
index.html      # Page markup — sections are added here one at a time
css/styles.css  # All styles. Theme tokens live in :root (top of file)
js/main.js      # Mobile nav, header scroll state, misc interactions
```

## Theming

Colors, fonts, and spacing are CSS custom properties in `:root` at the top of
`css/styles.css`. Change them there to restyle the whole site at once.

## Responsiveness

Mobile-first. Fluid type via `clamp()`, a flex/grid layout, and a full mobile
nav drawer. The primary breakpoint is `860px`.
