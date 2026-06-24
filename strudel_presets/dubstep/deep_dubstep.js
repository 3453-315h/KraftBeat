// @name Deep Dubstep
// @genre Dubstep
// @bpm 140
// @tags deep, sub, dark, uk

setcpm(140 / 4)

// ═══════════════════════════════════════════════════════════════
// DEEP DUBSTEP - Dark minimal vibes with deep sub bass
// ═══════════════════════════════════════════════════════════════

// Sparse half-time kick with weight
$kick: s("bd ~ ~ ~ ~ ~ ~ ~ bd ~ ~ ~ ~ ~ ~ ~").bank("RolandTR808")
    .gain("<1.1 1.05 1.08 1.02> <1.05 1.02 1.1 1.05>")  // Subtle dynamics
    .shape(slider(0.28, 0, 0.55))
    .lpf(300)  // Warm kick
    .every(16, x => x.s("bd ~ ~ ~ ~ ~ bd ~ bd ~ ~ ~ ~ ~ ~ ~"))  // Variation
    .color("orange")
    ._punchcard()

// Sparse snare with big reverb
$snare: stack(
    s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ sd ~ ~ ~").gain(slider(0.92, 0, 2)).room(slider(0.4, 0, 0.9)),  // Big reverb
    s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ [sd:3 ~] ~ ~").gain(0.22).lpf(4000)  // Ghost
).bank("RolandTR808")
    .every(16, x => x.s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ sd ~ [sd sd] ~"))  // Sparse fill
    ._punchcard()

// Minimal offbeat hats
$hat: s("[~ hh] [~ hh] [~ hh] [hh ~]").bank("RolandTR808")
    .gain(perlin.range(0.28, 0.42))  // Soft humanized
    .lpf(perlin.range(4000, 8000))  // Muted
    .pan(perlin.range(-0.2, 0.2).slow(0.5))
    .sometimes(x => x.s("[hh ~] [~ hh] [hh ~] [~ hh]"))  // Variation
    .every(8, x => x.s("[hh hh] [~ hh] [hh hh hh hh] [oh hh]"))  // Fill
    ._punchcard()

// DEEP SUB BASS - the foundation
$sub: note("<c1 ~ ~ ~ ~ ~ [c1 ~] ~ d#1 ~ ~ ~ ~ ~ [d#1 c1] ~>")
    .s("sine")
    .lpf(slider(100, 40, 150))  // Deep sub focus
    .decay(slider(0.25, 0.1, 0.5))
    .gain(slider(0.75, 0, 2))
    .rarely(x => x.note("<c1 ~ ~ d1 ~ ~ [d#1 ~] ~ f1 ~ ~ ~ ~ ~ [d#1 c1] ~>"))  // Variation
    .scope({ size: 256 })
    .color("cyan")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Mid layer for presence
$mid: note("<c2 ~ ~ ~ ~ ~ ~ ~ d#2 ~ ~ ~ ~ ~ ~ ~>")
    .s("sine")
    .lpf(sine.range(300, 800).slow(8))
    .decay(0.18)
    .gain(slider(0.35, 0, 1.2))
    .slow(2)
    .color("orange")

// Dark pad with atmosphere
$pad: note("[c3,d#3,g3]")
    .s("sawtooth")
    .lpf(sine.range(300, 1000).slow(slider(8.0, 1, 16)))
    .attack(slider(0.7, 0.3, 1.3))
    .release(slider(0.8, 0.35, 1.5))
    .room(slider(0.55, 0, 1))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.42, 0, 1.5))
    .sometimes(x => x.note("[d3,f3,a3]"))  // Chord variation
    .color("purple")
    .scope({ size: 256 })

// Dub delay stab - UK dubstep character
$stab: note("[c3,d#3,g3]")
    .s("square")
    .struct("~ ~ ~ ~ ~ ~ ~ ~ x ~ ~ ~ ~ ~ ~ ~")
    .lpf(sine.range(1000, 2500).slow(8))
    .decay(slider(0.12, 0.04, 0.25))
    .delay(slider(0.4, 0, 0.8))
    .delaytime(0.375)  // Triplet dub delay
    .room(slider(0.45, 0, 1))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.45, 0, 1.8))
    .sometimes(x => x.struct("~ ~ ~ ~ ~ ~ ~ ~ ~ x ~ ~ ~ ~ ~ ~"))  // Shift
    .color("orange")

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR808")
    .gain(0.4)
    .room(0.55)
    .delay(0.2)
    .slow(2)
