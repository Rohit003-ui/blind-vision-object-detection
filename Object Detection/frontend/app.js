document.addEventListener('DOMContentLoaded', () => {
    // Determine Backend URL (auto fallback if opened via file:// vs http://localhost:5000)
    const API_BASE = window.location.protocol.startsWith('http') 
        ? window.location.origin 
        : 'http://localhost:5000';

    // DOM Elements
    const tryButtons = document.querySelectorAll('.try-button');
    const detectionModal = document.getElementById('detection-modal');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const startDetectionBtn = document.getElementById('start-detection-btn');
    const stopDetectionBtn = document.getElementById('stop-detection-btn');
    const toggleAudioBtn = document.getElementById('toggle-audio-btn');
    const videoStream = document.getElementById('video-stream');
    const streamPlaceholder = document.getElementById('stream-placeholder');
    const statusBadge = document.getElementById('status-badge');
    const detectionsContainer = document.getElementById('detections-list');
    const contactForm = document.querySelector('.contact-form');
    const contactResponse = document.getElementById('contact-response');

    let isDetecting = false;
    let isAudioEnabled = true;
    let statusInterval = null;

    // --- Modal Controls ---
    function openDetectionModal() {
        if (detectionModal) {
            detectionModal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
            startDetection();
        }
    }

    function closeDetectionModal() {
        if (detectionModal) {
            stopDetection();
            detectionModal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    }

    tryButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const targetSection = document.getElementById('live-detection');
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth' });
                startDetection();
            } else {
                openDetectionModal();
            }
        });
    });

    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', closeDetectionModal);
    }

    // --- Detection Controls ---
    async function startDetection() {
        if (isDetecting) return;
        isDetecting = true;

        if (videoStream) {
            videoStream.src = `${API_BASE}/api/video_feed?t=${new Date().getTime()}`;
            videoStream.style.display = 'block';
        }
        if (streamPlaceholder) {
            streamPlaceholder.style.display = 'none';
        }
        if (statusBadge) {
            statusBadge.textContent = '● LIVE DETECTION';
            statusBadge.className = 'status-badge active';
        }
        startStatusPolling();

        try {
            const response = await fetch(`${API_BASE}/api/start_detection`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            const data = await response.json();
            if (!data.success) {
                console.warn('Backend reported issue starting camera:', data.message);
            }
        } catch (error) {
            console.error('Detection start error:', error);
            if (statusBadge) {
                statusBadge.textContent = 'Backend Offline / Camera Error';
                statusBadge.className = 'status-badge error';
            }
            if (streamPlaceholder) {
                streamPlaceholder.style.display = 'flex';
                streamPlaceholder.innerHTML = `
                    <div class="placeholder-content">
                        <span class="icon">⚠️</span>
                        <p>Could not connect to Python OpenCV Backend.</p>
                        <small>Make sure python backend server is running on <code>http://localhost:5000</code></small>
                    </div>
                `;
            }
        }
    }

    async function stopDetection() {
        isDetecting = false;
        stopStatusPolling();

        try {
            await fetch(`${API_BASE}/api/stop_detection`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
        } catch (err) {
            console.warn('Backend stop notification error:', err);
        }

        if (videoStream) {
            videoStream.src = '';
            videoStream.style.display = 'none';
        }
        if (streamPlaceholder) {
            streamPlaceholder.style.display = 'flex';
        }
        if (statusBadge) {
            statusBadge.textContent = '○ DETECTION OFF';
            statusBadge.className = 'status-badge inactive';
        }
        if (detectionsContainer) {
            detectionsContainer.innerHTML = '<span class="empty-msg">No active camera stream</span>';
        }
    }

    async function toggleAudio() {
        isAudioEnabled = !isAudioEnabled;
        try {
            const res = await fetch(`${API_BASE}/api/toggle_audio`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ enabled: isAudioEnabled })
            });
            const data = await res.json();
            isAudioEnabled = data.audio_enabled;
        } catch (err) {
            console.warn('Failed to sync audio toggle with backend', err);
        }

        if (toggleAudioBtn) {
            toggleAudioBtn.innerHTML = isAudioEnabled ? '🔊 Audio Feedback: ON' : '🔇 Audio Feedback: OFF';
            toggleAudioBtn.classList.toggle('muted', !isAudioEnabled);
        }
    }

    function startStatusPolling() {
        stopStatusPolling();
        statusInterval = setInterval(async () => {
            if (!isDetecting) return;
            try {
                const res = await fetch(`${API_BASE}/api/status`);
                if (res.ok) {
                    const status = await res.json();
                    updateDetectionsUI(status.detections);
                }
            } catch (e) {
                console.warn('Status poll error', e);
            }
        }, 1000);
    }

    function stopStatusPolling() {
        if (statusInterval) {
            clearInterval(statusInterval);
            statusInterval = null;
        }
    }

    function updateDetectionsUI(detections) {
        if (!detectionsContainer) return;

        if (!detections || detections.length === 0) {
            detectionsContainer.innerHTML = '<span class="empty-msg">Scanning environment...</span>';
            return;
        }

        detectionsContainer.innerHTML = detections.map(item => `
            <div class="detection-tag">
                <span class="det-name">${item.name}</span>
                <span class="det-conf">${item.confidence}%</span>
            </div>
        `).join('');
    }

    // Attach Event Listeners
    if (startDetectionBtn) startDetectionBtn.addEventListener('click', startDetection);
    if (stopDetectionBtn) stopDetectionBtn.addEventListener('click', stopDetection);
    if (toggleAudioBtn) toggleAudioBtn.addEventListener('click', toggleAudio);

    // --- Contact Form AJAX Handler ---
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(contactForm);
            const payload = Object.fromEntries(formData.entries());

            try {
                const res = await fetch(`${API_BASE}/api/contact`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                
                if (contactResponse) {
                    contactResponse.className = 'contact-alert success';
                    contactResponse.textContent = data.message || 'Message sent successfully!';
                    contactResponse.style.display = 'block';
                }
                contactForm.reset();
            } catch (err) {
                if (contactResponse) {
                    contactResponse.className = 'contact-alert success';
                    contactResponse.textContent = 'Thank you! Your feedback has been recorded.';
                    contactResponse.style.display = 'block';
                }
                contactForm.reset();
            }
        });
    }
});
