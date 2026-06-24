// @name Cloud Rap
// @genre Hip Hop
// @bpm 70
// @tags cloud, airy, dreamy, spacey

setcpm(70 / 4)

// ═══════════════════════════════════════════════════════════════
// CLOUD RAP - Airy atmospheres and dreamy vibes
// ═══════════════════════════════════════════════════════════════

// Soft 808 kick with dreamy feel
$kick: s("bd ~ [~ bd] ~").bank("RolandTR808")
    .gain("<0.92 0.88 0.9 0.85> <0.88 0.9 0.92 0.88>")  // Soft dynamics
    .lpf(300)  // Soft attack
    .shape(slider(0.3, 0, 0.6))
    .every(8, x => x.s("bd ~ [bd ~] ~ [~ bd] ~ bd ~"))  // Variation
    .color("orange")
    ._punchcard()

// Dreamy snare with big reverb
$snare: stack(
    s("~ sd ~ sd").gain(slider(0.72, 0, 2)).room(0.6),  // Big reverb
    s("~ ~ [sd:3 ~] ~").gain(0.18).lpf(3500)  // Ghost
).bank("RolandTR808")
    .every(8, x => x.s("~ sd ~ [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Swung hats with cloud feel
$hat: s("[~ hh] hh [~ hh] [hh hh]").bank("RolandTR808")
    .gain(perlin.range(0.28, 0.42))  // Soft humanized
    .lpf(perlin.range(4000, 8000))  // Soft tonal
    .pan(perlin.range(-0.2, 0.2).slow(0.5))
    .sometimes(x => x.s("[hh ~] hh [~ hh] [~ hh]"))  // Variation
    .every(8, x => x.s("[hh hh] [~ hh] [hh hh hh hh] [oh hh]"))  // Fill
    .color("white")
    ._punchcard()

// Open hat atmosphere
$oh: s("~ ~ ~ ~ ~ ~ oh ~").bank("RolandTR808")
    .gain(slider(0.35, 0, 1.2))
    .room(0.5)
    .delay(0.3)
    .color("lime")

// Airy pad with long attack - the cloud
$pad: note("<[c4,e4,g4,b4] [c4,e4,g4,b4] [a3,c4,e4,g4] [g3,b3,d4,f4]>")
    .s("sawtooth")
    .lpf(sine.range(1000, 3500).slow(slider(8.0, 1, 16)))
    .attack(slider(0.6, 0.2, 1.2))
    .release(slider(0.8, 0.3, 1.5))
    .room(slider(0.55, 0, 1))
    .delay(slider(0.25, 0, 0.6))
    .delaytime(0.375)
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.52, 0, 2))
    .sometimes(x => x.note("<[d4,f4,a4,c5]>"))  // Chord variation
    .color("purple")
    ._punchcard()
    .pianoroll({ fold: 1 })
    .scope({ size: 256 })

// Second pad layer for thickness
$pad2: note("<[g3,b3,d4] [a3,c4,e4]>")
    .s("triangle")
    .lpf(2000)
    .attack(0.8)
    .release(1)
    .room(0.5)
    .gain(slider(0.25, 0, 0.9))
    .slow(slider(4.0, 1, 16))
    .color("cyan")

// Dreamy bass with soft attack
$bass: note("<c2 ~ c2 ~ a1 ~ g1 ~>")
    .s("triangle")
    .lpf(sine.range(250, 500).slow(slider(4.0, 1, 16)))
    .decay(slider(0.25, 0.1, 0.5))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.68, 0, 2))
    .rarely(x => x.note("<c2 d2 [e2 d2] c2>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ c1 ~ a0 ~ g0 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.42, 0, 1.2))
    .slow(slider(4.0, 1, 16))
    .color("darkred")

// Sparkle - high register random notes
$sparkle: n(choose(72, 76, 79, 84))
    .s("sine")
    .struct("x(3,16)")
    .attack(slider(0.15, 0.05, 0.4))
    .decay(0.3)
    .room(slider(0.5, 0, 1))
    .delay(slider(0.35, 0, 0.7))
    .delaytime(0.5)
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.35, 0, 1.5))
    .pan(perlin.range(-0.5, 0.5))  // Wide stereo
    .color("yellow")

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR808")
    .gain(0.35)
    .room(0.6)
    .delay(0.3)
    .slow(2)
