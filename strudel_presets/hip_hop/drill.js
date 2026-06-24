// @name Drill
// @genre Hip Hop
// @bpm 140
// @tags drill, dark, sliding, uk

setcpm(140 / 4)

// ═══════════════════════════════════════════════════════════════
// DRILL - Dark sliding 808s with syncopated patterns
// ═══════════════════════════════════════════════════════════════

// Syncopated drill kick pattern with dynamics
$kick: s("bd ~ ~ ~ ~ ~ ~ ~ bd ~ ~ ~ bd ~ ~ ~").bank("RolandTR808")
    .gain("<1.15 1.1 1.12 1.08> <1.1 1.08 1.15 1.1>")  // Dynamics
    .shape(slider(0.35, 0, 0.7))
    .every(4, x => x.s("bd ~ ~ ~ ~ ~ bd ~ bd ~ ~ ~ bd ~ ~ ~"))  // Variation
    .every(8, x => x.s("bd ~ ~ bd ~ ~ ~ ~ bd ~ ~ ~ bd ~ bd bd"))  // 8-bar fill
    .color("orange")
    ._punchcard()

// Drill hat rolls with triplet feel
$hat: s("[hh hh hh] [hh hh [hh hh hh]] [hh hh hh] [hh [hh hh] hh]").bank("RolandTR808")
    .gain(perlin.range(0.35, 0.52))  // Humanized velocity
    .pan(perlin.range(-0.25, 0.25).slow(0.25))  // Stereo movement
    .sometimes(x => x.fast(1.5))  // Triplet rolls
    .rarely(x => x.fast(2))  // 32nd rolls
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh hh hh*8]"))  // Build
    ._punchcard()

// Drill snare with syncopation
$snare: stack(
    s("~ ~ ~ ~ sd ~ ~ ~ ~ ~ ~ ~ sd ~ [~ sd] ~").gain(slider(0.88, 0, 2)).room(0.3),
    s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ sd:3 ~ ~").gain(0.25).lpf(4500)  // Ghost
).bank("RolandTR808")
    .every(8, x => x.s("~ ~ ~ ~ sd ~ ~ ~ ~ ~ sd ~ sd ~ [sd sd] sd"))  // Fill
    .color("white")
    ._punchcard()

// Open hat accents
$oh: s("~ ~ ~ ~ ~ ~ ~ [oh ~] ~ ~ ~ ~ ~ ~ oh ~").bank("RolandTR808")
    .gain(slider(0.45, 0, 1.5))
    .sometimes(x => x.s("~ ~ ~ oh ~ ~ ~ [oh ~]"))  // Variation
    .color("lime")

// Drill sliding 808 bass - signature sound
$bass: note("<c1 ~ ~ ~ ~ ~ [c1 d1] ~ d#1 ~ ~ ~ ~ ~ [d#1 c1] ~>")
    .s("sine")
    .lpf(slider(140, 60, 220))  // Sub focus
    .decay(slider(0.4, 0.2, 0.7))  // Long slide tail
    .gain(slider(0.88, 0, 2))
    .rarely(x => x.note("<c1 ~ ~ d1 ~ ~ [d1 d#1] ~ f1 ~ ~ ~ ~ ~ [d#1 d1] c1>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Dark minor piano - drill signature
$piano: note("<[c4,d#4,g4] ~ ~ ~ ~ ~ ~ ~ [g#3,c4,d#4] ~ ~ ~ ~ ~ ~ ~>")
    .s("triangle")  // Piano-like
    .lpf(sine.range(1000, 2500).slow(slider(8, 1, 16)))
    .decay(0.3)
    .room(slider(0.4, 0, 1))
    .slow(slider(8, 1, 16))
    .gain(slider(0.52, 0, 2))
    .sometimes(x => x.note("<[d4,f4,a#4]>"))  // Variation
    .rarely(x => x.fast(2).gain(0.4))  // Double hit
    .color("cyan")
    ._punchcard()

// Dark string layer
$strings: note("[c3,d#3,g3]")
    .s("sawtooth")
    .lpf(sine.range(400, 1500).slow(16))
    .attack(0.5)
    .release(0.8)
    .room(0.4)
    .gain(slider(0.25, 0, 0.8))
    .slow(8)
    .color("purple")
    .scope({ size: 256 })

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR808")
    .gain(0.45)
    .room(0.35)
    .slow(2)
