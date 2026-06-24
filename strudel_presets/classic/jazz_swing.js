// @name Jazz Swing
// @genre Classic
// @bpm 130
// @tags swing, jazzy, brushes, ii-V-I

setcpm(130 / 4)

// ═══════════════════════════════════════════════════════════════
// JAZZ SWING - Classic swing rhythm with ii-V-I progression
// ═══════════════════════════════════════════════════════════════

// Swing ride pattern with triplet feel
$ride: s("ride:0 [ride:1 ride:0] ride:0 [ride:1 ride:0]")
    .gain(perlin.range(0.65, 0.88))  // Velocity variation
    .pan(slider(0.5, 0.3, 0.7))
    .nudge(perlin.range(-0.01, 0.025))  // Swing timing
    .sometimes(x => x.s("ride:0 [~ ride:0] ride:0 [ride:1 ride:0]"))  // Variation
    .every(8, x => x.fast(1.5).gain(0.75))  // Triplet energy
    .color("gold")
    ._punchcard()

// Subtle kick with swing feel
$kick: s("bd ~ ~ ~ [bd ~] ~ ~ ~").bank("RolandTR808")
    .gain("<0.75 0.82 0.78 0.85>")  // Dynamics
    .shape(slider(0.22, 0, 0.5))
    .nudge("<0 0 0.02 0>")  // Swing
    .every(8, x => x.s("bd ~ bd ~ [bd ~] ~ ~ [~ bd]"))  // Variation
    .color("orange")
    ._punchcard()

// Brush snare with ghost notes
$snare: stack(
    s("~ ~ sd ~ ~ ~ sd ~").gain(slider(0.75, 0, 2)).room(0.35),
    s("~ [sd:3 ~] ~ ~ ~ [sd:3 ~] ~ [~ sd:3]").gain(0.3).lpf(4500)  // Brush ghosts
).bank("RolandTR808")
    .nudge("0 0.015 0 0.02")  // Swing
    .every(8, x => x.s("~ ~ sd ~ ~ ~ sd [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Hi-hat texture
$hat: s("~ [~ hh] ~ [hh ~]").bank("RolandTR808")
    .gain(perlin.range(0.28, 0.42))
    .sometimes(x => x.s("[hh ~] [~ hh] [~ hh] [hh ~]"))
    .color("gray")
    ._punchcard()

// Walking bass - jazzy chromatic movement
$bass: note("<c2 e2 g2 a2 b2 a2 g2 e2>")
    .s("sawtooth")
    .lpf(sine.range(350, 800).slow(slider(8, 4, 16)))
    .decay(slider(0.15, 0.06, 0.3))
    .gain(slider(0.78, 0, 2))
    .nudge(perlin.range(-0.01, 0.02))  // Swing
    .rarely(x => x.note("<c2 d2 e2 f2 g2 a2 b2 c3>"))  // Ascending walk
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ ~ ~ ~ ~ g0 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.4, 0, 1.1))
    .color("darkred")

// Jazz voicings - ii-V-I progression (Dm7 - G7 - Cmaj7)
$keys: note("<[d4,f4,a4,c5] [g4,b4,d5,f5] [c4,e4,g4,b4] [c4,e4,g4,b4]>")
    .s("triangle")  // Piano-like
    .lpf(sine.range(2500, 5500).slow(8))
    .decay(0.25)
    .room(slider(0.35, 0, 0.9))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.note("<[e4,g4,b4,d5] [a4,c5,e5,g5] [d4,f4,a4,c5]>"))  // iii-VI-ii
    .color("cyan")
    ._punchcard()

// Comping variation layer
$comp: note("<~ ~ [f4,a4,c5] ~ ~ [g4,b4,d5] ~ ~>")
    .s("sine")
    .lpf(3500)
    .decay(0.15)
    .room(0.3)
    .gain(slider(0.28, 0, 1))
    .slow(slider(4.0, 1, 16))
    .color("yellow")

// Optional horn lead
$horn: note("<~ ~ ~ ~ g5 ~ a5 ~ b5 ~ a5 ~ g5 ~ ~ ~>")
    .s("sawtooth")
    .lpf(slider(3500, 1500, 6000))
    .attack(0.05)
    .decay(0.3)
    .gain(slider(0.35, 0, 1.5))
    .slow(4)
    .sometimes(x => x.note("<c5 d5 e5 f5 g5 a5 b5 c6>"))  // Scale run
    .color("purple")
    .pianoroll({ fold: 1 })
