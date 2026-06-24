// @name Electro
// @genre Techno
// @bpm 128
// @tags electro, 808, robotic, breakbeat

setcpm(128 / 4)

// ═══════════════════════════════════════════════════════════════
// ELECTRO - Classic 808 machine funk, Detroit/Egyptian Lover style
// ═══════════════════════════════════════════════════════════════

// 808 kick - syncopated electro pattern with dynamics
$kick: s("[bd ~ ~ ~] [bd ~ bd ~] [~ ~ bd ~] [bd ~ ~ bd]").bank("RolandTR808")
    .gain("<1.2 1.15 1.18 1.12> <1.15 1.18 1.2 [1.22 1.15]>")  // Dynamics
    .shape(slider(0.2, 0, 0.5))
    .every(8, x => x.s("[bd ~ ~ ~] [bd ~ bd ~] [bd ~ bd ~] [bd bd ~ bd]"))  // 8-bar variation
    .every(16, x => x.s("[bd ~ ~ bd] [bd ~ bd ~] [bd ~ bd bd] [bd bd bd bd]"))  // Build
    .color("orange")
    ._punchcard()

// Electro clap with ghost hits
$clap: stack(
    s("~ ~ ~ ~ cp ~ ~ ~ ~ ~ ~ ~ cp ~ ~ ~").gain(slider(0.95, 0, 2)).room(0.25),
    s("~ ~ ~ ~ ~ ~ [cp:3 ~] ~ ~ ~ ~ ~ ~ ~ [~ cp:3] ~").gain(0.25).lpf(5000)  // Ghost clap
).bank("RolandTR808")
    .every(8, x => x.s("~ ~ ~ ~ cp ~ ~ ~ ~ ~ ~ ~ cp ~ cp cp"))  // 8-bar fill
    .color("white")
    ._punchcard()

// Syncopated hats with humanized velocity
$hat: s("[hh ~ hh ~] [~ hh ~ hh] [hh ~ oh ~] [~ hh hh ~]").bank("RolandTR808")
    .gain(perlin.range(0.35, 0.52))  // Humanized
    .pan(perlin.range(-0.15, 0.15).slow(0.25))  // Stereo movement
    .sometimes(x => x.s("[hh hh ~ ~] [~ hh ~ hh] [hh ~ oh ~] [hh ~ hh hh]"))  // Variation
    .every(8, x => x.s("[hh hh hh hh] [hh hh oh hh] [hh hh hh hh] [oh hh hh hh]"))  // Fill
    ._punchcard()

// Cowbell - essential electro element with variations
$cowbell: s("~ ~ [ag ~] ~ ~ ~ ~ ~ ~ ~ [ag ~] ~ ~ ~ ~ ~")
    .gain(perlin.range(0.4, 0.58))  // Velocity variation
    .sometimes(x => x.s("~ ~ [ag ~] ~ ~ ~ [~ ag] ~ ~ ~ [ag ~] ~ ~ [ag ~] ~ ~"))  // Extended pattern
    .rarely(x => x.s("[ag ~] [~ ag] [ag ~] ~ ~ ~ ~ ~"))  // Fill
    .color("yellow")
    ._punchcard()

// 808 snare accent
$snare808: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ sd ~ ~ ~").bank("RolandTR808")
    .gain(0.5)
    .room(0.2)
    .every(4, x => x.s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ [sd sd] ~ ~ ~"))  // Double snare fill
    .color("gray")

// 808 bass with movement
$bass: note("<c1 ~ c1 [c1 d#1] g0 ~ [g0 c1] ~ c1 ~ c1 ~ g0 ~ c1 ~>")
    .s("sine")
    .lpf(sine.range(250, 450).slow(8))  // Subtle filter movement
    .decay(slider(0.18, 0.06, 0.4))
    .gain(slider(0.92, 0, 2))
    .rarely(x => x.note("<c1 c1 [c1 d#1] g1 c1 ~ g0 c1>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })

// Robotic lead with variations
$lead: note("<c4 d#4 g4 d#4 c4 ~ ~ ~ g3 a#3 c4 ~ ~ ~ ~ ~>")
    .s("square")
    .lpf(sine.range(3000, 5500).slow(4))
    .decay(slider(0.12, 0.03, 0.3))
    .gain(slider(0.48, 0, 2))
    .sometimes(x => x.rev())  // Reverse pattern
    .rarely(x => x.fast(2).gain(0.4))  // Double-time fill
    .color("cyan")
    ._punchcard()

// Synth stab with movement
$stab: note("<[c4,d#4,g4] ~ ~ ~ ~ ~ ~ ~ [g3,a#3,d4] ~ ~ ~ ~ ~ ~ ~>")
    .s("sawtooth")
    .lpf(sine.range(3500, 6500).slow(8))
    .attack(slider(0.005, 0, 0.03))
    .decay(slider(0.1, 0.02, 0.25))
    .gain(slider(0.45, 0, 2))
    .sometimes(x => x.note("<[d4,f4,a4]>"))  // Stab variation
    .color("magenta")
    ._punchcard()

// Tom accent for fills
$tom: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ tom tom").bank("RolandTR808")
    .gain(slider(0.45, 0, 1.5))
    .lpf(500)
    .room(0.2)
    .every(4, x => x.s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ tom ~ tom ~ tom tom"))  // Extended fill
    .color("brown")

// Crash accent
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR808")
    .gain(0.45)
    .room(0.35)
    .slow(2)
