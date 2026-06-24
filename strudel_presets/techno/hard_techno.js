// @name Hard Techno
// @genre Techno
// @bpm 145
// @tags hard, industrial, pounding, warehouse

setcpm(145 / 4)

// ═══════════════════════════════════════════════════════════════
// HARD TECHNO - Warehouse pounding with relentless energy
// ═══════════════════════════════════════════════════════════════

// Distorted kick with dynamics and fills
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.35 1.28 1.32 1.25> <1.3 1.25 1.35 [1.4 1.3]>")  // Power dynamics
    .shape(slider(0.38, 0, 0.8))
    .every(4, x => x.s("[bd bd] bd bd bd"))  // 4-bar punch
    .every(8, x => x.s("bd bd bd bd [bd bd bd bd]"))  // 8-bar fill
    .every(16, x => x.s("bd bd bd [bd bd] bd bd [bd*4] [bd*8]"))  // Build
    .color("orange")
    ._punchcard()

// Aggressive 16th hats with dynamics and open hat accents
$hat: s("[hh hh hh hh] [hh hh hh oh] [hh hh hh hh] [hh oh hh hh]").bank("RolandTR909")
    .gain(perlin.range(0.38, 0.55))  // Velocity variation
    .sometimes(x => x.fast(1.5))  // Triplet feel occasionally
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh*16]"))  // Hat roll build
    ._punchcard()

// Hard clap with ghost accents
$clap: stack(
    s("~ cp ~ cp").gain(slider(1.0, 0, 2)).room(0.15),  // Main clap
    s("~ [cp:3 ~] ~ [~ cp:3]").gain(0.3).lpf(6000)  // Ghost claps
).bank("RolandTR909")
    .every(4, x => x.s("~ cp ~ [cp cp]"))  // 4-bar fill
    .every(8, x => x.s("~ cp ~ [cp cp cp cp]"))  // 8-bar fill
    .color("white")
    ._punchcard()

// Snare roll build-ups
$snareroll: s("~ ~ ~ ~ ~ ~ ~ ~")
    .bank("RolandTR909")
    .every(16, x => x.s("~ ~ ~ ~ ~ ~ sd [sd*4] ~ ~ ~ ~ ~ [sd*8] [sd*16] [sd*32]"))
    .gain(slider(0.7, 0, 2))
    .lpf(sine.range(3000, 8000).fast(8))
    .color("yellow")

// Crash accent every 8 bars
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh").bank("RolandTR909")
    .gain(slider(0.5, 0, 2))
    .room(0.3)
    .slow(2)
    ._punchcard()

// Ride for intensity layers
$ride: s("rd*8").bank("RolandTR909")
    .gain(perlin.range(0.2, 0.35))
    .sometimes(x => x.fast(2))  // Double-time ride
    .color("gray")
    ._punchcard()

// Driving acid bass with aggressive filter
$bass: note("<c1 c1 [c1 d#1] c1 g0 g0 [a#0 g0] c1>")
    .s("sawtooth")
    .lpf(sine.range(120, 1400).fast(2))
    .lpq(sine.range(3, 12).slow(2))  // Resonance movement
    .decay(slider(0.08, 0.02, 0.2))
    .gain(slider(0.95, 0, 2))
    .rarely(x => x.fast(2))  // Double-time bass
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })

// Dark stab - minor chord hits with filter
$stab: note("<[c4,d#4,g4] ~ ~ ~ ~ ~ ~ ~ [a#3,d4,f4] ~ ~ ~ ~ ~ ~ ~>")
    .s("sawtooth")
    .lpf(sine.range(2000, 5000).slow(4))
    .attack(slider(0.005, 0, 0.03))
    .decay(slider(0.1, 0.02, 0.25))
    .gain(slider(0.52, 0, 2))
    .sometimes(x => x.fast(2).lpf(8000))  // Hard stab hits
    .color("purple")
    ._punchcard()

// Industrial noise hit with variations
$noise: s("~ ~ ~ ~ ~ ~ noise ~")
    .lpf(sine.range(2000, 6000).fast(4))
    .decay(slider(0.08, 0.02, 0.2))
    .gain(slider(0.35, 0, 1.5))
    .sometimes(x => x.s("[noise noise] ~ ~ ~"))  // Double hits
    .rarely(x => x.fast(4))  // Noise roll
    .color("gray")
    ._punchcard()

// Reversed crash for tension
$revcr: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ cp:5")
    .gain(0.4)
    .speed(-1)
    .room(0.5)
    .slow(4)
    .color("magenta")
