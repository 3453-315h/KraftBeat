// @name Polymetric Layers
// @genre Experimental
// @bpm 110
// @tags multiple, time, signatures, polyrhythm

setcpm(110 / 4)

// ═══════════════════════════════════════════════════════════════
// POLYMETRIC LAYERS - Multiple time signatures creating complex
// ═══════════════════════════════════════════════════════════════

// Layer 1: 4/4 base - foundation
$four: s("bd sd:1 bd [sd:1 sd:2]")
    .bank("RolandTR808")
    .gain("<0.92 0.98 0.95 1.0>")  // Dynamics
    .shape(slider(0.28, 0, 0.6))
    .every(8, x => x.s("bd [sd sd] bd [sd sd sd sd]"))  // Fill
    .color("orange")
    ._punchcard()

// Additional 4/4 accent
$accent: s("~ ~ ~ ~ ~ ~ ~ rim")
    .bank("RolandTR808")
    .gain(slider(0.55, 0, 1.5))
    .sometimes(x => x.s("~ ~ ~ ~ rim ~ ~ ~"))  // Shift
    .color("yellow")
    ._punchcard()

// Layer 2: 3/4 overlay (creates 12-beat cycle)
$three: s("hh hh hh").euclid(3, 4)
    .bank("RolandTR808")
    .gain(perlin.range(0.38, 0.52))  // Velocity
    .pan(perlin.range(-0.2, 0.2).slow(0.5))
    .every(4, x => x.euclid(5, 8))  // Shift
    .every(8, x => x.euclid(7, 12))  // More complex
    .color("white")
    ._punchcard()

// Layer 3: 5/4 melody (creates complex polyrhythm) in D Dorian
$five: n("0 2 4 5 7")
    .scale("d:dorian")
    .s("triangle")
    .struct("x x x x x").slow(1.25)  // 5/4 feel
    .lpf(sine.range(1500, 4000).slow(slider(8, 4, 16)))
    .decay(slider(0.18, 0.08, 0.35))
    .delay(0.2)
    .delaytime(0.25)
    .room(slider(0.35, 0, 0.85))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.n("7 9 11 12 9"))  // Upper variation
    .color("cyan")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Layer 4: 7/8 arpeggios - D Dorian
$seven: n("<0 2 4 5 7 9 11>")
    .scale("d:dorian")
    .struct("x x x x x x x").slow(0.875)  // 7/8 feel
    .s("sine")
    .lpf(4000)
    .decay(0.12)
    .delay(slider(0.25, 0.1, 0.5))
    .delaytime(0.375)  // Triplet delay
    .room(0.35)
    .trans(12)
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.42, 0, 1.5))
    .sometimes(x => x.rev())  // Reverse phrase
    .color("lime")
    ._punchcard()

// Bass in 4/4 for grounding
$bass: n("<0 ~ 0 ~ 5 ~ 3 ~>")
    .scale("d:dorian")
    .s("sawtooth")
    .lpf(sine.range(280, 650).slow(slider(8, 4, 16)))
    .trans(-12)
    .decay(slider(0.15, 0.06, 0.3))
    .gain(slider(0.75, 0, 2))
    .every(4, x => x.n("<0 3 ~ 0 5 3 ~ 7>"))  // Walking
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer - stable
$sub: n("<0 ~ 0 ~ 5 ~ 5 ~>")
    .scale("d:dorian")
    .s("sine")
    .lpf(80)
    .trans(-24)
    .gain(slider(0.48, 0, 1.3))
    .color("darkred")

// 6/8 percussion layer
$six: s("rim rim rim rim rim rim").euclid(6, 8)
    .bank("RolandTR808")
    .gain(perlin.range(0.28, 0.42))
    .pan(slider(-0.4, -0.6, -0.2))
    .every(4, x => x.euclid(9, 12))
    .color("gray")
    ._punchcard()

// Pad layer for harmony
$pad: n("<[0,4,7] [2,5,9] [4,7,11] [0,4,7]>")
    .scale("d:dorian")
    .s("sawtooth")
    .lpf(sine.range(700, 1800).slow(16))
    .attack(0.4)
    .release(0.5)
    .room(0.5)
    .trans(-12)
    .gain(slider(0.32, 0, 1.1))
    .slow(4)
    .color("purple")
    .scope({ size: 256 })
