// @name Granular Texture
// @genre Ambient
// @bpm 70
// @tags grains, atmospheric, subtle, texture

setcpm(70 / 4)

// ═══════════════════════════════════════════════════════════════
// GRANULAR TEXTURE - Chopped samples creating atmospheric clouds
// ═══════════════════════════════════════════════════════════════

// Granular-style textures using chopped voice samples
$grains: s("alphabet:0")
    .chop(choose(16, 32, 64))
    .speed(choose(0.25, 0.5, 0.75, 1, 1.5))
    .pan(perlin.range(-0.8, 0.8))
    .lpf(sine.range(800, 4000).slow(slider(16, 4, 32)))
    .room(slider(0.55, 0, 1))
    .delay(0.4)
    .delaytime(0.333)
    .struct("x(11,16)")  // Dense cloud
    .gain(slider(0.65, 0, 2))
    .shuffle()
    .color("orange")
    ._punchcard()

// Second granular layer - metallic
$metals: s("metal:3")
    .chop(choose(8, 16))
    .speed(choose(0.5, 2))
    .lpf(3000)
    .hpf(500)
    .struct("x(5,16)")
    .pan(rand.range(-0.6, 0.6))
    .gain(slider(0.35, 0, 1.2))
    .color("gray")

// Deep evolving pad
$pad: note("<c3 d3 e3 g3>")
    .s("sawtooth")
    .lpf(sine.range(300, 1500).slow(slider(24, 8, 48)))
    .attack(slider(1.5, 0.5, 3))
    .release(slider(2, 0.5, 4))
    .slow(slider(8, 4, 16))
    .room(slider(0.6, 0, 1))
    .gain(slider(0.45, 0, 1.5))
    .color("purple")
    .scope({ size: 256 })

// Sub drone foundation
$sub: note("c1")
    .s("sine")
    .lpf(80)
    .attack(2)
    .release(2)
    .gain(slider(0.55, 0, 1.8))
    .color("cyan")

// High frequency dust
$dust: s("noise:2")
    .chop(32)
    .lpf(10000)
    .hpf(4000)
    .gain(0.15)
    .pan(rand.range(-0.5, 0.5))
    .struct("x(3,16)")
    .color("white")
