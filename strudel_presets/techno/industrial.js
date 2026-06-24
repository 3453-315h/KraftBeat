// @name Industrial Techno
// @genre Techno
// @bpm 142
// @tags industrial, dark, harsh, mechanical

setcpm(142 / 4)

// ═══════════════════════════════════════════════════════════════
// INDUSTRIAL TECHNO - Harsh, mechanical, relentless punishment
// ═══════════════════════════════════════════════════════════════

// Crushing kick with machine-like precision and fills
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.4 1.32 1.38 1.3> <1.35 1.3 1.4 [1.45 1.35]>")  // Power dynamics
    .shape(slider(0.45, 0, 0.9))
    .every(4, x => x.s("[bd bd] bd bd bd"))  // Machine stutter
    .every(8, x => x.s("bd bd bd bd [bd bd bd bd]"))  // 8-bar fill
    .every(16, x => x.s("bd bd [bd bd] bd bd bd [bd*8]"))  // Build pattern
    .color("orange")
    ._punchcard()

// Metallic 16th hats with aggressive dynamics
$hat: s("[hh hh hh hh] [hh hh [hh hh] oh] [hh hh hh hh] [oh hh hh hh]").bank("RolandTR909")
    .gain(perlin.range(0.4, 0.58))  // Mechanical velocity
    .sometimes(x => x.fast(1.5))  // Triplet hits
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh oh hh*8]"))  // Hat roll
    ._punchcard()

// Industrial clap layered with noise bursts
$clap: stack(
    s("~ [cp noise:2] ~ cp").gain(slider(0.9, 0, 2)).room(0.18),
    s("~ ~ [cp:3 ~] ~").gain(0.3).lpf(5000)  // Ghost clap
).bank("RolandTR909")
    .every(4, x => x.s("~ cp ~ [cp cp]"))  // Machine rhythm
    .every(8, x => x.s("~ cp ~ [cp cp cp cp]"))  // Build fill
    .color("white")
    ._punchcard()

// Snare roll builders for intensity
$snareroll: s("~ ~ ~ ~ ~ ~ ~ ~")
    .bank("RolandTR909")
    .every(8, x => x.s("~ ~ ~ ~ ~ ~ sd [sd sd sd sd]"))  // 8-bar fill
    .every(16, x => x.s("~ ~ ~ ~ ~ ~ [sd*4] [sd*8] ~ ~ ~ ~ [sd*8] [sd*16] [sd*32] [sd*64]"))  // Build
    .gain(slider(0.7, 0, 2))
    .lpf(sine.range(2000, 8000).fast(8))
    .color("yellow")

// Noise bursts - mechanical texture with variations
$noise: s("[~ ~ ~ noise] [~ ~ ~ ~] [~ ~ noise ~] [~ ~ ~ ~]")
    .lpf(sine.range(3000, 8000).fast(2))
    .decay(slider(0.06, 0.02, 0.15))
    .gain(slider(0.4, 0, 1.5))
    .sometimes(x => x.fast(2))  // Double burst
    .rarely(x => x.s("[noise*4] ~ ~ ~"))  // Noise roll
    .color("gray")
    ._punchcard()

// Additional noise layer - pitched for industrial character
$noisepitch: s("~ ~ ~ ~ ~ noise ~ ~")
    .lpf(1500)
    .hpf(800)
    .gain(0.25)
    .speed("<1 0.5 1.5 2>")  // Pitched variation
    .room(0.2)
    ._punchcard()

// Aggressive bass - detuned, distorted machine
$bass: note("<c1 c1 c1 [c1 d1] g0 g0 [a0 g0] c1>")
    .s("sawtooth")
    .lpf(sine.range(100, 1000).fast(slider(2, 0.5, 4)))
    .lpq(sine.range(2, 8).slow(2))  // Resonance movement
    .decay(slider(0.08, 0.02, 0.2))
    .gain(slider(0.95, 0, 2))
    .rarely(x => x.fast(2))  // Machine stutter
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })

// Industrial stab - dissonant cluster hits
$stab: note("<[c4,d4,g4] ~ ~ ~ ~ ~ ~ ~ [f3,g3,c4] ~ ~ ~ ~ ~ ~ ~>")
    .s("square")
    .lpf(sine.range(1500, 4000).slow(4))
    .attack(slider(0.002, 0, 0.02))
    .decay(slider(0.08, 0.02, 0.2))
    .gain(slider(0.5, 0, 2))
    .sometimes(x => x.fast(2).gain(0.7))  // Double stab
    .rarely(x => x.note("<[c4,d#4,f#4,a4]>"))  // Dissonant cluster
    .color("purple")
    ._punchcard()

// Metal texture - rim hits with variations
$metal: s("~ ~ ~ ~ [rim rim] ~ ~ ~").bank("RolandTR909")
    .gain(perlin.range(0.45, 0.62))
    .room(slider(0.3, 0, 0.7))
    .sometimes(x => x.s("~ ~ [rim ~] ~ [rim rim rim] ~ ~ ~"))  // Variation
    .every(8, x => x.s("[rim*4] ~ ~ ~ ~ [rim*8] ~ ~"))  // Metal roll
    ._punchcard()

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.5)
    .room(0.35)
    .slow(2)

// Reverse crash tension builder
$revcr: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ cp:5")
    .gain(0.4)
    .speed(-1)
    .room(0.6)
    .slow(4)
    .color("magenta")
