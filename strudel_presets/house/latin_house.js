// @name Latin House
// @genre House
// @bpm 123
// @tags latin, percussion, tropical, salsa

setcpm(123 / 4)

// ═══════════════════════════════════════════════════════════════
// LATIN HOUSE - Tropical percussion with house foundation
// ═══════════════════════════════════════════════════════════════

// Four-on-floor with subtle dynamics
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.0 0.95 0.98 0.95> <0.95 0.98 1.0 0.95>")  // Breathing
    .shape(slider(0.25, 0, 0.6))
    .lpf(300)  // Warm kick
    .every(16, x => x.s("bd bd bd [~ bd] bd bd [bd bd] bd"))  // Variation
    .color("orange")
    ._punchcard()

// Latin-influenced hat pattern
$hat: s("[~ hh] hh [~ hh] [hh oh]").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.5))  // Humanized
    .pan(perlin.range(-0.15, 0.15).slow(0.25))
    .sometimes(x => x.s("[hh ~] hh [~ hh] [~ oh]"))  // Variation
    .every(8, x => x.s("[hh hh] [~ hh] [hh hh hh hh] [oh hh]"))  // Fill
    ._punchcard()

// Clap with Latin delay
$clap: stack(
    s("~ cp ~ cp").gain(slider(0.8, 0, 2)).room(0.3),
    s("~ ~ [~ cp:3] ~").gain(0.2).lpf(4000)  // Ghost
).bank("RolandTR909")
    .delay(slider(0.15, 0, 0.4))
    .every(8, x => x.s("~ cp ~ [cp cp cp cp]"))  // Fill
    .color("yellow")
    ._punchcard()

// CONGA - authentic Latin rhythm pattern
$conga: s("~ conga:0 [conga:1 ~] conga:2")
    .gain(perlin.range(0.42, 0.58))  // Velocity variation
    .pan(slider(-0.2, -0.5, 0.3))
    .room(0.15)
    .sometimes(x => x.s("conga:0 ~ [conga:1 conga:2] conga:0"))  // Variation
    .every(4, x => x.s("[conga:0 conga:1] conga:2 [conga:0 conga:1] conga:2"))  // Roll
    .color("brown")
    ._punchcard()

// Shaker with Latin feel
$shaker: s("shaker*8")
    .gain(perlin.range(0.2, 0.32))
    .pan(perlin.range(-0.3, 0.3).slow(0.25))
    .nudge(perlin.range(-0.01, 0.015))  // Micro-timing
    .color("gray")

// Cowbell - classic Latin house element
$cowbell: s("~ ~ cb ~").bank("RolandTR808")
    .gain(perlin.range(0.35, 0.5))  // Velocity
    .sometimes(x => x.s("~ cb [~ cb] ~"))  // Extended pattern
    .every(8, x => x.s("[~ cb] [cb ~] [~ cb] cb"))  // Fill
    .color("yellow")
    ._punchcard()

// Timbale accent
$timbale: s("~ ~ ~ ~ ~ tim ~ ~")
    .gain(slider(0.4, 0, 1.2))
    .room(0.2)
    .sometimes(x => x.s("~ ~ tim ~ ~ ~ tim tim"))  // Roll
    .color("orange")

// Tropical bass with movement
$bass: note("<c2 ~ [c2 c3] ~ g2 ~ [f2 g2] ~>")
    .s("sawtooth")
    .lpf(sine.range(300, 700).slow(slider(4.0, 1, 16)))
    .decay(slider(0.12, 0.04, 0.25))
    .gain(slider(0.78, 0, 2))
    .rarely(x => x.note("<c2 c3 [c2 d2] g2 g2 g3 [f2 g2] f3>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ c1 ~ g1 ~ f1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.4, 0, 1.2))
    .color("darkred")

// Piano house chords with Latin feel
$piano: note("<[c4,e4,g4] ~ [c4,e4,g4] ~ [f4,a4,c5] ~ [g4,b4,d5] ~>")
    .s("triangle")  // Piano-like
    .lpf(sine.range(2500, 5000).slow(8))
    .decay(0.2)
    .room(slider(0.3, 0, 1))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.note("<[d4,f4,a4] ~ [e4,g4,b4] ~>"))  // Chord variation
    .rarely(x => x.fast(2).gain(0.45))  // Double chord hit
    .color("cyan")
    ._punchcard()

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.4)
    .room(0.4)
    .slow(2)
