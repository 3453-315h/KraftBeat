// @name Global Fusion
// @genre World
// @bpm 100
// @tags fusion, world, multicultural, groove, hybrid

setcpm(100 / 4)

// ═══════════════════════════════════════════════════════════════
// GLOBAL FUSION - Multicultural hybrid rhythms and scales
// ═══════════════════════════════════════════════════════════════

// Hybrid drums - Afro-Cuban funk blend
$kick: s("[bd ~ bd ~] [~ ~ bd ~] [bd ~ ~ bd] [~ ~ bd ~]").bank("RolandTR808")
    .gain("<0.95 0.92 0.98 0.9>")
    .shape(slider(0.25, 0, 0.6))
    .nudge(perlin.range(-0.015, 0.02))
    .every(8, x => x.s("[bd ~ bd bd] [~ bd ~ bd] [bd ~ bd ~] [bd bd bd ~]"))
    .color("orange")
    ._punchcard()

$snare: s("~ ~ ~ ~ sd ~ ~ ~ ~ ~ ~ ~ sd ~ ~ ~").bank("RolandTR808")
    .gain(slider(0.85, 0, 2))
    .room(slider(0.25, 0, 0.7))
    .sometimes(x => x.s("~ ~ ~ ~ sd ~ ~ ~ ~ ~ sd ~ sd ~ ~ ~"))
    .color("white")
    ._punchcard()

// African shekere + Latin shaker hybrid
$shaker: s("shaker*16")
    .gain(perlin.range(0.25, 0.45))
    .pan(sine.range(-0.35, 0.35).slow(8))
    .every(4, x => x.gain(perlin.range(0.35, 0.55)))  // Accents
    ._punchcard()

// Tabla-influenced percussion
$tabla: s("[tabla:0 ~ tabla:1] [~ tabla:2 ~] [tabla:0 ~ ~] [tabla:1 tabla:2 ~]")
    .gain(slider(0.58, 0, 1.8))
    .pan(slider(-0.4, -1, 1))
    .sometimes(x => x.s("[tabla:0 tabla:1] [tabla:2 tabla:0] [tabla:1 ~] tabla:2"))
    ._punchcard()

// Congas - Afro-Latin crossover
$conga: s("[conga:0 ~ conga:1] [conga:2 ~ conga:0] [~ conga:1 conga:2] [conga:0 ~ ~]")
    .gain(slider(0.52, 0, 1.8))
    .pan(slider(0.4, -1, 1))
    .struct("x(7,16)")
    .sometimes(x => x.struct("x(9,16)"))
    ._punchcard()

// Fretless bass - Middle Eastern/Jazz fusion with slides
$bass: note("<c2 ~ d2 ~ eb2 ~ f2 ~ g2 ~ f2 ~ eb2 ~ d2 ~>")
    .s("sawtooth")
    .lpf(sine.range(400, 1200).slow(slider(4.0, 1, 16)))
    .decay(slider(0.25, 0.1, 0.6))
    .gain(slider(0.82, 0, 2))
    .slide(0.2)  // Fretless feel
    .rarely(x => x.note("<c2 d2 eb2 f2 g2 ab2 g2 f2>"))  // Phrygian run
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })

// Koto/Sitar hybrid melody - Asian pentatonic scales
$melody: note("<c5 d5 eb5 g5 ab5 g5 eb5 d5 c5 ~ ~ ~ ~ ~ ~ ~>")
    .s("pluck")
    .lpf(sine.range(3000, 8000).slow(16))
    .decay(slider(0.35, 0.15, 0.75))
    .struct("x(7,16)")
    .slow(slider(2, 1, 4))
    .room(slider(0.35, 0, 0.8))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.note("<eb5 f5 g5 bb5 c6 bb5 g5 f5>"))  // Shift
    .color("cyan")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Synth pad - world texture
$pad: note("<[c3,eb3,g3] [c3,eb3,g3] [ab2,c3,eb3] [bb2,d3,f3]>")
    .s("sawtooth")
    .lpf(sine.range(400, 2500).slow(slider(16, 8, 32)))
    .attack(slider(0.8, 0.2, 1.5))
    .release(slider(1, 0.4, 2))
    .slow(slider(4, 2, 8))
    .room(0.5)
    .gain(slider(0.35, 0, 1.2))
    .color("purple")
    .scope({ size: 256 })

// Flute/whistle - Celtic/Andean blend with breath
$flute: note("<g5 ~ ab5 ~ c6 ~ ab5 ~ g5 ~ eb5 ~ c5 ~ ~ ~>")
    .s("triangle")
    .lpf(slider(7000, 3000, 11000))
    .attack(slider(0.08, 0.02, 0.25))
    .decay(slider(0.45, 0.2, 0.8))
    .slow(slider(4, 2, 8))
    .room(0.4)
    .gain(slider(0.42, 0, 1.5))
    .sometimes(x => x.note("<c6 d6 eb6 c6 ab5 g5 eb5 c5>"))  // High run
    .color("lime")
    ._punchcard()
