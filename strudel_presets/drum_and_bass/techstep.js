// @name Tech Step
// @genre Drum and Bass
// @bpm 175
// @tags techstep, dark, sci-fi, futuristic

setcpm(175 / 4)

// ═══════════════════════════════════════════════════════════════
// TECHSTEP - Dark sci-fi DnB with metallic textures
// ═══════════════════════════════════════════════════════════════

// Punchy techstep kick with dynamics
$kick: s("bd ~ ~ ~ bd ~ bd ~").bank("RolandTR909")
    .gain("<1.1 1.05 1.08 1.02> <1.05 1.08 1.1 [1.15 1.08]>")  // Dynamics
    .shape(slider(0.32, 0, 0.65))
    .every(4, x => x.s("[bd ~] ~ ~ ~ bd ~ [bd bd] ~"))  // Variation
    .every(8, x => x.s("bd ~ bd ~ bd ~ [bd bd] bd"))  // 8-bar fill
    .color("orange")
    ._punchcard()

// Snappy snare with ghost layers
$snare: stack(
    s("~ ~ sd ~ ~ ~ sd ~").gain(slider(0.95, 0, 2)).room(0.28),
    s("~ ~ ~ [sd:3 ~] ~ ~ ~ [sd:3 sd:3]").gain(0.28).lpf(5500)  // Ghost rush
).bank("RolandTR909")
    .every(8, x => x.s("~ ~ sd ~ ~ ~ sd [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Fast rolling hats with filter
$hat: s("hh*16").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.52))  // Humanized
    .lpf(perlin.range(5000, 12000))  // Filter movement
    .pan(perlin.range(-0.12, 0.12).slow(0.25))
    .sometimes(x => x.s("[hh*4] [hh hh oh hh] [hh*4] [hh hh hh oh]"))  // Accents
    .every(8, x => x.fast(1.5).gain(0.45))  // Triplet build
    .color("white")
    ._punchcard()

// Techstep bass with aggressive modulation
$bass: note("<c1 ~ c1 ~ d#1 ~ [c1 d#1] ~>")
    .s("sawtooth")
    .lpf(sine.range(200, 2200).fast(slider(2, 1, 8)))
    .lpq(sine.range(4, 12).slow(2))  // Resonance sweep
    .decay(slider(0.12, 0.04, 0.25))
    .gain(slider(0.85, 0, 2))
    .chop(sine.range(4, 8).slow(4))  // Modulation
    .rarely(x => x.note("<c1 d1 [d#1 f1] d#1>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Mid bass layer
$midbass: note("<c2 ~ c2 ~ d#2 ~ [c2 d#2] ~>")
    .s("square")
    .lpf(sine.range(500, 1500).fast(2))
    .lpq(5)
    .decay(0.1)
    .gain(slider(0.4, 0, 1.3))
    .color("orange")

// Sub layer
$sub: note("<c1 ~ c1 ~ d#1 ~ c1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.55, 0, 1.5))
    .color("darkred")

// Sci-fi pad - atmospheric
$pad: note("[c3,d#3,g3]")
    .s("sawtooth")
    .lpf(sine.range(400, 1500).slow(slider(8.0, 1, 16)))
    .attack(slider(0.5, 0.2, 1.1))
    .release(slider(0.6, 0.25, 1.2))
    .slow(slider(4.0, 1, 16))
    .room(slider(0.4, 0, 1))
    .gain(slider(0.45, 0, 1.5))
    .sometimes(x => x.note("[d3,f3,a3]"))  // Variation
    .color("purple")
    ._punchcard()
    .scope({ size: 256 })

// Metallic hit - techstep texture
$hit: s("metal:0")
    .struct("~ ~ ~ ~ ~ ~ x ~")
    .chop(4)
    .speed(slider(0.6, 0.3, 1.5))
    .room(slider(0.35, 0, 0.8))
    .delay(0.2)
    .gain(slider(0.42, 0, 1.5))
    .sometimes(x => x.struct("~ ~ x ~ ~ ~ x ~"))  // Double hit
    .rarely(x => x.speed(choose(0.5, 0.75, 1.5)))  // Speed variation
    .color("orange")

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.5)
    .room(0.4)
    .slow(2)
