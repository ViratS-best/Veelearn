/**
 * Animation System - Frame loop, easing, keyframe management
 * Provides animation timing and easing functions for block simulators
 * ~320 lines
 */

class AnimationSystem {
    constructor() {
        this.isRunning = false;
        this.frameCount = 0;
        this.startTime = 0;
        this.lastFrameTime = 0;
        this.deltaTime = 0;
        this.elapsedTime = 0;
        this.fps = 60;
        this.targetFrameTime = 1000 / 60;
        this.animationFrameId = null;
        this.callbacks = [];
    }

    /**
     * Start animation loop
     * @param {Function} callback - Called each frame with frameInfo
     */
    start(callback) {
        if (this.isRunning) return;

        this.isRunning = true;
        this.frameCount = 0;
        this.startTime = performance.now();
        this.lastFrameTime = this.startTime;
        this.elapsedTime = 0;

        if (typeof callback === 'function') {
            this.callbacks.push(callback);
        }

        this.loop(this.startTime);
    }

    /**
     * Stop animation loop
     */
    stop() {
        this.isRunning = false;
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
            this.animationFrameId = null;
        }
    }

    /**
     * Pause animation
     */
    pause() {
        this.stop();
    }

    /**
     * Resume animation
     */
    resume() {
        this.start();
    }

    /**
     * Main animation loop
     * @private
     */
    loop = (currentTime) => {
        if (!this.isRunning) return;

        // Calculate delta time
        this.deltaTime = (currentTime - this.lastFrameTime) / 1000; // Convert to seconds
        this.lastFrameTime = currentTime;
        this.elapsedTime = (currentTime - this.startTime) / 1000;
        this.frameCount++;

        // Calculate FPS
        this.fps = 1 / this.deltaTime;

        // Create frame info object
        const frameInfo = {
            frameCount: this.frameCount,
            deltaTime: this.deltaTime,
            elapsed: this.elapsedTime,
            fps: this.fps,
            isFirstFrame: this.frameCount === 1
        };

        // Call all registered callbacks
        this.callbacks.forEach(callback => {
            try {
                callback(frameInfo);
            } catch (error) {
                console.error('Animation callback error:', error);
            }
        });

        // Schedule next frame
        this.animationFrameId = requestAnimationFrame(this.loop);
    }

    /**
     * Add callback to animation loop
     * @param {Function} callback - Called each frame
     */
    addCallback(callback) {
        if (typeof callback === 'function') {
            this.callbacks.push(callback);
        }
    }

    /**
     * Remove callback
     * @param {Function} callback - Callback to remove
     */
    removeCallback(callback) {
        const index = this.callbacks.indexOf(callback);
        if (index > -1) {
            this.callbacks.splice(index, 1);
        }
    }

    /**
     * Seek to specific time
     * @param {Number} time - Time in seconds
     */
    seek(time) {
        this.elapsedTime = time;
    }

    /**
     * Get animation info
     * @returns {Object} Current animation state
     */
    getInfo() {
        return {
            isRunning: this.isRunning,
            frameCount: this.frameCount,
            deltaTime: this.deltaTime,
            elapsed: this.elapsedTime,
            fps: this.fps
        };
    }

    /**
     * Clear all callbacks
     */
    clear() {
        this.callbacks = [];
        this.stop();
    }
}

// ===== EASING FUNCTIONS =====
const EasingFunctions = {
    /**
     * Linear easing
     * @param {Number} t - Progress (0-1)
     */
    linear: (t) => t,

    /**
     * Ease in (quadratic)
     * @param {Number} t - Progress (0-1)
     */
    easeIn: (t) => t * t,

    /**
     * Ease out (quadratic)
     * @param {Number} t - Progress (0-1)
     */
    easeOut: (t) => 1 - (1 - t) * (1 - t),

    /**
     * Ease in-out (quadratic)
     * @param {Number} t - Progress (0-1)
     */
    easeInOut: (t) => t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2,

    /**
     * Cubic ease in
     * @param {Number} t - Progress (0-1)
     */
    easeInCubic: (t) => t * t * t,

    /**
     * Cubic ease out
     * @param {Number} t - Progress (0-1)
     */
    easeOutCubic: (t) => 1 - Math.pow(1 - t, 3),

    /**
     * Cubic ease in-out
     * @param {Number} t - Progress (0-1)
     */
    easeInOutCubic: (t) => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2,

    /**
     * Spring easing
     * @param {Number} t - Progress (0-1)
     */
    spring: (t) => 1 + -Math.exp(-6 * t) * Math.cos(t * 4 * Math.PI),

    /**
     * Bounce easing
     * @param {Number} t - Progress (0-1)
     */
    bounce: (t) => {
        if (t < 0.5) {
            return (1 - Math.cos(t * Math.PI * 4)) / 2;
        } else {
            return (1 + Math.cos((1 - t) * Math.PI * 4)) / 2;
        }
    },

    /**
     * Back easing (overshoot)
     * @param {Number} t - Progress (0-1)
     */
    back: (t) => t * t * (2.70158 * t - 1.70158),

    /**
     * Elastic easing
     * @param {Number} t - Progress (0-1)
     */
    elastic: (t) => {
        const c4 = (2 * Math.PI) / 3;
        return t === 0 ? 0 : t === 1 ? 1 : -Math.pow(2, 10 * t - 10) * Math.sin((t * 10 - 10.75) * c4);
    },

    /**
     * Get easing function by name
     * @param {String} name - Easing function name
     * @returns {Function} Easing function
     */
    get: function(name) {
        return this[name] || this.linear;
    }
};

// ===== KEYFRAME SYSTEM =====
class KeyframeTimeline {
    constructor() {
        this.keyframes = [];
        this.duration = 0;
        this.isPlaying = false;
        this.currentTime = 0;
    }

    /**
     * Add keyframe
     * @param {Number} time - Time in seconds
     * @param {Object} value - Keyframe value
     */
    addKeyframe(time, value) {
        this.keyframes.push({ time, value });
        this.keyframes.sort((a, b) => a.time - b.time);
        this.duration = Math.max(this.duration, time);
    }

    /**
     * Get value at time
     * @param {Number} time - Time in seconds
     * @param {String} easing - Easing function name
     * @returns {Object} Interpolated value
     */
    getValueAtTime(time, easing = 'linear') {
        if (this.keyframes.length === 0) return null;
        if (this.keyframes.length === 1) return this.keyframes[0].value;

        // Find surrounding keyframes
        let before = null, after = null;
        for (const kf of this.keyframes) {
            if (kf.time <= time) before = kf;
            if (kf.time >= time && !after) after = kf;
        }

        // Handle edge cases
        if (!before) return this.keyframes[0].value;
        if (!after) return this.keyframes[this.keyframes.length - 1].value;
        if (before === after) return before.value;

        // Interpolate
        const timeDiff = after.time - before.time;
        const t = (time - before.time) / timeDiff;
        const easingFn = EasingFunctions.get(easing);
        const easedT = easingFn(t);

        // Linear interpolation between values
        if (typeof before.value === 'number' && typeof after.value === 'number') {
            return before.value + (after.value - before.value) * easedT;
        }

        return before.value;
    }

    /**
     * Play timeline
     */
    play() {
        this.isPlaying = true;
        this.currentTime = 0;
    }

    /**
     * Stop timeline
     */
    stop() {
        this.isPlaying = false;
        this.currentTime = 0;
    }

    /**
     * Update timeline
     * @param {Number} deltaTime - Delta time in seconds
     */
    update(deltaTime) {
        if (!this.isPlaying) return;

        this.currentTime += deltaTime;
        if (this.currentTime > this.duration) {
            this.stop();
        }
    }

    /**
     * Clear all keyframes
     */
    clear() {
        this.keyframes = [];
        this.duration = 0;
    }
}

// ===== ANIMATION BLOCKS =====
const AnimationBlocks = {
    frameCounter: {
        title: 'Frame Counter',
        category: 'Animation',
        inputs: [],
        outputs: ['frame_count', 'delta_time', 'elapsed_time', 'fps'],
        execute: (inputs, state) => {
            // These are typically filled by the animation loop
            return {
                frame_count: state.frameCount || 0,
                delta_time: state.deltaTime || 0.016,
                elapsed_time: state.elapsed || 0,
                fps: state.fps || 60,
                state
            };
        }
    },

    keyframe: {
        title: 'Keyframe',
        category: 'Animation',
        inputs: [
            { name: 'frame_number', type: 'number', default: 0 },
            { name: 'repeat', type: 'number', default: 1 }
        ],
        outputs: ['progress', 'is_active'],
        execute: (inputs, state) => {
            const frameCount = state.frameCount || 0;
            const framePos = frameCount % (inputs.frame_number + 1);
            const isActive = framePos === inputs.frame_number;
            const progress = framePos / (inputs.frame_number + 1);

            return {
                progress,
                is_active: isActive,
                state
            };
        }
    },

    tween: {
        title: 'Tween Animation',
        category: 'Animation',
        inputs: [
            { name: 'start_value', type: 'number', default: 0 },
            { name: 'end_value', type: 'number', default: 100 },
            { name: 'duration', type: 'number', default: 1 },
            { name: 'easing', type: 'text', default: 'easeInOut' },
            { name: 'elapsed', type: 'number', default: 0 }
        ],
        outputs: ['value', 'progress', 'complete'],
        execute: (inputs, state) => {
            const progress = Math.min(1, inputs.elapsed / inputs.duration);
            const easingFn = EasingFunctions.get(inputs.easing);
            const easedProgress = easingFn(progress);
            const value = inputs.start_value + (inputs.end_value - inputs.start_value) * easedProgress;
            const complete = progress >= 1;

            return {
                value,
                progress,
                complete,
                state
            };
        }
    },

    delay: {
        title: 'Delay',
        category: 'Animation',
        inputs: [
            { name: 'delay_time', type: 'number', default: 1 },
            { name: 'elapsed', type: 'number', default: 0 }
        ],
        outputs: ['elapsed_after', 'delay_complete'],
        execute: (inputs, state) => {
            const delayComplete = inputs.elapsed >= inputs.delay_time;
            const elapsedAfter = Math.max(0, inputs.elapsed - inputs.delay_time);

            return {
                elapsed_after: elapsedAfter,
                delay_complete: delayComplete,
                state
            };
        }
    }
};

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        AnimationSystem,
        EasingFunctions,
        KeyframeTimeline,
        AnimationBlocks
    };
}
