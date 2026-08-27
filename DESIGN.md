# Design

<!-- impeccable:design-schema 1 -->

## World

Flight-strip clearance bay (ATC strip desk) with split-flap cascade actuation. Cream paper strips sit in a graphite bay. Actuators land as matte-black flap faces. One safety-orange Admit key. Seed `27b2e849`, assigned index 4, raised by split-flap cascade + creator-hardware orange key.

## Mode

Operate (judge demo console).

## Color

- Bay graphite `#1c1f24` / raised `#262a31`
- Strip paper `#f4f0e6` / ink `#1a1c1f`
- Flap black `#0e0f12` / letter `#f7f4ec`
- Safety orange `#ff5a1f` (Admit + hold-adjacent strip tabs)
- Amber `#e8a317` (status lamps, live chain nodes)
- Hold red `#c62828` / Clear green `#1b7a4a`

Strategy: Restrained neutrals + one committed action orange.

## Typography

- UI: Public Sans (400–700)
- Data / flaps: system UI mono stack
- No display/decorative faces on Operate chrome

## Components

- Desk rail: scenario + stance selects, Admit CTA
- Strip cards: tab + body + flap actuator
- Cascade: staggered show + flap flip (honors prefers-reduced-motion)
- Receipts: progressive disclosure for claims/spans
- Meters: tabular decisions / would-hold / FNR / last ms

## Anti-references (rejected)

Neon cyan/purple AI dashboard, Syne/IBM Plex display pairing, hero-metric cards, glassmorphism, left accent borders as decoration, generic SaaS sidebar.
