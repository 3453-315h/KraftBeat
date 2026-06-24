// @name Euclidean Rhythms
// @genre Experimental
// @bpm 120
// @tags mathematical, complex, shifting, generative

setcpm(120 / 4)

// ═══════════════════════════════════════════════════════════════
// EUCLIDEAN RHYTHMS - Mathematical patterns that evolve
// ═══════════════════════════════════════════════════════════════

// Evolving euclidean kick - shifts between patterns
$kick: s("bd").euclid(5, 16).bank("RolandTR808")
    .gain("<0.95 1.02 0.98 1.05>")  // Dynamics
    .shape(slider(0.3, 0, 0.65))
    .every(4, x => x.euclid(7, 16))  // Pattern shift
    .every(8, x => x.euclid(9, 16))  // More complex
    .every(16, x => x.euclid(3, 8))  // Simple moment
    .color("orange")
    ._punchcard()

// Interlocking euclidean snare
$snare: s("sd").euclid(3, 8).bank("RolandTR808")
    .gain(slider(0.85, 0, 2))
    .room(slider(0.25, 0, 0.7))
    .slow(slider(2.0, 1, 8))
    .every(4, x => x.euclid(5, 8))  // Shift
    .every(8, x => x.euclid(7, 16))  // Complexity
    .color("white")
    ._punchcard()

// Fast euclidean hats with varying density
$hat: s("hh").euclid(7, 16).bank("RolandTR808")
    .gain(perlin.range(0.38, 0.55))  // Humanized
    .pan(perlin.range(-0.2, 0.2).slow(0.25))
    .every(4, x => x.euclid(11, 16))  // Denser
    .every(8, x => x.euclid(5, 8))  // Sparser
    .sometimes(x => x.euclid(13, 16))  // Very dense
    .color("white")
    ._punchcard()

// Rim accent pattern
$rim: s("rim").euclid(5, 12).bank("RolandTR808")
    .gain(perlin.range(0.45, 0.62))
    .pan(slider(0.4, 0.2, 0.6))
    .every(4, x => x.euclid(7, 12))  // Shift
    .rarely(x => x.euclid(9, 16))  // Occasional change
    .color("yellow")
    ._punchcard()

// Euclidean melody in C minor with pattern shifts
$melody: n("<0 2 4 5 7 9 11 12>")
    .scale("c:minor")
    .struct("x").euclid(7, 16)
    .s("triangle")
    .lpf(sine.range(1500, 5000).slow(slider(8, 4, 16)))
    .decay(slider(0.18, 0.08, 0.35))
    .room(slider(0.35, 0, 0.85))
    .gain(slider(0.52, 0, 2))
    .delay(0.2)
    .delaytime(0.25)
    .every(4, x => x.euclid(9, 16))  // Pattern shift
    .every(8, x => x.euclid(5, 8))  // Simplify
    .sometimes(x => x.rev())  // Reverse phrase
    .color("cyan")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Arp layer with euclidean gating
$arp: n("<0 4 7 11 7 4>")
    .scale("c:minor")
    .struct("x").euclid(5, 8)
    .s("sine")
    .lpf(4000)
    .decay(0.12)
    .delay(0.25)
    .room(0.3)
    .trans(12)
    .gain(slider(0.35, 0, 1.3))
    .every(4, x => x.euclid(7, 12))
    .color("lime")

// Evolving bass with euclidean rhythm
$bass: n("<0 5 3 7>")
    .scale("c:minor")
    .struct("x").euclid(5, 8)
    .s("sawtooth")
    .lpf(sine.range(250, 700).slow(slider(8, 4, 16)))
    .trans(-12)
    .decay(slider(0.15, 0.06, 0.3))
    .gain(slider(0.78, 0, 2))
    .every(4, x => x.euclid(7, 16))  // Busier
    .every(8, x => x.euclid(3, 8))  // Sparser
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: n("<0 ~ 0 ~ 5 ~ 3 ~>")
    .scale("c:minor")
    .s("sine")
    .lpf(80)
    .trans(-24)
    .gain(slider(0.48, 0, 1.3))
    .color("darkred")

// Pad with euclidean chords
$pad: n("<[0,4,7] [2,5,9] [4,7,11] [0,4,7]>")
    .scale("c:minor")
    .struct("x").euclid(3, 8)
    .s("sawtooth")
    .lpf(sine.range(800, 2000).slow(16))
    .attack(0.4)
    .release(0.5)
    .room(0.5)
    .trans(-12)
    .gain(slider(0.38, 0, 1.3))
    .slow(4)
    .every(8, x => x.euclid(5, 12))
    .color("purple")
    .scope({ size: 256 })
