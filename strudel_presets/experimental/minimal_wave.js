// @name Minimal Wave
// @genre Experimental
// @bpm 115
// @tags minimal, wave, cold, analog

setcpm(115 / 4)

// ═══════════════════════════════════════════════════════════════
// MINIMAL WAVE - Cold analog synthesis and motorik beats
// ═══════════════════════════════════════════════════════════════

// Motorik kick - steady pulse
$kick: s("bd*4").bank("RolandTR808")
    .gain("<0.95 0.92 0.95 0.98>")  // Slight dynamics
    .lpf(800)  // Darker kick
    .shape(slider(0.2, 0, 0.4))
    .color("orange")
    ._punchcard()

// Snare - dry and tight
$snare: s("~ sd ~ sd").bank("RolandTR808")
    .gain(slider(0.85, 0, 2))
    .room(slider(0.15, 0, 0.4))  // Small room
    .lpf(4000)
    .every(16, x => x.s("~ sd ~ [sd sd]"))  // Rare fill
    .color("white")
    ._punchcard()

// Hats - mechanical
$hat: s("[~ hh] hh [~ hh] hh").bank("RolandTR808")
    .gain(slider(0.65, 0, 2))
    .decay(0.05)  // Short decay
    .pan(slider(0.2, -0.2, 0.2))
    .color("lightgray")
    ._punchcard()

// Cold synth lead - square wave
$synth: note("<c4 c4 [c4 d4] d#4>")
    .s("square")
    .lpf(sine.range(800, 3000).slow(slider(8, 4, 16)))
    .width(0.5)  // Square width
    .decay(slider(0.15, 0.05, 0.3))
    .room(slider(0.25, 0, 0.6))
    .gain(slider(0.65, 0, 2))
    .sometimes(x => x.note("<f4 g4 d#4 c4>"))  // Variation
    .color("magenta")
    ._punchcard()
    .pianoroll({ fold: 1 })
    .scope({ size: 256 })

// Minimal bass - arpeggiated octave
$bass: note("<c2 c3 c2 d#2>")
    .s("sawtooth")
    .lpf(sine.range(300, 1200).slow(slider(8, 4, 16)))
    .decay(slider(0.12, 0.05, 0.25))
    .gain(slider(0.8, 0, 2))
    .struct("x*2")  // Eighth notes
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Cold pad - detached
$pad: note("[c3,d#3,g3]")
    .s("sawtooth")
    .lpf(sine.range(500, 2000).slow(slider(16, 8, 32)))
    .attack(slider(0.1, 0, 0.5))
    .release(slider(0.2, 0.1, 0.5))
    .struct("x(3,16)")  // Sparse
    .room(slider(0.3, 0, 0.8))
    .gain(slider(0.45, 0, 1.5))
    .color("purple")
    ._punchcard()

// Glitch texture
$glitch: s("noise:0")
    .struct("x(1,16)")
    .chop(16)
    .lpf(2000)
    .gain(slider(0.22, 0, 0.8))
    .slow(4)
    .color("cyan")
