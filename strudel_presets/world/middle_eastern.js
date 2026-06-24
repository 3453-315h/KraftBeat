// @name Middle Eastern
// @genre World
// @bpm 95
// @tags arabic, maqam, darbuka, oud, hijaz

setcpm(95 / 4)

// ═══════════════════════════════════════════════════════════════
// MIDDLE EASTERN - Maqam Hijaz with authentic percussion
// ═══════════════════════════════════════════════════════════════

// Darbuka (doumbek) - malfuf rhythm with dynamics
$darbuka: s("[bd ~ ~ rim] [~ rim bd ~] [bd ~ rim ~] [~ rim ~ rim]").bank("RolandTR808")
    .gain("<0.85 0.92 0.88 0.95> <0.9 0.88 0.85 0.92>")  // Dynamics
    .room(slider(0.12, 0, 0.4))
    .nudge(perlin.range(-0.01, 0.015))  // Humanized
    .sometimes(x => x.s("[bd rim ~ rim] [~ rim bd rim] [bd ~ rim ~] [rim ~ ~ rim]"))  // Variation
    .every(8, x => x.s("[bd rim rim ~] [rim bd rim ~] [bd rim bd rim] [rim ~ rim rim]"))  // Fill
    .color("orange")
    ._punchcard()

// Riq (tambourine) - fills and accents
$riq: s("shaker*16")
    .gain(perlin.range(0.28, 0.42))  // Humanized
    .pan(sine.range(-0.35, 0.35).slow(4))
    .euclid(7, 16)  // Rhythmic accent
    .sometimes(x => x.euclid(9, 16))  // Variation
    ._punchcard()

// Sagat (finger cymbals) with variations
$sagat: s("[~ ~ oh ~] [~ ~ ~ ~] [~ ~ oh ~] [~ oh ~ ~]").bank("RolandTR808")
    .gain(perlin.range(0.35, 0.5))
    .sometimes(x => x.s("[oh ~ ~ ~] [~ ~ oh ~] [~ ~ ~ oh] [~ oh ~ ~]"))
    ._punchcard()

// Oud - Maqam Hijaz (D Eb F# G A Bb C D) with ornamentation
$oud: note("<d4 eb4 f#4 g4 a4 bb4 a4 g4 f#4 eb4 d4 ~ ~ ~ ~ ~>")
    .s("triangle")  // Oud-like
    .lpf(slider(4000, 1500, 7000))
    .decay(slider(0.35, 0.15, 0.7))
    .struct("x(9,16)")
    .slow(slider(2, 1, 4))
    .room(slider(0.22, 0, 0.6))
    .gain(slider(0.58, 0, 2))
    .sometimes(x => x.note("<d4 f#4 a4 bb4 a4 f#4 d4>"))  // Condensed
    .rarely(x => x.fast(1.5))  // Faster passage
    .color("yellow")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Qanun (zither) - tremolo ornaments with delay
$qanun: note("<d5 ~ f#5 ~ a5 ~ bb5 ~ a5 ~ f#5 ~ d5 ~ ~ ~>")
    .s("triangle")
    .lpf(slider(6000, 2500, 9000))
    .attack(slider(0.02, 0.01, 0.08))
    .decay(slider(0.2, 0.08, 0.42))
    .delay(0.15)
    .delaytime(0.25)
    .slow(slider(4, 2, 8))
    .room(slider(0.28, 0, 0.7))
    .gain(slider(0.42, 0, 1.8))
    .sometimes(x => x.note("<f#5 a5 bb5 a5 f#5 d5>"))  // Variation
    .color("cyan")
    ._punchcard()

// Bass drone - tonic with movement
$bass: note("<d2 ~ ~ ~ d2 ~ a1 ~ d2 ~ ~ ~ a1 ~ d2 ~>")
    .s("sine")
    .lpf(slider(400, 120, 700))
    .decay(slider(0.3, 0.12, 0.6))
    .gain(slider(0.78, 0, 2))
    .rarely(x => x.note("<d2 eb2 d2 ~ d2 ~ a1 a1 d2 ~ ~ ~ a1 a1 d2 ~>"))  // Walking
    .scope({ size: 256 })
    .color("red")

// Sub layer
$sub: note("<d1 ~ ~ ~ ~ ~ ~ ~ d1 ~ ~ ~ ~ ~ ~ ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.45, 0, 1.2))
    .color("darkred")

// Nay (flute) - expressive Hijaz melody with vibrato feel
$nay: note("<d5 eb5 f#5 g5 ~ a5 bb5 a5 ~ g5 f#5 ~ eb5 ~ d5 ~>")
    .s("triangle")
    .lpf(slider(5000, 2500, 9000))
    .attack(slider(0.08, 0.02, 0.2))
    .decay(slider(0.5, 0.25, 0.9))
    .slow(slider(2, 1, 4))
    .room(slider(0.38, 0, 0.9))
    .delay(0.1)
    .gain(slider(0.48, 0, 2))
    .sometimes(x => x.note("<a5 bb5 a5 g5 f#5 eb5 d5>"))  // Descending
    .color("purple")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Atmospheric drone layer
$drone: note("[d3,a3]")
    .s("sawtooth")
    .lpf(sine.range(300, 700).slow(16))
    .attack(1)
    .release(1)
    .room(0.5)
    .gain(slider(0.18, 0, 0.6))
    .slow(8)
    .color("magenta")
    .scope({ size: 256 })
