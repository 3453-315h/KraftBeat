// @name Acid Bassline
// @genre Techno
// @bpm 135
// @tags acid, 303, squelch, chicago

setcpm(135 / 4)

// ═══════════════════════════════════════════════════════════════
// ACID TECHNO - Classic 303 squelch with production drums
// ═══════════════════════════════════════════════════════════════

// Production 909 kick with subtle dynamics and fills
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.15 1.1 1.12 1.1> <1.1 1.1 1.15 [1.18 1.1]>")  // Velocity variation
    .shape(slider(0.2, 0, 0.5))
    .every(8, x => x.s("bd*4 [bd bd bd bd]"))  // 8-bar fill
    .rarely(x => x.s("[bd bd] bd bd bd"))  // Occasional flam
    .color("orange")
    ._punchcard()

// Evolving offbeat hats with velocity and stereo movement
$hat: s("[~ hh] [~ <hh hh:1>] [~ hh] [~ oh:2]").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.52))  // Humanized velocity
    .pan(perlin.range(-0.15, 0.15).slow(0.5))  // Stereo movement
    .sometimes(x => x.fast(2))  // Double-time variations
    .every(16, x => x.s("[hh hh] [hh hh] [hh hh hh hh] [hh oh]"))  // Fill
    ._punchcard()

// Snappy clap with ghost hits for groove
$clap: stack(
    s("~ cp ~ cp").gain(slider(0.85, 0, 2)).room(0.18),  // Main clap
    s("~ [~ cp:3] ~ ~").gain(slider(0.25, 0, 1)).lpf(5000)  // Ghost clap
).bank("RolandTR909")
    .every(8, x => x.s("~ cp ~ [cp cp cp cp]"))  // 8-bar fill
    .color("white")
    ._punchcard()

// Ride for energy with evolving dynamics
$ride: s("~ ~ ~ ~ ~ ~ rd ~").bank("RolandTR909")
    .gain(slider(0.3, 0, 1.5))
    .sometimes(x => x.s("rd*8").gain(0.2))  // Ride layer on drops
    ._punchcard()

// TB-303 ACID LINE - Classic Chicago style with proper movement
$acid: note("<c2 [c2 c3] c2 [d#2 d2] c2 [c3 c2] [g1 a#1] c2>")
    .s("sawtooth")
    .lpf(sine.range(250, 4000).fast(slider(4, 1, 8)))
    .lpq(sine.range(5, 15).slow(4))  // Resonance sweep
    .decay(slider(0.08, 0.02, 0.2))
    .gain(slider(0.82, 0, 2))
    .rarely(x => x.note("<c2 c3 c2 c3>").fast(2))  // Octave jumps
    .scope({ size: 256 })
    .color("lime")
    .pianoroll({ fold: 1 })

// Counter acid - higher register with call-response
$acid2: note("<~ [g3 a#3] ~ [c4 d#4] ~ [a#3 g3] ~ c4>")
    .s("square")
    .lpf(sine.range(600, 5000).fast(slider(2, 0.5, 6)))
    .decay(slider(0.1, 0.03, 0.25))
    .gain(slider(0.4, 0, 2))
    .pan(sine.range(-0.25, 0.25).slow(2))  // Stereo movement
    .sometimes(x => x.fast(2).gain(0.3))  // Double-time fills
    .color("cyan")
    ._punchcard()

// Sub reinforcement with power on downbeats
$sub: note("<c1 c1 c1 c1 g0 g0 c1 c1>")
    .s("sine")
    .lpf(slider(120, 40, 200))
    .gain("<0.65 0.55 0.6 0.55>")  // Dynamic sub
    .color("red")

// Crash accent for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh:4")
    .bank("RolandTR909")
    .gain(slider(0.4, 0, 1.5))
    .room(0.4)
    .slow(2)
    .color("yellow")
