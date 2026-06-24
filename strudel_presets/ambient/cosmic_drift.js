// @name Cosmic Drift
// @genre Ambient
// @bpm 60
// @tags complex, cosmic, drones, evolving, space

setcpm(60 / 4)

// ═══════════════════════════════════════════════════════════════
// COSMIC DRIFT - Evolving space textures and generative melodies
// ═══════════════════════════════════════════════════════════════

// Main evolving pad drone
$pad1: note("[c2,g2,c3,g3]")
    .s("sawtooth")
    .lpf(sine.range(200, 1800).slow(slider(24, 8, 48)))  // Very slow sweep
    .attack(slider(2, 1, 4))
    .release(slider(3, 1, 6))
    .gain(slider(0.55, 0, 1.5))
    .room(slider(0.65, 0, 1))
    .slow(slider(8, 4, 16))
    .color("purple")
    .pianoroll({ fold: 1 })
    .scope({ size: 256 })

// Second pad layer - ethereal
$pad2: note("[g2,d3,g3,b3]")
    .s("triangle")
    .lpf(sine.range(300, 1200).slow(slider(32, 16, 64)))
    .attack(slider(2.5, 1, 5))
    .release(slider(3.5, 1, 7))
    .gain(slider(0.45, 0, 1.2))
    .room(slider(0.65, 0, 1))
    .slow(slider(16, 8, 32))
    .color("blue")

// High generative shimmer
$shimmer: n(choose(72, 74, 76, 79, 81, 84, 86, 88))
    .s("sine")
    .struct("x(3,16)")
    .attack(slider(0.2, 0.1, 0.5))
    .decay(slider(0.8, 0.4, 1.5))
    .gain(slider(0.32, 0, 1))
    .room(slider(0.75, 0, 1))
    .delay(slider(0.4, 0.2, 0.8))
    .delaytime(0.666)
    .pan(perlin.range(-0.6, 0.6))  // Wide stereo
    .slow(slider(4.0, 1, 16))
    .sometimes(x => x.struct("x(5,16)"))  // Denser
    .color("cyan")
    ._punchcard()

// Deep sub drone - foundation
$sub: note("c1")
    .s("sine")
    .lpf(80)
    .attack(3)
    .gain(slider(0.48, 0, 1.5))
    .slow(slider(8, 4, 16))
    .color("darkred")

// Generative slow melody
$melody: note("<c4 ~ e4 ~> <~ g4 ~ a4> <b4 ~ g4 ~> <~ d4 ~ c4>")
    .s("sine")
    .lpf(sine.range(1500, 4500).slow(slider(16, 8, 32)))
    .attack(0.5)
    .decay(2)
    .room(slider(0.6, 0.2, 1))
    .gain(slider(0.42, 0, 1.2))
    .slow(slider(8, 4, 16))
    .sometimes(x => x.note("<e4 g4 c5 b4>"))  // Variation
    .color("yellow")
    ._punchcard()

// Granular texture layer 1
$tex1: note("[c3,e3]")
    .s("sawtooth")
    .lpf(sine.range(400, 1200).fast(8))  // Faster modulation
    .attack(2)
    .release(2)
    .gain(slider(0.18, 0, 0.6))
    .room(0.5)
    .pan(sine.range(-0.3, 0.3).slow(8))
    .slow(16)
    .color("gray")

// Granular texture layer 2
$tex2: note("[g3,b3]")
    .s("triangle")
    .lpf(sine.range(600, 1500).fast(6))
    .attack(2)
    .release(2)
    .gain(slider(0.15, 0, 0.5))
    .room(0.5)
    .pan(sine.range(0.3, -0.3).slow(12))
    .slow(16)
    .color("lightgray")

// Sparse space percussion
$perc: s("~ ~ ~ [rim:5 ~]")
    .room(slider(0.8, 0.4, 1))
    .delay(slider(0.5, 0.2, 0.8))
    .lpf(2000)
    .gain(slider(0.25, 0, 0.8))
    .slow(slider(8, 4, 16))
    .pan(perlin.range(-0.4, 0.4))
    .color("white")
    ._punchcard()
