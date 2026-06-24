// @name Jazz Odyssey
// @genre Classic
// @bpm 125
// @tags complex, jazz, swing, sophisticated, fusion

setcpm(125 / 4)

// ═══════════════════════════════════════════════════════════════
// JAZZ ODYSSEY - High energy fusion jazz with complex harmonies
// ═══════════════════════════════════════════════════════════════

// Jazz brush drums - driving swing
$kick: s("[bd ~ ~ bd] [~ ~ bd ~]").bank("RolandTR909")
    .gain(slider(0.85, 0, 2))
    .lpf(600)
    .nudge(0.01)
    .color("orange")
    ._punchcard()

$brush: s("[~ ~ sd ~] [~ sd ~ sd]").bank("RolandTR909")
    .gain(slider(0.75, 0, 1.8))
    .lpf(3000)
    .decay(0.25)
    .color("tan")
    ._punchcard()

$ride: s("[rd ~ rd rd] [rd ~ rd ~]").bank("RolandTR909")
    .gain(perlin.range(0.45, 0.6))
    .nudge(perlin.range(0.01, 0.03))  // Swing
    .pan(0.4)
    .color("gold")
    ._punchcard()

$hat: s("~ ~ ~ ~ ~ ~ ~ [hh ~]").bank("RolandTR909")
    .gain(0.4)
    .color("white")
    ._punchcard()

$ghost: s("~ [sd:5 ~] ~ [~ sd:5]").bank("RolandTR909")
    .gain(0.6)
    .lpf(2000)
    .color("gray")

// Walking bass - driving line
$bass: note("c2 e2 g2 a2 b2 a2 g2 e2")
    .s("sawtooth")
    .lpf(sine.range(300, 900).slow(slider(4.0, 1, 16)))
    .decay(0.25)
    .gain(slider(0.82, 0, 2))
    .nudge(0.015)
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Jazz piano comping - complex rhythms
$piano: note("<[c3,e3,g3,b3] [d3,f3,a3,c4] [e3,g3,b3,d4] [a2,c3,e3,g3]>")
    .s("triangle")
    .lpf(sine.range(1500, 4500).slow(slider(8, 4, 16)))
    .decay(0.3)
    .struct("x(5,16)")  // Syncopated
    .room(slider(0.35, 0, 0.8))
    .gain(slider(0.6, 0, 2))
    .pan(0.2)
    .color("brown")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Rhodes counter-melody
$rhodes: note("<[c4,e4] ~ [g3,b3] ~> <~ [d4,f4] ~ [e4,g4]>")
    .s("sine")
    .lpf(3000)
    .decay(0.2)
    .room(0.3)
    .gain(slider(0.45, 0, 1.5))
    .pan(-0.3)
    .color("cyan")
    ._punchcard()

// Lead synth improvisation
$lead: note("<c4 ~ e4 ~> <g4 ~ ~ a4> <~ b4 a4 ~> <g4 e4 ~ ~>")
    .s("sawtooth")
    .lpf(sine.range(800, 3500).slow(8))
    .decay(0.15)
    .slide(0.1)
    .room(0.4)
    .gain(slider(0.55, 0, 1.8))
    .sometimes(x => x.note("<e4 g4 c5 b4 a4 g4 e4 d4>"))  // Fast run
    .color("yellow")
    ._punchcard()

// String pad backing
$strings: note("[c3,g3,e4]")
    .s("sawtooth")
    .lpf(sine.range(600, 1800).slow(16))
    .attack(0.5)
    .release(0.5)
    .room(0.5)
    .gain(slider(0.3, 0, 1))
    .slow(4)
    .color("purple")
    .scope({ size: 256 })
