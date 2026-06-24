// @name Bhangra Beat
// @genre World
// @bpm 95
// @tags bhangra, punjabi, dhol, tumbi, festival

setcpm(95 / 4)

// ═══════════════════════════════════════════════════════════════
// BHANGRA - Punjabi festival groove with dhol and tumbi
// ═══════════════════════════════════════════════════════════════

// Dhol bass - the heart of bhangra with dynamics
$dhol_bass: s("[bd ~ bd ~] [~ bd ~ ~] [bd ~ bd bd] [~ bd ~ ~]").bank("RolandTR808")
    .gain("<1.08 1.12 1.05 1.15> <1.1 1.05 1.12 1.08>")  // Dynamics
    .shape(slider(0.3, 0, 0.65))
    .nudge(perlin.range(-0.01, 0.02))  // Humanized
    .sometimes(x => x.s("[bd bd bd ~] [~ bd ~ bd] [bd ~ bd bd] [bd bd ~ ~]"))  // Variation
    .every(8, x => x.s("[bd bd bd bd] [bd bd ~ bd] [bd bd bd bd] [bd bd bd bd]"))  // Energetic fill
    .color("orange")
    ._punchcard()

// Dhol treble with velocity patterns
$dhol_treble: s("[~ sd ~ sd] [sd ~ sd ~] [~ sd ~ ~] [sd ~ sd sd]").bank("RolandTR808")
    .gain(perlin.range(0.75, 0.92))  // Velocity variation
    .sometimes(x => x.s("[sd ~ sd ~] [~ sd ~ sd] [sd ~ sd sd] [~ sd ~ ~]"))  // Variation
    .every(8, x => x.s("[sd sd ~ sd] [sd ~ sd sd] [sd sd sd ~] [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Chimta (tongs) - metallic accent with variations
$chimta: s("[~ ~ ~ ag:0] [~ ~ ~ ~] [~ ~ ~ ag:0] [~ ~ ag:0 ~]")
    .gain(perlin.range(0.52, 0.68))  // Velocity
    .sometimes(x => x.s("[ag:0 ~ ~ ~] [~ ~ ag:0 ~] [~ ~ ~ ag:0] [ag:0 ~ ~ ~]"))  // Pattern 2
    .every(8, x => x.s("[ag:0 ~ ag:0 ~] [~ ag:0 ~ ag:0] [ag:0 ~ ~ ag:0] [~ ag:0 ag:0 ~]"))  // Intensify
    .color("yellow")
    ._punchcard()

// Dholki pattern - lighter hand drum with dynamics
$dholki: s("tabla:1 ~ [tabla:2 tabla:1] ~ tabla:0 ~ [tabla:1 ~] tabla:2")
    .gain(perlin.range(0.42, 0.58))  // Velocity variation
    .pan(slider(0.3, 0.1, 0.5))
    .sometimes(x => x.s("[tabla:1 tabla:2] ~ tabla:0 ~ [tabla:1 ~] tabla:2 [tabla:0 tabla:1] ~"))
    ._punchcard()

// Tumbi - single-string Punjabi instrument (signature bhangra sound)
$tumbi: note("<g4 ~ g4 g4 ~ g4 ~ ~ a4 ~ g4 ~ e4 ~ g4 ~>")
    .s("triangle")  // Tumbi-like
    .lpf(slider(4000, 1500, 7000))
    .decay(slider(0.2, 0.08, 0.42))
    .gain(slider(0.68, 0, 2))
    .sometimes(x => x.note("<g4 a4 g4 ~ e4 g4 a4 ~ g4 ~ e4 ~ d4 e4 g4 ~>"))  // Melodic variation
    .rarely(x => x.fast(2).gain(0.55))  // Fast tumbi
    .color("lime")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Bass line - punchy and rhythmic with variations
$bass: note("<g2 ~ g2 ~ d2 ~ g2 ~ c3 ~ g2 ~ d2 ~ g2 ~>")
    .s("sawtooth")
    .lpf(slider(600, 250, 1200))
    .decay(slider(0.12, 0.05, 0.28))
    .gain(slider(0.82, 0, 2))
    .rarely(x => x.note("<g2 g2 [g2 a2] d2 d2 [d2 e2] g2 ~ c3 c3 [b2 a2] g2>"))  // Walking
    .scope({ size: 256 })
    .color("red")

// Sub layer
$sub: note("<g1 ~ ~ ~ ~ ~ ~ ~ g1 ~ ~ ~ ~ ~ ~ ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.48, 0, 1.3))
    .color("darkred")

// Synth stabs - modern bhangra element with variations
$synth: note("<[g4,b4,d5] ~ ~ ~ [a4,c5,e5] ~ ~ ~ ~ ~ ~ ~ [g4,b4,d5] ~ ~ ~>")
    .s("sawtooth")
    .lpf(slider(3000, 1500, 5500))
    .attack(slider(0.02, 0.01, 0.08))
    .decay(slider(0.2, 0.08, 0.42))
    .gain(slider(0.52, 0, 2))
    .sometimes(x => x.note("<[a4,c5,e5] ~ [g4,b4,d5] ~>"))  // Variation
    .rarely(x => x.fast(2).gain(0.42))  // Fast stabs
    .color("purple")
    ._punchcard()

// Algoza (double flute) melodic line with ornamentation
$flute: note("<g5 a5 b5 d6 b5 a5 g5 ~ e5 g5 a5 ~ g5 ~ ~ ~>")
    .s("triangle")
    .lpf(slider(6000, 2500, 9000))
    .attack(slider(0.05, 0.02, 0.15))
    .decay(slider(0.4, 0.15, 0.75))
    .slow(slider(2, 1, 4))
    .room(slider(0.22, 0, 0.6))
    .delay(0.1)
    .gain(slider(0.42, 0, 1.8))
    .sometimes(x => x.note("<b5 d6 b5 a5 g5 e5 d5>"))  // Descending
    .color("cyan")
    ._punchcard()
