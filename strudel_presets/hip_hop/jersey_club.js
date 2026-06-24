// @name Jersey Club
// @genre Hip Hop
// @bpm 140
// @tags jersey, club, bounce, baltimore

setcpm(140 / 4)

// ═══════════════════════════════════════════════════════════════
// JERSEY CLUB - Bed squeak synths and bouncy kicks
// ═══════════════════════════════════════════════════════════════

// Jersey club kick - the iconic bounce pattern
$kick: s("bd ~ bd [~ bd] bd ~ bd [bd bd]").bank("RolandTR808")
    .gain("<1.12 1.08 1.1 1.05> <1.08 1.05 1.12 [1.15 1.08]>")  // Dynamics
    .shape(slider(0.8, 0, 1))
    .every(4, x => x.s("bd bd bd [~ bd] bd ~ bd [bd bd]"))  // Variation
    .every(8, x => x.s("bd ~ bd [bd bd] bd ~ [bd bd bd] [bd bd]"))  // Fill
    .color("orange")
    ._punchcard()

// Fast rolling hats
$hat: s("hh*16").bank("RolandTR808")
    .gain(perlin.range(0.35, 0.5))  // Humanized
    .pan(perlin.range(-0.15, 0.15).slow(0.25))
    .sometimes(x => x.s("[hh*4] [hh hh oh hh] [hh*4] [hh hh hh oh]"))  // Accents
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh*16]"))  // Build
    ._punchcard()

// Jersey clap - rapid pattern
$clap: s("~ cp ~ cp ~ cp ~ cp").bank("RolandTR808")
    .gain(perlin.range(0.42, 0.58))  // Velocity variation
    .room(slider(0.25, 0, 0.6))
    .delay(slider(0.1, 0, 0.3))
    .sometimes(x => x.s("~ cp cp ~ ~ cp ~ cp"))  // Syncopation
    .every(8, x => x.s("[cp cp] cp ~ cp ~ cp [cp cp] [cp cp cp cp]"))  // Fill
    .color("yellow")
    ._punchcard()

// BED SQUEAK synth - THE jersey club signature
$squeak: note("<c6 c6 [c6 ~] c6 c6 c6 [c6 c6] c6>")
    .s("sine")
    .lpf(sine.range(6000, 12000).slow(slider(4.0, 1, 16)))
    .decay(slider(0.08, 0.03, 0.2))
    .gain(slider(0.55, 0, 2))
    .pan(perlin.range(-0.2, 0.2).slow(0.25))
    .sometimes(x => x.note("<c6 [c6 d6] c6 c6 [c6 c6 c6] c6 c6 [c6 c6]>"))  // Variation
    .rarely(x => x.note("<d6 d6 [d6 ~] d6>"))  // Pitch variation
    .color("cyan")
    .pianoroll({ fold: 1 })

// Secondary squeak - call and response
$squeak2: note("<~ ~ ~ ~ [c6 ~] ~ ~ ~>")
    .s("sine")
    .lpf(8000)
    .decay(0.06)
    .gain(slider(0.3, 0, 1.2))
    .color("yellow")

// Jersey bass
$bass: note("<c2 ~ c2 ~ c2 ~ [c2 d#2] ~>")
    .s("sine")
    .lpf(slider(150, 60, 250))
    .decay(slider(0.25, 0.1, 0.45))
    .gain(slider(0.78, 0, 2))
    .rarely(x => x.note("<c2 c2 [c2 d2] d#2>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ c1 ~ c1 ~ c1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.4, 0, 1.2))
    .color("darkred")

// Vocal chop simulation
$vox: s("vocal:0")
    .struct("~ ~ x ~ ~ ~ x x")
    .chop(8)
    .slice(4, "<0 1 2 3>")
    .speed(slider(0.75, 0.5, 1.5))
    .lpf(4000)
    .room(0.2)
    .gain(slider(0.45, 0, 2))
    .sometimes(x => x.struct("x ~ x ~ ~ x x x"))  // More chops
    .rarely(x => x.fast(2))  // Rapid chops
    .color("orange")

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR808")
    .gain(0.45)
    .room(0.35)
    .slow(2)
