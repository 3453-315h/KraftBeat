// @name Soulful Sunrise
// @genre House
// @bpm 122
// @tags complex, soulful, chords, layers, pianoroll

setcpm(122 / 4)

// Performance controls

// ═══════════════════════════════════════════════════════════════
// SOULFUL HOUSE - Deep chords and warm grooves
// ═══════════════════════════════════════════════════════════════

// Main chord progression with pianoroll
$chords: note("<[c3,eb3,g3,bb3] [ab2,c3,eb3,g3] [f2,ab2,c3,f3] [g2,bb2,d3,g3]>")
    .s("sawtooth")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .attack(slider(0.5, 0, 1))
    .decay(slider(0.3, 0, 1))
    .room(slider(0.3, 0, 1))
    .gain(slider(0.8, 0, 2))
    .slow(slider(4.0, 1, 16))
    .color("purple")
    ._punchcard()
    .pianoroll({ fold: 1 })
    .scope({ size: 256 })

// Rhodes stabs
$rhodes: note("[c4 ~] [eb4 ~] [g4 ~] [bb4 ~]")
    .s("sine")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .decay(slider(0.3, 0, 1))
    .room(slider(0.3, 0, 1))
    .gain(slider(0.8, 0, 2))
    .slow(slider(4.0, 1, 16))
    .color("cyan")
    ._punchcard()

// Arp layer
$arp: note("c4 eb4 g4 bb4 c5 bb4 g4 eb4")
    .s("triangle")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .decay(slider(0.3, 0, 1))
    .gain(slider(0.8, 0, 2))
    .fast(slider(2, 1, 16))
    .jux(rev)
    .color("yellow")
    ._punchcard()

// Deep rolling bass
$bass: note("<c2 [c2 c2] ab1 [ab1 ~] f1 [f1 f2] g1 [g1 g1]>")
    .s("sine")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .decay(slider(0.3, 0, 1))
    .gain(slider(0.8, 0, 2))
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Classic house kick
$kick: s("bd*4")
    .bank("RolandTR909")
    .gain(slider(0.8, 0, 2))
    .shape(slider(0.3, 0, 1))
    .color("orange")
    ._punchcard()

// Clap on 2 and 4
$clap: s("~ cp")
    .bank("RolandTR909")
    .room(slider(0.3, 0, 1))
    .gain(slider(0.8, 0, 2))
    .delay(slider(0.2, 0, 1))
    .color("white")
    ._punchcard()

// Open hat groove
$oh: s("~ ~ ~ ~ ~ ~ oh ~")
    .bank("RolandTR909")
    .gain(slider(0.8, 0, 2))
    .room(slider(0.3, 0, 1))
    .color("lime")
    ._punchcard()

// Shakers
$shaker: s("~ hh:3 ~ hh:3")
    .bank("RolandTR808")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .gain(slider(0.8, 0, 2))
    .color("gray")

// Closed hats
$hat: s("hh*8")
    .bank("RolandTR909")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .gain(slider(0.8, 0, 2))
    .color("white")
    ._punchcard()

// Conga pattern
$conga: s("~ [conga:1 ~] ~ conga:2")
    .gain(slider(0.8, 0, 2))
    .room(slider(0.3, 0, 1))
    .color("pink")
    ._punchcard()
