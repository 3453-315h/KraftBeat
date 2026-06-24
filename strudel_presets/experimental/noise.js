// @name Noise
// @genre Experimental
// @bpm 120
// @tags noise, harsh, industrial, power

setcpm(120 / 4)

// ═══════════════════════════════════════════════════════════════
// NOISE - Harsh industrial noise with extreme textures
// ═══════════════════════════════════════════════════════════════

// Industrial kick - heavy distortion
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.2 1.28 1.22 1.32>")  // Power dynamics
    .shape(slider(0.6, 0, 0.95))  // Heavy distortion
    .every(4, x => x.s("[bd bd bd bd bd bd bd bd]"))  // Machine gun
    .every(8, x => x.s("bd [bd bd] bd [bd bd bd bd]"))  // Fill
    .color("orange")
    ._punchcard()

// Industrial snare with distortion
$snare: s("~ sd ~ sd").bank("RolandTR909")
    .gain(slider(0.95, 0, 2))
    .shape(0.4)  // Distortion
    .room(0.2)
    .every(4, x => x.s("~ sd ~ [sd sd sd sd]"))  // Roll
    .every(8, x => x.fast(2).gain(0.85))  // Intensify
    .color("white")
    ._punchcard()

// Fast harsh hats
$hat: s("hh*16").bank("RolandTR909")
    .gain(perlin.range(0.38, 0.55))
    .lpf(perlin.range(6000, 14000))
    .shape(0.3)  // Distortion
    .every(8, x => x.fast(2).gain(0.45))  // Double-time
    .color("white")
    ._punchcard()

// Harsh noise burst - filtered and gated
$noise: s("noise:0")
    .struct("x(5,8)")
    .lpf(sine.range(500, 8000).fast(slider(4.0, 1, 16)))
    .hpf(300)
    .chop(choose(4, 8, 16))
    .gain(slider(0.72, 0, 2))
    .pan(perlin.range(-0.4, 0.4))
    .every(4, x => x.struct("x(7,8)"))  // Denser
    .sometimes(x => x.speed(choose(0.5, 2, -1)))  // Pitch chaos
    .color("orange")
    .scope({ size: 256 })

// White noise layer
$white: s("noise:0")
    .struct("x(3,16)")
    .lpf(perlin.range(2000, 10000))
    .hpf(1000)
    .gain(slider(0.45, 0, 1.5))
    .pan(perlin.range(-0.5, 0.5))
    .sometimes(x => x.chop(16).shuffle())
    .color("gray")

// Distorted bass
$bass: note("<c1 c1 [c1 d#1] c1>")
    .s("square")
    .lpf(sine.range(200, 1500).fast(slider(4.0, 1, 16)))
    .lpq(sine.range(4, 16).slow(2))  // Aggressive resonance
    .shape(0.5)  // Heavy distortion
    .decay(slider(0.1, 0.03, 0.22))
    .gain(slider(0.85, 0, 2))
    .chop(sine.range(4, 16).slow(4))
    .every(4, x => x.fast(2))  // Double-time bass
    .scope({ size: 256 })
    .color("red")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Sub layer
$sub: note("<c1 ~ c1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.52, 0, 1.5))
    .color("darkred")

// Feedback simulation - high pitched random
$fb: note(choose(60, 72, 84, 96))
    .s("sine")
    .struct("x(2,16)")
    .lpf(choose(4000, 6000, 8000))
    .delay(0.3)
    .room(0.4)
    .slow(slider(8, 4, 16))
    .gain(slider(0.42, 0, 1.5))
    .pan(perlin.range(-0.5, 0.5))
    .sometimes(x => x.struct("x(3,16)"))
    .color("cyan")
    ._punchcard()

// Metallic hits
$metal: s("metal:*")
    .n(irand(5))
    .struct("x(3,16)")
    .speed(choose(0.5, 1, 2, -1))
    .chop(choose(4, 8))
    .gain(slider(0.48, 0, 1.5))
    .room(0.3)
    .delay(0.2)
    .pan(perlin.range(-0.4, 0.4))
    .sometimes(x => x.struct("x(5,16)"))
    .color("yellow")
