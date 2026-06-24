// @name Study Beats
// @genre Lo-Fi
// @bpm 75
// @tags study, focus, calm, concentration

setcpm(75 / 4)

// ═══════════════════════════════════════════════════════════════
// STUDY BEATS - Calm lo-fi for focused concentration
// ═══════════════════════════════════════════════════════════════

// Soft dusty kick with swing
$kick: s("bd ~ [~ bd] ~").bank("SP1200")
    .gain("<0.85 0.8 0.82 0.78>")  // Soft dynamics
    .lpf(280)  // Lo-fi roll-off
    .nudge("<0 0 0.025 0>")  // Gentle swing
    .every(8, x => x.s("bd ~ [bd ~] ~ [~ bd] ~ bd ~"))  // Variation
    .color("orange")
    ._punchcard()

// Soft snare with room
$snare: stack(
    s("~ sd ~ sd").gain(slider(0.65, 0, 2)).room(0.45).lpf(4000),
    s("~ ~ [sd:3 ~] [~ sd:3]").gain(0.18).lpf(3200)  // Soft ghosts
).bank("SP1200")
    .nudge("0 0.012 0 0.018")  // Swing
    .every(8, x => x.s("~ sd ~ [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Sparse hats with filter
$hat: s("[~ hh] ~ [~ hh] [hh ~]").bank("SP1200")
    .gain(perlin.range(0.25, 0.38))  // Soft humanized
    .lpf(perlin.range(3000, 6000))  // Lo-fi filter
    .nudge(perlin.range(-0.015, 0.03))  // Swing
    .pan(perlin.range(-0.12, 0.12).slow(0.5))
    .sometimes(x => x.s("[hh ~] ~ [~ hh] [~ hh]"))  // Variation
    .color("white")
    ._punchcard()

// Vinyl crackle - essential lo-fi texture
$vinyl: s("[rim:5 rim:5 rim:5 rim:5]*4")
    .gain(slider(0.15, 0, 0.45))
    .lpf(2800)
    .hpf(450)
    .color("brown")

// Mellow Rhodes chords with warmth
$rhodes: note("<[c4,e4,g4] [c4,e4,g4] [a3,c4,e4] [g3,b3,d4]>")
    .s("sine")
    .lpf(sine.range(1600, 3500).slow(slider(8, 4, 16)))
    .decay(0.22)
    .room(slider(0.38, 0, 0.9))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.52, 0, 2))
    .sometimes(x => x.note("<[d4,f4,a4] [e4,g4,b4]>"))  // Chord variation
    .color("cyan")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Second Rhodes layer for depth
$rhodes2: note("<[g3,b3] ~ [a3,c4] ~ [b3,d4] ~ [g3,b3] ~>")
    .s("triangle")
    .lpf(2000)
    .decay(0.18)
    .delay(0.1)
    .room(0.32)
    .gain(slider(0.25, 0, 0.9))
    .slow(slider(4.0, 1, 16))
    .color("yellow")

// Simple warm bass
$bass: note("<c2 ~ c2 ~ a1 ~ g1 ~>")
    .s("triangle")
    .lpf(sine.range(240, 480).slow(slider(8, 4, 16)))
    .decay(slider(0.18, 0.08, 0.32))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.68, 0, 2))
    .rarely(x => x.note("<c2 d2 [e2 d2] c2>"))  // Walking variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ c1 ~ a0 ~ g0 ~>")
    .s("sine")
    .lpf(75)
    .gain(slider(0.38, 0, 1.1))
    .color("darkred")

// Rain-like ambient texture
$rain: s("[rim:5 rim:5]*8")
    .gain(perlin.range(0.08, 0.18))
    .lpf(perlin.range(1500, 4000))
    .hpf(800)
    .pan(perlin.range(-0.5, 0.5))
    .room(0.4)
    .color("gray")

// Ambient haze for depth
$haze: note("[c3,g3]")
    .s("sawtooth")
    .lpf(sine.range(320, 850).slow(32))
    .attack(1.2)
    .release(1)
    .room(0.55)
    .gain(slider(0.12, 0, 0.45))
    .slow(8)
    .color("purple")
    .scope({ size: 256 })
