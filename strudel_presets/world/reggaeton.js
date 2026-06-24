// @name Reggaeton
// @genre World
// @bpm 95
// @tags reggaeton, dembow, perreo, latin, puerto rico

setcpm(95 / 4)

// ═══════════════════════════════════════════════════════════════
// REGGAETON - Dembow rhythm with Latin bounce
// ═══════════════════════════════════════════════════════════════

// Dembow kick pattern - THE reggaeton beat
$kick: s("bd ~ ~ ~ bd ~ ~ ~ bd ~ ~ ~ bd ~ ~ ~").bank("RolandTR808")
    .gain("<1.1 1.05 1.08 1.02> <1.05 1.02 1.1 [1.15 1.05]>")  // Dynamics
    .shape(slider(0.3, 0, 0.65))
    .every(8, x => x.s("bd ~ bd ~ bd ~ ~ ~ bd ~ ~ bd bd ~ ~ ~"))  // Variation
    .color("orange")
    ._punchcard()

// Dembow snare pattern with dynamics
$snare: s("~ ~ ~ sd ~ ~ ~ sd ~ ~ ~ sd ~ ~ ~ sd").bank("RolandTR808")
    .gain(perlin.range(0.82, 0.98))  // Velocity variation
    .room(slider(0.12, 0, 0.4))
    .every(8, x => x.s("~ ~ ~ sd ~ ~ sd sd ~ ~ ~ sd ~ sd ~ sd"))  // Fill
    .color("white")
    ._punchcard()

// Hi-hat rolls with builds
$hat: s("[hh hh hh hh] [hh hh [hh hh hh hh] hh] [hh hh hh hh] [hh hh hh hh]").bank("RolandTR808")
    .gain(perlin.range(0.35, 0.5))  // Humanized
    .pan(perlin.range(-0.12, 0.12).slow(0.25))
    .sometimes(x => x.s("[hh hh hh hh] [hh hh oh hh] [hh hh hh hh] [hh oh hh hh]"))  // Accents
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh*16]"))  // Build
    ._punchcard()

// Rim shot - dembow accent with variations
$rim: s("~ rim ~ ~ ~ rim ~ ~ ~ rim ~ ~ ~ rim ~ ~").bank("RolandTR808")
    .gain(perlin.range(0.52, 0.68))  // Velocity
    .sometimes(x => x.s("rim ~ ~ ~ rim ~ ~ rim ~ rim ~ ~ rim ~ ~ ~"))  // Pattern 2
    .color("white")
    ._punchcard()

// 808 bass - bouncy and punchy
$bass: note("<c2 ~ c2 ~ eb2 ~ c2 ~ g1 ~ c2 ~ eb2 ~ g1 ~>")
    .s("sine")
    .lpf(slider(300, 100, 500))
    .decay(slider(0.18, 0.08, 0.35))
    .gain(slider(0.88, 0, 2))
    .rarely(x => x.note("<c2 c2 [c2 d2] eb2 eb2 eb2 [d2 c2] c2>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })

// Sub layer
$sub: note("<c1 ~ ~ ~ ~ ~ ~ ~ g0 ~ ~ ~ ~ ~ ~ ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.48, 0, 1.3))
    .color("darkred")

// Synth plucks - latin flavor
$pluck: note("<[c4,eb4,g4] ~ [c4,eb4,g4] ~ [f4,ab4,c5] ~ [eb4,g4,bb4] ~>")
    .s("triangle")  // Pluck-like
    .lpf(slider(4000, 1500, 7000))
    .decay(slider(0.15, 0.06, 0.35))
    .room(slider(0.15, 0, 0.5))
    .gain(slider(0.52, 0, 2))
    .sometimes(x => x.note("<[d4,f4,ab4] ~ [eb4,g4,bb4] ~>"))  // Variation
    .color("cyan")
    ._punchcard()

// Synth lead - catchy hook with variations
$lead: note("<c5 ~ eb5 ~ g5 ~ eb5 ~ c5 ~ bb4 ~ c5 ~ ~ ~>")
    .s("sawtooth")
    .lpf(slider(3000, 1500, 5500))
    .attack(slider(0.02, 0.01, 0.08))
    .decay(slider(0.2, 0.08, 0.42))
    .slow(slider(2, 1, 4))
    .gain(slider(0.48, 0, 2))
    .sometimes(x => x.note("<eb5 g5 bb5 g5 eb5 c5>"))  // Variation
    .rarely(x => x.fast(2).gain(0.4))  // Double-time
    .color("lime")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Vocal chop style stab
$vox: note("<c5 ~ ~ ~ eb5 ~ ~ ~ ~ ~ ~ ~ c5 ~ ~ ~>")
    .s("triangle")
    .lpf(slider(5000, 2500, 9000))
    .attack(slider(0.01, 0, 0.04))
    .decay(slider(0.1, 0.03, 0.25))
    .gain(slider(0.42, 0, 1.8))
    .room(slider(0.2, 0, 0.6))
    .sometimes(x => x.note("<eb5 ~ g5 ~>"))  // Variation
    .color("purple")

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR808")
    .gain(0.5)
    .room(0.4)
    .slow(2)
