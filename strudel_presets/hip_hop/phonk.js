// @name Phonk
// @genre Hip Hop
// @bpm 130
// @tags phonk, memphis, cowbell, dark

setcpm(130 / 4)

// ═══════════════════════════════════════════════════════════════
// PHONK - Memphis cowbells and dark vibrations
// ═══════════════════════════════════════════════════════════════

// Heavy kick with Memphis punch
$kick: s("bd ~ bd ~").bank("RolandTR808")
    .gain("<1.2 1.15 1.18 1.12> <1.15 1.12 1.2 [1.25 1.15]>")  // Dynamics
    .shape(slider(0.8, 0, 1))
    .every(4, x => x.s("[bd bd] ~ bd ~"))  // Double kick
    .every(8, x => x.s("bd ~ bd ~ [bd bd] ~ bd [bd bd]"))  // 8-bar fill
    .color("orange")
    ._punchcard()

// Rolling phonk hats with variations
$hat: s("hh*16").bank("RolandTR808")
    .gain(perlin.range(0.35, 0.5))  // Humanized
    .pan(perlin.range(-0.2, 0.2).slow(0.25))
    .sometimes(x => x.s("[hh*4] [hh hh oh hh] [hh*4] [hh hh hh oh]"))  // Accents
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh*16]"))  // Build
    ._punchcard()

// Phonk snare with Memphis reverb
$snare: stack(
    s("~ sd ~ sd").gain(slider(0.88, 0, 2)).room(0.4),  // Big Memphis reverb
    s("~ ~ [sd:3 ~] ~").gain(0.25).lpf(4500)  // Ghost
).bank("RolandTR808")
    .every(8, x => x.s("~ sd ~ [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// PHONK COWBELL - THE signature sound
$cowbell: s("cb*4").bank("RolandTR808")
    .gain(perlin.range(0.45, 0.65))  // Velocity variation
    .pan(slider(0.3, -0.5, 0.5))  // Off-center
    .sometimes(x => x.s("cb cb [~ cb] cb"))  // Syncopation
    .rarely(x => x.s("[cb cb] cb cb cb"))  // Extra cowbell
    .every(4, x => x.s("cb cb cb [cb cb]"))  // Fill
    ._punchcard()

// Secondary cowbell layer - higher pitch
$cowbell2: s("~ cb ~ ~").bank("RolandTR808")
    .gain(slider(0.3, 0, 1))
    .speed(1.5)  // Higher pitch
    .pan(slider(-0.3, -0.5, 0.3))
    .color("yellow")

// Dark phonk bass with distortion feel
$bass: note("<c1 ~ c1 ~ c1 ~ [c1 d#1] ~>")
    .s("square")
    .lpf(sine.range(150, 400).slow(slider(4.0, 1, 16)))
    .decay(slider(0.25, 0.1, 0.45))
    .gain(slider(0.82, 0, 2))
    .rarely(x => x.note("<c1 c1 [c1 d1] d#1 d#1 d#1 [d#1 c1] c1>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Sub layer for weight
$sub: note("<c1 ~ c1 ~ c1 ~ c1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.4, 0, 1.2))
    .color("darkred")

// Memphis vocal chop simulation
$vox: s("vocal:2")
    .struct("~ ~ ~ ~ x ~ ~ ~")
    .chop(8)
    .slice(4, "<0 1 2 3>")
    .speed(slider(0.5, 0.25, 1.5))
    .lpf(sine.range(1500, 4000).slow(slider(4.0, 1, 16)))
    .room(slider(0.35, 0, 1))
    .gain(slider(0.48, 0, 2))
    .sometimes(x => x.struct("~ ~ x ~ ~ ~ ~ x"))  // Double chop
    .rarely(x => x.fast(2))  // Rapid chops
    .color("orange")

// Eerie synth melody
$synth: note("<c4 ~ d#4 ~ c4 ~ g3 ~>")
    .s("sawtooth")
    .lpf(sine.range(800, 2500).slow(slider(4.0, 1, 16)))
    .decay(0.2)
    .room(slider(0.35, 0, 1))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.45, 0, 2))
    .sometimes(x => x.note("<c4 d#4 g4 d#4>"))  // Variation
    .color("magenta")
    .scope({ size: 256 })

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR808")
    .gain(0.45)
    .room(0.4)
    .slow(2)
