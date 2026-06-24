// @name Glitch Beats
// @genre Experimental
// @bpm 115
// @tags glitch, broken, digital, stutter

setcpm(115 / 4)

// ═══════════════════════════════════════════════════════════════
// GLITCH BEATS - Broken drums and digital artifacts
// ═══════════════════════════════════════════════════════════════

// Glitchy broken kick with chop and shuffle
$kick: s("bd ~ ~ ~").bank("RolandTR909")
    .gain("<0.85 0.92 0.88 0.95>")  // Dynamics
    .shape(slider(0.32, 0, 0.7))
    .sometimesBy(0.3, x => x.chop(4).shuffle())  // Random chop
    .sometimesBy(0.2, x => x.speed(choose(0.5, 2, -1)))  // Speed glitch
    .every(4, x => x.s("[bd bd] ~ ~ ~").chop(8).shuffle())  // More broken
    .every(8, x => x.s("bd [bd bd] ~ [~ bd]"))  // Variation
    .color("orange")
    ._punchcard()

// Glitched snare with speed manipulation
$snare: s("~ sd ~ sd").bank("RolandTR909")
    .gain(slider(0.85, 0, 2))
    .room(slider(0.25, 0, 0.7))
    .sometimesBy(0.25, x => x.speed(choose(0.5, 2, -1)))  // Speed glitch
    .sometimesBy(0.15, x => x.chop(choose(4, 8, 16)).slice(8, irand(8)))  // Slice
    .every(4, x => x.s("~ sd ~ [sd sd sd sd]"))  // Roll
    .every(8, x => x.chop(16).shuffle())  // Full scramble
    .color("white")
    ._punchcard()

// Stuttering hats with shuffle
$hat: s("hh*8").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.52))
    .pan(perlin.range(-0.2, 0.2).slow(0.25))
    .sometimesBy(0.4, x => x.chop(choose(4, 8, 16)).shuffle())  // Shuffle
    .sometimesBy(0.2, x => x.speed(choose(0.25, 0.5, 2, 4)))  // Speed glitch
    .every(4, x => x.s("[hh*4] [hh*8] [hh*16] [hh*4]"))  // Density shift
    .rarely(x => x.rev())  // Reverse
    .color("white")
    ._punchcard()

// Glitchy bass with chop and speed manipulation
$bass: note("<c2 c2 [c2 ~] ~>")
    .s("sawtooth")
    .lpf(sine.range(250, 1200).slow(slider(4.0, 1, 16)))
    .decay(slider(0.12, 0.04, 0.25))
    .gain(slider(0.82, 0, 2))
    .sometimesBy(0.3, x => x.chop(choose(4, 8)).speed(choose(0.5, 1, 2)))  // Chop glitch
    .sometimesBy(0.2, x => x.rev())  // Reverse
    .every(8, x => x.chop(16).shuffle())  // Full scramble
    .scope({ size: 256 })
    .color("red")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Sub layer - more stable
$sub: note("<c1 ~ c1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.48, 0, 1.3))
    .color("darkred")

// Digital artifacts - random samples
$glitch: s("alphabet:*")
    .n(irand(26))
    .chop(choose(4, 8, 16))
    .speed(choose(0.25, 0.5, 1, 2, 4))
    .struct("x(5,16)")
    .lpf(sine.range(2000, 8000).fast(4))
    .gain(slider(0.42, 0, 1.5))
    .pan(perlin.range(-0.5, 0.5))  // Wide stereo
    .room(0.3)
    .sometimes(x => x.struct("x(7,16)"))  // Denser
    .rarely(x => x.rev())  // Reverse
    .color("orange")

// Bitcrush-style synth texture
$texture: note("<c3 eb3 g3 c4>")
    .s("square")
    .lpf(sine.range(500, 3000).fast(choose(2, 4, 8)))
    .chop(choose(4, 8, 16))
    .crush(choose(4, 6, 8))  // Bitcrush
    .gain(slider(0.32, 0, 1.2))
    .room(0.3)
    .delay(0.2)
    .slow(4)
    .sometimesBy(0.3, x => x.shuffle())
    .color("cyan")

// Random glitch hits
$hits: s("cp:*")
    .n(irand(5))
    .struct("x(3,16)")
    .speed(choose(0.5, 1, 2, -1))
    .gain(slider(0.38, 0, 1.3))
    .room(0.4)
    .delay(0.25)
    .sometimes(x => x.chop(8).shuffle())
    .color("magenta")
