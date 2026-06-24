// @name Tearout
// @genre Dubstep
// @bpm 148
// @tags tearout, aggressive, metal, heavy

setcpm(148 / 4)

// ═══════════════════════════════════════════════════════════════
// TEAROUT - Ultra-aggressive bass with metal influence
// ═══════════════════════════════════════════════════════════════

// Heavy half-time kick with power
$kick: s("bd ~ ~ ~ ~ ~ ~ ~ bd ~ ~ ~ ~ ~ bd ~").bank("RolandTR808")
    .gain("<1.35 1.28 1.32 1.25> <1.28 1.25 1.35 [1.4 1.3]>")  // Power dynamics
    .shape(slider(0.45, 0, 0.9))  // Heavy distortion
    .every(4, x => x.s("[bd bd] ~ ~ ~ ~ ~ ~ ~ bd ~ ~ ~ ~ ~ bd ~"))  // Double kick
    .every(8, x => x.s("bd ~ bd ~ ~ ~ ~ ~ bd ~ bd ~ ~ ~ [bd bd bd bd] bd"))  // Build
    .color("orange")
    ._punchcard()

// Heavy snare with impact
$snare: stack(
    s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ sd ~ ~ ~").gain(slider(1.15, 0, 2)).room(slider(0.18, 0, 0.5)),
    s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ [sd:3 sd:3] ~ ~").gain(0.38).lpf(6500)  // Ghost rush
).bank("RolandTR808")
    .every(8, x => x.s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ sd [sd sd] [sd*4] [sd*8]"))  // Build
    .color("white")
    ._punchcard()

// Fast aggressive hats
$hat: s("hh*16").bank("RolandTR808")
    .gain(perlin.range(0.3, 0.45))  // Velocity
    .lpf(perlin.range(6000, 12000))
    .pan(perlin.range(-0.12, 0.12).slow(0.25))
    .sometimes(x => x.fast(1.5))  // Triplets
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh*16]"))  // Build
    ._punchcard()

// TEAROUT BASS - ultra aggressive
$bass: note("<c1 ~ c1 [c1 c1] c1 ~ [c1 d#1] c1>")
    .s("sawtooth")
    .lpf(sine.range(200, 3500).fast(slider(4.0, 1, 16)))
    .lpq(sine.range(8, 18).slow(2))  // Extreme resonance
    .decay(slider(0.08, 0.02, 0.18))
    .gain(slider(0.9, 0, 2))
    .chop(sine.range(4, 16).slow(2))  // Heavy modulation
    .rarely(x => x.fast(2))  // Double-time bass
    .every(4, x => x.lpf(sine.range(400, 5000).fast(16)))  // Fastest modulation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Mid tear layer
$midtear: note("<c2 ~ c2 [c2 c2] c2 ~ [c2 d#2] c2>")
    .s("square")
    .lpf(sine.range(700, 2500).fast(8))
    .lpq(12)
    .decay(0.06)
    .gain(slider(0.48, 0, 1.6))
    .chop(sine.range(8, 16).slow(2))
    .color("orange")

// Sub layer
$sub: note("<c1 ~ c1 c1 c1 ~ c1 c1>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.55, 0, 1.5))
    .color("darkred")

// Metal-style power chord lead
$guitar: note("<c4 ~ c4 ~ d#4 ~ [d#4 f4] ~>")
    .s("sawtooth")
    .lpf(sine.range(1500, 5000).slow(slider(4.0, 1, 16)))
    .lpq(sine.range(3, 8).slow(4))  // Resonance movement
    .decay(slider(0.12, 0.04, 0.25))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.note("<d#4 f4 g4 f4 d#4 c4>"))  // Variation
    .rarely(x => x.fast(2))  // Fast runs
    .color("cyan")
    ._punchcard()

// Crash for drops
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR808")
    .gain(0.65)
    .room(0.35)
    .slow(2)
