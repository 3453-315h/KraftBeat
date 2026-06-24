// @name Chillhop
// @genre Lo-Fi
// @bpm 80
// @tags chill, jazzy, summer, relaxing

setcpm(80 / 4)

// ═══════════════════════════════════════════════════════════════
// CHILLHOP - Jazzy lo-fi beats with warm textures
// ═══════════════════════════════════════════════════════════════

// Dusty kick with swing
$kick: s("bd ~ [~ bd] ~").bank("SP1200")
    .gain("<0.9 0.85 0.88 0.85>")  // Soft dynamics
    .lpf(300)  // Lo-fi roll-off
    .nudge("<0 0 0.03 0>")  // Swing
    .every(8, x => x.s("bd ~ [bd ~] ~ [~ bd] ~ bd ~"))  // Variation
    .color("orange")
    ._punchcard()

// Swung snare with ghost layers
$snare: stack(
    s("~ sd ~ sd").gain(slider(0.72, 0, 2)).room(0.4).lpf(4500),  // Lo-fi snare
    s("~ ~ [sd:3 ~] [~ sd:3]").gain(0.22).lpf(3500)  // Ghosts
).bank("SP1200")
    .n(1.0)
    .nudge("0 0.015 0 0.02")  // Swing
    .every(8, x => x.s("~ sd ~ [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Swung hats with lo-fi filter
$hat: s("[~ hh] hh [~ hh] [hh hh]").bank("SP1200")
    .gain(perlin.range(0.28, 0.42))  // Soft humanized
    .lpf(perlin.range(3500, 7000))  // Lo-fi filter
    .nudge(perlin.range(-0.02, 0.04))  // Swing timing
    .pan(perlin.range(-0.15, 0.15).slow(0.5))
    .sometimes(x => x.s("[hh ~] hh [~ hh] [~ hh]"))  // Variation
    .every(8, x => x.s("[hh hh] [~ hh] [hh hh hh hh] [oh hh]"))  // Fill
    .color("white")
    ._punchcard()

// Vinyl crackle texture - essential lo-fi
$vinyl: s("[rim:5 rim:5 rim:5 rim:5]*4")
    .gain(slider(0.18, 0, 0.5))
    .lpf(3000)
    .hpf(400)
    .color("brown")

// Lo-fi jazz piano with warm filter
$piano: note("<[c4,e4,g4,b4] [d4,f4,a4,c5] [e4,g4,b4,d5] [d4,f4,a4,c5]>")
    .s("triangle")  // Piano-like
    .lpf(sine.range(1800, 4000).slow(slider(8, 4, 16)))
    .decay(0.22)
    .room(slider(0.35, 0, 0.9))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.note("<[e4,g4,b4,d5] [f4,a4,c5,e5]>"))  // Variation
    .color("cyan")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Rhodes layer for warmth
$rhodes: note("<[g3,b3] ~ [a3,c4] ~ [b3,d4] ~ [g3,b3] ~>")
    .s("sine")
    .lpf(2200)
    .decay(0.2)
    .delay(0.12)
    .room(0.3)
    .gain(slider(0.28, 0, 1))
    .slow(slider(4.0, 1, 16))
    .color("yellow")

// Warm bass with lo-fi character
$bass: note("<c2 ~ [c2 ~] ~ d2 ~ [e2 d2] ~>")
    .s("triangle")
    .lpf(sine.range(280, 550).slow(slider(4.0, 1, 16)))
    .decay(slider(0.18, 0.08, 0.35))
    .gain(slider(0.72, 0, 2))
    .rarely(x => x.note("<c2 d2 [e2 d2] c2>"))  // Walking variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ c1 ~ d1 ~ e1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.42, 0, 1.2))
    .color("darkred")

// Ambient haze layer
$haze: note("[c3,g3]")
    .s("sawtooth")
    .lpf(sine.range(350, 900).slow(32))
    .attack(1.2)
    .release(1)
    .room(0.55)
    .gain(slider(0.15, 0, 0.5))
    .slow(8)
    .color("purple")
    .scope({ size: 256 })
