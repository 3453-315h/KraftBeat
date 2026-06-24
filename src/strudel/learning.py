"""
Strudel Learning & Help System.

Provides code snippets, syntax reference, and tutorial content
for the embedded Strudel live coding environment.
"""

from typing import Dict, List

# Quick syntax reference for common Strudel patterns
SYNTAX_REFERENCE = {
    "basics": {
        "title": "Basic Patterns",
        "items": [
            {"syntax": 's("bd sd")', "description": "Simple drum pattern"},
            {"syntax": 's("bd*4")', "description": "Repeat 4 times per cycle"},
            {"syntax": 's("bd sd hh oh")', "description": "4 sounds evenly spaced"},
            {"syntax": 's("[bd sd] hh")', "description": "Group sounds in one step"},
            {"syntax": 's("bd <sd cp>")', "description": "Alternate each cycle"},
        ]
    },
    "notes": {
        "title": "Notes & Chords",
        "items": [
            {"syntax": 'note("c4 e4 g4")', "description": "Play notes"},
            {"syntax": 'note("[c4,e4,g4]")', "description": "Play chord"},
            {"syntax": 'n("0 2 4").scale("C:minor")', "description": "Scale degrees"},
            {"syntax": 'note("c4").add(12)', "description": "Transpose up octave"},
        ]
    },
    "effects": {
        "title": "Effects & Modulation",
        "items": [
            {"syntax": '.lpf(1000)', "description": "Low-pass filter at 1000Hz"},
            {"syntax": '.hpf(500)', "description": "High-pass filter at 500Hz"},
            {"syntax": '.room(0.5)', "description": "Reverb amount (0-1)"},
            {"syntax": '.delay(0.25)', "description": "Delay amount"},
            {"syntax": '.gain(0.8)', "description": "Volume (0-1)"},
            {"syntax": '.pan(sine)', "description": "Auto-pan with LFO"},
            {"syntax": '.distort(0.3)', "description": "Distortion amount"},
        ]
    },
    "rhythm": {
        "title": "Rhythm Patterns",
        "items": [
            {"syntax": '.euclid(3,8)', "description": "Euclidean rhythm (3 hits in 8 steps)"},
            {"syntax": '.struct("x ~ x ~ x ~ ~ x")', "description": "Custom rhythm"},
            {"syntax": '.fast(2)', "description": "Double speed"},
            {"syntax": '.slow(2)', "description": "Half speed"},
            {"syntax": '.off(0.125, x => x.add(7))', "description": "Delay + transform"},
        ]
    },
    "modulation": {
        "title": "LFO & Modulation",
        "items": [
            {"syntax": 'sine.range(100, 1000)', "description": "Sine wave 100-1000"},
            {"syntax": 'saw.slow(4)', "description": "Slow sawtooth wave"},
            {"syntax": 'rand', "description": "Random value each step"},
            {"syntax": 'choose(1, 2, 3)', "description": "Random choice"},
            {"syntax": 'irand(10)', "description": "Random integer 0-9"},
        ]
    },
}


# Code snippets for quick insertion
CODE_SNIPPETS = {
    "drum_basic": {
        "name": "Basic Drums",
        "category": "Drums",
        "code": '''// Basic drum pattern
$kick: s("bd*4").bank("RolandTR909")
$snare: s("~ sd ~ sd").bank("RolandTR909")
$hat: s("hh*8").bank("RolandTR909").gain(0.4)''',
    },
    "drum_euclidean": {
        "name": "Euclidean Drums",
        "category": "Drums",
        "code": '''// Euclidean rhythms
$kick: s("bd").euclid(3,8).bank("RolandTR808")
$snare: s("sd").euclid(5,8).bank("RolandTR808")
$hat: s("hh").euclid(7,8).bank("RolandTR808").gain(0.4)''',
    },
    "bass_simple": {
        "name": "Simple Bass",
        "category": "Bass",
        "code": '''// Simple bassline
$bass: note("<c2 c2 f2 g2>")
  .s("sawtooth")
  .lpf(800)
  .decay(0.15)
  .gain(0.6)''',
    },
    "bass_filter": {
        "name": "Filter Bass",
        "category": "Bass",
        "code": '''// Filter sweep bass
$bass: note("c1*4")
  .s("sawtooth")
  .lpf(sine.range(200, 2000).slow(4))
  .resonance(10)
  .decay(0.1)
  .gain(0.7)''',
    },
    "chord_pads": {
        "name": "Chord Pads",
        "category": "Chords",
        "code": '''// Evolving pad
$pad: note("<[c4,e4,g4,b4] [a3,c4,e4,g4] [f3,a3,c4,e4] [g3,b3,d4,f4]>")
  .s("sawtooth")
  .lpf(2000)
  .attack(0.5)
  .release(1)
  .room(0.5)
  .slow(2)
  .gain(0.4)''',
    },
    "arp_basic": {
        "name": "Basic Arpeggio",
        "category": "Melody",
        "code": '''// Arpeggio pattern
$arp: note("<c4 e4 g4 c5 g4 e4 c4 d4>")
  .s("triangle")
  .lpf(3000)
  .delay(0.2)
  .room(0.3)
  .gain(0.45)''',
    },
    "arp_random": {
        "name": "Random Arpeggio",
        "category": "Melody",
        "code": '''// Generative arpeggio
$arp: n(choose(0, 2, 4, 5, 7, 9, 11, 12))
  .scale("C:minor")
  .s("triangle")
  .struct("x(5,8)")
  .lpf(2000)
  .delay(0.25)
  .room(0.4)
  .gain(0.4)''',
    },
    "perc_layers": {
        "name": "Layered Percussion",
        "category": "Percussion",
        "code": '''// Percussion layers
$shaker: s("shaker*8").gain(0.25)
$rim: s("~ rim ~ [rim rim]").bank("RolandTR909").gain(0.4)
$conga: s("~ conga:0 [conga:1 ~] conga:2").gain(0.35)''',
    },
    "atmosphere": {
        "name": "Atmosphere",
        "category": "Ambient",
        "code": '''// Atmospheric texture
$drone: note("c2")
  .s("sawtooth")
  .lpf(sine.range(200, 600).slow(16))
  .attack(2)
  .release(4)
  .slow(8)
  .room(0.8)
  .gain(0.25)''',
    },
    "vocal_chop": {
        "name": "Vocal Chop",
        "category": "Samples",
        "code": '''// Vocal chop effect
$vox: s("alphabet:*")
  .n(choose(0, 4, 8, 14))
  .chop(4)
  .speed(choose(1, 1.25, 1.5))
  .hpf(500)
  .room(0.3)
  .struct("x(3,8)")
  .gain(0.35)''',
    },
}


# Structured list of tutorials/learning resources
TUTORIALS = [
    {
        "title": "Getting Started",
        "url": "https://strudel.cc/learn/getting-started",
        "description": "Introduction to Strudel basics",
    },
    {
        "title": "Mini Notation",
        "url": "https://strudel.cc/learn/mini-notation",
        "description": "Pattern syntax reference",
    },
    {
        "title": "Synths & Sounds",
        "url": "https://strudel.cc/learn/synths",
        "description": "Using synthesizers and samples",
    },
    {
        "title": "Effects",
        "url": "https://strudel.cc/learn/effects",
        "description": "Filters, reverb, delay, etc.",
    },
    {
        "title": "Pattern Functions",
        "url": "https://strudel.cc/learn/functions",
        "description": "Transform and manipulate patterns",
    },
    {
        "title": "Samples",
        "url": "https://strudel.cc/learn/samples",
        "description": "Using sample banks and sounds",
    },
]


def get_snippets_by_category() -> Dict[str, List[Dict]]:
    """Get code snippets organized by category."""
    categories = {}
    for snippet_id, snippet in CODE_SNIPPETS.items():
        cat = snippet["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append({
            "id": snippet_id,
            "name": snippet["name"],
            "code": snippet["code"],
        })
    return categories


def get_snippet_code(snippet_id: str) -> str:
    """Get the code for a specific snippet."""
    if snippet_id in CODE_SNIPPETS:
        return CODE_SNIPPETS[snippet_id]["code"]
    return ""


def get_syntax_html() -> str:
    """Generate HTML for syntax reference popup."""
    html = '<div style="max-width: 400px; font-family: Inter, sans-serif;">'
    
    for section_id, section in SYNTAX_REFERENCE.items():
        html += f'<h4 style="color: #648cff; margin: 12px 0 6px 0;">{section["title"]}</h4>'
        html += '<table style="width: 100%; font-size: 11px; border-collapse: collapse;">'
        
        for item in section["items"]:
            html += f'''
            <tr>
                <td style="color: #20c997; padding: 2px 8px 2px 0; white-space: nowrap;"><code>{item["syntax"]}</code></td>
                <td style="color: #a0a0b0; padding: 2px 0;">{item["description"]}</td>
            </tr>
            '''
        
        html += '</table>'
    
    html += '</div>'
    return html


# Snippet categories for UI display
SNIPPET_CATEGORIES = [
    "Drums",
    "Bass", 
    "Chords",
    "Melody",
    "Percussion",
    "Ambient",
    "Samples",
]
