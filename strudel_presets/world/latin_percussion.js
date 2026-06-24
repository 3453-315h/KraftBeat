// @name Latin Salsa
// @genre World
// @bpm 105
// @tags salsa, mambo, conga, timbales, cuba

setcpm(105 / 4)

// ═══════════════════════════════════════════════════════════════
// LATIN SALSA - Authentic Cuban salsa with polyrhythmic percussion
// ═══════════════════════════════════════════════════════════════

// Son clave 3-2 - the heartbeat of salsa
$clave: s("rim ~ rim ~ ~ rim ~ ~ ~ ~ rim ~ ~ rim ~ ~")
    .bank("RolandTR808")
    .gain(perlin.range(0.6, 0.78))  // Velocity variation
    .sometimes(x => x.s("~ ~ rim ~ rim ~ ~ ~ rim ~ ~ rim ~ ~ ~ ~"))  // 2-3 clave
    .color("yellow")
    ._punchcard()

// Conga tumba pattern with dynamics
$conga: s("[conga:0 ~ conga:1] [conga:2 ~ conga:0] [~ conga:1 conga:2] [conga:0 ~ ~]")
    .gain(perlin.range(0.55, 0.75))  // Velocity variation
    .room(slider(0.12, 0, 0.4))
    .pan(slider(-0.3, -0.5, -0.1))
    .sometimes(x => x.s("[conga:0 conga:1 ~] [conga:2 conga:0 ~] [conga:1 ~ conga:2] [~ conga:0 ~]"))
    .every(4, x => x.s("[conga:0 conga:1 conga:2] [conga:0 conga:1 ~] [conga:2 conga:0 conga:1] [conga:2 ~ ~]"))  // Fill
    .color("orange")
    ._punchcard()

// Timbales - cascara pattern on shell with accents
$timbal: s("[rim rim rim rim] [rim rim rim rim] [rim rim rim rim] [rim rim ~ rim]")
    .bank("RolandTR808")
    .gain("<0.38 0.42 0.38 0.45> <0.38 0.42 0.4 0.5>")  // Velocity pattern
    .pan(slider(0.4, 0.2, 0.6))
    .sometimes(x => x.s("[rim rim ~ rim] [rim rim rim ~] [rim ~ rim rim] [rim rim rim rim]"))
    .every(8, x => x.s("[rim rim rim rim] [rim rim rim rim] [sd ~ sd ~] [sd sd sd sd]"))  // Paila accents
    .color("orange")
    ._punchcard()

// Bongo martillo pattern with variations
$bongo: s("bongo:0 bongo:1 bongo:0 [bongo:1 bongo:0]")
    .gain(perlin.range(0.42, 0.58))  // Humanized
    .pan(slider(0.5, 0.3, 0.7))
    .sometimes(x => x.s("[bongo:0 bongo:1] bongo:0 [bongo:1 ~] bongo:0"))  // Variation
    .every(4, x => x.s("[bongo:0 bongo:1 bongo:0] bongo:1 [bongo:0 bongo:1] [bongo:0 bongo:1 bongo:0]"))  // Fill
    ._punchcard()

// Cowbell - mambo bell pattern
$cowbell: s("[ag:0 ~ ag:0 ~] [~ ag:0 ~ ag:0] [ag:0 ~ ag:0 ~] [~ ag:0 ~ ~]")
    .gain(perlin.range(0.48, 0.62))  // Velocity
    .sometimes(x => x.s("[ag:0 ag:0 ~ ~] [~ ~ ag:0 ag:0] [ag:0 ~ ~ ag:0] [~ ag:0 ~ ~]"))
    .every(8, x => x.s("[ag:0 ag:0 ag:0 ~] [ag:0 ~ ag:0 ag:0] [ag:0 ag:0 ~ ag:0] [~ ag:0 ag:0 ~]"))  // Intensify
    .color("yellow")
    ._punchcard()

// Guiro texture
$guiro: s("~ ~ guiro ~ ~ ~ guiro ~")
    .gain(slider(0.35, 0, 1))
    .pan(slider(-0.5, -0.7, -0.3))
    .sometimes(x => x.s("guiro ~ ~ guiro ~ ~ ~ guiro"))
    .color("brown")

// Bass tumbao - syncopated Cuban bass
$bass: note("<c2 ~ ~ c2 ~ c3 ~ ~ g2 ~ ~ g2 ~ f2 ~ ~>")
    .s("sawtooth")
    .lpf(slider(700, 250, 1400))
    .decay(slider(0.12, 0.05, 0.25))
    .gain(slider(0.82, 0, 2))
    .rarely(x => x.note("<c2 ~ c3 c2 ~ c3 g2 ~ g2 ~ g3 g2 ~ f2 e2 ~>"))  // Walking variation
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })

// Sub layer
$sub: note("<c1 ~ ~ ~ ~ ~ ~ ~ g1 ~ ~ ~ ~ f1 ~ ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.45, 0, 1.2))
    .color("darkred")

// Piano montuno - the driving force
$piano: note("<[c4,e4,g4] ~ [e4,g4,c5] [c4,e4,g4] [g4,c5,e5] ~ [e4,g4,c5] ~>".add("<0 0 5 0 7 0 5 0>"))
    .s("triangle")  // Piano-like
    .lpf(sine.range(2500, 5000).slow(8))
    .decay(slider(0.15, 0.06, 0.28))
    .room(slider(0.2, 0, 0.6))
    .gain(slider(0.58, 0, 2))
    .sometimes(x => x.add(7))  // Transpose up 5th
    .color("cyan")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Brass section stabs with variations
$brass: note("<[c5,e5,g5] ~ ~ ~ [d5,f5,a5] ~ ~ ~ ~ ~ ~ ~ [e5,g5,b5] ~ ~ ~>")
    .s("sawtooth")
    .lpf(slider(3500, 1500, 5500))
    .attack(slider(0.03, 0.01, 0.1))
    .decay(slider(0.25, 0.1, 0.45))
    .gain(slider(0.48, 0, 2))
    .sometimes(x => x.note("<[d5,f5,a5] ~ [e5,g5,b5] ~>"))  // Variation
    .rarely(x => x.fast(2).gain(0.4))  // Double stab
    .color("orange")
    ._punchcard()
