// @name Fractured
// @genre Experimental
// @bpm 125
// @tags fractured, broken, abstract, glitch

setcpm(125 / 4)

// ═══════════════════════════════════════════════════════════════
// FRACTURED - Broken beats and abstract melodies
// ═══════════════════════════════════════════════════════════════

// Fractured rhythms - irregular euclidean
$snare: s("sd").struct("x(7,16)").bank("RolandTR909")
    .gain(slider(0.85, 0, 2))
    .room(0.25)
    .sometimesBy(0.3, x => x.speed(choose(0.5, 2)))
    .color("white")
    ._punchcard()

$kick: s("bd").struct("x(5,16)").bank("RolandTR909")
    .gain(slider(0.95, 0, 2))
    .shape(slider(0.35, 0, 0.7))
    .sometimesBy(0.2, x => x.struct("x(3,8)"))  // Shift pattern
    .color("orange")
    ._punchcard()

$hat: s("hh").struct("x(11,16)").bank("RolandTR909")
    .gain(slider(0.42, 0, 1.2))
    .pan(perlin.range(-0.3, 0.3))
    .chop(choose(2, 4))
    .color("lightgray")
    ._punchcard()

// Abstract melody - random notes in scale
$melody: n(choose(0, 3, 5, 7, 10, 12, 15))
    .scale("C:minor")
    .s("triangle")
    .struct("x(9,16)")
    .lpf(choose(800, 1500, 3000, 5000))
    .decay(choose(0.05, 0.1, 0.2, 0.4))
    .pan(rand.range(-0.6, 0.6))
    .gain(slider(0.55, 0, 2))
    .scope({ size: 256 })
    .color("cyan")
    ._punchcard()

// Glitch layer - alphabet heavy processing
$glitch: s("alphabet:*")
    .n(irand(26))
    .struct("x(3,16)")
    .chop(choose(4, 8, 16, 32))
    .speed(choose(0.25, 0.5, 1, 2, 4))
    .lpf(sine.range(500, 8000).fast(slider(8, 2, 16)))
    .lpq(sine.range(2, 8).slow(4))
    .room(0.4)
    .gain(slider(0.48, 0, 1.5))
    .color("orange")

// Sub pulse
$sub: note("<c1 g0>")
    .s("sine")
    .lpf(80)
    .struct("x(3,8)")
    .attack(0.1)
    .decay(0.3)
    .gain(slider(0.45, 0, 1.2))
    .color("darkred")

// Broken chord stabs
$stabs: note(choose([0, 3, 7], [5, 8, 12], [7, 10, 14]))
    .scale("c:minor")
    .s("sawtooth")
    .struct("x(3,16)")
    .lpf(1500)
    .decay(0.1)
    .delay(0.2)
    .gain(slider(0.35, 0, 1.2))
    .pan(rand.range(-0.4, 0.4))
    .color("purple")
