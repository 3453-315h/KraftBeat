// @name Hardstyle
// @genre Techno
// @bpm 150
// @tags hardstyle, hard, reverse bass, euphoric

setcpm(150 / 4)

// ═══════════════════════════════════════════════════════════════
// HARDSTYLE - Euphoric leads, reverse bass, pounding kicks
// ═══════════════════════════════════════════════════════════════

// Hardstyle kick with dynamics and build fills
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.4 1.32 1.38 1.32> <1.35 1.32 1.4 [1.45 1.35]>")  // Power dynamics
    .shape(slider(0.38, 0, 0.75))
    .every(4, x => x.s("[bd bd] bd bd bd"))  // 4-bar punch
    .every(8, x => x.s("bd bd bd bd [bd bd] bd bd"))  // 8-bar phrase
    .every(16, x => x.s("bd bd bd [bd bd] bd bd [bd*4] [bd*8]"))  // Build pattern
    .color("orange")
    ._punchcard()

// Offbeat hats with velocity dynamics
$hat: s("~ hh ~ hh ~ hh ~ oh").bank("RolandTR909")
    .gain(perlin.range(0.32, 0.48))  // Humanized velocity
    .pan(perlin.range(-0.1, 0.1).slow(0.25))  // Subtle stereo
    .sometimes(x => x.s("~ hh ~ hh ~ [hh hh] ~ oh"))  // Double hat
    .every(8, x => x.s("[hh hh] [hh hh] [hh hh hh hh] [oh hh]"))  // Hat fill
    .every(16, x => x.s("[hh*4] [hh*4] [hh*8] [hh*16]"))  // Build tension
    ._punchcard()

// Clap with ghost and fills
$clap: stack(
    s("~ cp ~ cp").gain(slider(0.9, 0, 2)).room(0.25),
    s("~ [~ cp:3] ~ ~").gain(0.25).lpf(5000)  // Ghost
).bank("RolandTR909")
    .every(8, x => x.s("~ cp ~ [cp cp cp cp]"))  // 8-bar fill
    .color("white")
    ._punchcard()

// Snare roll builds
$snareroll: s("~ ~ ~ ~ ~ ~ ~ ~")
    .bank("RolandTR909")
    .every(16, x => x.s("~ ~ ~ ~ ~ ~ sd [sd*4] ~ ~ ~ ~ [sd*4] [sd*8] [sd*16] [sd*32]"))
    .gain(slider(0.7, 0, 2))
    .lpf(sine.range(3000, 10000).fast(8))
    .color("yellow")

// Reverse bass - THE hardstyle signature with dynamics
$bass: note("<c1 c1 c1 c1 d#1 d#1 g0 g0>")
    .s("sawtooth")
    .lpf(sine.range(150, 1500).fast(slider(4, 1, 8)))
    .lpq(sine.range(2, 8).slow(2))  // Resonance sweep
    .decay(slider(0.08, 0.02, 0.2))
    .gain(slider(0.95, 0, 2))
    .rarely(x => x.note("<c1 c1 [c1 d#1] c2 d#1 d#1 g0 c1>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })

// Sub layer for weight
$sub: note("<c1 c1 c1 c1 d#1 d#1 g0 g0>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.4, 0, 1.2))
    .color("darkred")

// Euphoric lead melody with variations
$lead: note("<g5 ~ c6 ~ d#6 ~ c6 ~ g5 ~ ~ ~ d#5 ~ g5 ~>")
    .s("sawtooth")
    .lpf(sine.range(5000, 9000).slow(8))
    .attack(slider(0.02, 0, 0.08))
    .decay(slider(0.25, 0.08, 0.5))
    .room(slider(0.38, 0, 0.8))
    .gain(slider(0.52, 0, 2))
    .slow(2)
    .sometimes(x => x.note("<g5 c6 d#6 c6 g5 d#5 c5 g5>").fast(2))  // Double-time phrase
    .rarely(x => x.add(12))  // Octave up
    .color("cyan")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Counter melody
$lead2: note("<~ ~ ~ ~ c5 ~ d#5 ~ ~ ~ ~ ~ g4 ~ ~ ~>")
    .s("triangle")
    .lpf(4500)
    .decay(0.2)
    .room(0.25)
    .gain(slider(0.35, 0, 1.5))
    .slow(2)
    .color("yellow")

// Supersaw stab with variations
$stab: note("<[c5,d#5,g5] ~ ~ ~ ~ ~ ~ ~ [g4,a#4,d5] ~ ~ ~ ~ ~ ~ ~>")
    .s("sawtooth")
    .lpf(sine.range(4000, 7500).slow(4))
    .attack(slider(0.005, 0, 0.03))
    .decay(slider(0.15, 0.04, 0.32))
    .room(slider(0.35, 0, 0.75))
    .gain(slider(0.5, 0, 2))
    .sometimes(x => x.fast(2).gain(0.4))  // Double stab
    .color("magenta")
    ._punchcard()

// Big euphoric pad
$pad: note("<[c3,d#3,g3,c4] [c3,d#3,g3,c4] [d#3,g3,a#3,d#4] [g2,a#2,d3,g3]>")
    .s("sawtooth")
    .lpf(sine.range(2000, 4500).slow(16))
    .attack(slider(0.5, 0.2, 1.1))
    .release(slider(0.6, 0.25, 1.2))
    .room(slider(0.5, 0, 1))
    .gain(slider(0.35, 0, 1.2))
    .slow(4)
    .color("purple")
    .scope({ size: 256 })

// Crash for drops
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.55)
    .room(0.5)
    .slow(2)

// Reverse crash for builds
$revcr: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ cp:5")
    .gain(0.5)
    .speed(-1)
    .room(0.6)
    .slow(4)
