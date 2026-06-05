# Problem and requirements

Our project answers **2022 MCM Problem A — "Power Profile of a Cyclist."** Full statement: [`../references/2022_PowerOfCyclist.pdf`](../references/2022_PowerOfCyclist.pdf).

**The question.** In an individual time trial a rider covers a fixed course alone; fastest time wins. Each rider has a *power curve* (the most power they can hold for a given duration), a limited total energy budget, and accumulating fatigue from past over-effort. Given a rider's power curve, how should they distribute power along the course to minimise total time?

## Requirements checklist

*Live progress is tracked in the main [README](../README.md#requirements--status); the list below is the detailed source.*

**Riders**
- [ ] Power profiles for **two rider types** — one a **time-trial specialist**, the other a different type (climber, sprinter, rouleur, or puncheur).
- [ ] Consider **different genders**.

**Courses** (run every rider on every course)
- [ ] **2021 Olympic ITT — Tokyo, Japan**
- [ ] **2021 UCI Worlds ITT — Flanders, Belgium**
- [ ] **One self-designed course** — ≥4 sharp turns, ≥1 nontrivial grade, finishing near the start *(see [`../data/courses/custom_5km_loop.csv`](../data/courses/custom_5km_loop.csv))*.

**Analysis**
- [ ] **Power distribution vs. position** that minimises time, within the energy budget and fatigue limits.
- [ ] **Weather sensitivity** — effect of wind direction and strength.
- [ ] **Power-deviation sensitivity** — effect of the rider missing the target power; expected range of split times.

**Extension**
- [ ] Discuss extending to a **team time trial** of six riders (team time set by the **fourth** finisher).

**Write-up**
- [ ] Follow the **M142 structure** in [`paper-outline.md`](paper-outline.md) — *not* the contest's 25-page format. The class assignment states explicitly: do not follow the contest write-up instructions.
- [ ] The contest's two-page "Directeur Sportif race guidance" is a contest deliverable — include only if the group/professor wants it.
