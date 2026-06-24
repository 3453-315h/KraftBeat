// @name Tech House
// @genre House
// @bpm 126
// @tags techy, groovy, rolling, percussion

setcpm(126 / 4)

// ═══════════════════════════════════════════════════════════════
// TECH HOUSE - Groovy, rolling, percussive power
// ═══════════════════════════════════════════════════════════════

// Punchy 909 kick with dynamics
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.05 1 1.02 1> <1 1 1.05 [1.08 1]>")  // Dynamics
    .shape(slider(0.3, 0, 1))
    .every(8, x => x.s("bd bd bd bd [bd bd] bd bd"))  // 8-bar phrase
    .every(16, x => x.s("bd bd [~ bd] bd bd bd [bd bd bd bd] bd"))  // Variation
    .color("orange")
    ._punchcard()

// Rolling 16th hats with velocity
$hat: s("hh*16").bank("RolandTR909")
    .gain(perlin.range(0.32, 0.48))  // Humanized
    .pan(perlin.range(-0.12, 0.12).slow(0.25))  // Subtle stereo
    .sometimes(x => x.s("[hh*4] [hh hh oh hh] [hh*4] [hh hh hh oh]"))  // Open hat accents
    .every(8, x => x.s("[hh*4] [hh*4] [hh*8] [hh oh hh*4]"))  // Fill
    ._punchcard()

// Tech clap with layered ghost
$clap: stack(
    s("~ cp ~ cp").gain(slider(0.88, 0, 2)).room(0.35),
    s("~ [cp:3 ~] ~ ~").gain(0.25).lpf(5000)  // Ghost
).bank("RolandTR909")
    .every(8, x => x.s("~ cp ~ [cp cp cp cp]"))  // Fill
    .color("yellow")
    ._punchcard()

// Driving shaker with movement
$shaker: s("shaker*16")
    .gain(perlin.range(0.2, 0.35))
    .pan(sine.range(-0.4, 0.4).slow(2))  // Wide stereo sweep
    .lpf(perlin.range(4000, 8000))
    .color("gray")

// Rolling percussion - rim pattern essential for tech house
$perc: s("~ rim [~ rim] ~").bank("RolandTR909")
    .gain(perlin.range(0.4, 0.55))  // Velocity variation
    .delay(slider(0.2, 0, 1))
    .room(0.2)
    .sometimes(x => x.s("rim ~ [~ rim] rim"))  // Pattern variation
    .every(4, x => x.s("[rim ~] rim [~ rim] [rim rim]"))  // Fill
    ._punchcard()

// Tom accent for fills
$tom: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ tom tom ~ ~").bank("RolandTR909")
    .gain(slider(0.45, 0, 1.5))
    .lpf(500)
    .room(0.2)
    .every(4, x => x.s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ tom ~ tom tom tom ~"))  // Extended fill
    .color("brown")

// Tech house bass with octave jumps
$bass: note("<c2 ~ [c2 c3] ~ c2 ~ [d#2 ~] ~>")
    .s("sawtooth")
    .lpf(sine.range(300, 800).slow(slider(4.0, 1, 16)))
    .decay(slider(0.12, 0.04, 0.25))
    .gain(slider(0.82, 0, 2))
    .rarely(x => x.note("<c2 c3 [c2 d#2] g2>"))  // Variation
    .scope({ size: 256 })
    .color("red")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Sub layer
$sub: note("<c1 ~ c1 ~ c1 ~ d#1 ~>")
    .s("sine")
    .lpf(80)
    .gain(slider(0.45, 0, 1.2))
    .color("darkred")

// Vocal chop simulation with variations
$vox: s("alphabet:3")
    .struct("~ ~ x ~")
    .chop(16)
    .speed(choose(1, 1.5, 2))
    .slice(4, "<0 1 2 3>")
    .delay(slider(0.2, 0, 1))
    .room(0.25)
    .gain(slider(0.55, 0, 2))
    .sometimes(x => x.struct("~ x ~ x"))  // Double chop
    .rarely(x => x.fast(2))  // Fast chop fill
    .color("orange")

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh")
    .bank("RolandTR909")
    .gain(0.4)
    .room(0.35)
    .slow(2)
