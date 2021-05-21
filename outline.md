# On the Duration of Core Helium Burning

## Abstract

After stars reach the tip of the Red Giant Branch (RGB) they ignite Helium in their cores and quickly move onto the Horizontal Giant Branch (HGB). Because the HGB is very near the RGB in the Hertzsprung-Russel diagram, this produces an overabundance of stars in a region known as the Red Clump (RC). Here we use the observed properties of single and binary systems in the RC from SDSS DR17 to infer the duration of core helium burning. We find that the Core Helium Burning (CHeB) phase of stellar evolution takes about half as long as RGB stars take to pass through the RC. The nature of this inference means that the fractional time on the CHeB is independent of uncertainties in stellar evolution.We further use stellar models to convert this into an absolute time, and find that to be of order $30\rm Myr$. This is at some variance with existing calculations, and we discuss possible reasons for the discrepancies.

## Introduction



## Data



## Method

Stars expand dramatically as they pass from the RC to the tip of the RGB (TRGB). Binary stars that are too close together likely merge along the way, including many systems whose orbits lie entirely within the envelope of the primary on the TRGB. As a result we expect the HGB to be depleted in binaries relative to the RGB.

In particular, we may confidently identify all such binaries binaries whose orbits are smaller than the $\sim 10^3 R_\odot$ envelopes of TRGB stars as living on the RGB. Hereinafter we consider only binaries whose orbits are smaller than this threshold.

Let $f$ be the binary fraction of stars as a function of $\log g$. Let $f_r$ be the binary fraction of stars on the RGB as a function of $\log g$. Let $f_c$ be the binary fraction of stars on the RC, calculated across all stars on the RC (not a function of $\log g$). Notice that $f_c=f$ inside the RC and $f_r = f$ outside the RC, but that $f_r$ is not a direct observable inside the RC without identifying which stars are on the RGB and which are on the HGB.

Even though $f_r$ is not directly observable in the RC, it is related to $f_c$ by
$$
f_c = \frac{f_r(\mathrm{RC}) N_r}{N_c}
$$
where $N_r$ is the number of stars in the RC which are on the RGB, and $N_c$ is the total number of stars in the RC. Assuming a steady flux of stars through the HR diagram, we see that the duration of the HGB is related to the time RGB stars spend in the RC by
$$
\frac{\tau_{\rm HGB}}{\tau_{\rm RC}} = \frac{N_c}{N_r} = \frac{f_r({\rm RC})}{f_c}
$$
Assuming $f_r$ is smooth, we may estimate $f_r(\rm RC)$ in the RC by interpolating from values just outside the RC on either side, or by fitting a smooth polynomial to the data outside the RC. We then average it across the RC . Using equation (2) above then gives us the duration ratio.



**Thoughts from meeting with Adrian:**

1. Can use the peak deficit.
2. Can also try average the deficit over the clump using the *excess* of stars as a measure of where the clump is (as a weight).

## Analysis

### Time Ratio

Figures that would be good to have include:

- Plot of binary fraction as a function of $\log g$.
- Plot of interpolation for $f_r({\rm RC})$ for a few different interpolants (to show insenstivity).
- Maybe a plot of the duration ratio as a function of where exactly we draw the RC boundaries.

We probably also want to bin by mass to see if the duration changes noticeably across masses (if we have enough data + dynamic range for that to be interesting).

### Absolute Time

Figures include:

- $\log g$ vs time.
- $\log T_{\rm eff}$ vs time.
- Time spent in the RC versus $Z$ and $M$.

All of these can come from MESA.

## Conclusions

