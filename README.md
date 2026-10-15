# Water-inventory steam-engine governor: provisional ME319 project

This is a reviewable engineering draft, not a validated invention or a final submission. Author: **vikas H R**, roll number **23B2282**. Repository: https://github.com/vikashr-alt/steam-governor. Physical validation remains unresolved.

## Files and reproduction

- `paper/paper_and_ai_appendix.pdf`: five-page IEEE-style two-column paper plus one-page AI appendix.
- `paper/paper.tex`: editable IEEEtran source; the PDF was generated separately with ReportLab, not compiled from this source. Compare layout and content after compiling.
- `code/run_governor.m`: MATLAB / GNU Octave entry point, standard matrix operations, RK4 and `expm`, no control toolbox.
- `code/verify.py`: actually executed independent NumPy validation; RK4, eigenmode solution, halved timestep, sign symmetry, nonlinear pressure-sensor comparison, and 64 parameter corners.
- `results/verified.json`: executed Python results, parameters and checks. CSVs hold all traces.
- `figures/`: vector plots and schematic used in the paper. Student-generated MATLAB PNG plots and CSVs are included; the paper plots are drawn from those MATLAB trace CSVs.
- `code/build_paper.py`: PDF/figure generation, requires Python, NumPy, ReportLab and Pillow; supplied font paths are macOS-specific and may need changing.

Run MATLAB or Octave:

```matlab
cd code
run_governor
```

Or at a terminal: `octave --quiet --eval "addpath('code'); run_governor"` from the repository root. The student executed the script in MATLAB and supplied the CSVs, plots and completion screenshot. Both cases were independently checked: peak times 1.89 s, settling times 10.43 s, and RK4/expm maximum error 2.251e-11. Reported metrics agree with Python within 1e-9; full trace differences are recorded in `results/matlab_crosscheck.json`. MATLAB release was not recorded; Octave has not been tested. Re-running creates separately named `_matlab` output files.

Independent check: `python3 code/verify.py` (Python 3 + NumPy). Generate paper: `python3 code/build_paper.py` (also ReportLab + Pillow). For editable IEEE source install IEEEtran and run `pdflatex paper.tex` in `paper/` after copying desired author information. Source uses provided vector PDFs.

## Definitions

Time in seconds. Speed w=Omega/Omega0; load l=TL/TL0; v=w-1; d=l-1; throttle x in [0,1], u=x-0.6; inventory z=(A/q0)(h-h0), in seconds. Nominal state v=z=u=0. Steps occur at t=0 from equilibrium; load is 1.3 or 0.7 thereafter. Open loop means governor disconnected, throttle held at 0.6.

`M vdot = -D v + K u - d; zdot=v; tau udot=-u-kp v-ki z`.

M=5 s, D=1, K=2, tau=0.5 s, kp=2, ki=0.5 /s. All are selected engineering estimates, not measurements. Speed settling uses |w-w_final|<=0.02*0.3=0.006 for all later samples. Open-loop settling to its own displaced final speed is not successful regulation. Recovery overshoot is excursion across w=1 divided by 0.3; it is zero here. Complex-pair damping is not a damping ratio for the whole third-order system.

## Required student validation / limitations

1. Read the actual assignment and understand every equation; independently verify signs, units, lever gains and Routh table. Student/team names and contributions must reflect actual work.
2. MATLAB execution and independent output comparison are complete. Preserve the supplied results and rerun after any model or parameter change; record the MATLAB release for reproducibility.
3. Verify historical availability of leather differential bellows, low-friction water seals, floating outlet construction and a balanced steam throttle. Plausibility is argued, not established by a prototype or a period construction source.
4. Prototype the floating outlet: maintain constant free-surface-to-discharge elevation through full travel; collect discharge versus level and temperature; quantify leak/priming sensitivity. A fixed outlet would destroy ideal integral action.
5. Measure pump slip versus pressure, flow ripple, pressure-sensor dynamics, float loading, linkage friction/backlash and valve torque. Check force/power authority. Re-tune with measured M,D,K,tau. Steam/chest/boiler dynamics and variable load laws are omitted.
6. Broaden prior-art search beyond Maxwell: Siemens liquid governors, pump-pressure governors, float governors, constant-flow devices and hydraulic PI regulators. A non-centrifugal arrangement is not proof of originality. Instructor may judge it insufficiently novel; redesign if comparison warrants.
7. Check finite travel, startup/shutdown, empty/full tank, siphon loss, blocked pipes and overspeed protection. Normalized model cannot establish mechanical safety or nonlinear global stability.
8. Author vikas H R, roll no. 23B2282 is recorded. The public repository URL is included in the paper. Rebuild paper and verify <=6 main pages + exactly one appendix page. Submit official paper form and each student's confidential peer evaluation by **15 October 2026, 11:59 PM IST**, as specified in the assignment. Form URLs were not recovered and are not invented.

## Source integrity

References are sources actually retrieved during authoring, with scope stated in the paper. Maxwell directly establishes important prior art; museum evidence establishes period pumping context, not this exact governor's construction. The USGS floating-siphon search result is a useful lead, but its full PDF could not be retrieved, so it is not used as a verified paper citation. No claim of exhaustive originality search is made. Do not remove these limitations without evidence.
