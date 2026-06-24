// @name Chicago Classic
// @genre House
// @bpm 122
// @tags piano, chords, soulful, chicago

setcpm(122 / 4)

// ═══════════════════════════════════════════════════════════════
// CHICAGO CLASSIC - Frankie Knuckles / Marshall Jefferson feel
// ═══════════════════════════════════════════════════════════════

// Classic 909 kick with subtle dynamics
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.05 1 1.02 1> <1 1 1.05 1>")  // Subtle dynamics
    .shape(slider(0.3, 0, 1))
    .rarely(x => x.s("[bd bd:1] bd bd bd"))  // Ghost kick
    .every(16, x => x.s("bd bd bd [~ bd] bd bd [bd bd] bd"))  // Variation
    .color("orange")
    ._punchcard()

// Shuffled Chicago hi-hats with swing velocity
$hat: s("hh*16").bank("RolandTR909")
    .gain("<0.45 0.55 0.48 0.58 0.45 0.55 0.48 0.6>")  // Swing velocity
    .nudge("<0 0.025 0 0.03 0 0.025 0 0.028>")  // Shuffle timing
    .pan(perlin.range(-0.15, 0.15).slow(0.25))  // Stereo movement
    .sometimes(x => x.s("[hh ~] [hh hh] [hh ~] [hh oh]"))  // Pattern variation
    .every(8, x => x.s("[hh*4] [hh hh oh hh] [hh*4] [hh hh hh oh]"))  // Fill
    ._punchcard()

// Classic clap with ghost layering and slapback
$clap: stack(
    s("~ cp ~ cp").gain(slider(0.85, 0, 2)).room(0.35),
    s("~ [~ cp:3] ~ ~").gain(0.22).lpf(4500)  // Ghost clap
).bank("RolandTR909")
    .delay(0.08)
    .delaytime(0.125)  // Classic slapback
    .every(8, x => x.s("~ cp ~ [cp cp cp cp]"))  // 8-bar fill
    .color("yellow")
    ._punchcard()

// Open hat groove on upbeats
$oh: s("~ ~ ~ ~ ~ ~ oh ~").bank("RolandTR909")
    .gain(slider(0.45, 0, 1.5))
    .room(0.25)
    .sometimes(x => x.s("~ ~ ~ oh ~ ~ oh ~"))  // Double open hat
    .color("white")
    ._punchcard()

// Shaker texture layer
$shaker: s("shaker*16")
    .gain(perlin.range(0.12, 0.22))  // Subtle velocity
    .pan(perlin.range(-0.3, 0.3).slow(0.5))
    .lpf(perlin.range(4000, 8000))
    .color("gray")

// THE PIANO - classic Chicago chords with Rhodes feel
$piano: note("<[c4,e4,g4] [c4,e4,g4] [f4,a4,c5] [g4,b4,d5]>")
    .s("piano")
    .room(slider(0.3, 0, 1))
    .gain(slider(0.75, 0, 2))
    .slow(slider(4.0, 1, 16))
    .sometimes(x => x.note("<[c4,e4,g4] [d4,f4,a4] [e4,g4,b4] [g4,b4,d5]>"))  // Chord variation
    .rarely(x => x.fast(2).room(0.4))  // Double-chord hits
    .color("cyan")
    ._punchcard()

// Bass with movement
$bass: note("<c2 c2 f2 g2>")
    .s("sawtooth")
    .lpf(sine.range(300, 800).slow(slider(8.0, 1, 16)))
    .decay(slider(0.15, 0.05, 0.35))
    .gain(slider(0.82, 0, 2))
    .rarely(x => x.note("<c2 c2 [f2 g2] c2>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })

// Sub for weight
$sub: note("<c1 c1 f1 g1>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.4, 0, 1.2))
    .slow(slider(4.0, 1, 16))
    .color("darkred")

// Ride for energy (optional layer)
$ride: s("~ ~ ~ ~ ~ ~ ~ rd").bank("RolandTR909")
    .gain(slider(0.3, 0, 1))
    .sometimes(x => x.s("rd*8").gain(0.2))  // Ride layer builds
    .color("white")

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh:4")
    .bank("RolandTR909")
    .gain(0.4)
    .room(0.4)
    .slow(2)
