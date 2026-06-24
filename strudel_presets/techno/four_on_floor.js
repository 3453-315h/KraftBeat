// @name Four on Floor
// @genre Techno
// @bpm 126
// @tags basic, minimal, foundation, classic

setcpm(126 / 4)

// ═══════════════════════════════════════════════════════════════
// FOUR ON FLOOR - Classic techno foundation with production polish
// ═══════════════════════════════════════════════════════════════

// Production four-on-floor kick with subtle dynamics
$kick: s("bd*4").bank("RolandTR909")
    .gain("<1.15 1.1 1.12 1.08> <1.1 1.1 1.15 1.1>")  // Velocity cycle
    .shape(slider(0.18, 0, 0.45))
    .every(8, x => x.s("bd*4 [bd bd bd bd]"))  // 8-bar snare roll lead-in
    .every(16, x => x.s("[bd ~] bd bd bd bd bd [bd bd] bd"))  // 16-bar variation
    .rarely(x => x.s("[bd bd:1] bd bd bd"))  // Ghost kick accent
    .color("orange")
    ._punchcard()

// Offbeat hats with velocity dynamics and fills
$hat: s("~ hh ~ hh ~ hh ~ oh").bank("RolandTR909")
    .gain(perlin.range(0.38, 0.52))  // Humanized velocity
    .pan(perlin.range(-0.1, 0.1).slow(0.25))  // Subtle stereo
    .sometimes(x => x.s("~ hh ~ hh ~ [hh hh] ~ oh"))  // Variation
    .every(8, x => x.s("[hh hh] [hh hh] [hh hh hh hh] [hh oh:2]"))  // Fill
    ._punchcard()

// Clap with ghost notes for groove depth
$clap: stack(
    s("~ cp ~ cp").gain(slider(0.88, 0, 2)).room(0.28),  // Main clap
    s("~ ~ [~ cp:3] ~").gain(0.22).lpf(4500)  // Ghost clap
).bank("RolandTR909")
    .every(8, x => x.s("~ cp ~ [cp cp:2 cp cp]"))  // 8-bar fill
    .color("white")
    ._punchcard()

// Ride accent with variations
$ride: s("~ ~ ~ ~ ~ ~ ~ rd").bank("RolandTR909")
    .gain(slider(0.35, 0, 1.5))
    .sometimes(x => x.s("~ ~ rd ~ ~ ~ ~ rd"))  // Double ride
    .every(16, x => x.s("rd*8").gain(0.25))  // Build section
    ._punchcard()

// Rim click for texture (Berlin minimal influence)
$rim: s("~ ~ ~ ~ [rim ~] ~ ~ ~").bank("RolandTR909")
    .gain(slider(0.35, 0, 1.2))
    .delay(0.12)
    .room(0.2)
    .color("gray")

// Simple bass with filter movement
$bass: note("<c2 c2 c2 c2 g1 g1 g1 g1>")
    .s("sawtooth")
    .lpf(sine.range(350, 650).slow(8))
    .decay(slider(0.12, 0.04, 0.28))
    .gain(slider(0.85, 0, 2))
    .scope({ size: 256 })
    .color("red")

// Basic stab with movement
$stab: note("<[c4,g4] ~ ~ ~ [g3,d4] ~ ~ ~>")
    .s("sawtooth")
    .lpf(sine.range(2000, 4000).slow(4))
    .decay(slider(0.15, 0.05, 0.35))
    .room(slider(0.22, 0, 0.55))
    .gain(slider(0.5, 0, 2))
    .every(4, x => x.fast(2).gain(0.35))  // Double-time hits
    .color("cyan")
    ._punchcard()

// Subtle pad atmosphere
$pad: note("<[c3,g3,c4] [c3,g3,c4] [g2,d3,g3] [g2,d3,g3]>")
    .s("triangle")
    .lpf(slider(1500, 500, 3000))
    .attack(slider(0.5, 0.2, 1))
    .release(slider(0.6, 0.25, 1.1))
    .room(slider(0.4, 0, 0.85))
    .gain(slider(0.28, 0, 1))
    .slow(4)
    .color("purple")
    .scope({ size: 256 })

// Crash for transitions
$crash: s("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ oh:4")
    .bank("RolandTR909")
    .gain(0.45)
    .room(0.5)
    .slow(2)
