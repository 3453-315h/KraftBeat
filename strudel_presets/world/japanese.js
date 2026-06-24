// @name Japanese Koto
// @genre World
// @bpm 60
// @tags japanese, koto, shakuhachi, zen, traditional

setcpm(60 / 4)

// ═══════════════════════════════════════════════════════════════
// JAPANESE KOTO - Miyako-bushi scale with zen aesthetics
// ═══════════════════════════════════════════════════════════════

// Taiko ensemble - powerful don and ka strokes with dynamics
$taiko: s("[bd ~ ~ ~] [~ ~ ~ ~] [bd ~ ~ ~] [~ bd ~ ~]").bank("RolandTR808")
    .gain("<1.15 1.22 1.18 1.25>")  // Power dynamics
    .shape(slider(0.15, 0, 0.45))
    .decay(slider(0.65, 0.35, 1.1))
    .room(slider(0.52, 0, 1))
    .slow(2)
    .sometimes(x => x.s("[bd ~ bd ~] [~ ~ ~ ~] [bd ~ ~ bd] [~ bd ~ ~]"))  // Variation
    .every(8, x => x.s("[bd bd ~ ~] [bd ~ bd ~] [bd ~ ~ bd] [bd bd bd ~]"))  // Energetic fill
    .color("red")
    ._punchcard()

// Shime-daiko - sharp accent patterns with dynamics
$shime: s("~ ~ rim ~ ~ rim ~ ~ ~ ~ rim ~ ~ ~ ~ ~").bank("RolandTR808")
    .gain(perlin.range(0.48, 0.62))  // Velocity variation
    .sometimes(x => x.s("rim ~ ~ rim ~ ~ rim ~ ~ rim ~ ~ ~ ~ ~ ~"))  // Pattern 2
    .every(8, x => x.s("[rim rim] ~ rim ~ ~ rim ~ rim ~ ~ [rim rim] ~ ~ ~ ~ ~"))  // Fill
    .color("orange")
    ._punchcard()

// Kane (small gong) - sparse accents with resonance
$kane: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh ~ ~ ~").bank("RolandTR808")
    .gain(slider(0.48, 0, 1.5))
    .decay(slider(0.85, 0.45, 1.4))
    .room(slider(0.45, 0, 0.95))
    .slow(2)
    .sometimes(x => x.s("~ ~ ~ ~ ~ ~ ~ ~ oh ~ ~ ~ ~ ~ ~ ~"))  // Shift
    .color("yellow")
    ._punchcard()

// Koto - Miyako-bushi scale (D Eb G A Bb) with ornamentation
$koto: note("<d4 ~ eb4 ~ g4 ~ a4 ~ bb4 ~ a4 ~ g4 ~ eb4 d4>")
    .s("triangle")  // Koto-like
    .lpf(slider(5000, 2500, 7500))
    .decay(slider(0.6, 0.35, 0.95))
    .room(slider(0.32, 0, 0.8))
    .gain(slider(0.58, 0, 2))
    .slow(2)
    .sometimes(x => x.note("<a4 bb4 a4 g4 eb4 d4>"))  // Descending
    .rarely(x => x.fast(1.5))  // Faster phrase
    .color("cyan")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Shakuhachi - breathy zen flute with natural phrasing
$shakuhachi: note("<d5 ~ ~ ~ eb5 ~ ~ g5 ~ ~ a5 ~ g5 ~ eb5 ~>")
    .s("triangle")
    .lpf(slider(3500, 1500, 5500))
    .attack(slider(0.22, 0.08, 0.45))
    .decay(slider(0.85, 0.45, 1.4))
    .room(slider(0.48, 0, 0.95))
    .delay(0.12)
    .gain(slider(0.52, 0, 2))
    .slow(4)
    .sometimes(x => x.note("<g5 a5 bb5 a5 g5 eb5 d5>"))  // Phrase variation
    .color("purple")
    .scope({ size: 256 })
    .pianoroll({ fold: 1 })

// Shamisen - rhythmic plucked phrases with variations
$shamisen: note("<d4 d4 ~ g4 ~ a4 g4 ~ d4 ~ ~ ~ ~ ~ ~ ~>")
    .s("triangle")
    .lpf(slider(4500, 1800, 6800))
    .decay(slider(0.18, 0.08, 0.38))
    .gain(slider(0.55, 0, 2))
    .slow(2)
    .sometimes(x => x.note("<d4 ~ g4 a4 ~ g4 ~ d4 eb4 ~ d4 ~>"))  // Variation
    .rarely(x => x.fast(2).gain(0.45))  // Fast strumming
    .color("lime")
    ._punchcard()

// Biwa drone - deep sustained notes
$biwa: note("<d2 a2>")
    .s("sawtooth")
    .lpf(slider(380, 120, 580))
    .attack(slider(0.35, 0.12, 0.75))
    .decay(slider(1.1, 0.55, 1.9))
    .gain(slider(0.52, 0, 1.8))
    .slow(8)
    .color("red")
    .scope({ size: 256 })

// Zen atmosphere layer
$zen: note("[d2,a2]")
    .s("sine")
    .lpf(sine.range(150, 400).slow(32))
    .attack(1.5)
    .release(1.5)
    .room(0.6)
    .gain(slider(0.18, 0, 0.55))
    .slow(16)
    .color("magenta")
