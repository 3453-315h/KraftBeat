// @name Minimal Deep
// @genre House
// @bpm 122
// @tags minimal, deep, hypnotic

setcpm(122 / 4)

// ═══════════════════════════════════════════════════════════════
// MINIMAL DEEP - Hypnotic loops with space and groove
// ═══════════════════════════════════════════════════════════════

// Deep kick with subtle dynamics
$kick: s("bd*4").bank("RolandTR909")
    .gain("<0.95 0.9 0.92 0.9> <0.9 0.92 0.95 0.9>")  // Breathing
    .shape(slider(0.2, 0, 0.5))
    .lpf(slider(200, 80, 300))  // Deep character
    .rarely(x => x.s("[bd bd:1] bd bd bd"))  // Ghost kick
    .every(16, x => x.s("bd bd bd [~ bd] bd bd [bd ~] bd"))  // Sparse variation
    .color("orange")
    ._punchcard()

// Rim with delay - essential minimal character
$rim: s("~ rim ~ rim").bank("RolandTR909")
    .gain(perlin.range(0.38, 0.52))  // Velocity variation
    .delay(slider(0.2, 0, 0.6))
    .delaytime(0.375)  // Triplet delay
    .room(slider(0.35, 0, 1))
    .sometimes(x => x.s("rim ~ [~ rim] rim"))  // Pattern shift
    .every(4, x => x.delay(0.4))  // Longer delay occasionally
    .color("white")
    ._punchcard()

// Shuffled hats with minimal feel
$hat: s("[~ hh] hh [~ hh] hh").bank("RolandTR909")
    .gain(perlin.range(0.28, 0.42))  // Humanized
    .pan(perlin.range(-0.2, 0.2).slow(0.5))
    .nudge(perlin.range(-0.01, 0.015))  // Micro-timing
    .sometimes(x => x.s("[hh ~] hh [~ hh] ~"))  // Sparse variation
    .every(8, x => x.s("[hh ~] [~ hh] [hh hh] [~ oh]"))  // Fill
    ._punchcard()

// Shaker texture with polyrhythmic feel
$shaker: s("shaker*16")
    .gain(perlin.range(0.12, 0.22))  // Very subtle
    .pan(perlin.range(-0.3, 0.3).slow(0.25))
    .euclid(5, 8)  // Polyrhythmic accent
    .lpf(perlin.range(3500, 7000))
    .color("gray")

// Hypnotic loop - the centerpiece
$loop: note("<c4 c4 c4 d4 d#4 d4 c4 c4>")
    .s("triangle")
    .lpf(sine.range(1000, 3500).slow(slider(4.0, 1, 16)))
    .decay(slider(0.15, 0.05, 0.3))
    .delay(0.2)
    .delaytime(0.25)
    .room(0.25)
    .pan(sine.range(-0.3, 0.3).slow(8))  // Slow stereo movement
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.note("<c4 d4 c4 d#4 d4 c4 c4 c4>"))  // Variation
    .rarely(x => x.fast(2).gain(0.4))  // Double-time fills
    .color("cyan")
    .pianoroll({ fold: 1 })

// Counter loop - sparse
$loop2: note("<~ ~ g4 ~ ~ ~ e4 ~>")
    .s("sine")
    .lpf(2500)
    .decay(0.12)
    .delay(0.25)
    .room(0.3)
    .gain(slider(0.3, 0, 1.2))
    .color("yellow")

// Deep sub - foundation
$sub: note("<c1 c1 c1 c1>")
    .s("sine")
    .lpf(80)
    .decay(slider(0.15, 0.05, 0.3))
    .gain(slider(0.65, 0, 2))
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Percussive texture with variations
$perc: s("~ ~ [rim:2 ~] ~").bank("RolandTR909")
    .gain(perlin.range(0.3, 0.45))
    .delay(slider(0.2, 0, 0.6))
    .room(0.25)
    .sometimes(x => x.s("~ rim:2 [~ rim:2] ~"))  // Pattern shift
    .color("brown")
    ._punchcard()

// Atmospheric drone
$drone: note("[c2,g2]")
    .s("sawtooth")
    .lpf(sine.range(150, 600).slow(32))
    .attack(1.5)
    .release(1)
    .room(0.5)
    .gain(slider(0.1, 0, 0.35))
    .slow(8)
    .color("purple")
    .scope({ size: 256 })
