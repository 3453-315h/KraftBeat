// @name Trance Arps
// @genre Techno
// @bpm 138
// @tags trance, uplifting, arpeggios, euphoric

setcpm(138 / 4)

// ═══════════════════════════════════════════════════════════════
// TRANCE ARPS - Uplifting euphoric energy with classic builds
// ═══════════════════════════════════════════════════════════════

// Punchy kick with dynamics and builds
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.15 1.1 1.12 1.08> <1.1 1.08 1.15 [1.18 1.1]>")  // Dynamics
    .shape(slider(0.2, 0, 0.5))
    .every(8, x => x.s("bd bd bd bd [bd bd] bd bd"))  // 8-bar phrase
    .every(16, x => x.s("bd bd bd [bd bd] bd bd [bd*4] [bd*8]"))  // Build pattern
    .every(32, x => x.s("~ ~ ~ ~ ~ ~ ~ ~"))  // Breakdown (drop kick)
    .color("orange")
    ._punchcard()

// Offbeat hats with velocity dynamics
$hat: s("~ hh ~ hh ~ hh ~ oh").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.5))  // Humanized
    .pan(perlin.range(-0.1, 0.1).slow(0.25))  // Stereo
    .sometimes(x => x.s("~ hh ~ hh ~ [hh hh] ~ oh"))  // Double hat
    .every(8, x => x.s("[hh hh] [hh hh] [hh hh hh hh] [oh hh]"))  // Fill
    .every(16, x => x.s("[hh*4] [hh*4] [hh*8] [hh*16]"))  // Build tension
    ._punchcard()

// Clap with ghost and fills
$clap: stack(
    s("~ cp ~ cp").gain(slider(0.9, 0, 2)).room(0.35),
    s("~ [~ cp:3] ~ ~").gain(0.22).lpf(5000)  // Ghost
).bank("RolandTR909")
    .every(8, x => x.s("~ cp ~ [cp cp cp cp]"))  // 8-bar fill
    .color("white")
    ._punchcard()

// Snare roll for builds
$snareroll: s("~ ~ ~ ~ ~ ~ ~ ~")
    .bank("RolandTR909")
    .every(16, x => x.s("~ ~ ~ ~ ~ ~ sd [sd*4] ~ ~ ~ ~ [sd*4] [sd*8] [sd*16] [sd*32]"))
    .gain(slider(0.65, 0, 2))
    .lpf(sine.range(3000, 10000).fast(8))
    .color("yellow")

// THE trance arpeggio - uplifting with variations
$arp: note("<c5 e5 g5 c6 g5 e5 c5 g4>".add("<0 0 5 5 7 7 5 5>"))
    .s("sawtooth")
    .lpf(sine.range(2000, 6000).slow(slider(8, 2, 16)))
    .attack(slider(0.008, 0, 0.04))
    .decay(slider(0.12, 0.03, 0.28))
    .room(slider(0.32, 0, 0.7))
    .gain(slider(0.55, 0, 2))
    .jux(x => x.add(7))  // Stereo 5th
    .sometimes(x => x.fast(2).gain(0.42))  // Double-time runs
    .every(8, x => x.note("<c5 e5 g5 c6 e6 g6 c6 e6>"))  // Ascending build
    .color("cyan")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Counter arp for thickness
$arp2: note("<g4 ~ e4 ~ c4 ~ e4 ~>")
    .s("triangle")
    .lpf(3500)
    .decay(0.15)
    .delay(0.2)
    .room(0.25)
    .gain(slider(0.3, 0, 1.2))
    .color("yellow")

// Bassline with movement
$bass: note("<c2 c2 c2 c2 a1 a1 g1 g1>")
    .s("sawtooth")
    .lpf(sine.range(400, 750).slow(8))
    .decay(slider(0.12, 0.04, 0.28))
    .gain(slider(0.85, 0, 2))
    .rarely(x => x.note("<c2 c2 [c2 e2] g2 a1 a1 [g1 a1] c2>"))  // Variation
    .scope({ size: 256 })
    .color("red")

// Sub layer
$sub: note("<c1 c1 c1 c1 a0 a0 g0 g0>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.4, 0, 1.2))
    .color("darkred")

// Euphoric lead with emotional variations
$lead: note("<g5 ~ a5 ~ c6 ~ ~ ~ g5 ~ e5 ~ c5 ~ ~ ~>")
    .s("sawtooth")
    .lpf(sine.range(5000, 8500).slow(8))
    .attack(slider(0.05, 0, 0.15))
    .decay(slider(0.35, 0.12, 0.65))
    .room(slider(0.45, 0, 0.9))
    .gain(slider(0.48, 0, 1.8))
    .slow(2)
    .sometimes(x => x.note("<g5 a5 c6 e6 g5 e5 c5 g5>").fast(2))  // Fast emotional phrase
    .rarely(x => x.add(12))  // Octave up
    .color("magenta")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Big euphoric pad
$pad: note("<[c3,e3,g3,c4] [c3,e3,g3,c4] [a2,c3,e3,a3] [g2,b2,d3,g3]>")
    .s("sawtooth")
    .lpf(sine.range(1000, 4000).slow(16))
    .attack(slider(0.6, 0.25, 1.3))
    .release(slider(0.8, 0.35, 1.6))
    .room(slider(0.55, 0, 1))
    .gain(slider(0.38, 0, 1.3))
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
