// @name Midnight Study
// @genre Lofi
// @bpm 78
// @tags complex, lofi, chill, study, vinyl, pianoroll

setcpm(78 / 4)

// Vibe controls

// ═══════════════════════════════════════════════════════════════
// MIDNIGHT STUDY - Dusty beats and nostalgic vibes
// ═══════════════════════════════════════════════════════════════

// Lofi piano chops with pianoroll
$piano: note("<[c4,e4,g4] ~ [a3,c4,e4] ~> <[f3,a3,c4] ~ [g3,b3,d4] [e3,g3,b3]>")
    .s("piano")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .decay(slider(0.3, 0, 1))
    .gain(slider(0.8, 0, 2))
    .room(slider(0.3, 0, 1))
    .speed(slider(0.5, 0.5, 2))
    .color("brown")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Electric piano
$ep: note("<c5 ~ e5 ~> <~ g4 ~ ~> <a4 ~ ~ ~> <g4 ~ e4 ~>")
    .s("sine")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .decay(slider(0.3, 0, 1))
    .gain(slider(0.8, 0, 2))
    .room(slider(0.3, 0, 1))
    .pan(sine.range(200, 4000).slow(slider(4.0, 1, 16))
    .slow(slider(4.0, 1, 16))
    .color("cyan")

// Mellow bass
$bass: note("<c2 [c2 ~] a1 [a1 ~]> <f1 [f1 ~] g1 [g1 g1]>")
    .s("sine")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .decay(slider(0.3, 0, 1))
    .gain(slider(0.8, 0, 2))
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Vinyl crackle simulation
$vinyl: s("[rim:5 rim:5]*8")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .gain(slider(0.8, 0, 2))
    .pan(rand.range(-0.5, 0.5))
    .color("gray")

// Lofi kick - softened
$kick: s("[bd ~ ~ ~] [~ ~ bd ~]")
    .bank("RolandTR808")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .gain(slider(0.8, 0, 2))
    .shape(slider(0.3, 0, 1))
    .color("orange")
    ._punchcard()

// Soft snare
$snare: s("~ sd ~ sd")
    .bank("RolandTR808")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .room(slider(0.3, 0, 1))
    .gain(slider(0.8, 0, 2))
    .color("tan")
    ._punchcard()

// Ghost snares
$ghost: s("~ ~ [sd:3 ~] ~")
    .bank("RolandTR808")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .gain(slider(0.8, 0, 2))
    .color("beige")

// Lazy hi-hats
$hat: s("[hh ~ ~] [~ hh ~] [hh ~ hh] [~ ~ hh]")
    .bank("RolandTR808")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .gain(slider(0.8, 0, 2))
    .sometimes(x => x.gain(slider(0.8, 0, 2)))
    .color("white")
    ._punchcard()

// Ambient pad
$pad: note("[c3,g3,c4]")
    .s("sawtooth")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .attack(slider(0.5, 0, 1))
    .release(slider(0.3, 0, 1))
    .gain(slider(0.8, 0, 2))
    .room(slider(0.3, 0, 1))
    .slow(slider(4.0, 1, 16))
    .color("purple")
    .scope({ size: 256 })

// Tape stop effect style
$tape: note("<~ ~ ~ ~ ~ ~ ~ c4>")
    .s("sine")
    .decay(slider(0.3, 0, 1))
    .gain(slider(0.8, 0, 2))
    .speed(sine.range(200, 4000).slow(slider(4.0, 1, 16))
    .room(slider(0.3, 0, 1))
    .slow(slider(4.0, 1, 16))
    .color("pink")

// Jazz brush ghost
$brush: s("~ [hh:2 ~] ~ [~ hh:2]")
    .lpf(sine.range(200, 4000).slow(slider(4.0, 1, 16)))
    .gain(slider(0.8, 0, 2))
    .room(slider(0.3, 0, 1))
    .color("lightgray")
