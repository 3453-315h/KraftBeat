// @name Trap Symphony
// @genre Hip Hop
// @bpm 140
// @tags trap, 808, orchestral, epic

setcpm(140 / 4)

// ═══════════════════════════════════════════════════════════════
// TRAP SYMPHONY - Orchestral trap with epic sounds
// ═══════════════════════════════════════════════════════════════

// Heavy trap kick with half-time feel
$kick: s("bd ~ ~ ~ bd ~ ~ ~").bank("RolandTR808")
    .gain("<1.25 1.2 1.22 1.18> <1.2 1.18 1.25 [1.28 1.2]>")  // Dynamics
    .shape(slider(0.75, 0, 1))
    .every(4, x => x.s("[bd ~] ~ ~ ~ bd ~ [~ bd] ~"))  // Variation
    .every(8, x => x.s("bd ~ ~ ~ bd ~ [bd bd] ~"))  // Fill
    .every(16, x => x.s("bd ~ bd ~ bd ~ [bd*4] [bd*8]"))  // Build
    .color("orange")
    ._punchcard()

// Snare on 3 with ghost accents
$snare: stack(
    s("~ ~ ~ ~ sd ~ ~ ~").gain(slider(0.9, 0, 2)).room(0.35),
    s("~ ~ ~ ~ ~ ~ [sd:3 ~] ~").gain(0.25).lpf(5000)  // Ghost
).bank("RolandTR808")
    .every(8, x => x.s("~ ~ ~ ~ sd ~ ~ [sd sd sd sd]"))  // Fill
    .every(16, x => x.s("~ ~ ~ ~ sd ~ [sd*4] [sd*8]"))  // Build
    .color("white")
    ._punchcard()

// Rolling hi-hats with builds
$hat: s("[hh hh hh hh] [hh hh hh [hh hh hh]] [hh hh [hh hh hh] hh] [hh [hh hh] hh hh]")
    .bank("RolandTR808")
    .gain(perlin.range(0.35, 0.52))  // Humanized
    .pan(perlin.range(-0.25, 0.25).slow(0.25))
    .sometimes(x => x.fast(1.5))  // Triplets
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh*16]"))  // Build
    ._punchcard()

// Snare roll for builds
$snareroll: s("~ ~ ~ ~ ~ ~ ~ ~")
    .bank("RolandTR808")
    .every(16, x => x.s("~ ~ ~ ~ ~ ~ sd [sd*4] ~ ~ ~ ~ [sd*4] [sd*8] [sd*16] [sd*32]"))
    .gain(slider(0.65, 0, 2))
    .lpf(sine.range(2500, 10000).fast(8))
    .color("yellow")

// 808 bass with long decay - orchestral weight
$bass: n("<0 ~ [-5 ~] ~> <~ 0 ~ [-7 0]>")
    .scale("g:minor")
    .s("sine")
    .lpf(slider(140, 60, 220))
    .decay(slider(0.45, 0.2, 0.8))  // Long 808 tail
    .trans(-24)
    .gain(slider(0.85, 0, 2))
    .sometimes(x => x.note("<g1 ~ [d1 ~] ~ ~ g1 ~ [f1 g1]>"))  // Variation
    .color("red")
    ._punchcard()
    .scope({ size: 256 })

// Orchestral melody - strings feel
$melody: n("<0 2 3 5 7 5 3 2>")
    .scale("g:minor")
    .s("sawtooth")
    .lpf(sine.range(2500, 5500).slow(8))
    .attack(0.05)
    .decay(0.2)
    .room(slider(0.4, 0, 1))
    .delay(0.15)
    .trans(12)
    .gain(slider(0.48, 0, 2))
    .sometimes(x => x.rev())  // Reverse phrase
    .rarely(x => x.fast(2))  // Double-time
    .color("magenta")
    .pianoroll({ fold: 1 })

// Epic pad layer - orchestra depth
$pad: n("<[0,3,7] [0,3,7] [-2,2,5] [-5,0,3]>")
    .scale("g:minor")
    .s("sawtooth")
    .lpf(sine.range(800, 2500).slow(16))
    .attack(slider(0.5, 0.2, 1.1))
    .release(slider(0.6, 0.25, 1.2))
    .room(slider(0.5, 0, 1))
    .trans(-12)
    .gain(slider(0.45, 0, 1.5))
    .slow(4)
    .color("purple")
    .scope({ size: 256 })

// Bell melody - trap bells
$bells: n(choose(60, 63, 67, 70, 72))
    .scale("g:minor")
    .s("triangle")
    .struct("x(5,16)")
    .lpf(5000)
    .decay(0.25)
    .delay(slider(0.25, 0, 0.6))
    .delaytime(0.25)
    .room(0.35)
    .gain(slider(0.38, 0, 1.5))
    .color("cyan")

// Crash for drops
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR808")
    .gain(0.55)
    .room(0.45)
    .slow(2)

// Reverse crash for builds
$revcr: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ cp:5")
    .gain(0.5)
    .speed(-1)
    .room(0.6)
    .slow(4)
