// @name Slider Control
// @genre Experimental
// @bpm 128
// @tags interactive, filter, showcase, modulation

setcpm(128 / 4)

// ═══════════════════════════════════════════════════════════════
// SLIDER CONTROL - Showcase for interactive parameter control
// ═══════════════════════════════════════════════════════════════

// Main synth with heavy filter modulation attached to sliders
$synth: note("c3 e3 g3 c4 e4 g4 e4 c4")
    .s("sawtooth")
    .lpf(sine.range(100, 5000).slow(slider(4.0, 1, 16)))
    .lpq(slider(2, 0, 15))  // Resonance control
    .room(slider(0.35, 0, 1))
    .decay(slider(0.2, 0.05, 0.8))
    .gain(slider(0.65, 0, 2))
    .pan(sine.range(-0.5, 0.5).slow(slider(2, 0.5, 8)))
    .color("magenta")
    ._punchcard()
    .pianoroll({ fold: 1 })
    .scope({ size: 256 })

// Bass foundation
$bass: note("<c2 g1 f1 g1>")
    .s("sine")
    .gain(slider(0.85, 0, 2))
    .slow(slider(4.0, 1, 16))
    .scope({ size: 256 })
    .duck("4:8")
    .duckdepth(0.6)
    .color("red")
    ._punchcard()

// Interactive drums
$hat: s("[~ hh]*4").bank("RolandTR909")
    .gain(slider(0.45, 0, 2))
    .lpf(sine.range(3000, 12000).slow(slider(8, 2, 16)))
    .decay(slider(0.1, 0.05, 0.5))
    ._punchcard()

$kick: s("bd*4").bank("RolandTR909")
    .gain(slider(1.0, 0, 2))
    .shape(slider(0.3, 0, 1))
    ._punchcard()

$clap: s("~ cp").bank("RolandTR909")
    .room(slider(0.3, 0, 1))
    .gain(slider(0.75, 0, 2))
    .delay(slider(0.2, 0, 0.5))
    .delaytime(0.25)
    ._punchcard()

// Arp layer
$arp: note("c4 e4 g4 b4")
    .s("square")
    .lpf(slider(4000, 500, 10000))
    .speed(slider(1, 0.5, 2))  // Speed control
    .gain(slider(0.35, 0, 1))
    .jux(rev)
    .color("cyan")
