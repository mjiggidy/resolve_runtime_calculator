# Resolve Runtime Calculator EXTREME!*

A simple runtime calculator for Davinci Resolve.  Selected media pool items can be added to a list to calculate their total collective runtime.

>[!WARNING]
>This is still under heavy development.  Still very experimental.  Some things are still very alpha-y.  For example, it assumes 24 FPS.  I'll eventually fix this stuff.  In the meantime, use this at your own risk.  I assume no responsibility for anything, ever, in the world.

![Embarrassing Screenshot](screenshot.png)

## Trimming

In many cases, timelines or clips may start or end with slates or leaders which should not contribute to the runtime calculation.  For this, two options are provided:

### Trim From Each Head / Tail
Define a predetermined duration to remove from the head and/or tail of each clip as it is added to the list.  This is useful for cases when the amount to remove is consistent for each item, such as head and tail leaders.

### Use FFOA/LFOA Markers

Markers named "FFOA" (First Frame Of Action) and/or "LFOA" (Last Frame Of Action) may be placed in each timeline or clip to define the first and last frame to consider in the runtime calculation.  When enabled, FFOA/LFOA markers take precedence over "Trim From Each" settings.  If these options are enabled but no markers are found, the normal "Trim From Head/Tail" amounts will be applied.

## Installation

I plan to hammer this down for distribution, but for now: good luck!  Heehee!  Bye!  No I'm kiddin'.  But it's not so straightforward at the moment.

It's possible to get this working via the Workflow Integrations menu, but it's pretty tricky.  If you're game, the idea is to "vendor" this package into a subdirectory of your Workflow Integrations location, then write a little bootstrap script in the Worflow Integrations root.  *Obviously.  Puh.*

As an alternative for the moment, I recommend cloning the repo into some other location, installing its `requirements.txt` dependencies into a virtual environment, and running `Runtime Calculator.py` externally via the command line.  Not so glamorous, I know.  Give me a moment with this!

## Development Stuff

This is developed in python as a Workflow Integration plugin, using Resolve/Fusion's `UIDispatch` and `UIManager` for native widgets.

## Donations

If you're pickin' up what I'm throwin' down around here, and you think you might like me as a person, donations are greatly appreciated!

- https://ko-fi.com/lilbinboy

---

*\* Extreme-ness not guaranteed*
