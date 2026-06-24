// @name Hypnotic Warehouse
// @genre Techno
// @bpm 132
// @tags hypnotic, warehouse, trippy, loop

setcpm(132 / 4)

// ═══════════════════════════════════════════════════════════════
// HYPNOTIC WAREHOUSE - Trance-inducing loops, endless variation
// ═══════════════════════════════════════════════════════════════

// Punchy warehouse kick with subtle dynamics
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.2 1.15 1.18 1.12> <1.15 1.12 1.2 1.15>")  // Breathing dynamics
    .shape(slider(0.22, 0, 0.55))
    .rarely(x => x.s("[bd bd:1] bd bd bd"))  // Ghost kick
    .every(16, x => x.s("bd bd [~ bd] bd bd bd [bd ~] bd"))  // Hypnotic variation
    .color("orange")
    ._punchcard()

// Driving 16th hats with evolving dynamics
$hat: s("[hh hh hh hh] [hh hh oh hh] [hh hh hh hh] [hh hh hh oh]").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.52))  // Humanized velocity
    .pan(perlin.range(-0.15, 0.15).slow(0.5))  // Stereo sway
    .sometimes(x => x.s("[hh hh hh hh] [hh oh ~ hh] [hh hh hh hh] [oh ~ hh hh]"))  // Variation
    .every(8, x => x.s("[hh*4] [hh*4] [hh hh oh hh hh hh] [hh oh]"))  // Fill
    ._punchcard()

// Clap with space and variations
$clap: stack(
    s("~ cp ~ cp").gain(slider(0.9, 0, 2)).room(0.25),
    s("~ [~ cp:3] ~ ~").gain(0.22).lpf(4500)  // Ghost clap
).bank("RolandTR909")
    .every(8, x => x.s("~ cp ~ [cp cp cp cp]"))  // 8-bar fill
    .color("white")
    ._punchcard()

// Sparse rim for groove texture
$rim: s("~ ~ ~ ~ ~ ~ rim ~").bank("RolandTR909")
    .gain(perlin.range(0.38, 0.52))  // Velocity variation
    .delay(slider(0.2, 0, 0.5))
    .delaytime(0.375)  // Triplet delay for hypnotic feel
    .room(slider(0.35, 0, 0.8))
    .sometimes(x => x.s("~ ~ rim ~ ~ ~ ~ rim"))  // Answer pattern
    .rarely(x => x.delay(0.5))  // Longer delay tail
    ._punchcard()

// THE HYPNOTIC LOOP - one phrase with endless subtle variations
$loop: note("<c3 c3 d#3 c3 g3 d#3 c3 c3>")
    .s("sawtooth")
    .lpf(sine.range(400, 4000).slow(slider(8, 2, 16)))
    .lpq(perlin.range(0.5, 4).slow(4))  // Evolving resonance
    .decay(slider(0.12, 0.03, 0.3))
    .gain(slider(0.6, 0, 2))
    .sometimes(x => x.rev())  // Reverse pattern
    .rarely(x => x.fast(2).lpf(6000))  // Double-time burst
    .every(16, x => x.note("<c3 d#3 g3 d#3 c3 d#3 g3 c4>"))  // Ascending variation
    .color("lime")
    .scope({ size: 256 })
    .pianoroll({ fold: 1 })

// Counter phrase with delay tail
$counter: note("<g4 ~ d#4 ~ c4 ~ d#4 ~ g4 ~ ~ ~ c4 ~ ~ ~>")
    .s("triangle")
    .lpf(sine.range(3000, 6000).slow(8))
    .decay(slider(0.15, 0.04, 0.35))
    .room(slider(0.28, 0, 0.65))
    .delay(0.3)
    .delaytime(0.5)  // Half note delay for hypnosis
    .gain(slider(0.4, 0, 1.5))
    .slow(2)
    .rarely(x => x.note("<a4 ~ f4 ~ d4 ~ f4 ~>"))  // Variation
    .color("cyan")
    ._punchcard()

// Sub bass with minimal movement
$bass: note("<c1 c1 c1 c1 g0 g0 c1 c1>")
    .s("sine")
    .lpf(slider(200, 60, 350))
    .decay(slider(0.1, 0.03, 0.25))
    .gain(slider(0.88, 0, 2))
    .rarely(x => x.note("<c1 c1 g0 g0 c1 c1 d#1 c1>"))  // Occasional movement
    .color("red")

// Atmospheric drone layer
$drone: note("[c2,g2]")
    .s("sawtooth")
    .lpf(sine.range(200, 800).slow(32))
    .attack(1.5)
    .release(1)
    .room(0.6)
    .gain(slider(0.15, 0, 0.5))
    .slow(8)
    .color("purple")
    .scope({ size: 256 })

// Crash for section transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh:3")
    .bank("RolandTR909")
    .gain(0.4)
    .room(0.5)
    .slow(4)
