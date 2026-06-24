// @name Generative Melody
// @genre Ambient
// @bpm 80
// @tags random, evolving, notes, generative, probabilistic

setcpm(80 / 4)

// ═══════════════════════════════════════════════════════════════
// GENERATIVE MELODY - Euclidean rhythm with random note selection
// ═══════════════════════════════════════════════════════════════

// Probabilistic note selection from C Minor scale
$melody: n(choose(0, 2, 3, 5, 7, 8, 10, 12, 15))
    .scale("c:minor")
    .s("triangle")
    .lpf(sine.range(500, 3000).slow(slider(16, 4, 32)))
    .attack(slider(0.05, 0.01, 0.2))
    .decay(slider(0.3, 0.1, 0.8))
    .room(slider(0.35, 0, 0.9))
    .delay(slider(0.3, 0.1, 0.8))
    .struct("x(5,16)")  // Euclidean rhythm for interest
    .gain(slider(0.65, 0, 2))
    .pan(rand.range(-0.5, 0.5))  // Random panning
    .color("cyan")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Drone bass foundation
$drone: note("c2")
    .s("sawtooth")
    .lpf(sine.range(150, 600).slow(slider(24, 8, 48)))
    .attack(2)
    .release(3)
    .slow(slider(8, 4, 16))
    .gain(slider(0.55, 0, 1.8))
    .color("purple")
    .scope({ size: 256 })

// Subtle texture layer - high random notes
$texture: n(choose(12, 15, 19, 24))
    .scale("c:minor")
    .s("sine")
    .attack(0.5)
    .decay(1.5)
    .struct("x(3,16)")
    .room(0.6)
    .gain(slider(0.25, 0, 0.8))
    .pan(perlin.range(-0.6, 0.6))
    .color("orange")

// Periodic bass pulse
$pulse: note("<c1 g0>")
    .s("sine")
    .lpf(100)
    .attack(0.2)
    .decay(0.8)
    .slow(4)
    .gain(slider(0.45, 0, 1.5))
    .color("darkred")

// Generative chord beds
$chords: note(choose([0, 3, 7], [5, 8, 12], [8, 12, 15]))
    .scale("c:minor")
    .s("sawtooth")
    .lpf(800)
    .attack(1)
    .release(2)
    .struct("x(2,16)")
    .room(0.5)
    .gain(slider(0.32, 0, 1))
    .color("blue")
