// @name Gamelan
// @genre World
// @bpm 80
// @tags gamelan, balinese, gongs, metallophone, pelog

setcpm(80 / 4)

// ═══════════════════════════════════════════════════════════════
// GAMELAN - Balinese interlocking metallophone patterns
// ═══════════════════════════════════════════════════════════════

// Gong ageng - large gong marks the cycle
$gong: s("[~ ~ ~ ~] [~ ~ ~ ~] [~ ~ ~ ~] [bd ~ ~ ~]").bank("RolandTR808")
    .gain(slider(0.92, 0, 2))
    .decay(slider(1.2, 0.6, 2.2))
    .room(slider(0.55, 0, 1))
    .slow(slider(2, 1, 4))
    .color("yellow")
    ._punchcard()

// Kendhang (drums) - rhythmic guide with dynamics
$kendhang: s("[bd ~ rim ~] [~ rim ~ rim] [bd ~ ~ rim] [~ rim bd ~]").bank("RolandTR808")
    .gain("<0.65 0.72 0.68 0.75> <0.7 0.68 0.72 0.7>")  // Dynamics
    .room(slider(0.2, 0, 0.6))
    .nudge(perlin.range(-0.01, 0.015))  // Humanized
    .sometimes(x => x.s("[bd rim ~ ~] [~ rim bd rim] [bd ~ rim ~] [rim ~ bd ~]"))
    .color("orange")
    ._punchcard()

// Kempul (medium gong) - punctuation with variation
$kempul: s("~ ~ ~ ~ ~ ~ bd ~ ~ ~ ~ ~ ~ ~ ~ ~").bank("RolandTR808")
    .gain(slider(0.78, 0, 2))
    .decay(slider(0.85, 0.4, 1.4))
    .room(slider(0.42, 0, 0.9))
    .sometimes(x => x.s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ bd ~ ~ ~"))  // Shift
    .color("yellow")
    ._punchcard()

// Saron (metallophone) - Pelog scale (C Db E F G Ab B) with interlocking
$saron: note("<c5 db5 e5 f5 g5 f5 e5 db5 c5 ~ ~ ~ ~ ~ ~ ~>")
    .s("triangle")
    .lpf(slider(5000, 2500, 9000))
    .attack(slider(0.01, 0, 0.04))
    .decay(slider(0.4, 0.15, 0.75))
    .slow(slider(2, 1, 4))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.note("<e5 f5 g5 ab5 g5 f5 e5 db5>"))  // Variation
    .rarely(x => x.fast(1.5))  // Speed variation
    .color("cyan")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Gender (higher metallophone) - interlocking pattern
$gender: note("<e5 ~ g5 ~ ab5 ~ g5 ~ e5 ~ db5 ~ c5 ~ ~ ~>")
    .s("triangle")
    .lpf(slider(6000, 2800, 9500))
    .attack(slider(0.01, 0, 0.04))
    .decay(slider(0.3, 0.12, 0.55))
    .struct("x(7,16)")  // Euclidean interlocking
    .slow(slider(2, 1, 4))
    .pan(slider(0.35, 0.15, 0.55))
    .gain(slider(0.52, 0, 2))
    .sometimes(x => x.struct("x(9,16)"))  // Pattern variation
    .color("lime")
    ._punchcard()

// Suling (bamboo flute) - ornamental melody with breath
$suling: note("<c6 ~ db6 ~ e6 ~ ~ ~ f6 ~ e6 ~ db6 ~ c6 ~>")
    .s("triangle")
    .lpf(slider(8000, 3500, 11000))
    .attack(slider(0.08, 0.03, 0.2))
    .decay(slider(0.6, 0.25, 1))
    .slow(slider(4, 2, 8))
    .room(slider(0.38, 0, 0.85))
    .delay(0.1)
    .gain(slider(0.42, 0, 1.8))
    .sometimes(x => x.note("<e6 f6 g6 f6 e6 db6 c6>"))  // Ornament
    .color("purple")
    .pianoroll({ fold: 1 })
    .scope({ size: 256 })

// Bass bonang - low metallophones with resonance
$bonang: note("<c3 ~ e3 ~ f3 ~ e3 ~ c3 ~ ~ ~ ~ ~ ~ ~>")
    .s("triangle")
    .lpf(slider(2000, 600, 3800))
    .decay(slider(0.55, 0.22, 0.95))
    .slow(slider(2, 1, 4))
    .gain(slider(0.58, 0, 2))
    .rarely(x => x.note("<c3 e3 f3 g3 f3 e3 c3>"))  // Extended
    .color("red")
    .scope({ size: 256 })

// Ambient gong resonance layer
$resonance: note("[c2,g2]")
    .s("sawtooth")
    .lpf(sine.range(200, 500).slow(32))
    .attack(1.5)
    .release(1.5)
    .room(0.6)
    .gain(slider(0.15, 0, 0.5))
    .slow(16)
    .color("magenta")
