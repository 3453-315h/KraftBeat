"""
Strudel MIDI Integration.

Provides JavaScript code for Web MIDI API integration,
allowing MIDI controllers to interact with Strudel.
"""

# JavaScript for MIDI input handling
MIDI_INPUT_JS = """
(function() {
    // Check if MIDI is already initialized
    if (window.kraftbeatMIDI) {
        console.log('Kraftbeat MIDI already initialized');
        return;
    }
    
    // Store for MIDI state
    window.kraftbeatMIDI = {
        inputs: [],
        enabled: true,
        lastNote: null,
        noteLog: []
    };
    
    // Add MIDI status indicator
    var indicator = document.createElement('div');
    indicator.id = 'kraftbeat-midi-indicator';
    indicator.innerHTML = '🎹 MIDI: Connecting...';
    indicator.style.cssText = `
        position: fixed;
        bottom: 20px;
        left: 20px;
        background: rgba(30, 30, 40, 0.9);
        border: 1px solid #404060;
        border-radius: 6px;
        padding: 8px 12px;
        color: #a0a0b0;
        font-size: 11px;
        font-family: 'Inter', 'Segoe UI', sans-serif;
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 8px;
    `;
    document.body.appendChild(indicator);
    
    function updateIndicator(status, color) {
        indicator.innerHTML = '🎹 MIDI: ' + status;
        indicator.style.borderColor = color;
    }
    
    function noteToName(note) {
        var names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
        var octave = Math.floor(note / 12) - 1;
        return names[note % 12] + octave;
    }
    
    function handleMIDIMessage(event) {
        var data = event.data;
        var command = data[0] >> 4;
        var channel = data[0] & 0xf;
        var note = data[1];
        var velocity = data.length > 2 ? data[2] : 0;
        
        // Note On
        if (command === 9 && velocity > 0) {
            window.kraftbeatMIDI.lastNote = note;
            window.kraftbeatMIDI.noteLog.push({
                note: note,
                name: noteToName(note),
                velocity: velocity,
                time: Date.now()
            });
            
            // Keep only last 16 notes
            if (window.kraftbeatMIDI.noteLog.length > 16) {
                window.kraftbeatMIDI.noteLog.shift();
            }
            
            // Flash indicator
            updateIndicator(noteToName(note) + ' (vel:' + velocity + ')', '#20c997');
            setTimeout(function() {
                updateIndicator('Ready', '#648cff');
            }, 300);
            
            // Try to insert note into Strudel (if cursor is in editor)
            if (window.view && window.kraftbeatMIDI.enabled) {
                // Could insert note at cursor - but let user type manually
                // This just logs for now, visual feedback is the main feature
                console.log('MIDI Note:', noteToName(note), 'velocity:', velocity);
            }
        }
        // Note Off
        else if (command === 8 || (command === 9 && velocity === 0)) {
            // Note released
        }
        // Control Change
        else if (command === 11) {
            var cc = data[1];
            var value = data[2];
            console.log('MIDI CC:', cc, 'value:', value);
        }
    }
    
    function onMIDISuccess(midiAccess) {
        var inputs = midiAccess.inputs.values();
        var inputCount = 0;
        
        for (var input = inputs.next(); input && !input.done; input = inputs.next()) {
            input.value.onmidimessage = handleMIDIMessage;
            window.kraftbeatMIDI.inputs.push(input.value.name);
            inputCount++;
        }
        
        if (inputCount > 0) {
            updateIndicator('Ready (' + inputCount + ' device' + (inputCount > 1 ? 's' : '') + ')', '#648cff');
        } else {
            updateIndicator('No devices', '#808090');
        }
        
        // Listen for device changes
        midiAccess.onstatechange = function(e) {
            if (e.port.state === 'connected' && e.port.type === 'input') {
                e.port.onmidimessage = handleMIDIMessage;
                updateIndicator('Connected: ' + e.port.name, '#20c997');
            }
        };
    }
    
    function onMIDIFailure(error) {
        console.error('MIDI access denied:', error);
        updateIndicator('Not available', '#ff6b6b');
    }
    
    // Request MIDI access
    if (navigator.requestMIDIAccess) {
        navigator.requestMIDIAccess({ sysex: false })
            .then(onMIDISuccess)
            .catch(onMIDIFailure);
    } else {
        updateIndicator('Not supported', '#ff6b6b');
    }
    
    // Add helper functions
    window.kraftbeatMIDI.getLastNote = function() {
        return window.kraftbeatMIDI.lastNote;
    };
    
    window.kraftbeatMIDI.getNoteLog = function() {
        return window.kraftbeatMIDI.noteLog;
    };
    
    window.kraftbeatMIDI.close = function() {
        var indicator = document.getElementById('kraftbeat-midi-indicator');
        if (indicator) indicator.remove();
        window.kraftbeatMIDI = null;
    };
    
})();
"""

# JavaScript to close MIDI
MIDI_CLOSE_JS = """
(function() {
    if (window.kraftbeatMIDI && window.kraftbeatMIDI.close) {
        window.kraftbeatMIDI.close();
    }
    var indicator = document.getElementById('kraftbeat-midi-indicator');
    if (indicator) indicator.remove();
})();
"""


def get_midi_input_js() -> str:
    """Get JavaScript code for MIDI input initialization."""
    return MIDI_INPUT_JS


def get_midi_close_js() -> str:
    """Get JavaScript code to close MIDI handler."""
    return MIDI_CLOSE_JS
