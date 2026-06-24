// @name Garage UK
// @genre House
// @bpm 130
// @tags 2step, skippy, bass, uk

setcpm(130 / 4)

// ═══════════════════════════════════════════════════════════════
// UK GARAGE - Skippy 2-step patterns, octave bass jumps
// ═══════════════════════════════════════════════════════════════

// UK Garage 2-step kick with variations
$kick: s("bd ~ [~ bd] ~").bank("RolandTR909")
    .gain("<1.0 0.95 1.02 0.95> <0.98 0.95 1.0 0.95>")  // Dynamics
    .shape(slider(0.3, 0, 1))
    .sometimes(x => x.s("[bd ~] ~ [~ bd] ~"))  // Pattern shift
    .every(8, x => x.s("bd ~ [bd bd] ~ [~ bd] ~ [bd ~] ~"))  // 8-bar variation
    .color("orange")
    ._punchcard()

// 2-step hat pattern with skippy feel
$hat: s("[hh ~] hh [~ hh] hh").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.5))  // Humanized velocity
    .pan(perlin.range(-0.15, 0.15).slow(0.25))
    .nudge(perlin.range(-0.01, 0.015))  // Micro-timing for swing
    .sometimes(x => x.s("[hh hh] ~ [~ hh] [hh ~]"))  // Pattern variation
    .every(8, x => x.s("[hh hh] [~ oh] [hh ~] [hh hh]"))  // Fill
    ._punchcard()

// Snare with ghost layers
$snare: stack(
    s("~ sd ~ sd").gain(slider(0.85, 0, 2)).room(0.3),
    s("~ ~ [sd:3 ~] ~").gain(0.22).lpf(4500)  // Ghost snare
).bank("RolandTR909")
    .every(8, x => x.s("~ sd ~ [sd sd sd sd]"))  // 8-bar fill
    .color("white")
    ._punchcard()

// Skippy shaker with 2-step feel
$shaker: s("[~ shaker] shaker [shaker ~] shaker")
    .gain(perlin.range(0.25, 0.38))  // Humanized
    .pan(perlin.range(-0.3, 0.3).slow(0.25))
    .sometimes(x => x.s("[shaker ~] [~ shaker] [shaker shaker] ~"))  // Variation
    .color("gray")

// Garage bass with octave jumps - signature sound
$bass: note("<c2 ~ [c2 c3] ~ g2 ~ [f2 f3] ~>")
    .s("sawtooth")
    .lpf(sine.range(300, 900).slow(slider(4.0, 1, 16)))
    .decay(slider(0.12, 0.04, 0.25))
    .gain(slider(0.8, 0, 2))
    .rarely(x => x.note("<c2 c3 [c2 d2] c3 g2 g3 [f2 g2] f3>"))  // More octave movement
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ c1 ~ g1 ~ f1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.4, 0, 1.2))
    .color("darkred")

// Organ stabs with movement
$organ: note("<[c4,e4,g4] ~ ~ ~ [f4,a4,c5] ~ [g4,b4,d5] ~>")
    .s("triangle")  // Organ-like
    .lpf(sine.range(2500, 5000).slow(slider(4.0, 1, 16)))
    .attack(0.02)
    .decay(0.25)
    .room(slider(0.3, 0, 1))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.note("<[d4,f4,a4] ~ ~ ~>"))  // Chord variation
    .rarely(x => x.fast(2).gain(0.45))  // Double stab
    .color("cyan")
    ._punchcard()

// Pad layer for warmth
$pad: note("<[c3,e3,g3] [c3,e3,g3] [f3,a3,c4] [g3,b3,d4]>")
    .s("sine")
    .lpf(1500)
    .attack(0.3)
    .release(0.5)
    .room(0.4)
    .gain(slider(0.2, 0, 0.8))
    .slow(4)
    .color("purple")

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.4)
    .room(0.35)
    .slow(2)
