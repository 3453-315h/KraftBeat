// @name Blues Shuffle
// @genre Classic
// @bpm 100
// @tags blues, shuffle, guitar, 12bar

setcpm(100 / 4)

// ═══════════════════════════════════════════════════════════════
// BLUES SHUFFLE - 12-bar blues with shuffled triplet feel
// ═══════════════════════════════════════════════════════════════

// Shuffle kick with swing feel
$kick: s("bd ~ bd ~").bank("RolandTR808")
    .gain("<0.9 0.85 0.88 0.82>")  // Dynamics
    .shape(slider(0.22, 0, 0.5))
    .nudge("<0 0 0.02 0>")  // Shuffle
    .every(8, x => x.s("bd ~ bd [~ bd]"))  // Variation
    .color("orange")
    ._punchcard()

// Shuffled hats with triplet feel
$hat: s("[hh ~] hh [hh ~] hh").bank("RolandTR808")
    .gain(perlin.range(0.35, 0.5))  // Humanized
    .nudge(perlin.range(-0.01, 0.025))  // Shuffle timing
    .pan(perlin.range(-0.12, 0.12).slow(0.5))
    .sometimes(x => x.s("[~ hh] hh [hh ~] [hh hh]"))  // Variation
    .every(8, x => x.s("[hh hh] [~ hh] [hh hh hh hh] [oh hh]"))  // Fill
    .color("white")
    ._punchcard()

// Snare on 2 and 4 with ghost
$snare: stack(
    s("~ sd ~ sd").gain(slider(0.78, 0, 2)).room(0.3),
    s("~ ~ [sd:3 ~] ~").gain(0.22).lpf(4000)  // Ghost
).bank("RolandTR808")
    .nudge("0 0.015 0 0.02")  // Shuffle
    .every(8, x => x.s("~ sd ~ [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Blues shuffle bass (12-bar I-IV-V pattern)
$bass: note("<c2 c2 f2 c2 g2 f2 c2 g2>")
    .s("sawtooth")
    .lpf(sine.range(350, 750).slow(slider(8, 4, 16)))
    .decay(slider(0.15, 0.06, 0.3))
    .gain(slider(0.78, 0, 2))
    .nudge(perlin.range(-0.01, 0.02))  // Shuffle
    .rarely(x => x.note("<c2 [c2 d2] f2 [e2 f2] g2 [g2 f2] c2 [b1 c2]>"))  // Walking
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ f1 c1 g1 f1 c1 g1>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.42, 0, 1.1))
    .color("darkred")

// Blues guitar lick (C blues pentatonic)
$guitar: note("<c4 d#4 f4 g4 a#4 g4 f4 d#4 c4 ~ ~ ~ ~ ~ ~ ~>")
    .s("triangle")  // Guitar-like
    .lpf(slider(3500, 1500, 6000))
    .decay(slider(0.18, 0.08, 0.35))
    .room(slider(0.25, 0, 0.7))
    .delay(0.1)
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.note("<g4 a#4 c5 a#4 g4 f4 d#4 c4>"))  // High variation
    .rarely(x => x.fast(1.5))  // Fast lick
    .color("cyan")
    ._punchcard()

// Turnaround lick
$turn: note("<~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ g4 a4 a#4 b4>")
    .s("triangle")
    .lpf(4000)
    .decay(0.15)
    .gain(slider(0.42, 0, 1.5))
    .slow(4)
    .color("lime")

// Piano comp - blues voicings
$piano: note("<[c3,e3,g3] ~ [c3,e3,g3] ~>")
    .s("triangle")
    .lpf(sine.range(1800, 4000).slow(8))
    .decay(0.2)
    .room(slider(0.28, 0, 0.75))
    .gain(slider(0.52, 0, 2))
    .sometimes(x => x.note("<[f3,a3,c4] ~ [g3,b3,d4] ~>"))  // IV-V voicings
    .color("yellow")
    ._punchcard()

// Harmonica accent
$harp: note("<~ ~ c5 ~ ~ ~ d#5 ~ ~ ~ ~ ~ ~ ~ ~ ~>")
    .s("sawtooth")
    .lpf(3500)
    .attack(0.05)
    .decay(0.3)
    .gain(slider(0.32, 0, 1.2))
    .slow(4)
    .color("purple")
