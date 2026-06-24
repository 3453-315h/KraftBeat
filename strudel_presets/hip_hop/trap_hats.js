// @name Trap Hats
// @genre Hip Hop
// @bpm 140
// @tags 808, rolling, hard, trap

setcpm(140 / 4)

// ═══════════════════════════════════════════════════════════════
// TRAP HATS - Rolling hi-hat patterns with 808 sub
// ═══════════════════════════════════════════════════════════════

// Hard 808 kick with sub weight
$kick: s("bd ~ ~ ~ bd ~ ~ ~").bank("RolandTR808")
    .gain("<1.3 1.25 1.28 1.22> <1.25 1.22 1.3 [1.35 1.25]>")  // Dynamics
    .shape(slider(0.8, 0, 1))
    .every(4, x => x.s("[bd ~] ~ ~ ~ bd ~ [~ bd] ~"))  // Variation
    .every(8, x => x.s("bd ~ ~ ~ bd ~ [bd bd] ~"))  // 8-bar fill
    .every(16, x => x.s("bd ~ bd ~ bd ~ [bd bd bd bd] [bd*8]"))  // Build
    .color("orange")
    ._punchcard()

// Trap snare on 3 with ghost accents
$snare: stack(
    s("~ ~ ~ ~ sd ~ ~ ~").gain(slider(0.92, 0, 2)).room(0.3),
    s("~ ~ ~ ~ ~ ~ [sd:3 ~] ~").gain(0.28).lpf(5000)  // Ghost snare
).bank("RolandTR808")
    .every(8, x => x.s("~ ~ ~ ~ sd ~ ~ [sd sd sd sd]"))  // Fill
    .every(16, x => x.s("~ ~ ~ ~ sd ~ [sd*4] [sd*8]"))  // Build fill
    .color("white")
    ._punchcard()

// Rolling hi-hats - THE trap signature with builds
$hat: s("[hh hh hh hh] [hh hh hh [hh hh hh]] [hh hh [hh hh hh] hh] [hh [hh hh] hh [hh hh hh hh]]")
    .bank("RolandTR808")
    .gain("<0.5 0.45 0.5 0.55> <0.45 0.5 0.55 0.6>")  // Building velocity
    .pan(sine.range(-0.35, 0.35).fast(slider(2, 1, 8)))  // Fast stereo pan
    .lpf(perlin.range(6000, 12000))  // Tonal variation
    .sometimes(x => x.fast(1.5))  // 16th triplets
    .rarely(x => x.fast(2).gain(0.55))  // 32nd rolls
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh*16]"))  // 8-bar build
    .every(16, x => x.s("[hh*2] [hh*4] [hh*8] [hh*16] [hh*2] [hh*8] [hh*16] [hh*32]"))  // Big build
    .color("white")
    ._punchcard()

// Open hat accents
$oh: s("~ ~ ~ ~ ~ ~ ~ [oh ~]").bank("RolandTR808")
    .gain(slider(0.5, 0, 1.5))
    .room(0.2)
    .sometimes(x => x.s("~ ~ ~ oh ~ ~ ~ [oh ~]"))  // Double open
    .color("lime")
    ._punchcard()

// Clap layer
$clap: s("~ ~ ~ ~ cp ~ ~ ~").bank("RolandTR808")
    .gain(slider(0.45, 0, 1.5))
    .room(0.25)
    .color("gray")

// 808 bass with glide and sub weight
$bass: note("<c1 ~ ~ ~ ~ ~ [c1 d#1] ~ f1 ~ ~ ~ ~ ~ [f1 d#1] c1>")
    .s("sine")
    .lpf(slider(150, 60, 250))  // Sub focus
    .decay(slider(0.35, 0.15, 0.6))  // Long 808 tail
    .gain(slider(0.85, 0, 2))
    .rarely(x => x.note("<c1 ~ ~ ~ d#1 ~ [d#1 f1] ~ f1 ~ ~ ~ ~ ~ [g1 f1] c1>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR808")
    .gain(0.5)
    .room(0.4)
    .slow(2)
