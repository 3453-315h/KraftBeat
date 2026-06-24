// @name Soulful
// @genre House
// @bpm 121
// @tags soulful, gospel, uplifting, emotional

setcpm(121 / 4)

// ═══════════════════════════════════════════════════════════════
// SOULFUL HOUSE - Gospel chords and uplifting energy
// ═══════════════════════════════════════════════════════════════

// Warm kick with subtle dynamics
$kick: s("bd*4").bank("RolandTR909")
    .gain("<0.95 0.9 0.92 0.9> <0.9 0.92 0.95 0.9>")  // Breathing
    .shape(slider(0.22, 0, 0.5))
    .lpf(280)  // Warm character
    .every(16, x => x.s("bd bd bd [~ bd] bd bd [bd bd] bd"))  // Variation
    .color("orange")
    ._punchcard()

// Shuffled hats with swing
$hat: s("[~ hh] hh [~ hh] hh").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.5))  // Humanized velocity
    .nudge(perlin.range(-0.01, 0.02))  // Swing timing
    .pan(perlin.range(-0.15, 0.15).slow(0.5))
    .sometimes(x => x.s("[hh ~] hh [~ hh] [~ oh]"))  // Variation
    .every(8, x => x.s("[hh hh] [~ hh] [hh hh hh hh] [oh hh]"))  // Fill
    ._punchcard()

// Soulful clap with reverb tail
$clap: stack(
    s("~ cp ~ cp").gain(slider(0.8, 0, 2)).room(0.4),
    s("~ [~ cp:3] ~ ~").gain(0.2).lpf(4500)  // Ghost
).bank("RolandTR909")
    .delay(slider(0.18, 0, 0.5))
    .delaytime(0.25)  // Warm delay
    .every(8, x => x.s("~ cp ~ [cp cp cp cp]"))  // Fill
    .color("yellow")
    ._punchcard()

// Shaker for groove
$shaker: s("shaker*16")
    .gain(perlin.range(0.15, 0.25))
    .pan(perlin.range(-0.3, 0.3).slow(0.25))
    .color("gray")

// Gospel piano chords - the soul
$chords: note("<[c4,e4,g4,b4] [d4,f4,a4,c5] [e4,g4,b4,d5] [f4,a4,c5,e5]>")
    .s("triangle")  // Piano-like
    .lpf(sine.range(2000, 4500).slow(8))
    .attack(0.02)
    .decay(0.3)
    .room(slider(0.35, 0, 1))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.65, 0, 2))
    .jux(x => x.lpf(3000))  // Stereo warmth
    .sometimes(x => x.note("<[c4,e4,g4,c5] [d4,f4,a4,d5]>"))  // Variation
    .rarely(x => x.fast(2).gain(0.5))  // Double chord
    .color("purple")
    .pianoroll({ fold: 1 })
    .scope({ size: 256 })

// Counter chord - upper voicing
$chords2: note("<[g4,b4] ~ [a4,c5] ~ [b4,d5] ~ [c5,e5] ~>")
    .s("sine")
    .lpf(4000)
    .decay(0.2)
    .delay(0.15)
    .room(0.25)
    .gain(slider(0.25, 0, 1.2))
    .slow(slider(4.0, 1, 16))
    .color("cyan")

// Soulful bass with walking movement
$bass: note("<c2 ~ [c2 d2] ~ e2 ~ [d2 c2] ~>")
    .s("sawtooth")
    .lpf(sine.range(300, 650).slow(slider(4.0, 1, 16)))
    .decay(slider(0.15, 0.05, 0.3))
    .gain(slider(0.75, 0, 2))
    .rarely(x => x.note("<c2 d2 [e2 d2] c2 e2 d2 [c2 d2] e2>"))  // Walking variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ c1 ~ e1 ~ d1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.4, 0, 1.2))
    .color("darkred")

// String pad - emotional swells
$strings: note("[c3,e3,g3,b3]")
    .s("sawtooth")
    .lpf(sine.range(800, 2500).slow(slider(8.0, 1, 16)))
    .attack(slider(0.4, 0.15, 1))
    .release(slider(0.5, 0.2, 1))
    .slow(slider(4.0, 1, 16))
    .room(slider(0.45, 0, 1))
    .gain(slider(0.45, 0, 2))
    .sometimes(x => x.note("[d3,f3,a3,c4]"))  // Chord change
    .color("cyan")
    ._punchcard()
    .scope({ size: 256 })

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.4)
    .room(0.45)
    .slow(2)
