// @name Greek Bouzouki
// @genre World
// @bpm 95
// @tags greek, bouzouki, rebetiko, zembekiko

setcpm(95 / 4)

// ═══════════════════════════════════════════════════════════════
// GREEK BOUZOUKI - Zembekiko 9/8 rhythm with Greek minor scale
// ═══════════════════════════════════════════════════════════════

// Daouli (big drum) - zembekiko 9/8 rhythm with dynamics
$daouli: s("[bd ~ ~] [bd ~ ~] [bd ~ ~]").bank("RolandTR808")
    .gain("<0.88 0.95 0.92 0.98>")  // 9/8 accent
    .shape(slider(0.22, 0, 0.55))
    .room(slider(0.22, 0, 0.65))
    .nudge(perlin.range(-0.01, 0.015))  // Humanized
    .sometimes(x => x.s("[bd bd ~] [bd ~ ~] [bd ~ bd]"))  // Variation
    .every(8, x => x.s("[bd ~ bd] [bd bd ~] [bd ~ bd]"))  // Fill
    .color("orange")
    ._punchcard()

// Toumbi - small drum accents
$toumbi: s("[~ rim rim] [~ rim rim] [~ rim rim]").bank("RolandTR808")
    .gain(perlin.range(0.48, 0.62))  // Velocity variation
    .sometimes(x => x.s("[rim ~ rim] [~ rim ~] [rim rim ~]"))  // Variation
    .every(8, x => x.s("[rim rim rim] [rim ~ rim] [rim rim rim]"))  // Fill
    .color("white")
    ._punchcard()

// Finger cymbals - zilia
$zilia: s("[~ ~ oh] [~ ~ ~] [~ ~ oh]").bank("RolandTR808")
    .gain(perlin.range(0.3, 0.42))
    .sometimes(x => x.s("[oh ~ ~] [~ ~ oh] [~ ~ ~]"))  // Variation
    ._punchcard()

// Bouzouki - Greek minor scale (D E F G A Bb C# D) with ornamentation
$bouzouki: note("<d4 e4 f4 g4 a4 bb4 c#5 d5 c#5 bb4 a4 g4 f4 e4 d4 ~>")
    .s("triangle")  // Bouzouki-like
    .lpf(slider(5000, 2000, 7500))
    .decay(slider(0.32, 0.12, 0.55))
    .struct("x(9,16)")  // 9/8 feel
    .room(slider(0.22, 0, 0.65))
    .gain(slider(0.58, 0, 2))
    .sometimes(x => x.note("<a4 bb4 c#5 d5 c#5 bb4 a4 g4>"))  // Upper variation
    .rarely(x => x.fast(1.5))  // Ornamentation
    .color("cyan")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Second bouzouki - tremolo style
$trem: note("<a4 ~ a4 ~ bb4 ~ a4 ~ g4 ~ f4 ~ e4 ~ d4 ~>")
    .s("triangle")
    .lpf(slider(4000, 1500, 7000))
    .decay(slider(0.12, 0.05, 0.25))
    .struct("x*8")  // Fast tremolo
    .slow(slider(2, 1, 4))
    .pan(slider(-0.35, -0.5, -0.15))
    .gain(slider(0.42, 0, 1.5))
    .sometimes(x => x.note("<d4 e4 f4 g4 a4 bb4 c#5 d5>"))  // Ascending
    .color("lime")
    ._punchcard()

// Kanonaki (santouri) - zither-like with delay
$kanonaki: note("<d5 ~ f5 ~ a5 ~ g5 ~ f5 ~ e5 ~ d5 ~ ~ ~>")
    .s("triangle")
    .lpf(slider(6000, 2800, 9500))
    .attack(slider(0.02, 0.01, 0.08))
    .decay(slider(0.42, 0.15, 0.75))
    .delay(0.15)
    .delaytime(0.25)
    .slow(slider(4, 2, 8))
    .room(slider(0.28, 0, 0.7))
    .gain(slider(0.48, 0, 2))
    .sometimes(x => x.note("<a5 g5 f5 e5 d5 c#5 d5>"))  // Descending
    .color("yellow")
    ._punchcard()

// Bass - minor mode with movement
$bass: note("<d2 ~ d2 ~ g2 ~ a2 ~ d2 ~ ~ ~>")
    .s("sawtooth")
    .lpf(slider(500, 180, 900))
    .decay(slider(0.2, 0.08, 0.4))
    .gain(slider(0.75, 0, 2))
    .rarely(x => x.note("<d2 e2 f2 d2 g2 a2 bb2 a2 d2>"))  // Walking
    .scope({ size: 256 })
    .color("red")

// Sub layer
$sub: note("<d1 ~ d1 ~ g1 ~ a1 ~ d1 ~ ~ ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.45, 0, 1.2))
    .color("darkred")
