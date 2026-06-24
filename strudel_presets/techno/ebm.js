// @name EBM
// @genre Techno
// @bpm 125
// @tags ebm, body, dark, synth, front242

setcpm(125 / 4)

// ═══════════════════════════════════════════════════════════════
// EBM - Electronic Body Music, dark and driving
// ═══════════════════════════════════════════════════════════════

// Deep EBM kick - syncopated pattern with dynamics
$kick: s("[bd ~ ~ ~] [bd ~ ~ ~] [bd ~ bd ~] [bd ~ ~ ~]").bank("RolandTR909")
    .gain("<1.15 1.1 1.18 1.1> <1.12 1.1 1.15 1.1>")  // Subtle dynamics
    .shape(slider(0.22, 0, 0.55))
    .every(8, x => x.s("[bd ~ ~ ~] [bd ~ bd ~] [bd ~ bd ~] [bd bd ~ ~]"))  // 8-bar variation
    .every(16, x => x.s("[bd ~ ~ ~] [bd ~ ~ ~] [bd ~ bd ~] [bd bd bd bd]"))  // Build
    .color("orange")
    ._punchcard()

// Snare with ghost notes
$snare: stack(
    s("~ ~ ~ ~ sd ~ ~ ~ ~ ~ ~ ~ sd ~ ~ ~").gain(slider(0.92, 0, 2)).room(0.2),
    s("~ ~ ~ ~ ~ ~ [sd:3 ~] ~ ~ ~ ~ ~ ~ ~ [~ sd:3] ~").gain(0.28).lpf(4500)  // Ghost snare
).bank("RolandTR909")
    .every(8, x => x.s("~ ~ ~ ~ sd ~ ~ ~ ~ ~ ~ ~ sd ~ sd sd"))  // 8-bar fill
    .color("white")
    ._punchcard()

// Driving 8th note hats with dynamics
$hat: s("hh*8").bank("RolandTR909")
    .gain(perlin.range(0.32, 0.45))  // Humanized velocity
    .pan(perlin.range(-0.1, 0.1).slow(0.25))  // Subtle stereo
    .sometimes(x => x.s("[hh hh] [hh hh] [hh hh oh] [hh hh]"))  // Open hat accent
    .every(8, x => x.s("[hh*4] [hh*4] [hh hh oh hh] [hh*8]"))  // Hat fill
    ._punchcard()

// Tom fills - classic EBM with variations
$tom: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ tom tom ~ ~")
    .gain(perlin.range(0.5, 0.68))  // Velocity variation
    .room(slider(0.25, 0, 0.6))
    .sometimes(x => x.s("~ ~ ~ ~ ~ ~ tom ~ ~ ~ ~ ~ tom tom tom ~"))  // Extended fill
    .every(8, x => x.s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ tom ~ tom tom tom tom"))  // 8-bar tom roll
    .color("orange")
    ._punchcard()

// Tom layer for depth
$tom2: s("~ ~ ~ ~ ~ ~ ~ ~ [tom:2 ~] ~ ~ ~ ~ ~ ~ ~")
    .gain(0.35)
    .lpf(400)
    .room(0.3)
    .color("brown")

// THE EBM SEQUENCE - aggressive, repetitive machine rhythm
$seq: note("<c2 c2 c2 [c3 c2] c2 c2 [d#2 c2] c2>")
    .s("sawtooth")
    .lpf(sine.range(200, 2000).fast(slider(1, 0.25, 4)))
    .lpq(sine.range(2, 8).slow(4))  // Resonance movement
    .decay(slider(0.08, 0.02, 0.2))
    .gain(slider(0.82, 0, 2))
    .rarely(x => x.fast(2))  // Machine stutter
    .every(8, x => x.note("<c2 c2 [c2 d#2] [g2 c3] c2 c2 [d#2 c2] c2>"))  // Variation
    .scope({ size: 256 })
    .color("lime")
    .pianoroll({ fold: 1 })

// Dark lead with variations
$lead: note("<c4 ~ d#4 ~ c4 ~ g3 ~ a#3 ~ c4 ~ ~ ~ ~ ~>")
    .s("square")
    .lpf(sine.range(2000, 4500).slow(8))
    .decay(slider(0.18, 0.05, 0.4))
    .room(slider(0.22, 0, 0.55))
    .gain(slider(0.48, 0, 2))
    .slow(2)
    .sometimes(x => x.note("<c4 d#4 c4 ~ g3 a#3 c4 ~>").fast(2))  // Double-time
    .rarely(x => x.note("<c4 ~ f4 ~>"))  // Melodic variation
    .color("cyan")
    ._punchcard()

// Choir pad - dark atmosphere
$pad: note("<[c3,d#3,g3] [c3,d#3,g3] [a#2,d3,f3] [c3,d#3,g3]>")
    .s("triangle")
    .lpf(sine.range(1200, 2800).slow(16))
    .attack(slider(0.4, 0.12, 0.9))
    .release(slider(0.5, 0.2, 1))
    .room(slider(0.4, 0, 0.85))
    .gain(slider(0.28, 0, 1.1))
    .slow(4)
    .color("purple")
    .scope({ size: 256 })

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.45)
    .room(0.4)
    .slow(2)
