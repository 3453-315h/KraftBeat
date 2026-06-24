// @name Massive Drop
// @genre Dubstep
// @bpm 140
// @tags complex, wobble, massive, heavy, c minor

setcpm(140 / 4)

// ═══════════════════════════════════════════════════════════════
// MASSIVE DROP - Heavy wobbles and crushing bass
// ═══════════════════════════════════════════════════════════════

// Heavy half-time kick
$kick: s("bd ~ ~ ~ bd ~ ~ ~").bank("RolandTR808")
    .gain("<1.2 1.15 1.18 1.12> <1.15 1.12 1.2 [1.25 1.15]>")  // Dynamics
    .shape(slider(0.35, 0, 0.7))
    .every(4, x => x.s("[bd ~] ~ ~ ~ bd ~ bd ~"))  // Variation
    .every(8, x => x.s("bd ~ bd ~ bd ~ [bd bd] bd"))  // Build
    .color("orange")
    ._punchcard()

// Snare on 3 with ghost layers
$snare: stack(
    s("~ ~ sd ~").gain(slider(1.0, 0, 2)).room(slider(0.25, 0, 0.6)),
    s("~ ~ ~ [sd:3 ~]").gain(0.28).lpf(5000)  // Ghost
).bank("RolandTR808")
    .every(4, x => x.s("~ ~ sd [sd sd]"))  // Roll
    .every(8, x => x.s("~ ~ sd [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Snare fills for builds
$fill: s("~ ~ ~ ~ ~ ~ ~ ~")
    .bank("RolandTR808")
    .every(8, x => x.s("~ ~ ~ ~ ~ ~ ~ [sd sd sd sd]"))
    .every(16, x => x.s("~ ~ ~ ~ ~ ~ [sd*4] [sd*8]"))
    .gain(slider(0.75, 0, 2))
    .lpf(sine.range(2500, 8000).fast(8))
    .slow(slider(4.0, 1, 16))
    .color("gray")

// Rolling hats
$hat: s("hh*16").bank("RolandTR808")
    .gain(perlin.range(0.35, 0.52))
    .lpf(perlin.range(5000, 12000))
    .pan(perlin.range(-0.12, 0.12).slow(0.25))
    .sometimes(x => x.s("[hh*4] [hh hh oh hh] [hh*4] [hh hh hh oh]"))
    .every(8, x => x.fast(1.5).gain(0.45))
    .color("white")
    ._punchcard()

// MASSIVE WOBBLE BASS
$wobble: note("<c1 c1 [c1 eb1] c1> <c1 [c1 f1] g1 c1>")
    .s("sawtooth")
    .lpf(sine.range(200, 2800).fast(slider(4.0, 1, 16)))
    .lpq(sine.range(5, 14).slow(2))  // Heavy resonance
    .decay(slider(0.12, 0.04, 0.25))
    .gain(slider(0.85, 0, 2))
    .chop(sine.range(4, 16).slow(4))  // Wobble modulation
    .rarely(x => x.note("<c1 eb1 [f1 g1] c1>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Mid bass layer with jux
$mid: note("<c2 ~ eb2 ~> <~ f2 ~ g2>")
    .s("square")
    .lpf(sine.range(500, 1800).fast(slider(2, 1, 8)))
    .lpq(8)
    .decay(slider(0.1, 0.04, 0.22))
    .gain(slider(0.48, 0, 1.8))
    .jux(x => x.lpf(1200))  // Stereo difference
    .slow(slider(4.0, 1, 16))
    .color("orange")

// Growl texture
$growl: note("c2")
    .s("sawtooth")
    .lpf(sine.range(300, 2500).fast(slider(8, 1, 16)))
    .lpq(10)
    .gain(slider(0.42, 0, 1.5))
    .chop(sine.range(4, 16).slow(2))
    .every(2, x => x.speed(2))  // Speed variation
    .color("darkred")
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ ~ ~ ~ ~ ~ ~> <~ ~ ~ ~ c1 ~ ~ ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.55, 0, 1.5))
    .color("cyan")
    .scope({ size: 256 })

// Dark pad
$pad: note("[c2,eb2,g2,c3]")
    .s("sawtooth")
    .lpf(sine.range(400, 1200).slow(slider(8.0, 1, 16)))
    .attack(slider(0.5, 0.2, 1.1))
    .release(slider(0.6, 0.25, 1.2))
    .gain(slider(0.38, 0, 1.3))
    .room(slider(0.45, 0, 1))
    .slow(slider(4.0, 1, 16))
    .sometimes(x => x.note("[eb2,g2,bb2,eb3]"))  // Chord variation
    .color("purple")
    .scope({ size: 256 })

// Riser synth
$riser: note("<c3 d3 eb3 f3 g3 a3 bb3 c4>")
    .s("sawtooth")
    .lpf(sine.range(1000, 5000).slow(slider(8.0, 1, 16)))
    .decay(slider(0.15, 0.05, 0.3))
    .gain(slider(0.42, 0, 1.5))
    .room(slider(0.35, 0, 0.8))
    .slow(slider(4.0, 1, 16))
    .sometimes(x => x.rev())  // Reverse for builds
    .color("cyan")
    ._punchcard()

// FX hit
$fx: s("~ ~ ~ ~ ~ ~ ~ [cp:5 ~]")
    .room(slider(0.4, 0, 0.9))
    .delay(slider(0.25, 0, 0.6))
    .gain(slider(0.45, 0, 1.5))
    .slow(slider(4.0, 1, 16))
    .sometimes(x => x.s("~ ~ ~ ~ ~ ~ [cp:5 cp:5] ~"))  // Double hit
    .color("magenta")
    ._punchcard()

// Crash for drops
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR808")
    .gain(0.55)
    .room(0.45)
    .slow(2)
