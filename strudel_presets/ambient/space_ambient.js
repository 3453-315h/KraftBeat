// @name Space Ambient
// @genre Ambient
// @bpm 50
// @tags space, cosmic, vast, interstellar

setcpm(50 / 4)

// ═══════════════════════════════════════════════════════════════
// SPACE AMBIENT - Cosmic drifting with vast textures
// ═══════════════════════════════════════════════════════════════

// Cosmic pad layer 1 - deep evolving harmonics
$pad1: note("<c3 e3 g3 b3>")
    .s("sawtooth")
    .lpf(sine.range(500, 2500).slow(slider(16, 4, 32)))
    .lpq(sine.range(0.5, 2).slow(24))  // Gentle resonance sweep
    .attack(slider(1.5, 0.5, 3))
    .release(slider(2, 0.8, 4))
    .room(slider(0.6, 0, 1))
    .delay(0.2)
    .delaytime(0.666)  // Dotted delay
    .slow(slider(8, 4, 16))
    .gain(slider(0.48, 0, 1.8))
    .sometimes(x => x.note("<d3 f3 a3 c4>"))  // Dm7 variation
    .color("purple")
    .pianoroll({ fold: 1 })
    .scope({ size: 256 })

// Cosmic pad layer 2 - ethereal harmonies
$pad2: note("<g3 b3 d4 f#4>")
    .s("triangle")
    .lpf(sine.range(600, 3000).slow(slider(20, 8, 32)))
    .attack(slider(1.8, 0.6, 3.5))
    .release(slider(2.2, 0.9, 4.5))
    .room(slider(0.55, 0, 1))
    .slow(slider(8, 4, 16))
    .delay(slider(0.25, 0, 0.6))
    .delaytime(0.5)
    .gain(slider(0.42, 0, 1.5))
    .pan(sine.range(-0.3, 0.3).slow(16))  // Slow stereo drift
    .sometimes(x => x.note("<a3 c4 e4 g4>"))  // Variation
    .color("purple")
    .scope({ size: 256 })

// Third pad layer for depth
$pad3: note("<e2 ~ ~ ~ b2 ~ ~ ~>")
    .s("sawtooth")
    .lpf(sine.range(300, 1000).slow(32))
    .attack(2)
    .release(2.5)
    .room(0.6)
    .gain(slider(0.28, 0, 0.9))
    .slow(16)
    .color("cyan")

// Deep sub drone - cosmic foundation
$sub: note("c1")
    .s("sine")
    .lpf(80)
    .attack(slider(2, 1, 4))
    .release(slider(2.5, 1, 5))
    .slow(slider(8, 4, 16))
    .gain(slider(0.45, 0, 1.5))
    .scope({ size: 256 })
    .color("darkred")

// Fifth drone layer
$drone5: note("g0")
    .s("sine")
    .lpf(60)
    .attack(2.5)
    .release(3)
    .gain(slider(0.28, 0, 1))
    .slow(16)
    .color("red")

// Sparkling stars - random high notes
$stars: n(choose(12, 14, 16, 19, 21, 24))
    .scale("c:major")
    .s("sine")
    .attack(slider(0.15, 0.05, 0.4))
    .decay(0.5)
    .struct("x(3,16)")
    .slow(slider(8, 4, 16))
    .room(slider(0.55, 0, 1))
    .delay(slider(0.35, 0.1, 0.7))
    .delaytime(0.666)  // Dotted delay
    .gain(slider(0.28, 0, 1.2))
    .pan(perlin.range(-0.6, 0.6))  // Wide random stereo
    .sometimes(x => x.struct("x(5,16)"))  // More stars
    .rarely(x => x.struct("x(2,8)"))  // Denser
    .color("yellow")
    ._punchcard()

// High shimmer texture
$shimmer: note("<c6 ~ e6 ~ g6 ~ b6 ~>")
    .s("sine")
    .lpf(sine.range(4000, 10000).slow(32))
    .decay(0.4)
    .delay(0.4)
    .delaytime(0.5)
    .room(0.6)
    .gain(slider(0.18, 0, 0.6))
    .pan(perlin.range(-0.5, 0.5))
    .slow(16)
    .color("lime")

// Cosmic wind texture
$wind: s("wind:0")
    .loop()
    .lpf(sine.range(400, 2500).slow(slider(24, 8, 48)))
    .hpf(200)
    .gain(slider(0.22, 0, 0.7))
    .slow(slider(8, 4, 16))
    .color("orange")
    .scope({ size: 256 })
