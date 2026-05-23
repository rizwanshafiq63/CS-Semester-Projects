// typing logic
// Typing Test Module for TypeMaster

class TypingTest {
    constructor() {
        this.paragraph = '';
        this.paragraphId = null;
        this.difficulty = 'medium';
        this.durationSeconds = 60;
        this.words = [];
        this.currentWordIndex = 0;
        this.currentCharIndex = 0;
        this.typedCharacters = 0;
        this.correctCharacters = 0;
        this.incorrectCharacters = 0;
        this.startTime = null;
        this.endTime = null;
        this.timerInterval = null;
        this.isActive = false;
        this.isCompleted = false;
        this.mistakes = 0;
        this.totalKeystrokes = 0;
        this.mode = "normal";
        
        // DOM elements
        this.textDisplay = document.getElementById('text-display');
        this.inputField = document.getElementById('typing-input');
        this.wpmDisplay = document.getElementById('wpm');
        this.accuracyDisplay = document.getElementById('accuracy');
        this.timeDisplay = document.getElementById('time');
        this.progressBar = document.getElementById('progress-bar');
        this.mistakesDisplay = document.getElementById('mistakes');
        this.restartBtn = document.getElementById('restart-btn');
        this.newTestBtn = document.getElementById('new-test-btn');
        this.resultsModal = document.getElementById('results-modal');
    }
    
    async init() {
        const params = new URLSearchParams(window.location.search);
        this.mode = params.get("mode") === "practice" ? "practice" : "normal";
        const banner = document.getElementById("mode-banner");
        if (banner) {
            banner.style.display = this.mode === "practice" ? "block" : "none";
        }

        await this.loadParagraph();
        this.setupEventListeners();
        this.renderParagraph();
    }
    
    async loadParagraph() {
        const difficultySelect = document.getElementById('difficulty-select');
        const durationSelect = document.getElementById('duration-select');

        this.difficulty = difficultySelect ? difficultySelect.value : this.difficulty;
        this.durationSeconds = durationSelect ? Number(durationSelect.value) : this.durationSeconds;

        try {
            const result = await window.api.getRandomParagraph(this.difficulty);
            const paragraph = result.paragraph;
            this.paragraphId = paragraph._id;
            this.paragraph = paragraph.text;
        } catch (e) {
            // Hard fallback to keep the UI usable if backend is temporarily unavailable
            this.paragraphId = null;
            this.paragraph = "The quick brown fox jumps over the lazy dog. Practice makes progress every day.";
        }

        this.words = this.paragraph.split(' ');
    }
    
    setupEventListeners() {
        this.inputField.addEventListener('input', (e) => this.handleInput(e));
        this.inputField.addEventListener('keydown', (e) => this.handleKeyDown(e));
        this.restartBtn.addEventListener('click', () => this.restart());
        this.newTestBtn.addEventListener('click', () => this.newTest());
        
        // Prevent paste
        this.inputField.addEventListener('paste', (e) => {
            e.preventDefault();
            showToast('Pasting is not allowed!', 'warning');
        });
        
        // Prevent cut
        this.inputField.addEventListener('cut', (e) => {
            e.preventDefault();
            showToast('Cutting is not allowed!', 'warning');
        });
        
        // Focus input on container click
        document.querySelector('.typing-container').addEventListener('click', () => {
            if (!this.isCompleted) {
                this.inputField.focus();
            }
        });
    }
    
    handleInput(e) {
        if (this.isCompleted) return;
        
        const input = e.target.value;
        this.totalKeystrokes++;
        
        // Start timer on first input
        if (!this.isActive && input.length === 1) {
            this.start();
        }
        
        this.checkInput(input);
        this.updateStats();
        this.updateProgress();

        // Finish early when user reaches paragraph length
        if (this.isActive && input.length >= this.paragraph.length) {
            this.complete();
        }
    }
    
    handleKeyDown(e) {
        if (this.isCompleted) {
            e.preventDefault();
            return;
        }

        // Optional typing sound effect (user setting)
        if (this.shouldPlayKeySound(e)) {
            this.playKeySound();
        }
    }

    shouldPlayKeySound(e) {
        try {
            const settings = typeof Storage !== "undefined" ? Storage.get("userSettings", {}) : {};
            if (!settings || settings.soundEffects !== true) return false;

            // Don't play for modifier keys
            if (e.ctrlKey || e.metaKey || e.altKey) return false;

            // Prefer only printable keys + backspace/space
            if (e.key === "Backspace" || e.key === " " || e.key === "Spacebar") return true;
            return typeof e.key === "string" && e.key.length === 1;
        } catch {
            return false;
        }
    }

    ensureAudioContext() {
        if (this._audio && this._audio.ctx) return this._audio.ctx;
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return null;

        const ctx = new AudioCtx();
        this._audio = { ctx };
        return ctx;
    }

    playKeySound() {
        const ctx = this.ensureAudioContext();
        if (!ctx) return;

        // Some browsers start suspended until user gesture; keydown is a gesture.
        if (ctx.state === "suspended") {
            ctx.resume().catch(() => {});
        }

        const now = ctx.currentTime;

        // Subtle click using a short filtered noise burst (lightweight)
        const bufferSize = Math.floor(ctx.sampleRate * 0.02); // 20ms
        const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            data[i] = (Math.random() * 2 - 1) * 0.35;
        }

        const source = ctx.createBufferSource();
        source.buffer = buffer;

        const filter = ctx.createBiquadFilter();
        filter.type = "highpass";
        filter.frequency.value = 1200;

        const gain = ctx.createGain();
        gain.gain.setValueAtTime(0.0, now);
        gain.gain.linearRampToValueAtTime(0.035, now + 0.002);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.02);

        source.connect(filter);
        filter.connect(gain);
        gain.connect(ctx.destination);

        source.start(now);
        source.stop(now + 0.03);
        source.onended = () => {
            try {
                source.disconnect();
                filter.disconnect();
                gain.disconnect();
            } catch {}
        };
    }
    
    checkInput(input) {
        const targetText = this.paragraph;
        const rawTyped = input;

        // Determine typed words for highlighting/cursor
        const typedTrimmed = rawTyped.trim();
        const typedWords = typedTrimmed ? typedTrimmed.split(' ') : [];
        const typedEndsWithSpace = rawTyped.endsWith(' ');

        let computedWordIndex = 0;
        if (rawTyped.length === 0) {
            computedWordIndex = 0;
        } else if (typedEndsWithSpace) {
            computedWordIndex = typedWords.length;
        } else {
            computedWordIndex = typedWords.length - 1;
        }
        computedWordIndex = Math.max(0, Math.min(computedWordIndex, this.words.length));

        this.currentWordIndex = computedWordIndex;
        this.currentCharIndex =
            computedWordIndex < typedWords.length && computedWordIndex < this.words.length
                ? (typedWords[computedWordIndex] || '').length
                : 0;

        const currentTypedWord =
            computedWordIndex < typedWords.length && computedWordIndex < this.words.length
                ? typedWords[computedWordIndex]
                : '';

        // Compute metrics using character-by-character comparison
        let correctChars = 0;
        const typedLen = rawTyped.length;
        const compareLen = Math.min(typedLen, targetText.length);
        for (let i = 0; i < compareLen; i++) {
            if (rawTyped[i] === targetText[i]) correctChars++;
        }

        this.typedCharacters = typedLen;
        this.correctCharacters = correctChars;
        this.mistakes = Math.max(0, this.typedCharacters - this.correctCharacters);

        // Render words with highlighting
        let html = '';
        for (let i = 0; i < this.words.length; i++) {
            const word = this.words[i];

            if (i < this.currentWordIndex) {
                const wasCorrect = typedWords[i] === word;
                html += `<span class="word ${wasCorrect ? 'correct' : 'incorrect'}">${word}</span> `;
                continue;
            }

            if (i === this.currentWordIndex && this.currentWordIndex < this.words.length) {
                html += '<span class="word active">';
                for (let j = 0; j < word.length; j++) {
                    if (j < currentTypedWord.length) {
                        if (currentTypedWord[j] === word[j]) {
                            html += `<span class="char correct">${word[j]}</span>`;
                        } else {
                            html += `<span class="char incorrect">${word[j]}</span>`;
                        }
                    } else {
                        html += `<span class="char">${word[j]}</span>`;
                    }
                }

                // Extra typed chars beyond the target word length
                if (currentTypedWord.length > word.length) {
                    for (let j = word.length; j < currentTypedWord.length; j++) {
                        html += `<span class="char incorrect extra">${currentTypedWord[j]}</span>`;
                    }
                }

                html += '</span> ';
                continue;
            }

            // Future words
            html += `<span class="word">${word}</span> `;
        }

        this.textDisplay.innerHTML = html;
        this.mistakesDisplay.textContent = this.mistakes;
    }
    
    start() {
        this.isActive = true;
        this.durationSeconds = Number(
            document.getElementById('duration-select')?.value || this.durationSeconds
        );
        this.startTime = Date.now();
        
        // Start timer
        this.timerInterval = setInterval(() => {
            this.updateTimer();
        }, 250);
    }
    
    updateTimer() {
        if (!this.startTime) return;

        const elapsedSeconds = (Date.now() - this.startTime) / 1000;
        const clampedElapsed = Math.min(elapsedSeconds, this.durationSeconds || 60);

        this.timeDisplay.textContent = formatTime(Math.floor(clampedElapsed));
        this.updateStats();
        this.updateProgress();

        if (elapsedSeconds >= (this.durationSeconds || 60)) {
            this.complete();
        }
    }
    
    updateStats() {
        if (!this.isActive) return;

        const elapsedSeconds = this.startTime
            ? (Date.now() - this.startTime) / 1000
            : 0;

        const minutes = elapsedSeconds / 60;
        const wpm =
            minutes > 0 ? Math.round((this.correctCharacters / 5) / minutes) : 0;

        const accuracy =
            this.typedCharacters > 0
                ? (this.correctCharacters / this.typedCharacters) * 100
                : 100;

        this.wpmDisplay.textContent = wpm;
        this.accuracyDisplay.textContent = Math.round(accuracy) + "%";
        this.mistakesDisplay.textContent = this.mistakes;
    }
    
    updateProgress() {
        const elapsedSeconds = this.startTime
            ? (Date.now() - this.startTime) / 1000
            : 0;

        const duration = this.durationSeconds || 60;
        const progress = Math.min(100, (elapsedSeconds / duration) * 100);
        this.progressBar.style.width = progress + "%";
    }
    
    complete() {
        if (this.isCompleted) return;
        this.isActive = false;
        this.isCompleted = true;
        this.endTime = Date.now();

        clearInterval(this.timerInterval);

        const timeInSeconds = this.startTime
            ? Math.min(this.durationSeconds || 60, (this.endTime - this.startTime) / 1000)
            : 0;

        // Recompute metrics from current input right at completion
        this.checkInput(this.inputField.value);

        const minutes = timeInSeconds / 60;
        const wpm =
            minutes > 0 ? Math.round((this.correctCharacters / 5) / minutes) : 0;

        const accuracy =
            this.typedCharacters > 0
                ? (this.correctCharacters / this.typedCharacters) * 100
                : 100;

        // Save result in background (don't block modal)
        this.saveResult(wpm, Number(accuracy.toFixed(2)), timeInSeconds);

        // Show results modal
        this.showResults(wpm, Number(accuracy.toFixed(2)), timeInSeconds);

        this.inputField.disabled = true;
    }
    
    async saveResult(wpm, accuracy, timeInSeconds) {
        if (this.mode === "practice") return;
        if (!this.paragraphId) return;
        if (!window.auth || !auth.isAuthenticated || !auth.isAuthenticated()) return;

        try {
            await window.api.submitResult({
                paragraph: this.paragraphId,
                difficulty: this.difficulty,
                duration: this.durationSeconds,
                wpm,
                accuracy,
                mistakes: this.mistakes,
                charsTyped: this.typedCharacters,
                timeTaken: timeInSeconds,
            });
        } catch (e) {
            console.error("Failed to save result:", e);
            showToast(e.message || "Failed to save result", "error");
        }
    }
    
    // Leaderboard update is handled by the backend after submitting results.
    
    showResults(wpm, accuracy, timeInSeconds) {
        const modal = document.getElementById('results-modal');
        const finalWpm = document.getElementById('final-wpm');
        const finalAccuracy = document.getElementById('final-accuracy');
        const finalTime = document.getElementById('final-time');
        const finalCharacters = document.getElementById('final-characters');
        const mistakesCount = document.getElementById('mistakes-count');
        
        finalWpm.textContent = wpm;
        finalAccuracy.textContent = accuracy + '%';
        finalTime.textContent = formatTime(Math.floor(timeInSeconds));
        finalCharacters.textContent = this.typedCharacters;
        mistakesCount.textContent = this.mistakes;
        
        modal.style.display = 'flex';
        
        // Animate numbers
        this.animateValue(finalWpm, 0, wpm, 1000, false);
        this.animateValue(finalAccuracy, 0, accuracy, 1000, true);
    }
    
    animateValue(element, start, end, duration, suffixPercent = false) {
        const range = end - start;
        const increment = range / (duration / 16);
        let current = start;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= end) {
                element.textContent = `${Math.round(end)}${suffixPercent ? "%" : ""}`;
                clearInterval(timer);
            } else {
                element.textContent = `${Math.round(current)}${suffixPercent ? "%" : ""}`;
            }
        }, 16);
    }
    
    restart() {
        this.currentWordIndex = 0;
        this.currentCharIndex = 0;
        this.typedCharacters = 0;
        this.correctCharacters = 0;
        this.incorrectCharacters = 0;
        this.startTime = null;
        this.endTime = null;
        this.isActive = false;
        this.isCompleted = false;
        this.mistakes = 0;
        this.totalKeystrokes = 0;
        
        clearInterval(this.timerInterval);
        
        this.inputField.value = '';
        this.inputField.disabled = false;
        this.wpmDisplay.textContent = '0';
        this.accuracyDisplay.textContent = '100%';
        this.timeDisplay.textContent = '00:00';
        this.mistakesDisplay.textContent = '0';
        this.progressBar.style.width = '0%';
        
        this.renderParagraph();
        this.inputField.focus();
        
        document.getElementById('results-modal').style.display = 'none';
    }
    
    async newTest() {
        await this.loadParagraph();
        this.restart();
    }
    
    renderParagraph() {
        let html = '';
        this.words.forEach((word, index) => {
            if (index === 0) {
                html += `<span class="word active">${word}</span> `;
            } else {
                html += `<span class="word">${word}</span> `;
            }
        });
        this.textDisplay.innerHTML = html;
    }
}

// Initialize typing test when page loads
let typingTest;
document.addEventListener('DOMContentLoaded', () => {
    typingTest = new TypingTest();
    typingTest.init().catch((e) => {
        console.error("Typing init failed:", e);
        showToast("Failed to load typing paragraph", "error");
    });
});