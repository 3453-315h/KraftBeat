// @name Binaural
// @genre Ambient
// @bpm 60
// @tags binaural, meditation, theta, focus

setcpm(60 / 4)

// ═══════════════════════════════════════════════════════════════
// BINAURAL BEATS - Frequency difference for theta waves (5Hz)
// ═══════════════════════════════════════════════════════════════

// Left channel sine - base frequency
$left: note("c3")
    .s("sine")
    .pan(-1)  // Hard left
    .attack(slider(1.5, 0.5, 2.5))
    .release(slider(1, 0.5, 2))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.8, 0, 1.5))
    .color("cyan")
    .pianoroll({ fold: 1 })

// Right channel sine - 5Hz detune
$right: note("c3")
    .s("sine")
    .detune(5)  // 5Hz difference for theta waves
    .pan(1)  // Hard right
    .attack(slider(1.5, 0.5, 2.5))
    .release(slider(1, 0.5, 2))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.8, 0, 1.5))
    .color("blue")

// Binaural beating visualization
$visual: note("c3")
    .s("sawtooth")
    .lpf(200)
    .gain(0)  // Silent visualizer
    .scope({ size: 256 })
    .color("white")

// Soft breathing pad
$pad: note("<[c4,e4,g4,b4] [a3,c4,e4,g4]>")
    .s("triangle")
    .lpf(sine.range(300, 1200).slow(slider(16, 8, 32)))
    .attack(slider(2, 1, 4))
    .release(slider(2.5, 1, 5))
    .struct("x")
    .slow(slider(8, 4, 16))
    .room(slider(0.55, 0, 1))
    .gain(slider(0.35, 0, 0.9))
    .color("purple")
    ._punchcard()

// Deep sub grounding
$sub: note("c2")
    .s("sine")
    .lpf(80)
    .decay(slider(0.5, 0.2, 1.5))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.42, 0, 1.2))
    .color("darkred")

// Subtle white noise washing
$wash: s("noise:0")
    .lpf(sine.range(400, 1500).slow(24))
    .hpf(200)
    .attack(3)
    .release(3)
    .pan(sine.range(-0.3, 0.3).slow(12))  // Slow movement
    .gain(slider(0.12, 0, 0.4))
    .slow(16)
    .color("gray")

// Bell accent
$bell: note("<~ ~ g5 ~ ~ ~ e5 ~>")
    .s("sine")
    .lpf(3000)
    .attack(0.05)
    .decay(3)
    .room(0.7)
    .gain(slider(0.18, 0, 0.6))
    .slow(8)
    .color("yellow")
