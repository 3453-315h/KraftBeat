// @name Balkan Brass
// @genre World
// @bpm 130
// @tags balkan, brass, čoček, gypsy, hijaz

setcpm(130 / 4)

// ═══════════════════════════════════════════════════════════════
// BALKAN BRASS - Čoček rhythm with Hijaz scale brass section
// ═══════════════════════════════════════════════════════════════

// Tapan (bass drum) - driving čoček rhythm with dynamics
$tapan: s("[bd ~ bd ~] [~ bd ~ bd] [bd ~ bd ~] [~ bd ~ bd]").bank("RolandTR808")
    .gain("<1.0 1.05 0.98 1.08> <1.02 0.95 1.05 1.0>")  // Dynamics
    .shape(slider(0.25, 0, 0.55))
    .nudge(perlin.range(-0.01, 0.015))  // Humanized
    .sometimes(x => x.s("[bd bd ~ ~] [~ bd bd ~] [bd ~ bd bd] [~ bd ~ ~]"))  // Variation
    .every(8, x => x.s("[bd ~ bd bd] [bd bd ~ bd] [bd ~ bd ~] [bd bd bd ~]"))  // Fill
    .color("orange")
    ._punchcard()

// Snare side of tapan with dynamics
$snare: s("[~ sd ~ sd] [sd ~ sd ~] [~ sd ~ sd] [sd ~ sd ~]").bank("RolandTR808")
    .gain(perlin.range(0.65, 0.82))  // Velocity variation
    .nudge(perlin.range(-0.01, 0.015))
    .sometimes(x => x.s("[sd ~ sd ~] [~ sd ~ sd] [sd sd ~ ~] [~ ~ sd sd]"))
    .every(8, x => x.s("[sd sd ~ sd] [sd ~ sd sd] [~ sd sd ~] [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Zurla (shawm) - main melody - Hijaz scale with ornamentation
$zurla: note("<d5 eb5 f#5 g5 a5 bb5 a5 g5 f#5 eb5 d5 ~ ~ ~ ~ ~>")
    .s("sawtooth")
    .lpf(slider(4000, 2000, 7000))
    .attack(slider(0.02, 0.01, 0.08))
    .decay(slider(0.25, 0.12, 0.45))
    .struct("x(11,16)")  // Euclidean pattern
    .gain(slider(0.58, 0, 2))
    .sometimes(x => x.note("<f#5 g5 a5 bb5 a5 g5 f#5 eb5 d5>"))  // Variation
    .rarely(x => x.fast(1.5))  // Faster ornament
    .color("lime")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Trumpet section - harmonized brass with variations
$trumpet: note("<[d5,f#5,a5] ~ ~ ~ [eb5,g5,bb5] ~ ~ ~ [d5,f#5,a5] ~ [eb5,g5,bb5] ~ ~ ~ ~ ~>")
    .s("sawtooth")
    .lpf(slider(5000, 2500, 9000))
    .attack(slider(0.03, 0.01, 0.12))
    .decay(slider(0.3, 0.15, 0.55))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.note("<[g5,bb5,d6] ~ [f#5,a5,d6] ~>"))  // Variation
    .rarely(x => x.fast(2).gain(0.45))  // Fast stab
    .color("yellow")
    ._punchcard()

// Trombone - bass stabs with movement
$trombone: note("<d3 ~ ~ ~ g3 ~ a3 ~ d3 ~ ~ ~ a2 ~ d3 ~>")
    .s("sawtooth")
    .lpf(slider(2000, 700, 3800))
    .decay(slider(0.35, 0.15, 0.6))
    .gain(slider(0.62, 0, 2))
    .rarely(x => x.note("<d3 eb3 ~ ~ g3 a3 bb3 ~ d3 ~ ~ ~ a2 bb2 d3 ~>"))  // Walking
    .color("orange")
    ._punchcard()

// Tuba - bass line foundation
$tuba: note("<d2 ~ d2 ~ g2 ~ a2 ~ d2 ~ g2 ~ a2 ~ d2 ~>")
    .s("sawtooth")
    .lpf(slider(400, 150, 700))
    .decay(slider(0.2, 0.08, 0.42))
    .gain(slider(0.78, 0, 2))
    .rarely(x => x.note("<d2 eb2 d2 ~ g2 g2 a2 a2 d2 ~ g2 a2 bb2 a2 d2 ~>"))  // Walking
    .scope({ size: 256 })
    .color("red")

// Sub layer
$sub: note("<d1 ~ d1 ~ g1 ~ a1 ~ d1 ~ g1 ~ a1 ~ d1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.45, 0, 1.2))
    .color("darkred")

// Clarinet ornaments with euclidean gating
$clarinet: note("<a5 ~ bb5 ~ a5 g5 f#5 ~ g5 ~ a5 ~ ~ ~ ~ ~>")
    .s("triangle")
    .lpf(slider(6000, 2800, 9500))
    .attack(slider(0.02, 0.01, 0.08))
    .decay(slider(0.2, 0.08, 0.38))
    .struct("x(7,16)")
    .slow(slider(2, 1, 4))
    .gain(slider(0.48, 0, 2))
    .sometimes(x => x.note("<d6 eb6 d6 c6 bb5 a5 g5>"))  // High ornament
    .color("cyan")
    ._punchcard()
