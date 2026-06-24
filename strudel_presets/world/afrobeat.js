// @name Afrobeat Groove
// @genre World
// @bpm 115
// @tags afrobeat, fela, polyrhythm, lagos, tony allen

setcpm(115 / 4)

// ═══════════════════════════════════════════════════════════════
// AFROBEAT - Fela Kuti / Tony Allen-style polyrhythmic groove
// ═══════════════════════════════════════════════════════════════

// Tony Allen-style kick with dynamics
$kick: s("bd ~ ~ ~ bd ~ ~ ~ bd ~ ~ bd ~ ~ ~ ~").bank("RolandTR808")
    .gain("<1.1 1.05 1.08 1.02> <1.05 1.02 1.1 1.05>")  // Dynamics
    .shape(slider(0.2, 0, 0.5))
    .nudge(perlin.range(-0.01, 0.02))  // Humanized timing
    .every(8, x => x.s("bd ~ ~ bd bd ~ ~ ~ bd ~ bd ~ ~ ~ ~ ~"))  // Variation
    .color("orange")
    ._punchcard()

// Snare with ghost layers
$snare: stack(
    s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ sd ~ ~ ~").gain(slider(0.9, 0, 2)).room(0.2),
    s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ sd:3 ~ ~ ~ ~ ~").gain(0.28).lpf(4500)  // Ghost
).bank("RolandTR808")
    .nudge(perlin.range(-0.01, 0.015))  // Humanized
    .every(8, x => x.s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ sd ~ [sd sd] ~"))  // Fill
    .color("white")
    ._punchcard()

// Hat pattern with organic feel
$hat: s("[hh hh hh hh] [hh hh hh hh] [hh hh oh hh] [hh hh hh hh]").bank("RolandTR808")
    .gain(perlin.range(0.35, 0.5))  // Humanized velocity
    .pan(perlin.range(-0.15, 0.15).slow(0.5))
    .sometimes(x => x.s("[hh hh hh hh] [hh hh oh hh] [hh hh hh hh] [hh oh hh hh]"))
    .every(8, x => x.s("[hh hh hh hh] [hh hh [hh hh hh] hh] [hh hh oh hh] [hh hh hh oh]"))
    ._punchcard()

// Shekere pattern - essential for afrobeat
$shekere: s("shaker*16")
    .gain(perlin.range(0.28, 0.42))  // Humanized
    .pan(sine.range(-0.35, 0.35).slow(4))
    .euclid(7, 12)  // African polyrhythmic accent
    .sometimes(x => x.euclid(5, 8))  // Variation
    ._punchcard()

// Conga polyrhythm (cross rhythm) with dynamics
$conga: s("[conga:0 ~ conga:1] [~ conga:2 ~] [conga:0 ~ ~] [conga:1 conga:2 ~]")
    .gain(perlin.range(0.5, 0.7))  // Velocity variation
    .room(slider(0.15, 0, 0.5))
    .pan(slider(-0.4, -0.6, -0.2))
    .sometimes(x => x.s("[conga:0 conga:1 ~] [~ conga:2 conga:0] [~ conga:1 ~] [conga:2 ~ conga:0]"))
    .every(4, x => x.s("[conga:0 conga:1 conga:2] [conga:0 ~ conga:1] [conga:2 conga:0 ~] [conga:1 conga:2 conga:0]"))
    ._punchcard()

// Agogo bell - timeline pattern with variations
$bell: s("[ag:0 ~ ag:1 ~] [~ ag:0 ~ ag:1] [ag:0 ~ ~ ag:1] [~ ~ ag:0 ~]")
    .gain(perlin.range(0.42, 0.58))  // Velocity
    .pan(slider(0.5, 0.3, 0.7))
    .sometimes(x => x.s("[ag:0 ag:1 ~ ~] [~ ag:0 ag:1 ~] [ag:0 ~ ag:1 ~] [~ ag:0 ~ ag:1]"))
    .color("yellow")
    ._punchcard()

// Afrobeat bass - syncopated and melodic
$bass: note("<c2 ~ c2 ~ g1 ~ c2 ~ e2 ~ ~ f2 g2 ~ c2 ~>")
    .s("sawtooth")
    .lpf(slider(800, 300, 1500))
    .decay(slider(0.15, 0.06, 0.3))
    .gain(slider(0.82, 0, 2))
    .rarely(x => x.note("<c2 e2 c2 ~ g1 g1 c2 ~ e2 f2 ~ g2 g2 f2 e2 c2>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })

// Sub layer
$sub: note("<c1 ~ ~ ~ g0 ~ ~ ~ e1 ~ ~ ~ g1 ~ ~ ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.45, 0, 1.2))
    .color("darkred")

// Rhythm guitar - choppy off-beat skank
$guitar: note("<[c4,e4,g4] ~ [c4,e4,g4] ~>".add("<0 0 5 7>"))
    .s("sawtooth")
    .lpf(slider(2500, 800, 4500))
    .struct("~ x ~ x ~ x ~ x")
    .decay(slider(0.08, 0.03, 0.18))
    .gain(slider(0.48, 0, 2))
    .room(slider(0.12, 0, 0.4))
    .sometimes(x => x.struct("[~ x] x [~ x] x"))  // Syncopation
    .color("lime")
    ._punchcard()

// Horn stabs (brass section) with variations
$horns: note("<[c5,e5,g5] ~ ~ ~ [d5,f5,a5] ~ ~ ~ [e5,g5,b5] ~ [c5,e5,g5] ~ ~ ~ ~ ~>")
    .s("sawtooth")
    .lpf(slider(3000, 1500, 5500))
    .attack(slider(0.02, 0.01, 0.08))
    .decay(slider(0.2, 0.1, 0.4))
    .gain(slider(0.48, 0, 2))
    .room(slider(0.25, 0, 0.6))
    .sometimes(x => x.note("<[d5,f5,a5] ~ ~ ~>"))  // Variation
    .rarely(x => x.fast(2).gain(0.4))  // Double stab
    .color("orange")
    ._punchcard()
    .pianoroll({ fold: 1 })
