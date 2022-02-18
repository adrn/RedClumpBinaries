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

---

## Updates

- The validation check doesn't work. The data's just too noisy. So we see lots of variation in the RHS in (10).
- Integrating over $\log g$ with measure $q$ produces results that seem well-behaved and consistent between e.g. adjacent bins in metallicity. So we'll use that as our headline result.
- I checked and $dt/d\log g|r$ does vary substantially (2x or more) with mass, so we need to account for mass here.



## Planned Storyboard

- Intro
  - The CHeB is interesting.
  - Predicting CHeB timing is hard because convective boundaries screw us over (MESA 4, MESA 5).
  - If we could tell which stars are CHeB vs RGB in the Red Clump, the ratio of their numbers would tell us the time spent on the CHeB.
    - This is a hard sample to get, because it requires seismology.
  - Conveniently, on the RGB stars get big, and engulf their binary companions.
  - Hence, binarity is correlated with being a CHeB star in the Red Clump.
  - We use APOGEE stars with binarity determinations to figure out how long stars spend on the CHeB.
- Theory
  - Stars expand dramatically as they pass from the RC to the tip of the RGB (TRGB).
    - Figure: HR diagram showing evolution from the ZAMS through the TACHeB.
  - Binary stars that are too close together likely merge along the way, including many systems whose orbits lie entirely within the envelope of the primary on the TRGB.
  - When stars contract onto the CHeB they should have very few binaries.
  - As a result we expect the Red Clump (RC), which are a mix of CHeB and RGB stars, to be depleted in binaries relative to the RGB.
  - Stars move fast from the TRGB onto the CHeB, then sit on the CHeB for a while, then move fast onto the AGB.
  - Run through the logic above through equation (10).
- Data
  - Adrian writes some stuff about APOGEE and the data set.
  - Explain our assumptions, e.g. that we take $[M/H]=0$ when $Z_\odot=0.014$ for running MESA models with APOGEE metallicities.
- Method
  - We do some basic cuts on mass, metallicity, $\log g$.
  - We divide the data into bins of mass and metallicity. For each bin:
    - We fit $q$ using a mixture model.
      - Show an example figure.
    - We fit $f_r$ using a linear model excluding the region where $q > q_{\rm min}$.
      - Show an example figure.
    - We interpolate $dt/d\log g|r$ from MESA models run through the ZACHeB for various masses and metallicities.
      - Show a figure of $dt/d\log g|r$ versus $\log g$ for a few masses.
    - Our headline numbers:
      - We average equation (10) over the region where $q > q_{\rm min}$, weighting by $q$, giving $\tau_{\rm CHeB}$.
        - At this stage comment on how there's lots of noise in the RHS of (10), which is why we can't use that directly.
      - We also average $(1/q)(\frac{f_r(\log g)}{f(\log g)}-1)$, weighted by $q$, over the region where $q > q_{\rm min}$, giving an estimate of $\tau_{\rm CHeB}/\tau_{\rm RGB}$, independent of the MESA models. 
        - By $\tau_{\rm RGB}$ we mean the time it takes to pass through the Red Clump on the ascent of the RGB, where the Clump is for that (mass, metallicity) bin.
- Results
  - Table showing:
    - Bin properties
    - Number of stars in each bin
    - Range in $\log g$ with $q > q_{\rm min}$, identifying the RC.
    - $\tau_{\rm CHeB}$ in that bin with error bars
    - $\tau_{\rm CHeB}/\tau_{\rm RGB}$ in that bin with error bars.
  - Maybe some plots of trends in mass and metallicity?
- Discussion
  - Lars can hopefully say something here.
  - Key point is that the CHeB is much shorter than MESA models suggest.
    - Points to differences in treatment of convective boundary mixing.



## Some more thoughts

I got worried about $q$ for a while and managed to make myself not worried, so I wanted to write that down.

Suppose we had observational uncertainties that blurred the RC out more, so that $q$ is a broader distribution. Let's say it doubles the width. That changes $f_r/f-1$ by making $f_r/f$ closer to $1$ (roughly halves it), but we don't want our headline number to be sensitive to this blurring.

Fortunately it isn't, at least not to leading order. The quantity we estimate $\tau_{\rm CHeB}$ from has a $1/q$ out front, so even though $f_r/f-1$ roughly halves if we double the width of $q$,  that gets cancelled out by the magnitude of $q$ halving because the integral of $q$ is conserved.

But wait, you say, we integrate with respect to the measure $q$, so doesn't this come out dependent on the blur? No! Because the integral is now over twice the range. So we've halved $f_r/f-1$ but integrated it over twice the range, giving a nearly-unchanged number ('nearly' because $dt/d\log g$ is varying slowly in the background).

So, $f_r/f-1$ is only meaningful as a way of describing the observations. $\tau_{\rm CHeB}$ though is physically meaningful.
