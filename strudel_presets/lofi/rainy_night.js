// @name Rainy Night
// @genre Lo-Fi
// @bpm 70
// @tags rain, night, melancholy, a minor

setcpm(70 / 4)

// ═══════════════════════════════════════════════════════════════
// RAINY NIGHT - Melancholic lo-fi with A minor mood
// ═══════════════════════════════════════════════════════════════

// Soft dusty kick
$kick: s("bd ~ bd ~").bank("SP1200")
    .gain("<0.72 0.68 0.7 0.65>")  // Very soft
    .lpf(240)  // Warm lo-fi
    .nudge("<0 0 0.02 0>")  // Swing
    .every(8, x => x.s("bd ~ [bd ~] ~ [~ bd] ~ bd ~"))
    .color("orange")
    ._punchcard()

// Soft snare with big room
$snare: stack(
    s("~ sd ~ sd").gain(slider(0.62, 0, 2)).room(0.52).lpf(3600),
    s("~ ~ [sd:3 ~] ~").gain(0.15).lpf(2800)  // Ghost
).bank("SP1200")
    .nudge("0 0.012 0 0.018")  // Swing
    .every(8, x => x.s("~ sd ~ [sd sd sd sd]"))
    .color("white")
    ._punchcard()

// Sparse offbeat hats
$hat: s("[~ hh] hh [~ hh] hh").bank("SP1200")
    .gain(perlin.range(0.22, 0.35))  // Soft humanized
    .lpf(perlin.range(3000, 6000))
    .nudge(perlin.range(-0.015, 0.03))
    .pan(perlin.range(-0.12, 0.12).slow(0.5))
    .sometimes(x => x.s("[hh ~] hh [~ hh] [~ hh]"))
    .color("white")
    ._punchcard()

// Rain texture - essential element
$rain: s("[rim:5 rim:5 rim:5 rim:5]*8")
    .gain(perlin.range(0.08, 0.2))  // Variable rain intensity
    .lpf(perlin.range(1500, 4500))
    .hpf(700)
    .pan(perlin.range(-0.5, 0.5))  // Wide stereo
    .room(0.4)
    .color("gray")

// Vinyl crackle
$vinyl: s("[rim:5 rim:5]*4")
    .gain(slider(0.12, 0, 0.35))
    .lpf(2500)
    .hpf(400)
    .color("brown")

// Melancholic A minor piano chords
$piano: note("<[a3,c4,e4] [a3,c4,e4] [f3,a3,c4] [g3,b3,d4]>")
    .s("triangle")  // Piano-like
    .lpf(sine.range(1600, 3800).slow(slider(8, 4, 16)))
    .decay(0.22)
    .room(slider(0.42, 0, 0.95))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.52, 0, 2))
    .sometimes(x => x.note("<[e4,g4,b4] [d4,f4,a4]>"))  // Chord variation
    .color("cyan")
    .pianoroll({ fold: 1 })
    ._punchcard()

// Piano accent notes
$accent: note("<~ ~ e4 ~ ~ ~ c4 ~>")
    .s("sine")
    .lpf(2500)
    .decay(0.15)
    .delay(0.2)
    .room(0.4)
    .gain(slider(0.2, 0, 0.7))
    .slow(slider(4.0, 1, 16))
    .color("yellow")

// Soft bass in A minor
$bass: note("<a1 ~ f1 ~ g1 ~ f1 ~>")
    .s("triangle")
    .lpf(sine.range(220, 420).slow(slider(8, 4, 16)))
    .decay(slider(0.18, 0.08, 0.35))
    .slow(slider(4.0, 1, 16))
    .gain(slider(0.65, 0, 2))
    .rarely(x => x.note("<a1 [a1 b1] f1 [g1 f1]>"))  // Walking
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: note("<a0 ~ f0 ~ g0 ~ f0 ~>")
    .s("sine")
    .lpf(70)
    .gain(slider(0.35, 0, 1))
    .color("darkred")

// Subtle melancholic pad
$pad: note("[a2,c3,e3]")
    .s("sawtooth")
    .lpf(sine.range(350, 950).slow(32))
    .attack(slider(0.8, 0.3, 1.5))
    .release(slider(0.9, 0.4, 1.8))
    .slow(slider(8, 4, 16))
    .room(slider(0.5, 0, 1))
    .gain(slider(0.22, 0, 0.75))
    .sometimes(x => x.note("[f2,a2,c3]"))  // Chord shift
    .color("purple")
    ._punchcard()
    .scope({ size: 256 })

// Distant melody
$melody: note("<~ ~ a4 ~ ~ ~ e4 ~ ~ ~ c4 ~ ~ ~ ~ ~>")
    .s("sine")
    .lpf(2800)
    .decay(0.4)
    .delay(0.3)
    .delaytime(0.5)
    .room(0.55)
    .gain(slider(0.18, 0, 0.6))
    .slow(4)
    .color("lime")
