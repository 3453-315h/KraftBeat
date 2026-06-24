// @name Crossbreed
// @genre Drum and Bass
// @bpm 180
// @tags crossbreed, hardcore, industrial, gabber

setcpm(180 / 4)

// ═══════════════════════════════════════════════════════════════
// CROSSBREED - Industrial hardcore meets DnB
// ═══════════════════════════════════════════════════════════════

// Industrial distorted kick with power
$kick: s("bd ~ ~ ~ bd ~ bd ~").bank("RolandTR909")
    .gain("<1.3 1.25 1.28 1.2> <1.25 1.2 1.3 [1.35 1.25]>")  // Power dynamics
    .shape(slider(0.85, 0, 1))  // Heavy distortion
    .every(4, x => x.s("[bd bd] ~ ~ ~ bd ~ bd ~"))  // Double kick
    .every(8, x => x.s("bd ~ bd ~ bd ~ [bd bd bd bd] bd"))  // 8-bar fill
    .color("orange")
    ._punchcard()

// Heavy industrial snare
$snare: stack(
    s("~ ~ sd ~ ~ ~ sd ~").gain(slider(1.1, 0, 2)).room(0.25),
    s("~ ~ ~ [sd:3 sd:3] ~ ~ ~ [sd:3 ~]").gain(0.35).lpf(6000)  // Ghost rush
).bank("RolandTR909")
    .every(4, x => x.s("~ ~ sd ~ ~ [sd sd] sd ~"))  // Roll
    .every(8, x => x.s("~ ~ sd ~ ~ ~ sd [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Fast industrial hats
$hat: s("hh*16").bank("RolandTR909")
    .gain(perlin.range(0.4, 0.58))  // Hard velocity
    .lpf(perlin.range(6000, 14000))  // Bright
    .pan(perlin.range(-0.15, 0.15).slow(0.25))
    .sometimes(x => x.fast(1.5))  // Triplets
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh*16]"))  // Build
    .color("white")
    ._punchcard()

// Aggressive crossbreed bass
$bass: note("<c1 c1 [c1 d#1] c1 f1 f1 [d#1 c1] c1>")
    .s("sawtooth")
    .lpf(sine.range(200, 3000).fast(slider(4, 1, 16)))
    .lpq(sine.range(6, 15).slow(2))  // Aggressive resonance
    .decay(slider(0.12, 0.04, 0.25))
    .gain(slider(0.88, 0, 2))
    .chop(sine.range(4, 16).slow(4))  // Wobble
    .rarely(x => x.fast(2))  // Double-time bass
    .scope({ size: 256 })
    .color("red")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Mid bass layer for thickness
$midbass: note("<c2 c2 [c2 d#2] c2 f2 f2 [d#2 c2] c2>")
    .s("square")
    .lpf(sine.range(600, 2000).fast(4))
    .lpq(8)
    .decay(0.1)
    .gain(slider(0.45, 0, 1.5))
    .color("orange")

// Sub layer
$sub: note("<c1 c1 c1 c1 f1 f1 c1 c1>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.55, 0, 1.5))
    .color("darkred")

// Industrial hit
$hit: s("industrial:0")
    .struct("~ ~ ~ ~ x ~ ~ ~")
    .chop(4)
    .speed(slider(0.6, 0.3, 1.5))
    .slow(slider(4.0, 1, 16))
    .room(0.25)
    .gain(slider(0.52, 0, 2))
    .sometimes(x => x.struct("~ ~ x ~ x ~ ~ ~"))  // Double hit
    .color("orange")

// Gabber-style synth lead
$synth: note("<c4 ~ d#4 ~ c4 ~ ~ ~>")
    .s("square")
    .lpf(sine.range(1500, 5000).slow(slider(4.0, 1, 16)))
    .decay(0.15)
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.52, 0, 2))
    .sometimes(x => x.note("<d#4 f4 d#4 c4>"))  // Variation
    .rarely(x => x.fast(2))  // Fast arps
    .color("magenta")
    .scope({ size: 256 })

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.6)
    .room(0.35)
    .slow(2)
