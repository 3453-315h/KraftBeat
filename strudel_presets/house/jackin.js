// @name Jackin
// @genre House
// @bpm 127
// @tags jackin, funky, chicago, energetic

setcpm(127 / 4)

// ═══════════════════════════════════════════════════════════════
// JACKIN HOUSE - High energy Chicago funk
// ═══════════════════════════════════════════════════════════════

// Punchy kick with jackin dynamics
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.05 1 1.02 1> <1 1 1.05 [1.08 1]>")  // Energy dynamics
    .shape(slider(0.32, 0, 0.7))
    .every(4, x => x.s("[bd bd] bd bd bd"))  // 4-bar punch
    .every(8, x => x.s("bd bd bd bd [bd bd] bd bd"))  // 8-bar phrase
    .color("orange")
    ._punchcard()

// Rolling 16th hats with jackin energy
$hat: s("hh*16").bank("RolandTR909")
    .gain(perlin.range(0.38, 0.55))  // Energetic velocity
    .pan(perlin.range(-0.1, 0.1).slow(0.25))
    .sometimes(x => x.s("[hh*4] [hh hh oh hh] [hh*4] [hh hh hh oh]"))  // Open hat accents
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh oh hh*4]"))  // Fill
    ._punchcard()

// Jackin clap with slapback
$clap: stack(
    s("~ cp ~ cp").gain(slider(0.9, 0, 2)).room(0.3),
    s("~ [cp:3 ~] ~ ~").gain(0.25).lpf(5000)  // Ghost
).bank("RolandTR909")
    .delay(slider(0.1, 0, 0.3))
    .delaytime(0.125)  // Slapback
    .every(8, x => x.s("~ cp ~ [cp cp cp cp]"))  // Fill
    .color("yellow")
    ._punchcard()

// Ride cymbal with jackin pattern
$ride: s("[~ rd] [rd ~] [~ rd] rd").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.5))  // Velocity variation
    .sometimes(x => x.s("[rd ~] [~ rd] [rd rd] ~"))  // Pattern variation
    .every(4, x => x.s("rd rd [~ rd] [rd rd]"))  // Fill
    .color("white")
    ._punchcard()

// Jackin bassline with octave energy
$bass: note("<c2 ~ [c2 c3] ~ g2 ~ [f2 g2] ~>")
    .s("sawtooth")
    .lpf(sine.range(350, 900).slow(slider(4.0, 1, 16)))
    .decay(slider(0.1, 0.03, 0.22))
    .gain(slider(0.82, 0, 2))
    .rarely(x => x.note("<c2 c3 [c2 d2] c3 g2 g3 [f2 g2] f3>"))  // More octave jumps
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ c1 ~ g1 ~ f1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.45, 0, 1.2))
    .color("darkred")

// Funky stab with variations
$stab: note("<[c4,e4,g4] ~ ~ ~ [f4,a4,c5] ~ [g4,b4,d5] ~>")
    .s("square")
    .lpf(sine.range(2500, 5500).slow(slider(4.0, 1, 16)))
    .decay(slider(0.12, 0.04, 0.25))
    .room(slider(0.25, 0, 0.6))
    .gain(slider(0.58, 0, 2))
    .sometimes(x => x.note("<[d4,f4,a4] ~ ~ ~>"))  // Chord variation
    .rarely(x => x.fast(2).gain(0.5))  // Double stab
    .color("cyan")
    ._punchcard()

// Shaker for energy
$shaker: s("shaker*16")
    .gain(perlin.range(0.2, 0.32))
    .pan(perlin.range(-0.3, 0.3).slow(0.25))
    .color("gray")

// Tom for fills
$tom: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ tom tom ~ ~").bank("RolandTR909")
    .gain(slider(0.4, 0, 1.5))
    .room(0.2)
    .every(4, x => x.s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ tom ~ tom tom tom ~"))  // Extended
    .color("brown")

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.45)
    .room(0.35)
    .slow(2)
