// @name Meditation
// @genre Ambient
// @bpm 45
// @tags meditation, healing, calm, tibetan

setcpm(45 / 4)

// ═══════════════════════════════════════════════════════════════
// MEDITATION - Tibetan bowls and healing frequencies
// ═══════════════════════════════════════════════════════════════

// Tibetan bowl 1 - C fundamental with natural decay
$bowl1: note("c4")
    .s("sine")
    .attack(slider(0.08, 0.02, 0.2))
    .decay(slider(2.5, 1.5, 4))
    .struct("x ~ ~ ~ ~ ~ ~ ~")
    .slow(slider(8, 4, 16))
    .room(slider(0.55, 0, 1))
    .delay(0.15)
    .delaytime(0.666)
    .gain(slider(0.52, 0, 1.8))
    .sometimes(x => x.struct("x ~ ~ ~ x ~ ~ ~"))  // Two strikes
    .color("cyan")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Tibetan bowl 2 - G perfect fifth harmony
$bowl2: note("g4")
    .s("sine")
    .attack(slider(0.08, 0.02, 0.2))
    .decay(slider(2.8, 1.5, 4.5))
    .struct("~ ~ ~ ~ x ~ ~ ~")
    .slow(slider(8, 4, 16))
    .room(slider(0.55, 0, 1))
    .delay(0.12)
    .gain(slider(0.48, 0, 1.5))
    .sometimes(x => x.struct("~ ~ x ~ x ~ ~ ~"))  // Variation
    .color("cyan")
    ._punchcard()

// Bowl harmonic overtones
$overtones: note("<c5 e5 g5 c6>")
    .s("sine")
    .struct("x(2,16)")
    .attack(0.03)
    .decay(1.5)
    .room(0.5)
    .delay(0.2)
    .gain(slider(0.22, 0, 0.8))
    .slow(16)
    .pan(perlin.range(-0.3, 0.3))
    .color("yellow")

// Healing drone - Sa-Pa relationship
$drone: note("<c2 g2>")
    .s("triangle")
    .lpf(sine.range(250, 700).slow(slider(24, 8, 48)))
    .attack(slider(1.5, 0.6, 3))
    .release(slider(2, 0.8, 4))
    .slow(slider(8, 4, 16))
    .gain(slider(0.45, 0, 1.5))
    .room(0.5)
    .color("cyan")
    .scope({ size: 256 })

// Second drone layer for richness
$drone2: note("c1")
    .s("sine")
    .lpf(80)
    .attack(2)
    .release(2.5)
    .gain(slider(0.38, 0, 1.2))
    .slow(16)
    .color("darkred")

// Soft wind chimes - sparse random notes
$chimes: n(choose(60, 64, 67, 72, 76))
    .s("sine")
    .attack(slider(0.02, 0.01, 0.08))
    .decay(slider(1.2, 0.6, 2))
    .struct("x(2,16)")
    .slow(slider(8, 4, 16))
    .room(slider(0.55, 0, 1))
    .delay(0.25)
    .delaytime(0.5)
    .pan(perlin.range(-0.5, 0.5))  // Wide random stereo
    .gain(slider(0.32, 0, 1.2))
    .sometimes(x => x.struct("x(3,16)"))  // More chimes
    .color("orange")
    ._punchcard()

// High bell tone - rare accent
$bell: note("c6")
    .s("sine")
    .struct("x ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
    .decay(2)
    .room(0.6)
    .delay(0.3)
    .gain(slider(0.18, 0, 0.6))
    .slow(32)
    .color("lime")

// Breath-like pad for meditation flow
$breath: note("[c3,g3,c4]")
    .s("sawtooth")
    .lpf(sine.range(300, 900).slow(32))
    .attack(2)
    .release(2.5)
    .room(0.6)
    .gain(slider(0.18, 0, 0.6))
    .slow(16)
    .color("purple")
    .scope({ size: 256 })
