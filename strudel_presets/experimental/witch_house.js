// @name Witch House
// @genre Experimental
// @bpm 110
// @tags witch, dark, occult, slowed

setcpm(110 / 4)

// ═══════════════════════════════════════════════════════════════
// WITCH HOUSE - Dark, slowed-down electronic with occult vibes
// ═══════════════════════════════════════════════════════════════

// Heavy slowed kick
$kick: s("bd ~ bd ~").bank("RolandTR808")
    .gain("<0.98 1.05 1.0 1.08>")  // Dark dynamics
    .lpf(350)  // Dark roll-off
    .shape(slider(0.35, 0, 0.7))  // Slight distortion
    .every(8, x => x.s("bd ~ [bd ~] ~ [~ bd] ~ bd ~"))  // Variation
    .color("red")
    ._punchcard()

// Clap with big reverb
$clap: s("~ cp ~ cp").bank("RolandTR808")
    .gain(slider(0.72, 0, 2))
    .room(slider(0.55, 0, 1))  // Huge reverb
    .delay(0.2)
    .delaytime(0.5)
    .every(8, x => x.s("~ cp ~ [cp cp cp cp]"))  // Fill
    .color("purple")
    ._punchcard()

// Sparse offbeat hats
$hat: s("[hh ~] [~ hh] [hh ~] hh").bank("RolandTR808")
    .gain(perlin.range(0.32, 0.48))  // Velocity
    .lpf(perlin.range(4000, 8000))
    .sometimes(x => x.s("[~ hh] [hh ~] [~ hh] [~ hh]"))  // Variation
    .color("white")
    ._punchcard()

// Dark chopped vocal sample
$vocal: s("vocal:*")
    .n(irand(8))
    .chop(choose(4, 8, 16))
    .speed(slider(0.7, 0.4, 1.0))  // Slowed down
    .lpf(sine.range(500, 3000).slow(slider(8, 4, 16)))
    .room(slider(0.45, 0, 1))
    .delay(0.3)
    .delaytime(0.666)
    .struct("~ x ~ ~")
    .gain(slider(0.48, 0, 1.8))
    .pan(perlin.range(-0.3, 0.3))
    .sometimes(x => x.speed(choose(-0.5, -0.7)))  // Reversed
    .sometimes(x => x.struct("x ~ ~ ~"))  // Different position
    .color("orange")

// Occult synth - dark minor chords
$synth: note("<c3 ~ d#3 ~ c3 ~ g2 ~>")
    .s("sawtooth")
    .lpf(sine.range(400, 1800).slow(slider(16, 8, 32)))
    .lpq(sine.range(2, 6).slow(16))  // Dark resonance
    .attack(slider(0.15, 0.05, 0.35))
    .release(slider(0.5, 0.2, 1))
    .room(slider(0.48, 0, 1))
    .gain(slider(0.52, 0, 2))
    .sometimes(x => x.note("<d#3 ~ f3 ~ d#3 ~ g#2 ~>"))  // Variation
    .color("magenta")
    ._punchcard()
    .pianoroll({ fold: 1 })
    .scope({ size: 256 })

// Second synth layer - more dissonant
$synth2: note("<~ ~ ~ ~ g#3 ~ ~ ~ ~ ~ ~ ~ c4 ~ ~ ~>")
    .s("square")
    .lpf(1800)
    .decay(0.5)
    .delay(0.35)
    .room(0.5)
    .gain(slider(0.28, 0, 1))
    .slow(2)
    .color("cyan")

// Sub bass - heavy foundation
$sub: note("<c1 ~ c1 ~ c1 ~ [c1 d#1] ~>")
    .s("sine")
    .lpf(80)
    .decay(slider(0.25, 0.1, 0.5))
    .gain(slider(0.55, 0, 1.8))
    .scope({ size: 256 })
    .color("darkred")
    ._punchcard()

// Second sub layer
$sub2: note("<c0 ~ ~ ~ ~ ~ ~ ~>")
    .s("sine")
    .lpf(50)
    .gain(slider(0.38, 0, 1.2))
    .slow(2)
    .color("black")

// Noise texture
$noise: s("noise:0")
    .struct("x(2,16)")
    .lpf(sine.range(500, 2000).slow(16))
    .hpf(300)
    .gain(slider(0.18, 0, 0.6))
    .room(0.5)
    .delay(0.3)
    .slow(8)
    .color("gray")

// Dark ambient pad
$dark: note("[c2,g2,c3]")
    .s("sawtooth")
    .lpf(sine.range(250, 700).slow(32))
    .attack(1.5)
    .release(2)
    .room(0.6)
    .gain(slider(0.22, 0, 0.8))
    .slow(8)
    .color("purple")
