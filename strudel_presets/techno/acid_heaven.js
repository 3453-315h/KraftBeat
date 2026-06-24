// @name Acid Heaven
// @genre Techno
// @bpm 140
// @tags acid, 303, squelch, trippy, rave

setcpm(140 / 4)

// ═══════════════════════════════════════════════════════════════
// ACID HEAVEN - Triple 303 chaos with rave energy
// ═══════════════════════════════════════════════════════════════

// 909 kick with drive and fills
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.2 1.15 1.18 1.12> <1.15 1.12 1.2 [1.25 1.18]>")  // Power dynamics
    .shape(slider(0.22, 0, 0.5))
    .every(4, x => x.s("[bd bd] bd bd bd"))  // 4-bar punch
    .every(8, x => x.s("bd bd bd bd [bd bd] bd bd"))  // 8-bar phrase
    .every(16, x => x.s("bd bd bd [bd bd] bd [bd bd bd bd] [bd*8]"))  // Build
    .color("orange")
    ._punchcard()

// Fast rolling hats with variations
$hat: s("[hh hh hh hh] [hh hh oh hh] [hh hh hh hh] [oh hh hh hh]").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.52))  // Humanized velocity
    .sometimes(x => x.s("[hh hh hh hh] [hh oh ~ hh] [hh hh hh hh] [oh ~ hh hh]"))  // Variation
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh oh hh*8]"))  // Hat roll
    .every(16, x => x.fast(1.5))  // Triplet rave energy
    ._punchcard()

// Claps with reverb tail and ghost
$clap: stack(
    s("~ cp ~ cp").gain(slider(0.9, 0, 2)).room(0.3),
    s("~ [cp:3 ~] ~ ~").gain(0.25).lpf(5000)  // Ghost clap
).bank("RolandTR909")
    .every(8, x => x.s("~ cp ~ [cp cp cp cp]"))  // 8-bar fill
    .color("white")
    ._punchcard()

// Snare roll for builds
$snareroll: s("~ ~ ~ ~ ~ ~ ~ ~")
    .bank("RolandTR909")
    .every(16, x => x.s("~ ~ ~ ~ ~ ~ [sd*4] [sd*8] ~ ~ ~ ~ [sd*8] [sd*16] [sd*32] [sd*64]"))
    .gain(slider(0.65, 0, 2))
    .lpf(sine.range(2500, 10000).fast(8))
    .color("yellow")

// Main acid - aggressive low end with squelch
$acid1: note("<g1 [g1 a#1] g1 [c2 d#2] g1 [a#1 g1] c2 g1>")
    .s("square")
    .lpf(sine.range(400, 5000).fast(slider(6, 2, 12)))
    .lpq(sine.range(5, 18).slow(2))  // Heavy resonance
    .decay(slider(0.06, 0.02, 0.15))
    .gain(slider(0.85, 0, 2))
    .rarely(x => x.note("<g1 g2 g1 g2>").fast(2))  // Octave madness
    .every(8, x => x.fast(1.5))  // Triplet acid
    .scope({ size: 256 })
    .color("yellow")
    .pianoroll({ fold: 1 })

// Second acid - squelchy mid range
$acid2: note("<d#3 ~ [d#3 g3] ~ a#3 ~ [g3 d#3] ~>")
    .s("sawtooth")
    .lpf(sine.range(600, 4500).fast(slider(4, 1, 8)))
    .lpq(sine.range(3, 12).fast(2))  // Resonance sweep
    .decay(slider(0.08, 0.02, 0.2))
    .gain(slider(0.55, 0, 2))
    .pan(sine.range(-0.4, 0.1).slow(2))  // Stereo movement
    .sometimes(x => x.fast(2))  // Double-time fills
    .rarely(x => x.rev())  // Reverse pattern
    .color("lime")
    ._punchcard()

// High acid stabs - screaming leads
$acid3: note("<g4 ~ a#4 ~ d#5 ~ g4 ~>")
    .s("square")
    .lpf(sine.range(1500, 7000).fast(slider(8, 2, 16)))
    .lpq(sine.range(2, 10).slow(4))  // Screaming resonance
    .decay(slider(0.1, 0.03, 0.25))
    .gain(slider(0.38, 0, 1.5))
    .pan(sine.range(-0.1, 0.4).slow(4))  // Counter stereo
    .sometimes(x => x.note("<g4 a#4 d#5 g5>").fast(2))  // Ascending runs
    .rarely(x => x.note("<c5 d#5 g5 a#5>"))  // Higher register
    .color("cyan")

// Bonus acid layer - chaotic fills
$acid4: note("<~ ~ c3 ~ ~ ~ g3 ~>")
    .s("sawtooth")
    .lpf(sine.range(800, 6000).fast(6))
    .lpq(8)
    .decay(0.08)
    .gain(slider(0.3, 0, 1.2))
    .delay(0.2)
    .room(0.15)
    .rarely(x => x.note("<c3 d#3 g3 c4>").fast(4))  // Acid run
    .color("orange")

// Dark pad underneath for depth
$pad: note("<[g2,d3,g3] [g2,d3,g3] [d#2,a#2,d#3] [g2,d3,g3]>")
    .s("triangle")
    .lpf(slider(1000, 300, 2000))
    .attack(slider(0.5, 0.2, 1))
    .release(slider(0.6, 0.25, 1.1))
    .room(slider(0.4, 0, 0.85))
    .gain(slider(0.28, 0, 1))
    .slow(4)
    .color("purple")
    .scope({ size: 256 })

// Sub for weight
$sub: note("<g0 g0 g0 g0 g0 g0 c1 c1>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.5, 0, 1.2))
    .color("darkred")

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.5)
    .room(0.4)
    .slow(2)
