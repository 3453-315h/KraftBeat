// @name Southern Crunk
// @genre Hip Hop
// @bpm 75
// @tags crunk, southern, heavy, atlanta

setcpm(75 / 4)

// ═══════════════════════════════════════════════════════════════
// SOUTHERN CRUNK - Heavy 808s and aggressive energy
// ═══════════════════════════════════════════════════════════════

// Heavy crunk kick with punch
$kick: s("bd ~ bd ~").bank("RolandTR808")
    .gain("<1.3 1.25 1.28 1.22> <1.25 1.22 1.3 [1.35 1.25]>")  // Power dynamics
    .shape(slider(0.85, 0, 1))
    .every(4, x => x.s("[bd bd] ~ bd ~"))  // Double kick
    .every(8, x => x.s("bd ~ bd ~ [bd bd] ~ bd [bd bd]"))  // 8-bar fill
    .color("orange")
    ._punchcard()

// Rolling crunk hats with triplets
$hat: s("[hh hh hh] [hh hh [hh hh]] [hh hh hh] [hh [hh hh] hh]").bank("RolandTR808")
    .gain(perlin.range(0.38, 0.55))  // Velocity variation
    .pan(perlin.range(-0.2, 0.2).slow(0.25))
    .sometimes(x => x.fast(1.5))  // Triplet rolls
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh hh*8]"))  // Build
    ._punchcard()

// Crunk snare with power
$snare: stack(
    s("~ sd ~ sd").gain(slider(0.95, 0, 2)).room(0.35),
    s("~ ~ [sd:3 ~] ~").gain(0.28).lpf(5000)  // Ghost
).bank("RolandTR808")
    .every(4, x => x.s("~ [sd sd] ~ sd"))  // Roll
    .every(8, x => x.s("~ sd ~ [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Clap layer
$clap: s("~ cp ~ cp").bank("RolandTR808")
    .gain(slider(0.5, 0, 1.5))
    .room(0.3)
    .color("gray")

// Heavy 808 bass with sub weight
$bass: note("<c1 ~ c1 ~ c1 ~ [c1 d#1] ~>")
    .s("sine")
    .lpf(slider(140, 60, 220))
    .decay(slider(0.4, 0.2, 0.7))  // Long decay
    .gain(slider(0.88, 0, 2))
    .rarely(x => x.note("<c1 c1 [c1 d1] d#1 d#1 d#1 [d#1 c1] c1>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Synth horn - crunk stab
$horn: note("[c4,d#4,g4,c5]")
    .s("sawtooth")
    .lpf(sine.range(1500, 4000).slow(slider(4.0, 1, 16)))
    .struct("x ~ ~ ~ ~ ~ x ~")
    .decay(slider(0.15, 0.05, 0.3))
    .room(slider(0.25, 0, 0.6))
    .gain(slider(0.58, 0, 2))
    .sometimes(x => x.struct("x ~ x ~ ~ ~ x ~"))  // More hits
    .rarely(x => x.note("[d4,f4,a4,d5]"))  // Variation
    .color("cyan")
    ._punchcard()

// Shout vocal simulation
$shout: s("vocal:0")
    .struct("~ ~ ~ ~ ~ ~ ~ x")
    .chop(4)
    .speed(slider(0.5, 0.25, 1.5))
    .lpf(3000)
    .room(0.2)
    .gain(slider(0.45, 0, 2))
    .sometimes(x => x.struct("~ ~ ~ x ~ ~ ~ x"))  // Double shout
    .rarely(x => x.fast(2))  // Rapid shouts
    .color("orange")

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR808")
    .gain(0.5)
    .room(0.35)
    .slow(2)
