// @name Ocean
// @genre Ambient
// @bpm 40
// @tags ocean, waves, peaceful, underwater

setcpm(40 / 4)

// ═══════════════════════════════════════════════════════════════
// OCEAN - Deep underwater atmosphere with waves
// ═══════════════════════════════════════════════════════════════

// Wave-like noise - rhythmic swells
$waves: s("noise:0")
    .loop()
    .lpf(sine.range(300, 2500).slow(slider(8, 4, 16)))
    .hpf(150)
    .attack(slider(1.5, 0.6, 3))
    .release(slider(2, 0.8, 4))
    .slow(slider(8, 4, 16))
    .gain(sine.range(0.2, 0.55).slow(8))  // Swell dynamics
    .color("orange")
    .scope({ size: 256 })
    ._punchcard()

// Second wave layer - crashing
$crash: s("noise:0")
    .loop()
    .lpf(sine.range(800, 4000).slow(4))
    .hpf(400)
    .gain(sine.range(0.08, 0.35).slow(4))  // Faster swell
    .slow(slider(8, 4, 16))
    .color("white")

// Deep ocean drone - foundation
$deep: note("<c1 d1 c1 b0>")
    .s("sine")
    .lpf(sine.range(60, 200).slow(slider(24, 8, 48)))
    .attack(slider(2, 1, 4))
    .release(slider(2.5, 1, 5))
    .slow(slider(8, 4, 16))
    .gain(slider(0.48, 0, 1.5))
    .color("cyan")
    .pianoroll({ fold: 1 })

// Second deep layer
$deep2: note("g0")
    .s("sine")
    .lpf(80)
    .attack(2.5)
    .release(3)
    .gain(slider(0.32, 0, 1.1))
    .slow(16)
    .color("darkred")

// Surface shimmer - random high notes
$shimmer: n(choose(60, 64, 67, 72, 76, 79))
    .s("sine")
    .struct("x(2,16)")
    .attack(slider(0.1, 0.04, 0.25))
    .decay(0.6)
    .room(slider(0.55, 0, 1))
    .delay(slider(0.35, 0.1, 0.7))
    .delaytime(0.5)
    .slow(slider(8, 4, 16))
    .pan(perlin.range(-0.5, 0.5))  // Wide random stereo
    .gain(slider(0.28, 0, 1.1))
    .sometimes(x => x.struct("x(3,16)"))  // More shimmer
    .color("yellow")

// High sparkle layer
$sparkle: n(choose(79, 84, 88, 91))
    .s("sine")
    .struct("x(1,16)")
    .decay(0.5)
    .delay(0.4)
    .room(0.5)
    .pan(perlin.range(-0.6, 0.6))
    .gain(slider(0.18, 0, 0.7))
    .slow(16)
    .color("lime")

// Whale song - slow melodic movements
$whale: note("<c3 ~ ~ ~ e3 ~ ~ ~ g3 ~ ~ ~ e3 ~ ~ ~>")
    .s("triangle")
    .lpf(sine.range(400, 1500).slow(slider(16, 8, 32)))
    .speed(sine.range(0.98, 1.02).slow(4))  // Pitch wobble
    .attack(slider(0.3, 0.1, 0.7))
    .decay(slider(1.2, 0.5, 2.5))
    .slow(slider(8, 4, 16))
    .room(slider(0.55, 0, 1))
    .delay(0.2)
    .gain(slider(0.42, 0, 1.5))
    .sometimes(x => x.note("<e3 g3 c4 g3 e3>"))  // Variation
    .color("purple")
    .scope({ size: 256 })

// Second whale layer - lower
$whale2: note("<~ ~ ~ ~ c2 ~ ~ ~ ~ ~ ~ ~ g2 ~ ~ ~>")
    .s("triangle")
    .lpf(600)
    .attack(0.4)
    .decay(1.5)
    .room(0.5)
    .gain(slider(0.28, 0, 1))
    .slow(8)
    .color("magenta")

// Underwater bubbles - sparse random
$bubbles: n(choose(72, 79, 84, 88))
    .s("sine")
    .struct("x(1,16)")
    .attack(0.01)
    .decay(0.3)
    .delay(0.2)
    .pan(perlin.range(-0.4, 0.4))
    .gain(slider(0.18, 0, 0.6))
    .slow(16)
    .sometimes(x => x.struct("x(2,16)"))
    .color("orange")
