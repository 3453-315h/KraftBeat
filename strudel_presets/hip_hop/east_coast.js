// @name East Coast
// @genre Hip Hop
// @bpm 88
// @tags east, gritty, new york, hardcore

setcpm(88 / 4)

// ═══════════════════════════════════════════════════════════════
// EAST COAST - NYC gritty boom bap with piano stabs
// ═══════════════════════════════════════════════════════════════

// Gritty kick with swing and off-grid feel
$kick: s("bd ~ [~ bd] bd").bank("SP1200")
    .gain("<1.05 1 0.98 1.02> <1 1.02 1.05 1>")  // Dynamics
    .nudge("<0 0 0.035 0.02>")  // Off-grid swing
    .shape(slider(0.8, 0, 1))
    .every(4, x => x.s("[bd ~] ~ [~ bd] bd"))  // Variation
    .every(8, x => x.s("bd ~ [bd bd] ~ bd [~ bd] ~ [bd bd]"))  // 8-bar fill
    .color("orange")
    ._punchcard()

// Swung hats with NYC grit
$hat: s("[hh ~] [~ hh] [hh ~] [hh hh]").bank("SP1200")
    .gain(perlin.range(0.35, 0.52))  // Humanized
    .nudge(perlin.range(-0.02, 0.04))  // Swing timing
    .pan(perlin.range(-0.12, 0.12).slow(0.5))
    .lpf(perlin.range(5000, 10000))  // Tonal grit
    .sometimes(x => x.s("[hh hh] [~ hh] [hh ~] [~ hh]"))  // Variation
    .every(8, x => x.s("[hh hh hh hh] [hh hh oh hh]"))  // Fill
    ._punchcard()

// East coast snare with layered ghost
$snare: stack(
    s("~ sd ~ sd").gain(slider(0.9, 0, 2)).room(0.35),
    s("~ ~ [sd:3 ~] [~ sd:3]").gain(0.28).lpf(4000)  // Ghost snares
).bank("SP1200")
    .nudge("0 0.015 0 0.02")  // Swing
    .every(8, x => x.s("~ sd ~ [sd sd sd sd]"))  // Fill
    .color("white")
    ._punchcard()

// Gritty bass with walking feel
$bass: note("<c2 ~ [c2 d2] ~ e2 ~ [d2 c2] ~>")
    .s("sawtooth")
    .lpf(sine.range(280, 550).slow(slider(4.0, 1, 16)))
    .decay(slider(0.18, 0.08, 0.35))
    .gain(slider(0.78, 0, 2))
    .rarely(x => x.note("<c2 d2 [e2 d2] c2 e2 d2 [c2 d2] e2>"))  // Walking variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Sub layer
$sub: note("<c1 ~ c1 ~ e1 ~ d1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.42, 0, 1.2))
    .color("darkred")

// NYC piano stab
$piano: note("[c4,e4,g4]")
    .s("triangle")  // Piano-like
    .struct("~ ~ x ~ ~ ~ [x ~] ~")
    .lpf(sine.range(2000, 4500).slow(8))
    .decay(0.2)
    .room(slider(0.35, 0, 1))
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.struct("~ x ~ ~ ~ ~ [x ~] x"))  // Variation
    .rarely(x => x.fast(2).gain(0.45))  // Double stab
    .color("cyan")
    ._punchcard()

// String hit on downbeat
$strings: note("[c3,g3,c4,e4]")
    .s("sawtooth")
    .lpf(sine.range(800, 2000).slow(slider(4.0, 1, 16)))
    .struct("x ~ ~ ~ ~ ~ ~ ~")
    .attack(slider(0.08, 0.02, 0.2))
    .release(slider(0.4, 0.15, 0.7))
    .slow(slider(4.0, 1, 16))
    .room(slider(0.35, 0, 1))
    .gain(slider(0.5, 0, 2))
    .sometimes(x => x.struct("x ~ ~ ~ x ~ ~ ~"))  // Double hit
    .color("purple")
    ._punchcard()
    .scope({ size: 256 })

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("SP1200")
    .gain(0.4)
    .room(0.35)
    .slow(2)
