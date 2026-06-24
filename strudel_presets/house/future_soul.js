// @name Future Soul
// @genre House
// @bpm 122
// @tags soulful, ducking, chords, advanced, deep

setcpm(122 / 4)

// ═══════════════════════════════════════════════════════════════
// FUTURE SOUL - Deep house with sidechain pumping and lush chords
// ═══════════════════════════════════════════════════════════════

// Deep house kick with subtle dynamics
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.0 0.95 0.98 0.95> <0.95 0.98 1.0 0.95>")  // Breathing
    .shape(slider(0.25, 0, 0.55))
    .lpf(280)  // Warm kick
    .every(16, x => x.s("bd bd bd [~ bd] bd bd [bd bd] bd"))  // Variation
    .color("orange")
    ._punchcard()

// Shuffled hats with groove
$hat: s("[~ hh] hh [~ hh] hh").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.5))  // Humanized
    .pan(perlin.range(-0.15, 0.15).slow(0.5))
    .nudge(perlin.range(-0.01, 0.02))  // Micro-timing
    .sometimes(x => x.s("[hh ~] hh [~ hh] [~ oh]"))  // Variation
    .every(8, x => x.s("[hh hh] [~ hh] [hh hh hh hh] [oh hh]"))  // Fill
    ._punchcard()

// Clap with space
$clap: stack(
    s("~ cp ~ cp").gain(slider(0.8, 0, 2)).room(0.38),
    s("~ [~ cp:3] ~ ~").gain(0.2).lpf(4500)  // Ghost
).bank("RolandTR909")
    .delay(slider(0.2, 0, 0.5))
    .every(8, x => x.s("~ cp ~ [cp cp cp cp]"))  // Fill
    .color("yellow")
    ._punchcard()

// Open hat groove
$oh: s("~ ~ ~ ~ ~ ~ oh ~").bank("RolandTR909")
    .gain(slider(0.42, 0, 1.5))
    .room(0.25)
    .sometimes(x => x.s("~ ~ ~ oh ~ ~ oh ~"))  // Double open
    .color("white")
    ._punchcard()

// Shaker texture
$shaker: s("shaker*16")
    .gain(perlin.range(0.15, 0.25))
    .pan(perlin.range(-0.3, 0.3).slow(0.25))
    .color("gray")

// Soul chord progression - with sidechain feel
$chords: n("<[0,3,7,10] [5,8,0,3] [3,7,10,2] [7,10,2,5]>")
    .scale("f:minor7")
    .s("sawtooth")
    .lpf(sine.range(1500, 4000).slow(8))
    .lpq(sine.range(1, 4).slow(16))
    .attack(slider(0.05, 0.01, 0.2))
    .release(slider(0.4, 0.15, 0.8))
    .room(slider(0.4, 0, 1))
    .gain(slider(0.55, 0, 2))
    .slow(slider(4.0, 1, 16))
    .jux(x => x.lpf(2500))  // Stereo filtering
    .sometimes(x => x.add(7))  // Chord variation (add 5th)
    .color("purple")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Electric piano stabs - Rhodes feel
$epiano: note("<[f4,a4] ~ ~ ~ [ab4,c5] ~ [bb4,d5] ~>")
    .s("triangle")  // Rhodes-like
    .lpf(sine.range(2000, 4500).slow(8))
    .decay(0.2)
    .delay(0.18)
    .room(0.3)
    .gain(slider(0.4, 0, 1.5))
    .slow(slider(4.0, 1, 16))
    .sometimes(x => x.note("<[g4,bb4]>"))  // Variation
    .color("cyan")
    ._punchcard()

// Deep bass with movement
$bass: note("<f2 ~ [f2 ~] ~ ab2 ~ [bb2 ab2] ~>")
    .s("sawtooth")
    .lpf(sine.range(250, 550).slow(slider(4.0, 1, 16)))
    .decay(slider(0.15, 0.05, 0.3))
    .gain(slider(0.75, 0, 2))
    .rarely(x => x.note("<f2 ab2 [bb2 ab2] f2>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: note("<f1 ~ f1 ~ ab1 ~ bb1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.45, 0, 1.2))
    .slow(slider(4.0, 1, 16))
    .color("darkred")

// String pad layer - emotional swells
$strings: note("<[f3,ab3,c4] [f3,ab3,c4] [ab3,c4,eb4] [bb3,d4,f4]>")
    .s("sawtooth")
    .lpf(sine.range(600, 2000).slow(16))
    .attack(slider(0.5, 0.2, 1))
    .release(slider(0.6, 0.25, 1.1))
    .room(slider(0.5, 0, 1))
    .gain(slider(0.35, 0, 1.2))
    .slow(slider(4.0, 1, 16))
    .color("magenta")
    .scope({ size: 256 })

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.4)
    .room(0.45)
    .slow(2)
