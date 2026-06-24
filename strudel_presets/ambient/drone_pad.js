// @name Drone Pad
// @genre Ambient
// @bpm 60
// @tags slow, evolving, peaceful, meditative

setcpm(60 / 4)

// ═══════════════════════════════════════════════════════════════
// DRONE PAD - Evolving textures and peaceful atmospheres
// ═══════════════════════════════════════════════════════════════

// Main evolving pad with slow filter sweep
$pad: note("<c3 e3 g3 b3>")
    .s("sawtooth")
    .lpf(sine.range(400, 2500).slow(slider(16, 4, 32)))
    .lpq(sine.range(0.5, 2).slow(24))  // Gentle resonance
    .attack(slider(1.2, 0.5, 2.5))
    .release(slider(1.5, 0.6, 3))
    .room(slider(0.55, 0, 1))
    .delay(0.15)
    .delaytime(0.5)
    .slow(slider(8, 4, 16))
    .gain(slider(0.52, 0, 1.8))
    .sometimes(x => x.note("<d3 f3 a3 c4>"))  // Dm7 variation
    .color("purple")
    ._punchcard()
    .pianoroll({ fold: 1 })
    .scope({ size: 256 })

// Second pad layer for thickness
$pad2: note("<g2 ~ ~ ~ d3 ~ ~ ~>")
    .s("triangle")
    .lpf(sine.range(300, 1200).slow(24))
    .attack(1.5)
    .release(2)
    .room(0.5)
    .gain(slider(0.28, 0, 0.9))
    .slow(slider(8, 4, 16))
    .color("cyan")

// Deep drone foundation
$drone: note("c2")
    .s("triangle")
    .lpf(sine.range(150, 600).slow(slider(16, 4, 32)))
    .attack(slider(1.8, 0.8, 3))
    .release(slider(2, 0.8, 4))
    .slow(slider(8, 4, 16))
    .gain(slider(0.5, 0, 1.5))
    .color("cyan")
    .scope({ size: 256 })

// Fifth drone layer
$drone5: note("g1")
    .s("sine")
    .lpf(200)
    .attack(2)
    .release(2)
    .gain(slider(0.35, 0, 1.2))
    .slow(16)
    .color("darkred")

// High shimmer texture
$shimmer: note(choose(72, 76, 79, 84, 88))
    .s("sine")
    .struct("x(3,16)")
    .attack(slider(0.2, 0.08, 0.5))
    .decay(0.5)
    .delay(slider(0.4, 0.15, 0.7))
    .delaytime(0.666)  // Dotted eighth
    .room(slider(0.6, 0, 1))
    .gain(slider(0.22, 0, 0.8))
    .pan(perlin.range(-0.5, 0.5))  // Wide stereo
    .slow(slider(8, 4, 16))
    .color("yellow")

// Texture layer (wind-like)
$texture: s("wind:0")
    .loop()
    .lpf(sine.range(300, 2000).slow(slider(16, 4, 32)))
    .hpf(200)
    .gain(slider(0.25, 0, 0.8))
    .slow(slider(8, 4, 16))
    .color("orange")
    .scope({ size: 256 })

// Subtle movement layer
$movement: note("<c4 ~ e4 ~ g4 ~ b4 ~>")
    .s("sine")
    .lpf(sine.range(1500, 4000).slow(32))
    .attack(0.8)
    .decay(1)
    .delay(0.3)
    .room(0.6)
    .gain(slider(0.18, 0, 0.6))
    .slow(16)
    .color("lime")
