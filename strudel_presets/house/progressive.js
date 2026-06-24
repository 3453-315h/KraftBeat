// @name Progressive
// @genre House
// @bpm 124
// @tags progressive, build, emotional, melodic

setcpm(124 / 4)

// ═══════════════════════════════════════════════════════════════
// PROGRESSIVE HOUSE - Emotional builds and melodic journeys
// ═══════════════════════════════════════════════════════════════

// Driving kick with build dynamics
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.0 0.95 0.98 0.95> <0.95 0.98 1.0 [1.05 0.98]>")  // Dynamics
    .shape(slider(0.3, 0, 1))
    .every(8, x => x.s("bd bd bd bd [bd bd] bd bd"))  // 8-bar phrase
    .every(16, x => x.s("bd bd bd [bd bd] bd bd [bd*4] [bd*8]"))  // Build
    .every(32, x => x.s("~ ~ ~ ~ ~ ~ ~ ~"))  // Breakdown
    .color("orange")
    ._punchcard()

// Progressive hats with build tension
$hat: s("[~ hh] hh [~ hh] hh").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.5))  // Humanized
    .pan(perlin.range(-0.12, 0.12).slow(0.25))
    .sometimes(x => x.s("[hh ~] hh [~ hh] [hh hh]"))  // Variation
    .every(8, x => x.s("[hh hh] [hh hh] [hh hh hh hh] [hh oh]"))  // Fill
    .every(16, x => x.s("[hh*4] [hh*4] [hh*8] [hh*16]"))  // Build tension
    ._punchcard()

// Clap with ghost and reverb
$clap: stack(
    s("~ cp ~ cp").gain(slider(0.85, 0, 2)).room(0.35),
    s("~ [~ cp:3] ~ ~").gain(0.2).lpf(4500)  // Ghost
).bank("RolandTR909")
    .every(8, x => x.s("~ cp ~ [cp cp cp cp]"))  // Fill
    .color("yellow")
    ._punchcard()

// Snare roll for builds
$snareroll: s("~ ~ ~ ~ ~ ~ ~ ~")
    .bank("RolandTR909")
    .every(16, x => x.s("~ ~ ~ ~ ~ ~ sd [sd*4] ~ ~ ~ ~ [sd*4] [sd*8] [sd*16] [sd*32]"))
    .gain(slider(0.6, 0, 2))
    .lpf(sine.range(3000, 10000).fast(8))
    .color("white")

// Progressive arp with stereo and variations
$arp: note("<c4 e4 g4 c5 g4 e4 c4 d4>".add("<0 0 5 7>"))
    .s("triangle")
    .lpf(sine.range(1500, 5000).slow(slider(4.0, 1, 16)))
    .delay(slider(0.22, 0, 0.5))
    .delaytime(0.375)  // Triplet delay
    .room(slider(0.35, 0, 1))
    .gain(slider(0.58, 0, 2))
    .jux(rev)  // Stereo reversal
    .sometimes(x => x.note("<c4 e4 g4 b4 c5 b4 g4 e4>"))  // Variation
    .every(8, x => x.fast(2).gain(0.45))  // Double-time build
    .color("lime")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Counter arp
$arp2: note("<~ ~ g4 ~ ~ ~ e4 ~>")
    .s("sine")
    .lpf(3500)
    .decay(0.15)
    .delay(0.28)
    .room(0.3)
    .gain(slider(0.28, 0, 1.2))
    .color("yellow")

// Emotional pad with swells
$pad: note("<[c4,e4,g4,b4] [c4,e4,g4,b4] [a3,c4,e4,g4] [g3,b3,d4,f4]>")
    .s("sawtooth")
    .lpf(sine.range(800, 3500).slow(slider(8.0, 1, 16)))
    .attack(slider(0.4, 0.15, 1))
    .release(slider(0.5, 0.2, 1))
    .slow(slider(4.0, 1, 16))
    .room(slider(0.45, 0, 1))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.note("<[d4,f4,a4,c5]>"))  // Chord variation
    .color("purple")
    ._punchcard()
    .scope({ size: 256 })

// Rolling bass with movement
$bass: note("<c2 ~ [c2 ~] ~ g1 ~ [a1 b1] ~>")
    .s("sawtooth")
    .lpf(sine.range(300, 700).slow(slider(4.0, 1, 16)))
    .decay(slider(0.12, 0.04, 0.25))
    .gain(slider(0.8, 0, 2))
    .rarely(x => x.note("<c2 c2 [c2 d2] g2 g1 g1 [a1 c2] b1>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ c1 ~ g0 ~ a0 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.45, 0, 1.2))
    .color("darkred")

// Crash for drops
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.5)
    .room(0.5)
    .slow(2)

// Reverse crash for builds
$revcr: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ cp:5")
    .gain(0.45)
    .speed(-1)
    .room(0.6)
    .slow(4)
