// @name Bass Cannon
// @genre Dubstep
// @bpm 140
// @tags wobble, massive, ducking, advanced, e minor

setcpm(140 / 4)

// ═══════════════════════════════════════════════════════════════
// BASS CANNON - Massive dubstep with E minor scale
// ═══════════════════════════════════════════════════════════════

// Heavy half-time kick
$kick: s("bd ~ ~ ~ ~ ~ ~ ~ bd ~ ~ ~ ~ ~ ~ ~").bank("RolandTR808")
    .gain("<1.25 1.2 1.22 1.15> <1.2 1.15 1.25 [1.3 1.2]>")  // Dynamics
    .shape(slider(0.38, 0, 0.75))
    .every(8, x => x.s("bd ~ ~ bd ~ ~ ~ ~ bd ~ ~ ~ ~ ~ bd ~"))  // Variation
    .every(16, x => x.s("bd ~ bd ~ ~ ~ ~ ~ bd ~ bd ~ ~ ~ [bd bd bd bd] bd"))  // Build
    .color("orange")
    ._punchcard()

// Snare on 3 with layers
$snare: stack(
    s("~ ~ ~ ~ sd ~ ~ ~").gain(slider(1.0, 0, 2)).room(slider(0.2, 0, 0.5)),
    s("~ ~ ~ ~ ~ [sd:3 ~] ~ ~").gain(0.3).lpf(5500)  // Ghost
).bank("RolandTR808")
    .every(4, x => x.s("~ ~ ~ ~ sd ~ [sd sd] ~"))  // Roll
    .every(8, x => x.s("~ ~ ~ ~ sd ~ ~ [sd sd sd sd]"))  // Fill
    ._punchcard()

// Rolling hats
$hat: s("hh*16").bank("RolandTR808")
    .gain(perlin.range(0.35, 0.52))
    .pan(perlin.range(-0.12, 0.12).slow(0.25))
    .lpf(perlin.range(5000, 10000))
    .sometimes(x => x.s("[hh*4] [hh hh oh hh] [hh*4] [hh hh hh oh]"))
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh*16]"))
    ._punchcard()

// MAIN WOBBLE BASS - E minor scale
$wobble: n("<0 ~ ~ 0> <~ 0 ~ ~>")
    .scale("e:minor")
    .s("square")
    .lpf(sine.range(200, 3000).fast(slider(8.0, 1, 16)))
    .lpq(sine.range(5, 14).slow(2))  // Heavy resonance
    .trans(-12)  // Down octave
    .decay(slider(0.12, 0.04, 0.25))
    .gain(slider(0.85, 0, 2))
    .chop(sine.range(4, 16).slow(4))  // Wobble modulation
    .sometimes(x => x.n("<0 3 ~ 0> <~ 5 ~ 3>"))  // Variation
    .every(8, x => x.lpf(sine.range(400, 4500).fast(16)))  // Faster wobble
    .color("orange")
    ._punchcard()

// Growl layer
$growl: n("<0 0 [0 3] 0> <0 [0 5] 5 0>")
    .scale("e:minor")
    .s("sawtooth")
    .lpf(sine.range(300, 2000).fast(8))
    .lpq(10)
    .trans(-12)
    .decay(0.1)
    .gain(slider(0.45, 0, 1.5))
    .chop(sine.range(4, 8).slow(2))
    .color("red")

// Sub layer
$sub: n("<0 ~ 0 ~ 0 ~ 0 ~>")
    .scale("e:minor")
    .s("sine")
    .lpf(80)
    .trans(-24)
    .gain(slider(0.55, 0, 1.5))
    .color("darkred")
    .scope({ size: 256 })

// Lead melody - E minor
$lead: n("<0 2 3 5 7 5 3 2>")
    .scale("e:minor")
    .s("triangle")
    .lpf(sine.range(2500, 6000).slow(8))
    .decay(0.15)
    .delay(0.2)
    .room(0.35)
    .trans(12)
    .gain(slider(0.45, 0, 1.8))
    .sometimes(x => x.rev())
    .color("cyan")
    .pianoroll({ fold: 1 })

// Dark pad
$pad: n("<[0,3,7] [0,3,7] [-2,2,5] [-5,0,3]>")
    .scale("e:minor")
    .s("sawtooth")
    .lpf(sine.range(500, 1500).slow(16))
    .attack(slider(0.5, 0.2, 1.1))
    .release(slider(0.6, 0.25, 1.2))
    .room(slider(0.45, 0, 1))
    .trans(-12)
    .gain(slider(0.38, 0, 1.3))
    .slow(4)
    .color("purple")
    .scope({ size: 256 })

// Riser FX
$riser: n("<0 1 2 3 4 5 6 7>")
    .scale("e:minor")
    .s("sawtooth")
    .lpf(sine.range(1000, 5000).slow(8))
    .decay(0.18)
    .gain(slider(0.35, 0, 1.2))
    .room(0.4)
    .slow(16)
    .color("magenta")

// Crash for drops
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR808")
    .gain(0.55)
    .room(0.45)
    .slow(2)
