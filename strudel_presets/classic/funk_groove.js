// @name Funk Groove
// @genre Classic
// @bpm 105
// @tags funky, groovy, bass, slap

setcpm(105 / 4)

// ═══════════════════════════════════════════════════════════════
// FUNK GROOVE - Tight pocket with slap bass and wah guitar
// ═══════════════════════════════════════════════════════════════

// Funky kick with syncopated pattern and dynamics
$kick: s("bd ~ bd [~ bd]").bank("RolandTR808")
    .gain("<0.9 0.85 0.88 0.92>")  // Pocket dynamics
    .shape(slider(0.28, 0, 0.6))
    .nudge("<0 0 0.015 0>")  // Tight swing
    .every(4, x => x.s("[bd ~] ~ bd [bd bd]"))  // Variation
    .every(8, x => x.s("bd ~ bd [~ bd] [bd bd] ~ bd [bd bd]"))  // Fill
    .color("orange")
    ._punchcard()

// Snare with ghost layers - the pocket
$snare: stack(
    s("~ sd ~ sd").gain(slider(0.82, 0, 2)).room(0.2),
    s("~ ~ [sd:3 ~] [~ sd:3]").gain(0.28).lpf(5000)  // Ghosts
).bank("RolandTR808")
    .nudge("0 0.012 0 0.015")  // Tight swing
    .every(4, x => x.s("~ sd ~ [sd sd]"))  // Roll
    .every(8, x => x.s("~ sd ~ [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Hats with open hat accents
$hat: s("hh [hh oh] hh [hh oh]").bank("RolandTR808")
    .gain(perlin.range(0.38, 0.55))  // Velocity
    .pan(perlin.range(-0.12, 0.12).slow(0.5))
    .sometimes(x => x.s("[hh hh] [oh hh] [hh hh] [hh oh]"))  // Variation
    .every(8, x => x.s("[hh hh hh hh] [hh oh] [hh hh] [oh oh]"))  // Fill
    .color("white")
    ._punchcard()

// Clav - funk essential
$clav: s("~ clav:0 ~ [~ clav:1]")
    .gain(perlin.range(0.52, 0.68))  // Velocity
    .pan(slider(-0.3, -0.5, -0.1))
    .sometimes(x => x.s("[~ clav:0] clav:1 [~ clav:0] ~"))  // Syncopation
    .every(8, x => x.s("[clav:0 clav:1] clav:0 ~ [clav:1 clav:0]"))  // Fill
    .color("yellow")

// Funky slap bass with octave pops
$bass: note("<c2 ~ [c2 c3] ~ g2 ~ [f2 g2] ~>")
    .s("sawtooth")
    .lpf(sine.range(350, 900).slow(slider(4.0, 1, 16)))
    .decay(slider(0.12, 0.05, 0.25))
    .gain(slider(0.82, 0, 2))
    .rarely(x => x.note("<c2 [c2 c3] [g2 c3] ~ [g2 a2] ~ [f2 g2] c3>"))  // Slap variation
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ ~ ~ g1 ~ f1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.45, 0, 1.2))
    .color("darkred")

// Wah guitar - auto-wah effect with chords
$wah: note("<[c4,e4,g4] ~ ~ ~ [g4,b4,d5] ~ [f4,a4,c5] ~>")
    .s("square")
    .lpf(sine.range(400, 3000).fast(slider(2, 1, 8)))  // Wah sweep
    .lpq(6)  // Resonance
    .decay(slider(0.15, 0.06, 0.3))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.note("<[d4,f4,a4] ~ [e4,g4,b4] ~>"))  // Chord variation
    .rarely(x => x.fast(2).gain(0.45))  // Choppy rhythm
    .color("cyan")
    ._punchcard()

// Rhythm guitar skank
$skank: note("[c4,e4,g4]")
    .s("sawtooth")
    .lpf(2500)
    .struct("~ x ~ x ~ x ~ x")
    .decay(0.06)
    .gain(slider(0.38, 0, 1.5))
    .sometimes(x => x.struct("[~ x] x [~ x] x"))  // Syncopation
    .color("lime")
    ._punchcard()

// Horn stab
$horns: note("<[c5,e5,g5] ~ ~ ~ ~ ~ ~ ~>")
    .s("sawtooth")
    .lpf(slider(3500, 1800, 5500))
    .attack(0.02)
    .decay(0.18)
    .gain(slider(0.42, 0, 1.5))
    .sometimes(x => x.note("<[d5,f5,a5] ~ ~ ~ ~ ~ [c5,e5,g5] ~>"))  // Stab variation
    .color("orange")
