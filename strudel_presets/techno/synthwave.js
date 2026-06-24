// @name Synthwave
// @genre Techno
// @bpm 118
// @tags synthwave, retro, 80s, outrun, nostalgia

setcpm(118 / 4)

// ═══════════════════════════════════════════════════════════════
// SYNTHWAVE - 80s nostalgia with gated drums and lush synths
// ═══════════════════════════════════════════════════════════════

// 80s style kick pattern with dynamics
$kick: s("bd ~ ~ ~ bd ~ ~ ~ bd ~ ~ ~ bd ~ bd ~").bank("RolandTR808")
    .gain("<1.05 1 1.02 1> <1 1.02 1.05 [1.08 1.02]>")  // Subtle dynamics
    .shape(slider(0.15, 0, 0.4))
    .every(8, x => x.s("bd ~ ~ ~ bd ~ bd ~ bd ~ ~ ~ bd ~ bd bd"))  // 8-bar variation
    .every(16, x => x.s("bd ~ ~ ~ bd ~ ~ ~ bd ~ bd ~ bd bd bd bd"))  // Build
    .color("orange")
    ._punchcard()

// Gated snare with BIG reverb and fills
$snare: s("~ ~ ~ ~ sd ~ ~ ~ ~ ~ ~ ~ sd ~ ~ ~").bank("RolandTR808")
    .gain(slider(0.95, 0, 2))
    .room(slider(0.5, 0, 1))  // Big 80s reverb
    .every(8, x => x.s("~ ~ ~ ~ sd ~ ~ ~ ~ ~ ~ ~ sd ~ sd sd"))  // 8-bar fill
    .every(16, x => x.s("~ ~ ~ ~ sd ~ ~ ~ ~ ~ sd ~ sd sd sd sd"))  // Build
    .color("white")
    ._punchcard()

// 16th hi-hats with gated feel
$hat: s("hh*16").bank("RolandTR808")
    .gain("<0.35 0.28 0.32 0.3> <0.28 0.32 0.35 0.3>")  // Gated velocity
    .pan(perlin.range(-0.1, 0.1).slow(0.25))  // Subtle stereo
    .sometimes(x => x.s("[hh*4] [hh*4] [hh hh oh hh] [hh*4]"))  // Open hat accent
    ._punchcard()

// Tom fills - classic 80s
$tom: s("~ ~ ~ ~ ~ ~ tom ~ ~ ~ ~ ~ ~ ~ tom ~")
    .gain(perlin.range(0.42, 0.58))  // Velocity variation
    .room(slider(0.35, 0, 0.75))
    .sometimes(x => x.s("~ ~ ~ ~ ~ ~ tom tom ~ ~ ~ ~ ~ ~ tom ~"))  // Extended fill
    .every(8, x => x.s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ tom tom tom tom"))  // 8-bar tom roll
    .color("orange")
    ._punchcard()

// Clap layer on snare
$clap: s("~ ~ ~ ~ cp ~ ~ ~ ~ ~ ~ ~ cp ~ ~ ~").bank("RolandTR808")
    .gain(0.4)
    .room(0.6)
    .color("gray")

// THE SYNTH ARP - lush, shimmering with stereo
$arp: note("<c4 e4 g4 c5 g4 e4 c4 e4>".add("<0 0 5 5 7 7 5 5>"))
    .s("sawtooth")
    .lpf(sine.range(4000, 7500).slow(8))
    .attack(slider(0.008, 0, 0.04))
    .decay(slider(0.15, 0.04, 0.35))
    .room(slider(0.38, 0, 0.8))
    .gain(slider(0.52, 0, 2))
    .jux(x => x.add(7))  // Stereo widening with 5th
    .sometimes(x => x.fast(2).gain(0.4))  // Double-time runs
    .color("cyan")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Synth bass with movement
$bass: note("<c2 ~ c2 ~ g1 ~ g1 ~ a1 ~ a1 ~ g1 ~ ~ ~>")
    .s("sawtooth")
    .lpf(sine.range(450, 800).slow(8))  // Filter movement
    .decay(slider(0.12, 0.04, 0.3))
    .gain(slider(0.85, 0, 2))
    .rarely(x => x.note("<c2 c2 g1 g1 a1 a1 [g1 a1] c2>"))  // Variation
    .scope({ size: 256 })
    .color("red")

// Sub layer
$sub: note("<c1 ~ c1 ~ g0 ~ g0 ~ a0 ~ a0 ~ g0 ~ ~ ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.4, 0, 1.2))
    .color("darkred")

// Emotional lead melody with variations
$lead: note("<g5 ~ e5 ~ c5 ~ d5 ~ e5 ~ ~ ~ g5 ~ ~ ~>")
    .s("sawtooth")
    .lpf(sine.range(5000, 8500).slow(8))
    .attack(slider(0.06, 0.01, 0.2))
    .decay(slider(0.4, 0.15, 0.8))
    .room(slider(0.45, 0, 0.9))
    .gain(slider(0.45, 0, 1.8))
    .slow(2)
    .sometimes(x => x.note("<g5 e5 c5 d5 e5 g5 c6 ~>").fast(2))  // Fast phrase
    .rarely(x => x.add(12))  // Octave up
    .color("magenta")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Lush 80s pad
$pad: note("<[c3,e3,g3,c4] [c3,e3,g3,c4] [a2,c3,e3,a3] [g2,b2,d3,g3]>")
    .s("sawtooth")
    .lpf(sine.range(700, 3200).slow(16))
    .attack(slider(0.55, 0.2, 1.2))
    .release(slider(0.7, 0.3, 1.5))
    .room(slider(0.6, 0, 1))
    .gain(slider(0.32, 0, 1.2))
    .slow(4)
    .color("purple")
    .scope({ size: 256 })

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR808")
    .gain(0.45)
    .room(0.6)
    .slow(2)
