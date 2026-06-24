// @name Disco Groove
// @genre Classic
// @bpm 115
// @tags disco, strings, bassline, 70s

setcpm(115 / 4)

// ═══════════════════════════════════════════════════════════════
// DISCO GROOVE - Four on the floor with strings and octave bass
// ═══════════════════════════════════════════════════════════════

// Four on the floor kick - disco essential
$kick: s("bd*4").bank("RolandTR909")
    .gain("<0.98 1.02 0.95 1.05>")  // Pump dynamics
    .shape(slider(0.28, 0, 0.6))
    .every(8, x => x.s("bd bd bd [bd bd bd bd]"))  // Fill
    .color("orange")
    ._punchcard()

// Offbeat hats with open accents
$hat: s("[~ hh] [hh hh] [~ hh] [hh hh]").bank("RolandTR909")
    .gain(perlin.range(0.38, 0.52))  // Velocity
    .sometimes(x => x.s("[~ hh] [hh oh] [~ hh] [oh hh]"))  // More opens
    .every(8, x => x.s("[hh hh] [oh hh] [hh hh hh hh] [oh oh]"))  // Fill
    .color("white")
    ._punchcard()

// Clap on 2 and 4 with delay
$clap: s("~ cp ~ cp").bank("RolandTR909")
    .gain(slider(0.78, 0, 2))
    .room(slider(0.35, 0, 0.8))
    .delay(slider(0.18, 0, 0.5))
    .delaytime(0.25)
    .every(4, x => x.s("~ cp ~ [cp cp]"))  // Roll
    .every(8, x => x.s("~ cp ~ [cp cp cp cp]"))  // Fill
    .color("yellow")
    ._punchcard()

// Octave disco bass - the signature sound
$bass: note("<c2 c3 c2 c3 f2 f3 f2 f3 g2 g3 g2 g3 f2 f3 f2 f3>")
    .s("sawtooth")
    .lpf(sine.range(400, 1000).slow(slider(8, 4, 16)))
    .decay(slider(0.12, 0.05, 0.25))
    .gain(slider(0.8, 0, 2))
    .rarely(x => x.note("<c2 c3 [c2 d2] c3 f2 f3 [e2 f2] f3 g2 g3 [g2 a2] g3>"))  // Walking octaves
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ c1 ~ f1 ~ f1 ~ g1 ~ g1 ~ f1 ~ f1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.42, 0, 1.2))
    .color("darkred")

// Disco strings - lush pad chords
$strings: note("<[c4,e4,g4,c5] [c4,e4,g4,c5] [f4,a4,c5,f5] [g4,b4,d5,g5]>")
    .s("sawtooth")
    .lpf(sine.range(1500, 4500).slow(slider(8, 4, 16)))
    .attack(slider(0.12, 0.04, 0.28))
    .release(slider(0.38, 0.15, 0.7))
    .room(slider(0.42, 0, 1))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.note("<[d4,f4,a4,d5] [e4,g4,b4,e5]>"))  // Chord variation
    .color("cyan")
    ._punchcard()
    .scope({ size: 256 })

// String countermelody
$strings2: note("<~ ~ [e5,g5] ~ ~ ~ [f5,a5] ~>")
    .s("triangle")
    .lpf(3500)
    .attack(0.08)
    .release(0.3)
    .room(0.4)
    .gain(slider(0.28, 0, 1))
    .slow(slider(4.0, 1, 16))
    .color("purple")

// Wah rhythm guitar with filter sweep
$wah: note("<c4 ~ e4 ~ g4 ~ e4 ~>")
    .s("square")
    .lpf(sine.range(500, 3500).fast(slider(2, 1, 8)))  // Wah effect
    .lpq(6)  // Resonance for wah character
    .decay(slider(0.1, 0.04, 0.22))
    .gain(slider(0.42, 0, 1.5))
    .sometimes(x => x.note("<c4 e4 g4 c5 g4 e4 c4 ~>"))  // Arp
    .color("lime")
    ._punchcard()

// Horn stabs
$horns: note("<[c5,e5,g5] ~ ~ ~ ~ ~ ~ ~>")
    .s("sawtooth")
    .lpf(slider(4000, 2000, 6500))
    .attack(0.02)
    .decay(0.2)
    .gain(slider(0.42, 0, 1.5))
    .slow(4)
    .sometimes(x => x.note("<~ ~ ~ ~ [d5,f5,a5] ~ ~ ~>"))  // Answer
    .color("orange")
