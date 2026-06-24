// @name Soul Groove
// @genre Classic
// @bpm 95
// @tags soul, motown, groove, rhodes

setcpm(95 / 4)

// ═══════════════════════════════════════════════════════════════
// SOUL GROOVE - Motown-inspired with horns and Rhodes
// ═══════════════════════════════════════════════════════════════

// Punchy kick with syncopation
$kick: s("bd ~ [~ bd] ~").bank("RolandTR808")
    .gain("<0.9 0.85 0.88 0.82>")  // Dynamics
    .shape(slider(0.25, 0, 0.55))
    .nudge("<0 0 0.015 0>")  // Swing
    .every(4, x => x.s("[bd ~] ~ [bd ~] [~ bd]"))  // Variation
    .every(8, x => x.s("bd ~ [bd bd] ~ [~ bd] ~ bd [bd bd]"))  // Fill
    .color("orange")
    ._punchcard()

// Snare on 2 and 4 with ghost layers
$snare: stack(
    s("~ sd ~ sd").gain(slider(0.82, 0, 2)).room(0.3),
    s("~ ~ [sd:3 ~] [~ sd:3]").gain(0.25).lpf(4500)  // Ghosts
).bank("RolandTR808")
    .nudge("0 0.012 0 0.015")  // Swing
    .every(4, x => x.s("~ sd ~ [sd sd]"))  // Roll
    .every(8, x => x.s("~ sd ~ [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Sixteenth hats with velocity
$hat: s("hh*8").bank("RolandTR808")
    .gain(perlin.range(0.3, 0.42))  // Humanized
    .pan(perlin.range(-0.1, 0.1).slow(0.5))
    .sometimes(x => x.s("[hh hh oh hh] [hh hh hh hh] [hh hh oh hh] [hh hh hh oh]"))
    .color("white")
    ._punchcard()

// Tambourine - essential soul groove
$tamb: s("[~ tamb] [tamb ~] [~ tamb] [tamb tamb]")
    .gain(perlin.range(0.42, 0.58))  // Velocity
    .pan(slider(0.3, 0.1, 0.5))
    .sometimes(x => x.s("[tamb ~] [~ tamb] [tamb ~] [~ tamb]"))  // Variation
    .color("yellow")
    .scope({ size: 256 })

// Motown bass - melodic and syncopated
$bass: note("<c2 ~ [c2 d2] ~ e2 ~ [d2 c2] ~>")
    .s("sawtooth")
    .lpf(sine.range(350, 800).slow(slider(8, 4, 16)))
    .decay(slider(0.12, 0.05, 0.25))
    .gain(slider(0.78, 0, 2))
    .nudge(perlin.range(-0.01, 0.02))  // Swing
    .rarely(x => x.note("<c2 [c2 d2] e2 [d2 e2] g2 [f2 e2] [d2 c2] ~>"))  // Walking
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ c1 ~ e1 ~ d1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.42, 0, 1.1))
    .color("darkred")

// Soul horns - stabs with variations
$horns: note("<[c4,e4,g4] ~ ~ ~ [f4,a4,c5] ~ [g4,b4,d5] ~>")
    .s("sawtooth")
    .lpf(slider(3500, 1800, 5500))
    .attack(slider(0.03, 0.01, 0.1))
    .decay(slider(0.22, 0.1, 0.42))
    .room(slider(0.28, 0, 0.7))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.note("<[d4,f4,a4] ~ [e4,g4,b4] ~>"))  // Variation
    .rarely(x => x.fast(2).gain(0.45))  // Double stab
    .color("orange")
    ._punchcard()

// Rhodes - soulful chords with euclidean
$rhodes: note("<c4 e4 g4 c5>")
    .s("sine")
    .lpf(sine.range(2000, 4500).slow(slider(8, 4, 16)))
    .decay(0.18)
    .struct("x(5,8)")  // Euclidean comping
    .room(slider(0.32, 0, 0.85))
    .gain(slider(0.52, 0, 2))
    .sometimes(x => x.note("<c4 f4 a4 c5>"))  // IV chord
    .color("cyan")
    ._punchcard()

// Rhodes second layer
$rhodes2: note("<[e4,g4] ~ [f4,a4] ~ [g4,b4] ~ [e4,g4] ~>")
    .s("sine")
    .lpf(3500)
    .decay(0.15)
    .room(0.3)
    .gain(slider(0.28, 0, 1))
    .color("yellow")

// String swell for emotion
$strings: note("[c3,e3,g3,c4]")
    .s("sawtooth")
    .lpf(sine.range(800, 2000).slow(16))
    .attack(slider(0.5, 0.2, 1.1))
    .release(slider(0.6, 0.25, 1.2))
    .room(0.5)
    .gain(slider(0.28, 0, 1))
    .slow(8)
    .color("purple")
    .scope({ size: 256 })
