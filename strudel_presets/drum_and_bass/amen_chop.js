// @name Amen Chop
// @genre Drum and Bass
// @bpm 174
// @tags break, jungle, chopped, amen

setcpm(174 / 4)

// ═══════════════════════════════════════════════════════════════
// AMEN CHOP - Classic jungle break programming
// ═══════════════════════════════════════════════════════════════

// Classic 2-step DnB kick pattern with dynamics
$kick: s("[bd ~ ~ bd] [~ ~ bd ~] [bd ~ ~ ~] [~ bd ~ bd]").bank("RolandTR909")
    .gain("<1.08 1.02 1.05 1> <1.02 1.05 1.08 [1.1 1.05]>")  // Dynamics
    .shape(slider(0.25, 0, 0.5))
    .every(8, x => x.s("[bd ~ ~ bd] [~ bd bd ~] [bd ~ bd ~] [~ bd ~ bd]"))  // Variation
    .color("orange")
    ._punchcard()

// Snare pattern with ghost rushes
$snare: stack(
    s("~ ~ sd ~ ~ ~ sd ~").gain(slider(0.95, 0, 2)).room(0.25),
    s("~ ~ ~ [sd:3 ~] ~ ~ ~ [sd:3 sd:3]").gain(0.32).lpf(5000)  // Ghost snare rush
).bank("RolandTR909")
    .every(4, x => x.s("~ ~ sd ~ ~ [sd sd] sd ~"))  // 4-bar fill
    .every(8, x => x.s("~ ~ sd ~ ~ ~ sd [sd sd sd sd]"))  // 8-bar fill
    .color("white")
    ._punchcard()

// Ride cymbal - essential DnB
$ride: s("rd*8").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.52))  // Humanized
    .pan(perlin.range(-0.15, 0.15).slow(0.25))
    .sometimes(x => x.s("[rd rd rd rd] [rd rd oh rd]"))  // Open hat accent
    .every(8, x => x.fast(2).gain(0.45))  // Double-time energy
    .color("white")
    ._punchcard()

// Closed hat texture
$hat: s("[hh hh hh hh] [hh hh [hh hh hh] hh]").bank("RolandTR909")
    .gain(perlin.range(0.28, 0.42))  // Subtle
    .lpf(perlin.range(6000, 10000))
    .sometimes(x => x.fast(1.5))  // Triplet feel
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh*16]"))  // Hat roll
    ._punchcard()

// Reese bass with movement
$bass: note("<c2 c2 [c2 eb2] c2> <c2 g1 [f1 g1] c2>")
    .s("sawtooth")
    .lpf(sine.range(250, 900).fast(slider(2, 1, 8)))
    .lpq(sine.range(2, 8).slow(4))  // Resonance movement
    .decay(slider(0.15, 0.05, 0.3))
    .gain(slider(0.82, 0, 2))
    .rarely(x => x.note("<c2 eb2 [f2 g2] c2>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Sub bass layer
$sub: note("<c1 ~ ~ ~ ~ g0 ~ ~> <~ ~ ~ ~ c1 ~ ~ ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.55, 0, 1.5))
    .color("darkred")

// Jungle stab
$stab: note("<[c4,eb4,g4] ~ ~ ~> <~ ~ [g3,bb3,d4] ~>")
    .s("square")
    .lpf(sine.range(2000, 5000).slow(4))
    .decay(slider(0.12, 0.04, 0.25))
    .delay(slider(0.2, 0, 0.5))
    .delaytime(0.25)
    .room(slider(0.3, 0, 0.7))
    .gain(slider(0.48, 0, 2))
    .fast(slider(2, 1, 8))
    .sometimes(x => x.fast(2).gain(0.4))  // Double stab
    .color("cyan")
    ._punchcard()

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.5)
    .room(0.4)
    .slow(2)
