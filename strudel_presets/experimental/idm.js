// @name IDM
// @genre Experimental
// @bpm 135
// @tags idm, glitchy, complex, aphex

setcpm(135 / 4)

// ═══════════════════════════════════════════════════════════════
// IDM - Intelligent dance music with complex rhythms
// ═══════════════════════════════════════════════════════════════

// Complex polyrhythmic kick
$kick: s("bd").struct("x(3,8)").bank("RolandTR909")
    .gain("<1.0 1.05 0.98 1.08>")  // Dynamics
    .shape(slider(0.32, 0, 0.7))
    .every(4, x => x.struct("x(5,8)"))  // Pattern shift
    .every(8, x => x.struct("x(7,16)"))  // More complex
    .sometimesBy(0.2, x => x.speed(choose(0.5, 2)))  // Occasional pitch
    .color("orange")
    ._punchcard()

// Glitchy snare with speed manipulation
$snare: s("sd").struct("x(5,8)").bank("RolandTR909")
    .gain(slider(0.88, 0, 2))
    .room(0.25)
    .sometimesBy(0.3, x => x.speed(choose(0.5, 2, -1)))  // Speed glitch
    .sometimesBy(0.2, x => x.chop(choose(4, 8)).shuffle())  // Chop
    .every(4, x => x.struct("x(7,16)"))  // Shift
    .every(8, x => x.struct("x(3,8)"))  // Simplify
    .color("white")
    ._punchcard()

// Polyrhythmic hats
$hat: s("hh").struct("x(9,16)").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.52))  // Humanized
    .pan(perlin.range(-0.2, 0.2).slow(0.25))
    .every(4, x => x.struct("x(11,16)"))  // Denser
    .every(8, x => x.struct("x(7,12)"))  // Different polyrhythm
    .sometimesBy(0.2, x => x.speed(choose(0.5, 2)))
    .color("white")
    ._punchcard()

// Rim polyrhythm layer
$rim: s("rim").struct("x(5,12)").bank("RolandTR909")
    .gain(perlin.range(0.42, 0.58))
    .every(4, x => x.struct("x(7,12)"))
    .color("yellow")
    ._punchcard()

// Glitchy melodic synth with random elements
$synth: n(choose(0, 2, 4, 5, 7, 9, 11).add(choose(0, 12, 24)))
    .scale("c:minor")
    .s("triangle")
    .struct("x(7,16)")
    .lpf(choose(500, 1000, 2000, 4000))
    .decay(choose(0.05, 0.1, 0.2))
    .delay(0.2)
    .delaytime(0.375)
    .room(0.3)
    .pan(perlin.range(-0.5, 0.5))  // Wide random stereo
    .gain(slider(0.52, 0, 2))
    .every(4, x => x.struct("x(9,16)"))  // Pattern shift
    .sometimes(x => x.rev())  // Reverse phrase
    .scope({ size: 256 })
    .color("magenta")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Arp layer
$arp: n("<0 4 7 11 7 4>")
    .scale("c:minor")
    .struct("x(5,8)")
    .s("sine")
    .lpf(3500)
    .decay(0.12)
    .delay(0.25)
    .delaytime(0.25)
    .room(0.3)
    .trans(12)
    .gain(slider(0.35, 0, 1.3))
    .every(4, x => x.struct("x(7,12)"))
    .sometimes(x => x.add(12))  // Octave up
    .color("cyan")

// Bass with euclidean rhythm
$bass: n("<0 5 3 7>")
    .scale("c:minor")
    .struct("x(5,8)")
    .s("sawtooth")
    .lpf(sine.range(250, 800).slow(slider(8, 4, 16)))
    .trans(-12)
    .decay(slider(0.12, 0.05, 0.25))
    .gain(slider(0.78, 0, 2))
    .every(4, x => x.struct("x(7,16)"))  // Pattern shift
    .every(8, x => x.struct("x(3,8)"))  // Sparser
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: n("<0 ~ 0 ~ 5 ~ 3 ~>")
    .scale("c:minor")
    .s("sine")
    .lpf(80)
    .trans(-24)
    .gain(slider(0.48, 0, 1.3))
    .color("darkred")

// Granular texture - alphabet samples
$grain: s("alphabet:*")
    .n(irand(26))
    .chop(choose(4, 8, 16))
    .speed(choose(0.25, 0.5, 1, 2))
    .struct("x(5,16)")
    .lpf(sine.range(1500, 6000).fast(4))
    .gain(slider(0.35, 0, 1.3))
    .pan(perlin.range(-0.4, 0.4))
    .room(0.3)
    .sometimes(x => x.rev())
    .rarely(x => x.struct("x(7,16)"))
    .color("orange")

// Pad layer for atmosphere
$pad: n("<[0,4,7] [2,5,9] [4,7,11] [0,4,7]>")
    .scale("c:minor")
    .s("sawtooth")
    .lpf(sine.range(600, 1800).slow(16))
    .attack(0.4)
    .release(0.5)
    .room(0.5)
    .trans(-12)
    .gain(slider(0.28, 0, 1))
    .slow(4)
    .color("purple")
    .scope({ size: 256 })
