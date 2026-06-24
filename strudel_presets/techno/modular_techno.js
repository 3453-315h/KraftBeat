// @name Modular Techno
// @genre Techno
// @bpm 130
// @tags modular, generative, evolving, eurorack

setcpm(130 / 4)

// ═══════════════════════════════════════════════════════════════
// MODULAR TECHNO - Generative, evolving patterns, Eurorack feel
// ═══════════════════════════════════════════════════════════════

// Kick with evolving shape modulation and variations
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.15 1.1 1.12 1.08>")  // Subtle dynamics
    .shape(sine.range(0.12, 0.28).slow(16))  // Evolving saturation
    .rarely(x => x.s("[bd bd:1] bd bd bd"))  // Ghost kick
    .every(8, x => x.s("bd bd bd bd [bd bd] bd bd"))  // 8-bar phrase
    .every(16, x => x.s("[bd ~] bd bd [~ bd] bd bd [bd bd bd bd] bd"))  // 16-bar evolution
    .color("orange")
    ._punchcard()

// Evolving hat pattern with euclidean variations
$hat: s("[hh hh] [hh [~ hh]] [hh hh] [oh ~]").bank("RolandTR909")
    .gain(perlin.range(0.32, 0.48))  // Humanized velocity
    .pan(sine.range(-0.25, 0.25).slow(8))  // Stereo movement
    .sometimes(x => x.euclid(5, 8))  // Euclidean rhythm
    .rarely(x => x.euclid(7, 16))  // Complex euclidean
    .every(8, x => x.s("[hh hh] [hh hh] [hh hh hh hh] [oh hh]"))  // Fill
    ._punchcard()

// Generative shaker with polyrhythmic feel
$shaker: s("shaker*16")
    .euclid(slider(5, 3, 11), 16)  // Variable euclidean pattern
    .gain(perlin.range(0.15, 0.28))
    .pan(perlin.range(-0.4, 0.4).slow(0.25))
    .lpf(perlin.range(3000, 8000))
    .color("gray")
    ._punchcard()

// Clap with evolving reverb space
$clap: s("~ cp ~ cp").bank("RolandTR909")
    .gain(slider(0.85, 0, 2))
    .room(sine.range(0.1, 0.45).slow(12))  // Breathing reverb
    .sometimes(x => x.s("~ cp ~ [cp cp:3]"))  // Ghost variation
    .every(8, x => x.s("~ cp [~ cp:3] [cp cp cp cp]"))  // 8-bar fill
    .color("white")
    ._punchcard()

// Rim click with evolving delay
$rim: s("~ ~ [rim ~] ~ ~ rim ~ ~").bank("RolandTR909")
    .gain(perlin.range(0.35, 0.5))
    .delay(sine.range(0.1, 0.4).slow(8))  // Evolving delay
    .room(0.25)
    .sometimes(x => x.s("rim ~ [rim ~] ~ ~ [~ rim] ~ rim"))  // Pattern shift
    .color("brown")
    ._punchcard()

// Modular sequence - filter sweeping generatively
$seq: note("<c3 d#3 g3 c4 d#4 g4 c4 g3>")
    .s("sawtooth")
    .lpf(sine.range(350, 4500).slow(slider(8, 2, 16)))
    .lpq(perlin.range(0.5, 5).slow(4))  // Evolving resonance
    .decay(slider(0.1, 0.03, 0.25))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.rev())  // Reverse pattern
    .rarely(x => x.fast(2))  // Double-time
    .color("lime")
    .scope({ size: 256 })
    .pianoroll({ fold: 1 })

// Generative melody - random notes from scale with euclidean gating
$melody: n(choose(48, 51, 55, 60, 63, 67))
    .s("triangle")
    .lpf(sine.range(2500, 5000).slow(16))
    .struct("x(5,16)")
    .decay(slider(0.18, 0.05, 0.4))
    .delay(slider(0.22, 0, 0.55))
    .room(slider(0.32, 0, 0.75))
    .gain(slider(0.38, 0, 1.5))
    .rarely(x => x.struct("x(7,16)"))  // Denser pattern
    .sometimes(x => x.struct("x(3,8)"))  // Sparser pattern
    .color("cyan")
    ._punchcard()

// Secondary generative voice - different timbre
$melody2: n(choose(60, 63, 67, 72, 75))
    .s("sine")
    .struct("x(3,8)")
    .lpf(2500)
    .decay(0.25)
    .delay(0.35)
    .room(0.4)
    .gain(perlin.range(0.15, 0.3))
    .pan(perlin.range(-0.5, 0.5))
    .color("yellow")

// Sub bass with generator feel
$bass: note("<c1 c1 c1 c1 g0 g0 c1 c1>")
    .s("sine")
    .lpf(sine.range(200, 350).slow(16))  // Subtle filter movement
    .decay(slider(0.12, 0.04, 0.3))
    .gain(slider(0.85, 0, 2))
    .rarely(x => x.note("<c1 c1 g0 g0 c1 c1 d#1 c1>"))  // Pattern variation
    .color("red")

// Modular drone - slowly evolving pad
$drone: note("<c2 g2>")
    .s("sawtooth")
    .lpf(sine.range(150, 1000).slow(32))
    .lpq(perlin.range(0.2, 1.5).slow(8))  // Gentle resonance
    .attack(slider(0.8, 0.3, 1.5))
    .release(slider(0.6, 0.2, 1.2))
    .room(slider(0.45, 0, 0.9))
    .gain(slider(0.25, 0, 0.9))
    .slow(8)
    .color("purple")
    .scope({ size: 256 })

// Background texture - evolving noise
$texture: s("noise")
    .lpf(perlin.range(300, 1500).slow(16))
    .hpf(200)
    .gain(perlin.range(0.03, 0.1))
    .room(0.5)
    .color("darkgray")

// Crash for section changes
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh:3")
    .bank("RolandTR909")
    .gain(0.4)
    .room(0.5)
    .slow(4)
