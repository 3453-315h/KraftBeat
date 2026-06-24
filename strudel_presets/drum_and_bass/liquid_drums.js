// @name Liquid Drums
// @genre Drum and Bass
// @bpm 170
// @tags smooth, rolling, melodic, soulful

setcpm(170 / 4)

// ═══════════════════════════════════════════════════════════════
// LIQUID DnB - Smooth rolling drums with melodic elements
// ═══════════════════════════════════════════════════════════════

// Two-step kick pattern with dynamics
$kick: s("bd ~ ~ ~ bd ~ ~ ~").bank("RolandTR909")
    .gain("<1.0 0.95 0.98 0.92> <0.95 0.92 1.0 0.95>")  // Smooth dynamics
    .shape(slider(0.25, 0, 0.5))
    .every(8, x => x.s("bd ~ ~ ~ bd ~ [~ bd] ~"))  // Variation
    .every(16, x => x.s("bd ~ ~ bd bd ~ ~ ~ bd ~ ~ ~ bd ~ bd ~"))  // 16-bar variation
    .color("orange")
    ._punchcard()

// Snare with ghost notes and space
$snare: stack(
    s("~ ~ sd ~ ~ ~ sd ~").gain(slider(0.85, 0, 2)).room(0.35),
    s("~ ~ ~ [sd:3 ~] ~ ~ ~ [~ sd:3]").gain(0.25).lpf(4500)  // Ghosts
).bank("RolandTR909")
    .every(8, x => x.s("~ ~ sd ~ ~ ~ sd [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Liquid rolling hats with stereo movement
$hat: s("hh*16").bank("RolandTR909")
    .gain(perlin.range(0.32, 0.48))  // Humanized
    .pan(sine.range(-0.35, 0.35).slow(2))  // Smooth stereo sweep
    .lpf(perlin.range(5000, 10000))
    .sometimes(x => x.s("[hh*4] [hh hh oh hh] [hh*4] [hh hh hh oh]"))  // Accents
    .every(8, x => x.fast(1.5).gain(0.4))  // Triplet roll
    ._punchcard()

// Ride for energy
$ride: s("~ ~ ~ ~ ~ ~ rd ~").bank("RolandTR909")
    .gain(slider(0.4, 0, 1.2))
    .room(0.2)
    .sometimes(x => x.s("rd*8").gain(0.3))  // Ride layer
    .color("gray")

// Smooth rolling bass with movement
$bass: note("<c2 ~ [c2 d2] ~ e2 ~ [d2 c2] ~>")
    .s("sawtooth")
    .lpf(sine.range(300, 800).slow(slider(4.0, 1, 16)))
    .lpq(sine.range(1, 4).slow(8))  // Gentle resonance
    .decay(slider(0.15, 0.06, 0.3))
    .gain(slider(0.78, 0, 2))
    .rarely(x => x.note("<c2 d2 [e2 d2] c2 e2 f2 [e2 d2] c2>"))  // Walking variation
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ c1 ~ e1 ~ d1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.5, 0, 1.3))
    .color("darkred")

// Liquid pad - smooth chords
$pad: note("<[c4,e4,g4] [d4,f4,a4] [e4,g4,b4] [d4,f4,a4]>")
    .s("sawtooth")
    .lpf(sine.range(1200, 3000).slow(slider(8.0, 1, 16)))
    .attack(slider(0.4, 0.15, 0.9))
    .release(slider(0.5, 0.2, 1))
    .room(slider(0.45, 0, 1))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.48, 0, 2))
    .sometimes(x => x.note("<[e4,g4,b4] [f4,a4,c5]>"))  // Chord variation
    .color("purple")
    .scope({ size: 256 })

// Arp layer for liquid feel
$arp: note("<c5 e5 g5 e5 d5 f5 a5 f5>")
    .s("triangle")
    .lpf(sine.range(3000, 6000).slow(4))
    .decay(0.15)
    .delay(0.25)
    .delaytime(0.375)  // Triplet delay
    .room(0.3)
    .gain(slider(0.32, 0, 1.2))
    .sometimes(x => x.rev())  // Reverse arp
    .color("cyan")
    ._punchcard()

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.45)
    .room(0.45)
    .slow(2)
