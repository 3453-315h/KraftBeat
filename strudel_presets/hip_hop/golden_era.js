// @name Golden Era
// @genre Hip Hop
// @bpm 92
// @tags complex, boom bap, golden, vinyl, pianoroll

setcpm(92 / 4)

// Beat controls

// ═══════════════════════════════════════════════════════════════
// GOLDEN ERA HIP HOP - Dusty samples and boom bap drums
// ═══════════════════════════════════════════════════════════════

// Jazz piano chops with pianoroll
$piano: note("<[c4,e4,g4] [~] [a3,c4,e4] [~]> <[f3,a3,c4] [~] [g3,b3,d4] [d4,f4,a4]>")
    .s("piano")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .decay(slider(0.3, 0, 1))
    .room(slider(0.3, 0, 1))
    .gain(slider(0.8, 0, 2))
    .color("yellow")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Rhodes layer
$rhodes: note("<c5 ~ e5 ~> <~ g4 ~ a4>")
    .s("sine")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .decay(slider(0.3, 0, 1))
    .gain(slider(0.8, 0, 2))
    .slow(slider(4.0, 1, 16))
    .color("cyan")
    ._punchcard()

// Deep bass
$bass: note("<c2 [c2 ~] c2 [~ c2]> <a1 [a1 ~] g1 [g1 g1]>")
    .s("sine")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .decay(slider(0.3, 0, 1))
    .gain(slider(0.8, 0, 2))
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Boom bap kick
$kick: s("[bd ~ ~ bd] [~ ~ bd ~]")
    .bank("RolandTR808")
    .gain(slider(0.8, 0, 2))
    .shape(slider(0.3, 0, 1))
    .color("orange")
    ._punchcard()

// Snare on 2 and 4
$snare: s("~ sd ~ sd")
    .bank("RolandTR808")
    .room(slider(0.3, 0, 1))
    .gain(slider(0.8, 0, 2))
    .color("white")
    ._punchcard()

// Ghost snares
$ghost: s("~ ~ [sd:3 ~] ~")
    .bank("RolandTR808")
    .gain(slider(0.8, 0, 2))
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .color("gray")

// Hi-hats with swing
$hat: s("[hh ~] [~ hh] [hh ~] [hh hh]")
    .bank("RolandTR808")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .gain(slider(0.8, 0, 2))
    .color("white")
    ._punchcard()

// Open hat
$oh: s("~ ~ ~ ~ ~ ~ [oh ~] ~")
    .bank("RolandTR808")
    .gain(slider(0.8, 0, 2))
    .color("lime")
    ._punchcard()

// Vinyl crackle simulation (rim)
$crackle: s("[rim:5 rim:5 rim:5 rim:5]*4")
    .gain(slider(0.8, 0, 2))
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .color("brown")

// String stab
$strings: note("<[c4,e4,g4,c5] ~ ~ ~>")
    .s("sawtooth")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .attack(slider(0.5, 0, 1))
    .decay(slider(0.3, 0, 1))
    .gain(slider(0.8, 0, 2))
    .room(slider(0.3, 0, 1))
    .slow(slider(4.0, 1, 16))
    .color("purple")
    ._punchcard()
    .scope({ size: 256 })
