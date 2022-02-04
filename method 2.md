## Premise

- Stars expand dramatically as they pass from the RC to the tip of the RGB (TRGB).
- Binary stars that are too close together likely merge along the way, including many systems whose orbits lie entirely within the envelope of the primary on the TRGB.
- When stars contract onto the CHeB they should have very few binaries.
- As a result we expect the Red Clump (RC), which are a mix of CHeB and RGB stars, to be depleted in binaries relative to the RGB.
- Stars move fast from the TRGB onto the CHeB, then sit on the CHeB for a while, then move fast onto the AGB.

## Definitions

- We can identify all binaries whose orbits are smaller than  $\sim 10^3 R_\odot$.
  - That's also the radius of a TRGB star.
  - We'll call these systems binaries going forward, and call all other systems are single.
- With these definitions:
  -  The binary fraction of CHeB ($f_c$) is zero.
  -  The binary fraction of the RGB ($f_r$) is some decreasing function towards lower $\log g$, eventually reaching zero at the TRGB.

## Populations

Stars move fast from the TRGB to the CHeB, then sit on the CHeB for a while, then move onto the AGB fast. The net result is that there is some excess population on the Red Clump (blurred by metallicity, rotation, etc.). We can model this by saying that a star entering the CHeB will land at a $\log g$ given by some probability distribution $q(\log g)$ normalized by $\int qd\log g=1$, so that the distribution of CHeB stars is
$$
\frac{dn_c}{d\log g} = n_c q(\log g)
$$
where $n_c$ is the total number of CHeB stars, given by
$$
n_c = \dot{N} \tau_{\rm CHeB}
$$
Here $\dot{N}$ is the star-formation rate, assumed constant, and $\tau_{\rm CHeB}$ is the time stars spend on the CHeB.

The total number of stars we see at any given $\log g$ is given by
$$
\frac{dn}{d\log g} = \frac{dn_c}{d\log g} + \frac{dn_r}{d\log g}
$$
We can relate the second term to the SFR by
$$
\dot{N} = \frac{dn_r}{d\log g} \left.\frac{d\log g}{dt}\right|_r
$$
where $d\log g/dt$ is the rate that stars evolve through a given region of the HR diagram. With some algebra on the last three equations we find
$$
\frac{dn}{d\log g} = \dot{N} \tau_{\rm CHeB} q(\log g) + \frac{dn_r}{d\log g}\\
= \frac{dn_r}{d\log g}\left(1 + \tau_{\rm CHeB} q(\log g)\left.\frac{d\log g}{dt}\right|_r\right)
$$
Just to break this down:

- $dn/d\log g$ is observed.
- $dn_r/d\log g$ is not (directly).
- $q(\log g)$ is not (directly).
- $d\log g/dt|_r$ is something we're confident in from theory (time to go up the RGB).
- $\tau_{\rm CHeB}$ is something we'd like to infer. **That's the headline result!!!**

## Distribution of CHeB Stars

One thing we need to infer from the observations is $q(\log g)$. Fortunately this is given by the excess population on the Red Clump. Specifically, we can notice that $dn/d\log g$ has a bump at the RC. We can then fit a line to the background ($dn_r/d\log g$) outside the bump, subtract that line, and get the excess. Normalize that and you get $q(\log g)$.

Ideally we'd have a physical basis for the line we fit. If we wanted to be really careful we'd do something like use a theoretical $d\log g/dt$ and constant SFR to get the shape of that line. But I think that's too much to do here, especially because the true SFR probably isn't exactly constant and there's metallicity and rotation and all that good stuff. So let's ignore that and fit a line.

## Binaries

At any given $\log g$, the binary fraction is some mix of the RGB binary fraction and the CHeB binary fraction:
$$
f(\log g)\frac{dn}{d\log g} = \frac{dn_{r}}{d\log g} f_{r} + \frac{dn_{c}}{d\log g}f_c
$$
but because $f_c = 0$, we have just
$$
f(\log g)\frac{dn}{d\log g} = \frac{dn_{r}}{d\log g} f_{r}(\log g)
$$
We know $f(\log g)$ and $dn/d\log g$ from observations. That's just the overall binary fraction as a function of $\log g$. We'd like to infer $dn_r/d\log g$, so that we can plug it into equation (3) above and obtain $d\log g/dt|_c$.

To get at $dn_r/d\log g$, we need to know $f_r(\log g)$. Fortunately we can get at this by interpolating across the RC. Essentially we pick two points on opposite sides of the RC, far enough away that we're confident all the stars are on the RGB. Then we fit a function in between.

What function do we fit? Ideally we'd fit something informed by the radius evolution of stars and the period distribution of the binaries. In particular:

- Take the period distribution of binaries on the subgiant branch (before ascending the RGB).
- Turn this into a distribution of semimajor axes $df/da$ (this is the fraction of binaries at semimajor axis $a$).
- $df_r/d\log g = -(dR/d\log g)(df/da)$. There may need to be a scaling up/down because more binaries are destroyed than just the directly engulfed ones, so we can fit this by throwing a scaling factor in front.
  - $dR/d\log g$ we also know as $-R/2$, so the function we fit is:
    - $df_r/d\log g = \alpha R df/da$, where $\alpha$ is a free parameter.

I don't think the details of this part will matter all that much so I'd be inclined to once more just fit a line. The point is that we can get a plausible $f_r(\log g)$. Given that, we write
$$
\frac{dn_r}{d\log g} = \frac{f(\log g)}{f_r(\log g)}\frac{dn}{d\log g}
$$
and so
$$
1 + \tau_{\rm CHeB} q(\log g)\left.\frac{d\log g}{dt}\right|_r = \frac{f_r(\log g)}{f(\log g)}
$$
or
$$
 \tau_{\rm CHeB} = \frac{1}{q(\log g)}\left(\frac{f_r(\log g)}{f(\log g)}-1\right)\left.\frac{dt}{d\log g}\right|_r
$$
The object on the LHS is the thing we want! And note that it's independent of $\log g$, which means the object on the RHS ought to be independent of $\log g$ as well. That provides something of a validation check that we can perform. If it's not independent (which seems likely given all the uncertainties in the analysis) we probably want to note that and provide an average or central value for $\tau_{\rm CHeB}$. (Probably don't believe values on the edges of the RC where $q$ gets small anyway...).





