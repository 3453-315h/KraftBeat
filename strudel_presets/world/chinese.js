// @name Chinese Traditional
// @genre World
// @bpm 72
// @tags chinese, guzheng, erhu, pentatonic

setcpm(72 / 4)

// ═══════════════════════════════════════════════════════════════
// CHINESE TRADITIONAL - Pentatonic scales with traditional instruments
// ═══════════════════════════════════════════════════════════════

// Tang gu (hall drum) - ceremonial rhythm with dynamics
$drum: s("[bd ~ ~ ~] [~ ~ bd ~] [~ ~ ~ ~] [bd ~ ~ ~]").bank("RolandTR808")
    .gain("<0.78 0.85 0.8 0.88>")  // Dynamics
    .decay(slider(0.45, 0.2, 0.8))
    .room(slider(0.35, 0, 0.85))
    .nudge(perlin.range(-0.01, 0.015))  // Humanized
    .sometimes(x => x.s("[bd ~ bd ~] [~ ~ bd ~] [~ bd ~ ~] [bd ~ ~ ~]"))  // Variation
    .every(8, x => x.s("[bd ~ bd ~] [bd ~ bd ~] [~ bd ~ bd] [bd ~ bd ~]"))  // Fill
    .color("red")
    ._punchcard()

// Muyu (wooden fish) - meditative pulse with variations
$muyu: s("rim*4").bank("RolandTR808")
    .gain(perlin.range(0.35, 0.48))  // Velocity variation
    .pan(slider(0.25, 0, 0.45))
    .sometimes(x => x.s("[rim ~ rim rim] [rim rim ~ rim]"))  // Variation
    .every(8, x => x.s("[rim rim rim rim rim rim rim rim]"))  // Intensify
    .color("orange")
    ._punchcard()

// Luo (gong) - accents with resonance
$gong: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ [bd:0 ~] ~ ~ ~").bank("RolandTR808")
    .gain(slider(0.62, 0, 1.8))
    .decay(slider(0.9, 0.4, 1.5))
    .room(slider(0.55, 0, 1))
    .slow(slider(2, 1, 4))
    .sometimes(x => x.s("~ ~ ~ ~ [bd:0 ~] ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~"))  // Earlier hit
    .color("yellow")
    ._punchcard()

// Guzheng (zither) - Chinese pentatonic (C D E G A) with ornamentation
$guzheng: note("<c5 d5 e5 g5 a5 g5 e5 d5 c5 ~ a4 ~ c5 ~ ~ ~>")
    .s("triangle")  // Guzheng-like
    .lpf(slider(6000, 2800, 9500))
    .decay(slider(0.42, 0.15, 0.75))
    .struct("x(7,16)")  // Euclidean pattern
    .slow(slider(2, 1, 4))
    .room(slider(0.28, 0, 0.7))
    .delay(0.1)
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.note("<a5 g5 e5 d5 c5 d5 e5 g5>"))  // Variation
    .rarely(x => x.fast(1.5))  // Ornamentation
    .color("cyan")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Erhu (bowed string) - expressive melody with vibrato feel
$erhu: note("<e5 ~ g5 ~ a5 ~ g5 ~ ~ e5 d5 ~ c5 ~ ~ ~>")
    .s("sawtooth")
    .lpf(slider(3000, 1500, 5500))
    .attack(slider(0.1, 0.03, 0.25))
    .decay(slider(0.65, 0.3, 1.1))
    .slow(slider(4, 2, 8))
    .room(slider(0.32, 0, 0.8))
    .delay(0.08)
    .gain(slider(0.48, 0, 2))
    .sometimes(x => x.note("<g5 a5 g5 e5 d5 c5 d5 e5>"))  // Variation
    .color("purple")
    .pianoroll({ fold: 1 })
    .scope({ size: 256 })

// Dizi (bamboo flute) - ornamentation with breath
$dizi: note("<c6 ~ d6 ~ e6 ~ ~ ~ g6 ~ e6 ~ d6 ~ c6 ~>")
    .s("triangle")
    .lpf(slider(8000, 4000, 11000))
    .attack(slider(0.03, 0.01, 0.1))
    .decay(slider(0.32, 0.12, 0.55))
    .slow(slider(4, 2, 8))
    .delay(0.12)
    .room(0.35)
    .gain(slider(0.38, 0, 1.5))
    .sometimes(x => x.note("<e6 g6 a6 g6 e6 d6 c6>"))  // High phrase
    .color("lime")
    ._punchcard()

// Bass drone - tonic and fifth with movement
$bass: note("<c2 g2 c2 g2>")
    .s("triangle")
    .lpf(slider(500, 150, 900))
    .attack(0.3)
    .decay(0.8)
    .slow(slider(8, 4, 16))
    .gain(slider(0.52, 0, 1.8))
    .rarely(x => x.note("<c2 d2 g2 c2>"))  // Movement
    .color("red")
    .scope({ size: 256 })

// Sub layer
$sub: note("<c1 ~ c1 ~ g1 ~ c1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.42, 0, 1.2))
    .slow(4)
    .color("darkred")
