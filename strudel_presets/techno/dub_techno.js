// @name Dub Techno
// @genre Techno
// @bpm 124
// @tags dub, echo, spacious, basic channel, chain reaction

setcpm(124 / 4)

// ═══════════════════════════════════════════════════════════════
// DUB TECHNO - Basic Channel/Chain Reaction style with endless echoes
// ═══════════════════════════════════════════════════════════════

// Muffled kick with subtle dynamics
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.0 0.95 0.98 0.95>")  // Subtle breathing
    .shape(slider(0.12, 0, 0.35))
    .lpf(slider(150, 60, 250))
    .rarely(x => x.s("[bd ~] bd bd bd"))  // Occasional skip
    .every(16, x => x.s("bd bd bd [~ bd] bd bd [bd bd] bd"))  // Sparse variation
    .color("orange")
    ._punchcard()

// Sparse shuffled hats swimming in delay
$hat: s("[~ hh] ~ [~ hh] ~").bank("RolandTR909")
    .gain(perlin.range(0.22, 0.35))  // Gentle velocity
    .delay(slider(0.35, 0, 0.7))
    .delaytime(0.375)  // Triplet delay for dub feel
    .room(slider(0.45, 0, 0.9))
    .pan(perlin.range(-0.3, 0.3).slow(0.5))  // Swimming stereo
    .sometimes(x => x.s("[~ hh] [hh ~] ~ ~"))  // Variation
    .every(8, x => x.s("[~ hh] ~ [hh ~] [~ oh]"))  // 8-bar fill
    ._punchcard()

// Rim with classic dub delay - essential character
$rim: s("~ rim ~ ~ ~ ~ rim ~").bank("RolandTR909")
    .gain(perlin.range(0.38, 0.52))  // Humanized velocity
    .delay(slider(0.5, 0, 0.9))
    .delaytime(0.333)  // Different delay rate for depth
    .room(slider(0.55, 0, 1))
    .sometimes(x => x.s("~ rim ~ ~ rim ~ ~ ~"))  // Pattern variation
    .rarely(x => x.s("[rim ~] rim ~ ~ ~ ~ rim [~ rim]"))  // Fill
    .color("white")
    ._punchcard()

// Ghost rim for texture depth
$rimghost: s("~ ~ [rim:3 ~] ~ ~ ~ ~ ~").bank("RolandTR909")
    .gain(0.18)
    .delay(0.6)
    .room(0.7)
    .lpf(3000)
    .color("gray")

// THE DUB CHORD - filtered, swimming forever in reverb
$chord: note("<[c3,g3,c4] ~ ~ ~ ~ ~ ~ ~ [a2,e3,a3] ~ ~ ~ ~ ~ ~ ~>")
    .s("sawtooth")
    .lpf(sine.range(350, 1800).slow(16))
    .attack(slider(0.1, 0.02, 0.3))
    .decay(slider(0.5, 0.2, 1))
    .delay(slider(0.55, 0, 0.9))
    .delaytime(0.375)
    .room(slider(0.65, 0, 1))
    .gain(slider(0.42, 0, 2))
    .slow(2)
    .rarely(x => x.note("<[d3,a3,d4] ~ ~ ~ ~ ~ ~ ~>"))  // Chord variation
    .color("cyan")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Chord layer for thickness - slightly detuned
$chord2: note("<[c3,g3,c4] ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~>")
    .s("triangle")
    .lpf(sine.range(400, 1200).slow(24))
    .attack(0.15)
    .decay(0.8)
    .delay(0.45)
    .room(0.5)
    .gain(0.2)
    .slow(2)
    .color("purple")

// Deep sub bass - round sine with weight
$bass: note("<c1 ~ ~ ~ c1 ~ ~ ~ a0 ~ ~ ~ c1 ~ ~ ~>")
    .s("sine")
    .lpf(slider(180, 60, 300))
    .decay(slider(0.25, 0.1, 0.5))
    .gain(slider(0.75, 0, 2))
    .rarely(x => x.note("<c1 ~ g0 ~ c1 ~ ~ ~>"))  // Occasional movement
    .scope({ size: 256 })
    .color("red")

// Dub stab - sparse, echoing into infinity
$stab: note("<g4 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~>")
    .s("sine")
    .lpf(sine.range(1000, 3500).slow(8))
    .delay(slider(0.6, 0, 0.95))
    .delaytime(0.5)  // Half note delay
    .room(slider(0.7, 0, 1))
    .gain(slider(0.25, 0, 1))
    .slow(4)
    .rarely(x => x.note("<e4 ~ ~ ~ ~ ~ ~ ~>").fast(2))  // Answer stab
    .color("yellow")
    ._punchcard()

// Background texture - filtered noise atmosphere
$texture: s("noise")
    .lpf(sine.range(200, 800).slow(32))
    .gain(perlin.range(0.04, 0.12))  // Breathing texture
    .room(slider(0.6, 0, 1))
    .color("purple")
    .scope({ size: 256 })

// Sparse crash swells for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh:3")
    .bank("RolandTR909")
    .gain(0.35)
    .room(0.8)
    .delay(0.5)
    .slow(4)
