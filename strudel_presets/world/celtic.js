// @name Celtic Jig
// @genre World
// @bpm 115
// @tags celtic, irish, fiddle, bodhran, mixolydian

setcpm(115 / 4)

// ═══════════════════════════════════════════════════════════════
// CELTIC JIG - Irish jig in D Mixolydian with 6/8 feel
// ═══════════════════════════════════════════════════════════════

// Bodhran (Irish frame drum) - jig rhythm (6/8 feel) with dynamics
$bodhran: s("[bd rim rim] [bd rim rim] [bd rim rim] [bd rim rim]").bank("RolandTR808")
    .gain("<0.85 0.9 0.82 0.88> <0.88 0.82 0.9 0.85>")  // 6/8 accent
    .room(slider(0.15, 0, 0.45))
    .nudge(perlin.range(-0.01, 0.015))  // Humanized
    .sometimes(x => x.s("[bd rim rim] [rim bd rim] [bd rim rim] [rim rim bd]"))  // Variation
    .every(8, x => x.s("[bd rim rim] [bd bd rim] [bd rim bd] [rim rim rim rim rim rim]"))  // Fill
    .color("orange")
    ._punchcard()

// Bones (rhythm sticks) with variations
$bones: s("[rim ~ rim] [~ rim ~] [rim ~ rim] [~ rim rim]").bank("RolandTR808")
    .gain(perlin.range(0.38, 0.52))  // Velocity
    .pan(slider(0.4, 0.2, 0.6))
    .sometimes(x => x.s("[~ rim rim] [rim ~ rim] [rim rim ~] [~ rim ~]"))
    .color("yellow")
    ._punchcard()

// Fiddle - Irish jig melody (D Mixolydian) with ornamentation
$fiddle: note("<d5 e5 f#5 g5 a5 b5 a5 g5 f#5 e5 d5 c5 d5 ~ ~ ~>")
    .s("sawtooth")
    .lpf(slider(5000, 2500, 9000))
    .attack(slider(0.02, 0.01, 0.08))
    .decay(slider(0.25, 0.12, 0.45))
    .struct("x(11,16)")  // Jig feel
    .room(slider(0.2, 0, 0.6))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.note("<a5 b5 d6 b5 a5 g5 f#5 e5 d5>"))  // Upper variation
    .rarely(x => x.fast(1.5))  // Triplet ornament
    .color("lime")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Tin whistle - counter melody with breath
$whistle: note("<a5 ~ b5 ~ d6 ~ b5 ~ a5 ~ g5 ~ f#5 ~ e5 ~>")
    .s("triangle")
    .lpf(slider(8000, 3500, 11000))
    .attack(slider(0.03, 0.01, 0.1))
    .decay(slider(0.3, 0.15, 0.55))
    .delay(0.1)
    .slow(slider(2, 1, 4))
    .gain(slider(0.48, 0, 2))
    .sometimes(x => x.note("<d6 b5 a5 g5 f#5 e5 d5>"))  // Descending
    .color("cyan")
    ._punchcard()

// Uilleann pipes - drone with slow movement
$drone: note("<d2 a2 d3 a2>")
    .s("sawtooth")
    .lpf(slider(800, 250, 1800))
    .attack(0.3)
    .release(0.5)
    .slow(slider(8, 4, 16))
    .gain(slider(0.42, 0, 1.5))
    .color("purple")
    .scope({ size: 256 })

// Second drone layer
$drone2: note("d1")
    .s("sine")
    .lpf(100)
    .attack(0.5)
    .gain(slider(0.35, 0, 1.1))
    .slow(16)
    .color("darkred")

// Acoustic guitar strumming - jig pattern
$guitar: note("<[d4,f#4,a4] [d4,f#4,a4] [g4,b4,d5] [d4,f#4,a4]>")
    .s("triangle")  // Acoustic-like
    .lpf(slider(4000, 1500, 7000))
    .struct("[x x x] [x x x] [x x x] [x x x]")  // 6/8 strum
    .decay(slider(0.15, 0.06, 0.32))
    .room(slider(0.15, 0, 0.5))
    .gain(slider(0.52, 0, 2))
    .sometimes(x => x.note("<[g4,b4,d5] [a4,c5,e5] [d4,f#4,a4] [d4,f#4,a4]>"))  // Chord variation
    .color("yellow")
    ._punchcard()

// Bass - root movement with walking
$bass: note("<d2 ~ ~ d2 ~ a2 g2 ~ ~ g2 ~ a2 d2 ~ ~ ~>")
    .s("sawtooth")
    .lpf(slider(500, 180, 900))
    .decay(slider(0.2, 0.08, 0.38))
    .gain(slider(0.72, 0, 2))
    .rarely(x => x.note("<d2 e2 f#2 d2 g2 a2 g2 f#2 e2 g2 f#2 a2 d2 e2 d2 ~>"))  // Walking
    .color("red")
    .scope({ size: 256 })
