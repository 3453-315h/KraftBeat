// @name Pianoroll Demo
// @genre Experimental
// @bpm 120
// @tags pianoroll, visualization, melody, showcase

setcpm(120 / 4)

// ═══════════════════════════════════════════════════════════════
// PIANOROLL DEMO - Visual showcase with melodic elements
// ═══════════════════════════════════════════════════════════════

// Main melody with clear visualization
$melody: note("<c4 e4 g4 b4> <d4 f4 a4 c5>")
    .s("triangle")  // Clear tone
    .lpf(2500)
    .slow(slider(4.0, 1, 16))
    .decay(0.3)
    .gain(slider(0.65, 0, 2))
    .room(slider(0.3, 0, 0.8))
    .pianoroll({ fold: 1 })
    ._punchcard()

// Arpeggiated synth flowing up and down
$arp: note("c3 e3 g3 b3 c4 b3 g3 e3")
    .s("sawtooth")
    .lpf(sine.range(800, 3000).slow(slider(4.0, 1, 16)))
    .decay(slider(0.15, 0.05, 0.3))
    .gain(slider(0.45, 0, 1.5))
    .fast(slider(4.0, 1, 16))
    .jux(rev)  // Stereo mirror
    .color("cyan")
    ._punchcard()

// Walking bass line
$bass: note("<c2 g1 a1 f1>")
    .s("sawtooth")
    .lpf(sine.range(300, 1000).slow(slider(8, 4, 16)))
    .decay(0.2)
    .gain(slider(0.75, 0, 2))
    .slow(slider(4.0, 1, 16))
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Standard visual drums
$kick: s("bd*4").bank("RolandTR909")
    .gain(slider(0.9, 0, 2))
    .color("orange")
    ._punchcard()

$hat: s("[~ hh]*4").bank("RolandTR909")
    .gain(slider(0.35, 0, 1.2))
    .color("white")
    ._punchcard()

$snare: s("~ sd").bank("RolandTR909")
    .gain(slider(0.8, 0, 2))
    .room(0.2)
    .color("yellow")
    ._punchcard()

// Chord pad backdrop
$pad: note("<[c3,e3,g3] [f3,a3,c4]>")
    .s("sine")
    .lpf(1200)
    .attack(0.5)
    .release(0.5)
    .gain(slider(0.3, 0, 1))
    .slow(4)
    .color("purple")
