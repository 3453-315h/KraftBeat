// @name Deep Groove
// @genre House
// @bpm 120
// @tags bass, warm, groove, deep

setcpm(120 / 4)

// ═══════════════════════════════════════════════════════════════
// DEEP GROOVE - Warm basslines and lush chords
// ═══════════════════════════════════════════════════════════════

// Deep 909 kick with subtle breathing
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.0 0.95 0.98 0.95> <0.95 0.98 1.0 0.95>")  // Breathing dynamics
    .shape(slider(0.3, 0, 1))
    .lpf(slider(250, 100, 400))  // Deep kick
    .rarely(x => x.s("[bd bd:1] bd bd bd"))  // Ghost kick
    .every(16, x => x.s("bd bd [~ bd] bd bd bd [bd bd] bd"))  // Sparse variation
    .color("orange")
    ._punchcard()

// Shuffled offbeat hats with groove
$hat: s("[~ hh]*4").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.5))  // Humanized velocity
    .nudge(perlin.range(-0.01, 0.02))  // Micro-timing
    .pan(perlin.range(-0.2, 0.2).slow(0.5))  // Stereo sway
    .sometimes(x => x.s("[~ hh] [hh ~] [~ hh] [~ oh]"))  // Pattern variation
    .every(8, x => x.s("[hh ~] [~ hh] [hh hh] [~ oh]"))  // Fill
    ._punchcard()

// Deep clap with warm reverb
$clap: stack(
    s("~ cp ~ cp").gain(slider(0.8, 0, 2)).room(0.35),
    s("~ ~ [~ cp:3] ~").gain(0.2).lpf(4000)  // Ghost clap
).bank("RolandTR909")
    .delay(slider(0.2, 0, 1))
    .every(8, x => x.s("~ cp ~ [cp cp:3 cp cp]"))  // Fill
    .color("yellow")
    ._punchcard()

// Shaker texture with feel
$shaker: s("shaker*16")
    .gain(perlin.range(0.15, 0.25))
    .pan(perlin.range(-0.35, 0.35).slow(0.25))
    .lpf(perlin.range(3500, 7000))
    .euclid(5, 8)  // Polyrhythmic feel
    .color("gray")

// Deep rolling bass with filter movement
$bass: note("<c2 ~ [c2 ~] ~ g2 ~ [f2 ~] ~>")
    .s("sawtooth")
    .lpf(sine.range(250, 650).slow(slider(4.0, 1, 16)))
    .decay(slider(0.18, 0.08, 0.35))
    .gain(slider(0.8, 0, 2))
    .rarely(x => x.note("<c2 c2 [c2 d2] ~ g2 ~ [f2 g2] ~>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ c1 ~ g1 ~ f1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.45, 0, 1.2))
    .color("darkred")

// Warm pad stab with movement
$pad: note("<[c4,e4,g4] ~ ~ ~ [f4,a4,c5] ~ ~ ~>")
    .s("triangle")
    .attack(slider(0.1, 0.02, 0.3))
    .release(slider(0.4, 0.15, 0.8))
    .lpf(sine.range(1500, 3500).slow(slider(8.0, 1, 16)))
    .room(slider(0.4, 0, 1))
    .gain(slider(0.55, 0, 2))
    .jux(x => x.lpf(2000))  // Stereo warmth
    .sometimes(x => x.note("<[d4,f4,a4] ~ ~ ~>"))  // Chord variation
    .color("purple")
    .scope({ size: 256 })

// Rim for texture
$rim: s("~ ~ ~ ~ rim ~ ~ ~").bank("RolandTR909")
    .gain(slider(0.35, 0, 1.2))
    .delay(0.15)
    .room(0.2)
    .sometimes(x => x.s("~ ~ rim ~ ~ ~ ~ rim"))  // Answer pattern
    .color("brown")
    ._punchcard()

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh:3")
    .bank("RolandTR909")
    .gain(0.35)
    .room(0.45)
    .slow(2)
