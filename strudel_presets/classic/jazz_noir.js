// @name Jazz Noir
// @genre Classic
// @bpm 90
// @tags jazz, noir, smoky, sophisticated, slow

setcpm(90 / 4)

// ═══════════════════════════════════════════════════════════════
// JAZZ NOIR - Smoky, slow, atmospheric jazz
// ═══════════════════════════════════════════════════════════════

// Brush kit - smoky rhythm
$kick: s("bd ~ ~ bd").bank("RolandTR909")
    .gain(slider(0.7, 0, 2))
    .lpf(400)  // Soft kick
    .shape(0.2)
    .nudge(0.02)  // Laid back
    .color("orange")
    ._punchcard()

// Brush snare sweeps
$brush: s("~ [sd:5 ~] ~ [sd:5 ~]").bank("RolandTR909")
    .gain(slider(0.65, 0, 1.5))
    .lpf(2500)
    .decay(0.4)
    .room(0.3)
    .color("tan")
    ._punchcard()

// Ride cymbal - slow swing
$ride: s("rd ~ rd ~").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.5))
    .nudge(perlin.range(0.02, 0.04))  // Heavy swing
    .pan(0.3)
    .color("gold")
    ._punchcard()

// Hi-hat foot
$hat: s("~ hh ~ hh").bank("RolandTR909")
    .gain(0.3)
    .color("white")
    ._punchcard()

// Walking bass - slow and deep
$bass: note("d2 a1 c2 d2 f2 e2 d2 a1")
    .s("sine")
    .lpf(sine.range(200, 600).slow(8))
    .decay(0.4)
    .gain(slider(0.8, 0, 2))
    .nudge(0.01)
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Jazz piano voicings - rootless/extended
$: n("<[f3,a3,c4,e4] [e3,g3,b3,d4] [eb3,g3,bb3,d4] [d3,f3,a3,c4]>")
    .s("triangle")  // Piano-like
    .lpf(sine.range(1500, 3500).slow(16))
    .decay(slider(0.35, 0.1, 0.8))
    .room(slider(0.45, 0, 0.9))
    .gain(slider(0.65, 0, 2))
    .slow(slider(2, 1, 8))
    .pan(slider(-0.2, -0.5, 0.5))
    .color("brown")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Rhodes drops
$rhodes: note("<~ ~ c5 ~> <~ a4 ~ ~>")
    .s("sine")
    .lpf(2000)
    .decay(0.25)
    .room(0.4)
    .gain(slider(0.35, 0, 1))
    .slow(2)
    .color("cyan")

// String pad - noir strings
$strings: note("d3")
    .s("sawtooth")
    .lpf(800)
    .attack(1.5)
    .release(2)
    .room(0.6)
    .gain(slider(0.25, 0, 0.8))
    .slow(4)
    .color("purple")
    .scope({ size: 256 })

// Saxophone-ish lead (placeholder texture)
$sax: note("<f4 ~ d4 ~ e4 ~ c4 ~>")
    .s("sawtooth")
    .lpf(sine.range(600, 2000).slow(4))
    .attack(0.1)
    .decay(0.4)
    .room(0.5)
    .gain(slider(0.4, 0, 1.2))
    .slow(2)
    .color("yellow")
