// @name Liquid Dreams
// @genre Drum and Bass
// @bpm 174
// @tags liquid, melodic, dorian, soulful

setcpm(174 / 4)

// ═══════════════════════════════════════════════════════════════
// LIQUID DREAMS - Melodic DnB with D Dorian scale
// ═══════════════════════════════════════════════════════════════

// DnB break pattern with dynamics
$kick: s("[bd ~ ~ bd] [~ ~ bd ~] [bd ~ ~ ~] [~ bd ~ bd]").bank("RolandTR909")
    .gain("<1.0 0.95 0.98 0.92> <0.95 0.98 1.0 0.95>")  // Dynamics
    .shape(slider(0.25, 0, 0.5))
    .every(8, x => x.s("[bd ~ ~ bd] [~ bd bd ~] [bd ~ bd ~] [~ bd ~ bd]"))
    .color("orange")
    ._punchcard()

// Snare with ghost layers
$snare: stack(
    s("~ ~ sd ~ ~ ~ sd ~").gain(slider(0.88, 0, 2)).room(0.35),
    s("~ ~ ~ [sd:3 ~] ~ ~ ~ [sd:3 sd:3]").gain(0.28).lpf(5000)  // Ghosts
).bank("RolandTR909")
    .every(8, x => x.s("~ ~ sd ~ ~ ~ sd [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Ride pattern with movement
$ride: s("rd*8").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.5))  // Humanized
    .pan(perlin.range(-0.15, 0.15).slow(0.25))
    .lpf(perlin.range(5000, 12000))
    .sometimes(x => x.fast(2).gain(0.4))  // Double-time
    .color("white")
    ._punchcard()

// Hat rolls
$hat: s("[hh hh hh hh] [hh hh [hh hh hh] hh]").bank("RolandTR909")
    .gain(perlin.range(0.28, 0.42))
    .sometimes(x => x.fast(1.5))  // Triplets
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh*16]"))  // Build
    ._punchcard()

// LIQUID MELODY - D Dorian scale
$melody: n("<0 2 4 7 9 7 4 2>")
    .scale("d:dorian")
    .s("triangle")
    .lpf(sine.range(2500, 6000).slow(slider(4.0, 1, 16)))
    .decay(slider(0.18, 0.08, 0.35))
    .delay(slider(0.25, 0, 0.6))
    .delaytime(0.375)  // Triplet delay
    .room(slider(0.4, 0, 1))
    .gain(slider(0.55, 0, 2))
    .trans(12)  // Up octave
    .sometimes(x => x.rev())  // Reverse melody
    .rarely(x => x.fast(2))  // Double-time
    .color("cyan")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Arp layer
$arp: n("<0 4 7 11 7 4>")
    .scale("d:dorian")
    .s("sine")
    .lpf(4500)
    .decay(0.12)
    .delay(0.3)
    .delaytime(0.25)
    .room(0.35)
    .gain(slider(0.32, 0, 1.2))
    .trans(24)  // Two octaves up
    .color("yellow")

// Pad chords - dorian harmony
$pad: n("<[0,4,7,11] [2,5,9,12] [4,7,11,14] [2,5,9,12]>")
    .scale("d:dorian")
    .s("sawtooth")
    .lpf(sine.range(1000, 3000).slow(8))
    .attack(slider(0.4, 0.15, 0.9))
    .release(slider(0.5, 0.2, 1))
    .room(slider(0.45, 0, 1))
    .gain(slider(0.48, 0, 1.8))
    .slow(4)
    .color("purple")
    .scope({ size: 256 })

// Reese bass with wobble
$bass: n("<0 ~ [0 3] ~> <0 -5 [-7 -5] 0>")
    .scale("d:dorian")
    .s("sawtooth")
    .lpf(sine.range(250, 800).fast(slider(2, 1, 8)))
    .lpq(sine.range(2, 6).slow(4))
    .trans(-24)  // Down 2 octaves
    .decay(slider(0.15, 0.06, 0.3))
    .gain(slider(0.8, 0, 2))
    .rarely(x => x.note("<d2 e2 [f2 e2] d2>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: n("<0 ~ 0 ~ -5 ~ -7 ~>")
    .scale("d:dorian")
    .s("sine")
    .lpf(80)
    .trans(-36)
    .gain(slider(0.52, 0, 1.5))
    .color("darkred")

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.45)
    .room(0.5)
    .slow(2)
