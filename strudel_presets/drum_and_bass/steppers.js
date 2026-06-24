// @name Steppers
// @genre Drum and Bass
// @bpm 173
// @tags steppers, dub, reggae, offbeat

setcpm(173 / 4)

// ═══════════════════════════════════════════════════════════════
// STEPPERS - Dub-influenced DnB with offbeat skanks
// ═══════════════════════════════════════════════════════════════

// Steppers kick pattern with dynamics
$kick: s("bd ~ ~ ~ bd ~ ~ ~").bank("RolandTR909")
    .gain("<1.0 0.95 0.98 0.92> <0.95 0.98 1.0 0.95>")  // Dynamics
    .shape(slider(0.28, 0, 0.55))
    .every(8, x => x.s("bd ~ ~ ~ bd ~ [~ bd] ~"))  // Variation
    .every(16, x => x.s("bd ~ ~ bd bd ~ ~ ~ bd ~ bd ~ bd ~ ~ ~"))  // 16-bar variation
    .color("orange")
    ._punchcard()

// Snare with dub delay
$snare: stack(
    s("~ ~ ~ ~ sd ~ ~ ~").gain(slider(0.88, 0, 2)).room(0.35),
    s("~ ~ ~ ~ ~ [sd:3 ~] ~ ~").gain(0.25).lpf(4500)  // Ghost
).bank("RolandTR909")
    .delay(slider(0.25, 0, 0.6))
    .delaytime(0.375)  // Triplet dub delay
    .every(8, x => x.s("~ ~ ~ ~ sd ~ ~ [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Rolling hats with filter movement
$hat: s("[~ hh] [~ hh] [hh ~] [~ hh]").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.52))  // Humanized
    .lpf(sine.range(5000, 12000).slow(slider(4.0, 1, 16)))
    .pan(perlin.range(-0.15, 0.15).slow(0.5))
    .sometimes(x => x.s("hh*8").gain(0.4))  // 8th note layer
    .every(8, x => x.fast(1.5).gain(0.42))  // Triplet build
    .color("white")
    ._punchcard()

// Dub bass with octave jumps
$bass: note("<c2 ~ [c2 c3] ~ g1 ~ [g1 g2] ~>")
    .s("sawtooth")
    .lpf(sine.range(280, 700).slow(slider(4.0, 1, 16)))
    .lpq(sine.range(1, 4).slow(8))  // Resonance movement
    .decay(slider(0.15, 0.06, 0.3))
    .delay(slider(0.2, 0, 0.5))
    .delaytime(0.375)  // Triplet dub delay
    .gain(slider(0.78, 0, 2))
    .rarely(x => x.note("<c2 [c2 d2] [c2 c3] g2 g1 [g1 a1] [g1 g2] c2>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Sub layer
$sub: note("<c1 ~ c1 ~ g0 ~ g0 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.52, 0, 1.5))
    .color("darkred")

// Dub delay stab - signature dub element
$stab: note("[c3,d#3,g3]")
    .s("square")
    .lpf(sine.range(1200, 3000).slow(slider(4.0, 1, 16)))
    .struct("~ ~ x ~ ~ ~ ~ ~")
    .decay(slider(0.12, 0.04, 0.25))
    .delay(slider(0.4, 0, 0.8))
    .delaytime(0.375)  // Triplet reggae delay
    .room(slider(0.4, 0, 0.9))
    .gain(slider(0.48, 0, 2))
    .sometimes(x => x.struct("~ x ~ ~ ~ ~ x ~"))  // Skank pattern
    .rarely(x => x.note("[d3,f3,a3]"))  // Chord variation
    .color("cyan")
    ._punchcard()

// OFFBEAT SKANK - steppers signature
$skank: note("[c4,d#4,g4]")
    .s("square")
    .lpf(sine.range(2000, 4500).slow(slider(4.0, 1, 16)))
    .struct("~ x ~ x")
    .decay(slider(0.1, 0.03, 0.2))
    .gain(slider(0.45, 0, 1.5))
    .sometimes(x => x.note("[d4,f4,a4]"))  // Chord variation
    .rarely(x => x.struct("[~ x] x [~ x] x"))  // Syncopation
    .color("yellow")

// Atmospheric pad
$pad: note("[c3,g3,c4]")
    .s("sawtooth")
    .lpf(sine.range(400, 1200).slow(16))
    .attack(0.7)
    .release(0.9)
    .room(0.55)
    .gain(slider(0.22, 0, 0.7))
    .slow(8)
    .color("purple")
    .scope({ size: 256 })

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.45)
    .room(0.5)
    .delay(0.2)
    .slow(2)
