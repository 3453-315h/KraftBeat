// @name Vocal House
// @genre House
// @bpm 125
// @tags vocal, chopped, uplifting, samples

setcpm(125 / 4)

// ═══════════════════════════════════════════════════════════════
// VOCAL HOUSE - Chopped vocals and uplifting energy
// ═══════════════════════════════════════════════════════════════

// Punchy kick with dynamics
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.0 0.95 0.98 0.95> <0.95 0.98 1.0 [1.05 0.98]>")  // Dynamics
    .shape(slider(0.28, 0, 0.6))
    .every(8, x => x.s("bd bd bd bd [bd bd] bd bd"))  // 8-bar phrase
    .every(16, x => x.s("bd bd bd [bd bd] bd bd [bd*4] bd"))  // Build
    .color("orange")
    ._punchcard()

// Rolling 16th hats with groove
$hat: s("hh*16").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.5))  // Humanized
    .pan(perlin.range(-0.1, 0.1).slow(0.25))
    .sometimes(x => x.s("[hh*4] [hh hh oh hh] [hh*4] [hh hh hh oh]"))  // Open hat accents
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh oh hh*4]"))  // Fill
    ._punchcard()

// Clap with reverb
$clap: stack(
    s("~ cp ~ cp").gain(slider(0.85, 0, 2)).room(0.35),
    s("~ [~ cp:3] ~ ~").gain(0.2).lpf(4500)  // Ghost
).bank("RolandTR909")
    .every(8, x => x.s("~ cp ~ [cp cp cp cp]"))  // Fill
    .color("yellow")
    ._punchcard()

// Shaker for groove
$shaker: s("shaker*16")
    .gain(perlin.range(0.18, 0.28))
    .pan(perlin.range(-0.3, 0.3).slow(0.25))
    .color("gray")

// Chopped vocal simulation with variations
$vocal: s("alphabet:*")
    .n(choose(0, 4, 8, 14, 20))
    .struct("[~ x] ~ [x ~] x")
    .chop(16)
    .slice(8, "<0 1 2 3 4 5 6 7>")
    .speed(choose(1, 1.25))
    .room(slider(0.35, 0, 1))
    .delay(slider(0.22, 0, 0.6))
    .delaytime(0.25)
    .gain(slider(0.58, 0, 2))
    .sometimes(x => x.struct("[x ~] x [~ x] ~"))  // Pattern variation
    .rarely(x => x.fast(2).gain(0.45))  // Double-time fills
    .every(8, x => x.struct("x x x [x x]"))  // Dense fill
    .color("orange")

// Secondary vocal layer
$vocal2: s("alphabet:*")
    .n(choose(1, 5, 12))
    .struct("~ ~ [~ x] ~")
    .chop(8)
    .speed(0.75)
    .delay(0.3)
    .room(0.4)
    .gain(slider(0.3, 0, 1.2))
    .color("pink")

// House bass with octave movement
$bass: note("<c2 ~ [c2 c3] ~ g2 ~ [f2 g2] ~>")
    .s("sawtooth")
    .lpf(sine.range(300, 750).slow(slider(4.0, 1, 16)))
    .decay(slider(0.12, 0.04, 0.25))
    .gain(slider(0.78, 0, 2))
    .rarely(x => x.note("<c2 c3 [c2 d2] g2>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ c1 ~ g1 ~ f1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.4, 0, 1.2))
    .color("darkred")

// Organ stabs with movement
$organ: note("<[c4,e4,g4] ~ ~ ~ [f4,a4,c5] ~ ~ ~>")
    .s("triangle")  // Organ-like
    .lpf(sine.range(2500, 5000).slow(slider(4.0, 1, 16)))
    .decay(0.2)
    .room(slider(0.3, 0, 1))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.48, 0, 2))
    .sometimes(x => x.note("<[d4,f4,a4] ~ [e4,g4,b4] ~>"))  // Variation
    .color("cyan")
    ._punchcard()

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.45)
    .room(0.4)
    .slow(2)
