// @name Forest
// @genre Ambient
// @bpm 55
// @tags forest, nature, organic, peaceful

setcpm(55 / 4)

// ═══════════════════════════════════════════════════════════════
// FOREST - Organic nature sounds and peaceful atmosphere
// ═══════════════════════════════════════════════════════════════

// Bird-like sounds - random high notes in stereo
$birds: n(choose(72, 76, 79, 84, 88, 91))
    .s("sine")
    .struct("x(3,16)")
    .attack(slider(0.02, 0.01, 0.08))
    .decay(0.4)
    .pan(perlin.range(-0.6, 0.6))  // Wide random stereo
    .delay(0.2)
    .delaytime(0.375)
    .room(0.4)
    .slow(slider(8, 4, 16))
    .gain(slider(0.35, 0, 1.2))
    .sometimes(x => x.struct("x(5,16)"))  // More birds
    .rarely(x => x.struct("x(2,16)"))  // Fewer birds
    .color("orange")
    ._punchcard()

// Second bird layer - chirps
$chirps: n(choose(84, 88, 91, 96))
    .s("sine")
    .struct("x(2,16)")
    .attack(0.01)
    .decay(0.2)
    .pan(perlin.range(-0.5, 0.5))
    .delay(0.15)
    .slow(slider(8, 4, 16))
    .gain(slider(0.22, 0, 0.9))
    .offset(8)  // Don't overlap with main birds
    .color("yellow")

// Wind through trees - filtered noise
$wind: s("noise:0")
    .loop()
    .lpf(sine.range(400, 2000).slow(slider(16, 8, 32)))
    .hpf(200)
    .attack(slider(1, 0.5, 2.5))
    .release(slider(1.2, 0.5, 3))
    .slow(slider(8, 4, 16))
    .gain(slider(0.35, 0, 1.2))
    .color("cyan")
    .scope({ size: 256 })

// Deep earth drone - grounding
$earth: note("c1")
    .s("sine")
    .lpf(sine.range(80, 250).slow(slider(24, 8, 48)))
    .attack(slider(2, 1, 4))
    .release(slider(2.5, 1, 5))
    .slow(slider(8, 4, 16))
    .gain(slider(0.42, 0, 1.5))
    .color("brown")

// Earth harmonic
$earth2: note("g1")
    .s("sine")
    .lpf(150)
    .attack(2)
    .release(2)
    .gain(slider(0.28, 0, 1))
    .slow(16)
    .color("darkred")

// Organic percussion - wood sounds
$perc: s("woodblock:*")
    .n(irand(4))
    .struct("x(2,16)")
    .speed(choose(0.7, 1, 1.3))
    .room(slider(0.35, 0, 0.9))
    .delay(0.15)
    .slow(slider(8, 4, 16))
    .gain(slider(0.32, 0, 1.2))
    .pan(perlin.range(-0.3, 0.3))
    .sometimes(x => x.struct("x(3,16)"))
    .color("pink")
    ._punchcard()

// Leaves rustling - high filtered noise
$leaves: s("noise:0")
    .loop()
    .lpf(perlin.range(3000, 8000))
    .hpf(2000)
    .gain(perlin.range(0.08, 0.2))  // Fluctuating
    .slow(slider(8, 4, 16))
    .color("lime")

// Gentle stream hint - subtle texture
$stream: s("noise:0")
    .loop()
    .lpf(sine.range(800, 2500).slow(12))
    .hpf(500)
    .gain(slider(0.15, 0, 0.5))
    .slow(16)
    .color("blue")

// Pad layer for atmosphere
$pad: note("[c3,e3,g3]")
    .s("triangle")
    .lpf(sine.range(400, 1200).slow(32))
    .attack(1.5)
    .release(2)
    .room(0.5)
    .gain(slider(0.22, 0, 0.8))
    .slow(8)
    .color("purple")
    .scope({ size: 256 })
