"""
Strudel Visualizer Module.

Provides JavaScript code for injecting audio visualizations into the 
embedded Strudel environment using Web Audio API.
"""

# Common visualizer container CSS
VISUALIZER_CONTAINER_CSS = """
#kraftbeat-visualizer {
    position: fixed;
    bottom: 60px;
    right: 20px;
    background: rgba(20, 20, 30, 0.9);
    border: 1px solid #404060;
    border-radius: 8px;
    padding: 10px;
    z-index: 9999;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

#kraftbeat-visualizer canvas {
    display: block;
    border-radius: 4px;
    background: #0a0a15;
}

#kraftbeat-visualizer .viz-title {
    color: #808090;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

#kraftbeat-visualizer .viz-controls {
    display: flex;
    gap: 8px;
    margin-top: 8px;
}

#kraftbeat-visualizer button {
    background: #303040;
    border: none;
    color: #a0a0b0;
    padding: 4px 10px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 11px;
}

#kraftbeat-visualizer button:hover {
    background: #404050;
    color: #e0e0f0;
}

#kraftbeat-visualizer button.active {
    background: #648cff;
    color: white;
}
"""


# Oscilloscope Visualizer
OSCILLOSCOPE_JS = """
(function() {
    // Remove existing visualizer
    var existing = document.getElementById('kraftbeat-visualizer');
    if (existing) existing.remove();
    
    // Create container
    var container = document.createElement('div');
    container.id = 'kraftbeat-visualizer';
    container.innerHTML = `
        <div class="viz-title">🔊 Oscilloscope</div>
        <canvas id="viz-canvas" width="300" height="100"></canvas>
        <div class="viz-controls">
            <button onclick="window.kraftbeatViz.setMode('oscilloscope')" class="active">Wave</button>
            <button onclick="window.kraftbeatViz.setMode('spectrum')">Spectrum</button>
            <button onclick="window.kraftbeatViz.close()">✕ Close</button>
        </div>
    `;
    document.body.appendChild(container);
    
    // Add styles
    var style = document.createElement('style');
    style.id = 'kraftbeat-viz-style';
    style.textContent = `VISUALIZER_CSS_PLACEHOLDER`;
    document.head.appendChild(style);
    
    // Get audio context from Strudel
    var audioCtx = window.audioContext || 
                   (window.repl && window.repl.scheduler && window.repl.scheduler.audio) ||
                   new (window.AudioContext || window.webkitAudioContext)();
    
    var analyser = audioCtx.createAnalyser();
    analyser.fftSize = 2048;
    
    // Try to connect to Strudel's audio output
    if (window.repl && window.repl.scheduler && window.repl.scheduler.audio) {
        try {
            // Connect to the audio destination's input
            var destination = audioCtx.destination;
            analyser.connect(destination);
        } catch(e) { console.log('Kraftbeat viz: Could not connect to Strudel audio', e); }
    }
    
    var canvas = document.getElementById('viz-canvas');
    var ctx = canvas.getContext('2d');
    var bufferLength = analyser.frequencyBinCount;
    var dataArray = new Uint8Array(bufferLength);
    var mode = 'oscilloscope';
    var running = true;
    
    function drawOscilloscope() {
        if (!running) return;
        requestAnimationFrame(drawOscilloscope);
        
        analyser.getByteTimeDomainData(dataArray);
        
        ctx.fillStyle = '#0a0a15';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#648cff';
        ctx.beginPath();
        
        var sliceWidth = canvas.width / bufferLength;
        var x = 0;
        
        for (var i = 0; i < bufferLength; i++) {
            var v = dataArray[i] / 128.0;
            var y = v * canvas.height / 2;
            
            if (i === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
            x += sliceWidth;
        }
        
        ctx.lineTo(canvas.width, canvas.height / 2);
        ctx.stroke();
    }
    
    function drawSpectrum() {
        if (!running) return;
        requestAnimationFrame(drawSpectrum);
        
        analyser.getByteFrequencyData(dataArray);
        
        ctx.fillStyle = '#0a0a15';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        var barWidth = (canvas.width / 64) - 1;
        var barHeight;
        var x = 0;
        
        for (var i = 0; i < 64; i++) {
            barHeight = dataArray[i * 2] / 255 * canvas.height;
            
            // Gradient from blue to purple to pink
            var hue = 220 + (i / 64) * 60;
            ctx.fillStyle = 'hsl(' + hue + ', 80%, 60%)';
            ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);
            
            x += barWidth + 1;
        }
    }
    
    window.kraftbeatViz = {
        setMode: function(newMode) {
            mode = newMode;
            running = false;
            setTimeout(function() {
                running = true;
                if (mode === 'oscilloscope') {
                    document.querySelector('#kraftbeat-visualizer .viz-title').textContent = '🔊 Oscilloscope';
                    drawOscilloscope();
                } else {
                    document.querySelector('#kraftbeat-visualizer .viz-title').textContent = '📊 Spectrum';
                    drawSpectrum();
                }
                
                // Update button states
                var buttons = document.querySelectorAll('#kraftbeat-visualizer button');
                buttons.forEach(function(btn) {
                    btn.classList.remove('active');
                    if (btn.textContent === 'Wave' && mode === 'oscilloscope') btn.classList.add('active');
                    if (btn.textContent === 'Spectrum' && mode === 'spectrum') btn.classList.add('active');
                });
            }, 50);
        },
        close: function() {
            running = false;
            var viz = document.getElementById('kraftbeat-visualizer');
            if (viz) viz.remove();
            var style = document.getElementById('kraftbeat-viz-style');
            if (style) style.remove();
        }
    };
    
    drawOscilloscope();
})();
"""


# Pianoroll Visualizer (shows note events)
PIANOROLL_JS = """
(function() {
    var existing = document.getElementById('kraftbeat-visualizer');
    if (existing) existing.remove();
    
    var container = document.createElement('div');
    container.id = 'kraftbeat-visualizer';
    container.innerHTML = `
        <div class="viz-title">🎹 Pianoroll</div>
        <canvas id="viz-canvas" width="300" height="150"></canvas>
        <div class="viz-controls">
            <button onclick="window.kraftbeatViz.clear()">Clear</button>
            <button onclick="window.kraftbeatViz.close()">✕ Close</button>
        </div>
    `;
    document.body.appendChild(container);
    
    var style = document.createElement('style');
    style.id = 'kraftbeat-viz-style';
    style.textContent = `VISUALIZER_CSS_PLACEHOLDER`;
    document.head.appendChild(style);
    
    var canvas = document.getElementById('viz-canvas');
    var ctx = canvas.getContext('2d');
    var notes = [];
    var running = true;
    
    function midiToY(midi) {
        // Map MIDI note 36-96 to canvas height
        var normalized = (midi - 36) / 60;
        return canvas.height - (normalized * canvas.height);
    }
    
    function noteToColor(midi) {
        var hue = (midi * 5) % 360;
        return 'hsl(' + hue + ', 70%, 55%)';
    }
    
    function draw() {
        if (!running) return;
        requestAnimationFrame(draw);
        
        ctx.fillStyle = '#0a0a15';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Draw piano roll grid
        ctx.strokeStyle = '#202030';
        ctx.lineWidth = 1;
        for (var i = 0; i < 12; i++) {
            var y = (i / 12) * canvas.height;
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(canvas.width, y);
            ctx.stroke();
        }
        
        // Update and draw notes
        var now = Date.now();
        notes = notes.filter(function(n) { return now - n.time < 3000; });
        
        notes.forEach(function(note) {
            var age = (now - note.time) / 3000;
            var x = (1 - age) * canvas.width;
            var y = midiToY(note.midi);
            var width = (note.duration || 100) / 10;
            
            ctx.fillStyle = noteToColor(note.midi);
            ctx.globalAlpha = 1 - age * 0.8;
            ctx.fillRect(x, y - 3, width, 6);
            ctx.globalAlpha = 1;
        });
    }
    
    // Try to hook into Strudel's note events
    if (window.scheduler) {
        var originalTrigger = window.scheduler.trigger;
        window.scheduler.trigger = function(hap) {
            if (hap && hap.value && hap.value.note !== undefined) {
                notes.push({
                    midi: hap.value.note,
                    time: Date.now(),
                    duration: (hap.duration || 0.1) * 1000
                });
            }
            return originalTrigger.apply(this, arguments);
        };
    }
    
    window.kraftbeatViz = {
        addNote: function(midi, duration) {
            notes.push({ midi: midi, time: Date.now(), duration: duration || 100 });
        },
        clear: function() {
            notes = [];
        },
        close: function() {
            running = false;
            var viz = document.getElementById('kraftbeat-visualizer');
            if (viz) viz.remove();
            var style = document.getElementById('kraftbeat-viz-style');
            if (style) style.remove();
        }
    };
    
    draw();
})();
"""


def get_oscilloscope_js() -> str:
    """Get JavaScript code for oscilloscope/spectrum visualizer."""
    return OSCILLOSCOPE_JS.replace('VISUALIZER_CSS_PLACEHOLDER', 
                                   VISUALIZER_CONTAINER_CSS.replace('\n', '\\n').replace("'", "\\'"))


def get_pianoroll_js() -> str:
    """Get JavaScript code for pianoroll visualizer."""
    from utils.config import get_config
    timing = get_config("note_display_timing_ms", 3000)
    js = PIANOROLL_JS.replace("3000", str(timing))
    return js.replace('VISUALIZER_CSS_PLACEHOLDER',
                                VISUALIZER_CONTAINER_CSS.replace('\n', '\\n').replace("'", "\\'"))


def get_close_visualizer_js() -> str:
    """Get JavaScript to close any open visualizer."""
    return """
    (function() {
        if (window.kraftbeatViz && window.kraftbeatViz.close) {
            window.kraftbeatViz.close();
        }
        var viz = document.getElementById('kraftbeat-visualizer');
        if (viz) viz.remove();
        var style = document.getElementById('kraftbeat-viz-style');
        if (style) style.remove();
    })();
    """


# Available visualizers for UI
VISUALIZERS = {
    "oscilloscope": {
        "name": "Oscilloscope",
        "description": "Waveform display with spectrum mode",
        "icon": "🔊",
    },
    "pianoroll": {
        "name": "Pianoroll", 
        "description": "MIDI-style note visualization",
        "icon": "🎹",
    },
}
