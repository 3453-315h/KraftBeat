// @name Disco Filter
// @genre House
// @bpm 118
// @tags filter, funky, uplifting, disco

setcpm(118 / 4)

// ═══════════════════════════════════════════════════════════════
// DISCO FILTER - French house vibes with sweeping filters
// ═══════════════════════════════════════════════════════════════

// Four-on-floor disco kick with subtle dynamics
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.02 0.98 1.0 0.98> <0.98 1.0 1.02 0.98>")  // Subtle dynamics
    .shape(slider(0.25, 0, 0.6))
    .lpf(300)  // Warm disco kick
    .every(16, x => x.s("bd bd bd [~ bd] bd bd [bd bd] bd"))  // Variation
    .color("orange")
    ._punchcard()

// Disco 16th hats with groove
$hat: s("hh*16").bank("RolandTR909")
    .gain("<0.38 0.48 0.4 0.5 0.38 0.48 0.42 0.52>")  // Disco groove velocity
    .pan(perlin.range(-0.12, 0.12).slow(0.25))
    .sometimes(x => x.s("[hh*4] [hh hh oh hh] [hh*4] [hh hh hh oh]"))  // Open hat accents
    .every(8, x => x.s("[hh*4] [hh*4] [hh hh oh hh hh hh] [hh oh]"))  // Fill
    ._punchcard()

// Funky clap with slapback
$clap: stack(
    s("~ cp ~ cp").gain(slider(0.82, 0, 2)).room(0.3),
    s("~ [~ cp:3] ~ ~").gain(0.2).lpf(4500)  // Ghost clap
).bank("RolandTR909")
    .delay(0.1)
    .delaytime(0.125)  // Slapback
    .every(8, x => x.s("~ cp ~ [cp cp cp cp]"))  // Fill
    .color("yellow")
    ._punchcard()

// Shaker for groove
$shaker: s("shaker*16")
    .gain(perlin.range(0.18, 0.28))
    .pan(perlin.range(-0.35, 0.35).slow(0.25))
    .color("gray")

// Disco-style filtered chords - THE SIGNATURE
$chords: note("<[c4,e4,g4,b4] [c4,e4,g4,b4] [f4,a4,c5,e5] [g4,b4,d5,f5]>")
    .s("sawtooth")
    .lpf(sine.range(400, 6000).slow(slider(4.0, 1, 16)))  // Big filter sweep
    .lpq(sine.range(2, 8).slow(8))  // Resonance movement
    .attack(slider(0.02, 0, 0.1))
    .release(slider(0.3, 0.1, 0.6))
    .room(slider(0.3, 0, 1))
    .gain(slider(0.65, 0, 2))
    .jux(x => x.lpf(3500))  // Stereo filter difference
    .sometimes(x => x.note("<[d4,f4,a4,c5] [e4,g4,b4,d5]>"))  // Chord variation
    .color("purple")
    ._punchcard()
    .pianoroll({ fold: 1 })
    .scope({ size: 256 })

// Counter chord layer - upper voicing
$chords2: note("<[g4,c5] ~ [a4,d5] ~ [b4,e5] ~ [d5,g5] ~>")
    .s("triangle")
    .lpf(sine.range(2000, 5000).slow(8))
    .decay(0.2)
    .delay(0.15)
    .room(0.25)
    .gain(slider(0.25, 0, 1.2))
    .color("cyan")

// Funky bass with octave jumps
$bass: note("<c2 c2 [c2 c3] c2 f2 f2 [f2 g2] g2>")
    .s("square")
    .lpf(sine.range(350, 900).slow(slider(4.0, 1, 16)))
    .decay(slider(0.12, 0.04, 0.25))
    .gain(slider(0.78, 0, 2))
    .rarely(x => x.note("<c2 c3 [c2 d2] c3 f2 f3 [g2 g1] g2>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: note("<c1 c1 c1 c1 f1 f1 g1 g1>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.4, 0, 1.2))
    .slow(2)
    .color("darkred")

// Tom fills for disco flavor
$tom: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ tom tom ~ ~").bank("RolandTR909")
    .gain(slider(0.4, 0, 1.5))
    .room(0.25)
    .every(4, x => x.s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ tom ~ tom tom tom ~"))  // Extended fill
    .color("brown")

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.45)
    .room(0.4)
    .slow(2)
