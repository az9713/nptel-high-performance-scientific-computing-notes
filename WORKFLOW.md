# Lecture-note production workflow

The NPTEL IIT Bombay course recordings provide the chronological spine of this
independent textbook rewrite. The plan groups playlist items 2–76 (75
recordings) into 31 topic chapters; the Week 12 revision lectures (items 71–74)
supply practice material, and the course trailer (item 1) is outside the
selected scope. This edition contains 31 chapters covering 75 assigned recordings.

1. Enumerate recordings and preserve lecture order, labels, durations, and source
   URLs in the source manifest.
2. Produce local faster-whisper `small.en` machine transcripts and retain source
   media and slide frames privately. The playlist's caption tracks are attached
   to the wrong videos, so they were not used. Machine recognition can introduce
   errors; a transcript reading is corrected only when a slide or the context
   confirms it.
3. Write one representative pilot chapter (chapter 11, OpenMP I) through the full
   pass sequence, review it, and record the lessons in the authoring contract
   before the other chapters start.
4. Read the assigned transcripts and develop substantial exposition with
   definitions, prerequisites, notation, derivations, and explicit assumptions.
   Inspect slide frames and accessible primary references for cited claims.
   Preserve uncertainty and unverified-claim labels instead of inventing
   page-level verification.
5. Develop original teaching constructions, runnable C, Python and Bash programs,
   and worked problems. Run every program on the verification machine and print
   its actual output beside it. Distinguish these constructions from lecture
   statements and empirical observations. Mark output that depends on timing or
   thread interleaving, so it is checked for a successful exit only.
6. Obtain an independent chapter review (correctness, lecture fidelity, rigor,
   sources, code, contract, prose), repair the findings, obtain a second
   independent review, repair again, and record the review rounds in the
   chapter sidecar. The lead spot-checks each repair. Full acceptance requires
   an independent zero-blocking verdict on the latest round.
7. Wrap authored bodies in the shared reader, preserving exact content digests.
   Validate links, timestamps, mathematics rendering, controls, and desktop/mobile
   layouts with bundled CSS, JavaScript, and MathJax.
8. Keep chapter commits, assemble public documentation and curated evidence,
   and publish only after explicit authorization. Raw sources and internal
   editorial material remain outside the repository.

All 31 chapters are written and independently reviewed. The latest recorded review of each written chapter has zero blocking findings. Historical verdicts are preserved in [the editorial record](editorial-review-summary.json); publication, content inventory and reader checks do not replace scientific acceptance.

Publication adds the same root-level HTML, sidecars, bundled assets, tools,
README preview, workflow documentation, and evidence-record arrangement used by
the other NPTEL repositories. The code laboratory indexes and launches the
existing chapter programs. Its execution checks reproduce teaching
constructions on one machine; they do not independently review the
derivations, and timings differ on other hardware.

The builder operates entirely on a downloaded repository. It does not require
private media, transcripts, original authoring folders, or a network connection.
The command-line code checker builds and runs listings in separate temporary
directories and records their output comparisons. Browser verification checks
actual offline reader behavior. Source-free export and live-publication checks
are recorded separately.
