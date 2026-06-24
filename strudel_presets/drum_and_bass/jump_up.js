// @name Jump Up
// @genre Drum and Bass
// @bpm 175
// @tags jump, energy, dancefloor, rave

setcpm(175 / 4)

// ═══════════════════════════════════════════════════════════════
// JUMP UP - High energy dancefloor DnB
// ═══════════════════════════════════════════════════════════════

// Energetic kick pattern with punch
$kick: s("bd ~ ~ ~ bd ~ bd ~").bank("RolandTR909")
    .gain("<1.1 1.05 1.08 1.02> <1.05 1.08 1.1 [1.15 1.08]>")  // Energy dynamics
    .shape(slider(0.32, 0, 0.65))
    .every(4, x => x.s("[bd ~] ~ ~ ~ bd ~ bd ~"))  // Opening kick
    .every(8, x => x.s("bd ~ bd ~ bd ~ [bd bd] bd"))  // 8-bar fill
    .color("orange")
    ._punchcard()

// Snappy snare with ghost layers
$snare: stack(
    s("~ ~ sd ~ ~ ~ sd ~").gain(slider(1.0, 0, 2)).room(0.25),
    s("~ ~ ~ [sd:3 ~] ~ ~ ~ [sd:3 sd:3]").gain(0.3).lpf(5500)  // Ghost rush
).bank("RolandTR909")
    .every(4, x => x.s("~ ~ sd ~ ~ [sd sd] sd ~"))  // 4-bar roll
    .every(8, x => x.s("~ ~ sd ~ ~ ~ sd [sd sd sd sd]"))  // 8-bar fill
    .color("white")
    ._punchcard()

// Fast rolling hats with energy
$hat: s("hh*16").bank("RolandTR909")
    .gain(perlin.range(0.38, 0.55))  // Velocity variation
    .pan(perlin.range(-0.15, 0.15).slow(0.25))
    .sometimes(x => x.s("[hh*4] [hh hh oh hh] [hh*4] [hh hh hh oh]"))  // Accents
    .every(8, x => x.fast(1.5).gain(0.48))  // Triplet energy
    .color("white")
    ._punchcard()

// Ride for intensity
$ride: s("rd*8").bank("RolandTR909")
    .gain(perlin.range(0.28, 0.42))
    .pan(perlin.range(-0.2, 0.2).slow(0.5))
    .sometimes(x => x.fast(2).gain(0.35))  // Double-time intensity
    .color("gray")
    ._punchcard()

// FOGHORN BASS - jump up signature sound
$bass: note("<c1 ~ c1 ~ c1 [c1 d#1] c1 ~>")
    .s("sawtooth")
    .lpf(sine.range(200, 2000).fast(slider(2, 1, 8)))
    .lpq(sine.range(4, 12).slow(2))  // Resonance movement
    .decay(slider(0.12, 0.04, 0.25))
    .gain(slider(0.85, 0, 2))
    .chop(sine.range(4, 16).slow(4))  // Wobble
    .rarely(x => x.note("<c1 d#1 [c1 f1] c1>"))  // Variation
    .every(8, x => x.lpf(sine.range(300, 3000).fast(8)))  // Faster modulation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Mid layer for thickness
$midbass: note("<c2 ~ c2 ~ c2 [c2 d#2] c2 ~>")
    .s("square")
    .lpf(sine.range(500, 1500).fast(2))
    .lpq(6)
    .decay(0.1)
    .gain(slider(0.42, 0, 1.3))
    .color("orange")

// Sub layer
$sub: note("<c1 ~ c1 ~ c1 c1 c1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.55, 0, 1.5))
    .color("darkred")

// MC-style vocal stab with variations
$mc: s("vocal:0")
    .struct("~ ~ ~ ~ ~ ~ x ~")
    .chop(8)
    .slice(4, "<0 1 2 3>")
    .speed(slider(0.6, 0.4, 1.5))
    .room(0.2)
    .gain(slider(0.45, 0, 2))
    .sometimes(x => x.struct("~ ~ ~ x ~ ~ x ~"))  // Double vocal
    .rarely(x => x.fast(2))  // Rapid chops
    .color("orange")

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.55)
    .room(0.35)
    .slow(2)
