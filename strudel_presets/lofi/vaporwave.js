// @name Vaporwave
// @genre Lo-Fi
// @bpm 80
// @tags vaporwave, 80s, slowed, aesthetic

setcpm(80 / 4)

// ═══════════════════════════════════════════════════════════════
// VAPORWAVE - Slowed 80s aesthetics with dreamy textures
// ═══════════════════════════════════════════════════════════════

// Soft 808 kick - slowed feel
$kick: s("bd ~ bd ~").bank("RolandTR808")
    .gain("<0.82 0.78 0.8 0.75>")  // Soft dynamics
    .lpf(320)  // Warm roll-off
    .shape(slider(0.18, 0, 0.4))
    .every(8, x => x.s("bd ~ [bd ~] ~ [~ bd] ~ bd ~"))  // Variation
    .color("orange")
    ._punchcard()

// Gated snare with reverb
$snare: stack(
    s("~ sd ~ sd").gain(slider(0.72, 0, 2)).room(0.45),  // Big reverb
    s("~ ~ [sd:3 ~] ~").gain(0.2).lpf(3800)  // Ghost
).bank("RolandTR808")
    .every(8, x => x.s("~ sd ~ [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Offbeat hats - dreamy feel
$hat: s("[~ hh] hh [~ hh] hh").bank("RolandTR808")
    .gain(perlin.range(0.28, 0.42))  // Humanized
    .lpf(perlin.range(4000, 8000))  // Filter
    .pan(perlin.range(-0.15, 0.15).slow(0.5))
    .sometimes(x => x.s("[hh ~] hh [~ hh] [~ hh]"))  // Variation
    .every(8, x => x.s("[hh hh] [~ hh] [hh hh hh hh] [oh hh]"))  // Fill
    .color("white")
    ._punchcard()

// Slowed 80s supersaw chords - THE vaporwave sound
$chords: note("<[c4,e4,g4,b4] [c4,e4,g4,b4] [f4,a4,c5,e5] [g4,b4,d5,f5]>")
    .s("sawtooth")
    .lpf(sine.range(1200, 4000).slow(slider(8, 4, 16)))
    .lpq(sine.range(0.5, 2).slow(16))  // Subtle resonance
    .attack(slider(0.15, 0.05, 0.35))
    .release(slider(0.45, 0.2, 0.9))
    .room(slider(0.48, 0, 1))
    .delay(0.18)
    .delaytime(0.375)
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.note("<[d4,f4,a4,c5] [e4,g4,b4,d5]>"))  // Chord variation
    .color("purple")
    ._punchcard()
    .pianoroll({ fold: 1 })
    .scope({ size: 256 })

// Second pad layer for thickness
$pad2: note("<[g3,c4] [f3,a3] [g3,b3] [g3,c4]>")
    .s("triangle")
    .lpf(2200)
    .attack(0.25)
    .release(0.5)
    .room(0.45)
    .gain(slider(0.28, 0, 0.9))
    .slow(slider(4.0, 1, 16))
    .color("cyan")

// Slowed bass - warm and deep
$bass: note("<c2 ~ f2 ~ g2 ~ f2 ~>")
    .s("triangle")
    .lpf(sine.range(280, 550).slow(slider(8, 4, 16)))
    .decay(slider(0.2, 0.1, 0.4))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.72, 0, 2))
    .rarely(x => x.note("<c2 c2 [f2 e2] f2 g2 g2 [f2 e2] c2>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ f1 ~ g1 ~ f1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.42, 0, 1.2))
    .color("darkred")

// Arpeggios with jux stereo - signature vaporwave
$arp: note("<c5 e5 g5 b5 g5 e5 c5 e5>")
    .s("sine")
    .lpf(sine.range(2500, 6000).slow(slider(8, 4, 16)))
    .decay(0.15)
    .delay(slider(0.28, 0.1, 0.5))
    .delaytime(0.375)
    .room(slider(0.4, 0, 0.9))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.42, 0, 1.5))
    .jux(rev)  // Stereo reversal
    .sometimes(x => x.note("<c5 g5 e5 b5 a5 e5 c5 e5>"))  // Variation
    .rarely(x => x.fast(2).gain(0.35))  // Double-time
    .color("lime")
    ._punchcard()

// VHS texture - degraded audio feel
$vhs: s("[rim:5 rim:5]*4")
    .gain(perlin.range(0.1, 0.22))
    .lpf(perlin.range(2000, 5000))
    .hpf(300)
    .pan(perlin.range(-0.4, 0.4))
    .color("gray")

// High shimmer layer
$shimmer: note("<~ ~ g6 ~ ~ ~ e6 ~>")
    .s("sine")
    .lpf(7000)
    .decay(0.5)
    .delay(0.35)
    .room(0.5)
    .gain(slider(0.18, 0, 0.6))
    .slow(8)
    .color("yellow")
