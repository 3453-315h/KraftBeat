// @name Berlin Minimal
// @genre Techno
// @bpm 128
// @tags minimal, berlin, groove, hypnotic

setcpm(128 / 4)

// ═══════════════════════════════════════════════════════════════
// BERLIN MINIMAL - Deep groove, hypnotic textures, Berghain feel
// ═══════════════════════════════════════════════════════════════

// Deep kick with subby round character and subtle variations
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.1 1.05 1.08 1.05> <1.05 1.08 1.1 1.05>")  // Subtle dynamics
    .shape(slider(0.15, 0, 0.4))
    .lpf(slider(180, 80, 300))
    .rarely(x => x.s("[bd bd:1] bd bd bd"))  // Occasional ghost kick
    .every(16, x => x.s("bd bd bd [~ bd] bd bd [bd ~] bd"))  // Sparse variation
    .color("orange")
    ._punchcard()

// Minimal shuffled hats with human feel
$hat: s("[~ hh] ~ [~ hh] [hh ~]").bank("RolandTR909")
    .gain(perlin.range(0.28, 0.42))  // Humanized velocity
    .nudge(perlin.range(-0.01, 0.02))  // Micro-timing variations
    .pan(perlin.range(-0.2, 0.2).slow(0.5))  // Stereo movement
    .sometimes(x => x.s("[~ hh] [hh ~] [~ hh] ~"))  // Pattern variation
    .every(8, x => x.s("[hh ~] [~ hh] [hh hh] [~ oh]"))  // 8-bar fill
    ._punchcard()

// Rim click groove - essential Berlin minimal character
$rim: s("~ ~ [rim ~] ~ ~ rim ~ ~").bank("RolandTR909")
    .gain(perlin.range(0.4, 0.55))  // Velocity variation
    .delay(slider(0.15, 0, 0.4))
    .room(slider(0.25, 0, 0.6))
    .sometimes(x => x.s("~ rim [rim ~] ~ ~ [~ rim] ~ rim"))  // Variation
    .every(4, x => x.delaytime(0.375))  // Triplet delay occasionally
    .color("white")
    ._punchcard()

// Tom groove for depth (classic minimal techno element)
$tom: s("~ ~ ~ ~ [tom:3 ~] ~ ~ ~").bank("RolandTR808")
    .gain(slider(0.35, 0, 1.2))
    .lpf(400)
    .room(0.2)
    .sometimes(x => x.s("~ ~ [tom:3 tom:2] ~ ~ ~ [~ tom:1] ~"))  // Tom groove
    .color("brown")

// Sparse clap with reverb tail
$clap: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ cp ~").bank("RolandTR909")
    .gain(slider(0.65, 0, 2))
    .room(slider(0.4, 0, 0.9))
    .delay(0.2)
    .every(8, x => x.s("~ ~ ~ cp ~ ~ ~ ~ ~ ~ ~ ~ ~ cp cp ~"))  // Variation
    ._punchcard()

// Subtle shaker texture with polyrhythmic feel
$shaker: s("shaker*16")
    .gain(perlin.range(0.12, 0.22))  // Very subtle velocity
    .pan(sine.range(-0.3, 0.3).slow(4))
    .lpf(perlin.range(4000, 8000))  // Tonal variation
    .euclid(5, 8)  // Polyrhythmic accent
    ._punchcard()

// Minimal bass - hypnotic one-note groove with filter modulation
$bass: note("<c2 ~ c2 ~ c2 ~ c2 ~ c2 ~ c2 ~ c2 c2 ~ ~>")
    .s("sine")
    .lpf(sine.range(200, 600).slow(8))
    .decay(slider(0.12, 0.04, 0.3))
    .gain(slider(0.85, 0, 2))
    .rarely(x => x.note("<c2 ~ g1 ~ c2 ~ eb2 ~>"))  // Occasional movement
    .scope({ size: 256 })
    .color("red")

// Sub layer for depth
$sub: note("c1")
    .s("sine")
    .lpf(80)
    .gain(slider(0.5, 0, 1.2))
    .color("darkred")

// Hypnotic stab - sparse with long delay tail
$stab: note("<[c4,g4] ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ [g3,d4] ~ ~ ~>")
    .s("triangle")
    .lpf(sine.range(800, 2500).slow(16))
    .decay(slider(0.2, 0.05, 0.5))
    .delay(slider(0.25, 0, 0.6))
    .delaytime(0.375)  // Triplet delay for hypnotic feel
    .room(slider(0.35, 0, 0.8))
    .gain(slider(0.35, 0, 1.5))
    .rarely(x => x.fast(2).delay(0.4))  // Double stab with more delay
    .color("cyan")
    ._punchcard()

// Atmospheric pad drone
$atmo: note("[c3,g3]")
    .s("sawtooth")
    .lpf(sine.range(400, 1200).slow(32))
    .attack(2)
    .release(2)
    .room(0.6)
    .gain(slider(0.12, 0, 0.4))
    .slow(8)
    .color("purple")
    .scope({ size: 256 })
