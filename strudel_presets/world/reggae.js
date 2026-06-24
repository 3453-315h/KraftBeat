// @name Reggae One Drop
// @genre World
// @bpm 72
// @tags reggae, dub, roots, one-drop, jamaica

setcpm(72 / 4)

// ═══════════════════════════════════════════════════════════════
// REGGAE ONE DROP - Classic roots reggae with dub elements
// ═══════════════════════════════════════════════════════════════

// Classic one-drop - kick and snare together on beat 3
$kick: s("~ ~ bd ~").bank("RolandTR808")
    .gain("<1.0 0.95 0.98 0.92>")  // Subtle dynamics
    .shape(slider(0.15, 0, 0.4))
    .nudge(0.02)  // Laid-back feel
    .every(8, x => x.s("~ ~ bd [~ bd]"))  // Variation
    .color("orange")
    ._punchcard()

// Snare with big room on 3
$snare: stack(
    s("~ ~ sd ~").gain(slider(0.88, 0, 2)).room(0.45),  // Big reggae reverb
    s("~ ~ ~ [sd:3 ~]").gain(0.22).lpf(4000)  // Ghost
).bank("RolandTR808")
    .nudge(0.02)  // Laid-back
    .every(8, x => x.s("~ ~ sd [sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Cross-stick on offbeats with variations
$rim: s("~ rim ~ rim").bank("RolandTR808")
    .gain(perlin.range(0.42, 0.58))  // Velocity variation
    .sometimes(x => x.s("rim ~ rim ~"))  // Pattern shift
    .rarely(x => x.s("[~ rim] rim [~ rim] rim"))  // Syncopation
    ._punchcard()

// Hats - relaxed offbeat feel
$hat: s("[~ hh] [~ hh] [~ oh] [~ hh]").bank("RolandTR808")
    .gain(perlin.range(0.3, 0.42))  // Humanized
    .nudge(perlin.range(0.01, 0.03))  // Laid-back timing
    .pan(perlin.range(-0.15, 0.15).slow(0.5))
    .sometimes(x => x.s("[hh ~] [~ hh] [oh ~] [~ hh]"))  // Variation
    .every(8, x => x.s("[~ hh] [hh hh] [~ oh] [hh hh]"))  // Fill
    ._punchcard()

// OFFBEAT SKANK - THE signature reggae sound
$skank: note("<[c4,eb4,g4] [c4,eb4,g4] [f4,ab4,c5] [f4,ab4,c5]>")
    .s("sawtooth")
    .lpf(slider(2000, 800, 4000))
    .struct("~ x ~ x ~ x ~ x")
    .decay(slider(0.06, 0.02, 0.15))
    .gain(slider(0.52, 0, 2))
    .room(slider(0.15, 0, 0.5))
    .sometimes(x => x.note("<[d4,f4,ab4] [eb4,g4,bb4]>"))  // Chord variation
    .rarely(x => x.struct("[~ x] x [~ x] x"))  // Syncopation
    .color("lime")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Deep dub bass with delays - foundation
$bass: note("<c2 ~ ~ ~ eb2 ~ c2 ~ g1 ~ ~ ~ f2 ~ eb2 ~>")
    .s("sine")
    .lpf(slider(600, 150, 1200))
    .decay(slider(0.25, 0.12, 0.5))
    .gain(slider(0.88, 0, 2))
    .delay(slider(0.18, 0, 0.5))
    .delaytime(0.375)  // Triplet dub delay
    .room(slider(0.4, 0, 1))
    .rarely(x => x.note("<c2 eb2 ~ ~ eb2 c2 g1 ~ g1 ab1 ~ ~ f2 eb2 c2 ~>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })

// Sub layer
$sub: note("<c1 ~ ~ ~ eb1 ~ c1 ~ g0 ~ ~ ~ f1 ~ ~ ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.5, 0, 1.3))
    .color("darkred")

// Organ bubble - classic reggae organ
$organ: note("<c4 eb4 g4 c5 eb5 c5 g4 eb4>")
    .s("triangle")  // Organ-like
    .lpf(slider(3000, 800, 5500))
    .struct("x(7,16)")  // Bubble pattern
    .decay(0.15)
    .room(slider(0.3, 0, 0.8))
    .gain(slider(0.42, 0, 2))
    .sometimes(x => x.note("<c4 g4 eb4 c5 g4 eb4 c4 g3>"))  // Variation
    .color("cyan")
    ._punchcard()

// Melodica for that authentic roots feel
$melodica: note("<c5 ~ eb5 ~ g5 ~ eb5 ~ c5 ~ ~ ~ ~ ~ ~ ~>")
    .s("triangle")
    .lpf(slider(4000, 1500, 7000))
    .decay(slider(0.3, 0.15, 0.6))
    .room(slider(0.4, 0, 0.9))
    .delay(0.2)
    .delaytime(0.375)  // Dub delay
    .gain(slider(0.38, 0, 2))
    .slow(slider(2, 1, 8))
    .sometimes(x => x.note("<eb5 g5 c6 g5 eb5 c5>"))  // Extended melody
    .color("yellow")
    ._punchcard()

// Dub FX - occasional echo stab
$dubfx: s("~ ~ ~ ~ ~ ~ ~ [cp:5 ~]")
    .delay(0.5)
    .delaytime(0.375)
    .room(0.6)
    .gain(slider(0.35, 0, 1.2))
    .slow(4)
    .color("magenta")
