// @name Global Rhythms
// @genre World
// @bpm 105
// @tags percussion, polyrhythm, world, drums, ensemble

setcpm(105 / 4)

// ═══════════════════════════════════════════════════════════════
// GLOBAL RHYTHMS - Complex polyrhythmic percussion ensemble
// ═══════════════════════════════════════════════════════════════

// West African djembe base
$djembe: s("[bd ~ rim rim] [~ bd ~ rim] [bd ~ rim ~] [~ rim bd rim]").bank("RolandTR808")
    .gain("<0.92 0.88 0.95 0.9>")
    .room(slider(0.2, 0, 0.6))
    .nudge(perlin.range(-0.015, 0.02))  // Humanized
    .sometimes(x => x.s("[bd bd rim ~] [~ bd rim rim] [bd ~ ~ rim] [~ rim bd ~]"))
    .color("orange")
    ._punchcard()

// Brazilian surdo - heartbeat
$surdo: s("[bd ~ ~ ~] [~ ~ bd ~] [~ ~ ~ ~] [bd ~ ~ ~]").bank("RolandTR808")
    .gain(slider(0.9, 0, 2))
    .decay(slider(0.5, 0.25, 0.9))
    .lpq(2)  // Resonance
    .color("red")
    ._punchcard()

// Cuban timbales cascade
$timbal: s("[rim rim rim rim] [rim rim rim rim] [rim rim rim rim] [rim rim ~ rim]")
    .bank("RolandTR808")
    .gain(perlin.range(0.35, 0.55))
    .pan(slider(0.45, -0.6, 0.6))
    .every(4, x => x.s("[rim rim ~ rim] [rim ~ rim rim] [rim rim rim ~] [~ rim rim rim]"))
    ._punchcard()

// Indian tabla pattern
$tabla: s("[tabla:0 tabla:1 tabla:1 tabla:0] [tabla:0 tabla:1 tabla:1 tabla:0]")
    .gain(slider(0.52, 0, 1.8))
    .room(slider(0.15, 0, 0.5))
    .slow(slider(2, 1, 4))
    .sometimes(x => x.s("[tabla:0 ~ tabla:2] [tabla:1 tabla:0 tabla:2]"))
    ._punchcard()

// Middle Eastern darbuka - intricate
$darbuka: s("[bd ~ ~ rim] [~ rim bd ~] [bd ~ rim ~] [~ rim ~ rim]").bank("RolandTR808")
    .gain(slider(0.55, 0, 1.8))
    .pan(slider(-0.45, -0.6, -0.2))
    .nudge(0.01)
    ._punchcard()

// Japanese taiko accent - heavy hits
$taiko: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ bd ~ ~ ~").bank("RolandTR808")
    .gain(slider(0.85, 0, 2))
    .decay(slider(0.7, 0.4, 1.2))
    .room(slider(0.5, 0, 1))
    .slow(slider(2, 1, 4))
    .color("yellow")
    ._punchcard()

// Shaker layer - glue
$shaker: s("shaker*8")
    .gain(perlin.range(0.25, 0.4))
    .pan(sine.range(-0.4, 0.4).slow(4))
    .sometimes(x => x.gain(0.45))
    ._punchcard()

// Agogo bells - timeline pattern (3-2 clave feel)
$bell: s("[ag:0 ~ ag:1 ~] [~ ag:0 ~ ag:1] [ag:0 ~ ~ ag:1] [~ ~ ag:0 ~]")
    .gain(slider(0.48, 0, 1.5))
    .color("yellow")
    ._punchcard()

// Bass pulsing with root
$bass: note("<c2 ~ g2 ~ f2 ~ g2 ~ c2 ~ eb2 ~ f2 ~ g2 ~>")
    .s("sine")
    .lpf(slider(450, 200, 900))
    .decay(slider(0.25, 0.1, 0.6))
    .gain(slider(0.78, 0, 2))
    .scope({ size: 256 })
    .color("red")
