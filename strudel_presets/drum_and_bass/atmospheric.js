// @name Atmospheric
// @genre Drum and Bass
// @bpm 168
// @tags atmospheric, cinematic, dark, lush

setcpm(168 / 4)

// ═══════════════════════════════════════════════════════════════
// ATMOSPHERIC DnB - Cinematic pads with lush textures
// ═══════════════════════════════════════════════════════════════

// Deep atmospheric kick with dynamics
$kick: s("bd ~ ~ ~ bd ~ ~ ~").bank("RolandTR909")
    .gain("<1.0 0.95 0.98 0.92> <0.95 0.98 1.0 0.95>")  // Smooth dynamics
    .shape(slider(0.25, 0, 0.5))
    .lpf(300)  // Warm kick
    .every(16, x => x.s("bd ~ ~ ~ bd ~ [~ bd] ~"))  // Variation
    .color("orange")
    ._punchcard()

// Snare with space
$snare: stack(
    s("~ ~ sd ~ ~ ~ sd ~").gain(slider(0.85, 0, 2)).room(0.45),  // Big reverb
    s("~ ~ ~ [sd:3 ~] ~ ~ ~ [~ sd:3]").gain(0.22).lpf(4500)  // Ghosts
).bank("RolandTR909")
    .every(8, x => x.s("~ ~ sd ~ ~ ~ sd [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Soft rolling hats with stereo movement
$hat: s("[~ hh] [~ hh] [hh ~] [~ hh]").bank("RolandTR909")
    .gain(perlin.range(0.28, 0.42))  // Soft humanized
    .pan(sine.range(-0.35, 0.35).slow(4))  // Slow stereo sweep
    .lpf(perlin.range(5000, 10000))
    .sometimes(x => x.s("hh*8").gain(0.35))  // 8th note layer
    .every(8, x => x.fast(1.5).gain(0.38))  // Triplet build
    .color("white")
    ._punchcard()

// Ride for atmosphere
$ride: s("~ ~ ~ rd ~ ~ ~ ~").bank("RolandTR909")
    .gain(slider(0.35, 0, 1.2))
    .room(0.35)
    .delay(0.2)
    .sometimes(x => x.s("rd*8").gain(0.25))  // Ride layer
    .color("gray")

// Atmospheric pad - lush and evolving
$pad: note("<[c3,d#3,g3] [c3,d#3,g3] [a#2,d3,f3] [g#2,c3,d#3]>")
    .s("sawtooth")
    .lpf(sine.range(600, 2500).slow(slider(8.0, 1, 16)))
    .attack(slider(0.6, 0.2, 1.2))
    .release(slider(0.8, 0.3, 1.5))
    .room(slider(0.55, 0, 1))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.52, 0, 2))
    .sometimes(x => x.note("<[d3,f3,a3] [c3,e3,g3]>"))  // Chord variation
    .color("purple")
    ._punchcard()
    .pianoroll({ fold: 1 })
    .scope({ size: 256 })

// Second pad layer for thickness
$pad2: note("<[g3,c4] [f3,a#3] [d#3,g3] [c3,d#3]>")
    .s("triangle")
    .lpf(2000)
    .attack(0.8)
    .release(1)
    .room(0.5)
    .gain(slider(0.25, 0, 0.9))
    .slow(slider(4.0, 1, 16))
    .color("cyan")

// Reese bass with movement
$bass: note("<c1 ~ c1 ~ d#1 ~ [d#1 c1] ~>")
    .s("sawtooth")
    .lpf(sine.range(250, 700).slow(slider(4.0, 1, 16)))
    .lpq(sine.range(1, 4).slow(8))  // Gentle resonance
    .detune(0.4)  // Reese detune
    .decay(slider(0.18, 0.08, 0.35))
    .gain(slider(0.78, 0, 2))
    .rarely(x => x.note("<c1 d1 [d#1 d1] c1>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ c1 ~ d#1 ~ d#1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.5, 0, 1.3))
    .color("darkred")

// Cinematic strings layer
$strings: note("[c4,g4,c5]")
    .s("sawtooth")
    .lpf(sine.range(800, 2000).slow(slider(8.0, 1, 16)))
    .attack(slider(0.6, 0.25, 1.2))
    .release(slider(0.7, 0.3, 1.3))
    .struct("x ~ ~ ~ ~ ~ ~ ~")
    .slow(slider(4.0, 1, 16))
    .room(slider(0.5, 0, 1))
    .gain(slider(0.4, 0, 1.5))
    .sometimes(x => x.note("[d4,a4,d5]"))  // Variation
    .color("cyan")
    ._punchcard()
    .scope({ size: 256 })

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.4)
    .room(0.55)
    .delay(0.2)
    .slow(2)
