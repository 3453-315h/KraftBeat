// @name Glitch Matrix
// @genre Experimental
// @bpm 130
// @tags glitch, generative, sliders, probability, euclidean

setcpm(130 / 4)

// ═══════════════════════════════════════════════════════════════
// GLITCH MATRIX - Generative chaos with probability and control
// ═══════════════════════════════════════════════════════════════

// Main glitch lead with chromatic movement
$: n("<0 4 7 11> <[0 12]?0.7 4 [7 -5]?0.5 11>")
    .scale("c:chromatic")
    .s("square")
    .lpf(sine.range(500, 3500).fast(slider(6, 2, 12)))
    .lpq(2)
    .decay(slider(0.15, 0.05, 0.3))
    .gain(slider(0.65, 0, 2))
    .chop(choose(4, 8))
    .sometimesBy(0.3, x => x.speed(slider(2, 0.5, 4)))
    .jux(rev)
    .color("magenta")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Granular texture
$gran: s("glitch:0")
    .struct("x(5,16)")
    .chop(16)
    .speed(choose(0.5, 1, 2))
    .lpf(sine.range(1000, 6000).slow(8))
    .gain(slider(0.42, 0, 1.5))
    .color("cyan")

// Probability bass
$bass: note("c2 [c2?0.6] <eb2 g2> [c2?0.4]")
    .s("sawtooth")
    .lpf(sine.range(200, 800).slow(4))
    .decay(0.15)
    .gain(slider(0.8, 0, 2))
    .color("red")
    ._punchcard()

// Euclidean kick
$kick: s("bd(5,8)")
    .bank("RolandTR909")
    .gain(slider(0.95, 0, 2))
    .shape(0.4)
    .color("orange")
    ._punchcard()

// Euclidean snare
$snare: s("sd(3,8,2)")
    .bank("RolandTR909")
    .gain(slider(0.85, 0, 2))
    .room(0.25)
    .color("white")
    ._punchcard()

// Glitch hats
$hat: s("hh*16")
    .bank("RolandTR909")
    .gain(perlin.range(0.2, 0.45))
    .chop(choose(2, 4))
    .every(4, x => x.rev())
    .color("gray")
    ._punchcard()

// Random stabs
$stab: note(choose(0, 3, 7, 10))
    .scale("c:minor")
    .s("sawtooth")
    .struct("x(3,16)")
    .lpf(2000)
    .decay(0.1)
    .room(0.4)
    .gain(slider(0.35, 0, 1.2))
    .pan(rand.range(-0.5, 0.5))
    .color("yellow")

// Noise bursts
$noise: s("noise:2")
    .struct("x(2,16)")
    .lpf(8000)
    .hpf(500)
    .decay(0.05)
    .gain(slider(0.25, 0, 0.8))
    .color("white")

// Polymetric rim
$rim: s("rim").struct("x(5,12)")
    .bank("RolandTR909")
    .gain(0.4)
    .pan(slider(0.3, -0.3, 0.3))
    .color("lime")
