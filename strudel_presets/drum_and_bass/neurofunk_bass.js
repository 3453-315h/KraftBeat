// @name Neurofunk Bass
// @genre Drum and Bass
// @bpm 176
// @tags dark, aggressive, wobble, neuro

setcpm(176 / 4)

// ═══════════════════════════════════════════════════════════════
// NEUROFUNK - Dark aggressive bass with hard drums
// ═══════════════════════════════════════════════════════════════

// Hard hitting kick with dynamics
$kick: s("bd ~ ~ ~ bd ~ [~ bd] ~").bank("RolandTR909")
    .gain("<1.2 1.15 1.18 1.12> <1.15 1.12 1.2 [1.25 1.15]>")  // Power dynamics
    .shape(slider(0.35, 0, 0.7))
    .every(4, x => x.s("[bd ~] ~ ~ ~ bd ~ [bd bd] ~"))  // Variation
    .every(8, x => x.s("bd ~ ~ bd bd ~ [~ bd] [bd bd]"))  // 8-bar fill
    .color("orange")
    ._punchcard()

// Aggressive snare with ghost layering
$snare: stack(
    s("~ ~ sd ~ ~ ~ sd ~").gain(slider(1.1, 0, 2)).room(0.25),
    s("~ ~ ~ [sd:3 sd:3] ~ ~ ~ [sd:3 ~]").gain(0.35).lpf(6000)  // Ghost rush
).bank("RolandTR909")
    .every(4, x => x.s("~ ~ sd ~ ~ ~ sd [sd sd]"))  // 4-bar fill
    .every(8, x => x.s("~ ~ sd ~ ~ [sd sd] sd [sd sd sd sd]"))  // 8-bar fill
    .color("white")
    ._punchcard()

// Fast rolling hats with aggression
$hat: s("[hh hh] [hh hh] [hh hh] [hh [hh hh]]").bank("RolandTR909")
    .gain(perlin.range(0.38, 0.55))  // Velocity variation
    .pan(perlin.range(-0.2, 0.2).slow(0.25))
    .sometimes(x => x.fast(1.5))  // Triplets
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh*16]"))  // Hat roll build
    .color("white")
    ._punchcard()

// Ride for intensity
$ride: s("rd*8").bank("RolandTR909")
    .gain(perlin.range(0.32, 0.48))
    .sometimes(x => x.fast(2).gain(0.4))  // Double-time intensity
    .color("gray")
    ._punchcard()

// AGGRESSIVE NEURO BASS - the signature sound
$bass: note("<c1 c1 [c1 d#1] c1 f1 f1 [d#1 c1] c1>")
    .s("sawtooth")
    .lpf(sine.range(200, 2500).fast(slider(4, 1, 16)))
    .lpq(sine.range(5, 15).slow(2))  // Heavy resonance movement
    .decay(slider(0.12, 0.04, 0.25))
    .gain(slider(0.85, 0, 2))
    .chop(sine.range(4, 16).slow(4))  // Wobble modulation
    .rarely(x => x.fast(2))  // Double-time bass
    .every(8, x => x.lpf(sine.range(300, 4000).fast(8)))  // Faster filter
    .scope({ size: 256 })
    .color("red")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Mid bass layer for thickness
$midbass: note("<c2 ~ [c2 d#2] ~ f2 ~ [d#2 c2] ~>")
    .s("square")
    .lpf(sine.range(600, 1800).fast(2))
    .lpq(6)
    .decay(0.1)
    .gain(slider(0.45, 0, 1.5))
    .color("orange")

// Sub layer
$sub: note("<c1 c1 c1 c1 f1 f1 c1 c1>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.55, 0, 1.5))
    .color("darkred")

// Dark atmosphere pad
$atmo: note("[c2,eb2,g2]")
    .s("sawtooth")
    .lpf(sine.range(200, 600).slow(16))
    .attack(1)
    .release(1)
    .room(0.5)
    .gain(slider(0.2, 0, 0.7))
    .slow(8)
    .color("purple")
    .scope({ size: 256 })

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.55)
    .room(0.35)
    .slow(2)
