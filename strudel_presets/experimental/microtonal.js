// @name Microtonal
// @genre Experimental
// @bpm 100
// @tags microtonal, quarter, turkish, maqam

setcpm(100 / 4)

// ═══════════════════════════════════════════════════════════════
// MICROTONAL - Quarter tone scales and detuned drones
// ═══════════════════════════════════════════════════════════════

// Microtonal melody (quarter tones via detune - Maqam Bayati-ish flavor)
// E half-flat and B half-flat
$melody: note("<d4 e4 f4 g4 a4 b4 c5 d5>")
    .s("sawtooth")
    .detune("<0 -50 0 0 0 -50 0 0>")  // Quarter tone flat on E and B
    .lpf(sine.range(800, 3500).slow(slider(8, 4, 16)))
    .attack(0.02)
    .decay(slider(0.25, 0.1, 0.5))
    .room(slider(0.35, 0, 0.8))
    .gain(slider(0.55, 0, 2))
    .struct("x(11,16)")
    .sometimes(x => x.note("<g4 a4 b4 c5 d5 c5 b4 a4>"))
    .rarely(x => x.fast(1.5))  // Ornamentation
    .color("cyan")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Drone with beating interference
$drone1: note("d3")
    .s("sawtooth")
    .lpf(sine.range(300, 900).slow(slider(16, 8, 32)))
    .detune(slider(5.0, 0, 15))  // Adjustable beating
    .attack(2)
    .release(2)
    .slow(slider(8, 4, 16))
    .gain(slider(0.35, 0, 1.2))
    .color("purple")
    .scope({ size: 256 })

// Second drone layer
$drone2: note("a2")
    .s("sawtooth")
    .lpf(sine.range(200, 600).slow(24))
    .detune(-5)
    .attack(2)
    .gain(slider(0.28, 0, 1))
    .slow(16)
    .color("magenta")

// Standard percussion with odd meter feel
$kick: s("bd ~ [~ bd] ~").bank("RolandTR808")
    .gain("<0.92 0.88 0.95 0.9>")
    .shape(slider(0.25, 0, 0.5))
    .nudge(perlin.range(-0.01, 0.015))
    .every(8, x => x.s("bd ~ bd [~ bd]"))
    .color("orange")
    ._punchcard()

$rim: s("~ rim ~ rim").bank("RolandTR808")
    .gain(perlin.range(0.42, 0.55))
    .pan(slider(0.2, -0.3, 0.3))
    .sometimes(x => x.s("~ rim [rim ~] rim"))
    .color("yellow")
    ._punchcard()

$hat: s("hh*8").bank("RolandTR808")
    .gain(perlin.range(0.3, 0.45))
    .pan(perlin.range(-0.1, 0.1).slow(0.5))
    .every(4, x => x.gain(0.4))
    .color("white")
    ._punchcard()

// Bass line tracking root
$bass: note("<d2 ~ ~ ~ g1 ~ a1 ~>")
    .s("sine")
    .lpf(200)
    .decay(slider(0.25, 0.1, 0.45))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.75, 0, 2))
    .scope({ size: 256 })
    .color("red")
    ._punchcard()
