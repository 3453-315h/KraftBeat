// @name Coffee Shop
// @genre Lo-Fi
// @bpm 78
// @tags coffee, warm, afternoon, jazzy

setcpm(78 / 4)

// ═══════════════════════════════════════════════════════════════
// COFFEE SHOP - Warm afternoon vibes with jazzy chords
// ═══════════════════════════════════════════════════════════════

// Soft dusty kick with swing
$kick: s("bd ~ [~ bd] ~").bank("SP1200")
    .gain("<0.82 0.78 0.8 0.75>")  // Soft dynamics
    .lpf(270)  // Warm lo-fi
    .nudge("<0 0 0.025 0>")  // Swing
    .every(8, x => x.s("bd ~ [bd ~] ~ [~ bd] ~ bd ~"))
    .color("orange")
    ._punchcard()

// Soft snare with room
$snare: stack(
    s("~ sd ~ sd").gain(slider(0.68, 0, 2)).room(0.42).lpf(3800),
    s("~ ~ [sd:3 ~] [~ sd:3]").gain(0.18).lpf(3200)  // Ghosts
).bank("SP1200")
    .nudge("0 0.012 0 0.018")  // Swing
    .every(8, x => x.s("~ sd ~ [sd sd sd sd]"))
    .color("white")
    ._punchcard()

// Offbeat hats with warmth
$hat: s("[~ hh] hh [~ hh] hh").bank("SP1200")
    .gain(perlin.range(0.28, 0.42))  // Humanized
    .lpf(perlin.range(3500, 6500))  // Lo-fi filter
    .nudge(perlin.range(-0.015, 0.03))  // Swing
    .pan(perlin.range(-0.12, 0.12).slow(0.5))
    .sometimes(x => x.s("[hh ~] hh [~ hh] [~ hh]"))
    .color("white")
    ._punchcard()

// Vinyl crackle - coffeeshop essential
$vinyl: s("[rim:5 rim:5 rim:5 rim:5]*4")
    .gain(perlin.range(0.12, 0.2))
    .lpf(2500)
    .hpf(400)
    .color("brown")

// Warm piano chords - jazz voicings
$piano: note("<[c4,e4,g4,b4] [f4,a4,c5,e5] [d4,f4,a4,c5] [g4,b4,d5,f5]>")
    .s("triangle")  // Piano-like
    .lpf(sine.range(1800, 4000).slow(slider(8, 4, 16)))
    .decay(0.22)
    .room(slider(0.38, 0, 0.9))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.note("<[e4,g4,b4,d5] [a4,c5,e5,g5]>"))  // Chord variation
    .color("cyan")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Rhodes layer for warmth
$rhodes: note("<[g3,b3] ~ [a3,c4] ~ [b3,d4] ~ [g3,b3] ~>")
    .s("sine")
    .lpf(2000)
    .decay(0.18)
    .delay(0.1)
    .room(0.32)
    .gain(slider(0.25, 0, 0.9))
    .slow(slider(4.0, 1, 16))
    .color("yellow")

// Mellow bass
$bass: note("<c2 ~ f2 ~ d2 ~ g2 ~>")
    .s("triangle")
    .lpf(sine.range(240, 500).slow(slider(8, 4, 16)))
    .decay(slider(0.18, 0.08, 0.32))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.7, 0, 2))
    .rarely(x => x.note("<c2 [c2 d2] f2 [e2 f2] d2 [d2 e2] g2 [f2 g2]>"))  // Walking
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ f1 ~ d1 ~ g1 ~>")
    .s("sine")
    .lpf(75)
    .gain(slider(0.4, 0, 1.1))
    .color("darkred")

// Coffee shop ambient - chatter/cups texture
$ambient: s("[rim:5 rim:5]*8")
    .gain(perlin.range(0.06, 0.15))  // Variable
    .lpf(perlin.range(1200, 3500))
    .hpf(600)
    .pan(perlin.range(-0.5, 0.5))
    .room(0.4)
    .color("gray")
    .scope({ size: 256 })

// Ambient haze pad
$haze: note("[c3,g3]")
    .s("sawtooth")
    .lpf(sine.range(350, 900).slow(32))
    .attack(1.2)
    .release(1)
    .room(0.55)
    .gain(slider(0.15, 0, 0.5))
    .slow(8)
    .color("purple")
