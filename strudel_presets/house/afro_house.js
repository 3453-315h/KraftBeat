// @name Afro House
// @genre House
// @bpm 116
// @tags african, percussion, tribal, polyrhythm

setcpm(116 / 4)

// ═══════════════════════════════════════════════════════════════
// AFRO HOUSE - Polyrhythmic percussion, organic grooves
// ═══════════════════════════════════════════════════════════════

// Deep organic kick with subtle dynamics
$kick: s("bd*4").bank("RolandTR909")
    .gain("<0.95 0.9 0.92 0.9> <0.9 0.92 0.95 0.9>")  // Subtle breathing
    .shape(slider(0.2, 0, 0.5))
    .lpf(300)  // Warm, deep
    .rarely(x => x.s("[bd bd:1] bd bd bd"))  // Ghost kick
    .every(16, x => x.s("bd bd [~ bd] bd bd bd [bd ~] bd"))  // Organic variation
    .color("orange")
    ._punchcard()

// Shuffled hats with organic feel
$hat: s("[~ hh] [~ hh] [~ hh] [~ oh]").bank("RolandTR909")
    .gain(perlin.range(0.3, 0.45))  // Humanized
    .pan(perlin.range(-0.2, 0.2).slow(0.5))
    .nudge(perlin.range(-0.01, 0.02))  // Micro-timing
    .sometimes(x => x.s("[~ hh] [hh ~] [~ hh] [oh ~]"))  // Variation
    .every(8, x => x.s("[hh ~] [~ hh] [hh hh] [oh hh]"))  // Fill
    ._punchcard()

// Warm clap with layering
$clap: stack(
    s("~ cp ~ cp").gain(slider(0.75, 0, 2)).room(0.3),
    s("~ ~ [~ cp:3] ~").gain(0.18).lpf(4000)  // Ghost
).bank("RolandTR909")
    .delay(slider(0.15, 0, 0.5))
    .every(8, x => x.s("~ cp ~ [cp cp cp cp]"))  // Fill
    .color("yellow")
    ._punchcard()

// CONGA - authentic African pattern with variations
$conga: s("conga:0 ~ [conga:1 conga:2] ~")
    .gain(perlin.range(0.42, 0.58))  // Velocity variation
    .pan(slider(0.0, -0.5, 0.5))
    .room(0.15)
    .sometimes(x => x.s("conga:0 conga:1 [conga:2 ~] conga:0"))  // Extended pattern
    .rarely(x => x.s("[conga:0 conga:1] conga:2 [conga:0 conga:1] conga:2"))  // Roll
    .color("brown")
    ._punchcard()

// Shaker with polyrhythmic feel
$shaker: s("shaker*12")  // 12/8 feel for African music
    .gain(perlin.range(0.2, 0.32))
    .pan(perlin.range(-0.4, 0.4).slow(0.25))
    .euclid(7, 12)  // Authentic African polyrhythm
    .color("gray")

// Djembe pattern - essential African character
$djembe: s("~ djembe:0 ~ [djembe:1 djembe:0]")
    .gain(perlin.range(0.5, 0.7))  // Dynamic playing
    .room(0.2)
    .sometimes(x => x.s("djembe:0 ~ [djembe:1 ~] djembe:0"))  // Variation
    .every(4, x => x.s("[djembe:0 djembe:1] djembe:0 [djembe:1 djembe:2] djembe:0"))  // Fill
    .color("orange")
    ._punchcard()

// Additional percussion - talking drum feel
$talking: s("~ ~ [tom:3 ~] ~ ~ ~ ~ tom:3").bank("RolandTR808")
    .gain(0.35)
    .lpf(800)
    .room(0.2)
    .sometimes(x => x.s("~ tom:3 [tom:2 ~] ~ ~ ~ tom:3 [~ tom:2]"))  // Call response
    .color("yellow")

// Marimba melody with organic movement
$marimba: note("<c5 d5 e5 g5 e5 d5 c5 a4>")
    .s("triangle")  // Marimba-like
    .lpf(sine.range(2500, 5000).slow(8))
    .decay(0.2)
    .room(slider(0.3, 0, 1))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.note("<c5 e5 g5 c6 g5 e5 c5 g4>"))  // Extended range
    .rarely(x => x.fast(2))  // Double-time fill
    .color("cyan")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Counter melody
$marimba2: note("<~ ~ g4 ~ ~ ~ e4 ~>")
    .s("triangle")
    .lpf(3000)
    .decay(0.15)
    .gain(0.35)
    .room(0.25)
    .color("yellow")

// Deep bass with movement
$bass: note("<c2 c2 f2 g2>")
    .s("sawtooth")
    .lpf(sine.range(200, 500).slow(slider(4.0, 1, 16)))
    .decay(slider(0.15, 0.05, 0.3))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.75, 0, 2))
    .rarely(x => x.note("<c2 f2 g2 c2>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: note("<c1 c1 f1 g1>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.4, 0, 1.2))
    .slow(slider(4.0, 1, 16))
    .color("darkred")

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh:3")
    .bank("RolandTR909")
    .gain(0.35)
    .room(0.4)
    .slow(2)
