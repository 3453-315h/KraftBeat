// @name Deep Visual House
// @genre House
// @bpm 124
// @tags deep, visual, soulful

setcpm(124 / 4)

// Performance controls

// Deep house chord stabs with pianoroll
$chords: note("<[c3,eb3,g3,bb3] [f2,ab2,c3,eb3] [ab2,c3,eb3,g3] [bb2,d3,f3,ab3]>")
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

// Deep bassline
$bass: note("<c2 c2 f1 f1 ab1 ab1 bb1 bb1>")
    .s("sine")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .decay(slider(0.3, 0, 1))
    .gain(slider(0.8, 0, 2))
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Rhodes-style keys
$keys: note("[c4 ~] [eb4 ~] <g4 f4> [eb4 ~]")
    .s("sine")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .decay(slider(0.3, 0, 1))
    .room(slider(0.3, 0, 1))
    .gain(slider(0.8, 0, 2))
    .slow(slider(4.0, 1, 16))
    .color("cyan")
    ._punchcard()

// Classic house drums
    .shape(slider(0.3, 0, 1))
$clap: s("~ cp").bank("RolandTR909").room(slider(0.2, 0, 1)).gain(slider(0.7, 0, 2)).color("yellow")
    ._punchcard()
$kick: s("bd*4").bank("RolandTR909").gain(slider(1.1, 0, 2)).color("orange")
    ._punchcard()
    .delay(slider(0.2, 0, 1))
$hat: s("hh*8").bank("RolandTR909").lpf(sine.range(200, 4000).slow(slider(8.0, 1, 16)).gain(slider(0.25, 0, 2)).color("white")
    ._punchcard()
$oh: s("~ ~ ~ ~ ~ ~ oh ~").bank("RolandTR909").gain(slider(0.8, 0, 2)).color("lime")

// Shaker groove
$shaker: s("~ hh:2 ~ hh:2").bank("RolandTR808").lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)).gain(slider(0.8, 0, 2)).color("gray")
