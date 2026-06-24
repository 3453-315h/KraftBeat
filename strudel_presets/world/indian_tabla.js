// @name Indian Tabla
// @genre World
// @bpm 85
// @tags tabla, hindustani, raga, classical, teental

setcpm(85 / 4)

// ═══════════════════════════════════════════════════════════════
// INDIAN TABLA - Teental theka with Raga Yaman Kalyan
// ═══════════════════════════════════════════════════════════════

// Tabla - Teental theka (16 matra cycle) with dynamics
// Dha Dhin Dhin Dha | Dha Dhin Dhin Dha | Dha Tin Tin Ta | Ta Dhin Dhin Dha
$tabla_r: s("[bd rim rim bd] [bd rim rim bd] [bd sd sd sd] [sd rim rim bd]").bank("RolandTR808")
    .gain("<0.65 0.72 0.68 0.75> <0.7 0.72 0.68 0.78>")  // Dynamics following theka
    .room(slider(0.12, 0, 0.4))
    .nudge(perlin.range(-0.01, 0.015))  // Humanized timing
    .sometimes(x => x.s("[bd rim rim bd] [bd rim rim bd] [bd sd rim sd] [sd rim bd bd]"))  // Variation
    .every(8, x => x.s("[bd rim rim bd] [bd rim rim bd] [bd sd sd sd] [sd rim [rim rim rim rim] bd]"))  // Tihai approach
    .color("orange")
    ._punchcard()

// Bayan (bass tabla) - Ge and Ghe strokes with weight
$bayan: s("[bd ~ ~ ~] [bd ~ ~ ~] [bd ~ ~ ~] [~ ~ ~ bd]").bank("RolandTR808")
    .gain(perlin.range(0.75, 0.92))  // Dynamics
    .lpf(slider(300, 100, 450))  // Deep bass
    .decay(slider(0.35, 0.15, 0.6))
    .nudge(perlin.range(-0.01, 0.01))
    .sometimes(x => x.s("[bd ~ ~ bd] [bd ~ ~ ~] [bd ~ bd ~] [~ ~ ~ bd]"))  // Variation
    .color("red")
    ._punchcard()

// Tanpura Sa-Pa-Sa drone - the meditative foundation
$tanpura: note("<c2 ~ ~ ~ g2 ~ ~ ~ c3 ~ ~ ~ g2 ~ ~ ~>")
    .s("triangle")
    .lpf(slider(600, 250, 1100))
    .attack(slider(1.2, 0.6, 2.2))
    .release(slider(1.5, 0.7, 2.8))
    .room(0.5)
    .gain(slider(0.42, 0, 1.5))
    .slow(4)
    .color("purple")
    .scope({ size: 256 })

// Tanpura second layer for richness
$tanpura2: note("<~ g2 ~ ~ ~ c3 ~ ~ ~ g2 ~ ~ ~ ~ ~ ~>")
    .s("sine")
    .lpf(500)
    .attack(1.5)
    .release(1.8)
    .room(0.4)
    .gain(slider(0.25, 0, 0.9))
    .slow(4)
    .color("magenta")

// Harmonium sustained chords with breathing
$harmonium: note("<[c3,e3,g3] ~ ~ ~ [c3,e3,g3] ~ ~ ~ [d3,f3,a3] ~ ~ ~ [g2,b2,d3] ~ ~ ~>")
    .s("triangle")  // Organ-like
    .lpf(slider(1800, 700, 3200))
    .attack(slider(0.25, 0.08, 0.5))
    .release(slider(0.4, 0.15, 0.75))
    .gain(slider(0.4, 0, 1.5))
    .slow(2)
    .sometimes(x => x.note("<[d3,f3,a3] ~ [e3,g3,b3] ~>"))  // Chord variation
    .color("cyan")
    .pianoroll({ fold: 1 })

// Sitar - Raga Yaman Kalyan (Ma# - teevra Ma) aroha
// Aroha: Sa Re Ga Ma# Pa Dha Ni Sa
$sitar: note("<c4 ~ d4 ~ e4 ~ f#4 ~ g4 ~ a4 ~ b4 ~ c5 ~>")
    .s("triangle")  // Pluck-like
    .lpf(slider(4500, 2000, 6500))
    .decay(slider(0.45, 0.2, 0.8))
    .room(slider(0.22, 0, 0.55))
    .delay(0.15)
    .delaytime(0.25)
    .gain(slider(0.52, 0, 2))
    .slow(2)
    .sometimes(x => x.note("<c5 b4 a4 g4 f#4 e4 d4 c4>"))  // Avaroha (descending)
    .color("yellow")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Sitar taans (fast runs) with euclidean pattern
$taan: note("<g4 a4 b4 c5 b4 a4 g4 f#4 e4 d4 c4 ~ ~ ~ ~ ~>")
    .s("triangle")
    .lpf(slider(5500, 2500, 8000))
    .decay(slider(0.12, 0.04, 0.25))
    .struct("x(9,16)")  // Euclidean pattern for taan feel
    .gain(slider(0.42, 0, 1.5))
    .slow(4)
    .sometimes(x => x.struct("x(7,16)"))  // Variation
    .rarely(x => x.fast(1.5))  // Faster taan
    .color("lime")
    ._punchcard()

// Gamak (ornament) layer
$gamak: note("<~ ~ e4 ~ ~ ~ d4 ~ ~ ~ ~ ~ ~ ~ ~ ~>")
    .s("sine")
    .lpf(4000)
    .decay(0.08)
    .delay(0.1)
    .room(0.2)
    .gain(slider(0.25, 0, 0.9))
    .slow(4)
    .color("white")

// Ghungroo bells - subtle dancer accompaniment
$ghungroo: s("shaker*16")
    .gain(perlin.range(0.18, 0.28))  // Subtle variation
    .pan(sine.range(-0.3, 0.3).slow(8))
    .euclid(7, 16)  // Subtle rhythmic accent
    .color("yellow")
    ._punchcard()
