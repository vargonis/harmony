# Microtonal Explorations

We want to explore just-intonation modulation and harmonic/melodic systems. 
Let's start by stating our understanding of the standard 12-semitone system, so as to explore the possible variations on its underlying principle.

## The standard western system

Harmony is in the ratio of note frequencies. An octave is a factor of $2$. A fifth is $3/2$ (and its converse, a fourth, is $4/3$).
A major third is $5/4$, and its complement to reach $3/2$ is $6/5$, a minor third.

There is an amazing beauty in how those ratios fit together to create a system. Starting from a base frequency of 1, we can stack
the most harmonic ratios $3/2$, $4/3$ and $5/4$ filling the (multiplicative) interval from $1$ to $2$, like this:

$$
1,\ 5/4,\ 4/3,\ 3/2,\ 5/3,\ 15/8,\ 2.
$$

The rationale behind the choice of the last two steps is: $4/3\cdot 5/4 = 5/3$, and $3/2\cdot 5/4 = 15/8$.
Now, note that the (multiplicative) "distance" from $4/3$ to $3/2$ is $9/8$, whereas the distance from
$3/2$ to $5/3$ is $10/9$. We see a remarkable progression of simple ratios that fit together to form the factor $2$.
The distance from $5/4$ to $4/3$ is $16/15$, which is also what's missing to get from $15/8$ to $2$. Thus, we can form a scale by stacking together the following sequence of increments:

$$
1\xrightarrow{9/8} 9/8\xrightarrow{10/9} 5/4\xrightarrow{16/15} 4/3\xrightarrow{9/8} 3/2\xrightarrow{10/9} 5/3\xrightarrow{9/8} 15/8\xrightarrow{16/15} 2.
$$

This is the major scale.
We can also switch the internal decomposition of the fifth into major/minor thirds, to get a minor scale arrangement:

$$
1\xrightarrow{9/8} 9/8\xrightarrow{16/15} 6/5\xrightarrow{10/9} 4/3\xrightarrow{9/8} 3/2\xrightarrow{10/9} 5/3\xrightarrow{16/15} 16/9\xrightarrow{9/8} 2.
$$

This one has a major sixth (dorian mode, common in jazz). The classical (aeolian mode) alternative would be

$$
1\xrightarrow{9/8} 9/8\xrightarrow{16/15} 6/5\xrightarrow{10/9} 4/3\xrightarrow{9/8} 3/2\xrightarrow{16/15} 8/5\xrightarrow{10/9} 16/9\xrightarrow{9/8} 2.
$$

(Explain well-temperedness.)

## The mathematics of harmony

At the heart of the above harmonic subdivisions is the following fact:

$$
\frac{n+1}{n} = \frac{2n+2}{2n+1} \frac{2n+1}{2n}
$$

Thus, the octave is subdivided into a perfect fifth and a perfect fourth ($2 = 3/2\cdot 4/3$), and the perfect fifth is subdivided into a major third and a minor third ($3/2 = 5/4\cdot 6/5$). The western system is based on those two subdivisions. But what about the harmonic subdivision of the perfect fourth, $4/3 = 8/7\cdot 7/6$? Based on it, we can build the following pentatonic scale:

$$
1\xrightarrow{7/6} 7/6\xrightarrow{8/7} 4/3\xrightarrow{9/8} 3/2\xrightarrow{7/6} 7/4\xrightarrow{8/7} 2.
$$

It has simpler ratios, but does not have "thirds". <!-- it decomposes $4/3$ (the perfect fourth), as opposed to $3/2$ (the perfect fifth) into two steps (one major, one minor). --> Its "minor" variant would be

$$
1\xrightarrow{8/7} 8/7\xrightarrow{7/6} 4/3\xrightarrow{9/8} 3/2\xrightarrow{8/7} 12/7\xrightarrow{7/6} 2.
$$

### Going deeper

Now, this only scratchs the surface. Consider the following sequences:
$$
(2, 3) / 2 \quad \rightarrow\quad \text{a perfect fifth}
$$
$$
(3, 4, 5) / 3 \quad \rightarrow\quad \text{a major chord (2nd inversion)}
$$
$$
(4, 5, 6, 7) / 4 \quad \rightarrow\quad \text{a dominant chord (fundamental position)}
$$
$$
(5, 6, 7, 8, 9) / 5 \quad \rightarrow\quad \text{some new stuff from now on...}
$$

But there's more: now consider their corresponding "inversions":
$$
4 / (4,3) \quad \rightarrow\quad \text{a perfect fourth}
$$
$$
6 / (6,5,4) \quad \rightarrow\quad \text{a minor chord (fundamental position)}
$$
$$
8 / (8,7,6,5) \quad \rightarrow\quad \text{a minor-7th chord (2nd inversion)}
$$
$$
10 / (10,9,8,7,6) \quad \rightarrow\quad \text{?}
$$
We want to explore the vast musical landscape that opens up with the observations above.

## Software implementation

We need a simple synthesizer that supports arbitrary frequency notes. In order to avoid implementing it from scratch, we've hacked a way to do it with standard tools.

### Python's `mido` + `fluidsynth`

This is our current implementation. Here are some rough setup notes.

`pip install mido python-rtmidi`.

Then, `sudo apt-get install fluidsynth`. Fluidsynth does not work with neither `alsa` nor `pulseaudio` for me (launches, no sound is produced, even system sounds stop working, until terminal is killed because `quit` seems to work but `fluidsynth` does not actually quit, terminal simply stops responding). So:

`fluidsynth -a jack GeneralUser_GS.sf2`

Problem: as `Qjackctl` shows, `fluidsynth` is not connected to playback output on startup. Have to connect it manually (using `Qjackctl` graph). To avoid this:

`fluidsynth --audio-driver=jack --connect-jack-outputs FluidR3_GM.sf2`

Now, to generate arbitrary frequency samples we need to use the `pitch` attribute, which is associated to a channel, not a single note. Thus, each channel becomes single-note, for microtonal purposes. This is a shame, but works for simple tests (polyphony is severely restricted).

### Potential alternatives

#### Use ALSA

To compile, need to `sudo apt-get install libasound2-dev`. Then, `gcc alsa.c -lasound`. See https://www.linuxjournal.com/article/6735.

#### Possibly useful links

Pyfluidsynth, [faust](https://faustdoc.grame.fr/), [supercollider](https://supercollider.github.io/). See https://wiki.linuxaudio.org/wiki/start.
