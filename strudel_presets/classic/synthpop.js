// @name Synth Pop
// @genre Classic
// @bpm 118
// @tags synthpop, 80s, catchy, new wave

setcpm(118 / 4)

// ═══════════════════════════════════════════════════════════════
// SYNTH POP - 80s electronic pop with catchy melodies
// ═══════════════════════════════════════════════════════════════

// Four on the floor kick - essential 80s
$kick: s("bd*4").bank("RolandTR808")
    .gain("<0.98 1.02 0.95 1.05>")  // Pump dynamics
    .shape(slider(0.25, 0, 0.55))
    .every(8, x => x.s("bd bd bd [bd bd bd bd]"))  // Fill
    .color("orange")
    ._punchcard()

// Gated snare with big reverb
$snare: s("~ sd ~ sd").bank("RolandTR808")
    .gain(slider(0.85, 0, 2))
    .room(slider(0.45, 0, 0.95))  // Big 80s reverb
    .every(4, x => x.s("~ sd ~ [sd sd]"))  // Roll
    .every(8, x => x.s("~ sd ~ [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Fast 16th hats
$hat: s("hh*8").bank("RolandTR808")
    .gain(perlin.range(0.35, 0.5))  // Velocity
    .lpf(8000)
    .sometimes(x => x.s("[hh hh oh hh] [hh hh hh hh] [hh hh oh hh] [hh hh hh oh]"))
    .color("white")
    ._punchcard()

// Clap accent
$clap: s("~ ~ ~ ~ ~ ~ ~ cp").bank("RolandTR808")
    .gain(slider(0.72, 0, 2))
    .room(0.4)
    .sometimes(x => x.s("~ ~ ~ cp ~ ~ ~ cp"))  // More frequent
    .color("magenta")
    ._punchcard()

// Synth pop melody with variations
$melody: note("<c5 d5 e5 g5 e5 d5 c5 d5 e5 g5 a5 g5 e5 d5 c5 c5>")
    .s("sawtooth")
    .lpf(sine.range(2000, 5500).slow(slider(8, 4, 16)))
    .lpq(2)  // Slight resonance
    .decay(slider(0.15, 0.06, 0.3))
    .room(slider(0.32, 0, 0.85))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.note("<e5 g5 a5 g5 e5 d5 c5 d5>"))  // Variation
    .rarely(x => x.fast(2).gain(0.45))  // Double-time
    .color("yellow")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Counter melody
$counter: note("<~ ~ g5 ~ ~ ~ e5 ~ ~ ~ c5 ~ ~ ~ ~ ~>")
    .s("square")
    .lpf(4000)
    .decay(0.12)
    .delay(0.15)
    .room(0.3)
    .gain(slider(0.32, 0, 1.2))
    .slow(2)
    .color("lime")

// Arp synth - essential 80s element
$arp: note("<c4 e4 g4 c5 g4 e4 c4 e4>")
    .s("square")
    .lpf(slider(3500, 1500, 6000))
    .decay(slider(0.1, 0.04, 0.22))
    .delay(0.2)
    .delaytime(0.25)
    .gain(slider(0.42, 0, 1.5))
    .jux(rev)  // Stereo
    .sometimes(x => x.note("<c4 g4 e4 c5 g4 e4 c4 g3>"))  // Variation
    .color("cyan")
    ._punchcard()

// Bass synth with movement
$bass: note("<c2 c2 a1 g1>")
    .s("sawtooth")
    .lpf(sine.range(350, 900).slow(slider(8, 4, 16)))
    .decay(slider(0.12, 0.05, 0.25))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.78, 0, 2))
    .rarely(x => x.note("<c2 [c2 d2] a1 [g1 a1]>"))  // Walking
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ a0 g0>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.45, 0, 1.2))
    .slow(slider(4.0, 1, 16))
    .color("darkred")

// Pad with slow filter sweep
$pad: note("<[c3,e3,g3] [c3,e3,g3] [a2,c3,e3] [g2,b2,d3]>")
    .s("sawtooth")
    .lpf(sine.range(800, 2500).slow(slider(8, 4, 16)))
    .attack(slider(0.15, 0.05, 0.35))
    .release(slider(0.4, 0.15, 0.75))
    .slow(slider(4.0, 1, 16))
    .room(slider(0.45, 0, 1))
    .gain(slider(0.42, 0, 1.5))
    .sometimes(x => x.note("<[d3,f3,a3] [e3,g3,b3]>"))  // Chord variation
    .color("purple")
    ._punchcard()
    .scope({ size: 256 })
