// @name Rock Beat
// @genre Classic
// @bpm 120
// @tags rock, drums, guitar, power

setcpm(120 / 4)

// ═══════════════════════════════════════════════════════════════
// ROCK BEAT - Classic rock rhythm with power chords
// ═══════════════════════════════════════════════════════════════

// Driving rock kick with dynamics
$kick: s("bd ~ bd ~").bank("RolandTR808")
    .gain("<1.0 0.95 0.98 0.92> <0.95 0.98 1.0 [1.05 0.95]>")  // Dynamics
    .shape(slider(0.32, 0, 0.7))
    .every(4, x => x.s("[bd ~] ~ bd [~ bd]"))  // Syncopation
    .every(8, x => x.s("bd ~ bd ~ bd ~ bd [bd bd]"))  // Fill
    .color("orange")
    ._punchcard()

// Backbeat snare with punch
$snare: stack(
    s("~ sd ~ sd").gain(slider(0.92, 0, 2)).room(0.25),
    s("~ ~ [sd:3 ~] ~").gain(0.22).lpf(4500)  // Ghost
).bank("RolandTR808")
    .every(4, x => x.s("~ sd ~ [sd sd]"))  // Roll
    .every(8, x => x.s("~ sd ~ [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Driving hats with accents
$hat: s("hh*8").bank("RolandTR808")
    .gain(perlin.range(0.35, 0.5))  // Velocity
    .pan(perlin.range(-0.1, 0.1).slow(0.5))
    .sometimes(x => x.s("[hh hh oh hh] [hh hh hh hh] [hh hh oh hh] [hh hh hh oh]"))  // Accents
    .every(8, x => x.fast(2).gain(0.45))  // Build intensity
    .color("white")
    ._punchcard()

// Crash on downbeats for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ crash")
    .gain(slider(0.72, 0, 2))
    .room(0.4)
    .slow(2)
    ._punchcard()

// Power chords with distortion character
$guitar: note("<[c4,g4,c5] [c4,g4,c5] [f4,c5,f5] [g4,d5,g5]>")
    .s("sawtooth")
    .lpf(slider(3500, 1500, 6000))
    .lpq(3)  // Edge
    .decay(slider(0.18, 0.08, 0.35))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.62, 0, 2))
    .sometimes(x => x.note("<[d4,a4,d5] [c4,g4,c5] [f4,c5,f5] [g4,d5,g5]>"))  // ii-I-IV-V
    .rarely(x => x.fast(2).gain(0.5))  // Chugging
    .color("cyan")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Rhythm guitar accent
$rhythm: note("[c4,g4,c5]")
    .s("square")
    .lpf(2500)
    .struct("x ~ x ~ x ~ x [x x]")
    .decay(0.08)
    .gain(slider(0.35, 0, 1.3))
    .sometimes(x => x.struct("[x x] ~ x ~ x ~ [x x] ~"))
    .color("lime")
    ._punchcard()

// Rock bass - root notes with movement
$bass: note("<c2 c2 f2 g2>")
    .s("sawtooth")
    .lpf(sine.range(350, 800).slow(slider(8, 4, 16)))
    .decay(slider(0.15, 0.06, 0.3))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.78, 0, 2))
    .rarely(x => x.note("<c2 [c2 d2] f2 [g2 f2]>"))  // Walking
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ f1 g1>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.45, 0, 1.2))
    .slow(slider(4.0, 1, 16))
    .color("darkred")
