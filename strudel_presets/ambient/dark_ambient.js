// @name Dark Ambient
// @genre Ambient
// @bpm 40
// @tags dark, horror, tension, cinematic

setcpm(40 / 4)

// ═══════════════════════════════════════════════════════════════
// DARK AMBIENT - Unsettling textures and tension
// ═══════════════════════════════════════════════════════════════

// Dark droning pad - descending chromatic movement
$drone: note("<c2 b1 a#1 a1>")
    .s("sawtooth")
    .lpf(sine.range(300, 1200).slow(slider(16, 8, 32)))
    .lpq(sine.range(1, 4).slow(24))  // Unsettling resonance
    .attack(slider(1.5, 0.6, 3))
    .release(slider(2, 0.8, 4))
    .slow(slider(8, 4, 16))
    .gain(slider(0.55, 0, 1.8))
    .sometimes(x => x.note("<c2 c#2 d2 c2>"))  // Dissonant variation
    .color("cyan")
    .pianoroll({ fold: 1 })
    .scope({ size: 256 })

// Second drone layer for depth
$drone2: note("<f#1 ~ ~ ~ g1 ~ ~ ~>")
    .s("sawtooth")
    .lpf(sine.range(200, 600).slow(24))
    .attack(2)
    .release(2.5)
    .room(0.5)
    .gain(slider(0.35, 0, 1.2))
    .slow(16)
    .color("purple")

// Dissonant texture - tritone intervals
$texture: note("<c3 d#3 f#3 a3>")
    .s("triangle")
    .lpf(sine.range(500, 2000).slow(slider(12, 4, 24)))
    .attack(slider(1.2, 0.5, 2.5))
    .release(slider(1.5, 0.6, 3))
    .room(slider(0.45, 0, 1))
    .delay(0.3)
    .delaytime(0.666)
    .slow(slider(8, 4, 16))
    .gain(slider(0.38, 0, 1.5))
    .sometimes(x => x.note("<d#3 f#3 a3 c4>"))  // Shift
    .color("red")
    .scope({ size: 256 })

// Random unsettling metal hits
$hits: s("metal:0")
    .struct("x(2,16)")
    .speed(choose(0.3, 0.5, 0.7, -0.5))  // Include reverse
    .chop(choose(4, 8))
    .room(slider(0.55, 0, 1))
    .delay(slider(0.35, 0.1, 0.7))
    .delaytime(0.5)
    .slow(slider(8, 4, 16))
    .gain(slider(0.42, 0, 1.5))
    .pan(perlin.range(-0.5, 0.5))  // Wide random
    .sometimes(x => x.struct("x(3,16)"))  // More frequent
    .color("orange")
    ._punchcard()

// Scraping texture
$scrape: s("noise:0")
    .struct("x(1,16)")
    .lpf(sine.range(1500, 5000).fast(choose(2, 4)))
    .hpf(800)
    .chop(choose(8, 16))
    .speed(choose(0.5, -0.5, 0.75))
    .gain(slider(0.28, 0, 1))
    .room(0.5)
    .delay(0.4)
    .slow(16)
    .sometimes(x => x.struct("x(2,16)"))
    .color("gray")

// Sub rumble - foundation
$rumble: note("c0")
    .s("sine")
    .lpf(60)
    .attack(2)
    .decay(slider(3, 1.5, 6))
    .slow(slider(8, 4, 16))
    .gain(slider(0.48, 0, 1.5))
    .sometimes(x => x.note("b-1"))  // Lower rumble
    .color("darkred")

// High tension notes - sparse and unsettling
$tension: note("<~ ~ ~ ~ c6 ~ ~ ~ ~ ~ ~ ~ f#5 ~ ~ ~>")
    .s("sine")
    .lpf(6000)
    .decay(0.8)
    .delay(0.4)
    .delaytime(0.666)
    .room(0.6)
    .gain(slider(0.22, 0, 0.8))
    .slow(8)
    .color("yellow")
