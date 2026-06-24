// @name Visual Showcase
// @genre Experimental
// @bpm 130
// @tags visualization, colors, showcase, graphics

setcpm(130 / 4)

// ═══════════════════════════════════════════════════════════════
// VISUAL SHOWCASE - High contrast patterns for visualization
// ═══════════════════════════════════════════════════════════════

// Colorful arpeggio with wide panning for visuals
$arp: note("c4 e4 g4 b4 d5 b4 g4 e4")
    .s("triangle")
    .lpf(sine.range(500, 6000).slow(slider(4.0, 1, 16)))
    .decay(slider(0.15, 0.05, 0.4))
    .gain(slider(0.65, 0, 2))
    .jux(rev)
    .pan(sine.range(-1, 1).fast(2))  // Fast visual movement
    .color("cyan")
    .fast(slider(2.0, 1, 8))
    .pianoroll({ fold: 1 })
    ._punchcard()

// Chord progression with slow scope movement
$chords: note("<[c3,e3,g3,b3] [a2,c3,e3,g3] [f2,a2,c3,f3] [g2,b2,d3,g3]>")
    .s("sawtooth")
    .lpf(sine.range(400, 3000).slow(slider(4.0, 1, 16)))
    .attack(slider(0.2, 0.05, 0.8))
    .release(slider(0.4, 0.1, 1))
    .room(slider(0.35, 0, 1))
    .gain(slider(0.55, 0, 2))
    .slow(slider(4.0, 1, 16))
    .color("purple")
    ._punchcard()
    .scope({ size: 256 })

// Bass foundation
$bass: note("<c2 a1 f1 g1>")
    .s("sawtooth")
    .lpf(slider(800, 200, 2000))
    .gain(slider(0.85, 0, 2))
    .slow(slider(4.0, 1, 16))
    .scope({ size: 128 })
    .color("red")
    ._punchcard()

// Colorful visual drums
$snare: s("~ sd ~ sd").bank("RolandTR909").room(0.3).gain(0.8).color("yellow")._punchcard()
$kick: s("bd*4").bank("RolandTR909").gain(1.0).color("orange")._punchcard()
$hat: s("hh*8").bank("RolandTR909").gain(0.4).color("white")._punchcard()
$rim: s("~ ~ rim ~").bank("RolandTR909").gain(0.6).color("lime")._punchcard()

// High contrast percussion
$perc: s("cp:5(3,8)")
    .bank("RolandTR808")
    .room(0.4)
    .gain(0.5)
    .color("pink")
    ._punchcard()

// Stabs for flashes
$stab: note("<c5 ~ g5 ~>")
    .s("square")
    .decay(0.1)
    .lpf(4000)
    .gain(slider(0.4, 0, 1))
    .color("magenta")
