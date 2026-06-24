// @name Future Bass
// @genre Dubstep
// @bpm 150
// @tags future, chords, emotional, supersaw

setcpm(150 / 4)

// ═══════════════════════════════════════════════════════════════
// FUTURE BASS - Emotional supersaw chords with half-time drums
// ═══════════════════════════════════════════════════════════════

// Half-time kick with dynamics
$kick: s("bd ~ ~ ~ ~ ~ ~ ~ bd ~ ~ ~ ~ ~ ~ ~").bank("RolandTR808")
    .gain("<1.1 1.05 1.08 1.02> <1.05 1.02 1.1 [1.15 1.05]>")  // Dynamics
    .shape(slider(0.28, 0, 0.55))
    .every(8, x => x.s("bd ~ ~ bd ~ ~ ~ ~ bd ~ ~ ~ ~ ~ bd ~"))  // Variation
    .every(16, x => x.s("bd ~ bd ~ ~ ~ ~ ~ bd ~ bd ~ ~ ~ [bd bd] bd"))  // Build
    .color("orange")
    ._punchcard()

// Snare on 3 with ghost and reverb
$snare: stack(
    s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ sd ~ ~ ~").gain(slider(0.95, 0, 2)).room(slider(0.3, 0, 0.7)),
    s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ [sd:3 ~] ~ ~").gain(0.25).lpf(5000)  // Ghost
).bank("RolandTR808")
    .every(8, x => x.s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ sd ~ [sd sd] sd"))  // Fill
    .every(16, x => x.s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ sd [sd sd] [sd*4] [sd*8]"))  // Build
    ._punchcard()

// Rolling hats with stereo movement
$hat: s("hh*16").bank("RolandTR808")
    .gain(perlin.range(0.32, 0.48))  // Humanized
    .pan(perlin.range(-0.15, 0.15).slow(0.25))
    .lpf(perlin.range(5000, 10000))
    .sometimes(x => x.s("[hh*4] [hh hh oh hh] [hh*4] [hh hh hh oh]"))  // Accents
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh*16]"))  // Build
    ._punchcard()

// FUTURE BASS SUPERSAWS - the signature emotional sound
$chords: note("<[c4,e4,g4,b4] [c4,e4,g4,b4] [a3,c4,e4,g4] [g3,b3,d4,f4]>")
    .s("sawtooth")
    .lpf(sine.range(1500, 6000).slow(slider(4.0, 1, 16)))
    .lpq(sine.range(1, 4).slow(8))  // Gentle resonance sweep
    .attack(slider(0.08, 0.02, 0.2))
    .release(slider(0.35, 0.15, 0.7))
    .room(slider(0.4, 0, 1))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.6, 0, 2))
    .jux(x => x.lpf(3500))  // Stereo width
    .sometimes(x => x.note("<[d4,f4,a4,c5] [e4,g4,b4,d5]>"))  // Chord variation
    .color("purple")
    ._punchcard()
    .pianoroll({ fold: 1 })
    .scope({ size: 256 })

// Wobbly sub with movement
$sub: note("<c1 ~ c1 ~ a0 ~ g0 ~>")
    .s("sine")
    .lpf(sine.range(60, 150).fast(slider(4.0, 1, 16)))  // Sub wobble
    .decay(slider(0.2, 0.1, 0.4))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.65, 0, 2))
    .rarely(x => x.note("<c1 c1 [c1 d1] a0 g0 g0 [g0 a0] c1>"))  // Variation
    .scope({ size: 256 })
    .color("cyan")
    ._punchcard()

// Arpeggiated lead with stereo jux
$arp: note("<c5 e5 g5 b5 g5 e5 c5 d5>")
    .s("triangle")
    .lpf(sine.range(3000, 7000).slow(slider(4.0, 1, 16)))
    .decay(0.15)
    .delay(slider(0.25, 0, 0.6))
    .delaytime(0.25)
    .room(slider(0.35, 0, 0.8))
    .gain(slider(0.45, 0, 1.8))
    .jux(rev)  // Stereo reversal
    .sometimes(x => x.note("<c5 g5 e5 b5 a5 e5 c5 d5>"))  // Variation
    .rarely(x => x.fast(2))  // Double-time
    .color("lime")
    ._punchcard()

// Secondary arp layer
$arp2: note("<~ ~ g5 ~ ~ ~ e5 ~>")
    .s("sine")
    .lpf(5000)
    .decay(0.12)
    .delay(0.3)
    .room(0.35)
    .gain(slider(0.28, 0, 1))
    .color("yellow")

// Crash for drops
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR808")
    .gain(0.5)
    .room(0.5)
    .slow(2)
