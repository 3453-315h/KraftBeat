// @name Wobble Bass
// @genre Dubstep
// @bpm 140
// @tags wobble, heavy, bass, classic

setcpm(140 / 4)

// ═══════════════════════════════════════════════════════════════
// WOBBLE BASS - Classic dubstep with LFO-modulated bass
// ═══════════════════════════════════════════════════════════════

// Half-time kick with dynamics
$kick: s("bd ~ ~ ~ ~ ~ ~ ~ bd ~ ~ ~ ~ ~ ~ ~").bank("RolandTR808")
    .gain("<1.2 1.15 1.18 1.12> <1.15 1.12 1.2 [1.25 1.15]>")  // Dynamics
    .shape(slider(0.35, 0, 0.7))
    .every(8, x => x.s("bd ~ ~ bd ~ ~ ~ ~ bd ~ ~ ~ ~ ~ bd ~"))  // Variation
    .every(16, x => x.s("bd ~ bd ~ ~ ~ ~ ~ bd ~ bd ~ ~ ~ [bd bd] bd"))  // Build
    .color("orange")
    ._punchcard()

// Heavy snare on 3 with ghost layers
$snare: stack(
    s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ sd ~ ~ ~").gain(slider(1.1, 0, 2)).room(slider(0.2, 0, 0.6)),
    s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ [sd:3 ~] ~ ~").gain(0.3).lpf(5000)  // Ghost
).bank("RolandTR808")
    .every(8, x => x.s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ sd ~ [sd sd] sd"))  // Fill
    .every(16, x => x.s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ sd [sd sd] [sd*4] [sd*8]"))  // Build
    ._punchcard()

// Rolling hats with movement
$hat: s("hh*16").bank("RolandTR808")
    .gain(perlin.range(0.32, 0.48))  // Humanized
    .pan(perlin.range(-0.12, 0.12).slow(0.25))
    .lpf(perlin.range(5000, 10000))
    .sometimes(x => x.s("[hh*4] [hh hh oh hh] [hh*4] [hh hh hh oh]"))  // Accents
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh*16]"))  // Build
    ._punchcard()

// CLASSIC WOBBLE BASS - the signature sound
$wobble: note("<c1 c1 [c1 d#1] c1 f1 f1 [d#1 c1] c1>")
    .s("sawtooth")
    .lpf(sine.range(200, 2500).fast(slider(4.0, 1, 16)))  // Wobble rate
    .lpq(sine.range(4, 12).slow(2))  // Resonance movement
    .decay(slider(0.12, 0.04, 0.25))
    .gain(slider(0.85, 0, 2))
    .chop(sine.range(4, 16).slow(4))  // Additional modulation
    .rarely(x => x.note("<c1 d#1 [f1 d#1] c1>"))  // Variation
    .every(8, x => x.lpf(sine.range(300, 4000).fast(8)))  // Faster wobble
    .color("cyan")
    ._punchcard()
    .pianoroll({ fold: 1 })
    .scope({ size: 256 })

// Mid bass layer for thickness
$midbass: note("<c2 ~ [c2 d#2] ~ f2 ~ [d#2 c2] ~>")
    .s("square")
    .lpf(sine.range(500, 1500).fast(4))
    .lpq(6)
    .decay(0.1)
    .gain(slider(0.4, 0, 1.3))
    .color("orange")

// Sub bass underneath - foundation
$sub: note("<c1 ~ ~ ~ f1 ~ ~ ~>")
    .s("sine")
    .lpf(80)
    .decay(slider(0.2, 0.1, 0.4))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.6, 0, 2))
    .scope({ size: 256 })
    .color("darkred")
    ._punchcard()

// Dark pad for atmosphere
$pad: note("[c3,d#3,g3]")
    .s("sawtooth")
    .lpf(sine.range(400, 1200).slow(16))
    .attack(0.6)
    .release(0.8)
    .room(0.5)
    .gain(slider(0.25, 0, 0.8))
    .slow(8)
    .color("purple")
    .scope({ size: 256 })

// Crash for drops
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR808")
    .gain(0.55)
    .room(0.45)
    .slow(2)
