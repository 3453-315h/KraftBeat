// @name Boom Bap
// @genre Hip Hop
// @bpm 92
// @tags classic, vinyl, drums, mpc

setcpm(92 / 4)

// ═══════════════════════════════════════════════════════════════
// BOOM BAP - Classic MPC swing with dusty samples
// ═══════════════════════════════════════════════════════════════

// Classic boom bap kick with MPC swing and off-grid feel
$kick: s("bd ~ [~ bd] ~  bd [~ bd] ~ bd").bank("SP1200")
    .gain("<1.1 1 0.95 1.05> <1.05 1 1.1 1>")  // Dynamics
    .nudge("<0 0 0.04 0  0 0.02 0 0.06>")  // Off-grid MPC feel
    .shape(slider(0.8, 0, 1))
    .every(4, x => x.s("[bd ~] ~ [~ bd] bd"))  // 4-bar variation
    .every(8, x => x.s("bd ~ [bd bd] ~ bd [~ bd] ~ [bd bd]"))  // 8-bar fill
    .color("orange")
    ._punchcard()

// Layered snare with ghost notes - essential boom bap
$snare: stack(
    s("~ sd ~ sd").gain(slider(0.9, 0, 2)).room(0.35),  // Main snare
    s("~ ~ [sd:3 ~] [~ sd:3]").gain(slider(0.3, 0, 1)).lpf(4000)  // Ghosts
).bank("SP1200")
    .nudge("0 0.015 0 0.02")  // Slight swing
    .every(8, x => x.s("~ sd ~ [sd sd sd sd]"))  // 8-bar fill
    .color("white")
    ._punchcard()

// Swung hi-hats with MPC groove
$hat: s("[hh ~] [~ hh] [hh ~] [hh hh]").bank("SP1200")
    .gain(perlin.range(0.35, 0.52))  // Humanized velocity
    .nudge(perlin.range(-0.02, 0.04))  // MPC swing timing
    .pan(perlin.range(-0.15, 0.15).slow(0.5))
    .lpf(perlin.range(5000, 10000))  // Tonal variation
    .sometimes(x => x.s("[hh hh] [~ hh] [hh ~] [~ hh]"))  // Variation
    .every(8, x => x.s("[hh hh hh hh] [hh hh oh hh]"))  // Fill
    ._punchcard()

// Open hat accent
$oh: s("~ ~ ~ ~ ~ ~ [oh ~] ~").bank("SP1200")
    .gain(slider(0.45, 0, 1.5))
    .room(0.2)
    .sometimes(x => x.s("~ ~ ~ oh ~ ~ [oh ~] ~"))  // Extra open hat
    .color("lime")
    ._punchcard()

// Vinyl crackle simulation (rim for texture)
$crackle: s("[rim:5 rim:5 rim:5 rim:5]*4")
    .gain(slider(0.12, 0, 0.5))
    .lpf(3000)
    .hpf(500)
    .color("brown")

// Deep boom bap bass with walking notes
$bass: note("<c2 ~ [c2 e2] f2>")
    .s("sawtooth")
    .lpf(sine.range(250, 550).slow(slider(4.0, 1, 16)))
    .decay(slider(0.18, 0.08, 0.35))
    .gain(slider(0.78, 0, 2))
    .rarely(x => x.note("<c2 d2 [e2 d2] c2>"))  // Walking bass variation
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ c1 f1>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.45, 0, 1.2))
    .color("darkred")

// Jazz piano sample feel
$piano: note("<[c4,e4,g4] ~ ~ ~ [a3,c4,e4] ~ ~ ~>")
    .s("triangle")  // Piano-like
    .lpf(sine.range(2000, 4500).slow(8))
    .decay(0.25)
    .room(slider(0.3, 0, 1))
    .gain(slider(0.45, 0, 1.8))
    .slow(2)
    .sometimes(x => x.note("<[f3,a3,c4]>"))  // Chord variation
    .color("cyan")
    ._punchcard()
