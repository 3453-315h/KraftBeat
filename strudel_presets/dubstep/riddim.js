// @name Riddim
// @genre Dubstep
// @bpm 150
// @tags heavy, riddim, aggressive, rhythmic

setcpm(150 / 4)

// ═══════════════════════════════════════════════════════════════
// RIDDIM - Aggressive rhythmic bass with half-time punch
// ═══════════════════════════════════════════════════════════════

// Heavy half-time kick
$kick: s("bd ~ ~ ~ ~ ~ ~ ~").bank("RolandTR808")
    .gain("<1.3 1.25 1.28 1.2> <1.25 1.2 1.3 [1.35 1.25]>")  // Power dynamics
    .shape(slider(0.4, 0, 0.8))
    .every(4, x => x.s("[bd ~] ~ ~ ~ ~ ~ bd ~"))  // Variation
    .every(8, x => x.s("bd ~ ~ bd ~ ~ ~ ~ bd ~ bd ~ ~ ~ [bd bd] bd"))  // Build
    .color("orange")
    ._punchcard()

// Snappy snare on 3
$snare: stack(
    s("~ ~ ~ ~ sd ~ ~ ~").gain(slider(1.15, 0, 2)).room(slider(0.15, 0, 0.4)),
    s("~ ~ ~ ~ ~ [sd:3 ~] ~ ~").gain(0.32).lpf(5500)  // Ghost
).bank("RolandTR808")
    .every(4, x => x.s("~ ~ ~ ~ sd ~ [sd sd] ~"))  // Roll
    .every(8, x => x.s("~ ~ ~ ~ sd ~ ~ [sd sd sd sd]"))  // Fill
    ._punchcard()

// Riddim hats with triplet feel
$hat: s("[hh hh] [hh hh] [hh hh] [hh [hh hh]]").bank("RolandTR808")
    .gain(perlin.range(0.38, 0.55))  // Velocity variation
    .pan(perlin.range(-0.15, 0.15).slow(0.25))
    .sometimes(x => x.fast(1.5))  // Triplets
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh hh*8]"))  // Build
    ._punchcard()

// RIDDIM BASS - aggressive rhythmic pattern
$bass: note("<c1 ~ c1 ~ c1 [c1 c1] c1 [c1 ~]>")
    .s("square")
    .lpf(sine.range(200, 2000).fast(slider(4.0, 1, 16)))
    .lpq(sine.range(5, 14).slow(2))  // Heavy resonance
    .decay(slider(0.1, 0.03, 0.22))
    .gain(slider(0.88, 0, 2))
    .chop(sine.range(4, 16).slow(4))  // Modulation
    .rarely(x => x.note("<c1 c1 [c1 d#1] c1 c1 [c1 f1] [d#1 c1] c1>"))  // Variation
    .every(8, x => x.lpf(sine.range(300, 3500).fast(8)))  // Faster modulation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Mid layer for thickness
$midbass: note("<c2 ~ c2 ~ c2 [c2 c2] c2 [c2 ~]>")
    .s("sawtooth")
    .lpf(sine.range(600, 1800).fast(4))
    .lpq(8)
    .decay(0.08)
    .gain(slider(0.42, 0, 1.4))
    .color("orange")

// Sub layer
$sub: note("<c1 ~ ~ ~ ~ ~ ~ ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.55, 0, 1.5))
    .color("darkred")

// Riddim stab with variations
$stab: note("<[c3,d#3,g3] ~ ~ ~ ~ ~ [c3,d#3,g3] ~>")
    .s("sawtooth")
    .lpf(sine.range(1500, 4000).slow(slider(4.0, 1, 16)))
    .decay(slider(0.12, 0.04, 0.25))
    .room(slider(0.25, 0, 0.6))
    .gain(slider(0.52, 0, 2))
    .sometimes(x => x.note("<[d3,f3,a3] ~ ~ ~>"))  // Variation
    .rarely(x => x.fast(2))  // Double stab
    .color("cyan")

// Crash for drops
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR808")
    .gain(0.55)
    .room(0.35)
    .slow(2)
