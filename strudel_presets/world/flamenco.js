// @name Flamenco
// @genre World
// @bpm 115
// @tags flamenco, spanish, bulerias, phrygian, compás

setcpm(115 / 4)

// ═══════════════════════════════════════════════════════════════
// FLAMENCO - Bulerías compás in E Phrygian
// ═══════════════════════════════════════════════════════════════

// Palmas fuertes (strong claps) - bulerias accent pattern with dynamics
$palmas: s("[cp ~ ~] [cp ~ ~] [cp cp] [~ cp] [cp ~]")
    .bank("RolandTR808")
    .gain("<0.6 0.68 0.72 0.65 0.75>")  // Compás dynamics
    .room(slider(0.18, 0.05, 0.45))
    .nudge(perlin.range(-0.01, 0.015))  // Humanized
    .sometimes(x => x.s("[cp cp ~] [cp ~ ~] [cp cp] [cp ~] [cp ~]"))  // Variation
    .every(8, x => x.s("[cp ~ cp] [cp ~ cp] [cp cp cp] [~ cp cp] [cp cp]"))  // Remate
    .color("orange")
    ._punchcard()

// Cajón - tono (bass) and slap pattern with dynamics
$cajon: s("[bd ~ ~] [~ sd ~] [bd sd] [~ sd] [bd ~]")
    .bank("RolandTR808")
    .gain("<0.9 0.98 1.02 0.95 1.0>")  // Accent-following dynamics
    .shape(slider(0.15, 0, 0.4))
    .room(slider(0.12, 0, 0.4))
    .sometimes(x => x.s("[bd bd ~] [~ sd sd] [bd sd] [sd ~] [bd bd]"))  // Variation
    .every(8, x => x.s("[bd ~ bd] [sd sd ~] [bd sd sd] [sd sd] [bd bd]"))  // Remate fill
    .color("orange")
    ._punchcard()

// Palillos (heel taps) - zapateado footwork with variations
$taconeo: s("~ rim rim ~ rim rim ~ rim ~ rim rim ~")
    .bank("RolandTR808")
    .gain(perlin.range(0.38, 0.52))  // Velocity variation
    .sometimes(x => x.s("rim ~ rim rim ~ rim rim ~ ~ rim ~ rim"))  // Syncopation
    .every(8, x => x.s("[rim rim rim] rim rim ~ [rim rim] rim ~ [rim rim rim] ~"))  // Zapateado intensity
    .color("white")
    ._punchcard()

// Guitar rasgueado - E Phrygian chord progression with variations
$rasgueado: note("<[e4,g#4,b4] ~ [e4,g#4,b4] ~ [f4,a4,c5] ~ [e4,g#4,b4] ~ [d4,f#4,a4] ~ [e4,g#4,b4] ~>")
    .s("triangle")  // Guitar-like
    .lpf(slider(4500, 1800, 7500))
    .decay(slider(0.28, 0.12, 0.55))
    .room(slider(0.18, 0, 0.5))
    .gain(slider(0.58, 0, 2))
    .sometimes(x => x.note("<[f4,a4,c5] ~ [e4,g#4,b4] ~>"))  // Am-E resolution
    .rarely(x => x.fast(2).gain(0.5))  // Fast rasgueado
    .color("lime")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Guitar alzapúa - thumb technique bass notes with dynamics
$alzapua: note("<e3 ~ e3 e3 ~ f3 ~ e3 ~ d3 ~ e3 ~ ~ ~ ~>")
    .s("triangle")
    .lpf(slider(2500, 900, 4200))
    .decay(slider(0.22, 0.1, 0.42))
    .gain(perlin.range(0.48, 0.62))  // Velocity variation
    .sometimes(x => x.note("<e3 e3 ~ e3 f3 f3 e3 ~ d3 d3 e3 e3>"))  // More active
    .color("yellow")
    ._punchcard()

// Picado - fast melodic runs in E Phrygian with euclidean
$picado: note("<e5 f5 g5 a5 b5 c6 b5 a5 g5 f5 e5 d5 e5 ~ ~ ~>")
    .s("triangle")
    .lpf(slider(5500, 2500, 8500))
    .decay(slider(0.12, 0.05, 0.25))
    .struct("x(9,16)")  // Euclidean pattern
    .gain(slider(0.5, 0, 2))
    .slow(2)
    .sometimes(x => x.note("<e5 d5 c5 b4 a4 g4 f4 e4>"))  // Descending run
    .rarely(x => x.fast(1.5))  // Faster picado
    .color("cyan")
    ._punchcard()

// Bajo - walking Phrygian bass with movement
$bajo: note("<e2 ~ f2 ~ g2 ~ a2 ~ g2 ~ f2 ~ e2 ~ ~ ~>")
    .s("sawtooth")
    .lpf(slider(450, 150, 750))
    .decay(slider(0.22, 0.1, 0.42))
    .gain(slider(0.75, 0, 2))
    .rarely(x => x.note("<e2 f2 g2 a2 g2 f2 e2 d2>"))  // Walking variation
    .scope({ size: 256 })
    .color("red")

// Sub layer
$sub: note("<e1 ~ ~ ~ ~ ~ ~ ~ e1 ~ ~ ~ ~ ~ ~ ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.45, 0, 1.2))
    .color("darkred")

// Cante-style melody - emotional Phrygian with vibrato feel
$cante: note("<e5 ~ ~ f5 ~ e5 d5 ~ e5 ~ ~ ~ b4 c5 d5 e5>")
    .s("sawtooth")
    .lpf(slider(3800, 1500, 6500))
    .attack(slider(0.08, 0.03, 0.2))
    .decay(slider(0.55, 0.25, 0.95))
    .room(slider(0.32, 0, 0.7))
    .gain(slider(0.45, 0, 2))
    .slow(2)
    .sometimes(x => x.note("<f5 e5 d5 e5 b4 c5 d5 e5>"))  // Variation
    .color("purple")
    .pianoroll({ fold: 1 })
    .scope({ size: 256 })
