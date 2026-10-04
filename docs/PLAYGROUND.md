# Marways / Curiosity in motion

## Design plan

The personal profile should make the person and their real projects memorable. The previous abstract sculpture overwhelmed both. This revision turns six actual project ideas into six distinct visual interactions, with a tangible, playful machine as the welcome image.

Palette: cobalt `#3548F5`, ink `#20234B`, lavender `#EEEAFB`, apricot `#FF9869`, mint `#A9E5D2`, white `#FFFFFF`. Use cobalt for identity, lavender for space, and project-specific colors for navigation.

Type: locally hosted Sora for English identity and project names; system Chinese sans serif for readable body text. Left-aligned copy, short lines, generous spacing. Large type supports the content without covering the illustration.

Layout:

```text
Site:   identity + clear navigation
        expressive headline | dimensional idea machine + project hotspots
        six project selectors
        illustrated scene   | project explanation, workflow, repository
        open project directory
        personal approach + actual tools
        GitHub / Bilibili

README: illustrated welcome cover
        animated signal ribbon + short personal introduction
        ECG project spread
        conversation | reading
        desktop     | live preparation
        learning resources spread
        capability map + ways of working + public snapshot
```

## Review against the brief

A generic creative portfolio could use an arbitrary 3D blob, repeated project cards, or a bank of decorative statistics. This design instead gives ECG its own signal trace, reading its annotated pages, desktop tools a cursor and action sequence, and learning resources a connected library. The illustration is a conceptual visual, not a claimed application screenshot. On GitHub, the content is visible without opening collapsed sections. The site adds scene changes, selectable project hotspots, and a hands-on demonstration for each idea.

Motion follows a common rhythm: quick acknowledgement, deliberate 650 ms scene change, slower ambient details. Pause and reduced-motion settings stop ambient animation and replace animated image assets with still variants. Native scrolling, keyboard navigation and a complete no-JavaScript directory are retained.

## Visual asset

`site/art/idea-machine.png` was generated with the built-in image tool, copied without changing its pixels or alpha channel. The source prompt is preserved in `IMAGE-PROMPT.md`. It is an illustration of making with AI, not a screenshot of a product.

## Build and verification

Run the existing three archive artwork builders, then `python scripts/build_playground_profile.py`, `python scripts/validate_shape_profile.py`, and `node --check site/app.js`. Inspect the actual GitHub rendering and the deployed site separately. Cover images are deliberate browser-rendered compositions from `site/profile-cover.html`; they are versioned assets and are not rebuilt by the daily public-data job.
