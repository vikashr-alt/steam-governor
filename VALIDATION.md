# Evidence and unresolved checks

## Actually performed on 15 October 2026

- Retrieved and extracted all five pages of the provided assignment.
- Retrieved Maxwell's original paper through Cambridge and the Science Museum catalogue entry cited in the paper. Limited comparison established relevant liquid-governor and integral-regulation prior art. No exhaustive search or originality certification.
- Executed `code/verify.py`: 12,002 reported LTI samples across both signs, independent eigenmode comparison, half-step repeat, sign symmetry, nonlinear pressure-sensor comparison, all 64 parameter corners and an intentionally unstable integral gain. Numerical tolerances and results are recorded in `results/verified.json`.
- Student executed the supplied MATLAB script and provided the completion screenshot, metrics CSV, full trace CSVs and both PNG plots. Metrics agreed with Python within 1e-9. Full traces also passed comparison; see `results/matlab_crosscheck.json`. Paper plots now use the MATLAB trace CSVs. MATLAB RK4/expm maximum error was 2.251e-11 in each case.
- Generated and rendered the PDF. Five main paper pages, followed by one appendix page; inspected all six pages. No invisible content overflow was allowed by the generator.

## Not performed

- Octave execution was not tested. MATLAB was executed by the student, rather than in the assistant environment; its release number was not recorded.
- LaTeX compilation: `paper.tex` is an editable IEEEtran source; delivered PDF was separately typeset by ReportLab in two-column IEEE style. Exact official-template conformity and source pagination require compilation/review. The delivered PDF has five paper pages plus one appendix, but that does not establish the source's page count.
- No prototype, experiment, detailed lever force balance, calibrated engine parameters, exhaustive historical component audit, verified novel-invention claim, repository publication or form submission.

## Before submission

1. MATLAB execution and comparison are complete. Record the release number and retain the output files; rerun after any numerical changes.
2. Resolve float force/valve friction and moving-outlet construction. If a pilot servo is added, include its dynamics and repeat the stability analysis.
3. Revisit novelty against prior art; obtain instructor guidance if necessary.
4. Author vikas H R, roll no. 23B2282 is recorded. Repository: https://github.com/vikashr-alt/steam-governor. Compile `paper.tex` in the official IEEE conference template, polish equation numbering and verify main-paper/appendix page limits; compare content with the provided PDF.
5. Update the AI appendix with actual student decisions and validation. Submit through official course links and complete the confidential peer evaluation independently.

The artifact is therefore a substantial, reproducible project draft with explicit remaining validation, not a submission-ready claim of completion.
