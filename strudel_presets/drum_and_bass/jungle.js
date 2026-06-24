// @name Jungle
// @genre Drum and Bass
// @bpm 168
// @tags jungle, ragga, reggae, breaks

setcpm(168 / 4)

// ═══════════════════════════════════════════════════════════════
// JUNGLE - Ragga-influenced breaks with dub vibes
// ═══════════════════════════════════════════════════════════════

// Chopped amen with speed variations - jungle signature
$break: s("amen:0 amen:1 [amen:2 amen:3] amen:4")
    .speed("<1 1.25 1 1.5>")
    .gain(perlin.range(0.65, 0.88))  // Humanized dynamics
    .chop(16)
    .slice(8, "<0 1 2 3 4 5 6 7>")
    .sometimes(x => x.speed("<1.5 1.25 1 0.75>"))  // Speed variation
    .rarely(x => x.rev())  // Reverse break
    .every(4, x => x.speed("<1 [1.5 1] 1 [1 1.25]>"))  // 4-bar variation
    .every(8, x => x.chop(32).speed("<1 [1.5 2] 1 [1 1.5 2 1]>"))  // Faster chops
    .color("orange")
    ._punchcard()

// Additional break layer for fills
$break2: s("~ ~ ~ ~ ~ ~ amen:5 amen:6")
    .speed("<1.25 1 1.5 0.75>")
    .gain(0.4)
    .chop(8)
    .rarely(x => x.s("amen:7 amen:8 [amen:9 amen:10] amen:11"))  // Fill
    .color("brown")

// Sub bass with octave jumps - dub reggae influence
$bass: note("<c2 ~ [c2 c3] ~ g1 ~ [g1 g2] ~>")
    .s("sine")
    .lpf(slider(150, 60, 250))  // Deep sub
    .decay(slider(0.2, 0.1, 0.4))
    .delay(slider(0.15, 0, 0.4))
    .delaytime(0.375)  // Triplet dub delay
    .gain(slider(0.78, 0, 2))
    .rarely(x => x.note("<c2 [c2 d2] [c2 c3] g2 g1 [g1 a1] [g1 g2] c2>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Sub layer
$sub: note("<c1 ~ c1 ~ g0 ~ g0 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.5, 0, 1.3))
    .color("darkred")

// Ragga vocal stab with variations
$vox: s("vocal:0")
    .struct("~ ~ ~ ~ x ~ ~ ~")
    .chop(8)
    .slice(4, "<0 1 2 3>")
    .speed(slider(0.6, 0.4, 1.5))
    .room(slider(0.35, 0, 0.8))
    .delay(0.2)
    .gain(slider(0.52, 0, 2))
    .sometimes(x => x.struct("~ ~ x ~ x ~ ~ ~"))  // Double vocal
    .rarely(x => x.fast(2))  // Rapid chops
    .color("orange")

// Dub stab with skanking delay
$stab: note("[c3,d#3,g3]")
    .s("square")
    .lpf(sine.range(1200, 3000).slow(slider(4.0, 1, 16)))
    .struct("~ ~ x ~ ~ ~ ~ ~")
    .decay(slider(0.12, 0.04, 0.25))
    .delay(slider(0.35, 0, 0.7))
    .delaytime(0.375)  // Reggae triplet delay
    .room(slider(0.4, 0, 0.9))
    .gain(slider(0.48, 0, 2))
    .sometimes(x => x.struct("~ x ~ ~ ~ ~ x ~"))  // Skank pattern
    .rarely(x => x.note("[d3,f3,a3]"))  // Chord variation
    .color("cyan")
    ._punchcard()

// Atmospheric dub pad
$pad: note("[c3,g3,c4]")
    .s("sawtooth")
    .lpf(sine.range(400, 1200).slow(16))
    .attack(0.8)
    .release(1)
    .room(0.6)
    .gain(slider(0.22, 0, 0.7))
    .slow(8)
    .color("purple")
    .scope({ size: 256 })
