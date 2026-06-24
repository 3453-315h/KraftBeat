// @name Lo-Fi Chill
// @genre Hip Hop
// @bpm 85
// @tags dusty, relaxing, jazz, vinyl

setcpm(85 / 4)

// ═══════════════════════════════════════════════════════════════
// LO-FI CHILL - Dusty vinyl vibes with jazz chords
// ═══════════════════════════════════════════════════════════════

// Soft dusty kick with lo-fi character
$kick: s("bd ~ [~ bd] ~").bank("SP1200")
    .gain("<0.9 0.85 0.88 0.85> <0.85 0.88 0.9 0.85>")  // Soft dynamics
    .lpf(300)  // Lo-fi roll-off
    .nudge("<0 0 0.035 0>")  // Swing
    .every(8, x => x.s("bd ~ [bd ~] ~ [~ bd] ~ bd ~"))  // Variation
    .color("orange")
    ._punchcard()

// Dusty swung hats
$hat: s("[~ hh] [hh ~] [~ hh] [hh hh]").bank("SP1200")
    .gain(perlin.range(0.28, 0.42))  // Soft humanized
    .lpf(perlin.range(3000, 6000))  // Lo-fi filter
    .nudge(perlin.range(-0.02, 0.04))  // Swing timing
    .pan(perlin.range(-0.15, 0.15).slow(0.5))
    .sometimes(x => x.s("[hh ~] [~ hh] [hh ~] [~ hh]"))  // Variation
    .every(8, x => x.s("[hh hh] [~ hh] [hh hh hh hh] [oh hh]"))  // Fill
    ._punchcard()

// Soft dusty snare with room
$snare: stack(
    s("~ sd ~ sd").gain(slider(0.68, 0, 2)).room(0.45).lpf(4000),  // Lo-fi snare
    s("~ ~ [sd:3 ~] [~ sd:3]").gain(0.2).lpf(3000)  // Ghosts
).bank("SP1200")
    .n(0.5)  // Variant
    .nudge("0 0.015 0 0.02")  // Swing
    .every(8, x => x.s("~ sd ~ [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Vinyl crackle texture - essential lo-fi element
$vinyl: s("[rim:5 rim:5 rim:5 rim:5]*4")
    .gain(slider(0.18, 0, 0.5))
    .lpf(2500)
    .hpf(400)
    .color("brown")

// Jazz-influenced chords with lo-fi warmth
$keys: note("<[c4,e4,g4,b4] [c4,e4,g4,b4] [f4,a4,c5,e5] [g4,b4,d5]>")
    .s("triangle")  // Piano-like
    .lpf(sine.range(1500, 3500).slow(slider(4.0, 1, 16)))
    .decay(0.25)
    .room(slider(0.35, 0, 1))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.note("<[d4,f4,a4,c5] [e4,g4,b4,d5]>"))  // Chord variation
    .color("cyan")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Rhodes layer for warmth
$rhodes: note("<[g3,b3] ~ [a3,c4] ~ [b3,d4] ~ [g3,b3] ~>")
    .s("sine")
    .lpf(2000)
    .decay(0.2)
    .delay(0.15)
    .room(0.3)
    .gain(slider(0.25, 0, 1))
    .slow(slider(4.0, 1, 16))
    .color("yellow")

// Mellow bass with lo-fi warmth
$bass: note("<c2 ~ [c2 ~] ~ f2 ~ [g2 ~] ~>")
    .s("triangle")
    .lpf(sine.range(250, 450).slow(slider(4.0, 1, 16)))
    .decay(slider(0.2, 0.1, 0.4))
    .gain(slider(0.72, 0, 2))
    .rarely(x => x.note("<c2 d2 [e2 d2] c2>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ c1 ~ f1 ~ g1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.4, 0, 1.2))
    .color("darkred")

// Ambient texture - lo-fi haze
$haze: note("[c3,g3]")
    .s("sawtooth")
    .lpf(sine.range(300, 800).slow(32))
    .attack(1.5)
    .release(1)
    .room(0.6)
    .gain(slider(0.12, 0, 0.4))
    .slow(8)
    .color("purple")
    .scope({ size: 256 })
