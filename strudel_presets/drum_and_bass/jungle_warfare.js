// @name Jungle Warfare
// @genre Drum and Bass
// @bpm 174
// @tags complex, jungle, breaks, amen, aggressive

setcpm(174 / 4)

// ═══════════════════════════════════════════════════════════════
// JUNGLE WARFARE - Complex chopped breaks and rolling bass
// ═══════════════════════════════════════════════════════════════

// Amen-style break pattern with dynamics
$break1: s("[bd ~ ~ bd] [~ sd ~ ~] [bd ~ bd ~] [~ sd ~ sd]")
    .bank("RolandTR909")
    .gain("<1.0 0.95 0.98 0.92> <0.95 0.98 1.0 [1.05 0.98]>")  // Dynamics
    .shape(slider(0.28, 0, 0.55))
    .every(4, x => x.s("[bd ~ bd bd] [~ sd ~ ~] [bd ~ bd ~] [~ sd sd sd]"))  // Variation
    .every(8, x => x.s("[bd bd ~ bd] [~ sd ~ sd] [bd ~ bd bd] [~ sd sd sd]"))  // Fill
    .color("orange")
    ._punchcard()

// Ghost snares - essential jungle texture
$ghost: s("~ [sd:3 ~] ~ [~ sd:3]")
    .bank("RolandTR909")
    .gain(perlin.range(0.28, 0.42))  // Velocity variation
    .lpf(perlin.range(4000, 8000))
    .sometimes(x => x.s("[sd:3 ~] [sd:3 sd:3] ~ [sd:3 ~]"))  // Extended pattern
    .color("gray")

// Ride pattern with movement
$ride: s("rd*8")
    .bank("RolandTR909")
    .gain(perlin.range(0.35, 0.52))  // Humanized
    .lpf(perlin.range(5000, 12000))
    .pan(perlin.range(-0.15, 0.15).slow(0.25))
    .sometimes(x => x.fast(2).gain(0.4))  // Double-time intensity
    .color("white")
    ._punchcard()

// Hi-hat rolls with triplets
$hat: s("[hh hh hh hh] [hh hh [hh hh hh] hh]")
    .bank("RolandTR909")
    .gain(perlin.range(0.28, 0.42))
    .lpf(perlin.range(6000, 12000))
    .sometimes(x => x.fast(1.5))  // Triplets
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh*16]"))  // Build
    .color("white")
    ._punchcard()

// Reese bass with Jungle movement
$reese: note("<c2 c2 [c2 eb2] c2> <c2 g1 [f1 g1] c2>")
    .s("sawtooth")
    .lpf(sine.range(250, 1000).fast(slider(2, 1, 8)))
    .lpq(sine.range(2, 8).slow(4))  // Resonance movement
    .decay(slider(0.15, 0.06, 0.3))
    .gain(slider(0.82, 0, 2))
    .rarely(x => x.note("<c2 eb2 [f2 g2] c2>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Sub bass layer
$sub: note("<c1 ~ ~ ~> <~ g0 ~ ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.55, 0, 1.5))
    .slow(slider(4.0, 1, 16))
    .color("darkred")
    ._punchcard()
    .scope({ size: 256 })

// Synth stabs with variations
$stab: note("<[c4,eb4,g4] ~> <~ [g3,bb3,d4]> <[f3,ab3,c4] ~> <~ [eb3,g3,bb3]>")
    .s("square")
    .lpf(sine.range(1500, 4000).slow(slider(4.0, 1, 16)))
    .decay(slider(0.12, 0.04, 0.25))
    .delay(slider(0.2, 0, 0.5))
    .room(slider(0.35, 0, 0.8))
    .gain(slider(0.5, 0, 2))
    .fast(slider(2, 1, 8))
    .sometimes(x => x.fast(2).gain(0.4))  // Double stab
    .color("cyan")
    ._punchcard()

// Pad atmosphere
$pad: note("[c3,g3,c4]")
    .s("sawtooth")
    .lpf(sine.range(500, 1500).slow(slider(8.0, 1, 16)))
    .attack(slider(0.5, 0.2, 1.1))
    .release(slider(0.6, 0.25, 1.2))
    .gain(slider(0.42, 0, 1.5))
    .room(slider(0.45, 0, 1))
    .slow(slider(4.0, 1, 16))
    .sometimes(x => x.note("[eb3,g3,bb3]"))  // Chord variation
    .color("purple")
    .scope({ size: 256 })

// Vocal chop simulation
$vox: s("~ ~ ~ [cp:5 ~]")
    .chop(4)
    .speed(choose(0.75, 1, 1.25))
    .room(slider(0.35, 0, 0.8))
    .delay(slider(0.25, 0, 0.6))
    .gain(slider(0.42, 0, 1.5))
    .sometimes(x => x.s("~ cp:5 ~ [cp:5 cp:5]"))  // Extended pattern
    .color("pink")
    ._punchcard()

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.5)
    .room(0.45)
    .slow(2)
