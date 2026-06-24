// @name Roller
// @genre Drum and Bass
// @bpm 172
// @tags roller, minimal, rolling, driving

setcpm(172 / 4)

// ═══════════════════════════════════════════════════════════════
// ROLLER - Minimal rolling DnB with hypnotic groove
// ═══════════════════════════════════════════════════════════════

// Minimal roller kick - driving pattern
$kick: s("bd ~ bd ~ bd ~ bd ~").bank("RolandTR909")
    .gain("<1.0 0.95 0.98 0.92> <0.95 0.98 1.0 [1.05 0.98]>")  // Driving dynamics
    .shape(slider(0.28, 0, 0.55))
    .rarely(x => x.s("bd bd bd ~ bd ~ bd ~"))  // Double kick accent
    .every(16, x => x.s("bd ~ bd bd bd ~ bd ~ bd bd bd ~ bd ~ bd bd"))  // Variation
    .color("orange")
    ._punchcard()

// Snare with ghost textures
$snare: stack(
    s("~ ~ sd ~ ~ ~ sd ~").gain(slider(0.9, 0, 2)).room(0.3),
    s("~ ~ ~ [sd:3 ~] ~ ~ ~ [~ sd:3]").gain(0.28).lpf(5000)  // Ghosts
).bank("RolandTR909")
    .every(8, x => x.s("~ ~ sd ~ ~ ~ sd [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Fast rolling hats - continuous drive
$hat: s("hh*16").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.52))  // Humanized velocity
    .pan(perlin.range(-0.12, 0.12).slow(0.25))
    .lpf(perlin.range(6000, 12000))
    .sometimes(x => x.s("[hh*4] [hh hh oh hh] [hh*4] [hh hh hh oh]"))  // Accents
    .every(8, x => x.fast(1.5).gain(0.45))  // Triplet energy
    .color("white")
    ._punchcard()

// Ride layer for intensity
$ride: s("rd*8").bank("RolandTR909")
    .gain(perlin.range(0.25, 0.38))
    .pan(perlin.range(-0.2, 0.2).slow(0.5))
    .sometimes(x => x.fast(2).gain(0.32))  // Double-time layer
    .color("gray")
    ._punchcard()

// Rolling bass - hypnotic pattern
$bass: note("<c2 c2 c2 c2 d#2 d#2 f2 d#2>")
    .s("sawtooth")
    .lpf(sine.range(350, 1200).fast(slider(2, 1, 8)))
    .lpq(sine.range(2, 6).slow(4))  // Resonance movement
    .decay(slider(0.12, 0.04, 0.25))
    .gain(slider(0.82, 0, 2))
    .rarely(x => x.note("<c2 c2 [c2 d2] d#2 f2 f2 [f2 d#2] c2>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Sub layer for weight
$sub: note("<c1 c1 c1 c1 d#1 d#1 f1 d#1>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.55, 0, 1.5))
    .color("darkred")

// Subtle stab with delay
$stab: note("[c4,d#4,g4]")
    .s("square")
    .lpf(sine.range(1500, 4000).slow(slider(4.0, 1, 16)))
    .struct("~ ~ ~ ~ x ~ ~ ~")
    .decay(slider(0.12, 0.04, 0.25))
    .delay(slider(0.25, 0, 0.6))
    .delaytime(0.25)
    .room(slider(0.35, 0, 0.8))
    .gain(slider(0.48, 0, 2))
    .sometimes(x => x.struct("~ ~ x ~ x ~ ~ ~"))  // Double stab
    .rarely(x => x.note("[d4,f4,a4]"))  // Variation
    .color("cyan")
    ._punchcard()

// Atmospheric layer
$atmo: note("[c3,g3]")
    .s("sawtooth")
    .lpf(sine.range(300, 800).slow(16))
    .attack(1)
    .release(0.8)
    .room(0.5)
    .gain(slider(0.18, 0, 0.5))
    .slow(8)
    .color("purple")
    .scope({ size: 256 })

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.48)
    .room(0.4)
    .slow(2)
