// @name Halftime
// @genre Drum and Bass  
// @bpm 170
// @tags halftime, heavy, slow, neuro

setcpm(170 / 4)

// ═══════════════════════════════════════════════════════════════
// HALFTIME - Heavy slow drums with modulated bass
// ═══════════════════════════════════════════════════════════════

// Halftime kick - sparse and heavy
$kick: s("bd ~ ~ ~ ~ ~ ~ ~ bd ~ ~ ~ ~ ~ ~ ~").bank("RolandTR909")
    .gain("<1.2 1.15 1.18 1.12> <1.15 1.12 1.2 [1.25 1.18]>")  // Heavy dynamics
    .shape(slider(0.35, 0, 0.7))
    .every(8, x => x.s("bd ~ ~ ~ ~ ~ bd ~ bd ~ ~ ~ ~ ~ ~ ~"))  // Variation
    .every(16, x => x.s("bd ~ ~ bd ~ ~ ~ ~ bd ~ bd ~ ~ ~ bd bd"))  // Build
    .color("orange")
    ._punchcard()

// Halftime snare - on the 3 with heavy impact
$snare: stack(
    s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ sd ~ ~ ~").gain(slider(1.1, 0, 2)).room(0.35),
    s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ [sd:3 ~] ~ ~").gain(0.3).lpf(5000)  // Ghost
).bank("RolandTR909")
    .every(8, x => x.s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ sd ~ [sd sd] sd"))  // Fill
    .color("white")
    ._punchcard()

// Sparse hats with occasional bursts
$hat: s("[~ hh ~ hh] [~ hh ~ hh] [hh ~ hh ~] [~ hh hh hh]").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.52))  // Humanized
    .pan(perlin.range(-0.15, 0.15).slow(0.5))
    .sometimes(x => x.fast(2).gain(0.45))  // Double-time bursts
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh*16]"))  // Hat roll
    .color("white")
    ._punchcard()

// Ride accent
$ride: s("~ ~ ~ ~ ~ ~ ~ rd").bank("RolandTR909")
    .gain(slider(0.4, 0, 1.2))
    .room(0.2)
    .sometimes(x => x.s("~ ~ ~ rd ~ ~ ~ rd"))  // Double ride
    .color("gray")

// Heavy modulated bass - halftime signature
$bass: note("<c1 ~ ~ ~ d#1 ~ ~ ~ f1 ~ ~ ~ d#1 ~ c1 ~>")
    .s("sawtooth")
    .lpf(sine.range(200, 1800).fast(slider(1, 0.5, 8)))
    .lpq(sine.range(4, 12).slow(2))  // Heavy resonance
    .decay(slider(0.15, 0.05, 0.3))
    .gain(slider(0.85, 0, 2))
    .chop(sine.range(4, 16).slow(4))  // Wobble modulation
    .rarely(x => x.note("<c1 d1 [d#1 f1] d#1 f1 d#1 [d#1 c1] c1>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Mid bass layer
$midbass: note("<c2 ~ ~ ~ d#2 ~ ~ ~ f2 ~ ~ ~ d#2 ~ c2 ~>")
    .s("square")
    .lpf(sine.range(500, 1500).fast(1))
    .lpq(5)
    .decay(0.1)
    .gain(slider(0.4, 0, 1.3))
    .color("orange")

// Sub layer
$sub: note("<c1 ~ ~ ~ d#1 ~ ~ ~ f1 ~ ~ ~ d#1 ~ c1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.55, 0, 1.5))
    .color("darkred")

// Dark pad - atmospheric
$pad: note("[c3,d#3,g3]")
    .s("sawtooth")
    .lpf(sine.range(300, 1000).slow(slider(8.0, 1, 16)))
    .attack(slider(0.6, 0.2, 1.2))
    .release(slider(0.7, 0.25, 1.2))
    .slow(slider(4.0, 1, 16))
    .room(slider(0.45, 0, 1))
    .gain(slider(0.42, 0, 1.5))
    .sometimes(x => x.note("[d3,f3,a3]"))  // Chord variation
    .color("purple")
    ._punchcard()
    .scope({ size: 256 })

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.55)
    .room(0.4)
    .slow(2)
