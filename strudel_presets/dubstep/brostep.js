// @name Brostep
// @genre Dubstep
// @bpm 145
// @tags brostep, growl, aggressive, skrillex

setcpm(145 / 4)

// ═══════════════════════════════════════════════════════════════
// BROSTEP - Aggressive growl bass with hard drops
// ═══════════════════════════════════════════════════════════════

// Hard hitting half-time kick
$kick: s("bd ~ ~ ~ ~ ~ ~ ~ bd ~ ~ ~ ~ ~ bd ~").bank("RolandTR808")
    .gain("<1.3 1.25 1.28 1.2> <1.25 1.2 1.3 [1.35 1.25]>")  // Power dynamics
    .shape(slider(0.4, 0, 0.8))
    .every(4, x => x.s("[bd bd] ~ ~ ~ ~ ~ ~ ~ bd ~ ~ ~ ~ ~ bd ~"))  // Double kick
    .every(8, x => x.s("bd ~ bd ~ ~ ~ ~ ~ bd ~ bd ~ ~ ~ [bd bd] bd"))  // Build
    .color("orange")
    ._punchcard()

// Snare with heavy impact on 3
$snare: stack(
    s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ sd ~ ~ ~").gain(slider(1.2, 0, 2)).room(slider(0.15, 0, 0.4)),
    s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ [sd:3 sd:3] ~ ~").gain(0.35).lpf(6000)  // Ghost rush
).bank("RolandTR808")
    .every(8, x => x.s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ sd ~ [sd*4] [sd*8]"))  // Build
    ._punchcard()

// Fast rolling hats
$hat: s("hh*16").bank("RolandTR808")
    .gain(perlin.range(0.38, 0.55))  // Velocity
    .pan(perlin.range(-0.12, 0.12).slow(0.25))
    .sometimes(x => x.fast(1.5))  // Triplets
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh*16]"))  // Build
    ._punchcard()

// GROWL BASS - heavy modulation
$growl: note("<c1 ~ c1 ~ c1 [c1 d#1] f1 [d#1 c1]>")
    .s("sawtooth")
    .lpf(sine.range(200, 3000).fast(slider(4.0, 1, 16)))
    .lpq(sine.range(6, 16).slow(2))  // Aggressive resonance
    .decay(slider(0.1, 0.03, 0.22))
    .gain(slider(0.88, 0, 2))
    .chop(sine.range(4, 16).slow(2))  // Heavy modulation
    .rarely(x => x.fast(2))  // Double-time bass
    .every(4, x => x.lpf(sine.range(300, 4500).fast(8)))  // Faster modulation
    .color("cyan")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Mid growl layer
$midgrowl: note("<c2 ~ c2 ~ c2 [c2 d#2] f2 [d#2 c2]>")
    .s("square")
    .lpf(sine.range(600, 2200).fast(8))
    .lpq(10)
    .decay(0.08)
    .gain(slider(0.45, 0, 1.5))
    .chop(sine.range(4, 8).slow(2))
    .color("orange")

// Sub layer
$sub: note("<c1 ~ c1 ~ c1 c1 f1 c1>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.55, 0, 1.5))
    .color("darkred")

// Scream lead with modulation
$scream: note("<c4 ~ ~ ~ d#4 ~ ~ ~ f4 ~ d#4 ~ c4 ~ ~ ~>")
    .s("sawtooth")
    .lpf(sine.range(2000, 6000).slow(slider(4.0, 1, 16)))
    .lpq(sine.range(4, 10).slow(4))  // Resonance sweep
    .decay(slider(0.15, 0.05, 0.3))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.52, 0, 2))
    .sometimes(x => x.note("<d#4 f4 g4 f4 d#4 c4>"))  // Variation
    .rarely(x => x.fast(2))  // Rapid lead
    .color("magenta")
    ._punchcard()
    .scope({ size: 256 })

// Crash for drops
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR808")
    .gain(0.6)
    .room(0.4)
    .slow(2)
