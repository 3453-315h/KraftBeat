// @name Probability Drums
// @genre Experimental
// @bpm 130
// @tags random, weighted, evolving

setcpm(130 / 4)

// Chaos controls

// Kick with probability
$kick: s("bd").struct("x ~ x ~")
    .bank("RolandTR909")
    .sometimesBy(0.3, x => x.fast(slider(4.0, 1, 16)))  // Sometimes double time
    .gain(slider(0.8, 0, 2))
    .shape(slider(0.3, 0, 1))
    .color("orange")
    ._punchcard()

// Snare with random variations
$snare: s("~ sd ~ sd")
    .bank("RolandTR909")
    .n(chooseCycles(0, 1, 2))  // Random snare sound
    .sometimesBy(0.2, x => x.delay(slider(0.2, 0, 1)))
    .gain(slider(0.8, 0, 2))
    .color("white")
    ._punchcard()

// Probabilistic hi-hats
$hat: s("hh*8")
    .bank("RolandTR909")
    .gain(choose(0.3, 0.4, 0.5, 0.6))
    .pan(rand.range(-0.5, 0.5))
    .sometimesBy(0.1, x => x.speed(slider(1, 0.5, 2)))
    .color("white")
    ._punchcard()

// Random melodic hits
$melody: n(choose(0, 2, 4, 5, 7, 9, 11))
    .scale("C:minor")
    .s("triangle")
    .struct("x(3,8)")
    .lpf(choose(800, 1200, 2000, 3000))
    .decay(slider(0.3, 0, 1))
    .room(slider(0.3, 0, 1))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.8, 0, 2))
    .scope({ size: 256 })
    .color("cyan")
    ._punchcard()
