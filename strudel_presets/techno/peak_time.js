// @name Peak Time Techno
// @genre Techno
// @bpm 138
// @tags peak, energy, main room, driving

setcpm(138 / 4)

// ═══════════════════════════════════════════════════════════════
// PEAK TIME TECHNO - Main room energy, driving intensity
// ═══════════════════════════════════════════════════════════════

// Powerful 909 kick with dynamics and fills
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.25 1.18 1.22 1.18> <1.2 1.18 1.25 [1.28 1.2]>")  // Power dynamics
    .shape(slider(0.25, 0, 0.6))
    .every(4, x => x.s("[bd bd] bd bd bd"))  // 4-bar punch
    .every(8, x => x.s("bd bd bd bd [bd bd] bd bd"))  // 8-bar phrase
    .every(16, x => x.s("bd bd bd bd bd bd [bd bd bd bd] [bd*8]"))  // Build
    .color("orange")
    ._punchcard()

// Driving hats with velocity dynamics
$hat: s("[~ hh] [~ hh] [~ oh] [~ hh]").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.52))  // Humanized velocity
    .pan(perlin.range(-0.1, 0.1).slow(0.25))  // Subtle stereo
    .sometimes(x => x.s("[~ hh] [hh ~] [~ oh] [hh hh]"))  // Variation
    .every(8, x => x.s("[hh hh] [hh hh] [hh oh hh hh] [hh hh]"))  // Fill
    .every(16, x => x.s("[hh*4] [hh*4] [hh*8] [hh*16]"))  // Build tension
    ._punchcard()

// Snappy clap with ghost notes
$clap: stack(
    s("~ cp ~ cp").gain(slider(0.92, 0, 2)).room(0.25).delay(0.12),
    s("~ [~ cp:3] ~ ~").gain(0.25).lpf(5000)  // Ghost
).bank("RolandTR909")
    .every(8, x => x.s("~ cp ~ [cp cp cp cp]"))  // 8-bar fill
    .color("white")
    ._punchcard()

// Snare roll build-ups
$snareroll: s("~ ~ ~ ~ ~ ~ ~ ~")
    .bank("RolandTR909")
    .every(16, x => x.s("~ ~ ~ ~ ~ ~ sd [sd*4] ~ ~ ~ ~ [sd*4] [sd*8] [sd*16] [sd*32]"))
    .gain(slider(0.65, 0, 2))
    .lpf(sine.range(3000, 10000).fast(8))
    .color("yellow")

// Ride for intensity layers
$ride: s("~ ~ ~ ~ ~ ~ ~ rd").bank("RolandTR909")
    .gain(slider(0.35, 0, 1.5))
    .sometimes(x => x.s("~ ~ rd ~ ~ ~ ~ rd"))  // Double ride
    .every(8, x => x.s("rd*8").gain(0.28))  // Ride layer
    ._punchcard()

// Big room stab with evolving filter
$stab: note("<[c4,g4,c5] ~ ~ ~ [a3,e4,a4] ~ ~ ~ [g3,d4,g4] ~ [c4,g4,c5] ~ ~ ~ ~ ~>")
    .s("sawtooth")
    .lpf(sine.range(1200, 5500).slow(8))
    .attack(slider(0.008, 0, 0.05))
    .decay(slider(0.15, 0.04, 0.35))
    .room(slider(0.28, 0, 0.65))
    .gain(slider(0.58, 0, 2))
    .sometimes(x => x.fast(2).gain(0.45))  // Double stab energy
    .rarely(x => x.note("<[d4,a4,d5]>"))  // Variation
    .color("magenta")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Rolling bass with movement
$bass: note("<c1 c1 c1 c2 a0 a0 g0 g0>")
    .s("sawtooth")
    .lpf(sine.range(180, 700).slow(4))
    .decay(slider(0.1, 0.03, 0.25))
    .gain(slider(0.88, 0, 2))
    .rarely(x => x.fast(2))  // Rolling bass fills
    .scope({ size: 256 })
    .color("red")

// Sub layer for weight
$sub: note("<c1 c1 c1 c1 a0 a0 g0 g0>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.45, 0, 1.2))
    .slow(2)
    .color("darkred")

// Atmospheric pad builds tension
$pad: note("<[c3,g3,c4] [c3,g3,c4] [a2,e3,a3] [g2,d3,g3]>")
    .s("sawtooth")
    .lpf(sine.range(500, 2800).slow(16))
    .attack(slider(0.5, 0.15, 1.1))
    .release(slider(0.6, 0.2, 1.2))
    .room(slider(0.5, 0, 1))
    .gain(slider(0.32, 0, 1.2))
    .slow(4)
    .color("purple")
    .scope({ size: 256 })

// Crash for drops/transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.5)
    .room(0.4)
    .slow(2)

// Reversed crash for tension
$revcr: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ cp:5")
    .gain(0.45)
    .speed(-1)
    .room(0.5)
    .slow(4)
