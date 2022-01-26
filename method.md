## Premise

- Stars expand dramatically as they pass from the RC to the tip of the RGB (TRGB).
- Binary stars that are too close together likely merge along the way, including many systems whose orbits lie entirely within the envelope of the primary on the TRGB.
- When stars contract onto the CHeB they should have very few binaries.
- As a result we expect the Red Clump (RC), which are a mix of CHeB and RGB stars, to be depleted in binaries relative to the RGB.

## Definitions

- We can identify all binaries binaries whose orbits are smaller than  $\sim 10^3 R_\odot$.
  - That's also the radius of a TRGB star.
  - We'll call these systems binaries going forward, and call all other systems are single.
- With these definitions:
  -  The binary fraction of CHeB ($f_c$) is zero.
  - The binary fraction of the RGB ($f_r$) is some decreasing function towards lower $\log g$, eventually reaching zero at the TRGB.

## Populations

The total number of stars we see at any given $\log g$ is given by
$$
\frac{dn}{d\log g} = \frac{dn_c}{d\log g} + \frac{dn_r}{d\log g}
$$
We can relate these to the star formation rate if we assume it's uniform:
$$
\dot{N} = \frac{dn_r}{d\log g} \left.\frac{d\log g}{dt}\right|_r = \frac{dn_c}{d\log g} \left.\frac{d\log g}{dt}\right|_c
$$
where $d\log g/dt$ is the rate that stars evolve through a given region of the HR diagram. With some algebra on the last two equations we find
$$
\frac{dn}{d\log g} = \frac{dn_r}{d\log g}\left(1 + \left.\frac{d\log g}{dt}\right|_r\left.\frac{dt}{d\log g}\right|_c\right)
$$
Just to break this down:

- $dn/d\log g$ is observed.
- $dn_r/d\log g$ is not (directly).
- $d\log g/dt|_r$ is something we're confident in from theory (time to go up the RGB).
- $d\log g/dt|_c$ is something we'd like to infer. **That's the headline result!!!**

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

I don't think the details of this part will matter all that much. The point is that we can get a plausible $f_r(\log g)$. Given that, we write
$$
\frac{dn_r}{d\log g} = \frac{f(\log g)}{f_r(\log g)}\frac{dn}{d\log g}
$$
and so
$$
1 + \left.\frac{d\log g}{dt}\right|_r\left.\frac{dt}{d\log g}\right|_c = \frac{f_r(\log g)}{f(\log g)}
$$
or
$$
\left.\frac{dt}{d\log g}\right|_c = \left(\frac{f_r(\log g)}{f(\log g)}-1\right)\left.\frac{dt}{d\log g}\right|_r
$$
The object on the LHS is the thing we want! And we can turn it into a lifetime for the Red Clump by integrating it over the $\log g$ range of the RC.





