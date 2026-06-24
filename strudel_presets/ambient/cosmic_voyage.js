// @name Cosmic Voyage
// @genre Ambient
// @bpm 70
// @tags ambient, evolving, space, generative

setcpm(70 / 4)

// Main pad drone
$pad: note("<c3 e3 g3 b3>")
    .s("sawtooth")
    .lpf(sine.range(200, 4000).slow(slider(16, 1, 32)))
    .attack(slider(0.8, 0, 2))
    .release(slider(0.5, 0, 1))
    .room(slider(0.6, 0, 1))
    .slow(slider(8, 1, 16))
    .gain(slider(0.5, 0, 2))
    .color("purple")
    .scope({ size: 256 })

// Second pad layer
$pad2: note("<g2 b2 d3 f#3>")
    .s("triangle")
    .lpf(sine.range(300, 2000).slow(slider(12, 1, 32)))
    .attack(slider(1.0, 0, 2))
    .release(slider(0.8, 0, 1))
    .room(slider(0.5, 0, 1))
    .slow(slider(12, 1, 16))
    .gain(slider(0.4, 0, 2))
    .color("cyan")
    .scope({ size: 256 })

// Shimmer melody
$shimmer: n(choose(60, 64, 67, 72, 76, 79))
    .s("sine")
    .struct("x(3,16)")
    .attack(slider(0.3, 0, 1))
    .release(slider(0.5, 0, 1))
    .delay(slider(0.3, 0, 1))
    .room(slider(0.4, 0, 1))
    .slow(slider(4, 1, 16))
    .gain(slider(0.3, 0, 2))
    .color("yellow")
    ._punchcard()

// Sub drone
$sub: note("c1")
    .s("sine")
    .lpf(slider(200, 50, 500))
    .slow(slider(16, 1, 32))
    .gain(slider(0.6, 0, 2))
    .color("red")
    .scope({ size: 256 })

// Wind texture
$texture: s("wind:0")
    .loop()
    .lpf(sine.range(500, 3000).slow(slider(8, 1, 16)))
    .gain(slider(0.25, 0, 1))
    .color("lightgray")
