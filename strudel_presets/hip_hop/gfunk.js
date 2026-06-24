// @name G-Funk
// @genre Hip Hop
// @bpm 98
// @tags west, synth, smooth, dr dre

setcpm(98 / 4)

// ═══════════════════════════════════════════════════════════════
// G-FUNK - West Coast smoothness with synth whistles
// ═══════════════════════════════════════════════════════════════

// Deep 808 kick with west coast bounce
$kick: s("bd ~ [~ bd] ~").bank("RolandTR808")
    .gain("<1.0 0.95 0.98 0.95> <0.95 0.98 1.0 0.95>")  // Dynamics
    .shape(slider(0.75, 0, 1))
    .nudge("<0 0 0.03 0>")  // Slight swing
    .every(4, x => x.s("[bd ~] ~ [~ bd] bd"))  // Variation
    .every(8, x => x.s("bd ~ [bd bd] ~ [~ bd] ~ [bd ~] bd"))  // 8-bar fill
    .color("orange")
    ._punchcard()

// G-Funk snare with gated reverb
$snare: stack(
    s("~ sd ~ sd").gain(slider(0.9, 0, 2)).room(0.4),  // Gated feel
    s("~ ~ [sd:3 ~] ~").gain(0.22).lpf(4500)  // Ghost
).bank("RolandTR808")
    .nudge("0 0.015 0 0.02")  // Swing
    .every(8, x => x.s("~ sd ~ [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Smooth rolling hats
$hat: s("[hh ~] [~ hh] [hh hh] [~ hh]").bank("RolandTR808")
    .gain(perlin.range(0.38, 0.55))  // Humanized
    .lpf(perlin.range(5000, 10000))  // Tonal variation
    .pan(perlin.range(-0.15, 0.15).slow(0.5))
    .sometimes(x => x.s("hh*8"))  // 8th note variation
    .every(8, x => x.s("[hh hh hh hh] [hh hh oh hh]"))  // Fill
    .color("white")
    ._punchcard()

// G-FUNK SYNTH WHISTLE - THE signature sound
$synth: note("<g5 ~ f5 ~ d#5 ~ d5 ~ c5 ~ d5 ~ d#5 ~ ~ ~>")
    .s("sine")
    .lpf(sine.range(3000, 8000).slow(slider(4.0, 1, 16)))
    .room(slider(0.35, 0, 1))
    .delay(0.15)
    .delaytime(0.25)
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.note("<g5 f5 d#5 d5 c5 d5 d#5 g5>"))  // Different phrase
    .rarely(x => x.add(12))  // Octave up
    .color("magenta")
    .pianoroll({ fold: 1 })
    .scope({ size: 256 })

// Counter whistle - higher register
$synth2: note("<~ ~ c6 ~ ~ ~ d6 ~>")
    .s("sine")
    .lpf(6000)
    .decay(0.15)
    .delay(0.2)
    .gain(slider(0.28, 0, 1.2))
    .color("yellow")

// Smooth G-Funk bass
$bass: note("<c2 ~ [c2 ~] ~ g2 ~ [f2 ~] ~>")
    .s("triangle")
    .lpf(sine.range(300, 600).slow(slider(4.0, 1, 16)))
    .decay(slider(0.2, 0.1, 0.4))
    .gain(slider(0.78, 0, 2))
    .rarely(x => x.note("<c2 c2 [c2 d2] g2 g2 g2 [f2 g2] c2>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ c1 ~ g1 ~ f1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.45, 0, 1.2))
    .color("darkred")

// Rhodes chords - smooth west coast feel
$rhodes: note("<[c4,e4,g4] ~ ~ ~ [f4,a4,c5] ~ ~ ~>")
    .s("triangle")  // Rhodes-like
    .lpf(sine.range(2000, 4500).slow(slider(4.0, 1, 16)))
    .decay(0.25)
    .room(slider(0.35, 0, 1))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.48, 0, 2))
    .sometimes(x => x.note("<[d4,f4,a4] ~ [e4,g4,b4] ~>"))  // Chord variation
    .color("cyan")
    ._punchcard()

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR808")
    .gain(0.4)
    .room(0.4)
    .slow(2)
