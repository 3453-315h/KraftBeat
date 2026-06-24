// @name Chiptune
// @genre Lo-Fi
// @bpm 140
// @tags chiptune, 8bit, retro, gameboy

setcpm(140 / 4)

// ═══════════════════════════════════════════════════════════════
// CHIPTUNE - 8-bit retro gaming sounds
// ═══════════════════════════════════════════════════════════════

// 8-bit kick with punch
$kick: s("bd*4").bank("RolandTR808")
    .gain("<0.9 0.85 0.88 0.92>")  // Dynamics
    .lpf(400)  // 8-bit filtered
    .crush(8)  // Bitcrush
    .every(8, x => x.s("bd bd bd [bd bd bd bd]"))  // Fill
    .color("orange")
    ._punchcard()

// Punchy 8-bit snare
$snare: s("~ sd ~ sd").bank("RolandTR808")
    .gain(slider(0.78, 0, 2))
    .lpf(4500)
    .crush(12)  // Light bitcrush
    .room(slider(0.2, 0, 0.6))
    .every(4, x => x.s("~ sd ~ [sd sd]"))  // Roll
    .every(8, x => x.s("~ sd ~ [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Fast 8-bit hats
$hat: s("hh*8").bank("RolandTR808")
    .gain(perlin.range(0.32, 0.48))  // Velocity
    .lpf(8000)
    .sometimes(x => x.s("[hh*4] [hh hh oh hh] [hh*4] [hh hh hh oh]"))  // Accents
    .every(8, x => x.fast(2).gain(0.42))  // Build
    .color("white")
    ._punchcard()

// 8-bit melody - classic C major arpeggio style
$melody: note("<c5 d5 e5 g5 a5 g5 e5 d5 c5 e5 g5 c6 g5 e5 c5 c5>")
    .s("square")
    .lpf(slider(3500, 1500, 6000))
    .crush(choose(8, 12, 16))  // Random bitcrush
    .decay(slider(0.12, 0.05, 0.25))
    .gain(slider(0.58, 0, 2))
    .sometimes(x => x.note("<c5 e5 g5 c6 g5 e5 c5 d5>"))  // Variation
    .rarely(x => x.fast(2))  // Double-time
    .color("cyan")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Second melody layer for thickness
$melody2: note("<~ ~ g5 ~ ~ ~ e5 ~>")
    .s("square")
    .lpf(4000)
    .crush(10)
    .decay(0.1)
    .gain(slider(0.32, 0, 1.2))
    .delay(0.15)
    .color("yellow")

// Classic arpeggio with jux stereo
$arp: note("<c4 e4 g4 c5>")
    .s("square")
    .lpf(slider(3000, 1200, 5000))
    .crush(12)
    .decay(slider(0.1, 0.04, 0.22))
    .gain(slider(0.48, 0, 2))
    .jux(rev)  // Stereo separation
    .sometimes(x => x.note("<c4 g4 e4 c5 g4 e4 c4 g3>"))  // Variation
    .color("lime")
    ._punchcard()

// 8-bit bass
$bass: note("<c2 c2 a1 g1>")
    .s("square")
    .lpf(slider(600, 250, 1000))
    .crush(8)  // Heavy bitcrush
    .decay(slider(0.12, 0.05, 0.25))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.72, 0, 2))
    .rarely(x => x.note("<c2 [c2 d2] a1 [g1 a1]>"))  // Walking
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ a0 g0>")
    .s("square")
    .lpf(120)
    .crush(6)
    .gain(slider(0.42, 0, 1.2))
    .slow(slider(4.0, 1, 16))
    .color("darkred")

// Noise channel for texture - classic chiptune
$noise: s("noise:0")
    .struct("x(5,16)")
    .lpf(sine.range(2000, 8000).fast(4))
    .crush(6)
    .gain(slider(0.25, 0, 0.9))
    .pan(perlin.range(-0.3, 0.3))
    .sometimes(x => x.struct("x(7,16)"))
    .color("gray")
