// @name Old School
// @genre Hip Hop
// @bpm 95
// @tags oldschool, 90s, golden, classic

setcpm(95 / 4)

// ═══════════════════════════════════════════════════════════════
// OLD SCHOOL - 90s Golden Era with scratches and horn stabs
// ═══════════════════════════════════════════════════════════════

// Classic SP1200 kick with swing
$kick: s("bd ~ bd [~ bd]").bank("SP1200")
    .gain("<1.0 0.95 0.98 1.02> <0.98 1.0 1.02 0.98>")  // Dynamics
    .nudge("<0 0 0.02 0.03>")  // MPC swing
    .shape(slider(0.8, 0, 1))
    .every(4, x => x.s("[bd bd] ~ bd [~ bd]"))  // Variation
    .every(8, x => x.s("bd ~ bd [bd bd] [~ bd] ~ bd [bd bd]"))  // Fill
    .color("orange")
    ._punchcard()

// Swung hats with classic feel
$hat: s("[hh ~] [~ hh] [hh ~] [hh hh]").bank("SP1200")
    .gain(perlin.range(0.35, 0.5))  // Humanized
    .nudge(perlin.range(-0.02, 0.04))  // Swing
    .pan(perlin.range(-0.12, 0.12).slow(0.5))
    .lpf(perlin.range(5000, 10000))
    .sometimes(x => x.s("[hh hh] [~ hh] [hh ~] [~ hh]"))  // Variation
    .every(8, x => x.s("[hh hh hh hh] [hh hh oh hh]"))  // Fill
    ._punchcard()

// Classic snare with ghost layers
$snare: stack(
    s("~ sd ~ sd").gain(slider(0.88, 0, 2)).room(0.35),
    s("~ ~ [sd:3 ~] [~ sd:3]").gain(0.25).lpf(4000)  // Ghosts
).bank("SP1200")
    .nudge("0 0.015 0 0.02")  // Swing
    .every(8, x => x.s("~ sd ~ [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Scratch turntable - classic hip hop element
$scratch: s("scratch:0")
    .struct("~ ~ ~ ~ ~ ~ x ~")
    .chop(4)
    .slice(4, "<0 1 2 3>")
    .speed(choose(1, 1.5, -1, 0.75))
    .gain(slider(0.48, 0, 2))
    .room(0.15)
    .sometimes(x => x.struct("~ ~ ~ x ~ ~ x ~"))  // Double scratch
    .rarely(x => x.fast(2))  // Rapid scratches
    .color("orange")

// Old school bass with movement
$bass: note("<c2 ~ [c2 e2] ~ g2 ~ [f2 e2] ~>")
    .s("sawtooth")
    .lpf(sine.range(280, 550).slow(slider(4.0, 1, 16)))
    .decay(slider(0.18, 0.08, 0.35))
    .gain(slider(0.78, 0, 2))
    .rarely(x => x.note("<c2 d2 [e2 d2] c2 g2 f2 [e2 d2] c2>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ c1 ~ g1 ~ f1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.42, 0, 1.2))
    .color("darkred")

// Horn stab - old school signature
$horns: note("[c4,e4,g4,c5]")
    .s("sawtooth")
    .lpf(sine.range(1500, 4000).slow(slider(4.0, 1, 16)))
    .struct("~ ~ ~ ~ x ~ ~ ~")
    .decay(slider(0.15, 0.05, 0.3))
    .room(slider(0.3, 0, 1))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.struct("~ ~ x ~ x ~ ~ ~"))  // Double stab
    .rarely(x => x.note("[d4,f4,a4,d5]"))  // Chord variation
    .color("cyan")
    ._punchcard()

// Vinyl texture
$vinyl: s("[rim:5 rim:5 rim:5 rim:5]*4")
    .gain(slider(0.1, 0, 0.4))
    .lpf(3000)
    .hpf(500)
    .color("brown")

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("SP1200")
    .gain(0.4)
    .room(0.35)
    .slow(2)
