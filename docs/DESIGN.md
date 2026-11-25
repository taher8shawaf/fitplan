# FitPlan design notes

Direction: **iron & chalk**. The interface borrows from the gym itself instead of generic app styling.

## Colour
Colours come from competition weight plates, and every colour carries a meaning in the app:

| Plate | Light | Dark | Means |
|---|---|---|---|
| Red (25 kg) | `#c9343a` | `#e06a6e` | Protein |
| Yellow (15 kg) | `#c99400` | `#e6bd4c` | Carbs |
| Green (10 kg) | `#2e8f57` | `#5cc28a` | Fat |
| Blue (20 kg) | `#2f6cc0` | `#6fa1e6` | Water |

Everything else is neutral:
- **Light ("chalk")**: background `#eceeeb`, panels `#f8f9f7`, text and primary actions in iron `#1d2327`.
- **Dark ("rubber floor")**: slate `#1b1f22` (not pure black), panels `#23282c`, text and primary actions in chalk `#e8ebe7`.

There is no separate brand accent. Primary buttons, selected chips and checked sets use the ink colour, so the plate colours stay meaningful.

## Type
- **Readex Pro** for everything (Arabic and Latin), weights 300–700.
- Scale, ratio 1.25: 12.8 / 14 / 16 / 20 / 25 / 31 / 39 / 49 px.
- Numbers always use Western digits (0-9) and tabular figures, so columns line up.
- The type itself does the work on the Today page: the session name is set large (39 px) instead of being boxed in a card.

## Layout
- Panels only wrap things that are used together (logging a workout, adding food). Lists inside them are separated by rules, not more cards.
- Radius follows hierarchy: 18 px panels, 12 px controls, 8 px small controls, pills for chips.
- No drop shadows; one 1 px border.
- Facts are spaced apart in a row (`meta()` helper), never joined with dots.
- No emoji in headings or labels. The only emoji is the 💪 reaction, because it is the reaction itself.

## The one bold element
**The plate calculator.** Under every barbell exercise, a drawing of one side of the bar shows which plates to load, in plate colours, and updates live as the weight changes. It is decoration that does a job lifters actually need.

## Writing
- Plain verbs, sentence case, the user's words: "Save workout", "Copy yesterday".
- Empty states say what to do next.
