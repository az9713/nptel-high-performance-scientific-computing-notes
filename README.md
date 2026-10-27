# High Performance Scientific Computing — a textbook rewrite

**[Read the live textbook](https://az9713.github.io/nptel-high-performance-scientific-computing-notes/)**

[![Preview of the live High Performance Scientific Computing textbook](assets/site-preview.png)](https://az9713.github.io/nptel-high-performance-scientific-computing-notes/)

This project is an independent rewrite and expansion of Prof. Shivasubramanian
Gopalakrishnan's NPTEL IIT Bombay course, **High Performance Scientific Computing**.
The **[January 2025 YouTube playlist](https://www.youtube.com/playlist?list=PLOzRYVm0a65fSrgx3kroerFJtFjGGIcXm)
serves as the spine**: it sets the topic sequence and provides timestamped
anchors for the exposition.

Around that spine, the project develops explanations, definitions, derivations,
measurements, runnable C, Python and Bash programs, and worked problems. Source
maps distinguish lecture material, research extensions, and original teaching
constructions. Chapter citations and sidecars record source uncertainties and
claims that could not be checked.

**This is a partial edition.** The plan groups **75 recordings** (playlist items
2–76) into **31 chronological topic chapters**; the 2-minute course trailer is
outside the selected scope. **Chapters 1–11 are written.** They cover the first
**20 recordings**, from Week 0 Lecture 0 to Week 4 Lecture 1: the Linux
environment, HPC hardware and memory, concurrency, the cost of numerical models,
memory bottlenecks, and an introduction to OpenMP. **Chapters 12–31 (OpenMP II
onward: MPI, GPUs and CUDA, OpenACC, profiling, libraries, schedulers) are not
yet written**; the lecture index lists them as pending.

The written chapters contain **66 expandable solution disclosures** and **125
runnable listings** (56 C, 43 Python, 26 Bash). Transcripts were produced
locally with faster-whisper `small.en`; they are machine transcriptions, not
publisher captions. The NPTEL caption tracks on the playlist are attached to
the wrong videos and were not used.

The reader includes searchable chapter navigation, local MathJax, light/dark
themes, adjustable text size, expandable solutions, printing with solutions,
and a code-lab directory and launcher for the chapter programs. Rendering
assets are bundled, so a downloaded copy also works offline.

Explore the [source map](https://az9713.github.io/nptel-high-performance-scientific-computing-notes/source-map.html),
[primary references](https://az9713.github.io/nptel-high-performance-scientific-computing-notes/references.html),
and [code lab](https://az9713.github.io/nptel-high-performance-scientific-computing-notes/code-lab.html).
The preview above opens the live GitHub Pages edition, served from `index.html`.

## Run locally

Open `index.html` after downloading the repository. To rebuild and check it:

```sh
python tools/build_book.py
python tools/validate_books.py --browser
python code_lab.py
python code_lab.py --chapter 9
python tools/check_chapter_code.py
python tools/check_package.py
```

Rebuilding and static checks use Python's standard library. The chapter
programs run in a Linux shell: natively on Linux, or through WSL 2 on Windows
(`code_lab.py` calls `wsl`; set `HPSC_WSL_DISTRO` if the distribution is not
named `Ubuntu`). They need gcc with OpenMP support; the Python programs of
chapters 1, 4 and 9 also need NumPy. Browser checks require Python Playwright
and an installed supported browser.

All runs and timings made for these chapters come from one laptop (the lecture
screens analysed in the text come from the lecturer's machines): an Intel Core i5-12450H
(4 performance cores with 2 hardware threads each and 4 efficiency cores, 12
logical CPUs), an NVIDIA GeForce RTX 3050 Laptop GPU, WSL 2 Ubuntu 24.04 and
gcc 13.3. Timings, bandwidths and speedups differ on other machines. Listings
whose output depends on timing or thread interleaving are checked for a
successful exit only; the others are checked byte for byte.

## Evidence and scope

Every written chapter has two recorded independent review rounds. After each
round the author repaired the findings, and the lead checked the repairs.
**Final independent sign-offs remain pending for chapters 3, 9, 10 and 11**:
their second-round reviews (verdict "accept with fixes") still recorded one
blocking finding each. Those findings were repaired and checked by the lead,
but no later independent zero-blocking verdict is recorded. Chapters 1, 2 and
4–8 ended with zero blocking findings. Publication does not close those review
gaps.

The [workflow](WORKFLOW.md), [source record](source-validation-summary.json),
[editorial record](editorial-review-summary.json), [content inventory](completion.json),
[code checks](chapter-code-validation.json), [reader checks](reader-validation.json),
[clean-export checks](source-free-validation.json), and [package checks](package-validation.json)
record the evidence and its limits. Code checks report execution and
printed-output agreement separately from scientific acceptance. Reader checks
assess rendering and controls, not mathematical correctness. A whole-book
scientific review, full audiovisual review, and human accessibility
certification are not claimed. The [publication check](publication-validation.json)
records served-file integrity of the live GitHub Pages edition.

Public files contain the rewritten textbook, supporting code, source citations,
and curated verification records. Raw recordings, transcripts, slide frames,
downloaded papers, and private editorial records (author briefs and review
reports) remain outside this repository. Published instructor and
research-author names are retained for source attribution. GitHub Pages serves
the `main` branch at the repository root, matching the other NPTEL reading
editions.
