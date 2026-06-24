// @name Vinyl Dreams  
// @genre Lofi
// @bpm 78
// @tags lofi, vinyl, dusty, tape, jazz

setcpm(78 / 4)

// ═══════════════════════════════════════════════════════════════
// VINYL DREAMS - Dusty lofi with tape warmth
// ═══════════════════════════════════════════════════════════════

// Soft dusty kick with swing
$kick: s("bd ~ [~ bd] ~").bank("SP1200")
    .gain("<0.78 0.72 0.75 0.7>")  // Soft dynamics
    .lpf(260)  // Warm lo-fi
    .nudge("<0 0 0.025 0>")  // Swing
    .every(8, x => x.s("bd ~ [bd ~] ~ [~ bd] ~ bd ~"))
    .color("orange")
    ._punchcard()

// Soft snare with room
$snare: stack(
    s("~ sd ~ sd").gain(slider(0.65, 0, 2)).room(0.45).lpf(3800),
    s("~ ~ [sd:3 ~] [~ sd:3]").gain(0.15).lpf(3000)  // Soft ghosts
).bank("SP1200")
    .nudge("0 0.015 0 0.02")  // Swing
    .every(8, x => x.s("~ sd ~ [sd sd sd sd]"))
    .color("white")
    ._punchcard()

// Lazy hats with lo-fi filter
$hat: s("[~ hh] ~ [~ hh] [hh ~]").bank("SP1200")
    .gain(perlin.range(0.22, 0.35))  // Very soft
    .lpf(perlin.range(2800, 5500))
    .nudge(perlin.range(-0.02, 0.04))  // Swing
    .pan(perlin.range(-0.12, 0.12).slow(0.5))
    .sometimes(x => x.s("[hh ~] ~ [~ hh] [~ hh]"))
    .color("white")
    ._punchcard()

// Vinyl crackle - essential
$vinyl: s("[rim:5 rim:5 rim:5 rim:5]*4")
    .gain(perlin.range(0.12, 0.22))  // Variable crackle
    .lpf(2500)
    .hpf(400)
    .color("brown")

// Jazz piano chops with sidechain duck
$piano: n("<[0,4,7] ~ [2,5,9] ~> <[5,9,0] ~ [7,11,2] [4,7,11]>")
    .scale("c:major7")
    .s("triangle")  // Piano-like
    .lpf(sine.range(1500, 3500).slow(8))
    .decay(slider(0.2, 0.1, 0.4))
    .room(slider(0.38, 0, 0.9))
    .gain(slider(0.55, 0, 2))
    .duck("4:8")
    .duckdepth(0.3)
    .sometimes(x => x.n("<[0,3,7] ~ [2,6,9] ~>"))  // Chord variation
    .color("brown")
    ._punchcard()
    .pianoroll({ fold: 1 })

// Electric piano layer for warmth
$rhodes: note("<[g3,b3] ~ [a3,c4] ~ [b3,d4] ~ [g3,b3] ~>")
    .s("sine")
    .lpf(1800)
    .decay(0.15)
    .delay(0.1)
    .room(0.3)
    .gain(slider(0.22, 0, 0.8))
    .color("yellow")

// Mellow bass
$bass: note("<c2 ~ [c2 ~] ~ d2 ~ [e2 d2] ~>")
    .s("triangle")
    .lpf(sine.range(220, 450).slow(slider(8, 4, 16)))
    .decay(slider(0.18, 0.08, 0.32))
    .gain(slider(0.68, 0, 2))
    .rarely(x => x.note("<c2 d2 [e2 d2] c2>"))
    .scope({ size: 256 })
    .color("red")
    ._punchcard()

// Sub layer
$sub: note("<c1 ~ c1 ~ d1 ~ e1 ~>")
    .s("sine")
    .lpf(75)
    .gain(slider(0.38, 0, 1.1))
    .color("darkred")

// Ambient pad for dreaminess
$pad: note("[c3,e3,g3]")
    .s("sawtooth")
    .lpf(sine.range(320, 850).slow(32))
    .attack(1.2)
    .release(1)
    .room(0.55)
    .gain(slider(0.15, 0, 0.5))
    .slow(8)
    .color("purple")
    .scope({ size: 256 })

// Tape wobble melody
$wobble: note("<c5 ~ e5 ~ g5 ~ e5 ~>")
    .s("sine")
    .lpf(2200)
    .decay(0.15)
    .delay(0.2)
    .delaytime(0.375)
    .room(0.35)
    .gain(slider(0.22, 0, 0.8))
    .speed(sine.range(0.98, 1.02).slow(8))  // Tape wobble
    .slow(4)
    .color("lime")
