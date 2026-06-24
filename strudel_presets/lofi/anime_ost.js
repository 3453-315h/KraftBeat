// @name Anime OST
// @genre Lo-Fi
// @bpm 85
// @tags anime, nostalgic, warm, emotional

setcpm(85 / 4)

// ═══════════════════════════════════════════════════════════════
// ANIME OST - Nostalgic Japanese animation soundtrack vibes
// ═══════════════════════════════════════════════════════════════

// Soft kick with swing
$kick: s("bd ~ [~ bd] ~").bank("SP1200")
    .gain("<0.88 0.82 0.85 0.8>")  // Soft dynamics
    .lpf(300)  // Warm
    .nudge("<0 0 0.02 0>")  // Swing
    .every(8, x => x.s("bd ~ [bd ~] ~ [~ bd] ~ bd ~"))
    .color("orange")
    ._punchcard()

// Snare with ghost layers
$snare: stack(
    s("~ sd ~ sd").gain(slider(0.72, 0, 2)).room(0.38).lpf(4000),
    s("~ ~ [sd:3 ~] ~").gain(0.2).lpf(3500)  // Ghost
).bank("SP1200")
    .nudge("0 0.012 0 0.015")  // Swing
    .every(8, x => x.s("~ sd ~ [sd sd sd sd]"))
    .color("white")
    ._punchcard()

// Hats with warmth
$hat: s("hh*8").bank("SP1200")
    .gain(perlin.range(0.3, 0.45))  // Humanized
    .lpf(perlin.range(4000, 8000))
    .pan(perlin.range(-0.1, 0.1).slow(0.5))
    .sometimes(x => x.s("[hh hh oh hh] [hh hh hh hh] [hh hh oh hh] [hh hh hh oh]"))
    .color("white")
    ._punchcard()

// Vinyl crackle
$vinyl: s("[rim:5 rim:5 rim:5 rim:5]*4")
    .gain(slider(0.12, 0, 0.35))
    .lpf(2500)
    .hpf(400)
    .color("brown")

// Nostalgic melody - classic anime vibes (Mary Had a Little Lamb style)
$melody: note("<e5 d5 c5 d5 e5 e5 e5 ~ d5 d5 d5 ~ e5 g5 g5 ~>")
    .s("sine")
    .lpf(sine.range(2500, 5500).slow(slider(8, 4, 16)))
    .decay(0.18)
    .delay(0.12)
    .room(slider(0.35, 0, 0.9))
    .gain(slider(0.52, 0, 2))
    .sometimes(x => x.note("<c5 d5 e5 g5 e5 d5 c5>"))  // Variation
    .rarely(x => x.fast(1.5))  // Quick phrase
    .color("cyan")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Counter melody
$counter: note("<~ ~ g4 ~ ~ ~ e4 ~ ~ ~ c4 ~ ~ ~ ~ ~>")
    .s("sine")
    .lpf(4000)
    .decay(0.2)
    .delay(0.2)
    .room(0.35)
    .gain(slider(0.28, 0, 1))
    .slow(2)
    .color("lime")

// Warm chords - emotional progression
$chords: note("<[c4,e4,g4] [c4,e4,g4] [a3,c4,e4] [g3,b3,d4]>")
    .s("triangle")
    .lpf(sine.range(1800, 4000).slow(slider(8, 4, 16)))
    .attack(slider(0.12, 0.05, 0.28))
    .release(slider(0.35, 0.15, 0.65))
    .slow(slider(4.0, 1, 16))
    .room(slider(0.42, 0, 0.95))
    .gain(slider(0.48, 0, 1.8))
    .sometimes(x => x.note("<[d4,f4,a4] [e4,g4,b4]>"))  // ii-iii
    .color("purple")
    ._punchcard()
    .scope({ size: 256 })

// Second chord layer
$chords2: note("<[g3,c4] [a3,c4] [g3,b3] [g3,c4]>")
    .s("sine")
    .lpf(2500)
    .attack(0.15)
    .release(0.35)
    .room(0.35)
    .gain(slider(0.22, 0, 0.8))
    .slow(slider(4.0, 1, 16))
    .color("yellow")

// Bass - emotional movement
$bass: note("<c2 ~ a1 ~ g1 ~ a1 ~>")
    .s("triangle")
    .lpf(sine.range(260, 520).slow(slider(8, 4, 16)))
    .decay(slider(0.18, 0.08, 0.32))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.72, 0, 2))
    .rarely(x => x.note("<c2 [c2 d2] a1 [b1 a1] g1 [g1 a1] a1 [g1 a1]>"))  // Walking
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ a0 ~ g0 ~ a0 ~>")
    .s("sine")
    .lpf(75)
    .gain(slider(0.4, 0, 1.1))
    .color("darkred")
