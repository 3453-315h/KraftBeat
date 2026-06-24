// @name Chaos Engine
// @genre Experimental
// @bpm 140
// @tags complex, glitch, chaos, experimental, probability

setcpm(140 / 4)

// ═══════════════════════════════════════════════════════════════
// CHAOS ENGINE - Glitch, probability, and controlled chaos
// ═══════════════════════════════════════════════════════════════

// Glitchy lead with randomness
$lead: note("c4 e4 g4 b4 c5 b4 g4 e4")
    .s("square")
    .lpf(sine.range(500, 3000).fast(slider(8, 4, 16)))
    .lpq(0.5)
    .decay(slider(0.12, 0.05, 0.25))
    .gain(slider(0.72, 0, 2))
    .sometimesBy(0.3, x => x.speed(choice(2, 0.5, 4)))
    .sometimesBy(0.2, x => x.vowel("<a e i o u>"))
    .jux(rev)
    .room(slider(0.35, 0, 0.8))
    .color("magenta")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Granular-style texture
$grain: note("<c3 d3 e3 g3>")
    .s("sawtooth")
    .chop(choose(8, 16, 32))
    .gain(slider(0.55, 0, 1.5))
    .lpf(sine.range(300, 2000).slow(slider(16, 8, 32)))
    .room(slider(0.45, 0, 0.9))
    .pan(rand.range(-0.5, 0.5))
    .color("cyan")

// Probability bass - evolving line
$bass: note("c2 [c2?0.5 ~] <eb2 d2> [c2 c3?0.3]")
    .s("sawtooth")
    .lpf(sine.range(200, 800).slow(slider(4.0, 1, 16)))
    .decay(slider(0.15, 0.06, 0.3))
    .gain(slider(0.82, 0, 2))
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Euclidean kick
$kick: s("bd(5,8)")
    .bank("RolandTR909")
    .gain(slider(1.0, 0, 2))
    .sometimesBy(0.2, x => x.speed(choice(1.5, 0.5)))
    .shape(slider(0.4, 0, 0.85))
    .color("orange")
    ._punchcard()

// Euclidean snare with varying density
$snare: s("sd(3,8,1)")
    .bank("RolandTR909")
    .room(slider(0.25, 0, 0.65))
    .gain(slider(0.78, 0, 2))
    .every(4, x => x.fast(choice(2, 4)))
    .color("white")
    ._punchcard()

// Glitch hats with stutter
$hat: s("hh*16")
    .bank("RolandTR909")
    .lpf(sine.range(4000, 10000).fast(slider(2, 1, 16)))
    .gain(slider(0.42, 0, 1.2))
    .chop(choice(2, 4))
    .every(3, x => x.rev())
    .color("gray")
    ._punchcard()

// Random stabs
$stab: note("<c4?0.7 eb4?0.5 g4?0.8 bb4?0.4>")
    .s("square")
    .lpf(sine.range(1000, 4000).slow(slider(8, 4, 16)))
    .decay(slider(0.1, 0.05, 0.2))
    .gain(slider(0.65, 0, 2))
    .room(slider(0.3, 0, 0.8))
    .pan(rand.range(-0.5, 0.5))
    .color("yellow")
    ._punchcard()

// Noise bursts
$noise: s("h?0.3")
    .bank("RolandTR909")
    .lpf(sine.range(2000, 8000).fast(slider(8, 1, 16)))
    .gain(slider(0.38, 0, 1.2))
    .delay(slider(0.2, 0, 0.5))
    .color("white")
    .scope({ size: 256 })

// Polymetric percussion
$poly: s("rim*5")
    .bank("RolandTR808")
    .gain(slider(0.58, 0, 1.8))
    .lpf(sine.range(800, 3000).slow(slider(4.0, 1, 16)))
    .pan(sine.range(-0.5, 0.5).fast(slider(5, 1, 16)))
    .color("lime")

// Reverse stab effect
$rev: note("<[c4,e4,g4] ~ ~ ~>")
    .s("sawtooth")
    .lpf(sine.range(1500, 4500).slow(slider(4.0, 1, 16)))
    .decay(0.3)
    .rev()
    .gain(slider(0.45, 0, 1.5))
    .room(0.5)
    .slow(slider(4.0, 1, 16))
    .color("purple")
    ._punchcard()
