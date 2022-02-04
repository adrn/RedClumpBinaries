## Todo Online

- For metallicity: a few bins, plus one that lumps them all together.

- [x] Find the lowest metallicity such that CHeB stars are still in APOGEE. **[Done. Sticking to M/H > -1.5]**
- [ ] Get $q(\log g)$, the distribution of CHeB stars (i.e. the normalized distribution of the excess of stars on the RC).
  - [ ] Fit a Gaussian+background to number counts in each bin of metallicity.
- [ ] Get $f_r(\log g)$, the binary fraction for stars ascending the RGB.
  - [ ] Something like: fit the binary fraction on either side of the RC (where $q \ll 1$), then interpolate to get the value inside the RC.
  - [ ] Want to check the sensitivity of the final results to the way we did this interpolation, though it probably doesn't matter too much (the RC is a relatively narrow feature and nothing else is changing fast in $\log g$ here...).
- [ ] Get $f(\log g)$, the overall binary fraction on the RC.
- [ ] Load $dt/d\log g|_r$ from theory.

---

## Todo Offline

### Adam

- [ ] Factor notebooks into standalone scripts.
- [ ] Change mixture model from Gaussian+Truncated Broad Gaussian to Gaussian+Uniform or Gaussian+Line. 

### Adrian

- [ ] Check sensitivity to J-K cuts. Aim is to find the lowest metallicity for which we're confident APOGEE covers the RC. [**Current value in notebooks is -1, we think -1.5 might be fine**]