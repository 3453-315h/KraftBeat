// @name Breakcore
// @genre Experimental
// @bpm 180
// @tags breakcore, chaotic, fast, amen

setcpm(180 / 4)

// ═══════════════════════════════════════════════════════════════
// BREAKCORE - Chaotic chopped amen with intense energy
// ═══════════════════════════════════════════════════════════════

// Chaotic chopped amen break - the core sound
$break: s("amen:*")
    .n(irand(8))
    .chop(choose(4, 8, 16, 32))
    .shuffle()
    .speed(choose(0.5, 1, 1.5, 2, -1, -0.5))
    .gain(slider(0.82, 0, 2))
    .pan(perlin.range(-0.3, 0.3))  // Chaotic stereo
    .sometimes(x => x.rev())  // Sometimes reverse
    .every(4, x => x.chop(32).speed(choose(2, 4, -2)))  // Faster chopping
    .color("orange")
    ._punchcard()

// Distorted kick accent with gabber influence
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.15 1.22 1.18 1.25>")  // Power dynamics
    .shape(slider(0.5, 0, 0.9))  // Heavy distortion
    .sometimesBy(0.5, x => x.fast(choose(2, 4, 8)))  // Random speed-ups
    .sometimesBy(0.3, x => x.speed(choose(0.5, 2)))  // Pitch shift
    .every(4, x => x.s("[bd bd bd bd bd bd bd bd]"))  // Machine gun
    .color("red")
    ._punchcard()

// Snare chaos layer
$snare: s("sd").bank("RolandTR909")
    .gain(slider(0.88, 0, 2))
    .room(0.2)
    .struct("x(5,8)")
    .sometimesBy(0.4, x => x.chop(choose(4, 8)).shuffle())
    .sometimesBy(0.3, x => x.speed(choose(0.5, 2, -1)))
    .every(4, x => x.struct("x(7,8)"))  // Denser
    .rarely(x => x.rev())
    .color("white")
    ._punchcard()

// Chaotic bassline with random notes
$bass: note(choose(24, 26, 27, 29, 31, 32))
    .s("square")
    .lpf(sine.range(300, 2000).fast(slider(4.0, 1, 16)))
    .lpq(sine.range(4, 12).slow(2))  // Heavy resonance
    .struct("x(7,8)")
    .decay(slider(0.1, 0.03, 0.22))
    .gain(slider(0.82, 0, 2))
    .sometimesBy(0.3, x => x.speed(choose(0.5, 2)))  // Pitch chaos
    .every(4, x => x.struct("x(9,16)"))  // Pattern shift
    .scope({ size: 256 })
    .color("red")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Sub layer - more stable foundation
$sub: note("<c1 ~ c1 ~ c1 ~ c1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.48, 0, 1.3))
    .color("darkred")

// Gabber kick hits for intensity
$gabber: s("gabba:0")
    .struct("~ ~ ~ ~ x ~ ~ ~")
    .speed(slider(0.6, 0.4, 1.5))
    .gain(slider(0.72, 0, 2))
    .sometimesBy(0.3, x => x.struct("x ~ ~ ~ x ~ x ~"))  // More hits
    .every(8, x => x.struct("[x ~ x ~] ~ [x x] ~"))  // Intensify
    .color("orange")
    ._punchcard()

// Scream synth stabs
$scream: note("<c5 ~ d#5 ~ f5 ~ d#5 ~>")
    .s("sawtooth")
    .lpf(sine.range(1500, 6000).fast(8))
    .lpq(10)  // Aggressive resonance
    .decay(0.08)
    .gain(slider(0.48, 0, 1.8))
    .struct("x(5,8)")
    .sometimesBy(0.4, x => x.fast(2))  // Double-time
    .sometimes(x => x.rev())
    .color("magenta")

// Noise burst accents
$noise: s("noise:0")
    .struct("x(3,16)")
    .chop(choose(4, 8))
    .speed(choose(0.5, 1, 2))
    .lpf(sine.range(2000, 10000).fast(4))
    .gain(slider(0.32, 0, 1.2))
    .pan(perlin.range(-0.5, 0.5))
    .sometimes(x => x.struct("x(5,16)"))
    .color("gray")
