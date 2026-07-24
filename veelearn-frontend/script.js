// ===== GLOBAL VARIABLES =====
let serverLoadingManager = null;

// Determine API base URL based on environment
const API_BASE_URL = (() => {
    if (window.location.hostname.includes('veelearn.org')) {
        return 'https://api.veelearn.org';
    }
    // If on GitHub Pages, use Render backend
    if (window.location.hostname.includes('github.io')) {
        return 'https://veelearn.onrender.com';
    }
    // If on localhost, use local backend
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        return 'http://localhost:3000';
    }
    // Otherwise use same origin
    return window.location.origin;
})();

let currentUser = null;
let courseBlocks = [];
let currentEditingCourseId = null;
let currentEditingSimulatorBlockId = null;
let simulatorCache = [];
let authToken = localStorage.getItem("token") || null; // Restore session on refresh
let myCourses = [];
let coursePages = [""]; // Array to store content for each page
let currentPageIndex = 0;
let isPlacementMode = false; // Flag for cursor-based placement
let placementType = null; // 'visual-simulator', 'block-simulator', 'quiz'
let placementData = null; // Data to pass to insertion function
let availableCourses = [];
/** All approved courses (incl. own) — used when searching so units/masters appear */
let allApprovedCourses = [];
let allUsers = [];
let courseQuestions = [];
let pendingCourses = [];
/** When viewing a course, sent to study coach for context (child unit id in master courses). */
let currentViewingCourseId = null;
let currentEditingQuestionId = null;
let lastDeletedQuestion = null; // Store last deleted question for undo
let savedSelection = null; // Save cursor position when editor loses focus
const COURSE_LIST_PAGE_SIZE = 12;
let myCoursesCurrentPage = 1;
let availableCoursesCurrentPage = 1;
let myCoursesCurrentSearch = "";
let availableCoursesCurrentSearch = "";

// (Old timer variables removed — courseTimer object at bottom of file handles everything)

// Animation preference
let animationMode = localStorage.getItem('animationMode') || 'short';
let transitionCount = 0;

// Global keyboard listener for Ctrl+Z undo
document.addEventListener('keydown', async (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'z' && lastDeletedQuestion) {
        e.preventDefault();
        if (window.logger) window.logger.debug('↩️ Ctrl+Z pressed - Undoing quiz deletion');

        if (!currentEditingCourseId) {
            console.warn('Cannot undo: no course being edited');
            return;
        }

        // Re-create the question via API
        try {
            const response = await fetch(`${API_BASE_URL}/api/courses/${currentEditingCourseId}/questions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${authToken}`
                },
                body: JSON.stringify(lastDeletedQuestion)
            });

            const result = await response.json();
            if (result.success) {
                alert('✅ Question restored!');
                await loadCourseQuestions(currentEditingCourseId);

                // Clear all placeholders and re-render
                const editor = document.getElementById('course-content-editor');
                editor.querySelectorAll('.quiz-question-placeholder').forEach(p => p.remove());
                courseQuestions.forEach(q => insertQuizPlaceholder(q.question_text, q.id));

                lastDeletedQuestion = null; // Clear undo history
            } else {
                alert('Error restoring question: ' + result.message);
            }
        } catch (error) {
            console.error('Error undoing deletion:', error);
            alert('Error restoring question');
        }
    }
});


// ===== CLIENT-SIDE KEEP-ALIVE SYSTEM =====

// Keep server alive during user activity
let keepAliveInterval = null;
let lastActivityTime = Date.now();

function startKeepAlive() {
    // Clear any existing interval
    if (keepAliveInterval) {
        clearInterval(keepAliveInterval);
    }
    
    // Ping server every 10 minutes during user activity
    keepAliveInterval = setInterval(async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/health`, {
                method: 'GET',
                cache: 'no-store',
                credentials: 'omit'
            });
            
            if (response.ok) {
                console.log('✅ Keep-alive ping successful');
            } else {
                console.log('⚠️ Keep-alive ping failed:', response.status);
            }
        } catch (error) {
            console.log('❌ Keep-alive ping error:', error.message);
        }
    }, 10 * 60 * 1000); // Every 10 minutes
    
    console.log('🔄 Client-side keep-alive started');
}

// Track user activity to keep server alive
function trackUserActivity() {
    lastActivityTime = Date.now();
    
    // Start keep-alive if not already running
    if (!keepAliveInterval) {
        startKeepAlive();
    }
}

// Stop keep-alive after 30 minutes of inactivity
function checkInactivity() {
    const inactiveTime = Date.now() - lastActivityTime;
    const thirtyMinutes = 30 * 60 * 1000;
    
    if (inactiveTime > thirtyMinutes && keepAliveInterval) {
        clearInterval(keepAliveInterval);
        keepAliveInterval = null;
        console.log('⏸️ Keep-alive paused due to inactivity');
    }
}

// Set up activity tracking
document.addEventListener('DOMContentLoaded', () => {
    // Track user interactions
    const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];
    events.forEach(event => {
        document.addEventListener(event, trackUserActivity, { passive: true });
    });
    
    // Check inactivity every 5 minutes
    setInterval(checkInactivity, 5 * 60 * 1000);
    
    // Start keep-alive immediately
    startKeepAlive();
});

// ===== SERVER LOADING DETECTION =====

async function checkServerHealth() {
    try {
        // Use a shorter timeout to quickly detect if server is responsive
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 2000);
        
        const response = await fetch(`${API_BASE_URL}/api/health`, {
            method: 'GET',
            signal: controller.signal,
            cache: 'no-store'
        });
        
        clearTimeout(timeoutId);
        
        // Check if response is successful and has valid JSON
        if (response.ok) {
            const data = await response.json();
            return data.status === 'ok';
        }
        return false;
    } catch (error) {
        // Only treat as failure if it's not a timeout (server might be slow but working)
        if (error.name === 'AbortError') {
            console.log('Server health check timeout - server might be slow');
            return false;
        }
        console.log('Server health check failed:', error.message);
        return false;
    }
}

async function handleWithServerLoading(apiCall, action = 'login') {
    // Try the API call first - only show loading screen if it fails
    try {
        // Set a timeout for the API call
        const timeoutPromise = new Promise((_, reject) => {
            setTimeout(() => reject(new Error('API timeout')), 5000);
        });
        
        // Race between the actual API call and timeout
        const result = await Promise.race([apiCall(), timeoutPromise]);
        
        // If we get here, the API call succeeded - no loading screen needed
        return result;
        
    } catch (error) {
        // API call failed or timed out - now check if it's a server wake-up issue
        console.log('API call failed, checking server health:', error.message);
        
        // Quick server health check
        const isServerHealthy = await checkServerHealth();
        
        if (!isServerHealthy && (error.message === 'API timeout' || error.message.includes('fetch'))) {
            // Server is likely waking up - show loading screen
            console.log('Server appears to be waking up, showing loading screen');
            ServerLoadingManager.show(action);
            
            // Wait for server to be ready
            let attempts = 0;
            const maxAttempts = 15; // 15 * 2 seconds = 30 seconds max
            
            while (attempts < maxAttempts) {
                await new Promise(resolve => setTimeout(resolve, 2000));
                const serverReady = await checkServerHealth();
                
                if (serverReady) {
                    ServerLoadingManager.hide();
                    console.log('Server is ready, retrying API call');
                    // Retry the original API call
                    return apiCall();
                }
                attempts++;
            }
            
            // If server still not ready, hide loading screen and proceed with original error
            console.warn('Server still not ready after maximum attempts');
            ServerLoadingManager.hide();
        }
        
        // Re-throw the original error
        throw error;
    }
}

// ===== INITIALIZATION =====
if (window.logger) {
    window.logger.debug("🚀 Veelearn Script v3 Loaded");
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeApp);
} else {
    initializeApp();
}

// ===== PAGE TRANSITION HELPERS =====
function createAuroraOverlay() {
    // Create aurora overlay if it doesn't exist
    if (!document.getElementById('aurora-overlay')) {
        const overlay = document.createElement('div');
        overlay.id = 'aurora-overlay';
        overlay.className = 'aurora-overlay';
        overlay.innerHTML = `
      <div class="aurora-light aurora-light-1"></div>
      <div class="aurora-light aurora-light-2"></div>
      <div class="aurora-light aurora-light-3"></div>
    `;
        document.body.appendChild(overlay);
    }
}

function playPageTransition() {
    // Create transition overlay
    const overlay = document.createElement('div');
    overlay.className = 'page-transition-overlay';
    document.body.appendChild(overlay);

    // Remove after animation
    setTimeout(() => {
        overlay.remove();
    }, 3000);
}

/**
 * Create awesome wave transition with particles and glow
 */
function createWaveTransition() {
    // Wave overlay
    const wave = document.createElement('div');
    wave.className = 'wave-transition-overlay';
    document.body.appendChild(wave);

    // Create particle burst
    createParticleBurst();

    // Glow flash
    const glow = document.createElement('div');
    glow.className = 'page-glow-flash';
    document.body.appendChild(glow);

    // Remove overlays after animation
    setTimeout(() => {
        wave.remove();
        glow.remove();
    }, 1200);
}

/**
 * Create particle burst effect at center
 */
function createParticleBurst() {
    const container = document.createElement('div');
    container.className = 'particle-burst-container';
    document.body.appendChild(container);

    const particleCount = 20;
    const colors = [
        'rgba(59, 130, 246, 0.8)',   // Blue
        'rgba(6, 182, 212, 0.8)',    // Cyan
        'rgba(16, 185, 129, 0.8)',   // Green
        'rgba(245, 158, 11, 0.8)',   // Amber
    ];

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';

        // Random direction
        const angle = (i / particleCount) * Math.PI * 2;
        const distance = 150 + Math.random() * 100;
        const tx = Math.cos(angle) * distance;
        const ty = Math.sin(angle) * distance;

        particle.style.setProperty('--tx', `${tx}px`);
        particle.style.setProperty('--ty', `${ty}px`);
        particle.style.backgroundColor = colors[i % colors.length];
        particle.style.animation = `particleBurst 0.8s ease-out forwards`;
        particle.style.animationDelay = `${i * 0.02}s`;

        container.appendChild(particle);
    }

    setTimeout(() => container.remove(), 1000);
}

/**
 * Create wave pulse bars
 */
function createWaveBars() {
    const barCount = 4;
    for (let i = 0; i < barCount; i++) {
        const bar = document.createElement('div');
        bar.className = 'wave-bar';
        bar.style.top = `${25 + i * 20}%`;
        bar.style.animation = `wavePulse 0.6s ease-out ${i * 0.1}s forwards`;
        document.body.appendChild(bar);

        setTimeout(() => bar.remove(), 800);
    }
}

function transitionPage(fromSection, toSection) {
    // Add exit animation to current section
    if (fromSection && fromSection.style.display !== 'none') {
        fromSection.classList.add('page-transition-out');
    }

    // Choose animation based on preference
    if (animationMode === 'long') {
        playEpicBattleAnimation(fromSection, toSection);
    } else {
        playShortTransition(fromSection, toSection);
    }
}

/**
 * Play short transition (original animations)
 */
function playShortTransition(fromSection, toSection) {
    createWaveTransition();
    createWaveBars();

    setTimeout(() => {
        if (fromSection) fromSection.style.display = 'none';
        if (fromSection) fromSection.classList.remove('page-transition-out');

        toSection.style.display = 'block';
        toSection.classList.add('transition-in-active');

        setTimeout(() => {
            const sections = toSection.querySelectorAll('section');
            sections.forEach((section, index) => {
                section.style.animation = `contentFadeInScale 0.7s cubic-bezier(0.34, 1.56, 0.64, 1) ${index * 0.1}s forwards`;
                section.style.opacity = '0';
            });
        }, 100);

        setTimeout(() => {
            toSection.classList.remove('transition-in-active');
        }, 800);
    }, 400);
}

/**
 * Play epic battle animation with professional anime-style visual
 */
function playEpicBattleAnimation(fromSection, toSection) {
    transitionCount++;
    createAnimeStyleBattle(() => {
        if (fromSection) fromSection.style.display = 'none';
        if (fromSection) fromSection.classList.remove('page-transition-out');

        toSection.style.display = 'block';
        toSection.classList.add('transition-in-active');

        setTimeout(() => {
            const sections = toSection.querySelectorAll('section');
            sections.forEach((section, index) => {
                section.style.animation = `contentFadeInScale 0.7s cubic-bezier(0.34, 1.56, 0.64, 1) ${index * 0.1}s forwards`;
                section.style.opacity = '0';
            });
        }, 100);

        setTimeout(() => {
            toSection.classList.remove('transition-in-active');
        }, 800);
    });
}

/**
 * Create professional anime-style battle animation
 * Uses canvas-rendered characters, no HUD elements, 5s backstory + 15-20s epic fight
 */
async function createAnimeStyleBattle(onComplete) {
    if (typeof AnimeBattleSystem === "undefined" && typeof window.__veelearnLoadHeavy === "function") {
        try {
            await window.__veelearnLoadHeavy("battle");
        } catch (e) {
            console.warn("Battle system failed to load; skipping animation", e);
            if (typeof onComplete === "function") onComplete();
            return;
        }
    }
    if (typeof AnimeBattleSystem === "undefined") {
        if (typeof onComplete === "function") onComplete();
        return;
    }

    const setup = getRandomCharacterSetup();

    // Create container
    const container = document.createElement('div');
    container.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 9999;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
    `;
    document.body.appendChild(container);

    // Initialize anime battle system
    const battleSystem = new AnimeBattleSystem(setup);
    battleSystem.init(container);

    // Animation loop
    let lastTime = Date.now();
    let isComplete = false;

    function animate() {
        const currentTime = Date.now();
        const deltaTime = currentTime - lastTime;
        lastTime = currentTime;

        battleSystem.animate(deltaTime);

        // Apply camera shake effect
        if (battleSystem.cameraShakeIntensity > 0) {
            const shake = battleSystem.cameraShakeIntensity;
            container.style.transform = `translate(${(Math.random() - 0.5) * shake * 10}px, ${(Math.random() - 0.5) * shake * 10}px)`;
        } else {
            container.style.transform = 'translate(0, 0)';
        }

        // Check if battle complete (immediately, no delay)
        if (battleSystem.isComplete && !isComplete) {
            isComplete = true;
            container.remove();
            onComplete();
        } else if (!isComplete) {
            requestAnimationFrame(animate);
        }
    }

    animate();
}

/**
 * NEW: Character and environment generation for anime-style battles
 */
const characterProfiles = {
    heroes: [
        { id: 'samurai', name: 'Shadow Samurai', color: '#e74c3c', accent: '#c0392b', weapon: 'katana' },
        { id: 'knight', name: 'Steel Knight', color: '#3498db', accent: '#2980b9', weapon: 'sword' },
        { id: 'mage', name: 'Archmage', color: '#9b59b6', accent: '#8e44ad', weapon: 'staff' },
        { id: 'rogue', name: 'Shadow Assassin', color: '#34495e', accent: '#2c3e50', weapon: 'dagger' },
        { id: 'paladin', name: 'Holy Knight', color: '#f39c12', accent: '#e67e22', weapon: 'mace' },
    ],
    enemies: [
        { id: 'demon', name: 'Demon Lord', color: '#8b0000', accent: '#c41e3a', size: 1.2 },
        { id: 'dragon', name: 'Ancient Dragon', color: '#2f4f4f', accent: '#4db8ff', size: 1.4 },
        { id: 'warlock', name: 'Dark Warlock', color: '#4b0082', accent: '#9932cc', size: 0.95 },
        { id: 'golem', name: 'Stone Titan', color: '#696969', accent: '#a9a9a9', size: 1.3 },
        { id: 'wraith', name: 'Void Wraith', color: '#1a1a2e', accent: '#16213e', size: 1.05 },
    ],
    environments: [
        { id: 'forest', name: 'Mystic Forest', skyColor: '#2d5016', groundColor: '#1b3a0d', accent1: '#52b788', accent2: '#2d6a4f' },
        { id: 'volcano', name: 'Volcanic Crater', skyColor: '#5c2e1a', groundColor: '#8b0000', accent1: '#ff4500', accent2: '#ffa500' },
        { id: 'ocean', name: 'Stormy Ocean', skyColor: '#0a3d62', groundColor: '#1c5aa0', accent1: '#5dade2', accent2: '#3498db' },
        { id: 'castle', name: 'Ruined Castle', skyColor: '#4a4a4a', groundColor: '#2a2a2a', accent1: '#696969', accent2: '#808080' },
        { id: 'sky', name: 'Floating Sky', skyColor: '#4a90e2', groundColor: '#87ceeb', accent1: '#2c5aa0', accent2: '#5dade2' },
    ]
};

function getRandomCharacterSetup() {
    const hero = characterProfiles.heroes[Math.floor(Math.random() * characterProfiles.heroes.length)];
    const enemy = characterProfiles.enemies[Math.floor(Math.random() * characterProfiles.enemies.length)];
    const environment = characterProfiles.environments[Math.floor(Math.random() * characterProfiles.environments.length)];
    const isEpic = Math.random() < 0.05;
    return { hero, enemy, environment, isEpic, duration: isEpic ? 25000 : 17000 };
}

/**
 * Get random story with probability - DEPRECATED, use getRandomCharacterSetup instead
 */
function getRandomStory() {
    const rand = Math.random() * 100;
    // Common stories (70% chance)
    if (rand < 70) return Math.floor(Math.random() * 5);
    // Uncommon stories (25% chance)
    if (rand < 95) return 5 + Math.floor(Math.random() * 3);
    // Ultra rare (5% chance)
    return 8;
}

/**
 * Get all battle stories with full combat details
 */
function getBattleStories() {
    return [
        // COMMON STORIES (70% chance)
        {
            name: 'Forest Guardian Battle',
            hero: { char: '⚔️', name: 'Knight', class: 'warrior' },
            monster: { char: '🐺', name: 'Shadow Beast', health: 100 },
            environment: 'forest',
            duration: 18000,
            difficulty: 'normal'
        },
        {
            name: 'Ocean Depths Battle',
            hero: { char: '🧜', name: 'Mage', class: 'mage' },
            monster: { char: '🦑', name: 'Kraken', health: 120 },
            environment: 'ocean',
            duration: 20000,
            difficulty: 'normal'
        },
        {
            name: 'Sky Realm Battle',
            hero: { char: '🦅', name: 'Archer', class: 'archer' },
            monster: { char: '🦇', name: 'Night Demon', health: 90 },
            environment: 'sky',
            duration: 17000,
            difficulty: 'normal'
        },
        {
            name: 'Lava Castle Battle',
            hero: { char: '🛡️', name: 'Paladin', class: 'warrior' },
            monster: { char: '🔥', name: 'Inferno Lord', health: 150 },
            environment: 'lava',
            duration: 22000,
            difficulty: 'normal'
        },
        {
            name: 'Ancient Tomb Battle',
            hero: { char: '💀', name: 'Necromancer', class: 'mage' },
            monster: { char: '👻', name: 'Phantom King', health: 110 },
            environment: 'tomb',
            duration: 19000,
            difficulty: 'normal'
        },
        // UNCOMMON STORIES (25% chance)
        {
            name: 'Thunder Sanctum Battle',
            hero: { char: '⚡', name: 'Thunder Sage', class: 'mage' },
            monster: { char: '🐉', name: 'Ancient Dragon', health: 180 },
            environment: 'thunder',
            duration: 24000,
            difficulty: 'hard'
        },
        {
            name: 'Ice Peak Battle',
            hero: { char: '❄️', name: 'Frost Knight', class: 'warrior' },
            monster: { char: '🧊', name: 'Ice Titan', health: 160 },
            environment: 'ice',
            duration: 23000,
            difficulty: 'hard'
        },
        {
            name: 'Shadow Void Battle',
            hero: { char: '🌑', name: 'Shadow Assassin', class: 'archer' },
            monster: { char: '👁️', name: 'Void Entity', health: 140 },
            environment: 'void',
            duration: 21000,
            difficulty: 'hard'
        },
        // ULTRA RARE EPIC BOSS (5% chance)
        {
            name: '✨ THE LEGEND AWAKENS ✨',
            hero: { char: '👑', name: 'Chosen One', class: 'legendary' },
            monster: { char: '🐲', name: 'Eternal Dragon', health: 300 },
            environment: 'cosmic',
            duration: 30000,
            difficulty: 'legendary',
            isEpic: true
        }
    ];
}

/**
 * DEPRECATED: Old battle scene creation - replaced by anime-battle-system.js
 * Kept for backwards compatibility if needed, but not used in playEpicBattleAnimation
 * 
 * The new system provides:
 * - Canvas-rendered drawn characters (no emojis)
 * - 5-second backstory montage with animated scenes
 * - 15-20 second epic anime-style combat
 * - Camera shake effects
 * - Perspective-shifting artistic backgrounds
 * - Zero HUD elements (no stats, health bars, or battle logs)
 */
function createBattleScene_DEPRECATED(story, onComplete) {
    // This function is deprecated. Use createAnimeStyleBattle() instead
    // which calls AnimeBattleSystem from anime-battle-system.js

    console.warn('createBattleScene_DEPRECATED called - using new anime battle system instead');
    createAnimeStyleBattle(onComplete);
    return;
}

/**
 * Get environment background CSS
 */
function getEnvironmentBackground(env) {
    const backgrounds = {
        forest: 'linear-gradient(135deg, #1a4d2e 0%, #2d5a3d 50%, #1a3a28 100%)',
        ocean: 'linear-gradient(135deg, #001f3f 0%, #003d7a 50%, #000000 100%)',
        sky: 'linear-gradient(180deg, #87ceeb 0%, #e0f6ff 50%, #ffb6c1 100%)',
        lava: 'linear-gradient(135deg, #8b0000 0%, #ff4500 50%, #4d0000 100%)',
        tomb: 'linear-gradient(135deg, #2f2f2f 0%, #1a1a1a 50%, #0d0d0d 100%)',
        thunder: 'linear-gradient(135deg, #1a1a3e 0%, #0f0f2e 50%, #2d2d5f 100%)',
        ice: 'linear-gradient(135deg, #b0e0e6 0%, #87ceeb 50%, #4682b4 100%)',
        void: 'linear-gradient(135deg, #0a0a0a 0%, #1a0033 50%, #000000 100%)',
        cosmic: 'linear-gradient(135deg, #0a0a2e 0%, #16213e 50%, #0f3460 100%)'
    };
    return backgrounds[env] || backgrounds.forest;
}

/**
 * Create environment visual layer
 */
function createEnvironmentLayer(container, env) {
    const layer = document.createElement('div');
    layer.style.position = 'absolute';
    layer.style.width = '100%';
    layer.style.height = '100%';
    layer.style.pointerEvents = 'none';
    layer.style.overflow = 'hidden';

    if (env === 'forest') {
        // Trees
        for (let i = 0; i < 5; i++) {
            const tree = document.createElement('div');
            tree.textContent = '🌲';
            tree.style.position = 'absolute';
            tree.style.fontSize = '120px';
            tree.style.opacity = '0.3';
            tree.style.left = (i * 20) + '%';
            tree.style.top = (10 + Math.random() * 20) + '%';
            layer.appendChild(tree);
        }
    } else if (env === 'ocean') {
        // Waves animation
        for (let i = 0; i < 3; i++) {
            const wave = document.createElement('div');
            wave.style.position = 'absolute';
            wave.style.width = '200%';
            wave.style.height = '80px';
            wave.style.bottom = (i * 60) + 'px';
            wave.style.background = `url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120"><path d="M0,50 Q300,0 600,50 T1200,50" stroke="rgba(255,255,255,0.2)" fill="none" stroke-width="2"/></svg>')`;
            wave.style.animation = `wave 8s linear infinite`;
            wave.style.animationDelay = (i * -2) + 's';
            layer.appendChild(wave);
        }
    } else if (env === 'sky') {
        // Clouds
        for (let i = 0; i < 4; i++) {
            const cloud = document.createElement('div');
            cloud.textContent = '☁️';
            cloud.style.position = 'absolute';
            cloud.style.fontSize = '100px';
            cloud.style.opacity = '0.4';
            cloud.style.left = (i * 25) + '%';
            cloud.style.top = (5 + Math.random() * 15) + '%';
            layer.appendChild(cloud);
        }
    } else if (env === 'lava') {
        // Lava bubbles
        for (let i = 0; i < 15; i++) {
            const bubble = document.createElement('div');
            bubble.style.position = 'absolute';
            bubble.style.width = '20px';
            bubble.style.height = '20px';
            bubble.style.borderRadius = '50%';
            bubble.style.background = 'rgba(255, 69, 0, 0.5)';
            bubble.style.left = Math.random() * 100 + '%';
            bubble.style.bottom = '-20px';
            bubble.style.animation = `float ${2 + Math.random() * 3}s ease-in infinite`;
            bubble.style.animationDelay = (Math.random() * 5) + 's';
            layer.appendChild(bubble);
        }
    } else if (env === 'ice') {
        // Icicles
        for (let i = 0; i < 8; i++) {
            const icicle = document.createElement('div');
            icicle.textContent = '❄️';
            icicle.style.position = 'absolute';
            icicle.style.fontSize = '60px';
            icicle.style.opacity = '0.6';
            icicle.style.left = (i * 12.5) + '%';
            icicle.style.top = '-10px';
            icicle.style.animation = 'sway 3s ease-in-out infinite';
            icicle.style.animationDelay = (i * 0.3) + 's';
            layer.appendChild(icicle);
        }
    } else if (env === 'thunder') {
        // Lightning bolts - will flash
    } else if (env === 'cosmic') {
        // Stars
        for (let i = 0; i < 20; i++) {
            const star = document.createElement('div');
            star.textContent = '⭐';
            star.style.position = 'absolute';
            star.style.fontSize = '40px';
            star.style.opacity = Math.random() * 0.6 + 0.2;
            star.style.left = Math.random() * 100 + '%';
            star.style.top = Math.random() * 100 + '%';
            star.style.animation = `twinkle ${2 + Math.random() * 2}s ease-in-out infinite`;
            layer.appendChild(star);
        }
    }

    container.appendChild(layer);
}

/**
 * Create battle HUD (health bars, names, log)
 */
function createBattleHUD(container, story, battleState) {
    const hud = document.createElement('div');
    hud.style.position = 'absolute';
    hud.style.width = '100%';
    hud.style.padding = '20px';
    hud.style.color = '#fff';
    hud.style.fontSize = '14px';
    hud.style.fontFamily = 'Arial, sans-serif';
    hud.style.pointerEvents = 'none';

    // Hero health bar
    const heroBar = document.createElement('div');
    heroBar.id = 'hero-health-bar';
    heroBar.style.position = 'absolute';
    heroBar.style.top = '20px';
    heroBar.style.left = '20px';
    heroBar.style.width = '200px';
    heroBar.innerHTML = `
    <div style="color: #4ade80; font-weight: bold; margin-bottom: 5px;">${story.hero.name}</div>
    <div style="background: rgba(0,0,0,0.5); border: 2px solid #4ade80; height: 20px; border-radius: 4px; overflow: hidden;">
      <div id="hero-health" style="background: linear-gradient(90deg, #4ade80, #22c55e); height: 100%; width: 100%; transition: width 0.3s;"></div>
    </div>
    <div style="margin-top: 5px; color: #cbd5e1; font-size: 12px;">HP: <span id="hero-hp">200</span>/200</div>
  `;
    hud.appendChild(heroBar);

    // Monster health bar
    const monsterBar = document.createElement('div');
    monsterBar.id = 'monster-health-bar';
    monsterBar.style.position = 'absolute';
    monsterBar.style.top = '20px';
    monsterBar.style.right = '20px';
    monsterBar.style.width = '200px';
    monsterBar.style.textAlign = 'right';
    monsterBar.innerHTML = `
    <div style="color: #ef4444; font-weight: bold; margin-bottom: 5px;">${story.monster.name}</div>
    <div style="background: rgba(0,0,0,0.5); border: 2px solid #ef4444; height: 20px; border-radius: 4px; overflow: hidden;">
      <div id="monster-health" style="background: linear-gradient(90deg, #ef4444, #dc2626); height: 100%; width: 100%; transition: width 0.3s;"></div>
    </div>
    <div style="margin-top: 5px; color: #cbd5e1; font-size: 12px;">HP: <span id="monster-hp">${story.monster.health}</span>/${story.monster.health}</div>
  `;
    hud.appendChild(monsterBar);

    // Battle log
    const log = document.createElement('div');
    log.id = 'battle-log';
    log.style.position = 'absolute';
    log.style.bottom = '20px';
    log.style.left = '20px';
    log.style.width = '400px';
    log.style.maxHeight = '150px';
    log.style.background = 'rgba(0, 0, 0, 0.7)';
    log.style.border = '2px solid #3b82f6';
    log.style.borderRadius = '6px';
    log.style.padding = '10px';
    log.style.fontSize = '12px';
    log.style.color = '#cbd5e1';
    log.style.overflowY = 'auto';
    log.style.fontFamily = 'monospace';
    hud.appendChild(log);

    container.appendChild(hud);
    return hud;
}

/**
 * Create hero character with animations
 */
function createHeroCharacter(container, hero, battleState) {
    const heroEl = document.createElement('div');
    heroEl.style.position = 'absolute';
    heroEl.style.left = '15%';
    heroEl.style.top = '50%';
    heroEl.style.transform = 'translateY(-50%)';
    heroEl.style.fontSize = '120px';
    heroEl.style.filter = 'drop-shadow(0 0 20px rgba(74, 222, 128, 0.8))';
    heroEl.style.zIndex = '10';
    heroEl.textContent = hero.char;
    container.appendChild(heroEl);
    return heroEl;
}

/**
 * Create monster character with animations
 */
function createMonsterCharacter(container, monster, battleState) {
    const monsterEl = document.createElement('div');
    monsterEl.style.position = 'absolute';
    monsterEl.style.right = '15%';
    monsterEl.style.top = '50%';
    monsterEl.style.transform = 'translateY(-50%)';
    monsterEl.style.fontSize = '120px';
    monsterEl.style.filter = 'drop-shadow(0 0 20px rgba(239, 68, 68, 0.8))';
    monsterEl.style.zIndex = '10';
    monsterEl.textContent = monster.char;
    container.appendChild(monsterEl);
    return monsterEl;
}

/**
 * Perform hero attack with sword swing
 */
function performHeroAttack(heroEl, monsterEl, battleState, story, effectsLayer, hud) {
    const damage = 25 + Math.random() * 20;

    // Sword swing animation
    heroEl.style.animation = 'heroSwordSwing 0.6s ease-out';

    // Create sword slash effect
    createSlashEffect(effectsLayer, 'hero');

    // Create damage number
    const damageNum = document.createElement('div');
    damageNum.textContent = `-${Math.floor(damage)}`;
    damageNum.style.position = 'absolute';
    damageNum.style.right = '20%';
    damageNum.style.top = '40%';
    damageNum.style.fontSize = '48px';
    damageNum.style.fontWeight = 'bold';
    damageNum.style.color = '#ef4444';
    damageNum.style.textShadow = '0 0 10px rgba(239, 68, 68, 1)';
    damageNum.style.animation = 'damageFloat 1.5s ease-out forwards';
    damageNum.style.pointerEvents = 'none';
    effectsLayer.appendChild(damageNum);

    // Monster hit reaction
    monsterEl.style.animation = 'monsterHitReact 0.4s ease-out';

    // Update health
    battleState.monsterHealth -= damage;
    updateHealthBar('monster', battleState.monsterHealth, story.monster.health);

    // Log message
    const attackType = Math.random() > 0.7 ? 'CRITICAL HIT!' : 'Attack!';
    displayBattleMessage(hud, `${story.hero.name}: ${attackType}`, 'attack');
}

/**
 * Perform monster attack
 */
function performMonsterAttack(heroEl, monsterEl, battleState, story, effectsLayer, hud) {
    const damage = 15 + Math.random() * 25;

    // Monster attack animation
    monsterEl.style.animation = 'monsterAttack 0.6s ease-out';

    // Create monster attack effect
    createSlashEffect(effectsLayer, 'monster');

    // Hero hit reaction
    heroEl.style.animation = 'heroHitReact 0.4s ease-out';

    // Create damage number
    const damageNum = document.createElement('div');
    damageNum.textContent = `-${Math.floor(damage)}`;
    damageNum.style.position = 'absolute';
    damageNum.style.left = '20%';
    damageNum.style.top = '40%';
    damageNum.style.fontSize = '48px';
    damageNum.style.fontWeight = 'bold';
    damageNum.style.color = '#fbbf24';
    damageNum.style.textShadow = '0 0 10px rgba(251, 191, 36, 1)';
    damageNum.style.animation = 'damageFloat 1.5s ease-out forwards';
    damageNum.style.pointerEvents = 'none';
    effectsLayer.appendChild(damageNum);

    // Update health
    battleState.heroHealth -= damage;
    updateHealthBar('hero', battleState.heroHealth, 200);

    displayBattleMessage(hud, `${story.monster.name}: Counterattack!`, 'enemy-attack');
}

/**
 * Create slash effect
 */
function createSlashEffect(layer, direction) {
    const slash = document.createElement('div');
    slash.style.position = 'absolute';
    slash.style.fontSize = '80px';
    slash.textContent = direction === 'hero' ? '⚔️' : '🔥';
    slash.style.pointerEvents = 'none';

    if (direction === 'hero') {
        slash.style.left = '50%';
        slash.style.top = '45%';
        slash.style.animation = 'slashAttack 0.5s ease-out forwards';
    } else {
        slash.style.right = '50%';
        slash.style.top = '45%';
        slash.style.animation = 'slashAttackReverse 0.5s ease-out forwards';
    }

    layer.appendChild(slash);
    setTimeout(() => slash.remove(), 600);
}

/**
 * Update health bar display
 */
function updateHealthBar(character, current, max) {
    const percent = Math.max(0, (current / max) * 100);
    const healthBar = document.getElementById(`${character}-health`);
    const healthText = document.getElementById(`${character}-hp`);

    if (healthBar) healthBar.style.width = percent + '%';
    if (healthText) healthText.textContent = Math.max(0, Math.floor(current));
}

/**
 * Display battle message in log
 */
function displayBattleMessage(hud, message, type) {
    const log = document.getElementById('battle-log');
    if (log) {
        const msg = document.createElement('div');
        msg.textContent = '> ' + message;
        msg.style.color = type === 'attack' ? '#4ade80' : type === 'enemy-attack' ? '#fbbf24' : '#3b82f6';
        msg.style.marginBottom = '4px';
        msg.style.animation = 'slideIn 0.3s ease-out';
        log.appendChild(msg);
        log.scrollTop = log.scrollHeight;

        // Limit log lines
        if (log.children.length > 8) {
            log.removeChild(log.firstChild);
        }
    }
}

/**
 * Play victory sequence
 */
function playVictorySequence(container, heroEl, monsterEl, story, battleState, hud) {
    displayBattleMessage(hud, `${story.hero.name} WINS!`, 'victory');

    // Monster disappears
    monsterEl.style.animation = 'monsterDefeated 1s ease-out forwards';

    // Hero victory pose
    heroEl.style.animation = 'heroVictoryPose 2s ease-out';

    // Explosion effect
    createExplosionEffects(container);

    // Victory text
    const victoryText = document.createElement('div');
    victoryText.textContent = '⚡ VICTORY ⚡';
    victoryText.style.position = 'absolute';
    victoryText.style.top = '50%';
    victoryText.style.left = '50%';
    victoryText.style.transform = 'translate(-50%, -50%)';
    victoryText.style.fontSize = '80px';
    victoryText.style.fontWeight = 'bold';
    victoryText.style.color = '#fbbf24';
    victoryText.style.textShadow = '0 0 30px rgba(251, 191, 36, 1), 0 0 60px rgba(245, 158, 11, 0.8)';
    victoryText.style.animation = 'victoryAppear 1.5s cubic-bezier(0.34, 1.56, 0.64, 1) forwards';
    victoryText.style.pointerEvents = 'none';
    container.appendChild(victoryText);

    // Particle celebration
    for (let i = 0; i < 50; i++) {
        setTimeout(() => {
            createCelebrationParticle(container);
        }, i * 50);
    }
}

/**
 * Create explosion effects
 */
function createExplosionEffects(container) {
    for (let i = 0; i < 8; i++) {
        const explosion = document.createElement('div');
        explosion.textContent = '💥';
        explosion.style.position = 'absolute';
        explosion.style.right = '20%';
        explosion.style.top = '50%';
        explosion.style.fontSize = '60px';
        explosion.style.pointerEvents = 'none';
        explosion.style.animation = `explosionBurst 0.8s ease-out forwards`;
        explosion.style.animationDelay = (i * 0.1) + 's';
        const angle = (i / 8) * Math.PI * 2;
        explosion.style.setProperty('--tx', Math.cos(angle) * 200 + 'px');
        explosion.style.setProperty('--ty', Math.sin(angle) * 200 + 'px');
        container.appendChild(explosion);
    }
}

/**
 * Create celebration particle
 */
function createCelebrationParticle(container) {
    const particles = ['⭐', '✨', '💫', '🎆', '🌟'];
    const particle = document.createElement('div');
    particle.textContent = particles[Math.floor(Math.random() * particles.length)];
    particle.style.position = 'absolute';
    particle.style.left = '50%';
    particle.style.top = '50%';
    particle.style.fontSize = '30px';
    particle.style.pointerEvents = 'none';
    particle.style.animation = `celebration 3s ease-out forwards`;

    const tx = (Math.random() - 0.5) * 400;
    const ty = (Math.random() - 0.5) * 400;
    particle.style.setProperty('--tx', tx + 'px');
    particle.style.setProperty('--ty', ty + 'px');

    container.appendChild(particle);
    setTimeout(() => particle.remove(), 3500);
}

/**
 * Setup animation preference listeners
 */
function setupAnimationPreference() {
    const btn = document.getElementById('animation-pref-btn');
    if (btn) {
        btn.addEventListener('click', () => {
            document.getElementById('animation-pref-modal').style.display = 'block';
            updateAnimationButtonStates();
        });
    }
}

/**
 * Set animation mode and save preference
 */
function setAnimationMode(mode) {
    animationMode = mode;
    localStorage.setItem('animationMode', mode);
    updateAnimationButtonStates();
    closeAnimationPrefModal();

    const btn = document.getElementById('animation-pref-btn');
    if (btn) {
        if (mode === 'long') {
            btn.classList.add('active');
            btn.title = '🎬 Epic Battle Animations (ON)';
        } else {
            btn.classList.remove('active');
            btn.title = '⚡ Short Animations (ON)';
        }
    }
}

/**
 * Update animation button states
 */
function updateAnimationButtonStates() {
    const shortBtn = document.getElementById('short-anim-btn');
    const longBtn = document.getElementById('long-anim-btn');

    if (shortBtn && longBtn) {
        if (animationMode === 'short') {
            shortBtn.style.borderColor = '#3b82f6';
            shortBtn.style.backgroundColor = 'rgba(59, 130, 246, 0.2)';
            longBtn.style.borderColor = 'transparent';
            longBtn.style.backgroundColor = '#1e293b';
        } else {
            longBtn.style.borderColor = '#3b82f6';
            longBtn.style.backgroundColor = 'rgba(59, 130, 246, 0.2)';
            shortBtn.style.borderColor = 'transparent';
            shortBtn.style.backgroundColor = '#1e293b';
        }
    }
}

/**
 * Close animation preference modal
 */
function closeAnimationPrefModal() {
    document.getElementById('animation-pref-modal').style.display = 'none';
}

// Add fade out animation
const style = document.createElement('style');
style.textContent = `
  @keyframes fadeOut {
    from { opacity: 1; }
    to { opacity: 0; }
  }
`;
document.head.appendChild(style);

function initializeApp() {
    if (window.logger) window.logger.debug("Initializing App...");
    createAuroraOverlay();
    setupAuthListeners();
    setupNavigationListeners();
    setupLandingPageListeners();
    setupCourseEditorListeners();
    setupContentEditorListeners();
    setupMessageListeners();
    setupQuizModalListeners();
    setupPhetModalListeners();
    setupLatexHelpModalListeners();
    setupCourseSearchListeners();
    setupCourseSortListener();
    setupAnimationPreference();
    setupCourseNestingListeners();
    setupStudyCoachListeners();
    exposeAiEditorHelpBridge();
    if (typeof setupAiEditorHelp === "function") {
        setupAiEditorHelp();
    }

    // Prefer restored localStorage token; cookie also keeps httpOnly sessions alive
    if (!authToken) {
        const saved = localStorage.getItem("token");
        if (saved) authToken = saved;
    }
    if (document.cookie.includes("token=") || authToken || (typeof validateAuthToken === "function" && validateAuthToken())) {
        fetchUserProfile();
    } else {
        showLandingPage();
    }
}

/**
 * Bridge script.js locals to window for ai-editor-help.js skills.
 */
function exposeAiEditorHelpBridge() {
    window.API_BASE_URL = API_BASE_URL;
    window.escapeHtml = escapeHtml;
    window.insertSimulatorBlock = insertSimulatorBlock;
    window.insertQuizPlaceholder = insertQuizPlaceholder;
    window.loadCourseQuestions = loadCourseQuestions;
    window.saveCurrentPageContent = saveCurrentPageContent;
    window.openQuizModal = openQuizModal;

    try {
        Object.defineProperty(window, "authToken", {
            get() { return authToken; },
            set(v) { authToken = v; },
            configurable: true
        });
        Object.defineProperty(window, "currentEditingCourseId", {
            get() { return currentEditingCourseId; },
            set(v) { currentEditingCourseId = v; },
            configurable: true
        });
        Object.defineProperty(window, "courseBlocks", {
            get() { return courseBlocks; },
            set(v) { courseBlocks = v; },
            configurable: true
        });
        Object.defineProperty(window, "courseQuestions", {
            get() { return courseQuestions; },
            set(v) { courseQuestions = v; },
            configurable: true
        });
        Object.defineProperty(window, "coursePages", {
            get() { return coursePages; },
            set(v) { coursePages = v; },
            configurable: true
        });
    } catch (e) {
        // Fallbacks if properties already defined non-configurable
        window.authToken = authToken;
        window.currentEditingCourseId = currentEditingCourseId;
        window.courseBlocks = courseBlocks;
        window.courseQuestions = courseQuestions;
        window.coursePages = coursePages;
    }
}

// Setup course nesting system event listeners
function setupCourseNestingListeners() {
    // Course type toggle
    setupCourseTypeToggle();
    
    // Unit management panel
    const backToEditorBtn = document.getElementById("back-to-course-editor");
    if (backToEditorBtn) {
        backToEditorBtn.addEventListener("click", backToCourseEditor);
    }
    
    const addUnitBtn = document.getElementById("add-unit-btn");
    if (addUnitBtn) {
        addUnitBtn.addEventListener("click", showUnitSelectionModal);
    }
}

function setStudyCoachVisible(visible) {
    const root = document.getElementById("study-coach-root");
    if (root) root.style.display = visible ? "block" : "none";
}

function setupStudyCoachListeners() {
    const fab = document.getElementById("study-coach-fab");
    const panel = document.getElementById("study-coach-panel");
    const closeBtn = document.getElementById("study-coach-close");
    const sendBtn = document.getElementById("study-coach-send");
    const input = document.getElementById("study-coach-input");

    if (!fab || !panel) return;

    fab.addEventListener("click", () => {
        const open = panel.style.display === "flex";
        if (open) {
            panel.style.display = "none";
        } else {
            panel.style.display = "flex";
            panel.style.flexDirection = "column";
            loadStudyCoachHistory();
            if (input) input.focus();
        }
    });

    if (closeBtn) {
        closeBtn.addEventListener("click", () => {
            panel.style.display = "none";
        });
    }

    if (sendBtn) {
        sendBtn.addEventListener("click", () => sendStudyCoachMessage());
    }
    if (input) {
        input.addEventListener("keydown", (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendStudyCoachMessage();
            }
        });
    }
}

function typesetStudyCoachBubble(el) {
    if (!el) return;
    const eng = window.VeelearnWidgetEngine;
    if (eng && typeof eng.typesetMath === "function") {
        eng.typesetMath(el);
        return;
    }
    if (window.MathJax && typeof window.MathJax.typesetPromise === "function") {
        window.MathJax.typesetPromise([el]).catch(() => {});
    }
}

async function ensureStudyCoachWidgetEngine() {
    if (window.VeelearnWidgetEngine) return window.VeelearnWidgetEngine;
    if (typeof window.__veelearnLoadHeavy === "function") {
        await window.__veelearnLoadHeavy("widgets");
    }
    return window.VeelearnWidgetEngine;
}

async function mountStudyCoachWidgets(host, widgets, opts) {
    if (!host || !widgets || !widgets.length) return;
    const eng = await ensureStudyCoachWidgetEngine();
    if (!eng || typeof eng.mountWidgets !== "function") return;
    await eng.mountWidgets(host, widgets, opts || {});
}

function removeStudyCoachTypingIndicator() {
    document.getElementById("study-coach-typing")?.remove();
}

function showStudyCoachTypingIndicator() {
    const box = document.getElementById("study-coach-messages");
    if (!box) return;
    removeStudyCoachTypingIndicator();
    const wrap = document.createElement("div");
    wrap.id = "study-coach-typing";
    wrap.className = "study-coach-bubble";
    wrap.classList.add("study-coach-coach");
    wrap.setAttribute("aria-busy", "true");
    wrap.setAttribute("aria-live", "polite");
    wrap.style.marginBottom = "10px";
    wrap.style.padding = "8px 10px";
    wrap.style.borderRadius = "8px";
    wrap.style.background = "rgba(255,255,255,0.1)";
    wrap.style.marginRight = "12px";
    wrap.innerHTML =
        '<strong>Coach</strong><div class="study-coach-typing-dots" aria-hidden="true"><span>.</span><span>.</span><span>.</span></div>';
    box.appendChild(wrap);
    box.scrollTop = box.scrollHeight;
}

function appendStudyCoachBubble(role, text, widgets, mountOpts) {
    const box = document.getElementById("study-coach-messages");
    if (!box) return null;
    const wrap = document.createElement("div");
    wrap.className = "study-coach-bubble";
    wrap.style.marginBottom = "10px";
    wrap.style.padding = "8px 10px";
    wrap.style.borderRadius = "8px";
    wrap.style.whiteSpace = "pre-wrap";
    if (role === "user") {
        wrap.classList.add("study-coach-user");
        wrap.style.background = "rgba(118, 139, 255, 0.35)";
        wrap.style.marginLeft = "12px";
        wrap.innerHTML = `<strong>You</strong><div class="study-coach-body">${escapeHtml(text)}</div>`;
    } else {
        wrap.classList.add("study-coach-coach");
        wrap.style.background = "rgba(255,255,255,0.1)";
        wrap.style.marginRight = "12px";
        wrap.innerHTML = `<strong>Coach</strong><div class="study-coach-body">${escapeHtml(text)}</div>`;
    }
    const widgetHost = document.createElement("div");
    widgetHost.className = "vl-widget-host";
    wrap.appendChild(widgetHost);
    box.appendChild(wrap);
    box.scrollTop = box.scrollHeight;
    typesetStudyCoachBubble(wrap.querySelector(".study-coach-body") || wrap);
    if (role !== "user" && widgets && widgets.length) {
        mountStudyCoachWidgets(widgetHost, widgets, mountOpts).then(() => {
            box.scrollTop = box.scrollHeight;
        });
    }
    return wrap;
}

function renderStudyCoachRecommendations(recs) {
    const el = document.getElementById("study-coach-recs");
    if (!el) return;
    el.innerHTML = "";
    if (!recs || !recs.length) return;
    const title = document.createElement("div");
    title.textContent = "Suggested courses:";
    title.style.fontWeight = "600";
    title.style.marginBottom = "6px";
    el.appendChild(title);
    recs.forEach((r) => {
        const row = document.createElement("div");
        row.style.marginBottom = "6px";
        const link = document.createElement("button");
        link.type = "button";
        link.textContent = r.title || `Course ${r.courseId}`;
        link.style.cssText =
            "background:none;border:none;cursor:pointer;text-align:left;padding:0;font-size:13px;text-decoration:underline;";
        link.addEventListener("click", () => {
            if (typeof viewCourse === "function") viewCourse(r.courseId);
            document.getElementById("study-coach-panel").style.display = "none";
        });
        row.appendChild(link);
        if (r.reason) {
            const why = document.createElement("div");
            why.textContent = r.reason;
            why.style.fontSize = "12px";
            why.style.marginTop = "2px";
            why.style.opacity = "0.92";
            row.appendChild(why);
        }
        el.appendChild(row);
    });
}

async function loadStudyCoachHistory() {
    const box = document.getElementById("study-coach-messages");
    if (!box || !currentUser) return;
    removeStudyCoachTypingIndicator();
    try {
        const res = await fetch(`${API_BASE_URL}/api/ai/tutor/history?limit=30`, {
            credentials: "include",
            headers: { Authorization: `Bearer ${authToken || ""}` }
        });
        const data = await res.json();
        if (!data.success || !Array.isArray(data.data)) return;
        box.innerHTML = "";
        data.data.forEach((row) => {
            if (row.role === "user" || row.role === "assistant") {
                appendStudyCoachBubble(row.role, row.content || "", row.widgets || [], {
                    skipDrawing: true
                });
            }
        });
    } catch (e) {
        console.warn("Study coach history:", e);
    }
}

async function sendStudyCoachMessage() {
    const input = document.getElementById("study-coach-input");
    const sendBtn = document.getElementById("study-coach-send");
    if (!input || !currentUser) return;
    const text = input.value.trim();
    if (!text) return;

    input.value = "";
    appendStudyCoachBubble("user", text);
    const recsEl = document.getElementById("study-coach-recs");
    if (recsEl) recsEl.innerHTML = "";

    const payload = { message: text };
    if (currentViewingCourseId != null) {
        payload.courseId = currentViewingCourseId;
    }

    if (sendBtn) sendBtn.disabled = true;
    if (input) input.disabled = true;
    showStudyCoachTypingIndicator();
    try {
        const res = await fetch(`${API_BASE_URL}/api/ai/tutor/chat`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${authToken || ""}`
            },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        removeStudyCoachTypingIndicator();
        if (!data.success) {
            appendStudyCoachBubble("assistant", data.message || "Something went wrong. Try again later.");
            return;
        }
        const reply = data.data?.reply || "";
        appendStudyCoachBubble("assistant", reply, data.data?.widgets || []);
        renderStudyCoachRecommendations(data.data?.recommendations);
    } catch (e) {
        console.error(e);
        removeStudyCoachTypingIndicator();
        appendStudyCoachBubble("assistant", "Could not reach the study coach. Check your connection and try again.");
    } finally {
        if (sendBtn) sendBtn.disabled = false;
        if (input) input.disabled = false;
    }
}

/**
 * Robust HTML escaping utility to prevent XSS
 */
function escapeHtml(unsafe) {
    if (unsafe === null || unsafe === undefined) return "";
    return String(unsafe)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function getYoutubeEmbedUrl(url) {
    if (!url) return null;
    let videoId = null;
    try {
        if (url.includes('youtube.com/watch')) {
            videoId = new URL(url).searchParams.get('v');
        } else if (url.includes('youtu.be/')) {
            videoId = url.split('youtu.be/')[1].split(/[?#]/)[0];
        } else if (url.includes('youtube.com/embed/')) {
            return url;
        }
    } catch (e) {
        console.warn('Invalid YouTube URL:', url);
    }
    return videoId ? `https://www.youtube.com/embed/${videoId}` : null;
}

function setupMessageListeners() {
    window.addEventListener("message", (e) => {
        if (e.data.type === "closeBlockSimulator") {
            // If the course editor is open, stay there — the user was editing a
            // simulator inside a course and closing the studio shouldn't lose the course.
            const editorSection = document.getElementById("course-editor-section");
            const inCourseEditor = editorSection && getComputedStyle(editorSection).display !== "none";
            if (!inCourseEditor) showDashboard();
        } else if (e.data.type === "save-simulator") {
            // Receive simulator data from popup (scratch-studio / legacy studio)
            const { data } = e.data;
            if (window.logger) {
                window.logger.debug('💾 Received save-simulator message');
                window.logger.debug('   currentEditingSimulatorBlockId:', currentEditingSimulatorBlockId);
            }

            // Use the stored currentEditingSimulatorBlockId, falling back to the id sent by the studio
            const targetBlockId = currentEditingSimulatorBlockId || Number(e.data.courseBlockId) || e.data.courseBlockId;
            if (targetBlockId && data) {
                const blockIndex = courseBlocks.findIndex(b => b.id === targetBlockId);
                if (blockIndex !== -1) {
                    if (isScratchSimulatorData(data)) {
                        courseBlocks[blockIndex].data = {
                            format: 'veelearn-scratch-1',
                            project: data.project || data.blocks || data,
                            blocks: data.project || data.blocks || data,
                            connections: [],
                            sim_type: 'scratch'
                        };
                    } else {
                        courseBlocks[blockIndex].data = {
                            blocks: data.blocks || [],
                            connections: data.connections || []
                        };
                    }
                    if (window.logger) window.logger.debug('✅ Saved to block:', targetBlockId, 'at index:', blockIndex);
                } else {
                    console.warn('⚠️ Block not found:', targetBlockId);
                }
            }
        } else if (e.data.type === "saveBlockSimulator") {
            // Legacy support - receive simulator data
            const { courseBlockId, blocks, connections } = e.data;
            if (window.logger) window.logger.debug('💾 Saving simulator data:', courseBlockId, 'Blocks:', blocks?.length, 'Connections:', connections?.length);

            const blockIndex = courseBlocks.findIndex(b => b.id === courseBlockId);
            if (blockIndex !== -1) {
                courseBlocks[blockIndex].data = {
                    blocks: blocks || [],
                    connections: connections || []
                };
                if (window.logger) window.logger.debug('✅ Simulator data saved to courseBlocks[' + blockIndex + ']');
            } else {
                console.warn('⚠️ Block not found:', courseBlockId);
            }
        } else if (e.data.type === "saveVisualSimulator") {
            // Receive visual simulator code
            const { courseBlockId, code, variables } = e.data;
            if (window.logger) window.logger.debug('💾 Saving visual simulator:', courseBlockId);

            const blockIndex = courseBlocks.findIndex(b => b.id === courseBlockId);
            if (blockIndex !== -1) {
                courseBlocks[blockIndex].data = {
                    code: code || "",
                    variables: variables || {}
                };
                if (window.logger) window.logger.debug('✅ Visual simulator saved');
            }
        }
    });
}

// ===== AUTHENTICATION =====
function setupAuthListeners() {
    const loginForm = document.querySelector("#login-form form");
    const registerForm = document.querySelector("#register-form form");
    const logoutButton = document.getElementById("logout-button");
    const showRegister = document.getElementById("show-register");
    const showLogin = document.getElementById("show-login");

    if (loginForm) {
        loginForm.addEventListener("submit", (e) => {
            e.preventDefault();
            handleLogin();
        });
    }

    if (registerForm) {
        registerForm.addEventListener("submit", (e) => {
            e.preventDefault();
            handleRegister();
        });
    }

    if (logoutButton) {
        logoutButton.addEventListener("click", handleLogout);
    }

    if (showRegister) {
        showRegister.addEventListener("click", (e) => {
            e.preventDefault();
            document.getElementById("login-form").style.display = "none";
            document.getElementById("register-form").style.display = "block";
            document.getElementById("forgot-password-form").style.display = "none";
        });
    }

    if (showLogin) {
        showLogin.addEventListener("click", (e) => {
            e.preventDefault();
            document.getElementById("login-form").style.display = "block";
            document.getElementById("register-form").style.display = "none";
            document.getElementById("forgot-password-form").style.display = "none";
        });
    }

    // Forgot Password listeners
    const showForgotPassword = document.getElementById("show-forgot-password");
    if (showForgotPassword) {
        showForgotPassword.addEventListener("click", (e) => {
            e.preventDefault();
            document.getElementById("login-form").style.display = "none";
            document.getElementById("register-form").style.display = "none";
            document.getElementById("forgot-password-form").style.display = "block";
            // Reset to step 1
            document.getElementById("forgot-step-1").style.display = "block";
            document.getElementById("forgot-step-2").style.display = "none";
            document.getElementById("forgot-error-message").textContent = "";
            document.getElementById("forgot-success-message").textContent = "";
        });
    }

    const showLoginFromForgot = document.getElementById("show-login-from-forgot");
    if (showLoginFromForgot) {
        showLoginFromForgot.addEventListener("click", (e) => {
            e.preventDefault();
            document.getElementById("forgot-password-form").style.display = "none";
            document.getElementById("login-form").style.display = "block";
        });
    }

    const forgotEmailForm = document.getElementById("forgot-email-form");
    if (forgotEmailForm) {
        forgotEmailForm.addEventListener("submit", (e) => {
            e.preventDefault();
            handleForgotPassword();
        });
    }

    const forgotResetForm = document.getElementById("forgot-reset-form");
    if (forgotResetForm) {
        forgotResetForm.addEventListener("submit", (e) => {
            e.preventDefault();
            handleResetPassword();
        });
    }
}

function handleForgotPassword() {
    const email = document.getElementById("forgot-email").value;
    const errorMsg = document.getElementById("forgot-error-message");
    const successMsg = document.getElementById("forgot-success-message");
    const submitBtn = document.querySelector("#forgot-email-form button[type='submit']");

    errorMsg.textContent = "";
    successMsg.textContent = "";

    if (!email) {
        errorMsg.textContent = "Please enter your email address";
        return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = "Sending...";

    fetch(`${API_BASE_URL}/api/forgot-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
        credentials: "include"
    })
        .then((res) => res.json())
        .then((data) => {
            submitBtn.disabled = false;
            submitBtn.textContent = "Send Reset Code";

            if (data.success) {
                successMsg.textContent = data.message;
                // Move to step 2
                document.getElementById("forgot-step-1").style.display = "none";
                document.getElementById("forgot-step-2").style.display = "block";
                successMsg.textContent = "Code sent! Check your email (including spam folder).";
            } else {
                errorMsg.textContent = data.message || "Something went wrong";
            }
        })
        .catch((err) => {
            submitBtn.disabled = false;
            submitBtn.textContent = "Send Reset Code";
            console.error("Forgot password error:", err);
            errorMsg.textContent = "Network error. Please try again.";
        });
}

function handleResetPassword() {
    const email = document.getElementById("forgot-email").value;
    const code = document.getElementById("reset-code").value;
    const newPassword = document.getElementById("reset-new-password").value;
    const errorMsg = document.getElementById("forgot-error-message");
    const successMsg = document.getElementById("forgot-success-message");
    const submitBtn = document.querySelector("#forgot-reset-form button[type='submit']");

    errorMsg.textContent = "";
    successMsg.textContent = "";

    if (!code || !newPassword) {
        errorMsg.textContent = "Please enter the code and a new password";
        return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = "Resetting...";

    fetch(`${API_BASE_URL}/api/reset-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, code, newPassword }),
        credentials: "include"
    })
        .then((res) => res.json())
        .then((data) => {
            submitBtn.disabled = false;
            submitBtn.textContent = "Reset Password";

            if (data.success) {
                successMsg.textContent = data.message;
                // After 2 seconds, go back to login
                setTimeout(() => {
                    document.getElementById("forgot-password-form").style.display = "none";
                    document.getElementById("login-form").style.display = "block";
                    // Clear all forgot password fields
                    document.getElementById("forgot-email").value = "";
                    document.getElementById("reset-code").value = "";
                    document.getElementById("reset-new-password").value = "";
                    document.getElementById("forgot-error-message").textContent = "";
                    document.getElementById("forgot-success-message").textContent = "";
                    document.getElementById("forgot-step-1").style.display = "block";
                    document.getElementById("forgot-step-2").style.display = "none";
                }, 2000);
            } else {
                errorMsg.textContent = data.message || "Reset failed";
            }
        })
        .catch((err) => {
            submitBtn.disabled = false;
            submitBtn.textContent = "Reset Password";
            console.error("Reset password error:", err);
            errorMsg.textContent = "Network error. Please try again.";
        });
}

function handleLogin() {
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;
    const errorMessage = document.getElementById("login-error-message");

    if (!email || !password) {
        errorMessage.textContent = "Please fill in all fields";
        return;
    }

    handleWithServerLoading(async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
                credentials: "include"
            });
            
            const data = await response.json();
            
            if (data.success) {
                authToken = data.data.token;
                localStorage.setItem("token", authToken); // Store for API calls like 'like' feature
                // Backend returns: {token, user: {id, email, role, shells}}
                const userData = data.data.user || data.data;
                currentUser = {
                    id: userData.id,
                    email: userData.email,
                    role: userData.role,
                    shells: userData.shells || 0
                };
                try { window.currentUser = currentUser; } catch (_) { /* ignore */ }
                if (window.logger) window.logger.debug("Login successful, currentUser set:", currentUser);
                // INSTANT: Show dashboard immediately without needing a reload
                showDashboard();
                // Setup teacher/student UI right away after login
                setupTeacherStudentListeners();
                // Also load initial data in background
                setTimeout(() => {
                    if (currentUser?.role === "superadmin") {
                        loadAllUsers();
                        loadPendingCourses();
                        loadUserCourses();
                        loadAvailableCourses();
                    } else if (currentUser?.role === "admin") {
                        loadPendingCourses();
                        loadUserCourses();
                        loadAvailableCourses();
                    } else {
                        loadUserCourses();
                        loadAvailableCourses();
                    }
                }, 100);
            } else {
                errorMessage.textContent = data.message || "Login failed";
            }
        } catch (err) {
            console.error("Login error:", err);
            errorMessage.textContent = "Connection error";
        }
    }, 'login');
}

function handleRegister() {
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;
    const errorMsg = document.getElementById("register-error-message");

    if (!email || !password) {
        errorMsg.textContent = "All fields required";
        return;
    }

    // Wrap API call with server loading detection
    handleWithServerLoading(async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/register`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
                credentials: "include"
            });
            
            const data = await response.json();
            
            if (data.success) {
                alert("Registration successful! Please login.");
                document.getElementById("show-login").click();
            } else {
                errorMsg.textContent = data.message || "Registration failed";
            }
        } catch (err) {
            console.error("Register error:", err);
            errorMsg.textContent = "Connection error";
        }
    }, 'register');
}

function fetchUserProfile() {
    // Use cookie-based auth - authToken may be null on page reload but cookie is preserved
    const headers = {};
    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
    }

    fetch(`${API_BASE_URL}/api/users/profile`, {
        headers,
        credentials: "include"
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                currentUser = data.data;
                try { window.currentUser = currentUser; } catch (_) { /* ignore */ }
                // Sync authToken from cookie/response if available
                if (data.data.token) {
                    authToken = data.data.token;
                    localStorage.setItem("token", authToken);
                } else if (!authToken) {
                    const saved = localStorage.getItem("token");
                    if (saved) authToken = saved;
                }
                showDashboard();
                // Setup teacher/student UI after currentUser is loaded
                setupTeacherStudentListeners();
            } else {
                showLandingPage();
            }
        })
        .catch((err) => {
            console.error("Profile fetch error:", err);
            showLandingPage();
        });
}

function handleLogout() {
    logout();
}

function logout() {
    if (window.logger) window.logger.debug("LOGOUT CALLED - Token will be cleared!");

    // Call backend logout to clear cookie
    fetch(`${API_BASE_URL}/api/logout`, { method: 'POST', credentials: 'include' })
        .catch(err => console.warn('Logout API error:', err));

    authToken = null;
    currentUser = null;
    localStorage.removeItem("token"); // Clear from localStorage on logout
    if (window.LearnerShell?.hideLearnerShell) window.LearnerShell.hideLearnerShell();
    showAuthSection();
}

// ===== TOKEN VALIDATION =====
/**
 * Validate and check if token is still valid
 */
function validateAuthToken() {
    const token = localStorage.getItem("token");
    if (!token) {
        console.warn("⚠️ No token found in localStorage");
        return false;
    }

    // Check token format (JWT has 3 parts)
    try {
        const parts = token.split('.');
        if (parts.length !== 3) {
            console.error("Invalid token format - expected 3 parts, got", parts.length);
            return false;
        }

        // Decode payload
        const payload = JSON.parse(atob(parts[1]));
        const expiryTime = payload.exp * 1000;

        if (Date.now() > expiryTime) {
            console.warn("⚠️ Token expired at:", new Date(expiryTime).toISOString());
            return false;
        }

        if (window.logger) window.logger.debug("✅ Token is valid, expires at:", new Date(expiryTime).toISOString());
        return true;
    } catch (e) {
        console.error("❌ Invalid token format:", e.message);
        return false;
    }
}

// ===== TOKEN STORAGE (httpOnly Cookies) =====
// Note: Tokens are now stored in httpOnly cookies for security
// We no longer use localStorage for tokens (XSS protection)
// The backend automatically sends/validates token via cookie header

// ===== NAVIGATION =====
function setupNavigationListeners() {
    const dashboardLink = document.getElementById("dashboard-link");
    const homeLink = document.getElementById("home-link");
    const loginLink = document.getElementById("login-link");
    const registerLink = document.getElementById("register-link");

    if (dashboardLink) {
        dashboardLink.addEventListener("click", (e) => {
            e.preventDefault();
            showDashboard();
        });
    }

    if (homeLink) {
        homeLink.addEventListener("click", (e) => {
            e.preventDefault();
            if (currentUser) {
                showDashboard();
            } else {
                showLandingPage();
            }
        });
    }

    if (loginLink) {
        loginLink.addEventListener("click", (e) => {
            e.preventDefault();
            showAuthSection("login");
        });
    }

    if (registerLink) {
        registerLink.addEventListener("click", (e) => {
            e.preventDefault();
            showAuthSection("register");
        });
    }
}

function setupLandingPageListeners() {
    const getStartedBtn = document.getElementById("get-started-btn");
    const viewCoursesBtn = document.getElementById("view-courses-btn");

    if (getStartedBtn) {
        getStartedBtn.addEventListener("click", () => {
            showAuthSection("register");
        });
    }

    if (viewCoursesBtn) {
        viewCoursesBtn.addEventListener("click", () => {
            // Show available courses even if not logged in (they will prompt login to view)
            showLandingPage(); // For now keep on landing page or scroll down if I added courses there
            // Better: scroll to how it works or just show register
            showAuthSection("register");
        });
    }
}

// ===== COURSE CREATION TIMER =====
// Simple timer: counts seconds while user is actively typing in the editor.
// Goes idle (pauses) after 60s of no typing in the content editor / title / description.

function formatCreationTime(seconds) {
    if (!seconds || seconds <= 0) return '';
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    if (h > 0) return h + 'h ' + m + 'm';
    return m + 'm';
}

// ===== COURSE EDITOR LISTENERS =====
function setupCourseEditorListeners() {
    if (window.logger) window.logger.debug("Setting up course editor listeners...");
    const courseForm = document.getElementById("course-form");
    const cancelBtn = document.getElementById("cancel-course-edit");
    const backBtn = document.getElementById("back-to-dashboard");
    const saveDraftBtn = document.getElementById("save-draft-btn");
    const submitApprovalBtn = document.getElementById("submit-approval-btn");

    // Pagination Controls
    // Pagination Controls
    const addPageBtn = document.getElementById("add-page-btn");
    const prevPageBtn = document.getElementById("prev-page-btn");
    const nextPageBtn = document.getElementById("next-page-btn");
    const deletePageBtn = document.getElementById("delete-page-btn");

    if (addPageBtn) {
        if (window.logger) window.logger.debug("Add Page button found, attaching listener");
        addPageBtn.addEventListener("click", addNewPage);
    } else {
        console.error("Add Page button NOT found");
    }

    if (prevPageBtn) prevPageBtn.addEventListener("click", () => changePage(-1));
    if (nextPageBtn) nextPageBtn.addEventListener("click", () => changePage(1));
    if (deletePageBtn) deletePageBtn.addEventListener("click", deleteCurrentPage);

    // Click listener for placement mode
    const editor = document.getElementById("course-content-editor");
    if (editor) {
        editor.addEventListener("click", handleEditorClick);
    } else {
        console.error("Editor NOT found for click listener");
    }

    // Save draft button - DIRECTLY call saveCourse with "draft" action
    if (saveDraftBtn) {
        saveDraftBtn.addEventListener("click", (e) => {
            e.preventDefault();
            if (window.logger) window.logger.debug("📝 Save Draft button clicked - action: draft");
            saveCourse("draft");
        });
    }

    // Submit for approval button - DIRECTLY call saveCourse with "pending" action
    if (submitApprovalBtn) {
        submitApprovalBtn.addEventListener("click", (e) => {
            e.preventDefault();
            if (window.logger) window.logger.debug("📋 Submit for Approval button clicked - action: pending");
            saveCourse("pending");
        });
    }

    if (cancelBtn) {
        cancelBtn.addEventListener("click", showDashboard);
    }

    if (backBtn) {
        backBtn.addEventListener("click", showDashboard);
    }

    // Rich text editor toolbar
    setupRichTextEditor();
}

function setupRichTextEditor() {
    const buttons = document.querySelectorAll(".editor-toolbar button");
    const contentEditor = document.getElementById("course-content-editor");

    buttons.forEach((button) => {
        button.addEventListener("click", (e) => {
            e.preventDefault();
            const command = button.dataset.command;
            const id = button.id;

            if (id === "insert-math-simulator") {
                showMarketplaceSelector("math");
            } else if (id === "insert-coding-simulator") {
                showMarketplaceSelector("coding");
            } else if (id === "insert-visual-simulator") {
                savedSelection = saveCursorPosition();
                addVisualSimulator();
            } else if (id === "insert-block-simulator") {
                savedSelection = saveCursorPosition();
                addBlockSimulator();
            } else if (id === "insert-phet-simulator") {
                savedSelection = saveCursorPosition();
                openPhetModal();
            } else if (id === "insert-quiz-question") {
                savedSelection = saveCursorPosition();
                openQuizModal();
            } else if (id === "insert-latex") {
                insertLatexEquation();
            } else {
                document.execCommand(command, false, null);
                contentEditor.focus();
            }
        });
    });
}

function showMarketplaceSelector(type) {
    // Fetch marketplace simulators
    fetch(`${API_BASE_URL}/api/simulators?limit=50`, {
        headers: { Authorization: `Bearer ${authToken}` },
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                showSimulatorSelectionModal(data.data.simulators, type);
            }
        })
        .catch((err) => console.error("Error loading simulators:", err));
}

function showSimulatorSelectionModal(simulators, type) {
    const html = `
        <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 9999;">
            <div style="background: white; padding: 20px; border-radius: 8px; max-width: 600px; max-height: 80vh; overflow-y: auto;">
                <h3>Select a Simulator</h3>
                <button onclick="openSimulatorStudio(); closeSimulatorModal();" style="padding: 8px 16px; background: var(--primary); color: white; border: none; border-radius: 4px; cursor: pointer; margin-bottom: 15px;">✨ Create New Simulator</button>
                <div id="simulator-list" style="margin: 20px 0;">
                    ${simulators
            .map(
                (sim) => `
                        <div style="padding: 10px; border: 1px solid #ddd; margin: 10px 0; border-radius: 4px; cursor: pointer;" onclick="selectSimulatorForCourse(${sim.id
                    }, '${type}', '${sim.title.replace(/'/g, "\\'")}')">
                            <strong>${sim.title}</strong>
                            <p style="margin: 5px 0; font-size: 0.9em; color: #666;">${sim.description || "No description"
                    }</p>
                            <p style="margin: 5px 0; font-size: 0.8em; color: #999;">by ${sim.creator_email
                    } | Downloads: ${sim.downloads}</p>
                        </div>
                    `
            )
            .join("")}
                </div>
                <button onclick="closeSimulatorModal()" style="padding: 8px 16px; background: #999; color: white; border: none; border-radius: 4px; cursor: pointer;">Close</button>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML("beforeend", html);
}

function selectSimulatorForCourse(simulatorId, type, title) {
    const blockId = Date.now();
    courseBlocks.push({
        id: blockId,
        type: `${type}-simulator`,
        title: title,
        simulatorId: simulatorId,
        data: { simulatorId: simulatorId },
    });

    insertSimulatorBlock(
        blockId,
        title,
        `${type.charAt(0).toUpperCase() + type.slice(1)} Simulator`
    );
    closeSimulatorModal();
}

function closeSimulatorModal() {
    const modal = document.querySelector('[style*="position: fixed"]');
    if (modal) modal.remove();
}

// Helper: Save cursor position in contenteditable div
// Uses multiple strategies to ensure position can be restored
function saveCursorPosition() {
    const contentEditor = document.getElementById('course-content-editor');
    const selection = window.getSelection();

    if (selection.rangeCount === 0) {
        // No selection, put cursor at end
        return { position: 'end' };
    }

    try {
        const range = selection.getRangeAt(0);

        // Calculate character offset from start of editor
        const preCaretRange = range.cloneRange();
        preCaretRange.selectNodeContents(contentEditor);
        preCaretRange.setEnd(range.endContainer, range.endOffset);
        const offset = preCaretRange.toString().length;

        // Also save some context text before/after cursor for robustness
        const fullText = contentEditor.textContent;
        const textBefore = fullText.substring(Math.max(0, offset - 20), offset);
        const textAfter = fullText.substring(offset, Math.min(fullText.length, offset + 20));

        return {
            offset: offset,
            textBefore: textBefore,
            textAfter: textAfter,
            range: range.cloneRange()
        };
    } catch (e) {
        console.warn('Failed to save cursor position:', e);
        return { position: 'end' };
    }
}

// Helper: Restore cursor position in contenteditable div
// Uses text context to find the right position even if DOM changed
function restoreCursorPosition(saved) {
    if (!saved) return false;

    const selection = window.getSelection();
    const contentEditor = document.getElementById('course-content-editor');

    // If marked as end position, put at end
    if (saved.position === 'end') {
        const range = document.createRange();
        range.selectNodeContents(contentEditor);
        range.collapse(false);
        selection.removeAllRanges();
        selection.addRange(range);
        return true;
    }

    // Try to restore using saved range first
    if (saved.range) {
        try {
            if (contentEditor.contains(saved.range.commonAncestorContainer)) {
                selection.removeAllRanges();
                selection.addRange(saved.range);
                return true;
            }
        } catch (e) {
            // Range is invalid, continue to offset method
        }
    }

    // Restore by finding the text pattern in current content
    if (saved.textBefore !== undefined && saved.offset !== undefined) {
        const currentText = contentEditor.textContent;

        // Try to find the exact position using context
        if (saved.textBefore && saved.textAfter) {
            // Search for the text before/after pattern
            const pattern = saved.textBefore + saved.textAfter;
            const patternIndex = currentText.indexOf(pattern);
            if (patternIndex !== -1) {
                const exactOffset = patternIndex + saved.textBefore.length;
                return setOffsetInEditor(contentEditor, selection, exactOffset);
            }
        }

        // If pattern not found, try just using the offset
        // (content may have changed but similar length)
        return setOffsetInEditor(contentEditor, selection, saved.offset);
    }

    // Last resort: put cursor at end
    const range = document.createRange();
    range.selectNodeContents(contentEditor);
    range.collapse(false);
    selection.removeAllRanges();
    selection.addRange(range);
    return false;
}

// Helper: Set cursor position by character offset
function setOffsetInEditor(editor, selection, offset) {
    let charCount = 0;
    let nodeStack = [editor];
    let node;

    while (node = nodeStack.pop()) {
        if (node.nodeType === 3) { // Text node
            let nextCharCount = charCount + node.length;
            if (offset <= nextCharCount) {
                const range = document.createRange();
                range.setStart(node, offset - charCount);
                range.collapse(true);
                selection.removeAllRanges();
                selection.addRange(range);
                return true;
            }
            charCount = nextCharCount;
        } else {
            let i = node.childNodes.length;
            while (i--) {
                nodeStack.push(node.childNodes[i]);
            }
        }
    }

    // If we couldn't find the offset, put at end
    const range = document.createRange();
    range.selectNodeContents(editor);
    range.collapse(false);
    selection.removeAllRanges();
    selection.addRange(range);
    return false;
}

function insertLatexEquation() {
    // Save cursor position before opening modal
    savedSelection = saveCursorPosition();
    openLatexEditorModal();
}

function openLatexEditorModal() {
    const modal = document.createElement('div');
    modal.id = 'latex-editor-modal';
    modal.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10000;
  `;

    modal.innerHTML = `
    <div style="background: #18181b; color: #fafafa; padding: 25px; border-radius: 8px; max-width: 900px; width: 95%; max-height: 90vh; display: flex; flex-direction: column; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
      <h2 style="margin: 0 0 15px 0; color: #6366f1;">Insert LaTeX Equation</h2>
      
      <div style="margin-bottom: 15px;">
        <label style="display: block; margin-bottom: 8px; font-weight: 500; color: #a1a1aa;">Equation Type:</label>
        <div style="display: flex; gap: 10px;">
          <label style="display: flex; align-items: center; cursor: pointer;">
            <input type="radio" name="latex-type" value="inline" checked style="margin-right: 5px;" />
            <span>Inline (<code>$...$</code>) - in text</span>
          </label>
          <label style="display: flex; align-items: center; cursor: pointer;">
            <input type="radio" name="latex-type" value="display" style="margin-right: 5px;" />
            <span>Display (<code>$$...$$</code>) - centered</span>
          </label>
        </div>
      </div>
      
      <div style="display: flex; flex: 1; gap: 15px; margin-bottom: 15px; min-height: 200px;">
        <!-- Left: Input -->
        <div style="flex: 1; display: flex; flex-direction: column;">
          <label style="display: block; margin-bottom: 8px; font-weight: 500; color: #a1a1aa;">LaTeX Code:</label>
          <textarea id="latex-input" placeholder="Enter your LaTeX equation here&#10;&#10;Examples:&#10;E = mc^2&#10;\\frac{a}{b}&#10;\\sum_{i=1}^{n} x_i&#10;x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}" 
            style="flex: 1; width: 100%; padding: 12px; background: #09090b; border: 1px solid #27272a; border-radius: 6px; color: #fafafa; font-family: 'Menlo', 'Monaco', monospace; font-size: 14px; resize: none;"></textarea>
        </div>
        
        <!-- Divider -->
        <div style="width: 2px; background: #27272a;"></div>
        
        <!-- Right: Preview -->
        <div style="flex: 1; display: flex; flex-direction: column;">
          <label style="display: block; margin-bottom: 8px; font-weight: 500; color: #a1a1aa;">Live Preview:</label>
          <div id="latex-preview" style="flex: 1; display: flex; align-items: center; justify-content: center; padding: 15px; background: #09090b; border: 1px solid #27272a; border-radius: 6px; overflow: auto; transition: opacity 0.15s; font-size: 1.2em;">
            <span style="color: #a1a1aa;">(preview will appear here)</span>
          </div>
        </div>
      </div>
      
      <div style="margin-bottom: 15px;">
        <strong style="display: block; margin-bottom: 8px; color: #a1a1aa;">Common Symbols:</strong>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 6px;">
          <button type="button" onclick="insertLatexSnippet('\\\\alpha')" class="latex-snippet-btn" style="background:#27272a;color:#fff;border:none;padding:5px;border-radius:4px;cursor:pointer;">α (alpha)</button>
          <button type="button" onclick="insertLatexSnippet('\\\\beta')" class="latex-snippet-btn" style="background:#27272a;color:#fff;border:none;padding:5px;border-radius:4px;cursor:pointer;">β (beta)</button>
          <button type="button" onclick="insertLatexSnippet('\\\\gamma')" class="latex-snippet-btn" style="background:#27272a;color:#fff;border:none;padding:5px;border-radius:4px;cursor:pointer;">γ (gamma)</button>
          <button type="button" onclick="insertLatexSnippet('\\\\Delta')" class="latex-snippet-btn" style="background:#27272a;color:#fff;border:none;padding:5px;border-radius:4px;cursor:pointer;">Δ (Delta)</button>
          <button type="button" onclick="insertLatexSnippet('\\\\frac{a}{b}')" class="latex-snippet-btn" style="background:#27272a;color:#fff;border:none;padding:5px;border-radius:4px;cursor:pointer;">a/b (fraction)</button>
          <button type="button" onclick="insertLatexSnippet('\\\\sqrt{x}')" class="latex-snippet-btn" style="background:#27272a;color:#fff;border:none;padding:5px;border-radius:4px;cursor:pointer;">√x (sqrt)</button>
          <button type="button" onclick="insertLatexSnippet('x^{2}')" class="latex-snippet-btn" style="background:#27272a;color:#fff;border:none;padding:5px;border-radius:4px;cursor:pointer;">x² (power)</button>
          <button type="button" onclick="insertLatexSnippet('x_{i}')" class="latex-snippet-btn" style="background:#27272a;color:#fff;border:none;padding:5px;border-radius:4px;cursor:pointer;">xᵢ (subscript)</button>
          <button type="button" onclick="insertLatexSnippet('\\\\sum_{i=1}^{n}')" class="latex-snippet-btn" style="background:#27272a;color:#fff;border:none;padding:5px;border-radius:4px;cursor:pointer;">Σ (sum)</button>
          <button type="button" onclick="insertLatexSnippet('\\\\int_a^b')" class="latex-snippet-btn" style="background:#27272a;color:#fff;border:none;padding:5px;border-radius:4px;cursor:pointer;">∫ (integral)</button>
          <button type="button" onclick="insertLatexSnippet('\\\\pm')" class="latex-snippet-btn" style="background:#27272a;color:#fff;border:none;padding:5px;border-radius:4px;cursor:pointer;">± (plus/minus)</button>
          <button type="button" onclick="insertLatexSnippet('\\\\times')" class="latex-snippet-btn" style="background:#27272a;color:#fff;border:none;padding:5px;border-radius:4px;cursor:pointer;">× (times)</button>
        </div>
      </div>
      
      <div style="margin-bottom: 20px;">
        <strong style="display: block; margin-bottom: 8px; color: #a1a1aa;">Common Equations:</strong>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 6px;">
          <button type="button" onclick="insertLatexSnippet('E = mc^2')" class="latex-template-btn" style="background:#3f3f46;color:#fff;border:none;padding:5px;border-radius:4px;cursor:pointer;">E = mc²</button>
          <button type="button" onclick="insertLatexSnippet('x = \\\\frac{-b \\\\pm \\\\sqrt{b^2 - 4ac}}{2a}')" class="latex-template-btn" style="background:#3f3f46;color:#fff;border:none;padding:5px;border-radius:4px;cursor:pointer;">Quadratic formula</button>
          <button type="button" onclick="insertLatexSnippet('\\\\lambda = \\\\frac{h}{p}')" class="latex-template-btn" style="background:#3f3f46;color:#fff;border:none;padding:5px;border-radius:4px;cursor:pointer;">de Broglie wavelength</button>
          <button type="button" onclick="insertLatexSnippet('\\\\Delta x \\\\cdot \\\\Delta p \\\\geq \\\\frac{h}{4\\\\pi}')" class="latex-template-btn" style="background:#3f3f46;color:#fff;border:none;padding:5px;border-radius:4px;cursor:pointer;">Uncertainty principle</button>
          <button type="button" onclick="insertLatexSnippet('\\\\int_0^\\\\infty e^{-x} dx = 1')" class="latex-template-btn" style="background:#3f3f46;color:#fff;border:none;padding:5px;border-radius:4px;cursor:pointer;">Integral example</button>
          <button type="button" onclick="insertLatexSnippet('F = ma')" class="latex-template-btn" style="background:#3f3f46;color:#fff;border:none;padding:5px;border-radius:4px;cursor:pointer;">Newton's 2nd law</button>
        </div>
      </div>
      
      <div style="display: flex; gap: 10px; justify-content: flex-end; margin-top: auto;">
        <button type="button" onclick="closeLatexEditorModal()" style="padding: 10px 20px; background: #27272a; color: white; border: none; border-radius: 4px; cursor: pointer;">Cancel</button>
        <button type="button" onclick="confirmLatexInsertion()" style="padding: 10px 20px; background: #6366f1; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">Insert Equation</button>
      </div>
    </div>
  `;

    document.body.appendChild(modal);

    // Add event listeners for preview
    const input = document.getElementById('latex-input');
    const previewDiv = document.getElementById('latex-preview');
    const typeRadios = document.querySelectorAll('input[name="latex-type"]');

    let latexDebounceTimer = null;
    input.addEventListener('input', () => {
        clearTimeout(latexDebounceTimer);
        previewDiv.style.opacity = '0.5';
        latexDebounceTimer = setTimeout(() => {
            updateLatexPreview();
            previewDiv.style.opacity = '1';
        }, 150);
    });

    typeRadios.forEach(radio => radio.addEventListener('change', updateLatexPreview));

    input.focus();
}

function updateLatexPreview() {
    const input = document.getElementById('latex-input');
    const preview = document.getElementById('latex-preview');
    const type = document.querySelector('input[name="latex-type"]:checked').value;

    if (!input.value.trim()) {
        preview.innerHTML = '(enter LaTeX to preview)';
        return;
    }

    let latex = input.value.trim();
    if (type === 'display') {
        latex = '$$' + latex + '$$';
    } else {
        latex = '$' + latex + '$';
    }

    // Clear previous content and error states
    preview.innerHTML = '';
    preview.classList.remove('error');
    
    // Create a container for the math
    const mathContainer = document.createElement('div');
    mathContainer.textContent = latex;
    preview.appendChild(mathContainer);

    // Trigger MathJax to render with error handling
    if (window.MathJax && window.MathJax.typesetPromise) {
        window.MathJax.typesetPromise([mathContainer])
            .then(() => {
                preview.classList.add('success');
            })
            .catch(err => {
                preview.classList.add('error');
                if (window.logger) window.logger.debug('LaTeX preview error:', err);
            });
    } else {
        // Fallback if MathJax not ready
        preview.classList.add('warning');
        mathContainer.textContent = 'MathJax loading...';
    }
}

function insertLatexSnippet(snippet) {
    const input = document.getElementById('latex-input');
    input.value = snippet;
    updateLatexPreview();
    input.focus();
}

function closeLatexEditorModal() {
    const modal = document.getElementById('latex-editor-modal');
    if (modal) modal.remove();
}

function confirmLatexInsertion() {
    const input = document.getElementById('latex-input');
    const type = document.querySelector('input[name="latex-type"]:checked').value;
    const latex = input.value.trim();

    if (!latex) {
        alert('Please enter a LaTeX equation');
        return;
    }

    closeLatexEditorModal();

    // Build final LaTeX string
    let finalLatex = latex;
    if (type === 'display') {
        finalLatex = '$$' + latex + '$$';
    } else {
        finalLatex = '$' + latex + '$';
    }

    // Get the content editor
    const contentEditor = document.getElementById('course-content-editor');

    // Create span for the LaTeX equation
    const span = document.createElement('span');
    span.className = 'latex-equation';
    span.textContent = finalLatex;
    span.setAttribute('data-latex', 'true');

    // Restore the cursor position that was saved when button was clicked
    contentEditor.focus();
    restoreCursorPosition(savedSelection);
    savedSelection = null;

    const selection = window.getSelection();

    // Try to insert at the restored cursor position
    if (selection.rangeCount > 0) {
        try {
            const range = selection.getRangeAt(0);
            const commonAncestor = range.commonAncestorContainer;

            // If cursor is in text, use insertNode which works for inline elements
            if (commonAncestor.nodeType === Node.TEXT_NODE) {
                // Insert the LaTeX span at cursor
                range.insertNode(span);
                
                // Add a zero-width space after it so cursor doesn't get trapped
                const zws = document.createTextNode('\u200B');
                span.parentNode.insertBefore(zws, span.nextSibling);

                // Move cursor after the equation
                range.setStartAfter(zws);
                range.collapse(true);
                selection.removeAllRanges();
                selection.addRange(range);

                // Trigger MathJax to re-render
                if (window.MathJax && window.MathJax.typesetPromise) {
                    setTimeout(() => {
                        window.MathJax.typesetPromise([contentEditor]).catch(err => { if (window.logger) window.logger.debug('MathJax error:', err); });
                    }, 100);
                }
                return;
            }
        } catch (e) {
            console.warn('Failed to insert LaTeX at cursor:', e);
        }
    }

    // Fallback: append to end
    contentEditor.appendChild(span);

    // Trigger MathJax to re-render the equation
    if (window.MathJax && window.MathJax.typesetPromise) {
        setTimeout(() => {
            window.MathJax.typesetPromise([contentEditor]).catch(err => { if (window.logger) window.logger.debug('MathJax error:', err); });
        }, 100);
    }
}

// Process LaTeX in text - convert $...$ to rendered equations
// Preserves already-processed equations
function processLatexInEditor() {
    const contentEditor = document.getElementById('course-content-editor');
    if (!contentEditor) {
        console.warn("⚠️ LaTeX: course-content-editor not found");
        return;
    }

    const latexPattern = /\$\$([^$]+)\$\$|\$([^$]+)\$/g;

    // Walk through all text nodes and find unprocessed LaTeX patterns
    const walker = document.createTreeWalker(
        contentEditor,
        NodeFilter.SHOW_TEXT,
        null,
        false
    );

    const nodesToProcess = [];
    let currentNode;

    while (currentNode = walker.nextNode()) {
        // Skip text nodes that are already inside latex-equation spans
        if (currentNode.parentElement && currentNode.parentElement.classList.contains('latex-equation')) {
            continue;
        }

        // Check if this text node contains LaTeX patterns
        if (latexPattern.test(currentNode.textContent)) {
            nodesToProcess.push(currentNode);
        }
    }

    // Reset pattern for matching
    latexPattern.lastIndex = 0;

    // Process each text node that has unprocessed LaTeX
    nodesToProcess.forEach(textNode => {
        const text = textNode.textContent;
        const matches = [...text.matchAll(/\$\$([^$]+)\$\$|\$([^$]+)\$/g)];

        if (matches.length === 0) return;

        // Create a fragment to hold the new content
        const fragment = document.createDocumentFragment();
        let lastIndex = 0;

        matches.forEach(match => {
            const fullMatch = match[0];
            const startIndex = match.index;

            // Add text before this LaTeX
            if (startIndex > lastIndex) {
                const textBefore = text.substring(lastIndex, startIndex);
                fragment.appendChild(document.createTextNode(textBefore));
            }

            // Create LaTeX span
            const span = document.createElement('span');
            span.className = 'latex-equation';
            span.setAttribute('data-latex', 'true');
            span.textContent = fullMatch;
            fragment.appendChild(span);

            lastIndex = startIndex + fullMatch.length;
        });

        // Add remaining text
        if (lastIndex < text.length) {
            fragment.appendChild(document.createTextNode(text.substring(lastIndex)));
        }

        // Replace the text node with the new content
        textNode.parentNode.replaceChild(fragment, textNode);
    });

    // Trigger MathJax rendering for new equations
    if (window.MathJax && window.MathJax.typesetPromise && nodesToProcess.length > 0) {
        // Use longer timeout and ensure proper rendering
        setTimeout(async () => {
            try {
                if (window.logger) window.logger.debug("🔵 LaTeX: Processing", nodesToProcess.length, "text nodes");
                await window.MathJax.typesetPromise([contentEditor]);
                if (window.logger) window.logger.debug("✅ LaTeX: All equations rendered");
            } catch (err) {
                console.error("❌ LaTeX render error:", err);
            }
        }, 100);
    } else if (window.MathJax && window.MathJax.typesetPromise) {
        if (window.logger) window.logger.debug("ℹ️ LaTeX: No new equations to process");
    } else {
        console.warn("⚠️ LaTeX: MathJax not loaded yet");
    }
}

function addVisualSimulator() {
    const blockId = Date.now();
    courseBlocks.push({
        id: blockId,
        type: "visual-simulator",
        title: "Code-based Visual Simulator",
        data: { code: "", variables: {} },
    });

    // Start placement mode instead of direct insertion
    startPlacementMode('visual-simulator', {
        id: blockId,
        title: "Code-based Visual",
        type: "Code-based Simulator"
    });
}

function isScratchSimulatorData(data) {
    if (!data) return false;
    if (data.format === 'veelearn-scratch-1' || data.sim_type === 'scratch') return true;
    if (data.project && data.project.format === 'veelearn-scratch-1') return true;
    if (data.blocks && !Array.isArray(data.blocks) && data.blocks.format === 'veelearn-scratch-1') return true;
    return false;
}

function getScratchProjectFromData(data) {
    if (!data) return null;
    // Prefer an actual project object (has sprites) over the save wrapper
    if (data.format === 'veelearn-scratch-1' && data.sprites) return data;
    if (data.project && data.project.format === 'veelearn-scratch-1') return data.project;
    if (data.blocks && data.blocks.format === 'veelearn-scratch-1' && data.blocks.sprites) return data.blocks;
    if (data.format === 'veelearn-scratch-1') return data;
    return null;
}

function addBlockSimulator() {
    const blockId = Date.now();
    courseBlocks.push({
        id: blockId,
        type: "block-simulator",
        title: "Interactive Simulator",
        data: {
            format: 'veelearn-scratch-1',
            connections: [],
            sim_type: 'scratch'
        },
    });

    startPlacementMode('block-simulator', {
        id: blockId,
        title: "Interactive Simulator",
        type: "Interactive Simulator"
    });
}

function insertSimulatorBlock(blockId, title, type) {
    const contentEditor = document.getElementById("course-content-editor");
    const simulatorDiv = document.createElement("div");
    simulatorDiv.className = "simulator-block";
    simulatorDiv.dataset.blockId = blockId;
    simulatorDiv.contentEditable = 'false'; // Make non-editable block
    simulatorDiv.style.cssText =
        "background: #f0f0f0; padding: 15px; margin: 10px 0; border-left: 4px solid #667eea; border-radius: 4px; display: block;";
    simulatorDiv.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong>${escapeHtml(type)}</strong>
                <p style="margin: 5px 0; color: #666;">${escapeHtml(title)}</p>
            </div>
            <div style="display: flex; gap: 10px;">
                <button type="button" onclick="openSliderConfigModal(${blockId})" style="padding: 5px 10px; background: #10b981; color: white; border: none; border-radius: 4px; cursor: pointer;">⚙️ Configure Sliders</button>
                <button type="button" onclick="handleEditSimulator(event, ${blockId})" style="padding: 5px 10px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer;">Edit</button>
                <button type="button" onclick="handleRemoveSimulator(event, ${blockId})" style="padding: 5px 10px; background: #f44336; color: white; border: none; border-radius: 4px; cursor: pointer;">Remove</button>
            </div>
        </div>
    `;

    // Restore the cursor position that was saved when button was clicked
    contentEditor.focus();
    restoreCursorPosition(savedSelection);
    savedSelection = null;

    const selection = window.getSelection();

    // For contenteditable divs, insert at the position where cursor is
    // by finding the element after the current node
    if (selection.rangeCount > 0) {
        try {
            const range = selection.getRangeAt(0);
            const commonAncestor = range.commonAncestorContainer;

            // Get the parent element (could be text node's parent or element itself)
            let parent = commonAncestor.nodeType === Node.TEXT_NODE
                ? commonAncestor.parentNode
                : commonAncestor;

            // If parent is the editor, we're at top level - good for insertion
            if (parent === contentEditor || parent.nodeType === Node.TEXT_NODE) {
                // Split text at cursor if in middle of text
                if (commonAncestor.nodeType === Node.TEXT_NODE) {
                    const offset = range.endOffset;
                    const textNode = commonAncestor;

                    // Split the text node at cursor position
                    if (offset < textNode.length) {
                        textNode.splitText(offset);
                    }

                    // Insert simulator after this text node
                    const nextNode = textNode.nextSibling;
                    if (nextNode) {
                        contentEditor.insertBefore(simulatorDiv, nextNode);
                    } else {
                        contentEditor.appendChild(simulatorDiv);
                    }
                } else {
                    // If not in text, just append (fallback)
                    contentEditor.appendChild(simulatorDiv);
                }
            } else {
                // Different parent, use appendChild as fallback
                contentEditor.appendChild(simulatorDiv);
            }

            // Move cursor after the simulator
            const range2 = document.createRange();
            range2.setStartAfter(simulatorDiv);
            range2.collapse(true);
            selection.removeAllRanges();
            selection.addRange(range2);

            return;
        } catch (e) {
            console.warn('Failed to insert simulator at cursor:', e);
        }
    }

    // Fallback: just append to end
    contentEditor.appendChild(simulatorDiv);
    contentEditor.focus();
}


// ===== UI RENDERING =====
function showLandingPage() {
    if (window.LearnerShell?.hideLearnerShell) window.LearnerShell.hideLearnerShell();
    const landing = document.getElementById("landing-page");
    const auth = document.getElementById("auth-section");
    const dashboard = document.getElementById("dashboard-section");
    const editor = document.getElementById("course-editor-section");
    const viewer = document.getElementById("course-viewer-section");

    // Find currently visible section
    const currentVisible = [auth, dashboard, editor, viewer].find(s => s && s.style.display !== 'none');

    if (currentVisible && currentVisible !== landing) {
        transitionPage(currentVisible, landing);
    } else {
        landing.style.display = "block";
    }

    auth.style.display = "none";
    dashboard.style.display = "none";
    editor.style.display = "none";
    viewer.style.display = "none";

    document.getElementById("login-link").style.display = "inline";
    document.getElementById("register-link").style.display = "inline";
    document.getElementById("dashboard-link").style.display = "none";
    document.getElementById("logout-button").style.display = "none";

    setStudyCoachVisible(false);
    currentViewingCourseId = null;

    // Initialize aurora ball on landing page
    initializeAuroraBall();
}

/**
 * Initialize mouse-following aurora ball for landing page
 */
function initializeAuroraBall() {
    // Remove existing ball if any
    const existingBall = document.querySelector('.aurora-ball');
    if (existingBall) existingBall.remove();

    // Create aurora ball element
    const ball = document.createElement('div');
    ball.className = 'aurora-ball';
    document.body.appendChild(ball);

    // Track mouse movement with smooth interpolation
    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let ballX = mouseX;
    let ballY = mouseY;
    const speed = 0.08; // Smoothing factor (lower = smoother)

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    // Animation loop for smooth following
    function updateBallPosition() {
        ballX += (mouseX - ballX) * speed;
        ballY += (mouseY - ballY) * speed;

        ball.style.left = ballX + 'px';
        ball.style.top = ballY + 'px';

        // Only animate if on landing page
        if (document.getElementById("landing-page").style.display !== 'none') {
            requestAnimationFrame(updateBallPosition);
        }
    }

    updateBallPosition();
}

function showAuthSection(type = "login") {
    if (window.LearnerShell?.hideLearnerShell) window.LearnerShell.hideLearnerShell();

    const auth = document.getElementById("auth-section");
    const landing = document.getElementById("landing-page");
    const dashboard = document.getElementById("dashboard-section");
    const editor = document.getElementById("course-editor-section");
    const viewer = document.getElementById("course-viewer-section");

    // Find currently visible section
    const currentVisible = [landing, dashboard, editor, viewer].find(s => s && s.style.display !== 'none');

    if (currentVisible && currentVisible !== auth) {
        transitionPage(currentVisible, auth);
    } else {
        auth.style.display = "block";
    }

    landing.style.display = "none";
    dashboard.style.display = "none";
    editor.style.display = "none";
    viewer.style.display = "none";

    const hide = id => { const el = document.getElementById(id); if (el) el.style.display = "none"; };
    const show = (id, d = "inline") => { const el = document.getElementById(id); if (el) el.style.display = d; };

    hide("simulator-link");
    hide("marketplace-link");
    hide("creator-link");
    hide("dashboard-link");
    hide("logout-button");

    show("login-link");
    show("register-link");

    setStudyCoachVisible(false);
    currentViewingCourseId = null;

    if (type === "register") {
        hide("login-form");
        show("register-form", "block");
        hide("forgot-password-form");
    } else {
        show("login-form", "block");
        hide("register-form");
        hide("forgot-password-form");
    }
}

function showDashboard() {
    stopCourseTimer();
    currentViewingCourseId = null;
    exitCourseViewerMode();

    // Redirect EMS roles to their specific dashboards
    if (currentUser?.role === 'school_admin') {
        window.location.href = 'school-admin-dashboard.html';
        return;
    } else if (currentUser?.role === 'teacher') {
        window.location.href = 'teacher-dashboard.html';
        return;
    } else if (currentUser?.role === 'student') {
        window.location.href = 'student-dashboard.html';
        return;
    } else if (currentUser?.role === 'parent') {
        window.location.href = 'parent-dashboard.html';
        return;
    }

    // Khan-style learner shell for everyone except superadmin
    if (currentUser?.role !== 'superadmin' && window.LearnerShell?.showLearnerShell) {
        const landing = document.getElementById("landing-page");
        const auth = document.getElementById("auth-section");
        const editor = document.getElementById("course-editor-section");
        const viewer = document.getElementById("course-viewer-section");
        const dashboard = document.getElementById("dashboard-section");
        if (landing) landing.style.display = "none";
        if (auth) auth.style.display = "none";
        if (editor) editor.style.display = "none";
        if (viewer) viewer.style.display = "none";
        if (dashboard) dashboard.style.display = "none";
        window.LearnerShell.showLearnerShell();

        if (!window.__pendingAddSimHandled) {
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('action') === 'addSimulator' && urlParams.get('simulatorId')) {
                window.__pendingAddSimHandled = true;
                const pendingSimId = parseInt(urlParams.get('simulatorId'));
                history.replaceState({}, '', window.location.pathname);
                setTimeout(() => showCoursePickerForSimulator(pendingSimId, null), 400);
            }
        }
        return;
    }

    if (window.LearnerShell?.hideLearnerShell) window.LearnerShell.hideLearnerShell();

    const dashboard = document.getElementById("dashboard-section");
    const landing = document.getElementById("landing-page");
    const auth = document.getElementById("auth-section");
    const editor = document.getElementById("course-editor-section");
    const viewer = document.getElementById("course-viewer-section");

    // Find currently visible section
    const currentVisible = [landing, auth, editor, viewer].find(s => s && s.style.display !== 'none');

    if (currentVisible && currentVisible !== dashboard) {
        transitionPage(currentVisible, dashboard);
    } else {
        dashboard.style.display = "block";
    }

    landing.style.display = "none";
    auth.style.display = "none";
    editor.style.display = "none";
    viewer.style.display = "none";

    const showEl = (id, d = "inline") => { const el = document.getElementById(id); if (el) el.style.display = d; };
    const hideEl = id => { const el = document.getElementById(id); if (el) el.style.display = "none"; };

    showEl("simulator-link");
    showEl("marketplace-link");
    showEl("creator-link");
    showEl("dashboard-link");
    showEl("logout-button");

    hideEl("login-link");
    hideEl("register-link");

    setStudyCoachVisible(true);

    const userEmail = document.getElementById("user-email");
    if (userEmail) userEmail.textContent = currentUser?.email || "User";

    // INSTANT: Show dashboard content immediately
    if (currentUser?.role === "superadmin") {
        showSuperadminDashboard();
    } else if (currentUser?.role === "admin") {
        showAdminDashboard();
    } else {
        showUserDashboard();
    }

    // Handle "Use in Course" redirect from the marketplace page
    if (!window.__pendingAddSimHandled) {
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('action') === 'addSimulator' && urlParams.get('simulatorId')) {
            window.__pendingAddSimHandled = true;
            const pendingSimId = parseInt(urlParams.get('simulatorId'));
            history.replaceState({}, '', window.location.pathname);
            setTimeout(() => showCoursePickerForSimulator(pendingSimId, null), 400);
        }
    }

    // INSTANT: Load all data asynchronously in background without blocking UI
    setTimeout(() => {
        loadVolunteerStats();
        renderSimulatorMarketplace();
        if (currentUser?.role === "superadmin") {
            loadAllUsers();
            loadPendingCourses();
            loadUserCourses();
            loadAvailableCourses();
        } else if (currentUser?.role === "admin") {
            loadPendingCourses();
            loadUserCourses();
            loadAvailableCourses();
        } else {
            loadUserCourses();
            loadAvailableCourses();
            loadStudentAssignments();
            loadEnrolledCourses();
        }
    }, 0);
}

function showSuperadminDashboard() {
    document.getElementById("user-dashboard").style.display = "none";
    document.getElementById("admin-dashboard").style.display = "none";
    document.getElementById("superadmin-dashboard").style.display = "block";

    // INSTANT: Only set up event listeners, data loads in showDashboard() asynchronously
    document
        .getElementById("create-course-button-superadmin")
        ?.addEventListener("click", createNewCourse);

    // Load EMS school approval data
    loadPendingSchools();
    loadAllSchools();
    loadPendingTeachers();
}

function showAdminDashboard() {
    document.getElementById("user-dashboard").style.display = "none";
    document.getElementById("superadmin-dashboard").style.display = "none";
    document.getElementById("admin-dashboard").style.display = "block";

    // INSTANT: Only set up event listeners, data loads in showDashboard() asynchronously
    document
        .getElementById("create-course-button-admin")
        ?.addEventListener("click", createNewCourse);
}

function showUserDashboard() {
    document.getElementById("superadmin-dashboard").style.display = "none";
    document.getElementById("admin-dashboard").style.display = "none";
    document.getElementById("user-dashboard").style.display = "block";

    // INSTANT: Only set up event listeners, data loads in showDashboard() asynchronously
    document
        .getElementById("create-course-button-user")
        ?.addEventListener("click", createNewCourse);
}

function loadAllUsers() {
    fetch(`${API_BASE_URL}/api/users`, {
        headers: { Authorization: `Bearer ${authToken}` },
        credentials: "include"
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                allUsers = data.data;
                renderUserList();
            } else {
                console.error("Error loading users:", data.message);
            }
        })
        .catch((err) => console.error("Error loading users:", err));
}

function renderUserList() {
    const userList = document.getElementById("user-list");
    if (!userList) return;

    userList.innerHTML = allUsers
        .map(
            (user) => {
                const pendingApproval = user.role === 'teacher' && !user.teacher_approved;
                const approveBtn = pendingApproval ?
                    `<button onclick="approveTeacher(${user.id}, '${user.email}')" style="background: #ff9800; color: #fff;">⚠️ APPROVE TEACHER</button>` : '';

                return `
        <li>
            <strong>${escapeHtml(user.email)}</strong>
            <p>Role: ${escapeHtml(user.role)} ${user.class_code ? `| Class Code: ${escapeHtml(user.class_code)}` : ''} | ${user.teacher_approved ? '✅ Approved' : user.role === 'teacher' ? '⏳ Pending Approval' : ''} | Shells: ${user.shells} | Gems: ${user.gems || 0} | Volunteer: ${(user.total_volunteer_hours || 0).toFixed(1)}h ${user.is_verified_creator ? '✅' : ''}</p>
            ${approveBtn}
            <button onclick="changeUserRole('${escapeHtml(user.email)}', 'admin')">Make Admin</button>
            <button onclick="changeUserRole('${escapeHtml(user.email)}', 'teacher')">Make Teacher</button>
            <button onclick="changeUserRole('${escapeHtml(user.email)}', 'user')">Make User</button>
            <button onclick="grantVolunteerHours(${user.id}, '${escapeHtml(user.email)}')" style="background: #4ade80; color: #000;">Grant Hours</button>
            <button onclick="grantGems(${user.id}, '${escapeHtml(user.email)}')" style="background: #fbbf24; color: #000;">Grant Gems</button>
        </li>
    `;
            }
        )
        .join("");
}

function changeUserRole(email, newRole) {
    fetch(`${API_BASE_URL}/api/admin/users/${email}/role`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authToken}`,
        },
        credentials: "include",
        body: JSON.stringify({ role: newRole }),
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                alert(`User role changed to ${newRole}`);
                loadAllUsers();
            } else {
                alert("Error: " + data.message);
            }
        })
        .catch((err) => console.error("Error changing role:", err));
}

// Approve teacher request
function approveTeacher(userId, email) {
    if (!confirm(`Approve ${email} as a teacher? Their students will then be able to enroll.`)) return;

    fetch(`${API_BASE_URL}/api/admin/approve-teacher/${userId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authToken}`,
        },
        credentials: "include"
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                alert(`✅ Teacher ${email} approved! Students can now enroll in their class.`);
                // Refresh user list to show updated status
                loadAllUsers();

                // If this is the current logged-in teacher, update their approval status too
                if (currentUser && currentUser.id === userId) {
                    currentUser.teacher_approved = true;
                    // Refresh their UI if they're on dashboard
                    setupTeacherStudentListeners();
                }
            } else {
                alert("Error: " + data.message);
            }
        })
        .catch((err) => {
            console.error("Error approving teacher:", err);
            alert("Error approving teacher");
        });
}

window.approveTeacher = approveTeacher;

function loadPendingCourses() {
    fetch(`${API_BASE_URL}/api/admin/courses/pending`, {
        headers: { Authorization: `Bearer ${authToken}` },
        credentials: "include"
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                pendingCourses = data.data;
                renderPendingCourses(data.data);
            }
        })
        .catch((err) => console.error("Error loading pending courses:", err));
}

// ===== EMS SCHOOL APPROVAL FUNCTIONS =====

function loadPendingSchools() {
    fetch(`${API_BASE_URL}/api/schools/pending`, {
        headers: { Authorization: `Bearer ${authToken}` },
        credentials: "include"
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success || data.data) {
                renderPendingSchools(data.data);
            }
        })
        .catch((err) => console.error("Error loading pending schools:", err));
}

function renderPendingSchools(schools) {
    const list = document.getElementById("superadmin-pending-schools-list");
    if (!list) return;

    if (!schools || schools.length === 0) {
        list.innerHTML = "<li><em>No pending schools</em></li>";
        return;
    }

    list.innerHTML = schools
        .map(
            (school) => `
        <li>
            <strong>${escapeHtml(school.name)}</strong>
            <p>Admin: ${escapeHtml(school.admin_name)} (${escapeHtml(school.email)})</p>
            <button onclick="approveSchool(${school.id})">Approve</button>
        </li>
    `
        )
        .join("");
}

function loadAllSchools() {
    fetch(`${API_BASE_URL}/api/schools`, {
        headers: { Authorization: `Bearer ${authToken}` },
        credentials: "include"
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success || data.data) {
                renderAllSchools(data.data);
            }
        })
        .catch((err) => console.error("Error loading schools:", err));
}

function renderAllSchools(schools) {
    const list = document.getElementById("superadmin-all-schools-list");
    if (!list) return;

    if (!schools || schools.length === 0) {
        list.innerHTML = "<li><em>No schools</em></li>";
        return;
    }

    list.innerHTML = schools
        .map(
            (school) => `
        <li>
            <strong>${escapeHtml(school.name)}</strong>
            <p>Admin: ${escapeHtml(school.admin_name)} (${escapeHtml(school.email)})</p>
            <p>School Code: ${escapeHtml(school.school_code || 'Not approved yet')}</p>
            <p>Status: ${school.is_approved ? '✅ Approved' : '⏳ Pending'}</p>
        </li>
    `
        )
        .join("");
}

function approveSchool(schoolId) {
    if (!confirm("Are you sure you want to approve this school?")) return;

    fetch(`${API_BASE_URL}/api/schools/${schoolId}/approve`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authToken}`
        },
        credentials: "include"
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success || data.message) {
                alert("School approved! School code: " + (data.data?.school_code || 'Generated'));
                loadPendingSchools();
                loadAllSchools();
            } else {
                alert(data.message || "Failed to approve school");
            }
        })
        .catch((err) => {
            console.error("Error approving school:", err);
            alert("Error approving school");
        });
}

window.approveSchool = approveSchool;

function loadPendingTeachers() {
    fetch(`${API_BASE_URL}/api/users/pending-teachers`, {
        headers: { Authorization: `Bearer ${authToken}` },
        credentials: "include"
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success || data.data) {
                renderPendingTeachers(data.data);
            }
        })
        .catch((err) => console.error("Error loading pending teachers:", err));
}

function renderPendingTeachers(teachers) {
    const list = document.getElementById("superadmin-pending-teachers-list");
    if (!list) return;

    if (!teachers || teachers.length === 0) {
        list.innerHTML = "<li><em>No pending teachers</em></li>";
        return;
    }

    list.innerHTML = teachers
        .map(
            (teacher) => `
        <li>
            <strong>${escapeHtml(teacher.name)}</strong>
            <p>Email: ${escapeHtml(teacher.email)}</p>
            <p>School: ${escapeHtml(teacher.school_name || 'N/A')}</p>
            <button onclick="approveTeacher(${teacher.id})">Approve</button>
        </li>
    `
        )
        .join("");
}

function approveTeacher(userId) {
    if (!confirm("Are you sure you want to approve this teacher?")) return;

    fetch(`${API_BASE_URL}/api/users/${userId}/approve-teacher`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authToken}`
        },
        credentials: "include"
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success || data.message) {
                alert("Teacher approved successfully!");
                loadPendingTeachers();
            } else {
                alert(data.message || "Failed to approve teacher");
            }
        })
        .catch((err) => {
            console.error("Error approving teacher:", err);
            alert("Error approving teacher");
        });
}

window.approveTeacher = approveTeacher;

function renderPendingCourses(courses) {
    const list =
        document.getElementById("superadmin-pending-courses-list") ||
        document.getElementById("admin-pending-courses-list");
    if (!list) return;

    if (courses.length === 0) {
        list.innerHTML = "<li><em>No pending courses</em></li>";
        return;
    }

    list.innerHTML = courses
        .map(
            (course) => `
        <li>
            <strong>${escapeHtml(course.title)}</strong>
            <p>${escapeHtml(course.description || "No description")}</p>
            <button onclick="previewCourse(${course.id})">Preview</button>
            <button onclick="approveCourse(${course.id})">Approve</button>
            <button onclick="rejectCourse(${course.id})">Reject</button>
        </li>
    `
        )
        .join("");
}

function previewCourse(courseId) {
    viewCourse(courseId);
}

function approveCourse(courseId) {
    fetch(`${API_BASE_URL}/api/admin/courses/${courseId}/status`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authToken}`,
        },
        credentials: "include",
        body: JSON.stringify({ status: "approved" }),
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                alert("Course approved!");
                loadPendingCourses();
                loadAvailableCourses();
            }
        })
        .catch((err) => console.error("Error approving course:", err));
}

function rejectCourse(courseId) {
    const reason = prompt("Please provide a reason for rejection:");
    if (reason === null) return;

    fetch(`${API_BASE_URL}/api/admin/courses/${courseId}/status`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authToken}`,
        },
        credentials: "include",
        body: JSON.stringify({ status: "rejected", feedback: reason }),
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                alert("Course rejected!");
                loadPendingCourses();
            }
        })
        .catch((err) => console.error("Error rejecting course:", err));
}

function loadUserCourses() {
    if (window.logger) window.logger.debug("=== LOADING USER COURSES ===");
    
    // Show loading state
    if (window.loadingManager) window.loadingManager.show('Loading your courses...');
    
    // First load created courses, then enrich with enrollment data
    Promise.all([
        fetch(`${API_BASE_URL}/api/courses`, {
            headers: { Authorization: `Bearer ${authToken}` },
            credentials: "include"
        }).then(res => res.json()),
        loadEnhancedEnrollments()
    ])
    .then(([coursesData, enrollmentData]) => {
        if (coursesData.success) {
            const allCoursesFromServer = coursesData.data || [];
            if (window.logger) window.logger.debug("Total courses from API:", allCoursesFromServer.length);
            if (window.logger) window.logger.debug("Current user ID:", currentUser.id);

            myCourses = allCoursesFromServer.filter((c) => {
                const owner = c.creator_id != null ? c.creator_id : c.user_id;
                return Number(owner) === Number(currentUser.id);
            });
            myCourses = sortCoursesForDisplay(myCourses);
            try { window.myCourses = myCourses; } catch (_) { /* ignore */ }
            
            // Merge enrollment status into courses (for courses user is enrolled in)
            const enrolledCourseIds = new Set(enrollmentData?.map(e => e.id) || []);
            myCourses = myCourses.map(course => {
                const enrollment = enrollmentData?.find(e => e.id === course.id);
                return {
                    ...course,
                    enrollment_status: enrollment?.enrollment_status || null,
                    course_type: enrollment?.course_type || course.course_type,
                    total_units: enrollment?.total_units,
                    completed_units: enrollment?.completed_units
                };
            });
            
            if (window.logger) window.logger.debug("Filtered user courses:", myCourses.length);
            // Clear search box
            const myCoursesSearch = document.getElementById('myCoursesSearch');
            if (myCoursesSearch) myCoursesSearch.value = '';
            myCoursesCurrentSearch = '';
            myCoursesCurrentPage = 1;
            renderUserCourses('');

            if (typeof window.LearnerShell?.refreshCourseFlyout === 'function') {
                window.LearnerShell.refreshCourseFlyout();
            }

            // If teacher, populate assignment dropdown (only if empty or fallback needed)
            if (currentUser.role === 'teacher' && myCourses.length > 0) {
                const dropdown = document.getElementById('assignment-course-select');
                if (dropdown && dropdown.options.length <= 1) { // Only if not already populated by all courses
                    dropdown.innerHTML = '<option value="">Select a course...</option>' +
                        myCourses.map(c => `<option value="${c.id}">${escapeHtml(c.title)}</option>`).join('');
                }
            }
        }
    })
    .catch((err) => {
        console.error("Error loading user courses:", err);
    })
    .finally(() => {
        // Hide loading state
        if (window.loadingManager) window.loadingManager.hide();
    });
}

function loadAvailableCourses() {
    if (window.logger) window.logger.debug("=== LOADING AVAILABLE COURSES ===");
    
    // Show loading state
    if (window.loadingManager) window.loadingManager.show('Loading available courses...');
    
    fetch(`${API_BASE_URL}/api/courses`, {
        headers: { Authorization: `Bearer ${authToken}` },
        credentials: "include"
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                const allCoursesFromServer = data.data || [];
                if (window.logger) window.logger.debug("Total courses from API:", allCoursesFromServer.length);
                if (window.logger) window.logger.debug(
                    "Course statuses:",
                    allCoursesFromServer.map((c) => ({
                        id: c.id,
                        title: c.title,
                        status: c.status,
                        creator_id: c.user_id,
                        currentUserId: currentUser.id,
                    }))
                );

                allApprovedCourses = sortCoursesForDisplay(
                    allCoursesFromServer.filter((c) => c.status === "approved")
                );
                availableCourses = allApprovedCourses.filter(
                    (c) => Number(c.creator_id) !== Number(currentUser.id)
                );
                if (window.logger) window.logger.debug("Filtered available courses:", availableCourses.length);
                // Clear search box
                const availableCoursesSearch = document.getElementById('availableCoursesSearch');
                if (availableCoursesSearch) availableCoursesSearch.value = '';
                availableCoursesCurrentSearch = '';
                availableCoursesCurrentPage = 1;
                renderAvailableCourses('');
            }
        })
        .catch((err) => console.error("Error loading available courses:", err))
        .finally(() => {
            // Hide loading state
            if (window.loadingManager) window.loadingManager.hide();
        });
}



function sortCoursesForDisplay(courses) {
    return [...courses].sort((a, b) => (Number(b?.id) || 0) - (Number(a?.id) || 0));
}

function paginateItems(items, page, pageSize) {
    const safeSize = Math.max(1, Number(pageSize) || 12);
    const totalPages = Math.max(1, Math.ceil(items.length / safeSize));
    const currentPage = Math.min(Math.max(1, Number(page) || 1), totalPages);
    const start = (currentPage - 1) * safeSize;

    return {
        pageItems: items.slice(start, start + safeSize),
        totalPages,
        currentPage
    };
}

function getOrCreatePaginationContainer(listElement) {
    const containerId = `${listElement.id}-pagination`;
    let container = document.getElementById(containerId);
    if (!container) {
        container = document.createElement('div');
        container.id = containerId;
        container.className = 'course-pagination';
        listElement.insertAdjacentElement('afterend', container);
    }
    return container;
}

function renderCoursePagination(listElement, listType, totalItems, currentPage, pageSize) {
    const container = getOrCreatePaginationContainer(listElement);
    const totalPages = Math.max(1, Math.ceil(totalItems / pageSize));

    if (totalItems <= pageSize) {
        container.innerHTML = '';
        container.style.display = 'none';
        return;
    }

    const prevDisabled = currentPage <= 1 ? 'disabled' : '';
    const nextDisabled = currentPage >= totalPages ? 'disabled' : '';

    container.style.display = 'flex';
    container.innerHTML = `
      <div class="course-pagination-info">
        Showing page ${currentPage} of ${totalPages} (${totalItems} courses)
      </div>
      <div class="course-pagination-buttons">
        <button type="button" ${prevDisabled} onclick="changeCoursePage('${listType}', ${currentPage - 1})">← Prev</button>
        <button type="button" ${nextDisabled} onclick="changeCoursePage('${listType}', ${currentPage + 1})">Next →</button>
      </div>
    `;
}

function changeCoursePage(listType, page) {
    if (listType === 'my') {
        myCoursesCurrentPage = page;
        renderUserCourses(myCoursesCurrentSearch);
        return;
    }
    if (listType === 'available') {
        availableCoursesCurrentPage = page;
        renderAvailableCourses(availableCoursesCurrentSearch);
    }
}
window.changeCoursePage = changeCoursePage;

function filterCourseList(courseArray, searchText) {
    if (!searchText || searchText.trim() === "") {
        return courseArray;
    }

    const search = searchText.toLowerCase();
    return courseArray.filter((course) => {
        const titleMatch = (course.title || "").toLowerCase().includes(search);
        const descriptionMatch = (course.description || "").toLowerCase().includes(search);
        const creatorMatch = (course.creator_email || "").toLowerCase().includes(search);

        return titleMatch || descriptionMatch || creatorMatch;
    });
}

function renderUserCourses(searchText) {
    const lists = [
        document.getElementById("my-courses-list-user"),
        document.getElementById("my-courses-list-admin"),
        document.getElementById("my-courses-list-superadmin"),
    ];

    const resolvedSearch = typeof searchText === "string" ? searchText : myCoursesCurrentSearch;
    const normalizedSearch = resolvedSearch.trim();
    if (normalizedSearch !== myCoursesCurrentSearch) {
        myCoursesCurrentPage = 1;
    }
    myCoursesCurrentSearch = normalizedSearch;

    const filteredCourses = filterCourseList(myCourses, normalizedSearch);
    const pageData = paginateItems(filteredCourses, myCoursesCurrentPage, COURSE_LIST_PAGE_SIZE);
    myCoursesCurrentPage = pageData.currentPage;

    lists.forEach((list) => {
        if (!list) return;
        list.innerHTML = "";

        if (myCourses.length === 0) {
            list.innerHTML = "<li><em>No courses yet</em></li>";
            renderCoursePagination(list, "my", 0, 1, COURSE_LIST_PAGE_SIZE);
            return;
        }

        if (filteredCourses.length === 0) {
            list.innerHTML = `<li><em>No courses found matching "${escapeHtml(normalizedSearch)}"</em></li>`;
            renderCoursePagination(list, "my", 0, 1, COURSE_LIST_PAGE_SIZE);
            return;
        }

        pageData.pageItems.forEach((course) => {
            const li = document.createElement("li");
            const timeStr = formatCreationTime(course.creation_time);
            const likeCount = course.like_count || 0;

            li.className = "course-card";
            li.style.display = "block";
            li.style.listStyle = "none";
            li.dataset.courseId = String(course.id);
            li.setAttribute("data-my-course", "1");

            li.innerHTML = `
        <div class="course-card-image" style="font-size: 40px; height: 120px;">🎓</div>
        <div class="course-card-content">
          <div class="course-card-title">${escapeHtml(course.title)}</div>
          <div class="course-card-status" style="background: ${course.status === "pending" ? "rgba(255,152,0,0.1)" : "rgba(74,222,128,0.1)"}; color: ${course.status === "pending" ? "#ff9800" : "var(--success)"}">${escapeHtml(course.status?.toUpperCase()) || "UNKNOWN"}</div>
          <div class="course-progress">
             <div class="progress-text" style="display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; margin-bottom: 8px;">${escapeHtml(course.description || "No description")}</div>
             <div class="progress-text" style="margin-top: 8px; color: var(--text-muted);">❤️ ${likeCount} ${likeCount === 1 ? 'like' : 'likes'}</div>
              ${timeStr ? `<div class="progress-text" style="margin-top: 4px; font-size: 0.8em; color: var(--text-muted);">⌛ Created: ${escapeHtml(timeStr)}</div>` : ''}
              ${course.enrollment_status ? `
                <div class="progress-text" style="margin-top: 8px;">
                  <span style="
                    padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;
                    background: ${course.enrollment_status === 'completed' ? 'rgba(74,222,128,0.2)' : course.enrollment_status === 'in_progress' ? 'rgba(255,152,0,0.2)' : 'rgba(102,126,234,0.2)'};
                    color: ${course.enrollment_status === 'completed' ? 'var(--success)' : course.enrollment_status === 'in_progress' ? '#ff9800' : 'var(--primary)'};
                  ">
                    ${course.enrollment_status === 'completed' ? '✅ Completed' : course.enrollment_status === 'in_progress' ? '📚 In Progress' : '📝 Enrolled'}
                  </span>
                  ${course.course_type === 'master' && course.total_units ? `<span style="margin-left: 8px; font-size: 11px; color: var(--text-muted);">${course.completed_units || 0}/${course.total_units} units</span>` : ''}
                </div>
              ` : ''}
          </div>
          <div class="course-card-actions">
              <button onclick="editCourse(${course.id})" class="course-action-btn course-action-primary">Edit</button>
              <button onclick="viewCourse(${course.id})" class="course-action-btn course-action-secondary">View</button>
              <button onclick="deleteCourse(${course.id})" class="course-action-btn course-action-danger">Delete</button>
          </div>
        </div>
      `;
            list.appendChild(li);
            bindMyCourseContextMenu(li, course.id);
        });

        renderCoursePagination(
            list,
            "my",
            filteredCourses.length,
            myCoursesCurrentPage,
            COURSE_LIST_PAGE_SIZE
        );
    });
}

function ensureCourseContextMenu() {
    let menu = document.getElementById('course-card-context-menu');
    if (menu) return menu;
    menu = document.createElement('div');
    menu.id = 'course-card-context-menu';
    menu.className = 'course-card-context-menu';
    menu.setAttribute('role', 'menu');
    menu.style.display = 'none';
    menu.innerHTML = `<button type="button" class="course-context-item course-context-danger" data-action="delete" role="menuitem">Delete course</button>`;
    document.body.appendChild(menu);

    menu.addEventListener('click', (e) => {
        const btn = e.target.closest('[data-action]');
        if (!btn) return;
        e.preventDefault();
        e.stopPropagation();
        const courseId = parseInt(menu.dataset.courseId, 10);
        hideCourseContextMenu();
        if (btn.dataset.action === 'delete' && courseId) {
            deleteCourse(courseId);
        }
    });

    return menu;
}

function hideCourseContextMenu() {
    const menu = document.getElementById('course-card-context-menu');
    if (menu) {
        menu.style.display = 'none';
        menu.hidden = true;
    }
}

function showCourseContextMenu(clientX, clientY, courseId) {
    const menu = ensureCourseContextMenu();
    menu.dataset.courseId = String(courseId);
    menu.hidden = false;
    menu.style.display = 'block';
    menu.style.visibility = 'hidden';
    menu.style.left = '0px';
    menu.style.top = '0px';
    const rect = menu.getBoundingClientRect();
    let left = clientX;
    let top = clientY;
    if (left + rect.width > window.innerWidth - 8) left = window.innerWidth - rect.width - 8;
    if (top + rect.height > window.innerHeight - 8) top = window.innerHeight - rect.height - 8;
    menu.style.left = `${Math.max(8, left)}px`;
    menu.style.top = `${Math.max(8, top)}px`;
    menu.style.visibility = 'visible';
}

function resolveMyCourseCardFromEvent(target) {
    if (!target || !target.closest) return null;
    // Learner shell Course Creation flyout items
    const flyoutItem = target.closest('#ls-flyout-courses [data-edit-course], .ls-flyout-item[data-edit-course]');
    if (flyoutItem) return flyoutItem;

    const card = target.closest('.course-card[data-my-course="1"], .course-card[data-course-id]');
    if (!card) return null;
    // Only My Courses lists (not Available Courses)
    const inMyList = card.closest(
        '#my-courses-list-user, #my-courses-list-admin, #my-courses-list-superadmin'
    );
    if (!inMyList && card.getAttribute('data-my-course') !== '1') return null;
    if (inMyList || card.getAttribute('data-my-course') === '1') return card;
    return null;
}

function bindMyCourseContextMenu(cardEl, courseId) {
    if (!cardEl) return;
    cardEl.dataset.courseId = String(courseId);
    cardEl.setAttribute('data-my-course', '1');
    // Per-card bind kept as backup; primary handler is document capture below
    if (cardEl.dataset.contextBound === '1') return;
    cardEl.dataset.contextBound = '1';
    cardEl.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        e.stopPropagation();
        showCourseContextMenu(e.clientX, e.clientY, courseId);
    });
}

function setupMyCourseContextMenuDelegation() {
    if (document.documentElement.dataset.courseContextDelegation === '1') return;
    document.documentElement.dataset.courseContextDelegation = '1';

    // Capture phase so we beat Chrome's default menu even if something else listens later
    document.addEventListener(
        'contextmenu',
        (e) => {
            const card = resolveMyCourseCardFromEvent(e.target);
            if (!card) return;
            const courseId = parseInt(
                card.dataset.courseId ||
                    card.getAttribute('data-course-id') ||
                    card.getAttribute('data-edit-course'),
                10
            );
            if (!courseId) return;
            e.preventDefault();
            e.stopPropagation();
            if (typeof e.stopImmediatePropagation === 'function') e.stopImmediatePropagation();
            const flyout = card.closest('[data-flyout="create"]');
            if (flyout) flyout.classList.add('is-open');
            showCourseContextMenu(e.clientX, e.clientY, courseId);
        },
        true
    );

    document.addEventListener('click', (e) => {
        if (!e.target.closest('#course-card-context-menu')) hideCourseContextMenu();
    });
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') hideCourseContextMenu();
    });
    window.addEventListener('scroll', hideCourseContextMenu, true);
    window.addEventListener('blur', hideCourseContextMenu);
}

// Install immediately + on DOM ready
setupMyCourseContextMenuDelegation();
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupMyCourseContextMenuDelegation);
}
window.setupMyCourseContextMenuDelegation = setupMyCourseContextMenuDelegation;
window.showCourseContextMenu = showCourseContextMenu;
window.hideCourseContextMenu = hideCourseContextMenu;

function renderAvailableCourses(searchText) {
    const masterList = document.getElementById("available-courses-list-user");
    const singleSection = document.getElementById("single-courses-section");
    const singleList = document.getElementById("single-courses-list-user");

    // Also update admin/superadmin lists if they exist
    const adminList = document.getElementById("available-courses-list-admin");
    const superadminList = document.getElementById("available-courses-list-superadmin");

    const resolvedSearch = typeof searchText === "string" ? searchText : availableCoursesCurrentSearch;
    const normalizedSearch = resolvedSearch.trim();
    if (normalizedSearch !== availableCoursesCurrentSearch) {
        availableCoursesCurrentPage = 1;
    }
    availableCoursesCurrentSearch = normalizedSearch;

    // Browse: others' courses only. Search: all approved (incl. own) so units + masters match.
    const isSearching = normalizedSearch.length > 0;
    const searchPool = isSearching
        ? (allApprovedCourses.length ? allApprovedCourses : availableCourses)
        : availableCourses;
    const filteredCourses = filterCourseList(searchPool, normalizedSearch);

    const masterCourses = filteredCourses.filter((c) => c.course_type === "master");
    const singleCourses = filteredCourses.filter((c) => c.course_type !== "master");

    // --- Render Master Courses ---
    const masterPageData = paginateItems(masterCourses, availableCoursesCurrentPage, COURSE_LIST_PAGE_SIZE);
    availableCoursesCurrentPage = masterPageData.currentPage;

    const allMasterLists = [masterList, adminList, superadminList].filter(Boolean);
    allMasterLists.forEach((list) => {
        list.innerHTML = "";

        if (masterCourses.length === 0) {
            list.innerHTML = isSearching
                ? `<li><em>No master courses found matching "${escapeHtml(normalizedSearch)}"</em></li>`
                : "<li><em>No master courses available</em></li>";
            renderCoursePagination(list, "available", 0, 1, COURSE_LIST_PAGE_SIZE);
            return;
        }

        masterPageData.pageItems.forEach((course) => {
            list.appendChild(renderCourseCard(course));
        });

        renderCoursePagination(
            list,
            "available",
            masterCourses.length,
            availableCoursesCurrentPage,
            COURSE_LIST_PAGE_SIZE
        );
    });

    // --- Units / single courses: visible whenever searching ---
    if (singleSection) {
        if (isSearching) {
            singleSection.style.display = "block";
            if (singleList) {
                singleList.innerHTML = "";
                if (singleCourses.length === 0) {
                    singleList.innerHTML = `<li><em>No units / single courses matching "${escapeHtml(normalizedSearch)}"</em></li>`;
                } else {
                    singleCourses.forEach((course) => {
                        singleList.appendChild(renderCourseCard(course));
                    });
                }
            }
        } else {
            singleSection.style.display = "none";
            if (singleList) singleList.innerHTML = "";
        }
    }
}

function renderCourseCard(course) {
    const li = document.createElement("li");
    const isLiked = course.is_liked ? true : false;
    const likeCount = course.like_count || 0;
    const likeButtonText = isLiked ? `❤️ ${likeCount}` : `🤍 ${likeCount}`;
    const gradeLevelText = course.grade_level ? (course.grade_level === 13 ? 'College' : `Grade ${course.grade_level}`) : 'Any Level';

    li.className = "course-card";
    li.style.display = "block";
    li.style.listStyle = "none";

    li.innerHTML = `
         <div class="course-card-image" style="font-size: 40px; height: 120px;">🎓</div>
         <div class="course-card-content">
            <div class="course-card-title">${escapeHtml(course.title)}</div>
            <div class="course-card-status" style="background: rgba(102,126,234,0.1); color: var(--primary);">
              📚 ${gradeLevelText} ${course.course_type === 'master' ? '| 🎓 Master' : ''}
            </div>
            <div class="course-progress">
              <div class="progress-text" style="display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; margin-bottom: 8px;">${escapeHtml(course.description || "No description")}</div>
            </div>
            <div class="course-card-actions">
              <button onclick="viewCourse(${course.id})" class="course-action-btn course-action-secondary">View</button>
              ${course.course_type === 'master' 
                ? `<button onclick="enrollInMasterCourse(${course.id})" data-enroll-course="${course.id}" class="course-action-btn course-action-primary">Enroll (${course.units_count || 'Multi'})</button>`
                : `<button onclick="enrollInCourse(${course.id})" data-enroll-course="${course.id}" class="course-action-btn course-action-primary">Enroll</button>`
              }
              <button onclick="toggleCourseLike(${course.id}, this)" class="course-action-btn like-btn ${isLiked ? 'course-action-like-active' : 'course-action-like'}" data-course-id="${course.id}" data-liked="${isLiked}">
                ${likeButtonText}
              </button>
            </div>
          </div>
        `;
    return li;
}

function createNewCourse() {
    if (window.LearnerShell?.hideLearnerShell) window.LearnerShell.hideLearnerShell();
    currentEditingCourseId = null;
    courseBlocks = [];
    document.getElementById("course-title").value = "";
    document.getElementById("course-description").value = "";

    // Reset pagination
    coursePages = [""];
    currentPageIndex = 0;
    renderCurrentPage();

    document.getElementById("dashboard-section").style.display = "none";
    document.getElementById("course-editor-section").style.display = "block";
    updatePageControls();

    startCourseTimer(0);
    if (typeof window.onCourseEditorOpened === 'function') window.onCourseEditorOpened({ isNew: true });
}

function editCourse(courseId) {
    if (window.LearnerShell?.hideLearnerShell) window.LearnerShell.hideLearnerShell();
    const idNum = parseInt(courseId, 10);
    currentEditingCourseId = idNum;

    const openEditor = (course) => {
        if (!course) {
            alert("Course not found");
            return;
        }
        document.getElementById("course-title").value = course.title;
        document.getElementById("course-description").value =
            course.description || "";
        const videoEl = document.getElementById("course-video-url");
        if (videoEl) videoEl.value = course.video_url || "";

        // Load course type (Master vs Single)
        loadCourseTypeForEdit(idNum);

        // Split content into pages
        const rawContent = course.content || "";
        if (rawContent.includes('<hr class="page-break">')) {
            coursePages = rawContent.split('<hr class="page-break">');
        } else {
            coursePages = [rawContent];
        }
        currentPageIndex = 0;
        renderCurrentPage();

        // RESTORE SAVED BLOCKS from the course
        courseBlocks = course.blocks ?
            (typeof course.blocks === 'string' ? JSON.parse(course.blocks) : course.blocks)
            : [];

        if (window.logger) window.logger.debug("✅ Course loaded with", courseBlocks.length, "blocks");
        if (window.logger) window.logger.debug("  Blocks:", courseBlocks);

        // Load quiz questions for this course and re-render placeholders
        loadCourseQuestions(idNum).then(() => {
            const editor = document.getElementById('course-content-editor');

            // Check which question IDs already have placeholders in the saved content
            const existingPlaceholders = editor.querySelectorAll('.quiz-question-placeholder');
            const existingIds = new Set();
            existingPlaceholders.forEach(p => {
                const qId = p.dataset.questionId;
                if (qId) existingIds.add(String(qId));
            });

            // For any questions that DON'T have a placeholder in the content, add one at the end
            courseQuestions.forEach(q => {
                if (!existingIds.has(String(q.id))) {
                    insertQuizPlaceholder(q.question_text, q.id);
                }
            });

            // Re-attach handlers to existing simulators and quizzes

            // Simulators
            editor.querySelectorAll('.simulator-block').forEach(sim => {
                makeElementDraggable(sim);
            });

            // PhET Sims
            editor.querySelectorAll('.phet-sim-wrapper').forEach(wrapper => {
                makeElementDraggable(wrapper);
                const removeBtn = wrapper.querySelector('.phet-remove-btn');
                if (removeBtn) {
                    removeBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        if (confirm('Remove this simulator?')) {
                            wrapper.remove();
                        }
                    });
                }
            });

            // Quiz Placeholders - re-attach click and delete handlers
            editor.querySelectorAll('.quiz-question-placeholder').forEach(placeholder => {
                makeElementDraggable(placeholder);

                placeholder.addEventListener('click', (e) => {
                    if (e.target.closest('button')) return;
                    const qId = placeholder.dataset.questionId;
                    if (qId) {
                        openQuizModal(parseInt(qId));
                    }
                });

                const deleteBtn = placeholder.querySelector('.quiz-placeholder-delete-btn');
                if (deleteBtn) {
                    deleteBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        const qId = parseInt(placeholder.dataset.questionId);
                        if (confirm('Delete this question?')) {
                            deleteQuizQuestion(qId);
                        }
                    });
                }
            });

            document.getElementById("dashboard-section").style.display = "none";
            document.getElementById("course-editor-section").style.display = "block";
            if (typeof normalizeAbsoluteEmbeds === 'function') normalizeAbsoluteEmbeds(editor);
            updatePageControls();

            startCourseTimer(course.creation_time || 0);
            if (typeof window.onCourseEditorOpened === 'function') {
                window.onCourseEditorOpened({ isNew: false, courseId: idNum });
            }
        });
    };

    let course = myCourses.find((c) => Number(c.id) === idNum);
    if (course && course.content != null) {
        openEditor(course);
        return Promise.resolve();
    }

    const token = authToken || localStorage.getItem("token") || "";
    return fetch(`${API_BASE_URL}/api/courses/${idNum}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
        credentials: "include"
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success && data.data) {
                course = { ...data.data, id: Number(data.data.id) };
                if (!myCourses.some((c) => Number(c.id) === idNum)) myCourses.push(course);
                openEditor(course);
            } else {
                alert("Course not found");
            }
        })
        .catch((err) => {
            console.error("Failed to load course for edit:", err);
            alert("Course not found");
        });
}

function saveCourse(action = "draft", options = {}) {
    const quiet = !!(options && options.quiet);
    const title = document.getElementById("course-title").value;
    const description = document.getElementById("course-description").value;
    const gradeLevel = document.getElementById("course-grade-level").value;
    const videoUrl = document.getElementById("course-video-url").value;
    
    // Get course type from radio buttons
    const courseTypeRadios = document.getElementsByName("course_type");
    let courseType = "single";
    for (const radio of courseTypeRadios) {
        if (radio.checked) {
            courseType = radio.value;
            break;
        }
    }

    // Save current page content before gathering all content
    saveCurrentPageContent();

    // Join all pages with delimiter
    const fullContent = coursePages.join('<hr class="page-break">');

    // DO NOT remove quiz placeholders. They are needed for the viewer to know where to render quizzes.
    // The viewer will replace them with interactive elements.
    const content = fullContent;

    if (!title.trim()) {
        if (!quiet) alert("Please enter a course title");
        if (typeof window.setEditorAutosaveStatus === 'function') {
            window.setEditorAutosaveStatus('Add a title to auto-save');
        }
        return Promise.resolve(false);
    }

    // Set course status based on action
    const status = action === "pending" ? "pending" : "draft";

    if (window.logger) {
        window.logger.debug(`\n=== SAVE COURSE DEBUG ===`);
        window.logger.debug(`Action: ${action}`);
        window.logger.debug(`Status to save: ${status}`);
        window.logger.debug(`Course Type: ${courseType}`);
        window.logger.debug(`Title: "${title}"`);
        window.logger.debug(`Description: "${description}"`);
        window.logger.debug(`Content HTML length: ${content.length}`);
        window.logger.debug(`courseBlocks count: ${courseBlocks.length}`);
        window.logger.debug(`courseBlocks:`, courseBlocks);
    }

    const url = currentEditingCourseId
        ? `${API_BASE_URL}/api/courses/${currentEditingCourseId}`
        : `${API_BASE_URL}/api/courses`;

    const method = currentEditingCourseId ? "PUT" : "POST";

    if (window.logger) window.logger.debug(`Sending ${method} request to ${url}`);

    const courseData = {
        title,
        description,
        grade_level: gradeLevel ? parseInt(gradeLevel) : null,
        content,
        blocks: JSON.stringify(courseBlocks), // Save the blocks array
        status: status,
        creation_time: courseTimer.totalSeconds,
        video_url: videoUrl || null,
        course_type: courseType
    };

    // Already replaced above
    if (window.logger) window.logger.debug(`Payload:`, courseData);

    if (quiet && typeof window.setEditorAutosaveStatus === 'function') {
        window.setEditorAutosaveStatus('Saving…');
    }

    return fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authToken}`,
        },
        credentials: "include",
        body: JSON.stringify(courseData),
    })
        .then((res) => res.json())
        .then((data) => {
            if (window.logger) window.logger.debug(`Response:`, data);
            if (data.success) {
                // Set currentEditingCourseId if this was a new course
                if (!currentEditingCourseId) {
                    currentEditingCourseId = data.data?.id || data.data;
                    if (window.logger) window.logger.debug("✅ New course saved, currentEditingCourseId set to:", currentEditingCourseId);
                    if (typeof window.onCourseDraftIdAssigned === 'function') {
                        window.onCourseDraftIdAssigned(currentEditingCourseId);
                    }
                }

                if (!quiet) {
                    const message =
                        action === "pending"
                            ? "Course submitted for approval!"
                            : "Course saved as draft!";
                    alert(message);
                } else if (typeof window.setEditorAutosaveStatus === 'function') {
                    const t = new Date();
                    window.setEditorAutosaveStatus(
                        `Saved ${t.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })}`
                    );
                }

                // INSTANT: Stay in editor, just reload course data in background
                loadUserCourses();
                if (action === "pending") {
                    loadPendingCourses();
                }

                // DON'T navigate away - stay in editor for seamless quiz editing
                // showDashboard(); // REMOVED - user wants to stay in editor
                return true;
            } else {
                if (!quiet) alert(`Error: ${data.message || "Failed to save course"}`);
                else if (typeof window.setEditorAutosaveStatus === 'function') {
                    window.setEditorAutosaveStatus('Auto-save failed');
                }
                return false;
            }
        })
        .catch((err) => {
            console.error("Error saving course:", err);
            if (!quiet) alert("Error saving course. Check console for details.");
            else if (typeof window.setEditorAutosaveStatus === 'function') {
                window.setEditorAutosaveStatus('Auto-save failed');
            }
            return false;
        });
}

// Global variables for tracking context
let currentAssignmentId = null;

async function viewCourse(courseId, assignmentId = null, forceRegular = false) {
    if (window.LearnerShell?.hideLearnerShell) window.LearnerShell.hideLearnerShell();
    currentAssignmentId = assignmentId;
    const idNum = parseInt(courseId, 10);

    let course =
        myCourses.find((c) => Number(c.id) === idNum) ||
        availableCourses.find((c) => Number(c.id) === idNum) ||
        pendingCourses.find((c) => Number(c.id) === idNum);

    // Learner shell often has empty local lists — hydrate from API
    if (!course || course.content == null || course.content === undefined) {
        try {
            const token = authToken || localStorage.getItem("token") || "";
            const res = await fetch(`${API_BASE_URL}/api/courses/${idNum}`, {
                headers: token ? { Authorization: `Bearer ${token}` } : {},
                credentials: "include"
            });
            const data = await res.json();
            if (data.success && data.data) {
                const full = { ...data.data, id: Number(data.data.id) };
                if (course) {
                    Object.assign(course, full);
                } else {
                    course = full;
                    if (!availableCourses.some((c) => Number(c.id) === idNum)) {
                        availableCourses.push(course);
                    }
                }
            }
        } catch (err) {
            console.error("Failed to fetch course for view:", err);
        }
    }

    if (assignmentId && course) {
        localStorage.setItem('activeAssignmentId', assignmentId);
        setTimeout(() => {
            updateStudentActiveStatus("Active on Course: " + course.title);
        }, 500);
    } else {
        localStorage.removeItem('activeAssignmentId');
    }

    if (!course) {
        alert("Course not found");
        return;
    }

    currentViewingCourseId = idNum;
    courseId = idNum;

    // Creator of a master course: use creator preview (loads units without enrollment)
    const isCreator = Number(course.creator_id) === Number(currentUser?.id);
    const isMaster = course.course_type === 'master';
    if (isCreator && isMaster && !forceRegular) {
        return viewCreatorMasterCoursePreview(courseId);
    }

    // Check if user is enrolled in this course (but NOT the creator - creators aren't "enrolled")
    const isEnrolledStudent = !isCreator && myCourses.some(c => Number(c.id) === idNum);
    
    if (isEnrolledStudent && !forceRegular) {
        // Use enhanced navigation for enrolled students (supports master courses)
        return viewCourseWithNavigation(courseId);
    }

    // For non-enrolled users, use regular view
    // Load questions first so hydration works
    await loadCourseQuestions(courseId);

    // Hide unit navigation sidebar, show regular sidebar
    const unitSidebar = document.getElementById("unit-navigation-sidebar");
    const regularSidebar = document.getElementById("viewer-regular-sidebar");
    if (unitSidebar) unitSidebar.style.display = "none";
    if (regularSidebar) regularSidebar.style.display = "block";

    document.getElementById("dashboard-section").style.display = "none";
    document.getElementById("course-editor-section").style.display = "none";
    document.getElementById("course-viewer-section").style.display = "block";
    enterCourseViewerMode(courseId);

    // Handle Video Logic
    const videoContainer = document.getElementById("viewer-video-container");
    const videoIframe = document.getElementById("viewer-video-iframe");
    const videoLink = document.getElementById("viewer-video-link");
    const noVideoPlaceholder = document.getElementById("viewer-no-video");

    const embedUrl = getYoutubeEmbedUrl(course.video_url);
    if (embedUrl) {
        videoIframe.src = embedUrl;
        videoLink.href = course.video_url;
        videoContainer.style.display = "block";
        noVideoPlaceholder.style.display = "none";
    } else {
        videoIframe.src = "";
        videoContainer.style.display = "none";
        noVideoPlaceholder.style.display = "block";
    }

    const viewerContent = document.getElementById("course-viewer-content");

    // Split content into pages for viewer
    const rawContent = course.content || "";
    let viewerPages = [];
    if (rawContent.includes('<hr class="page-break">')) {
        viewerPages = rawContent.split('<hr class="page-break">');
    } else {
        viewerPages = [rawContent];
    }

    let currentViewerPageIndex = 0;

    const renderViewerPage = (index) => {
        viewerContent.innerHTML = `
         <h1>${escapeHtml(course.title)}</h1>
         <p><strong>Description:</strong> ${escapeHtml(course.description || "No description")}</p>
         <div id="course-content-display" style="margin: 20px 0; position: relative; min-height: 400px;">
             ${viewerPages[index] || "No content"}
         </div>
         <button onclick="showDashboard()" style="padding: 8px 16px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer;">Back to Dashboard</button>
     `;

        // Update viewer controls
        const indicator = document.getElementById("viewer-page-indicator");
        const prevBtn = document.getElementById("viewer-prev-btn");
        const nextBtn = document.getElementById("viewer-next-btn");

        if (indicator) indicator.textContent = `Page ${index + 1} of ${viewerPages.length}`;
        if (prevBtn) prevBtn.disabled = index === 0;
        if (nextBtn) {
            if (index === viewerPages.length - 1) {
                nextBtn.textContent = "Finish Course";
            } else {
                nextBtn.textContent = "Next Page";
            }
        }

        // Re-attach event listeners for interactive elements (quizzes, sims)
        // We need to wait for DOM update AND for MathJax to be ready
        setTimeout(async () => {
            // Trigger MathJax to render any LaTeX equations on the page
            if (window.MathJax && window.MathJax.typesetPromise) {
                try {
                    await window.MathJax.typesetPromise([document.getElementById('course-content-display')]);
                    if (window.logger) window.logger.debug('✅ MathJax rendered LaTeX equations');
                } catch (err) {
                    console.error('MathJax rendering error:', err);
                }
            }

            if (typeof setupViewerInteractions === 'function') {
                setupViewerInteractions(course.id);
            } else {
                console.error("setupViewerInteractions is NOT defined!");
            }
            // Convert simulator buttons for this page
            convertSimulatorButtonsForViewer(course.id, course);

            // Render LaTeX - CRITICAL: Must wait for MathJax to be fully loaded
            if (window.MathJax && window.MathJax.typesetPromise) {
                try {
                    if (window.logger) window.logger.debug("🔵 MathJax: Typesetting course content...");
                    const contentDisplay = document.getElementById("course-content-display");
                    if (contentDisplay) {
                        await window.MathJax.typesetPromise([contentDisplay]);
                        if (window.logger) window.logger.debug("✅ MathJax: Content typeset successfully");
                    }
                } catch (err) {
                    console.error("❌ MathJax error:", err);
                }
            } else {
                console.warn("⚠️ MathJax not available or typesetPromise not loaded");
            }
        }, 100);
    };

    // Define setupViewerInteractions if it's not already defined globally
    // This function attaches event listeners to interactive elements in the viewer
    function setupViewerInteractions(courseId) {
        if (window.logger) window.logger.debug("Setting up viewer interactions for course:", courseId);

        // Hydrate quiz placeholders first
        hydrateQuizPlaceholders();

        // Hydrate simulator placeholders (converts editor buttons to Run buttons)
        hydrateSimulatorPlaceholders();

        // Re-attach listeners for quizzes
        document.querySelectorAll(".quiz-submit-btn").forEach((btn) => {
            btn.addEventListener("click", (e) => {
                const questionId = e.target.dataset.questionId;
                submitQuizAnswer(questionId, courseId);
            });
        });
    }

    // Setup viewer pagination controls
    const viewerControls = document.getElementById("viewer-pagination-controls");
    if (viewerControls) {
        // Clear old listeners by cloning
        const newPrev = viewerControls.querySelector("#viewer-prev-btn").cloneNode(true);
        const newNext = viewerControls.querySelector("#viewer-next-btn").cloneNode(true);
        viewerControls.querySelector("#viewer-prev-btn").replaceWith(newPrev);
        viewerControls.querySelector("#viewer-next-btn").replaceWith(newNext);

        newPrev.addEventListener("click", () => {
            if (currentViewerPageIndex > 0) {
                currentViewerPageIndex--;
                renderViewerPage(currentViewerPageIndex);
            }
        });

        newNext.addEventListener("click", () => {
            if (currentViewerPageIndex < viewerPages.length - 1) {
                currentViewerPageIndex++;
                renderViewerPage(currentViewerPageIndex);
            } else {
                // Finish course logic
                if (currentAssignmentId) {
                    if (window.logger) window.logger.debug(`Course finished, auto-submitting assignment ${currentAssignmentId}`);
                    submitAssignmentWork(currentAssignmentId, course.title);
                } else {
                    alert('Congratulations! You have completed the course content.');
                }
                showDashboard();
            }
        });
    }

    // Render first page immediately
    renderViewerPage(0);

    // Set currentEditingCourseId for quiz answer submission
    currentEditingCourseId = courseId;
}

function convertSimulatorButtonsForViewer(courseId, course) {
    // Load courseBlocks from the course
    courseBlocks = course.blocks ?
        (typeof course.blocks === 'string' ? JSON.parse(course.blocks) : course.blocks)
        : [];

    // Find all simulator blocks in the viewer
    const simulatorDivs = document.querySelectorAll('.simulator-block');
    simulatorDivs.forEach((div) => {
        const blockId = parseInt(div.dataset.blockId);
        const buttons = div.querySelectorAll('button');

        // Replace Edit/Remove buttons with Run button
        buttons.forEach((btn) => {
            if (btn.textContent.includes('Edit')) {
                btn.textContent = '▶ Run Simulator';
                btn.style.cssText = 'background:#10b981;color:#fff;padding:10px 20px;border:none;border-radius:8px;cursor:pointer;font-weight:600;font-size:1em;transition:transform .2s;';
                btn.onmouseenter = () => { btn.style.transform = 'scale(1.05)'; };
                btn.onmouseleave = () => { btn.style.transform = 'scale(1)'; };
                btn.onclick = () => runEmbeddedBlockSimulator(blockId, div.querySelector('strong')?.textContent || 'Simulator');
            } else if (btn.textContent.includes('Remove')) {
                btn.style.display = 'none';
            }
        });

        // Add fullscreen hint below buttons
        if (!div.querySelector('.sim-fs-hint')) {
            const hint = document.createElement('p');
            hint.className = 'sim-fs-hint';
            hint.style.cssText = 'color:#94a3b8;font-size:.8em;margin-top:6px;font-style:italic;';
            hint.textContent = '💡 Press F inside the simulator for fullscreen';
            div.appendChild(hint);
        }
    });
}

function runEmbeddedBlockSimulator(blockId, title) {
    // Find the block
    const block = courseBlocks.find((b) => b.id === blockId);
    if (!block) {
        alert("Simulator not found");
        return;
    }

    if (window.logger) {
        window.logger.debug('🎮 Running simulator:', blockId, 'Type:', block.type);
        window.logger.debug('   Simulator data:', block.data);
    }

    if (block.type === 'block-simulator') {
        const baseUrl = window.location.pathname.includes('github.io')
            ? 'https://virat-sisodiya.github.io/Veelearn/veelearn-frontend'
            : window.location.origin;

        // New Scratch-format sims → player (stage + interactivity, no code editor)
        if (isScratchSimulatorData(block.data) || !Array.isArray(block.data?.blocks)) {
            openScratchPlayerEmbed(block, title, baseUrl);
            return;
        }

        // Legacy node/wire sims → old studio viewer
        const popup = window.open(
            `${baseUrl}/simulator-studio.html?embedded=true&courseBlockId=${blockId}&t=${Date.now()}`,
            "simulator-studio",
            "width=1400,height=900"
        );

        if (popup) {
            setTimeout(() => {
                popup.postMessage(
                    {
                        type: "load-simulator",
                        blocks: block.data?.blocks || [],
                        connections: block.data?.connections || [],
                        blockTitle: title,
                        courseBlockId: blockId,
                    },
                    "*"
                );
            }, 500);
        }
    } else if (block.type === 'marketplace-simulator') {
        // Marketplace sims live on the server — run them by id via the shared viewer
        const simulatorId = block.simulatorId || block.data?.simulatorId;
        if (!simulatorId) {
            alert("Simulator reference is missing");
            return;
        }
        viewSimulatorInStudio(simulatorId);
    } else if (block.type === 'visual-simulator') {
        // Run visual/code-based simulator
        const baseUrl = window.location.pathname.includes('github.io')
            ? 'https://virat-sisodiya.github.io/Veelearn/veelearn-frontend'
            : window.location.origin;
        const popup = window.open(
            `${baseUrl}/visual-simulator.html?embedded=true`,
            "visual-simulator",
            "width=1200,height=800"
        );

        if (popup) {
            setTimeout(() => {
                popup.postMessage(
                    {
                        type: "load-code",
                        code: block.data?.code || "",
                        variables: block.data?.variables || {},
                        courseBlockId: blockId,
                    },
                    "*"
                );
            }, 500);
        }
    }
}

function runEmbeddedVisualSimulator(blockId, title) {
    const block = courseBlocks.find((b) => b.id === blockId);
    if (!block) {
        alert("Simulator not found");
        return;
    }

    const baseUrl = window.location.pathname.includes('github.io')
        ? 'https://virat-sisodiya.github.io/Veelearn/veelearn-frontend'
        : window.location.origin;
    const popup = window.open(
        `${baseUrl}/visual-simulator.html?embedded=true`,
        "visual-simulator",
        "width=1200,height=800"
    );

    if (popup) {
        popup.onload = () => {
            popup.postMessage(
                {
                    type: "loadEmbeddedCode",
                    code: block.data?.code || "",
                    variables: block.data?.variables || {},
                },
                "*"
            );
        };
    }
}

function loadCourseSimulators(courseId) {
    // Display simulators from courseBlocks
    displayCourseSimulators(courseBlocks);
}

function displayCourseSimulators(blocks) {
    const viewerContent = document.getElementById("course-viewer-content");
    if (!blocks || blocks.length === 0) return;

    const simulatorSection = document.createElement("div");
    simulatorSection.style.marginTop = "30px";
    simulatorSection.innerHTML = "<h2>📊 Simulators</h2>";

    blocks.forEach((block) => {
        if (block.type.includes("simulator")) {
            const simulatorDiv = document.createElement("div");
            simulatorDiv.className = "simulator-block";
            simulatorDiv.dataset.blockId = block.id;
            simulatorDiv.style.cssText =
                "background: #f0f0f0; padding: 15px; margin: 10px 0; border-left: 4px solid #4caf50; border-radius: 4px;";
            simulatorDiv.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>${block.title}</strong>
                        <p style="margin: 5px 0; color: #666;">Type: ${block.type}</p>
                    </div>
                    <button type="button" style="padding: 8px 16px; background: #4caf50; color: white; border: none; border-radius: 4px; cursor: pointer;">▶ Run Simulator</button>
                </div>
            `;
            simulatorSection.appendChild(simulatorDiv);
        }
    });

    viewerContent.appendChild(simulatorSection);
}

function viewSimulator(simulatorId) {
    viewSimulatorInStudio(simulatorId);
}

function deleteCourse(courseId) {
    if (!confirm("Are you sure?")) return;

    fetch(`${API_BASE_URL}/api/courses/${courseId}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${authToken}` },
        credentials: "include"
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                alert("Course deleted!");
                // INSTANT: Remove from array immediately
                myCourses = myCourses.filter((c) => c.id !== courseId);
                // INSTANT: Render immediately without reload
                renderUserCourses();
                if (typeof window.LearnerShell?.refreshCourseFlyout === 'function') {
                    window.LearnerShell.refreshCourseFlyout();
                }
            } else {
                alert("Error: " + data.message);
            }
        })
        .catch((err) => {
            console.error("Error deleting course:", err);
            alert("Error deleting course. Check console.");
        });
}

function enrollInCourse(courseId) {
    fetch(`${API_BASE_URL}/api/courses/${courseId}/enroll`, {
        method: "POST",
        headers: { Authorization: `Bearer ${authToken}` },
        credentials: "include"
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                alert("Enrolled successfully!");
                // INSTANT: Update available courses list immediately
                availableCourses = availableCourses.filter((c) => c.id !== courseId);
                // INSTANT: Also reload in case there are other updates
                loadAvailableCourses();
                loadUserCourses();
                if (typeof loadEnrolledCourses === 'function') {
                    loadEnrolledCourses();
                }
            } else {
                alert("Error: " + data.message);
            }
        })
        .catch((err) => {
            console.error("Error enrolling:", err);
            alert("Error enrolling in course");
        });
}

function openScratchPlayerEmbed(block, title, baseUrl) {
    const existing = document.getElementById('scratch-player-modal');
    if (existing) existing.remove();

    const modal = document.createElement('div');
    modal.id = 'scratch-player-modal';
    modal.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,.75);z-index:10000;display:flex;align-items:center;justify-content:center;padding:20px;';
    modal.innerHTML = `
      <div style="background:#09090b;border-radius:12px;padding:12px;max-width:540px;width:100%;box-shadow:0 20px 60px rgba(0,0,0,.5);">
        <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;margin:0 4px 10px;">
          <h3 style="color:#fafafa;margin:0;font-size:16px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${escapeHtml(title || 'Simulator')}</h3>
          <button id="scratch-player-close" style="flex-shrink:0;background:#27272a;border:none;color:#fafafa;font-size:16px;cursor:pointer;border-radius:6px;width:28px;height:28px;line-height:1;">&times;</button>
        </div>
        <iframe id="scratch-player-frame" src="${baseUrl}/scratch-player.html?embedded=true&t=${Date.now()}"
          style="width:100%;height:500px;border:none;border-radius:8px;background:#111;" allowfullscreen></iframe>
      </div>`;
    document.body.appendChild(modal);
    modal.querySelector('#scratch-player-close').onclick = () => modal.remove();
    modal.addEventListener('click', (e) => { if (e.target === modal) modal.remove(); });

    const frame = modal.querySelector('#scratch-player-frame');
    const project = getScratchProjectFromData(block.data);
    frame.onload = () => {
        frame.contentWindow.postMessage({
            type: 'load-simulator',
            data: project || block.data,
            blockTitle: title,
            autoRun: true
        }, '*');
    };
}

function handleEditSimulator(event, blockId) {
    event.preventDefault();
    event.stopPropagation();

    const block = courseBlocks.find((b) => b.id === blockId);
    if (!block) {
        console.error("Block not found:", blockId);
        return;
    }

    if (window.logger) window.logger.debug("Opening simulator for editing:", block);
    currentEditingSimulatorBlockId = blockId; // Store for saving later

    if (block.type === "block-simulator") {
        const baseUrl = window.location.pathname.includes('github.io')
            ? 'https://virat-sisodiya.github.io/Veelearn/veelearn-frontend'
            : window.location.origin;

        const useScratch = isScratchSimulatorData(block.data) || !Array.isArray(block.data?.blocks);
        const studioUrl = useScratch
            ? `${baseUrl}/scratch-studio.html?edit=true&courseBlockId=${blockId}&t=${Date.now()}`
            : `${baseUrl}/simulator-studio.html?edit=true&courseBlockId=${blockId}&t=${Date.now()}`;

        const popup = window.open(studioUrl, "simulator-studio-editor", "width=1400,height=900");

        if (popup && useScratch) {
            // The scratch studio loads Blockly from a CDN, so its message listener may
            // not exist yet when a fixed timeout fires. Use a ready-handshake
            // (studio posts 'studio-ready') plus a retry-until-ack fallback so the
            // project payload is never lost — losing it would make the studio open
            // blank and overwrite the real project on exit.
            const project = getScratchProjectFromData(block.data);
            const payload = {
                type: "load-simulator",
                data: project || { format: 'veelearn-scratch-1' },
                blockTitle: block.title,
                courseBlockId: blockId,
            };

            let acked = false;
            let retryTimer = null;

            const sendLoad = () => {
                if (acked || popup.closed) return;
                try {
                    popup.postMessage(payload, "*");
                } catch (err) {
                    console.warn("Failed to post load-simulator to studio:", err);
                }
            };

            const cleanup = () => {
                window.removeEventListener("message", onStudioMessage);
                if (retryTimer) clearInterval(retryTimer);
            };

            const onStudioMessage = (e) => {
                if (!e.data || !e.data.type) return;
                const fromPopup = e.source === popup;
                const sameBlock = String(e.data.courseBlockId) === String(blockId);
                if (!fromPopup && !sameBlock) return;

                if (e.data.type === "studio-ready") {
                    sendLoad();
                } else if (e.data.type === "load-simulator-ack") {
                    acked = true;
                    cleanup();
                }
            };
            window.addEventListener("message", onStudioMessage);

            // Fallback: retry every 400ms until acked, give up after ~10s
            retryTimer = setInterval(() => {
                if (acked || popup.closed) {
                    cleanup();
                    return;
                }
                sendLoad();
            }, 400);
            setTimeout(cleanup, 10000);
        } else if (popup) {
            // Legacy node/wire studio — original single-shot delivery
            setTimeout(() => {
                popup.postMessage(
                    {
                        type: "load-simulator",
                        data: {
                            blocks: block.data?.blocks || [],
                            connections: block.data?.connections || []
                        },
                        blockTitle: block.title,
                        courseBlockId: blockId,
                    },
                    "*"
                );
            }, 500);
        }
    } else if (block.type === "marketplace-simulator") {
        // Marketplace sims are stored on the server; open the studio on the sim id.
        // The studio loads it via ?simId= and saves back to the marketplace (PUT).
        const simulatorId = block.simulatorId || block.data?.simulatorId;
        if (!simulatorId) {
            alert("Simulator reference is missing");
            return;
        }
        const baseUrl = window.location.pathname.includes('github.io')
            ? 'https://virat-sisodiya.github.io/Veelearn/veelearn-frontend'
            : window.location.origin;
        window.open(
            `${baseUrl}/scratch-studio.html?simId=${simulatorId}&t=${Date.now()}`,
            "simulator-studio-editor",
            "width=1400,height=900"
        );
    } else if (block.type === "visual-simulator") {
        const baseUrl = window.location.pathname.includes('github.io')
            ? 'https://virat-sisodiya.github.io/Veelearn/veelearn-frontend'
            : window.location.origin;
        const popup = window.open(
            `${baseUrl}/visual-simulator.html?edit=true&courseBlockId=${blockId}&t=${Date.now()}`,
            "visual-simulator-editor",
            "width=1200,height=800"
        );

        if (popup) {
            setTimeout(() => {
                popup.postMessage(
                    {
                        type: "load-code",
                        code: block.data?.code || "",
                        variables: block.data?.variables || {},
                        courseBlockId: blockId,
                    },
                    "*"
                );
            }, 500);
        }
    }
}


function handleRemoveSimulator(event, blockId) {
    event.preventDefault();
    event.stopPropagation();

    if (!confirm("Remove this simulator from the course?")) return;

    courseBlocks = courseBlocks.filter((b) => b.id !== blockId);

    const simulatorDiv = document.querySelector(`[data-block-id="${blockId}"]`);
    if (simulatorDiv) {
        simulatorDiv.remove();
    }

    if (window.logger) window.logger.debug("Simulator removed. Remaining blocks:", courseBlocks);
}

// ===== QUIZ FUNCTIONALITY =====
function setupQuizModalListeners() {
    const insertQuizBtn = document.getElementById('insert-quiz-question');
    const quizModal = document.getElementById('quiz-modal');
    const closeQuizModal = document.getElementById('close-quiz-modal');
    const cancelQuizModal = document.getElementById('cancel-quiz-modal');
    const quizForm = document.getElementById('quiz-question-form');
    const questionTypeSelect = document.getElementById('quiz-question-type');
    const optionsContainer = document.getElementById('quiz-options-container');
    const addOptionBtn = document.getElementById('add-quiz-option');

    if (insertQuizBtn) {
        insertQuizBtn.addEventListener('click', () => {
            if (!currentEditingCourseId) {
                alert('⚠️ Please save the course first ("Save as Draft") before adding quiz questions.');
                return;
            }
            openQuizModal();
        });
    }

    const deleteQuizBtn = document.getElementById('delete-quiz-question');
    if (deleteQuizBtn) {
        deleteQuizBtn.addEventListener('click', () => {
            if (currentEditingQuestionId) {
                if (window.logger) window.logger.debug('🗑️ Modal delete button clicked for question:', currentEditingQuestionId);
                deleteQuizQuestion(currentEditingQuestionId);
            } else {
                console.warn('⚠️ No question selected for deletion');
            }
        });
    }

    if (closeQuizModal) {
        closeQuizModal.addEventListener('click', () => {
            closeQuizModalFunc();
        });
    }

    if (cancelQuizModal) {
        cancelQuizModal.addEventListener('click', () => {
            closeQuizModalFunc();
        });
    }

    if (quizForm) {
        quizForm.addEventListener('submit', (e) => {
            e.preventDefault();
            saveQuizQuestion();
        });
    }

    if (questionTypeSelect) {
        questionTypeSelect.addEventListener('change', (e) => {
            const val = e.target.value;
            const imgUpload = document.getElementById('quiz-image-upload-container');
            const partsContainer = document.getElementById('quiz-parts-container');
            const singleAnswer = document.getElementById('quiz-correct-answer-container');
            
            optionsContainer.style.display = val === 'multiple_choice' ? 'block' : 'none';
            if (imgUpload) imgUpload.style.display = val === 'fill_in_blank_with_image' ? 'block' : 'none';
            if (partsContainer) partsContainer.style.display = val === 'fill_in_blank_with_image' ? 'block' : 'none';
            if (singleAnswer) singleAnswer.style.display = val === 'fill_in_blank_with_image' ? 'none' : 'block';
        });
    }

    const addPartBtn = document.getElementById('add-quiz-part');
    if (addPartBtn) {
        addPartBtn.addEventListener('click', () => {
            const partsList = document.getElementById('quiz-parts-list');
            const partCount = partsList.querySelectorAll('.quiz-part-item').length + 1;
            const newPart = document.createElement('div');
            newPart.className = 'quiz-part-item';
            newPart.style.display = 'flex';
            newPart.style.gap = '10px';
            newPart.style.marginBottom = '10px';
            newPart.innerHTML = `
                <input type="text" class="quiz-part-label" placeholder="Part Label (e.g. part ${String.fromCharCode(96 + partCount)})" style="flex: 1;" />
                <input type="text" class="quiz-part-answer" placeholder="Correct Answer" style="flex: 1;" />
                <input type="text" class="quiz-part-unit" placeholder="Unit (e.g. ft/min)" style="flex: 1;" />
            `;
            partsList.appendChild(newPart);
        });
    }

    const imgUpload = document.getElementById('quiz-image-upload');
    const imgPreview = document.getElementById('quiz-image-preview');
    const removeImgBtn = document.getElementById('remove-quiz-image');
    
    if (imgUpload && imgPreview && removeImgBtn) {
        imgUpload.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    imgPreview.style.display = 'block';
                    imgPreview.querySelector('img').src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
        removeImgBtn.addEventListener('click', () => {
            imgUpload.value = '';
            imgPreview.style.display = 'none';
            imgPreview.querySelector('img').src = '';
        });
    }

    if (addOptionBtn) {
        addOptionBtn.addEventListener('click', () => {
            const optionsList = document.getElementById('quiz-options-list');
            const optionCount = optionsList.querySelectorAll('.quiz-option-input').length + 1;
            const newOption = document.createElement('input');
            newOption.type = 'text';
            newOption.className = 'quiz-option-input';
            newOption.placeholder = `Option ${optionCount}`;
            optionsList.appendChild(newOption);
        });
    }

    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === quizModal) {
            quizModal.style.display = 'none';
            resetQuizForm();
            currentEditingQuestionId = null;
        }
    });

    // Delegated listener for quiz placeholders in the editor
    const editor = document.getElementById('course-content-editor');
    if (editor) {
        // Handle delete button clicks
        editor.addEventListener('click', (e) => {
            const deleteBtn = e.target.closest('.quiz-placeholder-delete-btn');
            if (deleteBtn) {
                e.preventDefault();
                e.stopPropagation();
                const questionId = parseInt(deleteBtn.dataset.questionId);
                if (window.logger) window.logger.debug(`🗑️ DELETE clicked for question:`, questionId);
                deleteQuizQuestion(questionId);
                return;
            }

            // Handle edit (click on placeholder, not on button)
            const placeholder = e.target.closest('.quiz-question-placeholder');
            if (placeholder && !e.target.closest('button')) {
                const questionId = placeholder.dataset.questionId;
                if (questionId) {
                    if (window.logger) window.logger.debug(`📝 EDIT clicked for question:`, questionId);
                    openQuizModal(parseInt(questionId));
                }
            }
        });
    }
}

function openQuizModal(questionId = null) {
    const quizModal = document.getElementById('quiz-modal');
    const modalTitle = document.getElementById('quiz-modal-title');
    const deleteBtn = document.getElementById('delete-quiz-question');

    if (!quizModal) return;

    currentEditingQuestionId = questionId;

    if (questionId) {
        // Editing existing question
        modalTitle.textContent = 'Edit Quiz Question';
        if (deleteBtn) deleteBtn.style.display = 'inline-block';

        const question = courseQuestions.find(q => q.id === questionId);
        if (question) {
            document.getElementById('quiz-question-text').value = question.question_text;
            document.getElementById('quiz-question-type').value = question.question_type;
            document.getElementById('quiz-correct-answer').value = question.correct_answer;

            // Load blocks into simulator editor if using it
            document.getElementById('quiz-explanation').value = question.explanation || '';
            document.getElementById('quiz-points').value = question.points;

            if (question.question_type === 'multiple_choice' && question.options) {
                const optionsList = document.getElementById('quiz-options-list');
                optionsList.innerHTML = '';
                question.options.forEach((option, index) => {
                    const input = document.createElement('input');
                    input.type = 'text';
                    input.className = 'quiz-option-input';
                    input.placeholder = `Option ${index + 1}`;
                    input.value = option;
                    optionsList.appendChild(input);
                });
                document.getElementById('quiz-options-container').style.display = 'block';
            } else {
                document.getElementById('quiz-options-container').style.display = 'none';
            }
        }
    } else {
        // Creating new question
        modalTitle.textContent = 'Add Quiz Question';
        if (deleteBtn) deleteBtn.style.display = 'none';
        resetQuizForm();
    }

    quizModal.style.display = 'block';
}

function closeQuizModalFunc() {
    const quizModal = document.getElementById('quiz-modal');
    if (quizModal) {
        quizModal.style.display = 'none';
        resetQuizForm();
        currentEditingQuestionId = null;
    }
}

function resetQuizForm() {
    document.getElementById('quiz-question-text').value = '';
    document.getElementById('quiz-question-type').value = 'multiple_choice';
    document.getElementById('quiz-correct-answer').value = '';
    document.getElementById('quiz-explanation').value = '';
    document.getElementById('quiz-points').value = '10';

    const optionsList = document.getElementById('quiz-options-list');
    if (optionsList) {
        optionsList.innerHTML = `
      <input type="text" class="quiz-option-input" placeholder="Option 1" />
      <input type="text" class="quiz-option-input" placeholder="Option 2" />
      <input type="text" class="quiz-option-input" placeholder="Option 3" />
      <input type="text" class="quiz-option-input" placeholder="Option 4" />
    `;
    }

    const optionsContainer = document.getElementById('quiz-options-container');
    if (optionsContainer) {
        optionsContainer.style.display = 'block';
    }
}

async function saveQuizQuestion() {
    let questionText = document.getElementById('quiz-question-text').value.trim();
    const questionType = document.getElementById('quiz-question-type').value;
    let correctAnswer = document.getElementById('quiz-correct-answer').value.trim();
    const explanation = document.getElementById('quiz-explanation').value.trim();
    const points = parseInt(document.getElementById('quiz-points').value);

    let options = null;

    if (questionType === 'fill_in_blank_with_image') {
        const imgPreview = document.getElementById('quiz-image-preview');
        if (imgPreview && imgPreview.style.display !== 'none') {
            const imgSrc = imgPreview.querySelector('img').src;
            if (imgSrc && imgSrc.startsWith('data:image')) {
                questionText = `<img src="${imgSrc}" class="quiz-embedded-image" style="max-width: 100%; border-radius: 4px; display: block; margin-bottom: 10px;" />\n` + questionText;
            }
        }

        const partItems = document.querySelectorAll('.quiz-part-item');
        options = [];
        let correctAnswersObj = {};
        
        partItems.forEach(item => {
            const label = item.querySelector('.quiz-part-label').value.trim();
            const ans = item.querySelector('.quiz-part-answer').value.trim();
            const unit = item.querySelector('.quiz-part-unit').value.trim();
            if (label && ans) {
                options.push({ label, unit });
                correctAnswersObj[label] = ans;
            }
        });
        
        if (options.length === 0) {
            alert('Please add at least one part for the fill-in-the-blank question.');
            return;
        }
        
        correctAnswer = JSON.stringify(correctAnswersObj);
    }

    if (!questionText || !correctAnswer) {
        alert('Please fill in the question text and correct answer');
        return;
    }

    if (questionType === 'multiple_choice') {
        const optionInputs = document.querySelectorAll('.quiz-option-input');
        options = Array.from(optionInputs)
            .map(input => input.value.trim())
            .filter(val => val !== '');

        if (options.length < 2) {
            alert('Please provide at least 2 options for multiple choice questions');
            return;
        }
    }

    const questionData = {
        question_text: questionText,
        question_type: questionType,
        options: options,
        correct_answer: correctAnswer,
        explanation: explanation,
        points: points,
        order_index: courseQuestions.length
    };

    try {
        let response;
        if (currentEditingQuestionId) {
            response = await fetch(`${API_BASE_URL}/api/courses/${currentEditingCourseId}/questions/${currentEditingQuestionId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${authToken}`
                },
                body: JSON.stringify(questionData)
            });
        } else {
            response = await fetch(`${API_BASE_URL}/api/courses/${currentEditingCourseId}/questions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${authToken}`
                },
                body: JSON.stringify(questionData)
            });
        }

        const result = await response.json();

        if (result.success) {
            alert(currentEditingQuestionId ? 'Question updated successfully!' : 'Question added successfully!');
            closeQuizModalFunc();
            await loadCourseQuestions(currentEditingCourseId);

            if (currentEditingQuestionId) {
                // Update existing placeholder text if found
                const editor = document.getElementById('course-content-editor');
                const existing = editor.querySelector(`.quiz-question-placeholder[data-question-id="${currentEditingQuestionId}"]`);
                if (existing) {
                    existing.innerHTML = `
            <strong>❓ Quiz Question:</strong> ${escapeHtml(questionText.substring(0, 100))}${questionText.length > 100 ? '...' : ''}
            <button type="button" class="quiz-placeholder-delete-btn" data-question-id="${currentEditingQuestionId}" style="position: absolute; top: 5px; right: 5px; background: #e53e3e; color: white; border: none; border-radius: 4px; padding: 2px 6px; cursor: pointer; font-size: 0.8em; z-index: 10;">🗑️ Delete</button>
            <div style="font-size: 0.85em; color: #999; margin-top: 0.5em;">Click to edit</div>
          `;
                }
            } else {
                // New question: Start placement mode
                const newQuestionId = result.data.questionId || result.data.insertId || result.data.id;
                if (window.logger) window.logger.debug('New question created with ID:', newQuestionId, 'result.data:', result.data);
                startPlacementMode('quiz', {
                    id: newQuestionId,
                    text: questionText
                });
            }
        } else {
            alert('Error saving question: ' + result.message);
        }
    } catch (error) {
        console.error('Error saving quiz question:', error);
        alert('Error saving question. Please try again.');
    }
}

function insertQuizPlaceholder(questionText, questionId) {
    const editor = document.getElementById('course-content-editor');
    const placeholder = document.createElement('div');
    placeholder.className = 'quiz-question-placeholder';
    placeholder.dataset.questionId = questionId || '';
    placeholder.contentEditable = 'false'; // Make it non-editable
    placeholder.style.cssText = 'background: #e0e7ff; border: 2px solid var(--primary); padding: 1.5em; margin: 1.5em 0; border-radius: 8px; position: relative; cursor: pointer; user-select: none; box-shadow: 0 4px 6px rgba(0,0,0,0.1);';

    let deleteBtnHtml = '';
    if (questionId) {
        deleteBtnHtml = `<button type="button" class="quiz-placeholder-delete-btn" data-question-id="${questionId}" style="position: absolute; top: 5px; right: 5px; background: #e53e3e; color: white; border: none; border-radius: 4px; padding: 2px 6px; cursor: pointer; font-size: 0.8em; z-index: 10;">🗑️ Delete</button>`;
    }

    placeholder.innerHTML = `
    <strong>❓ Quiz Question:</strong> ${escapeHtml(questionText.substring(0, 100))}${questionText.length > 100 ? '...' : ''}
    ${deleteBtnHtml}
    <div style="font-size: 0.85em; color: #999; margin-top: 0.5em;">Click to edit</div>
  `;

    // Click handler for editing (click anywhere except button)
    placeholder.addEventListener('click', (e) => {
        if (e.target.closest('button')) return; // Let button handle itself

        const qId = placeholder.dataset.questionId;
        if (qId) {
            openQuizModal(parseInt(qId));
        }
    });

    // Try to insert at saved cursor position
    editor.focus();
    if (savedSelection) {
        restoreCursorPosition(savedSelection);
        savedSelection = null;

        const selection = window.getSelection();
        if (selection.rangeCount > 0) {
            try {
                const range = selection.getRangeAt(0);
                const commonAncestor = range.commonAncestorContainer;

                // If cursor is in text, split the text node
                if (commonAncestor.nodeType === Node.TEXT_NODE) {
                    const offset = range.endOffset;
                    const textNode = commonAncestor;

                    // Split the text node at cursor position
                    if (offset < textNode.length) {
                        textNode.splitText(offset);
                    }

                    // Insert question placeholder after this text node
                    const nextNode = textNode.nextSibling;
                    if (nextNode) {
                        editor.insertBefore(placeholder, nextNode);
                    } else {
                        editor.appendChild(placeholder);
                    }

                    return;
                }
            } catch (e) {
                console.warn('Failed to insert quiz at cursor:', e);
            }
        }
    }

    // Fallback: append to end
    if (questionId && !isNaN(parseInt(questionId))) {
        editor.appendChild(placeholder);
    } else {
        console.error('Attempted to insert quiz placeholder with invalid ID:', questionId);
    }
}

async function deleteQuizQuestion(questionId, btnElement = null) {
    if (window.logger) {
        window.logger.debug(`🗑️ Delete button clicked for question ID:`, questionId);
        window.logger.debug(`   currentEditingCourseId:`, currentEditingCourseId);
        window.logger.debug(`   authToken exists:`, !!authToken);
    }

    if (!currentEditingCourseId) {
        alert('❌ Error: Course ID not set. Please save the course first.');
        return;
    }

    // Store question data for undo BEFORE deleting
    const questionToDelete = courseQuestions.find(q => q.id === questionId);
    if (questionToDelete) {
        lastDeletedQuestion = {
            question_text: questionToDelete.question_text,
            question_type: questionToDelete.question_type,
            options: questionToDelete.options,
            correct_answer: questionToDelete.correct_answer,
            explanation: questionToDelete.explanation,
            points: questionToDelete.points
        };
        console.log('💾 Stored question for undo:', lastDeletedQuestion);
    }

    // REMOVED confirmation dialog - it wasn't showing and was auto-cancelling
    // User can press Ctrl+Z to undo if they delete by accident
    console.log(`🗑️ Proceeding with deletion of question ID:`, questionId);

    try {
        const url = `${API_BASE_URL}/api/courses/${currentEditingCourseId}/questions/${questionId}`;
        console.log(`   API URL:`, url);

        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${authToken}`
            },
            credentials: 'include'
        });

        console.log(`   Response status:`, response.status);
        const result = await response.json();
        console.log(`   Delete response:`, result);

        if (result.success) {
            alert('Question deleted! Press Ctrl+Z to undo.');
            closeQuizModalFunc();

            // Remove from courseQuestions array
            courseQuestions = courseQuestions.filter(q => q.id !== questionId);
            console.log(`✅ Removed from array. Remaining questions:`, courseQuestions.length);

            // Remove placeholder from DOM by data attribute
            const editor = document.getElementById('course-content-editor');
            const placeholders = editor.querySelectorAll('.quiz-question-placeholder');
            console.log(`ðŸ“Œ Found ${placeholders.length} placeholders in editor`);

            // Match by data attribute value as string
            let removed = false;
            placeholders.forEach(p => {
                const pId = p.dataset.questionId;
                console.log(`  Checking placeholder with ID: "${pId}" vs "${questionId}"`);
                if (pId == questionId) {  // Use == to handle string/number comparison
                    p.remove();
                    removed = true;
                    console.log(`  ✔ Removed placeholder`);
                }
            });

            if (!removed) {
                console.warn(`⚠️ Warning: Placeholder not found for ID ${questionId}`);
            }
        } else {
            console.error(`❌ Delete failed:`, result.message);
            alert('Error deleting question: ' + result.message);
            lastDeletedQuestion = null; // Clear if delete failed
        }
    } catch (error) {
        console.error('❌ Error deleting question:', error);
        alert('Error deleting question: ' + error.message);
        lastDeletedQuestion = null; // Clear if error
    }
}

// ===== COURSE NESTING SYSTEM FUNCTIONS =====

// Setup course type toggle listeners
function setupCourseTypeToggle() {
    const courseTypeRadios = document.getElementsByName("course_type");
    const manageUnitsBtn = document.getElementById("manage-units-btn");
    
    for (const radio of courseTypeRadios) {
        radio.addEventListener("change", async (e) => {
            const newType = e.target.value;
            
            if (!currentEditingCourseId) {
                // New course - just show/hide manage units button
                if (manageUnitsBtn) {
                    manageUnitsBtn.style.display = newType === "master" ? "block" : "none";
                }
                return;
            }
            
            // For existing courses, check current type
            try {
                const response = await fetch(`${API_BASE_URL}/api/courses/${currentEditingCourseId}/type`, {
                    headers: { 'Authorization': `Bearer ${authToken}` },
                    credentials: 'include'
                });
                const result = await response.json();
                const currentType = result.data?.course_type || "single";
                
                if (currentType === newType) {
                    if (manageUnitsBtn) {
                        manageUnitsBtn.style.display = newType === "master" ? "block" : "none";
                    }
                    return;
                }
                
                // Show confirmation modal if converting from master to single
                if (currentType === "master" && newType === "single") {
                    showCourseTypeConfirmModal(newType);
                    // Reset radio to current type
                    for (const r of courseTypeRadios) {
                        r.checked = r.value === currentType;
                    }
                } else {
                    // Convert directly
                    await convertCourseType(currentEditingCourseId, newType);
                    if (manageUnitsBtn) {
                        manageUnitsBtn.style.display = newType === "master" ? "block" : "none";
                    }
                }
            } catch (err) {
                console.error("Error checking course type:", err);
            }
        });
    }
    
    // Manage units button click
    if (manageUnitsBtn) {
        manageUnitsBtn.addEventListener("click", () => {
            showUnitManagementPanel();
        });
    }
}

// Show confirmation modal for course type conversion
function showCourseTypeConfirmModal(newType) {
    const modal = document.getElementById("course-type-confirm-modal");
    if (!modal) return;
    
    const warningText = document.getElementById("course-type-warning-text");
    if (warningText) {
        warningText.textContent = "Converting to Single Module will detach all existing units. Your units will become standalone courses again.";
    }
    
    modal.style.display = "flex";
    
    // Setup modal buttons
    const confirmBtn = document.getElementById("confirm-course-type-convert");
    const cancelBtn = document.getElementById("cancel-course-type-convert");
    const closeModal = document.getElementById("close-course-type-modal");
    
    const cleanup = () => {
        modal.style.display = "none";
    };
    
    if (confirmBtn) {
        confirmBtn.onclick = async () => {
            cleanup();
            await convertCourseType(currentEditingCourseId, newType);
            const manageUnitsBtn = document.getElementById("manage-units-btn");
            if (manageUnitsBtn) manageUnitsBtn.style.display = "none";
        };
    }
    
    if (cancelBtn) cancelBtn.onclick = cleanup;
    if (closeModal) closeModal.onclick = cleanup;
    
    // Close on outside click
    modal.onclick = (e) => {
        if (e.target === modal) cleanup();
    };
}

// Convert course type
async function convertCourseType(courseId, newType) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/courses/${courseId}/type`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            credentials: 'include',
            body: JSON.stringify({ course_type: newType })
        });
        
        const result = await response.json();
        if (result.success) {
            alert(`Course converted to ${newType === 'master' ? 'Master Course' : 'Single Module'}`);
        } else {
            alert("Error: " + result.message);
        }
    } catch (err) {
        console.error("Error converting course type:", err);
        alert("Error converting course type");
    }
}

// Show unit management panel
async function showUnitManagementPanel() {
    // First check if course is saved
    if (!currentEditingCourseId) {
        alert("Please save the course first before managing units.");
        return;
    }
    
    const editorSection = document.getElementById("course-editor-section");
    const unitSection = document.getElementById("unit-management-section");
    const titleEl = document.getElementById("unit-management-title");
    
    // Check if course is a master course
    try {
        const response = await fetch(`${API_BASE_URL}/api/courses/${currentEditingCourseId}/type`, {
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });
        const result = await response.json();
        
        if (!result.success || result.data?.course_type !== 'master') {
            alert("This course is not a Master Course. Please save it as a Master Course first.");
            return;
        }
    } catch (err) {
        console.error("Error checking course type:", err);
        alert("Error checking course type. Please save the course first.");
        return;
    }
    
    if (editorSection) editorSection.style.display = "none";
    if (unitSection) {
        unitSection.style.display = "block";
        if (titleEl && currentEditingCourseId) {
            titleEl.textContent = `Manage Units - ${document.getElementById("course-title").value}`;
        }
    }
    
    // Load existing units
    await loadCourseUnits();
}

// Load course units
async function loadCourseUnits() {
    if (!currentEditingCourseId) return;
    
    const unitsList = document.getElementById("units-list");
    const noUnitsMsg = document.getElementById("no-units-message");
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/courses/${currentEditingCourseId}/units`, {
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });
        
        const result = await response.json();
        
        if (result.success && result.data && result.data.length > 0) {
            renderUnitsList(result.data);
            if (unitsList) unitsList.style.display = "flex";
            if (noUnitsMsg) noUnitsMsg.style.display = "none";
        } else {
            if (unitsList) unitsList.style.display = "none";
            if (noUnitsMsg) noUnitsMsg.style.display = "block";
        }
    } catch (err) {
        console.error("Error loading units:", err);
    }
}

// Render units list
function renderUnitsList(units) {
    const container = document.getElementById("units-list");
    if (!container) return;
    
    container.innerHTML = units.map((unit, index) => `
        <div class="unit-item" data-unit-id="${unit.id}" draggable="true" style="
            display: flex; align-items: center; gap: 15px; padding: 15px; 
            background: var(--bg-card); border: 1px solid var(--border); 
            border-radius: 10px; cursor: grab;
        ">
            <span class="drag-handle" style="color: var(--text-muted); cursor: grab;">☰</span>
            <span style="font-weight: bold; min-width: 30px;">${index + 1}</span>
            <div style="flex: 1;">
                <strong>${escapeHtml(unit.title || 'Untitled Unit')}</strong>
                <p style="margin: 5px 0 0 0; font-size: 12px; color: var(--text-muted);">
                    ${unit.is_draft ? '📝 Draft' : '✅ Published'}
                    ${unit.prerequisite_title ? ` | Prerequisites: ${unit.prerequisite_title}` : ''}
                </p>
            </div>
            <div style="display: flex; gap: 8px;">
                <button type="button" onclick="toggleUnitDraft(${unit.id}, ${!unit.is_draft})" 
                    style="padding: 6px 12px; border-radius: 6px; border: 1px solid var(--border); background: transparent; cursor: pointer;">
                    ${unit.is_draft ? '📤 Publish' : '📝 Draft'}
                </button>
                <button type="button" onclick="setUnitPrerequisite(${unit.id})" 
                    style="padding: 6px 12px; border-radius: 6px; border: 1px solid var(--border); background: transparent; cursor: pointer;">
                    🔗 Prereq
                </button>
                <button type="button" onclick="removeUnit(${unit.id})" 
                    style="padding: 6px 12px; border-radius: 6px; border: none; background: var(--danger); color: white; cursor: pointer;">
                    Remove
                </button>
            </div>
        </div>
    `).join('');
    
    // Add drag and drop
    setupUnitDragDrop();
}

// Setup drag and drop for units
function setupUnitDragDrop() {
    const container = document.getElementById("units-list");
    if (!container) return;
    
    let draggedItem = null;
    
    container.querySelectorAll(".unit-item").forEach(item => {
        item.addEventListener("dragstart", (e) => {
            draggedItem = item;
            e.dataTransfer.effectAllowed = "move";
        });
        
        item.addEventListener("dragover", (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = "move";
        });
        
        item.addEventListener("drop", async (e) => {
            e.preventDefault();
            if (draggedItem && draggedItem !== item) {
                await reorderUnits(draggedItem, item);
            }
        });
        
        item.addEventListener("dragend", () => {
            draggedItem = null;
        });
    });
}

// Reorder units
async function reorderUnits(draggedItem, targetItem) {
    const units = [...document.querySelectorAll(".unit-item")];
    const fromIndex = units.indexOf(draggedItem);
    const toIndex = units.indexOf(targetItem);
    
    if (fromIndex === -1 || toIndex === -1) return;
    
    // Reorder in DOM
    if (fromIndex < toIndex) {
        targetItem.parentNode.insertBefore(draggedItem, targetItem.nextSibling);
    } else {
        targetItem.parentNode.insertBefore(draggedItem, targetItem);
    }
    
    // Update order indices
    const unitOrders = units.map((item, index) => ({
        unitId: parseInt(item.dataset.unitId),
        order_index: index
    }));
    
    try {
        await fetch(`${API_BASE_URL}/api/courses/${currentEditingCourseId}/units/reorder`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            credentials: 'include',
            body: JSON.stringify({ unit_orders: unitOrders })
        });
        
        // Re-render with new indices
        await loadCourseUnits();
    } catch (err) {
        console.error("Error reordering units:", err);
    }
}

// Toggle unit draft status
async function toggleUnitDraft(unitId, isDraft) {
    try {
        await fetch(`${API_BASE_URL}/api/courses/units/${unitId}`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            credentials: 'include',
            body: JSON.stringify({ is_draft: isDraft })
        });
        
        await loadCourseUnits();
    } catch (err) {
        console.error("Error toggling unit draft:", err);
    }
}

// Set unit prerequisite
async function setUnitPrerequisite(unitId) {
    const units = document.querySelectorAll(".unit-item");
    const unitArray = [...units].map(item => ({
        id: parseInt(item.dataset.unitId),
        index: [...units].indexOf(item)
    }));
    
    const currentIndex = unitArray.find(u => u.id === unitId)?.index;
    if (currentIndex === 0) {
        alert("The first unit cannot have a prerequisite.");
        return;
    }
    
    const availableUnits = unitArray.filter(u => u.index < currentIndex);
    
    if (availableUnits.length === 0) {
        alert("No units available to set as prerequisite (must be before this unit).");
        return;
    }
    
    const prereqId = prompt(`Available prerequisites:\n${availableUnits.map((u, i) => `${i + 1}. Unit ${u.index + 1}`).join('\n')}\n\nEnter the number (or 0 to remove prerequisite):`);
    
    if (prereqId === null) return;
    
    const prereqIndex = parseInt(prereqId) - 1;
    let prereqUnitId = null;
    
    if (prereqIndex >= 0 && prereqIndex < availableUnits.length) {
        prereqUnitId = availableUnits[prereqIndex].id;
    } else if (prereqIndex === -1) {
        prereqUnitId = "null";
    } else {
        alert("Invalid selection");
        return;
    }
    
    try {
        await fetch(`${API_BASE_URL}/api/courses/units/${unitId}`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            credentials: 'include',
            body: JSON.stringify({ prerequisite_unit_id: prereqUnitId })
        });
        
        await loadCourseUnits();
    } catch (err) {
        console.error("Error setting prerequisite:", err);
    }
}

// Remove unit from master course
async function removeUnit(unitId) {
    if (!confirm("Are you sure you want to remove this unit from the Master Course?")) return;
    
    try {
        await fetch(`${API_BASE_URL}/api/courses/units/${unitId}`, {
            method: "DELETE",
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });
        
        await loadCourseUnits();
    } catch (err) {
        console.error("Error removing unit:", err);
    }
}

// Show unit selection modal
async function showUnitSelectionModal() {
    const modal = document.getElementById("unit-selection-modal");
    if (!modal) return;
    
    modal.style.display = "flex";
    
    // Load available courses
    await loadAvailableCoursesForUnits();
    
    // Setup close handlers
    const closeBtn = document.getElementById("close-unit-selection-modal");
    const cancelBtn = document.getElementById("cancel-unit-selection");
    
    const cleanup = () => { modal.style.display = "none"; };
    
    if (closeBtn) closeBtn.onclick = cleanup;
    if (cancelBtn) cancelBtn.onclick = cleanup;
    
    modal.onclick = (e) => {
        if (e.target === modal) cleanup();
    };
    
    // Setup search
    const searchInput = document.getElementById("unit-search-input");
    if (searchInput) {
        searchInput.oninput = () => filterAvailableUnits(searchInput.value);
    }
}

// Load available courses for adding as units
async function loadAvailableCoursesForUnits() {
    const container = document.getElementById("unit-selection-list");
    if (!container) return;
    
    container.innerHTML = '<p style="text-align: center; color: var(--text-muted);">Loading courses...</p>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/courses/available-for-units?exclude_parent=${currentEditingCourseId || 0}`, {
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });
        
        const result = await response.json();
        
        if (result.success && result.data) {
            window._availableCoursesForUnits = result.data;
            renderAvailableUnits(result.data);
        } else {
            container.innerHTML = '<p style="text-align: center; color: var(--text-muted);">No courses available</p>';
        }
    } catch (err) {
        console.error("Error loading available courses:", err);
        container.innerHTML = '<p style="text-align: center; color: var(--danger);">Error loading courses</p>';
    }
}

// Render available units
function renderAvailableUnits(courses) {
    const container = document.getElementById("unit-selection-list");
    if (!container) return;
    
    if (!courses || courses.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: var(--text-muted);">No courses found</p>';
        return;
    }
    
    container.innerHTML = courses.map(course => `
        <div class="unit-option" data-course-id="${course.id}" style="
            padding: 15px; border: 1px solid var(--border); border-radius: 8px; 
            cursor: pointer; transition: all 0.2s;
        " onmouseover="this.style.borderColor='var(--primary)'; this.style.background='rgba(102,126,234,0.05)';" 
           onmouseout="this.style.borderColor='var(--border)'; this.style.background='transparent';">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong>${escapeHtml(course.title)}</strong>
                <span style="font-size: 12px; color: ${course.status === 'approved' ? 'var(--success)' : 'var(--warning)'};">
                    ${course.status === 'approved' ? '✅ Published' : '📝 Draft'}
                </span>
            </div>
            <p style="margin: 5px 0 0 0; font-size: 12px; color: var(--text-muted);">
                ${escapeHtml(course.description || 'No description')} | By ${escapeHtml(course.creator_email)}
            </p>
        </div>
    `).join('');
    
    // Add click handlers
    container.querySelectorAll(".unit-option").forEach(option => {
        option.onclick = () => {
            const courseId = parseInt(option.dataset.courseId);
            addUnitToCourse(courseId);
        };
    });
}

// Filter available units
function filterAvailableUnits(query) {
    const filtered = window._availableCoursesForUnits?.filter(c => 
        c.title.toLowerCase().includes(query.toLowerCase()) ||
        c.description?.toLowerCase().includes(query.toLowerCase())
    ) || [];
    renderAvailableUnits(filtered);
}

// Add unit to course
async function addUnitToCourse(childCourseId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/courses/${currentEditingCourseId}/units`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            credentials: 'include',
            body: JSON.stringify({ child_course_id: childCourseId })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Close modal
            const modal = document.getElementById("unit-selection-modal");
            if (modal) modal.style.display = "none";
            
            // Reload units
            await loadCourseUnits();
        } else {
            alert("Error: " + result.message);
        }
    } catch (err) {
        console.error("Error adding unit:", err);
        alert("Error adding unit");
    }
}

// Back to course editor from unit management
function backToCourseEditor() {
    const editorSection = document.getElementById("course-editor-section");
    const unitSection = document.getElementById("unit-management-section");
    
    if (unitSection) unitSection.style.display = "none";
    if (editorSection) editorSection.style.display = "flex";
}

// Load course type for editing
async function loadCourseTypeForEdit(courseId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/courses/${courseId}/type`, {
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });
        
        const result = await response.json();
        const courseType = result.data?.course_type || "single";
        
        // Update radio buttons
        const courseTypeRadios = document.getElementsByName("course_type");
        for (const radio of courseTypeRadios) {
            radio.checked = radio.value === courseType;
        }
        
        // Show/hide manage units button
        const manageUnitsBtn = document.getElementById("manage-units-btn");
        if (manageUnitsBtn) {
            manageUnitsBtn.style.display = courseType === "master" ? "block" : "none";
        }
    } catch (err) {
        console.error("Error loading course type:", err);
    }
}

// ===== ENROLLMENT STATUS & DASHBOARD FUNCTIONS =====

// Enhanced enrollment with immediate dashboard update
async function enrollInCourse(courseId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/courses/${courseId}/enroll`, {
            method: "POST",
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });
        
        const result = await response.json();
        
        if (result.success) {
            // IMMEDIATE STATE UPDATE - add to myCourses immediately
            const course = availableCourses.find(c => c.id === courseId);
            if (course) {
                const enrollmentRecord = {
                    id: course.id,
                    title: course.title,
                    description: course.description,
                    creator_id: course.creator_id,
                    enrolled_at: new Date().toISOString(),
                    enrollment_status: 'enrolled',
                    course_type: course.course_type
                };
                
                // Add to myCourses array
                myCourses.push(enrollmentRecord);
                
                // Re-render dashboard immediately
                renderUserCourses();
                
                // Show success and update button
                alert("✅ Successfully enrolled! Course added to your dashboard.");
                
                // Update button to show enrolled
                updateEnrollButton(courseId, 'enrolled');
            }
        } else {
            alert("Error: " + result.message);
        }
    } catch (err) {
        console.error("Error enrolling:", err);
        alert("Error enrolling in course");
    }
}

// Enroll in master course
async function enrollInMasterCourse(courseId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/courses/${courseId}/enroll-master`, {
            method: "POST",
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });
        
        const result = await response.json();
        
        if (result.success) {
            // IMMEDIATE STATE UPDATE
            const course = availableCourses.find(c => c.id === courseId);
            if (course) {
                const enrollmentRecord = {
                    id: course.id,
                    title: course.title,
                    description: course.description,
                    creator_id: course.creator_id,
                    enrolled_at: new Date().toISOString(),
                    enrollment_status: 'enrolled',
                    course_type: 'master',
                    total_units: result.data?.units_enrolled || 0,
                    completed_units: 0
                };
                
                myCourses.push(enrollmentRecord);
                renderUserCourses();
                
                alert(`✅ Enrolled in Master Course! You now have access to ${result.data?.units_enrolled || 0} units.`);
                updateEnrollButton(courseId, 'enrolled');
                
                // Navigate to course
                viewCourse(courseId);
            }
        } else {
            alert("Error: " + result.message);
        }
    } catch (err) {
        console.error("Error enrolling in master course:", err);
        alert("Error enrolling in course");
    }
}

// Update enroll button state
function updateEnrollButton(courseId, status) {
    const btn = document.querySelector(`[data-enroll-course="${courseId}"]`);
    if (btn) {
        if (status === 'enrolled') {
            btn.textContent = "✅ Enrolled";
            btn.disabled = true;
            btn.style.background = "var(--success)";
        }
    }
}

// Load enhanced enrollments with status
async function loadEnhancedEnrollments() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/users/enrollments/enhanced`, {
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });
        
        const result = await response.json();
        
        if (result.success) {
            return result.data;
        }
    } catch (err) {
        console.error("Error loading enhanced enrollments:", err);
    }
    return [];
}

// ===== COURSE PLAYER NAVIGATION =====

// Current unit navigation state
let currentMasterCourse = null;
let courseUnits = [];
let currentUnitIndex = 0;

// View course with unit navigation
async function viewCourseWithNavigation(courseId) {
    currentViewingCourseId = courseId;
    try {
        // Get course type
        const typeResponse = await fetch(`${API_BASE_URL}/api/courses/${courseId}/type`, {
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });
        
        // If endpoint doesn't exist (404), fallback to regular view (forceRegular=true to avoid recursion)
        if (!typeResponse.ok) {
            console.log("Course type endpoint not available, using regular view");
            return viewCourse(courseId, null, true);
        }
        
        const typeResult = await typeResponse.json();
        const courseType = typeResult.data?.course_type || 'single';
        
        if (courseType === 'master') {
            // Load master course with unit navigation
            await loadMasterCourseView(courseId);
        } else {
            // Regular single course - use regular view (forceRegular=true to avoid recursion)
            viewCourse(courseId, null, true);
        }
    } catch (err) {
        console.error("Error checking course type for view:", err);
        viewCourse(courseId, null, true); // Fallback: forceRegular=true prevents infinite loop
    }
}

// Creator preview of a master course — loads units without requiring enrollment
async function viewCreatorMasterCoursePreview(courseId) {
    try {
        // Load course data
        const courseResponse = await fetch(`${API_BASE_URL}/api/courses/${courseId}`, {
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });
        const courseResult = await courseResponse.json();
        
        if (!courseResult.success) {
            alert('Course not found');
            return;
        }
        
        const course = courseResult.data;
        currentMasterCourse = course;
        currentViewingCourseId = courseId;

        // Load units directly (creator doesn't need enrollment)
        const unitsResponse = await fetch(`${API_BASE_URL}/api/courses/${courseId}/units`, {
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });
        const unitsResult = await unitsResponse.json();
        
        const units = (unitsResult.success ? unitsResult.data : []).filter(u => !u.is_draft);
        
        // Map units to compatible format for showUnitNavigationSidebar
        courseUnits = units.map(u => ({
            unit_id: u.id,
            child_course_id: u.child_course_id,
            unit_title: u.title,
            order_index: u.order_index,
            completed: false,
            progress_percentage: 0,
            is_unlocked: true, // Creator can view all units
            prerequisite_unit_id: u.prerequisite_unit_id
        }));
        
        currentUnitIndex = 0;
        
        // Show viewer section
        document.getElementById('dashboard-section').style.display = 'none';
        document.getElementById('course-editor-section').style.display = 'none';
        document.getElementById('course-viewer-section').style.display = 'block';
        enterCourseViewerMode(courseId);
        
        if (courseUnits.length === 0) {
            // No units added yet — show a helpful message
            const unitSidebar = document.getElementById('unit-navigation-sidebar');
            const regularSidebar = document.getElementById('viewer-regular-sidebar');
            if (unitSidebar) unitSidebar.style.display = 'none';
            if (regularSidebar) regularSidebar.style.display = 'block';
            
            document.getElementById('course-viewer-content').innerHTML = `
                <div style="text-align:center; padding:60px 20px; color:var(--text-muted);">
                    <p style="font-size:48px; margin-bottom:16px;">📚</p>
                    <h2 style="margin-bottom:12px;">No Units Added Yet</h2>
                    <p>Go back to the editor, switch to <strong>Master Course</strong> mode, then click <strong>📚 Manage Units</strong> to add units.</p>
                    <button onclick="showDashboard()" style="margin-top:20px; padding:10px 20px; background:var(--primary); color:white; border:none; border-radius:8px; cursor:pointer;">← Back to Dashboard</button>
                </div>
            `;
            const titleEl = document.getElementById('course-viewer-title');
            if (titleEl) titleEl.textContent = course.title;
        } else {
            // Show unit sidebar and first unit
            showUnitNavigationSidebar(course, {
                overall_progress: 0,
                completed_units: 0,
                total_units: courseUnits.length
            });
            await loadUnitContent(courseUnits[0]);
            updateViewerNavigation();
        }
        
        // Show a "Preview Mode" notice
        const existingBanner = document.getElementById('creator-preview-banner');
        if (!existingBanner) {
            const banner = document.createElement('div');
            banner.id = 'creator-preview-banner';
            banner.style.cssText = 'background: rgba(255,152,0,0.15); border: 1px solid rgba(255,152,0,0.4); border-radius:8px; padding:10px 16px; margin-bottom:16px; text-align:center; color:#ff9800; font-size:13px; font-weight:600;';
            banner.innerHTML = '👁️ Creator Preview Mode — Students see this with progress tracking enabled';
            const content = document.querySelector('.viewer-content');
            if (content) content.insertBefore(banner, content.firstChild);
        }
        
    } catch (err) {
        console.error('Error in creator master course preview:', err);
        viewCourse(courseId, null, true); // Final fallback — regular view
    }
}

// Load master course with unit navigation
async function loadMasterCourseView(courseId) {
    try {
        // Load course data
        const courseResponse = await fetch(`${API_BASE_URL}/api/courses/${courseId}`, {
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });
        const courseResult = await courseResponse.json();
        
        if (!courseResult.success) {
            alert("Course not found");
            return;
        }
        
        const course = courseResult.data;
        currentMasterCourse = course;
        
        // Load units and progress
        const progressResponse = await fetch(`${API_BASE_URL}/api/users/enrollments/${courseId}/progress`, {
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });
        const progressResult = await progressResponse.json();
        
        if (progressResult.success) {
            courseUnits = progressResult.data?.units || [];
            
            // Show unit navigation sidebar
            showUnitNavigationSidebar(course, progressResult.data);
            
            // Find first accessible unit
            currentUnitIndex = courseUnits.findIndex(u => u.is_unlocked) || 0;
            
            if (currentUnitIndex >= 0 && courseUnits[currentUnitIndex]) {
                await loadUnitContent(courseUnits[currentUnitIndex]);
            } else {
                // No units available
                document.getElementById("course-viewer-content").innerHTML = 
                    '<p style="text-align: center; padding: 40px;">No units available yet.</p>';
            }
        }
        
        // Show the viewer section
        document.getElementById("dashboard-section").style.display = "none";
        document.getElementById("course-editor-section").style.display = "none";
        document.getElementById("course-viewer-section").style.display = "block";
        enterCourseViewerMode(courseId);
        
    } catch (err) {
        console.error("Error loading master course:", err);
        viewCourse(courseId); // Fallback
    }
}

// Show unit navigation sidebar
function showUnitNavigationSidebar(course, progressData) {
    const unitSidebar = document.getElementById("unit-navigation-sidebar");
    const regularSidebar = document.getElementById("viewer-regular-sidebar");
    
    if (unitSidebar) unitSidebar.style.display = "block";
    if (regularSidebar) regularSidebar.style.display = "none";
    
    // Update progress
    const progressPercent = document.getElementById("unit-progress-percent");
    const progressBar = document.getElementById("unit-progress-bar");
    const progressText = document.getElementById("unit-progress-text");
    
    if (progressPercent) progressPercent.textContent = `${progressData?.overall_progress || 0}%`;
    if (progressBar) progressBar.style.width = `${progressData?.overall_progress || 0}%`;
    if (progressText) progressText.textContent = `${progressData?.completed_units || 0} of ${progressData?.total_units || 0} completed`;
    
    // Update course title
    const titleEl = document.getElementById("course-viewer-title");
    if (titleEl) {
        titleEl.textContent = course.title;
    }
    
    const descEl = document.getElementById("course-viewer-description");
    if (descEl) {
        descEl.textContent = course.description || '';
    }
    
    // Render unit list
    const unitList = document.getElementById("unit-list-container");
    if (unitList && courseUnits.length > 0) {
        unitList.innerHTML = courseUnits.map((unit, index) => `
            <div class="unit-nav-item ${index === currentUnitIndex ? 'active' : ''} ${!unit.is_unlocked ? 'locked' : ''}" 
                onclick="${unit.is_unlocked ? `loadUnitByIndex(${index})` : ''}"
                style="
                    padding: 12px; border-radius: 8px; cursor: ${unit.is_unlocked ? 'pointer' : 'not-allowed'};
                    background: ${index === currentUnitIndex ? 'rgba(102,126,234,0.15)' : 'var(--bg-card)'};
                    border: 1px solid ${index === currentUnitIndex ? 'var(--primary)' : 'var(--border)'};
                    opacity: ${unit.is_unlocked ? 1 : 0.5};
                    display: flex; align-items: center; gap: 10px;
                ">
                <span style="
                    width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
                    background: ${unit.completed ? 'var(--success)' : unit.is_unlocked ? 'var(--primary)' : 'var(--text-muted)'};
                    color: white; font-size: 12px; font-weight: bold;
                ">
                    ${unit.completed ? '✓' : (!unit.is_unlocked ? '🔒' : index + 1)}
                </span>
                <div style="flex: 1;">
                    <strong style="font-size: 13px;">${escapeHtml(unit.unit_title || 'Unit ' + (index + 1))}</strong>
                    ${unit.progress_percentage > 0 ? `<p style="margin: 3px 0 0 0; font-size: 11px; color: var(--text-muted);">${Math.round(unit.progress_percentage)}% complete</p>` : ''}
                </div>
            </div>
        `).join('');
    }
}

// Load unit by index
async function loadUnitByIndex(index) {
    if (index < 0 || index >= courseUnits.length) return;
    
    currentUnitIndex = index;
    await loadUnitContent(courseUnits[index]);
    
    // Update sidebar highlighting
    showUnitNavigationSidebar(currentMasterCourse, { 
        overall_progress: Math.round((courseUnits.filter(u => u.completed).length / courseUnits.length) * 100),
        completed_units: courseUnits.filter(u => u.completed).length,
        total_units: courseUnits.length
    });
}

// Load specific unit content
async function loadUnitContent(unit) {
    if (!unit || !unit.child_course_id) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/courses/${unit.child_course_id}`, {
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });
        
        const result = await response.json();
        
        if (result.success) {
            const unitCourse = result.data;
            currentViewingCourseId = unit.child_course_id;

            // CRITICAL: Load quiz questions for this unit's course BEFORE hydrating
            await loadCourseQuestions(unit.child_course_id);
            
            // Display content
            const contentEl = document.getElementById("course-viewer-content");
            if (contentEl) {
                contentEl.innerHTML = unitCourse.content || '<p>No content available.</p>';
                
                // Hydrate quiz placeholders (now courseQuestions is populated)
                await hydrateQuizPlaceholders();
                
                // Hydrate simulator placeholders
                if (typeof hydrateSimulatorPlaceholders === 'function') {
                    hydrateSimulatorPlaceholders();
                }
                
                // Re-attach quiz submit listeners (setupViewerInteractions is local to viewCourse,
                // so we inline the equivalent here)
                document.querySelectorAll('.quiz-submit-btn').forEach((btn) => {
                    btn.addEventListener('click', (e) => {
                        const questionId = e.target.dataset.questionId;
                        submitQuizAnswer(questionId, unit.child_course_id);
                    });
                });
                
                // MathJax render
                setTimeout(async () => {
                    if (window.MathJax && window.MathJax.typesetPromise) {
                        try {
                            await window.MathJax.typesetPromise([contentEl]);
                        } catch (err) {
                            console.error('MathJax error in unit:', err);
                        }
                    }
                }, 100);
            }
            
            // Update navigation buttons
            updateViewerNavigation();
        }
    } catch (err) {
        console.error("Error loading unit content:", err);
    }
}

// Update viewer navigation buttons
function updateViewerNavigation() {
    const prevBtn = document.getElementById("viewer-prev-btn");
    const nextBtn = document.getElementById("viewer-next-btn");
    
    if (prevBtn) {
        prevBtn.disabled = currentUnitIndex <= 0;
        prevBtn.onclick = () => loadUnitByIndex(currentUnitIndex - 1);
    }
    
    if (nextBtn) {
        const hasNext = currentUnitIndex < courseUnits.length - 1;
        if (hasNext) {
            nextBtn.textContent = "Next Unit →";
            nextBtn.disabled = !courseUnits[currentUnitIndex]?.is_unlocked || !courseUnits[currentUnitIndex]?.completed;
            nextBtn.onclick = () => loadUnitByIndex(currentUnitIndex + 1);
        } else {
            nextBtn.textContent = "Complete Course";
            nextBtn.disabled = false;
            nextBtn.onclick = () => completeCurrentUnit();
        }
    }
}

// Complete current unit
async function completeCurrentUnit() {
    if (!courseUnits[currentUnitIndex]) return;
    
    const unit = courseUnits[currentUnitIndex];
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/courses/units/${unit.unit_id}/complete`, {
            method: "POST",
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Update local state
            courseUnits[currentUnitIndex].completed = true;
            
            if (result.data?.all_units_complete) {
                alert("🎉 Congratulations! You've completed the Master Course!");
            } else {
                // Load next unit
                const nextIndex = currentUnitIndex + 1;
                if (nextIndex < courseUnits.length) {
                    loadUnitByIndex(nextIndex);
                }
            }
            
            // Refresh progress
            const courseId = currentMasterCourse?.id;
            if (courseId) {
                const progressResponse = await fetch(`${API_BASE_URL}/api/users/enrollments/${courseId}/progress`, {
                    headers: { 'Authorization': `Bearer ${authToken}` },
                    credentials: 'include'
                });
                const progressResult = await progressResponse.json();
                
                if (progressResult.success) {
                    courseUnits = progressResult.data?.units || [];
                    showUnitNavigationSidebar(currentMasterCourse, progressResult.data);
                }
            }
        }
    } catch (err) {
        console.error("Error completing unit:", err);
    }
}

// Update unit progress (for partial progress tracking)
async function updateUnitProgress(unitId, percentage) {
    try {
        await fetch(`${API_BASE_URL}/api/courses/units/${unitId}/progress`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            credentials: 'include',
            body: JSON.stringify({ progress_percentage: percentage })
        });
    } catch (err) {
        console.error("Error updating unit progress:", err);
    }
}

async function loadCourseQuestions(courseId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/courses/${courseId}/questions`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            },
            credentials: 'include'
        });

        const result = await response.json();
        if (result.success) {
            courseQuestions = result.data;
            console.log(`Loaded ${courseQuestions.length} questions for course ${courseId}`);
        }
    } catch (error) {
        console.error('Error loading course questions:', error);
    }
}

function hydrateQuizPlaceholders() {
    const viewerContent = document.getElementById('course-viewer-content');
    if (!viewerContent) {
        console.warn('hydrateQuizPlaceholders: course-viewer-content not found');
        return;
    }
    const placeholders = viewerContent.querySelectorAll('.quiz-question-placeholder');
    if (placeholders.length === 0) return;

    console.log(`Hydrating ${placeholders.length} quiz placeholders, courseQuestions: ${courseQuestions.length}`);

    let questionCounter = 0;

    placeholders.forEach(placeholder => {
        const questionId = parseInt(placeholder.dataset.questionId);
        if (!questionId || isNaN(questionId)) {
            console.error('Invalid question ID in placeholder:', placeholder);
            return;
        }

        const question = courseQuestions.find(q => q.id === questionId);

        if (question) {
            const questionEl = createQuizQuestionElement(question, questionCounter);
            questionCounter++;

            questionEl.style.cssText = '';
            questionEl.style.border = '2px solid var(--primary)';
            questionEl.style.background = 'rgba(102, 126, 234, 0.1)';
            questionEl.style.cursor = 'default';
            questionEl.style.userSelect = 'text';
            questionEl.className = 'quiz-question';

            // Add event listener for submit button
            const submitBtn = questionEl.querySelector('.quiz-submit-btn');
            if (submitBtn) {
                submitBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    submitQuizAnswer(question.id);
                });
            }

            placeholder.replaceWith(questionEl);
        } else {
            console.warn('Hydration failed for question ID:', questionId, 'courseQuestions:', courseQuestions);
            const unavailableEl = document.createElement('div');
            unavailableEl.className = 'quiz-question quiz-question-unavailable';
            unavailableEl.style.cssText = placeholder.style.cssText;
            unavailableEl.style.border = '2px solid #e94560';
            unavailableEl.style.background = 'rgba(233, 69, 96, 0.1)';
            unavailableEl.style.padding = '1em';
            unavailableEl.style.borderRadius = '8px';
            unavailableEl.style.margin = '1em 0';
            unavailableEl.innerHTML = `
        <div style="color: #e94560; font-weight: bold;">âš  Question not available</div>
        <div style="color: #999; font-size: 0.9em; margin-top: 0.5em;">This quiz question (ID: ${questionId}) could not be loaded. Please try refreshing the page.</div>
      `;
            placeholder.replaceWith(unavailableEl);
        }
    });

    console.log(`Hydrated ${questionCounter} quiz questions successfully`);
}

function hydrateSimulatorPlaceholders() {
    const viewerContent = document.getElementById('course-viewer-content');
    if (!viewerContent) return;

    const simulatorDivs = viewerContent.querySelectorAll('.simulator-block');
    if (simulatorDivs.length === 0) return;

    console.log(`Hydrating ${simulatorDivs.length} simulator placeholders, courseBlocks: ${courseBlocks.length}`);

    simulatorDivs.forEach(div => {
        const blockId = parseInt(div.dataset.blockId);
        const title = div.querySelector('strong')?.textContent || 'Interactive Simulator';

        div.style.cssText = 'margin: 16px 0; border-radius: 8px; overflow: hidden;';
        div.contentEditable = 'false';
        div.innerHTML = `
            <div style="display:flex; align-items:center; gap:14px; background:rgba(102,126,234,0.12); padding:18px 20px; border:2px solid #667eea; border-radius:8px;">
                <div style="font-size:2.2em; line-height:1;">🎮</div>
                <div style="flex:1;">
                    <div style="font-weight:700; font-size:1.05em; color:#e2e8f0;">${escapeHtml(title)}</div>
                    <div style="font-size:0.85em; color:#94a3b8; margin-top:4px;">Interactive simulator — click Run to launch</div>
                </div>
                <button class="sim-run-btn" data-sim-block-id="${blockId}" data-sim-title="${escapeHtml(title).replace(/"/g, '&quot;')}" style="padding:10px 24px; background:linear-gradient(135deg,#4caf50,#2e7d32); color:white; border:none; border-radius:6px; cursor:pointer; font-weight:700; font-size:1em; box-shadow:0 2px 8px rgba(76,175,80,0.3); transition:transform .15s;">▶ Run</button>
            </div>
        `;

        const btn = div.querySelector('.sim-run-btn');
        if (btn) {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                const bid = parseInt(btn.dataset.simBlockId);
                const t = btn.dataset.simTitle;
                runEmbeddedBlockSimulator(bid, t);
            });
            btn.addEventListener('mouseenter', () => { btn.style.transform = 'scale(1.05)'; });
            btn.addEventListener('mouseleave', () => { btn.style.transform = 'scale(1)'; });
        }
    });

    console.log(`Hydrated ${simulatorDivs.length} simulator blocks`);
}
window.hydrateSimulatorPlaceholders = hydrateSimulatorPlaceholders;

// Kept for backward compatibility if needed, but modified to use hydration
async function renderQuizQuestionsInViewer(courseId) {
    await loadCourseQuestions(courseId);
    hydrateQuizPlaceholders();
}

function createQuizQuestionElement(question, index) {
    const questionDiv = document.createElement('div');
    questionDiv.className = 'quiz-question';
    questionDiv.dataset.questionId = question.id;

    let optionsHTML = '';
    if (question.question_type === 'multiple_choice' && question.options) {
        optionsHTML = '<div class="quiz-options quiz-choice-container">';
        question.options.forEach((option, optIndex) => {
            optionsHTML += `
        <div class="quiz-option">
          <input type="radio" name="question-${question.id}" id="q${question.id}-opt${optIndex}" value="${option}">
          <label for="q${question.id}-opt${optIndex}">${option}</label>
        </div>
      `;
        });
        optionsHTML += '</div>';
    } else if (question.question_type === 'true_false') {
        optionsHTML = `
      <div class="quiz-options">
        <div class="quiz-option">
          <input type="radio" name="question-${question.id}" id="q${question.id}-true" value="True">
          <label for="q${question.id}-true">True</label>
        </div>
        <div class="quiz-option">
          <input type="radio" name="question-${question.id}" id="q${question.id}-false" value="False">
          <label for="q${question.id}-false">False</label>
        </div>
      </div>
    `;
    } else if (question.question_type === 'fill_in_blank_with_image') {
        optionsHTML = '<div class="quiz-parts">';
        if (question.options) {
            question.options.forEach((part) => {
                optionsHTML += `
                    <div class="quiz-part-container" style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                        <span class="quiz-part-label-display" style="min-width: 60px; font-weight: bold; color: var(--primary);">${escapeHtml(part.label)}: </span>
                        <input type="text" class="quiz-part-input" data-part="${escapeHtml(part.label)}" placeholder="Enter answer" style="flex: 1; padding: 0.8em; border: 1px solid var(--primary); border-radius: 4px; background: rgba(255,255,255,0.05); color: var(--light);">
                        ${part.unit ? `<span class="quiz-part-unit-display" style="min-width: 60px;">${escapeHtml(part.unit)}</span>` : ''}
                    </div>
                `;
            });
        }
        optionsHTML += '</div>';
    } else {
        optionsHTML = `
      <input type="text" id="q${question.id}-answer" placeholder="Enter your answer" style="width: 100%; padding: 0.8em; margin: 1em 0; border: 1px solid var(--primary); border-radius: 4px; background: rgba(255,255,255,0.05); color: var(--light);">
    `;
    }

    questionDiv.innerHTML = `
    <div class="quiz-question-header">
      <div class="quiz-question-text">Question ${index + 1}: ${escapeHtml(question.question_text)}</div>
      <div class="quiz-points">${question.points} pts</div>
    </div>
    ${optionsHTML}
    <button class="quiz-submit-btn" data-question-id="${question.id}">Submit Answer</button>
    <div id="feedback-${question.id}" class="quiz-feedback" style="display: none;"></div>
  `;

    return questionDiv;
}

async function submitQuizAnswer(questionId) {
    console.log(`Submitting answer for question ${questionId}`);
    const question = courseQuestions.find(q => q.id === parseInt(questionId));
    if (!question) {
        console.error(`Question ${questionId} not found in courseQuestions`, courseQuestions);
        return;
    }

    let userAnswer;
    if (question.question_type === 'short_answer') {
        userAnswer = document.getElementById(`q${questionId}-answer`).value.trim();
    } else if (question.question_type === 'fill_in_blank_with_image') {
        const partInputs = document.querySelectorAll(`.quiz-question[data-question-id="${questionId}"] .quiz-part-input`);
        let userAnswersObj = {};
        partInputs.forEach(input => {
            userAnswersObj[input.dataset.part] = input.value.trim();
        });
        userAnswer = JSON.stringify(userAnswersObj);
    } else {
        const selectedOption = document.querySelector(`input[name="question-${questionId}"]:checked`);
        if (!selectedOption) {
            alert('Please select an answer');
            return;
        }
        userAnswer = selectedOption.value;
    }

    if (!userAnswer) {
        alert('Please provide an answer');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/courses/${currentEditingCourseId}/questions/${questionId}/answer`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            credentials: 'include',
            body: JSON.stringify({ user_answer: userAnswer })
        });

        const result = await response.json();

        if (result.success) {
            const feedbackDiv = document.getElementById(`feedback-${questionId}`);
            feedbackDiv.style.display = 'block';

            if (result.data.is_correct) {
                feedbackDiv.className = 'quiz-feedback correct';
                feedbackDiv.innerHTML = `
          <div>✅ Correct!</div>
          ${result.data.explanation ? `<div class="quiz-explanation">${escapeHtml(result.data.explanation)}</div>` : ''}
        `;
                if (window.LearnerGamification?.onQuizCorrect) {
                    window.LearnerGamification.onQuizCorrect(questionId);
                }
            } else {
                feedbackDiv.className = 'quiz-feedback incorrect';
                feedbackDiv.innerHTML = `
          <div>❌ Incorrect. The correct answer is: ${escapeHtml(result.data.correct_answer)}</div>
          ${result.data.explanation ? `<div class="quiz-explanation">${escapeHtml(result.data.explanation)}</div>` : ''}
        `;
            }

            const submitBtn = feedbackDiv.previousElementSibling;
            if (result.data.is_correct) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Answered';
            } else {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Try Again';
            }
        } else {
            alert('Error submitting answer: ' + result.message);
        }
    } catch (error) {
        console.error('Error submitting answer:', error);
        alert('Error submitting answer. Please try again.');
    }
}

// Make functions globally accessible
window.submitQuizAnswer = submitQuizAnswer;
window.deleteQuizQuestion = deleteQuizQuestion;

// ======= INTERACTIVE SLIDER CONFIGURATION =======
// Global variable to store current simulator being configured
let currentConfiguringSimulatorId = null;

// Open slider configuration modal
async function openSliderConfigModal(blockId) {
    if (!currentEditingCourseId) {
        alert('Please save the course first before configuring sliders.');
        return;
    }

    currentConfiguringSimulatorId = blockId;
    console.log('📊 Opening slider config for simulator block:', blockId);

    // Find the simulator block in courseBlocks
    const simBlock = courseBlocks.find(b => b.id === blockId);
    if (!simBlock) {
        alert('Simulator block not found');
        return;
    }

    // Show modal
    const modal = document.getElementById('slider-config-modal');
    modal.style.display = 'block';

    // Reset form
    document.getElementById('slider-config-form').style.display = 'none';
    document.getElementById('add-new-slider-btn').style.display = 'block';

    // Load existing configs
    await fetchSliderConfigs();
}

// Fetch slider configurations from backend
async function fetchSliderConfigs() {
    const tbody = document.getElementById('slider-config-tbody');
    tbody.innerHTML = '<tr><td colspan="4" style="text-align:center; padding: 20px;">Loading...</td></tr>';

    try {
        const response = await fetch(`${API_BASE_URL}/api/courses/${currentEditingCourseId}/params`, {
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });
        const result = await response.json();

        if (result.success) {
            // Filter for current simulator block
            const configs = result.data.filter(p => p.simulator_block_id == currentConfiguringSimulatorId);
            renderSliderConfigs(configs);
        } else {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align:center; padding: 20px; color: red;">Failed to load configurations</td></tr>';
        }
    } catch (error) {
        console.error('Error fetching slider configs:', error);
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center; padding: 20px; color: red;">Error loading configurations</td></tr>';
    }
}

// Render slider configurations table
function renderSliderConfigs(configs) {
    const tbody = document.getElementById('slider-config-tbody');
    tbody.innerHTML = '';

    if (configs.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center; padding: 20px; color: #666;">No sliders configured yet. Click "Add New Slider" to create one.</td></tr>';
        return;
    }

    configs.forEach(config => {
        const tr = document.createElement('tr');
        tr.style.borderBottom = '1px solid #eee';
        tr.innerHTML = `
      <td style="padding: 10px;"><strong>${escapeHtml(config.param_label || config.param_name)}</strong></td>
      <td style="padding: 10px; color: #666;">${escapeHtml(config.param_name)}</td>
      <td style="padding: 10px;">${config.min_value} - ${config.max_value} (step: ${config.step_value})</td>
      <td style="padding: 10px;">
        <button onclick="deleteSliderConfig(${config.id})" style="background: #ef4444; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-size: 0.8em;">Delete</button>
      </td>
    `;
        tbody.appendChild(tr);
    });
}

// Event Listeners for Slider Modal
document.addEventListener('DOMContentLoaded', () => {
    // Close modal
    const closeModal = () => {
        document.getElementById('slider-config-modal').style.display = 'none';
    };

    const closeBtn = document.getElementById('close-slider-modal');
    if (closeBtn) closeBtn.onclick = closeModal;

    const doneBtn = document.getElementById('done-slider-config-btn');
    if (doneBtn) doneBtn.onclick = closeModal;

    // Add new slider button
    const addBtn = document.getElementById('add-new-slider-btn');
    if (addBtn) {
        addBtn.onclick = () => {
            document.getElementById('slider-config-form').style.display = 'block';
            document.getElementById('add-new-slider-btn').style.display = 'none';
            document.getElementById('slider-config-form').reset();
        };
    }

    // Cancel add button
    const cancelBtn = document.getElementById('cancel-slider-config-btn');
    if (cancelBtn) {
        cancelBtn.onclick = () => {
            document.getElementById('slider-config-form').style.display = 'none';
            document.getElementById('add-new-slider-btn').style.display = 'block';
        };
    }

    // Save slider form
    const form = document.getElementById('slider-config-form');
    if (form) {
        form.onsubmit = async (e) => {
            e.preventDefault();
            await saveSliderConfig();
        };
    }
});

// Save new slider configuration
async function saveSliderConfig() {
    const paramName = document.getElementById('slider-param-name').value.trim();
    const paramLabel = document.getElementById('slider-label').value.trim();
    const minValue = parseFloat(document.getElementById('slider-min').value);
    const maxValue = parseFloat(document.getElementById('slider-max').value);
    const stepValue = parseFloat(document.getElementById('slider-step').value);
    const defaultValue = parseFloat(document.getElementById('slider-default').value);

    if (!paramName || !paramLabel) {
        alert('Please fill in all required fields');
        return;
    }

    const saveBtn = document.getElementById('save-slider-config-btn');
    const originalText = saveBtn.textContent;
    saveBtn.disabled = true;
    saveBtn.textContent = 'Saving...';

    try {
        const response = await fetch(`${API_BASE_URL}/api/courses/${currentEditingCourseId}/simulators/${currentConfiguringSimulatorId}/params`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            credentials: 'include',
            body: JSON.stringify({
                block_id: 1,
                param_name: paramName,
                param_label: paramLabel,
                min_value: minValue,
                max_value: maxValue,
                step_value: stepValue,
                default_value: defaultValue
            })
        });

        const result = await response.json();

        if (result.success) {
            // Refresh list and hide form
            await fetchSliderConfigs();
            document.getElementById('slider-config-form').style.display = 'none';
            document.getElementById('add-new-slider-btn').style.display = 'block';
        } else {
            alert('Failed to save slider: ' + (result.message || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error saving slider:', error);
        alert('Error saving slider configuration');
    } finally {
        saveBtn.disabled = false;
        saveBtn.textContent = originalText;
    }
}

// Delete slider configuration
async function deleteSliderConfig(configId) {
    if (!confirm('Are you sure you want to delete this slider?')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/api/courses/${currentEditingCourseId}/params/${configId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });

        const result = await response.json();

        if (result.success) {
            await fetchSliderConfigs();
        } else {
            alert('Failed to delete slider: ' + result.message);
        }
    } catch (error) {
        console.error('Error deleting slider:', error);
        alert('Error deleting slider configuration');
    }
}

// Make functions globally accessible
window.openSliderConfigModal = openSliderConfigModal;
window.deleteSliderConfig = deleteSliderConfig;
// ===== PHET SIMULATOR INTEGRATION =====
// Complete list of PhET HTML5 Simulations using the standardized _all.html URL pattern
const PHET_SIMS = [
    // ===== PHYSICS =====
    // Mechanics & Motion
    { title: "Balancing Act", url: "https://phet.colorado.edu/sims/html/balancing-act/latest/balancing-act_all.html", description: "Explore torque and balance" },
    { title: "Forces and Motion: Basics", url: "https://phet.colorado.edu/sims/html/forces-and-motion-basics/latest/forces-and-motion-basics_all.html", description: "Explore forces, motion, and friction" },
    { title: "Friction", url: "https://phet.colorado.edu/sims/html/friction/latest/friction_all.html", description: "Feel the heat as you rub objects together" },
    { title: "Projectile Motion", url: "https://phet.colorado.edu/sims/html/projectile-motion/latest/projectile-motion_all.html", description: "Blast objects through the air" },
    { title: "Projectile Data Lab", url: "https://phet.colorado.edu/sims/html/projectile-data-lab/latest/projectile-data-lab_all.html", description: "Analyze projectile data" },
    { title: "Projectile Sampling Distributions", url: "https://phet.colorado.edu/sims/html/projectile-sampling-distributions/latest/projectile-sampling-distributions_all.html", description: "Explore sampling distributions with projectiles" },
    { title: "Bumper", url: "https://phet.colorado.edu/sims/html/bumper/latest/bumper_all.html", description: "Explore 1D collisions" },
    { title: "Collision Lab", url: "https://phet.colorado.edu/sims/html/collision-lab/latest/collision-lab_all.html", description: "Explore collisions in 1D and 2D" },
    { title: "Chains", url: "https://phet.colorado.edu/sims/html/chains/latest/chains_all.html", description: "Explore chain dynamics" },
    { title: "Vector Addition", url: "https://phet.colorado.edu/sims/html/vector-addition/latest/vector-addition_all.html", description: "Add vectors graphically" },
    { title: "Vector Addition: Equations", url: "https://phet.colorado.edu/sims/html/vector-addition-equations/latest/vector-addition-equations_all.html", description: "Explore vector equations" },

    // Gravity & Orbits
    { title: "Gravity Force Lab", url: "https://phet.colorado.edu/sims/html/gravity-force-lab/latest/gravity-force-lab_all.html", description: "Visualize gravitational force" },
    { title: "Gravity Force Lab: Basics", url: "https://phet.colorado.edu/sims/html/gravity-force-lab-basics/latest/gravity-force-lab-basics_all.html", description: "Introduction to gravity" },
    { title: "Gravity and Orbits", url: "https://phet.colorado.edu/sims/html/gravity-and-orbits/latest/gravity-and-orbits_all.html", description: "Move the sun, earth, moon and space station" },
    { title: "Kepler's Laws", url: "https://phet.colorado.edu/sims/html/keplers-laws/latest/keplers-laws_all.html", description: "Explore planetary motion" },
    { title: "My Solar System", url: "https://phet.colorado.edu/sims/html/my-solar-system/latest/my-solar-system_all.html", description: "Build your own solar system" },

    // Energy & Springs
    { title: "Energy Skate Park", url: "https://phet.colorado.edu/sims/html/energy-skate-park/latest/energy-skate-park_all.html", description: "Learn about energy conservation" },
    { title: "Energy Skate Park: Basics", url: "https://phet.colorado.edu/sims/html/energy-skate-park-basics/latest/energy-skate-park-basics_all.html", description: "Introduction to energy conservation" },
    { title: "Energy Forms and Changes", url: "https://phet.colorado.edu/sims/html/energy-forms-and-changes/latest/energy-forms-and-changes_all.html", description: "Explore energy transfer and transformation" },
    { title: "Masses and Springs", url: "https://phet.colorado.edu/sims/html/masses-and-springs/latest/masses-and-springs_all.html", description: "Hang masses from springs" },
    { title: "Masses and Springs: Basics", url: "https://phet.colorado.edu/sims/html/masses-and-springs-basics/latest/masses-and-springs-basics_all.html", description: "Introduction to spring systems" },
    { title: "Hooke's Law", url: "https://phet.colorado.edu/sims/html/hookes-law/latest/hookes-law_all.html", description: "Stretch and compress springs" },
    { title: "Pendulum Lab", url: "https://phet.colorado.edu/sims/html/pendulum-lab/latest/pendulum-lab_all.html", description: "Play with pendulums" },

    // Fluids & Pressure
    { title: "Under Pressure", url: "https://phet.colorado.edu/sims/html/under-pressure/latest/under-pressure_all.html", description: "Explore pressure in fluids" },
    { title: "Buoyancy", url: "https://phet.colorado.edu/sims/html/buoyancy/latest/buoyancy_all.html", description: "Why do objects float or sink?" },
    { title: "Buoyancy: Basics", url: "https://phet.colorado.edu/sims/html/buoyancy-basics/latest/buoyancy-basics_all.html", description: "Introduction to buoyancy" },
    { title: "Density", url: "https://phet.colorado.edu/sims/html/density/latest/density_all.html", description: "Explore density with blocks" },

    // Waves & Sound
    { title: "Wave Interference", url: "https://phet.colorado.edu/sims/html/wave-interference/latest/wave-interference_all.html", description: "Make waves with water, sound, and light" },
    { title: "Waves Intro", url: "https://phet.colorado.edu/sims/html/waves-intro/latest/waves-intro_all.html", description: "Introduction to waves" },
    { title: "Wave on a String", url: "https://phet.colorado.edu/sims/html/wave-on-a-string/latest/wave-on-a-string_all.html", description: "Wiggle the end of a string" },
    { title: "Fourier: Making Waves", url: "https://phet.colorado.edu/sims/html/fourier-making-waves/latest/fourier-making-waves_all.html", description: "Build waves with Fourier series" },
    { title: "Normal Modes", url: "https://phet.colorado.edu/sims/html/normal-modes/latest/normal-modes_all.html", description: "Explore standing waves and normal modes" },
    { title: "Sound Waves", url: "https://phet.colorado.edu/sims/html/sound-waves/latest/sound-waves_all.html", description: "Explore sound wave properties" },

    // Light & Optics
    { title: "Bending Light", url: "https://phet.colorado.edu/sims/html/bending-light/latest/bending-light_all.html", description: "Explore refraction of light" },
    { title: "Color Vision", url: "https://phet.colorado.edu/sims/html/color-vision/latest/color-vision_all.html", description: "Make a rainbow by mixing light" },
    { title: "Geometric Optics", url: "https://phet.colorado.edu/sims/html/geometric-optics/latest/geometric-optics_all.html", description: "How lenses and mirrors work" },
    { title: "Geometric Optics: Basics", url: "https://phet.colorado.edu/sims/html/geometric-optics-basics/latest/geometric-optics-basics_all.html", description: "Introduction to lenses and mirrors" },
    { title: "Blackbody Spectrum", url: "https://phet.colorado.edu/sims/html/blackbody-spectrum/latest/blackbody-spectrum_all.html", description: "How does temperature affect spectra?" },

    // Electricity & Magnetism
    { title: "Balloons and Static Electricity", url: "https://phet.colorado.edu/sims/html/balloons-and-static-electricity/latest/balloons-and-static-electricity_all.html", description: "Explore static electricity" },
    { title: "John Travoltage", url: "https://phet.colorado.edu/sims/html/john-travoltage/latest/john-travoltage_all.html", description: "Make sparks fly with static electricity" },
    { title: "Charges and Fields", url: "https://phet.colorado.edu/sims/html/charges-and-fields/latest/charges-and-fields_all.html", description: "Explore electric fields" },
    { title: "Coulomb's Law", url: "https://phet.colorado.edu/sims/html/coulombs-law/latest/coulombs-law_all.html", description: "Explore electrostatic force" },
    { title: "Capacitor Lab: Basics", url: "https://phet.colorado.edu/sims/html/capacitor-lab-basics/latest/capacitor-lab-basics_all.html", description: "Explore capacitors" },
    { title: "Circuit Construction Kit (AC)", url: "https://phet.colorado.edu/sims/html/circuit-construction-kit-ac/latest/circuit-construction-kit-ac_all.html", description: "Build AC circuits" },
    { title: "CCK AC: Virtual Lab", url: "https://phet.colorado.edu/sims/html/circuit-construction-kit-ac-virtual-lab/latest/circuit-construction-kit-ac-virtual-lab_all.html", description: "Advanced AC circuit lab" },
    { title: "Circuit Construction Kit (DC)", url: "https://phet.colorado.edu/sims/html/circuit-construction-kit-dc/latest/circuit-construction-kit-dc_all.html", description: "Build DC circuits" },
    { title: "CCK DC: Virtual Lab", url: "https://phet.colorado.edu/sims/html/circuit-construction-kit-dc-virtual-lab/latest/circuit-construction-kit-dc-virtual-lab_all.html", description: "Advanced DC circuit lab" },
    { title: "Ohm's Law", url: "https://phet.colorado.edu/sims/html/ohms-law/latest/ohms-law_all.html", description: "V = I × R" },
    { title: "Resistance in a Wire", url: "https://phet.colorado.edu/sims/html/resistance-in-a-wire/latest/resistance-in-a-wire_all.html", description: "How does resistance work?" },
    { title: "Faraday's Law", url: "https://phet.colorado.edu/sims/html/faradays-law/latest/faradays-law_all.html", description: "Generate electricity with magnets" },
    { title: "Faraday's Electromagnetic Lab", url: "https://phet.colorado.edu/sims/html/faradays-electromagnetic-lab/latest/faradays-electromagnetic-lab_all.html", description: "Explore electromagnetic phenomena" },
    { title: "Generator", url: "https://phet.colorado.edu/sims/html/generator/latest/generator_all.html", description: "Generate electricity" },
    { title: "Magnet and Compass", url: "https://phet.colorado.edu/sims/html/magnet-and-compass/latest/magnet-and-compass_all.html", description: "Explore magnets and compasses" },
    { title: "Magnets and Electromagnets", url: "https://phet.colorado.edu/sims/html/magnets-and-electromagnets/latest/magnets-and-electromagnets_all.html", description: "Explore magnets and electromagnets" },

    // Nuclear & Atomic Physics
    { title: "Rutherford Scattering", url: "https://phet.colorado.edu/sims/html/rutherford-scattering/latest/rutherford-scattering_all.html", description: "See how atoms are structured" },
    { title: "Models of the Hydrogen Atom", url: "https://phet.colorado.edu/sims/html/models-of-the-hydrogen-atom/latest/models-of-the-hydrogen-atom_all.html", description: "Compare hydrogen atom models" },

    // Quantum Physics
    { title: "Quantum Measurement", url: "https://phet.colorado.edu/sims/html/quantum-measurement/latest/quantum-measurement_all.html", description: "Explore quantum measurement and states" },
    { title: "Quantum Coin Toss", url: "https://phet.colorado.edu/sims/html/quantum-coin-toss/latest/quantum-coin-toss_all.html", description: "Explore quantum probability" },

    // ===== CHEMISTRY =====
    // Acids, Bases & Solutions
    { title: "Acid-Base Solutions", url: "https://phet.colorado.edu/sims/html/acid-base-solutions/latest/acid-base-solutions_all.html", description: "Explore acids and bases" },
    { title: "pH Scale", url: "https://phet.colorado.edu/sims/html/ph-scale/latest/ph-scale_all.html", description: "Test pH of liquids" },
    { title: "pH Scale: Basics", url: "https://phet.colorado.edu/sims/html/ph-scale-basics/latest/ph-scale-basics_all.html", description: "Introduction to pH" },
    { title: "Concentration", url: "https://phet.colorado.edu/sims/html/concentration/latest/concentration_all.html", description: "Make solutions by dissolving" },
    { title: "Molarity", url: "https://phet.colorado.edu/sims/html/molarity/latest/molarity_all.html", description: "Calculate solution concentrations" },
    { title: "Beer's Law Lab", url: "https://phet.colorado.edu/sims/html/beers-law-lab/latest/beers-law-lab_all.html", description: "Explore light absorption" },

    // Atoms & Molecules
    { title: "Atomic Interactions", url: "https://phet.colorado.edu/sims/html/atomic-interactions/latest/atomic-interactions_all.html", description: "How atoms attract and repel" },
    { title: "Build an Atom", url: "https://phet.colorado.edu/sims/html/build-an-atom/latest/build-an-atom_all.html", description: "Build atoms, ions, and isotopes" },
    { title: "Build a Molecule", url: "https://phet.colorado.edu/sims/html/build-a-molecule/latest/build-a-molecule_all.html", description: "Build molecules from atoms" },
    { title: "Isotopes and Atomic Mass", url: "https://phet.colorado.edu/sims/html/isotopes-and-atomic-mass/latest/isotopes-and-atomic-mass_all.html", description: "How isotopes affect mass" },
    { title: "Molecule Polarity", url: "https://phet.colorado.edu/sims/html/molecule-polarity/latest/molecule-polarity_all.html", description: "When is a molecule polar?" },
    { title: "Molecule Shapes", url: "https://phet.colorado.edu/sims/html/molecule-shapes/latest/molecule-shapes_all.html", description: "Explore 3D molecular geometry" },
    { title: "Molecule Shapes: Basics", url: "https://phet.colorado.edu/sims/html/molecule-shapes-basics/latest/molecule-shapes-basics_all.html", description: "Introduction to molecular geometry" },
    { title: "Molecules and Light", url: "https://phet.colorado.edu/sims/html/molecules-and-light/latest/molecules-and-light_all.html", description: "How molecules interact with light" },

    // Reactions
    { title: "Balancing Chemical Equations", url: "https://phet.colorado.edu/sims/html/balancing-chemical-equations/latest/balancing-chemical-equations_all.html", description: "Balance chemical equations" },
    { title: "Reactants, Products and Leftovers", url: "https://phet.colorado.edu/sims/html/reactants-products-and-leftovers/latest/reactants-products-and-leftovers_all.html", description: "Explore limiting reactants" },

    // States of Matter
    { title: "States of Matter", url: "https://phet.colorado.edu/sims/html/states-of-matter/latest/states-of-matter_all.html", description: "Watch atoms change phase" },
    { title: "States of Matter: Basics", url: "https://phet.colorado.edu/sims/html/states-of-matter-basics/latest/states-of-matter-basics_all.html", description: "Introduction to phases" },
    { title: "Gas Properties", url: "https://phet.colorado.edu/sims/html/gas-properties/latest/gas-properties_all.html", description: "Pump gas molecules into a box" },
    { title: "Gases: Intro", url: "https://phet.colorado.edu/sims/html/gases-intro/latest/gases-intro_all.html", description: "Introduction to gas behavior" },
    { title: "Diffusion", url: "https://phet.colorado.edu/sims/html/diffusion/latest/diffusion_all.html", description: "Watch particles spread out" },
    { title: "Density", url: "https://phet.colorado.edu/sims/html/density/latest/density_all.html", description: "Explore density with blocks" },

    // ===== MATHEMATICS =====
    // Arithmetic & Numbers
    { title: "Arithmetic", url: "https://phet.colorado.edu/sims/html/arithmetic/latest/arithmetic_all.html", description: "Practice arithmetic" },
    { title: "Make a Ten", url: "https://phet.colorado.edu/sims/html/make-a-ten/latest/make-a-ten_all.html", description: "Explore addition strategies" },
    { title: "Number Compare", url: "https://phet.colorado.edu/sims/html/number-compare/latest/number-compare_all.html", description: "Compare numbers" },
    { title: "Number Pairs", url: "https://phet.colorado.edu/sims/html/number-pairs/latest/number-pairs_all.html", description: "Explore number pairs" },
    { title: "Number Play", url: "https://phet.colorado.edu/sims/html/number-play/latest/number-play_all.html", description: "Play with numbers" },
    { title: "Number Line: Distance", url: "https://phet.colorado.edu/sims/html/number-line-distance/latest/number-line-distance_all.html", description: "Find distances on a number line" },
    { title: "Number Line: Integers", url: "https://phet.colorado.edu/sims/html/number-line-integers/latest/number-line-integers_all.html", description: "Learn about integers" },
    { title: "Number Line: Operations", url: "https://phet.colorado.edu/sims/html/number-line-operations/latest/number-line-operations_all.html", description: "Operations on number line" },

    // Fractions
    { title: "Build a Fraction", url: "https://phet.colorado.edu/sims/html/build-a-fraction/latest/build-a-fraction_all.html", description: "Build fractions from parts" },
    { title: "Fraction Matcher", url: "https://phet.colorado.edu/sims/html/fraction-matcher/latest/fraction-matcher_all.html", description: "Match fractions to pictures" },
    { title: "Fractions: Equality", url: "https://phet.colorado.edu/sims/html/fractions-equality/latest/fractions-equality_all.html", description: "Explore equivalent fractions" },
    { title: "Fractions: Intro", url: "https://phet.colorado.edu/sims/html/fractions-intro/latest/fractions-intro_all.html", description: "Learn about fractions" },
    { title: "Fractions: Mixed Numbers", url: "https://phet.colorado.edu/sims/html/fractions-mixed-numbers/latest/fractions-mixed-numbers_all.html", description: "Work with mixed numbers" },

    // Ratios & Proportions
    { title: "Proportion Playground", url: "https://phet.colorado.edu/sims/html/proportion-playground/latest/proportion-playground_all.html", description: "Play with proportions" },
    { title: "Ratio and Proportion", url: "https://phet.colorado.edu/sims/html/ratio-and-proportion/latest/ratio-and-proportion_all.html", description: "Explore ratios" },
    { title: "Unit Rates", url: "https://phet.colorado.edu/sims/html/unit-rates/latest/unit-rates_all.html", description: "Explore unit rates" },
    { title: "Mean: Share and Balance", url: "https://phet.colorado.edu/sims/html/mean-share-and-balance/latest/mean-share-and-balance_all.html", description: "Understand the mean" },

    // Algebra & Equations
    { title: "Equality Explorer", url: "https://phet.colorado.edu/sims/html/equality-explorer/latest/equality-explorer_all.html", description: "Explore equations" },
    { title: "Equality Explorer: Basics", url: "https://phet.colorado.edu/sims/html/equality-explorer-basics/latest/equality-explorer-basics_all.html", description: "Introduction to equations" },
    { title: "Equality Explorer: Two Variables", url: "https://phet.colorado.edu/sims/html/equality-explorer-two-variables/latest/equality-explorer-two-variables_all.html", description: "Two-variable equations" },
    { title: "Expression Exchange", url: "https://phet.colorado.edu/sims/html/expression-exchange/latest/expression-exchange_all.html", description: "Make algebraic expressions" },
    { title: "Function Builder", url: "https://phet.colorado.edu/sims/html/function-builder/latest/function-builder_all.html", description: "Build functions" },
    { title: "Function Builder: Basics", url: "https://phet.colorado.edu/sims/html/function-builder-basics/latest/function-builder-basics_all.html", description: "Introduction to functions" },

    // Graphing
    { title: "Graphing Lines", url: "https://phet.colorado.edu/sims/html/graphing-lines/latest/graphing-lines_all.html", description: "Explore linear functions" },
    { title: "Graphing Quadratics", url: "https://phet.colorado.edu/sims/html/graphing-quadratics/latest/graphing-quadratics_all.html", description: "Explore parabolas" },
    { title: "Graphing Slope-Intercept", url: "https://phet.colorado.edu/sims/html/graphing-slope-intercept/latest/graphing-slope-intercept_all.html", description: "Graph y = mx + b" },

    // Geometry & Area Models
    { title: "Area Builder", url: "https://phet.colorado.edu/sims/html/area-builder/latest/area-builder_all.html", description: "Build shapes and explore area" },
    { title: "Area Model Algebra", url: "https://phet.colorado.edu/sims/html/area-model-algebra/latest/area-model-algebra_all.html", description: "Visualize polynomial multiplication" },
    { title: "Area Model Decimals", url: "https://phet.colorado.edu/sims/html/area-model-decimals/latest/area-model-decimals_all.html", description: "Multiply decimals" },
    { title: "Area Model Introduction", url: "https://phet.colorado.edu/sims/html/area-model-introduction/latest/area-model-introduction_all.html", description: "Introduction to area models" },
    { title: "Area Model Multiplication", url: "https://phet.colorado.edu/sims/html/area-model-multiplication/latest/area-model-multiplication_all.html", description: "Visualize multiplication" },
    { title: "Quadrilateral", url: "https://phet.colorado.edu/sims/html/quadrilateral/latest/quadrilateral_all.html", description: "Explore quadrilateral properties" },
    { title: "Trig Tour", url: "https://phet.colorado.edu/sims/html/trig-tour/latest/trig-tour_all.html", description: "Explore trigonometry" },

    // Calculus & Statistics
    { title: "Calculus Grapher", url: "https://phet.colorado.edu/sims/html/calculus-grapher/latest/calculus-grapher_all.html", description: "Explore calculus concepts" },
    { title: "Curve Fitting", url: "https://phet.colorado.edu/sims/html/curve-fitting/latest/curve-fitting_all.html", description: "Fit curves to data" },
    { title: "Center and Variability", url: "https://phet.colorado.edu/sims/html/center-and-variability/latest/center-and-variability_all.html", description: "Explore data distributions" },
    { title: "Least-Squares Regression", url: "https://phet.colorado.edu/sims/html/least-squares-regression/latest/least-squares-regression_all.html", description: "Fit data with regression lines" },
    { title: "Plinko Probability", url: "https://phet.colorado.edu/sims/html/plinko-probability/latest/plinko-probability_all.html", description: "Explore probability" },

    // ===== BIOLOGY & EARTH SCIENCE =====
    { title: "Build a Nucleus", url: "https://phet.colorado.edu/sims/html/build-a-nucleus/latest/build-a-nucleus_all.html", description: "Build atomic nuclei" },
    { title: "Gene Expression Essentials", url: "https://phet.colorado.edu/sims/html/gene-expression-essentials/latest/gene-expression-essentials_all.html", description: "DNA to proteins" },
    { title: "Greenhouse Effect", url: "https://phet.colorado.edu/sims/html/greenhouse-effect/latest/greenhouse-effect_all.html", description: "Explore climate change" },
    { title: "Membrane Transport", url: "https://phet.colorado.edu/sims/html/membrane-transport/latest/membrane-transport_all.html", description: "Explore cell membrane transport" },
    { title: "Natural Selection", url: "https://phet.colorado.edu/sims/html/natural-selection/latest/natural-selection_all.html", description: "Watch evolution in action" },
    { title: "Neuron", url: "https://phet.colorado.edu/sims/html/neuron/latest/neuron_all.html", description: "Stimulate a neuron" }
];
window.PHET_SIMS = PHET_SIMS;

function setupPhetModalListeners() {
    const modal = document.getElementById("phet-modal");
    const closeBtn = document.getElementById("close-phet-modal");
    const cancelBtn = document.getElementById("cancel-phet-modal");
    const searchInput = document.getElementById("phet-search");

    if (closeBtn) closeBtn.onclick = () => modal.style.display = "none";
    if (cancelBtn) cancelBtn.onclick = () => modal.style.display = "none";

    if (searchInput) {
        searchInput.addEventListener("input", window.debounce((e) => {
            renderPhetList(e.target.value);
        }, 300));
    }

    // Close on outside click
    window.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });
}

function openPhetModal() {
    const modal = document.getElementById("phet-modal");
    modal.style.display = "block";
    renderPhetList();
}

function renderPhetList(filter = "") {
    const list = document.getElementById("phet-list");
    list.innerHTML = "";

    const filteredSims = PHET_SIMS.filter(sim =>
        sim.title.toLowerCase().includes(filter.toLowerCase()) ||
        sim.description.toLowerCase().includes(filter.toLowerCase())
    );

    filteredSims.forEach(sim => {
        const item = document.createElement("div");
        item.style.cssText = "border: 2px solid #ddd; border-radius: 8px; padding: 12px; cursor: pointer; transition: all 0.2s; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);";
        item.onmouseover = () => {
            item.style.transform = "translateY(-4px)";
            item.style.boxShadow = "0 4px 12px rgba(0,0,0,0.15)";
            item.style.borderColor = "#667eea";
        };
        item.onmouseout = () => {
            item.style.transform = "translateY(0)";
            item.style.boxShadow = "0 2px 4px rgba(0,0,0,0.1)";
            item.style.borderColor = "#ddd";
        };
        item.onclick = () => insertPhetSim(sim);

        item.innerHTML = `
            <div style="text-align: center; margin-bottom: 8px;">
                <div style="display: inline-block; padding: 6px 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 6px; margin-bottom: 8px;">
                    <span style="color: white; font-weight: 600; font-size: 0.95em;">⚛️ ${escapeHtml(sim.title)}</span>
                </div>
            </div>
            <p style="margin: 0; font-size: 0.85em; color: #666; text-align: center; line-height: 1.4;">${escapeHtml(sim.description)}</p>
            <div style="text-align: center; margin-top: 8px;">
                <span style="font-size: 0.75em; color: #667eea; font-weight: 500;">Click to add to course</span>
            </div>
        `;
        list.appendChild(item);
    });

    if (filteredSims.length === 0) {
        list.innerHTML = '<p style="text-align: center; color: #999; padding: 40px;">No simulations found</p>';
    }
}

function insertPhetSim(sim) {
    document.getElementById("phet-modal").style.display = "none";

    // Start placement mode
    startPlacementMode('phet-simulator', sim);
}

// ===== LATEX MODAL HELPERS =====
function setupLatexHelpModalListeners() {
    const latexHelpModal = document.getElementById('latex-help-modal');
    const closeLatexHelpBtn = document.getElementById('close-latex-help-btn');
    const closeLatexHelpX = document.getElementById('close-latex-help');

    if (closeLatexHelpBtn) {
        closeLatexHelpBtn.addEventListener('click', () => {
            if (latexHelpModal) latexHelpModal.style.display = 'none';
        });
    }

    if (closeLatexHelpX) {
        closeLatexHelpX.addEventListener('click', () => {
            if (latexHelpModal) latexHelpModal.style.display = 'none';
        });
    }

    // Close on outside click
    window.addEventListener('click', (e) => {
        if (e.target === latexHelpModal) {
            latexHelpModal.style.display = 'none';
        }
    });
}

function setupCourseSearchListeners() {
    // Debounce helper function
    const debounce = (func, delay) => {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func(...args), delay);
        };
    };

    // My Courses Search
    const myCoursesSearch = document.getElementById('myCoursesSearch');
    const clearMyCoursesSearch = document.getElementById('clearMyCoursesSearch');

    if (myCoursesSearch) {
        myCoursesSearch.addEventListener(
            'input',
            debounce((e) => {
                renderUserCourses(e.target.value);
            }, 150)
        );
    }

    if (clearMyCoursesSearch) {
        clearMyCoursesSearch.addEventListener('click', () => {
            if (myCoursesSearch) {
                myCoursesSearch.value = '';
                renderUserCourses('');
            }
        });
    }

    // Available Courses Search
    const availableCoursesSearch = document.getElementById('availableCoursesSearch');
    const clearAvailableCoursesSearch = document.getElementById('clearAvailableCoursesSearch');

    if (availableCoursesSearch) {
        availableCoursesSearch.addEventListener(
            'input',
            debounce((e) => {
                renderAvailableCourses(e.target.value);
            }, 150)
        );
    }

    if (clearAvailableCoursesSearch) {
        clearAvailableCoursesSearch.addEventListener('click', () => {
            if (availableCoursesSearch) {
                availableCoursesSearch.value = '';
                renderAvailableCourses('');
            }
        });
    }

    // Enrolled Courses Search
    const enrolledCoursesSearch = document.getElementById('enrolledCoursesSearch');
    const clearEnrolledCoursesSearch = document.getElementById('clearEnrolledCoursesSearch');

    if (enrolledCoursesSearch) {
        enrolledCoursesSearch.addEventListener(
            'input',
            debounce((e) => {
                // Filter and re-render enrolled courses
                const searchText = e.target.value;
                const assignmentsList = document.getElementById('assignments-list');
                if (assignmentsList) {
                    const filteredAssignments = filterCourseList(
                        Array.from(assignmentsList.querySelectorAll('[data-assignment-id]')),
                        searchText
                    );

                    // Show/hide assignments based on filter
                    assignmentsList.querySelectorAll('[data-assignment-id]').forEach(elem => {
                        const courseTitle = elem.querySelector('h5')?.textContent || '';
                        const matches = courseTitle.toLowerCase().includes(searchText.toLowerCase());
                        elem.style.display = matches ? 'block' : 'none';
                    });

                    // Show "no results" message if needed
                    const hasVisibleItems = Array.from(assignmentsList.children).some(
                        child => child.style.display !== 'none'
                    );
                    if (filteredAssignments.length === 0) {
                        assignmentsList.innerHTML = `<p><em>No assignments found matching "${escapeHtml(searchText)}"</em></p>`;
                        return;
                    }
                }
            }, 150)
        );
    }

    if (clearEnrolledCoursesSearch) {
        clearEnrolledCoursesSearch.addEventListener('click', () => {
            if (enrolledCoursesSearch) {
                enrolledCoursesSearch.value = '';
                const assignmentsList = document.getElementById('assignments-list');
                if (assignmentsList) {
                    assignmentsList.querySelectorAll('[data-assignment-id]').forEach(elem => {
                        elem.style.display = 'block';
                    });
                }
            }
        });
    }
}

function setupContentEditorListeners() {
    const contentEditor = document.getElementById('course-content-editor');
    if (!contentEditor) return;

    // Listen for Enter key to process LaTeX
    contentEditor.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && e.ctrlKey) {
            e.preventDefault();
            processLatexInEditor();
        }
    });

    // Auto-process LaTeX when editor loses focus
    contentEditor.addEventListener('blur', () => {
        // Small delay to ensure DOM is ready
        setTimeout(processLatexInEditor, 100);
    });

    // Fix empty editor state where it gets trapped
    const fixEmptyState = () => {
        // If there are no regular blocks (p, br, text) other than absolute wrappers
        const hasTextNode = Array.from(contentEditor.childNodes).some(n => 
            (n.nodeType === Node.TEXT_NODE && n.textContent.trim().length > 0) || 
            (n.nodeType === Node.ELEMENT_NODE && n.tagName === 'P') ||
            (n.nodeType === Node.ELEMENT_NODE && n.tagName === 'BR')
        );
        
        if (!hasTextNode) {
            const p = document.createElement('p');
            p.innerHTML = '<br>';
            contentEditor.appendChild(p);
        }
    };

    contentEditor.addEventListener('input', fixEmptyState);
    contentEditor.addEventListener('click', (e) => {
        if (e.target === contentEditor) {
            fixEmptyState();
        }
    });
}

// Initialize content editor listeners when page loads
document.addEventListener('DOMContentLoaded', () => {
    setupContentEditorListeners();
});

// Make functions globally accessible for modal buttons
window.closeLatexEditorModal = closeLatexEditorModal;
window.confirmLatexInsertion = confirmLatexInsertion;
window.insertLatexSnippet = insertLatexSnippet;
window.updateLatexPreview = updateLatexPreview;
window.processLatexInEditor = processLatexInEditor;

// ===== SIMULATOR MARKETPLACE & STUDIO INTEGRATION =====

function renderSimulatorMarketplace() {
    const container = document.getElementById('simulator-marketplace-section');
    if (!container) return;

    container.innerHTML = '<h3>🎮 Simulator Marketplace</h3><p style="color: var(--text-muted);">Loading...</p>';

    fetch(`${API_BASE_URL}/api/simulators?limit=12&sort=popular`, {
        credentials: 'include'
    })
    .then(r => r.json())
    .then(data => {
        if (!data.success) return;
        const sims = data.data.simulators || [];

        let html = `<h3>🎮 Simulator Marketplace</h3>
        <div style="display: flex; gap: 10px; margin-bottom: 15px; flex-wrap: wrap;">
            <button onclick="openSimulatorStudio()" class="primary-btn" style="padding: 8px 16px;">✨ Create New Simulator</button>
            <button onclick="showFullMarketplace()" class="secondary-btn" style="padding: 8px 16px;">Browse All →</button>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 15px;">`;

        sims.forEach(sim => {
            html += `
            <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 15px; cursor: pointer;" onclick="viewSimulatorDetail(${sim.id})">
                <h4 style="color: var(--text-light); margin-bottom: 8px;">${escapeHtml(sim.title)}</h4>
                <p style="color: var(--text-muted); font-size: 0.85em; margin-bottom: 10px;">${escapeHtml(sim.description || 'No description')}</p>
                <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8em; color: var(--text-muted);">
                    <span>by ${escapeHtml(sim.creator_email || 'Unknown')}</span>
                    <span>⬇️ ${sim.downloads || 0} | ⭐ ${sim.rating || '0.00'}</span>
                </div>
                <div style="display: flex; gap: 8px; margin-top: 10px;">
                    <button onclick="event.stopPropagation(); forkSimulator(${sim.id})" style="flex:1; padding: 6px; background: var(--primary); color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 0.8em;">🍴 Fork</button>
                    <button onclick="event.stopPropagation(); viewSimulatorInStudio(${sim.id})" style="flex:1; padding: 6px; background: var(--secondary); color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 0.8em;">▶ Run</button>
                </div>
            </div>`;
        });

        html += '</div>';
        container.innerHTML = html;
    })
    .catch(err => {
        console.error('Error loading marketplace:', err);
        container.innerHTML = '<h3>🎮 Simulator Marketplace</h3><p style="color: var(--text-muted);">Failed to load simulators.</p>';
    });
}

function openSimulatorStudio() {
    const baseUrl = window.location.pathname.includes('github.io')
        ? 'https://virat-sisodiya.github.io/Veelearn/veelearn-frontend'
        : window.location.origin;
    window.open(`${baseUrl}/scratch-studio.html`, 'simulator-studio', 'width=1400,height=900');
}

function viewSimulatorInStudio(simulatorId) {
    const baseUrl = window.location.pathname.includes('github.io')
        ? 'https://virat-sisodiya.github.io/Veelearn/veelearn-frontend'
        : window.location.origin;
    // Prefer player for running; fetch to detect type
    fetch(`${API_BASE_URL}/api/simulators/${simulatorId}`, { credentials: 'include' })
        .then(r => r.json())
        .then(data => {
            if (!data.success) {
                window.open(`${baseUrl}/scratch-player.html?simId=${simulatorId}`, 'simulator-player', 'width=560,height=520');
                return;
            }
            const sim = data.data;
            let blocks = sim.blocks;
            if (typeof blocks === 'string') {
                try { blocks = JSON.parse(blocks); } catch (_) {}
            }
            const isScratch = sim.sim_type === 'scratch' || (blocks && blocks.format === 'veelearn-scratch-1');
            if (isScratch) {
                window.open(`${baseUrl}/scratch-player.html?simId=${simulatorId}`, 'simulator-player', 'width=560,height=520');
            } else {
                window.open(`${baseUrl}/simulator-studio.html?viewOnly=true&simId=${simulatorId}`, 'simulator-studio', 'width=1400,height=900');
            }
        })
        .catch(() => {
            window.open(`${baseUrl}/scratch-player.html?simId=${simulatorId}`, 'simulator-player', 'width=560,height=520');
        });
}

function viewSimulatorDetail(simulatorId) {
    fetch(`${API_BASE_URL}/api/simulators/${simulatorId}`, { credentials: 'include' })
    .then(r => r.json())
    .then(data => {
        if (!data.success) return;
        const sim = data.data;

        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.style.display = 'block';
        modal.innerHTML = `
        <div class="modal-content" style="max-width: 700px;">
            <span class="close-modal" onclick="this.closest('.modal').remove()">&times;</span>
            <h2>${escapeHtml(sim.title)}</h2>
            <p style="color: var(--text-muted); margin: 10px 0;">${escapeHtml(sim.description || 'No description')}</p>
            <div style="display: flex; gap: 15px; margin: 15px 0; color: var(--text-muted); font-size: 0.9em;">
                <span>👤 ${escapeHtml(sim.creator_email || 'Unknown')}</span>
                <span>⬇️ ${sim.downloads || 0} downloads</span>
                <span>⭐ ${sim.rating || '0.00'}</span>
                <span>🍴 ${sim.fork_count || 0} forks</span>
                ${sim.forked_from ? `<span>Forked from #${sim.forked_from}</span>` : ''}
            </div>
            <div style="display: flex; gap: 10px; margin-top: 20px;">
                <button onclick="viewSimulatorInStudio(${sim.id}); this.closest('.modal').remove();" class="primary-btn">▶ Run Simulator</button>
                <button onclick="forkSimulator(${sim.id}); this.closest('.modal').remove();" class="secondary-btn">🍴 Fork & Edit</button>
                <button onclick="addMarketplaceSimToCourse(${sim.id}, '${escapeHtml(sim.title).replace(/'/g, "\\'")}'); this.closest('.modal').remove();" style="padding: 8px 16px; background: var(--accent); color: #000; border: none; border-radius: 4px; cursor: pointer;">📚 Add to Course</button>
            </div>
        </div>`;
        document.body.appendChild(modal);
        modal.addEventListener('click', (e) => { if (e.target === modal) modal.remove(); });
    })
    .catch(err => console.error('Error:', err));
}

async function forkSimulator(simulatorId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/simulators/${simulatorId}/fork`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include'
        });
        const data = await response.json();
        if (data.success) {
            alert('Simulator forked! Opening in editor...');
            const baseUrl = window.location.pathname.includes('github.io')
                ? 'https://virat-sisodiya.github.io/Veelearn/veelearn-frontend'
                : window.location.origin;
            window.open(`${baseUrl}/scratch-studio.html?simId=${data.data.simulatorId}`, 'simulator-studio', 'width=1400,height=900');
        } else {
            alert('Fork failed: ' + data.message);
        }
    } catch (err) {
        console.error('Fork error:', err);
        alert('Error forking simulator');
    }
}

function insertMarketplaceSimBlock(simulatorId, title) {
    const blockId = Date.now();
    courseBlocks.push({
        id: blockId,
        type: 'marketplace-simulator',
        title: title,
        simulatorId: simulatorId,
        data: { simulatorId: simulatorId }
    });
    insertSimulatorBlock(blockId, title, 'Marketplace Simulator');
}

function addMarketplaceSimToCourse(simulatorId, title) {
    const editorSection = document.getElementById("course-editor-section");
    const inCourseEditor = currentEditingCourseId && editorSection && getComputedStyle(editorSection).display !== "none";
    if (inCourseEditor) {
        insertMarketplaceSimBlock(simulatorId, title);
        return;
    }
    showCoursePickerForSimulator(simulatorId, title);
}

async function showCoursePickerForSimulator(simulatorId, title) {
    if (!currentUser) {
        alert('Please log in first to add simulators to your courses.');
        return;
    }

    // Resolve the simulator title if we weren't given one (e.g. marketplace redirect)
    if (!title) {
        try {
            const res = await fetch(`${API_BASE_URL}/api/simulators/${simulatorId}`, {
                headers: { Authorization: `Bearer ${authToken || localStorage.getItem('token') || ''}` },
                credentials: 'include'
            });
            const json = await res.json();
            if (json.success) title = json.data.title;
        } catch (_) { /* fall through */ }
        title = title || 'Simulator';
    }

    // Make sure we have the user's courses
    if (!myCourses || myCourses.length === 0) {
        try {
            const res = await fetch(`${API_BASE_URL}/api/courses`, {
                headers: { Authorization: `Bearer ${authToken || localStorage.getItem('token') || ''}` },
                credentials: 'include'
            });
            const json = await res.json();
            if (json.success) {
                myCourses = (json.data || []).filter((c) => {
                    const owner = c.creator_id != null ? c.creator_id : c.user_id;
                    return Number(owner) === Number(currentUser.id);
                });
                try { window.myCourses = myCourses; } catch (_) { /* ignore */ }
            }
        } catch (err) {
            console.error('Failed to load courses for picker:', err);
        }
    }

    const existing = document.getElementById('course-picker-modal');
    if (existing) existing.remove();

    const modal = document.createElement('div');
    modal.id = 'course-picker-modal';
    modal.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:10001;display:flex;align-items:center;justify-content:center;padding:20px;';

    const courseListHtml = (myCourses && myCourses.length > 0)
        ? myCourses.map(c => `
            <button class="course-picker-item" data-course-id="${c.id}"
                style="display:block;width:100%;text-align:left;padding:12px 14px;margin-bottom:8px;background:var(--panel,#18181b);border:1px solid var(--border,#3f3f46);border-radius:8px;color:var(--text,#fafafa);cursor:pointer;font-size:0.95em;">
                <strong>${escapeHtml(c.title)}</strong>
                <span style="display:block;font-size:0.8em;color:#a1a1aa;margin-top:2px;">${escapeHtml((c.description || '').slice(0, 80))}${c.status ? ` · ${escapeHtml(c.status)}` : ''}</span>
            </button>`).join('')
        : '<p style="color:#a1a1aa;padding:10px 0;">You haven\'t created any courses yet. Create a course first, then add this simulator to it.</p>';

    modal.innerHTML = `
      <div style="background:#09090b;border:1px solid #27272a;border-radius:12px;padding:20px;max-width:480px;width:100%;max-height:70vh;display:flex;flex-direction:column;box-shadow:0 20px 60px rgba(0,0,0,.5);">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
          <h3 style="color:#fafafa;margin:0;font-size:17px;">Add "${escapeHtml(title)}" to a course</h3>
          <button id="course-picker-close" style="background:transparent;border:none;color:#a1a1aa;font-size:22px;cursor:pointer;line-height:1;">&times;</button>
        </div>
        <p style="color:#a1a1aa;font-size:0.85em;margin:0 0 12px;">Pick one of your courses — it will open in the editor with the simulator placed for you.</p>
        <div style="overflow-y:auto;flex:1;">${courseListHtml}</div>
      </div>`;

    document.body.appendChild(modal);
    modal.querySelector('#course-picker-close').onclick = () => modal.remove();
    modal.addEventListener('click', (e) => { if (e.target === modal) modal.remove(); });

    modal.querySelectorAll('.course-picker-item').forEach(btn => {
        btn.addEventListener('click', () => {
            const courseId = parseInt(btn.dataset.courseId);
            modal.remove();
            editCourse(courseId);
            // The editor opens asynchronously (waits for quiz questions), so poll
            // until it's visible before inserting the simulator block.
            const started = Date.now();
            const waiter = setInterval(() => {
                const sec = document.getElementById('course-editor-section');
                if (sec && getComputedStyle(sec).display !== 'none') {
                    clearInterval(waiter);
                    insertMarketplaceSimBlock(simulatorId, title);
                } else if (Date.now() - started > 10000) {
                    clearInterval(waiter);
                }
            }, 150);
        });
    });
}

function showFullMarketplace() {
    const baseUrl = window.location.pathname.includes('github.io')
        ? 'https://virat-sisodiya.github.io/Veelearn/veelearn-frontend'
        : window.location.origin;
    window.open(`${baseUrl}/simulator-marketplace.html`, '_blank');
}

window.openSimulatorStudio = openSimulatorStudio;
window.viewSimulatorInStudio = viewSimulatorInStudio;
window.viewSimulatorDetail = viewSimulatorDetail;
window.forkSimulator = forkSimulator;
window.addMarketplaceSimToCourse = addMarketplaceSimToCourse;
window.showCoursePickerForSimulator = showCoursePickerForSimulator;
window.showFullMarketplace = showFullMarketplace;
window.renderSimulatorMarketplace = renderSimulatorMarketplace;

// ===== PAGINATION FUNCTIONS =====

function saveCurrentPageContent() {
    const editor = document.getElementById("course-content-editor");
    if (editor) {
        coursePages[currentPageIndex] = editor.innerHTML;
    }
}

function renderCurrentPage() {
    console.log(`Rendering page ${currentPageIndex + 1} of ${coursePages.length}`);
    const editor = document.getElementById("course-content-editor");
    if (!editor) {
        console.error("Editor not found in renderCurrentPage");
        return;
    }

    // Validate index
    if (currentPageIndex < 0) currentPageIndex = 0;
    if (currentPageIndex >= coursePages.length) currentPageIndex = coursePages.length - 1;

    editor.innerHTML = coursePages[currentPageIndex] || "";
    if (typeof normalizeAbsoluteEmbeds === 'function') normalizeAbsoluteEmbeds(editor);
    updatePageControls();
    if (typeof window.onCoursePageRendered === 'function') window.onCoursePageRendered();
}

function addNewPage() {
    console.log("Adding new page...");
    if (!Array.isArray(coursePages)) {
        console.error("coursePages is not an array! Resetting.");
        coursePages = [""];
    }
    saveCurrentPageContent();
    coursePages.push("");
    currentPageIndex = coursePages.length - 1;
    console.log("New page added. Total pages:", coursePages.length);
    renderCurrentPage();
}

function deleteCurrentPage() {
    if (coursePages.length <= 1) {
        alert("Cannot delete the only page.");
        return;
    }

    if (confirm("Are you sure you want to delete this page?")) {
        coursePages.splice(currentPageIndex, 1);
        if (currentPageIndex >= coursePages.length) {
            currentPageIndex = coursePages.length - 1;
        }
        renderCurrentPage();
    }
}

function changePage(delta) {
    saveCurrentPageContent();
    const newIndex = currentPageIndex + delta;
    if (newIndex >= 0 && newIndex < coursePages.length) {
        currentPageIndex = newIndex;
        renderCurrentPage();
    }
}

function updatePageControls() {
    const pageIndicator = document.getElementById("page-indicator");
    const prevBtn = document.getElementById("prev-page-btn");
    const nextBtn = document.getElementById("next-page-btn");

    if (pageIndicator) {
        pageIndicator.textContent = `Page ${currentPageIndex + 1} of ${coursePages.length}`;
    }

    if (prevBtn) prevBtn.disabled = currentPageIndex === 0;
    if (nextBtn) nextBtn.disabled = currentPageIndex === coursePages.length - 1;
    if (typeof window.renderPageStrip === 'function') window.renderPageStrip();
}

let currentViewerPageIndex = 0;
let viewerPages = [];

// ===== COURSE TIMER & ANTI-ABUSE =====
// ===== COURSE CREATION TIMER (SIMPLE & RELIABLE) =====
// Counts seconds of active editing. Goes idle after 60s of no typing in editor fields.
// No anti-macro pausing — just idle detection.

let courseTimer = {
    totalSeconds: 0,
    lastTypingTime: Date.now(),
    isIdle: false,
    intervalId: null
};

function startCourseTimer(initialSeconds = 0) {
    courseTimer.totalSeconds = initialSeconds;
    courseTimer.lastTypingTime = Date.now();
    courseTimer.isIdle = false;

    // Clear any existing interval
    if (courseTimer.intervalId) clearInterval(courseTimer.intervalId);

    updateTimerDisplay();

    courseTimer.intervalId = setInterval(() => {
        // Idle if no typing in editor for 60 seconds
        courseTimer.isIdle = (Date.now() - courseTimer.lastTypingTime > 60000);

        if (!courseTimer.isIdle) {
            courseTimer.totalSeconds++;
        }
        updateTimerDisplay();
    }, 1000);

    // Attach typing listeners to editor fields
    attachEditorTypingListeners();
}

function stopCourseTimer() {
    if (courseTimer.intervalId) clearInterval(courseTimer.intervalId);
    courseTimer.intervalId = null;
    updateTimerDisplay();
}

function updateTimerDisplay() {
    const valueEl = document.getElementById('course-timer-value');
    const statusEl = document.getElementById('course-timer-status');
    if (!valueEl) return;

    const h = Math.floor(courseTimer.totalSeconds / 3600);
    const m = Math.floor((courseTimer.totalSeconds % 3600) / 60);
    const s = courseTimer.totalSeconds % 60;
    valueEl.textContent = `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;

    if (statusEl) {
        if (courseTimer.isIdle) {
            statusEl.textContent = '(Idle - type in editor to resume)';
            valueEl.style.color = '#f59e0b';
        } else {
            statusEl.textContent = '(Tracking active time)';
            valueEl.style.color = '#4ade80';
        }
    }
}

// Track typing in the actual editor fields only
let _timerListenersAttached = false;
function attachEditorTypingListeners() {
    if (_timerListenersAttached) return;
    _timerListenersAttached = true;

    function onEditorActivity() {
        courseTimer.lastTypingTime = Date.now();
        if (courseTimer.isIdle) {
            courseTimer.isIdle = false;
            updateTimerDisplay();
        }
    }

    // Listen on the content editor, title, and description — input/keydown events only
    const editorEl = document.getElementById('course-content-editor');
    const titleEl = document.getElementById('course-title');
    const descEl = document.getElementById('course-description');

    [editorEl, titleEl, descEl].filter(Boolean).forEach(el => {
        el.addEventListener('input', window.debounce(onEditorActivity, 1000), { passive: true });
        el.addEventListener('keydown', onEditorActivity, { passive: true });
    });
}

// ===== COURSE MANAGEMENT VARIABLES =====

// ===== PLACEMENT LOGIC (inline document flow) =====

const EDITOR_EMBED_FLOW_CSS =
    'position:relative; width:100%; max-width:720px; margin:1em 0; display:block; box-sizing:border-box;';

let placementDropAnchor = null;
let placementMoveHandler = null;
let placementKeyHandler = null;

function applyFlowEmbedStyles(el, extraCss) {
    if (!el) return;
    el.style.cssText = EDITOR_EMBED_FLOW_CSS + (extraCss || '');
    el.classList.add('editor-embed-flow');
}

function normalizeAbsoluteEmbeds(editor) {
    if (!editor) return;
    editor.querySelectorAll('.simulator-block, .phet-sim-wrapper, .quiz-question-placeholder').forEach((el) => {
        const styleAttr = el.getAttribute('style') || '';
        const computedPos = (el.style.position || '').toLowerCase();
        const looksAbsolute =
            computedPos === 'absolute' ||
            /position\s*:\s*absolute/i.test(styleAttr) ||
            (/left\s*:/i.test(styleAttr) && /top\s*:/i.test(styleAttr));
        if (!looksAbsolute && el.classList.contains('editor-embed-flow')) return;

        let keep = '';
        if (el.classList.contains('simulator-block')) {
            keep = 'background:#f0f0f0; padding:15px; border-left:4px solid #667eea; border-radius:4px; box-shadow:0 2px 8px rgba(0,0,0,0.08);';
        } else if (el.classList.contains('phet-sim-wrapper')) {
            keep = 'border:1px solid #ddd; border-radius:8px; overflow:hidden; background:#fff; box-shadow:0 2px 8px rgba(0,0,0,0.1);';
        } else if (el.classList.contains('quiz-question-placeholder')) {
            keep = 'background:rgba(102,126,234,0.15); border:2px dashed var(--primary,#667eea); padding:1em; border-radius:8px; cursor:pointer; user-select:none;';
        }
        applyFlowEmbedStyles(el, keep);
    });
}

function ensurePlacementDropIndicator() {
    let ind = document.getElementById('editor-drop-indicator');
    if (!ind) {
        ind = document.createElement('div');
        ind.id = 'editor-drop-indicator';
        ind.className = 'editor-drop-indicator';
        ind.setAttribute('aria-hidden', 'true');
        document.body.appendChild(ind);
    }
    return ind;
}

function hidePlacementDropIndicator() {
    const ind = document.getElementById('editor-drop-indicator');
    if (ind) ind.style.display = 'none';
}

function resolveEditorBlockAnchor(editor, node) {
    if (!editor || !node) return null;
    let el = node.nodeType === Node.TEXT_NODE ? node.parentElement : node;
    const blockSel =
        '.quiz-question-placeholder, .simulator-block, .phet-sim-wrapper, p, h1, h2, h3, h4, h5, h6, li, blockquote, pre, table, hr, div';
    while (el && el !== editor) {
        if (el.matches && el.matches(blockSel)) {
            let top = el;
            while (top.parentElement && top.parentElement !== editor) top = top.parentElement;
            return top.parentElement === editor ? top : el;
        }
        el = el.parentElement;
    }
    return null;
}

function updatePlacementDropFromPoint(clientX, clientY) {
    const editor = document.getElementById('course-content-editor');
    if (!editor || !isPlacementMode) return;

    const ind = ensurePlacementDropIndicator();
    const editorRect = editor.getBoundingClientRect();
    if (
        clientX < editorRect.left ||
        clientX > editorRect.right ||
        clientY < editorRect.top ||
        clientY > editorRect.bottom
    ) {
        hidePlacementDropIndicator();
        placementDropAnchor = null;
        return;
    }

    let range = null;
    if (document.caretRangeFromPoint) {
        range = document.caretRangeFromPoint(clientX, clientY);
    } else if (document.caretPositionFromPoint) {
        const pos = document.caretPositionFromPoint(clientX, clientY);
        if (pos) {
            range = document.createRange();
            range.setStart(pos.offsetNode, pos.offset);
            range.collapse(true);
        }
    }

    let anchorEl = null;
    if (range && editor.contains(range.startContainer)) {
        anchorEl = resolveEditorBlockAnchor(editor, range.startContainer);
    }
    if (!anchorEl) {
        const under = document.elementFromPoint(clientX, clientY);
        if (under && editor.contains(under)) anchorEl = resolveEditorBlockAnchor(editor, under);
    }

    let insertBefore = null;
    let parent = editor;
    if (anchorEl && editor.contains(anchorEl)) {
        const rect = anchorEl.getBoundingClientRect();
        const midY = rect.top + rect.height / 2;
        insertBefore = clientY < midY ? anchorEl : anchorEl.nextSibling;
        parent = anchorEl.parentNode || editor;
    }
    placementDropAnchor = { before: insertBefore, parent };

    let lineY = clientY;
    if (insertBefore && insertBefore.getBoundingClientRect) {
        lineY = insertBefore.getBoundingClientRect().top;
    } else if (anchorEl) {
        lineY = anchorEl.getBoundingClientRect().bottom;
    }

    ind.style.display = 'block';
    ind.style.left = `${editorRect.left + 8}px`;
    ind.style.width = `${Math.max(40, editorRect.width - 16)}px`;
    ind.style.top = `${lineY - 1}px`;
}

function insertNodeInDocumentFlow(node) {
    const editor = document.getElementById('course-content-editor');
    if (!editor || !node) return;

    if (placementDropAnchor && placementDropAnchor.parent && editor.contains(placementDropAnchor.parent)) {
        const { parent, before } = placementDropAnchor;
        if (before && parent.contains(before)) parent.insertBefore(node, before);
        else parent.appendChild(node);
    } else {
        editor.appendChild(node);
    }

    if (
        node.nextSibling == null ||
        (node.nextSibling.nodeType === Node.ELEMENT_NODE && node.nextSibling.tagName !== 'P')
    ) {
        const p = document.createElement('p');
        p.innerHTML = '<br>';
        if (node.nextSibling) node.parentNode.insertBefore(p, node.nextSibling);
        else node.parentNode.appendChild(p);
    }

    if (typeof window.pushEditorUndoSnapshot === 'function') window.pushEditorUndoSnapshot();
}

function cancelPlacementMode() {
    if (!isPlacementMode && !placementType) {
        hidePlacementDropIndicator();
        return;
    }
    isPlacementMode = false;
    placementType = null;
    placementData = null;
    placementDropAnchor = null;

    const editor = document.getElementById('course-content-editor');
    if (editor) {
        editor.style.cursor = 'text';
        editor.classList.remove('placement-mode');
    }
    hidePlacementDropIndicator();

    if (placementMoveHandler) {
        document.removeEventListener('mousemove', placementMoveHandler);
        placementMoveHandler = null;
    }
    if (placementKeyHandler) {
        document.removeEventListener('keydown', placementKeyHandler);
        placementKeyHandler = null;
    }

    const banner = document.getElementById('placement-mode-banner');
    if (banner) banner.remove();
}

function showPlacementBanner(message) {
    let banner = document.getElementById('placement-mode-banner');
    if (!banner) {
        banner = document.createElement('div');
        banner.id = 'placement-mode-banner';
        banner.className = 'placement-mode-banner';
        document.body.appendChild(banner);
    }
    banner.innerHTML = `${escapeHtml(message)} <kbd>Esc</kbd> to cancel`;
}

function startPlacementMode(type, data) {
    cancelPlacementMode();
    isPlacementMode = true;
    placementType = type;
    placementData = data;

    const editor = document.getElementById('course-content-editor');
    if (!editor) return;
    editor.style.position = 'relative';
    editor.style.cursor = 'crosshair';
    editor.classList.add('placement-mode');
    editor.focus();

    showPlacementBanner('Click between paragraphs to place the element.');

    placementMoveHandler = (e) => updatePlacementDropFromPoint(e.clientX, e.clientY);
    document.addEventListener('mousemove', placementMoveHandler);

    placementKeyHandler = (e) => {
        if (e.key === 'Escape') {
            e.preventDefault();
            cancelPlacementMode();
        }
    };
    document.addEventListener('keydown', placementKeyHandler);
}

function handleEditorClick(e) {
    if (!isPlacementMode) return;

    const editor = document.getElementById('course-content-editor');
    if (!editor || (!editor.contains(e.target) && e.target !== editor)) return;

    e.preventDefault();
    e.stopPropagation();

    updatePlacementDropFromPoint(e.clientX, e.clientY);

    if (placementType === 'visual-simulator' || placementType === 'block-simulator') {
        insertSimulatorAtPosition(placementData.id, placementData.title, placementData.type);
    } else if (placementType === 'quiz') {
        insertQuizPlaceholderAtPosition(placementData.id, placementData.text);
    } else if (placementType === 'phet-simulator') {
        insertPhetSimAtPosition(placementData);
    }

    cancelPlacementMode();
}

function insertSimulatorAtPosition(blockId, title, type) {
    const simulatorDiv = document.createElement('div');
    simulatorDiv.className = 'simulator-block editor-embed-flow';
    simulatorDiv.dataset.blockId = blockId;
    simulatorDiv.contentEditable = 'false';
    applyFlowEmbedStyles(
        simulatorDiv,
        'background:#f0f0f0; padding:15px; border-left:4px solid #667eea; border-radius:4px; box-shadow:0 2px 8px rgba(0,0,0,0.08);'
    );

    simulatorDiv.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap;">
            <div>
                <strong>${escapeHtml(type)}</strong>
                <p style="margin: 5px 0; color: #666;">${escapeHtml(title)}</p>
            </div>
            <div style="display: flex; gap: 10px;">
                <button type="button" onclick="openSliderConfigModal(${blockId})" style="padding: 5px 10px; background: #10b981; color: white; border: none; border-radius: 4px; cursor: pointer;">⚙️</button>
                <button type="button" onclick="handleEditSimulator(event, ${blockId})" style="padding: 5px 10px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer;">Edit</button>
                <button type="button" onclick="handleRemoveSimulator(event, ${blockId})" style="padding: 5px 10px; background: #f44336; color: white; border: none; border-radius: 4px; cursor: pointer;">Remove</button>
            </div>
        </div>
    `;

    insertNodeInDocumentFlow(simulatorDiv);
}

/** Absolute overlays removed — embeds stay in document flow */
function makeElementDraggable() {
    /* no-op */
}

function insertQuizPlaceholderAtPosition(questionId, questionText) {
    const placeholder = document.createElement('div');
    placeholder.className = 'quiz-question-placeholder editor-embed-flow';
    placeholder.dataset.questionId = questionId;
    placeholder.contentEditable = 'false';
    applyFlowEmbedStyles(
        placeholder,
        'background:rgba(102,126,234,0.15); border:2px dashed var(--primary,#667eea); padding:1em; border-radius:8px; cursor:pointer; user-select:none;'
    );

    const preview = String(questionText || '');
    placeholder.innerHTML = `
    <strong>Quiz Question:</strong> ${escapeHtml(preview.substring(0, 100))}${preview.length > 100 ? '...' : ''}
    <button type="button" class="quiz-placeholder-delete-btn" data-question-id="${questionId}" style="float:right; background: #e53e3e; color: white; border: none; border-radius: 4px; padding: 2px 6px; cursor: pointer; font-size: 0.8em;">Delete</button>
    <div style="font-size: 0.85em; color: #999; margin-top: 0.5em; clear: both;">Click to edit</div>
  `;

    placeholder.addEventListener('click', (e) => {
        if (e.target.closest('button')) return;
        const qId = placeholder.dataset.questionId;
        if (qId) openQuizModal(parseInt(qId, 10));
    });

    const deleteBtn = placeholder.querySelector('.quiz-placeholder-delete-btn');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const qId = parseInt(placeholder.dataset.questionId, 10);
            if (qId && !isNaN(qId) && confirm('Delete this question?')) {
                deleteQuizQuestion(qId);
            }
        });
    }

    insertNodeInDocumentFlow(placeholder);
}

function insertPhetSimAtPosition(sim) {
    const wrapper = document.createElement('div');
    wrapper.className = 'phet-sim-wrapper editor-embed-flow';
    wrapper.contentEditable = 'false';
    applyFlowEmbedStyles(
        wrapper,
        'border:1px solid #ddd; border-radius:8px; overflow:hidden; background:#fff; box-shadow:0 2px 8px rgba(0,0,0,0.1);'
    );

    wrapper.innerHTML = `
        <div style="background: #f0f0f0; padding: 10px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #ddd;">
            <strong>⚛️ ${escapeHtml(sim.title)}</strong>
            <button type="button" class="phet-remove-btn" style="background: #ff4444; color: white; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer;">Remove</button>
        </div>
        <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
            <iframe src="${escapeHtml(sim.url)}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" allowfullscreen></iframe>
        </div>
    `;

    const removeBtn = wrapper.querySelector('.phet-remove-btn');
    if (removeBtn) {
        removeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (confirm('Remove this simulator?')) wrapper.remove();
        });
    }

    insertNodeInDocumentFlow(wrapper);
}

// ===== VOLUNTEER HOURS, CERTIFICATES & SPONSORSHIPS =====

async function loadVolunteerStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/users/volunteer-stats`, {
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });
        const result = await response.json();
        if (result.success) {
            renderVolunteerStats(result.data);
        }
    } catch (err) {
        console.error('Error loading volunteer stats:', err);
    }
}

function renderVolunteerStats(data) {
    let container = document.getElementById('volunteer-stats-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'volunteer-stats-container';
        container.style.cssText = 'background: rgba(74, 222, 128, 0.1); border: 1px solid rgba(74, 222, 128, 0.3); border-radius: 12px; padding: 20px; margin-bottom: 20px;';

        const dashboards = ['superadmin-dashboard', 'admin-dashboard', 'user-dashboard'];
        for (const id of dashboards) {
            const dash = document.getElementById(id);
            if (dash && dash.style.display !== 'none') {
                dash.insertBefore(container, dash.firstChild);
                break;
            }
        }
    }

    const hours = data.total_volunteer_hours || 0;
    const verified = data.is_verified_creator;
    const certs = data.certificates || [];

    let certsHtml = '';
    if (certs.length > 0) {
        certsHtml = '<div style="margin-top: 15px; border-top: 1px solid rgba(74, 222, 128, 0.2); padding-top: 15px;"><strong style="font-size: 15px;">📜 Your Certificates:</strong><div style="display: flex; flex-direction: column; gap: 10px; margin-top: 10px;">';
        certs.forEach(cert => {
            certsHtml += `
        <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(102, 126, 234, 0.1); border: 1px solid rgba(102, 126, 234, 0.3); border-radius: 8px; padding: 12px 16px; flex-wrap: wrap; gap: 10px;">
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 20px;">🏆</span>
            <div>
              <strong>${cert.hours_certified} Hours Volunteer Certificate</strong>
              <div style="font-size: 12px; color: #999; margin-top: 2px;">Issued: ${new Date(cert.issued_at).toLocaleDateString()}</div>
            </div>
          </div>
          <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <a href="${API_BASE_URL}/api/certificates/verify/${escapeHtml(cert.verification_code)}?format=pdf" target="_blank" style="display: inline-flex; align-items: center; gap: 6px; background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 14px; cursor: pointer; transition: transform 0.2s;">⬇️ Download PDF</a>
            <a href="${API_BASE_URL}/api/certificates/verify/${escapeHtml(cert.verification_code)}" target="_blank" style="display: inline-flex; align-items: center; gap: 6px; background: rgba(74, 222, 128, 0.2); color: #4ade80; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 13px; border: 1px solid rgba(74, 222, 128, 0.3);">✔️ Verify</a>
          </div>
        </div>`;
        });
        certsHtml += '</div></div>';
    }

    let generateBtn = '';
    if (hours > 0 && certs.length === 0) {
        generateBtn = `
      <div style="margin-top: 15px; border-top: 1px solid rgba(74, 222, 128, 0.2); padding-top: 15px;">
        <p style="color: #999; margin: 0 0 10px 0; font-size: 13px;">Loading certificates... If none appear, try refreshing the page.</p>
      </div>`;
        setTimeout(() => loadVolunteerStats(), 2000);
    }

    container.innerHTML = `
        <h4 style="margin: 0 0 12px 0; color: #4ade80; font-size: 18px;">🤝 Volunteer Status</h4>
        <div style="display: flex; gap: 20px; align-items: center; flex-wrap: wrap;">
            <div style="background: rgba(0,0,0,0.2); padding: 8px 14px; border-radius: 6px;"><strong>Total Hours:</strong> ${hours.toFixed(1)}h</div>
            <div style="background: rgba(0,0,0,0.2); padding: 8px 14px; border-radius: 6px;"><strong>Status:</strong> ${verified ? '✅ Verified Creator' : '⏳ Not Yet Verified (need 20h)'}</div>
            <div style="background: rgba(0,0,0,0.2); padding: 8px 14px; border-radius: 6px;"><strong>Next Milestone:</strong> ${getNextMilestone(hours)}h</div>
        </div>
        ${certsHtml}
        ${generateBtn}
    `;
}

function getNextMilestone(currentHours) {
    const milestones = [5, 10, 20, 50, 100];
    for (const m of milestones) {
        if (currentHours < m) return m;
    }
    return 'All achieved!';
}

async function grantVolunteerHours(userId, email) {
    const hours = prompt(`Grant volunteer hours to ${email}:`, '5');
    if (!hours || isNaN(hours)) return;

    try {
        const response = await fetch(`${API_BASE_URL}/api/users/update-volunteer-hours`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            credentials: 'include',
            body: JSON.stringify({ user_id: userId, hours_to_add: parseFloat(hours) })
        });
        const result = await response.json();
        if (result.success) {
            alert(`Granted ${hours} volunteer hours to ${email}. New total: ${result.data.new_total}h`);
            loadAllUsers();
            loadVolunteerStats();
        } else {
            alert('Error: ' + result.message);
        }
    } catch (err) {
        console.error('Error granting hours:', err);
        alert('Error granting hours');
    }
}
window.grantVolunteerHours = grantVolunteerHours;

async function grantGems(userId, email) {
    const gems = prompt(`Grant gems to ${email}:\n(Use a negative number to remove gems)`, '50');
    if (gems === null || gems === '' || isNaN(gems) || parseInt(gems, 10) === 0) return;

    try {
        const response = await fetch(`${API_BASE_URL}/api/users/grant-gems`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            credentials: 'include',
            body: JSON.stringify({ user_id: userId, gems_to_add: parseInt(gems, 10) })
        });
        const result = await response.json();
        if (result.success) {
            const total = result.data?.new_total ?? '?';
            alert(`Updated gems for ${email}. New total: ${total}`);
            loadAllUsers();
        } else {
            alert('Error: ' + result.message);
        }
    } catch (err) {
        console.error('Error granting gems:', err);
        alert('Error granting gems');
    }
}
window.grantGems = grantGems;

// ===== TEACHER/STUDENT SYSTEM =====

// Become a teacher
async function becomeTeacher() {
    const confirm_msg = `⚠️ IMPORTANT: This action cannot be undone without superadmin approval.\n\n✔️ You will get a unique class code immediately\n✔️ You can see it and use it right away\n❌ BUT students can't enroll until superadmin approves\n\nContinue becoming a teacher?`;
    if (!confirm(confirm_msg)) return;

    try {
        const response = await fetch(`${API_BASE_URL}/api/user/become-teacher`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            credentials: 'include'
        });

        const result = await response.json();
        if (result.success) {
            alert(`✅ You're now a teacher!\n\nYour class code: ${result.data.classCode}\n\n📋 Next steps:\n1. Share this code with students\n2. Wait for superadmin to approve your teacher status\n3. Once approved, students can join using the code`);
            currentUser.role = 'teacher';
            currentUser.class_code = result.data.classCode;
            showUserDashboard();
        } else {
            alert('Error: ' + result.message);
        }
    } catch (err) {
        console.error('Error:', err);
        alert('Error requesting teacher role');
    }
}

// Enroll student in class
async function enrollInClass() {
    const classCode = document.getElementById('class-code-input').value.trim().toUpperCase();
    if (!classCode) {
        alert('Please enter a class code');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/student/enroll-class`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            credentials: 'include',
            body: JSON.stringify({ classCode })
        });

        const result = await response.json();
        if (result.success) {
            // Update current user role to student
            currentUser.role = 'student';
            alert('✅ Enrolled in class successfully!');
            document.getElementById('class-code-input').value = '';
            // Refresh dashboard to show student view
            showUserDashboard();
            setupTeacherStudentListeners();
            loadStudentAssignments();
        } else {
            alert('Error: ' + result.message);
        }
    } catch (err) {
        console.error('Error:', err);
        alert('Error enrolling in class');
    }
}

// Load student assignments
async function loadStudentAssignments() {
    if (currentUser.role !== 'student' && currentUser.role !== 'user') return;

    try {
        const response = await fetch(`${API_BASE_URL}/api/student/assignments`, {
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });

        const result = await response.json();
        if (result.success) {
            const assignmentsDiv = document.getElementById('assignments-list');
            // Filter out assignments that are already submitted
            const pendingAssignments = result.data.filter(a => !a.is_submitted);

            if (pendingAssignments.length === 0) {
                assignmentsDiv.innerHTML = '<p style="text-align: center; color: #999;">🎉 No pending assignments! You are all caught up.</p>';
                return;
            }

            assignmentsDiv.innerHTML = pendingAssignments.map(a => `
        <div style="background: #222; padding: 12px; border-radius: 4px; margin-bottom: 10px; border-left: 4px solid #667eea;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
              <strong>${escapeHtml(a.course_title)}</strong> - ${escapeHtml(a.title)}<br/>
              <small>Teacher: ${escapeHtml(a.teacher_email)}</small><br/>
              <small>Due: ${a.due_date ? escapeHtml(new Date(a.due_date).toLocaleDateString()) : 'No due date'}</small>
            </div>
            <button onclick="viewCourse(${a.course_id}, ${a.id})" class="primary-btn" style="padding: 8px 16px;">
              ▶️ Work on Assignment
            </button>
          </div>
        </div>
      `).join('');

            document.getElementById('student-assignments').style.display = 'block';
        }
    } catch (err) {
        console.error('Error loading assignments:', err);
    }
}

// Track quiz answers and calculate progress
function trackQuizAnswers(courseId) {
    // Use provided courseId or global courseQuestions if they belong to current course
    if (!courseId && courseQuestions.length === 0) {
        return { correctAnswers: 0, totalQuestions: 0, percentage: 0 };
    }

    let correctAnswers = 0;
    const totalQuestions = courseQuestions.length;

    // Check each quiz question for answers
    courseQuestions.forEach(question => {
        const questionElement = document.querySelector(`[data-question-id="${question.id}"]`);
        if (questionElement) {
            const selectedOption = questionElement.querySelector('input[type="radio"]:checked');
            if (selectedOption) {
                // Get the selected answer value
                const selectedValue = selectedOption.value;
                // Check if it's correct (correct answer is stored in question.correct_answer)
                if (selectedValue === String(question.correct_answer)) {
                    correctAnswers++;
                }
            }
        }
    });

    const percentage = totalQuestions > 0 ? Math.round((correctAnswers / totalQuestions) * 100) : 0;
    console.log(`Progress calculated: ${correctAnswers}/${totalQuestions} correct = ${percentage}%`);

    return {
        correctAnswers,
        totalQuestions,
        percentage
    };
}

// Calculate progress from quiz submissions
function calculateProgress(courseId) {
    const progress = trackQuizAnswers(courseId);
    return progress.percentage;
}

// Submit assignment work with automatic progress calculation
async function submitAssignmentWork(assignmentId, courseTitle) {
    // Calculate progress automatically from quiz answers
    const progress = trackQuizAnswers(null);
    const { correctAnswers, totalQuestions, percentage } = progress;

    // AUTO-TRACK: Removed the manual prompt/confirm as per user request
    console.log(`Auto-submitting work for assignment ${assignmentId}: ${correctAnswers}/${totalQuestions} (${percentage}%)`);

    try {
        const response = await fetch(`${API_BASE_URL}/api/student/submit-assignment`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                assignmentId,
                completionPercentage: percentage,
                correctAnswers: correctAnswers,
                totalQuestions: totalQuestions
            })
        });

        const result = await response.json();
        if (result.success) {
            const statusMsg = result.data.isLate ? '⏰ LATE' : '✅ ON TIME';
            alert(`✅ Work submitted!\n\nProgress: ${correctAnswers}/${totalQuestions} (${percentage}%)\nStatus: ${statusMsg}\n\nYour teacher has been notified.`);
            loadStudentAssignments();
            loadEnrolledCourses();
        } else {
            alert('Error: ' + result.message);
        }
    } catch (err) {
        console.error('Error:', err);
        alert('Error submitting work');
    }
}

// Load and display enrolled courses with progress tracking
async function loadEnrolledCourses() {
    if (currentUser.role !== 'student' && currentUser.role !== 'user') return;

    try {
        // Get enrolled courses (via class code)
        const response = await fetch(`${API_BASE_URL}/api/student/enrolled-courses`, {
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });

        const result = await response.json();
        if (result.success && result.data.length > 0) {
            const enrolledCoursesDiv = document.getElementById('enrolled-courses-list');
            if (!enrolledCoursesDiv) {
                console.warn('enrolled-courses-list div not found');
                return;
            }

            enrolledCoursesDiv.innerHTML = result.data
                .map(course => {
                    // Calculate questions answered correctly across all assignments
                    const correctAnswers = course.submissions
                        ? course.submissions.reduce((sum, s) => sum + (s.correct_answers || 0), 0)
                        : 0;
                    const totalQuestions = course.submissions
                        ? course.submissions.reduce((sum, s) => sum + (s.total_questions || 0), 0)
                        : 0;

                    // Use question-based progress as requested by user
                    const questionProgress = totalQuestions > 0 ? Math.round((correctAnswers / totalQuestions) * 100) : 0;

                    // Determine status
                    let status = '⏳ Not Started';
                    let statusColor = '#888';
                    if (questionProgress >= 100) {
                        status = '✅ Completed';
                        statusColor = '#4caf50';
                    } else if (questionProgress > 0) {
                        status = '▶️ In Progress';
                        statusColor = '#2196f3';
                    }

                    // Find earliest upcoming due date
                    let earliestDueDate = null;
                    if (course.assignments && course.assignments.length > 0) {
                        const now = new Date();
                        const upcoming = course.assignments
                            .filter(a => a.due_date && new Date(a.due_date) > now)
                            .sort((a, b) => new Date(a.due_date) - new Date(b.due_date));
                        if (upcoming.length > 0) {
                            earliestDueDate = new Date(upcoming[0].due_date).toLocaleDateString();
                        }
                    }

                    return `
            <div style="background: #222; padding: 12px; border-radius: 4px; margin-bottom: 10px; border-left: 4px solid #667eea;">
              <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="flex: 1;">
                  <strong>${escapeHtml(course.title)}</strong><br/>
                  <small style="color: #999;">Teacher: ${escapeHtml(course.teacher_email)}</small><br/>
                  ${earliestDueDate ? `<small style="color: #ff9800; font-weight: bold;">⏰ Next Due: ${escapeHtml(earliestDueDate)}</small><br/>` : ''}
                  <small style="color: #ccc; margin-top: 5px;">
                    📊 Progress: ${correctAnswers}/${totalQuestions} questions answered (${questionProgress}%)
                  </small><br/>
                  <div style="margin-top: 8px; background: #111; border-radius: 4px; height: 20px; overflow: hidden;">
                    <div style="width: ${questionProgress}%; height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); transition: width 0.3s ease; display: flex; align-items: center; justify-content: center;">
                      <span style="color: white; font-size: 0.75em; font-weight: bold; text-shadow: 0 1px 2px rgba(0,0,0,0.5);">${questionProgress}%</span>
                    </div>
                  </div>
                  <small style="color: ${statusColor}; margin-top: 5px; display: block; font-weight: bold;">${status}</small>
                </div>
                <button onclick="viewEnrolledCourse(${course.course_id})" class="primary-btn" style="padding: 8px 16px; white-space: nowrap;">👉 View</button>
              </div>
            </div>
          `;
                })
                .join('');

            document.getElementById('enrolled-courses-section').style.display = 'block';
        } else {
            document.getElementById('enrolled-courses-section').style.display = 'none';
        }
    } catch (err) {
        console.error('Error loading enrolled courses:', err);
    }
}

// View enrolled course
async function viewEnrolledCourse(courseId) {
    try {
        // Load course content
        const response = await fetch(`${API_BASE_URL}/api/courses/${courseId}`, {
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });

        const result = await response.json();
        if (result.success) {
            await loadCourseQuestions(courseId);
            viewCourse(courseId);
        }
    } catch (err) {
        console.error('Error loading course:', err);
    }
}

// Create assignment
async function createAssignment() {
    const courseId = document.getElementById('assignment-course-select').value;
    const dueDate = document.getElementById('assignment-due-date').value;

    if (!courseId) {
        alert('Please select a course');
        return;
    }

    if (currentUser.role !== 'teacher') {
        alert('Only teachers can create assignments');
        return;
    }

    const classCode = currentUser.class_code;
    if (!classCode) {
        alert('No class code found. Please become a teacher first');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/teacher/assign-course`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                classCode,
                courseId,
                title: document.getElementById('assignment-course-select').options[document.getElementById('assignment-course-select').selectedIndex].text,
                dueDate: dueDate || null
            })
        });

        const result = await response.json();
        if (result.success) {
            alert(`✅ Assignment created and sent to students in your class!\n\nAssignment ID: ${result.data.assignmentId}`);
            document.getElementById('assignment-course-select').value = '';
            document.getElementById('assignment-due-date').value = '';
        } else {
            alert('Error: ' + result.message);
        }
    } catch (err) {
        console.error('Error:', err);
        alert('Error creating assignment');
    }
}

// Store all courses for search filtering
let allCoursesForAssignment = [];

// Populate course dropdown for assignment creation
async function populateAssignmentCourseDropdown() {
    const select = document.getElementById('assignment-course-select');
    if (!select) return;

    try {
        // Fetch all courses from backend for teacher assignments
        // Use limit=1000 to get all courses at once without pagination
        const response = await fetch(`${API_BASE_URL}/api/courses/all?limit=1000`, {
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });

        const result = await response.json();

        // Clear existing options except the default
        select.innerHTML = '<option value="">Select a course...</option>';

        // Store all courses and add to dropdown
        // The endpoint returns {courses: [...], pagination: {...}}
        if (result.success && result.data && result.data.courses && result.data.courses.length > 0) {
            allCoursesForAssignment = result.data.courses;
            allCoursesForAssignment.forEach(course => {
                const option = document.createElement('option');
                option.value = course.id;
                option.textContent = course.title;
                option.dataset.description = course.description || '';
                select.appendChild(option);
            });
        } else if (myCourses && myCourses.length > 0) {
            // Fallback to user's own courses if endpoint not available
            allCoursesForAssignment = myCourses;
            myCourses.forEach(course => {
                const option = document.createElement('option');
                option.value = course.id;
                option.textContent = course.title;
                select.appendChild(option);
            });
        }
    } catch (err) {
        console.error('Error loading courses for assignment:', err);
        // Fallback to user's courses
        if (myCourses && myCourses.length > 0) {
            select.innerHTML = '<option value="">Select a course...</option>';
            allCoursesForAssignment = myCourses;
            myCourses.forEach(course => {
                const option = document.createElement('option');
                option.value = course.id;
                option.textContent = course.title;
                select.appendChild(option);
            });
        }
    }
}

// Search and filter assignment courses in real-time
function searchAssignmentCourses() {
    const searchInput = document.getElementById('assignmentCourseSearch');
    const select = document.getElementById('assignment-course-select');

    if (!searchInput || !select) return;

    const searchText = searchInput.value.toLowerCase().trim();

    // Clear dropdown
    select.innerHTML = '<option value="">Select a course...</option>';

    if (!searchText) {
        // Show all courses if search is empty
        allCoursesForAssignment.forEach(course => {
            const option = document.createElement('option');
            option.value = course.id;
            option.textContent = course.title;
            option.dataset.description = course.description || '';
            select.appendChild(option);
        });
    } else {
        // Filter courses by title or description (case-insensitive)
        const filteredCourses = allCoursesForAssignment.filter(course =>
            course.title.toLowerCase().includes(searchText) ||
            (course.description && course.description.toLowerCase().includes(searchText))
        );

        if (filteredCourses.length > 0) {
            filteredCourses.forEach(course => {
                const option = document.createElement('option');
                option.value = course.id;
                option.textContent = course.title;
                option.dataset.description = course.description || '';
                select.appendChild(option);
            });
        } else {
            const option = document.createElement('option');
            option.value = '';
            option.textContent = 'No courses found...';
            option.disabled = true;
            select.appendChild(option);
        }
    }
}

// Load teacher's classes and submissions
async function loadTeacherClasses() {
    if (currentUser.role !== 'teacher') return;

    try {
        const response = await fetch(`${API_BASE_URL}/api/teacher/my-classes`, {
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });

        const result = await response.json();
        console.log('Teacher classes result:', result);

        if (result.success && result.data && result.data.length > 0) {
            const classList = document.getElementById('my-classes-list');
            classList.innerHTML = result.data.map(cls => `
        <div style="background: #222; padding: 12px; border-radius: 4px; margin-bottom: 10px; border-left: 4px solid #4ade80;">
          <strong>${escapeHtml(cls.classCode)}</strong> - ${cls.studentCount} student(s)
          <button onclick="viewClassSubmissions('${escapeHtml(cls.classCode)}')" class="primary-btn" style="padding: 6px 12px; margin-left: 10px; font-size: 0.85em;">
            📊 View Progress
          </button>
        </div>
      `).join('');
        } else {
            const classList = document.getElementById('my-classes-list');
            classList.innerHTML = '<p style="color: #999; font-size: 0.9em;">No classes yet. Assign a course to create a class.</p>';
        }
    } catch (err) {
        console.error('Error loading classes:', err);
    }
}

// View class submissions
// Display student accuracy with color coding
function displayStudentAccuracy(submission) {
    if (submission.accuracy === null || submission.total_questions === 0) {
        return { html: 'N/A', color: '#888' };
    }

    const percent = submission.accuracy_percent;
    let color = '#888'; // Gray - not started

    // Handle caso where no submission exists or no questions in course
    if (submission.total_questions === 0 || submission.correct_answers === null) {
        return { html: '<span style="color: #999;">Not Started</span>', color: '#888' };
    }

    const html = `${submission.correct_answers}/${submission.total_questions} (${percent}%)`;
    return { html, color };
}
async function viewClassSubmissions(classCode) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/teacher/class/${classCode}/submissions`, {
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });

        const result = await response.json();
        if (result.success) {
            const sectionDiv = document.getElementById('class-management-section');
            const submissionsDiv = document.getElementById('class-submissions');

            let html = `<h3>📊 Class Progress - ${escapeHtml(classCode)}</h3><table style="width: 100%; border-collapse: collapse;">
        <tr style="background: #333;">
          <th style="padding: 10px; border: 1px solid #555; text-align: left;">Student</th>
          <th style="padding: 10px; border: 1px solid #555;">Assignment</th>
          <th style="padding: 10px; border: 1px solid #555;">Completion %</th>
          <th style="padding: 10px; border: 1px solid #555;">Accuracy</th>
          <th style="padding: 10px; border: 1px solid #555;">Status</th>
          <th style="padding: 10px; border: 1px solid #555;">Submitted</th>
        </tr>`;

            result.data.forEach(sub => {
                const statusColor = sub.status === 'On Time' ? '#4ade80' : sub.status === 'Late' ? '#ff6b6b' : '#999';
                const accuracyDisplay = displayStudentAccuracy(sub);
                const currentStatus = sub.current_status || 'Not Started';
                const indicatorColor = currentStatus.includes('Stuck') ? '#ef4444' : currentStatus.includes('Completed') ? '#10b981' : '#3b82f6';
                html += `<tr style="border: 1px solid #555;">
          <td style="padding: 10px; border: 1px solid #555; position: relative;" class="student-name-cell">
            <span style="display: inline-flex; align-items: center; gap: 8px;">
              <span style="width: 8px; height: 8px; border-radius: 50%; background-color: ${indicatorColor}; display: inline-block;" title="${escapeHtml(currentStatus)}"></span>
              <strong>${escapeHtml(sub.email)}</strong>
            </span>
            <div class="hover-card" style="display: none; position: absolute; bottom: 100%; left: 0; background: var(--bg-card); border: 1px solid var(--border); border-radius: 6px; padding: 10px; box-shadow: var(--shadow-lg); z-index: 1000; width: 240px; font-size: 0.85em; pointer-events: none; color: var(--text-light); text-align: left;">
              <div style="font-weight: bold; color: var(--primary); margin-bottom: 4px;">Student Status:</div>
              <div>${escapeHtml(currentStatus)}</div>
            </div>
          </td>
          <td style="padding: 10px; border: 1px solid #555; font-size: 0.9em;">${escapeHtml(sub.assignment_title)}</td>
          <td style="padding: 10px; border: 1px solid #555;">
            <div style="background: #333; border-radius: 4px; overflow: hidden; height: 20px;">
              <div style="background: #667eea; width: ${sub.completion_percentage}%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 0.8em;">
                ${sub.completion_percentage}%
              </div>
            </div>
          </td>
          <td style="padding: 10px; border: 1px solid #555; font-weight: bold;">
            <span style="background: ${accuracyDisplay.color}; color: #fff; padding: 4px 8px; border-radius: 4px; display: inline-block; font-size: 0.9em;">
              ${accuracyDisplay.html}
            </span>
          </td>
          <td style="padding: 10px; border: 1px solid #555; color: ${statusColor}; font-weight: bold;">${escapeHtml(sub.status)}</td>
          <td style="padding: 10px; border: 1px solid #555;">${sub.is_submitted ? '✅ Yes' : '⏳ No'}</td>
        </tr>`;
            });

            html += '</table><button onclick="closeClassManagement()" class="secondary-btn" style="margin-top: 15px;">Back</button>';
            submissionsDiv.innerHTML = html;
            sectionDiv.style.display = 'block';
        }
    } catch (err) {
        console.error('Error:', err);
        alert('Error loading submissions');
    }
}

function closeClassManagement() {
    document.getElementById('class-management-section').style.display = 'none';
}

// Setup teacher/student listeners
function setupTeacherStudentListeners() {
    const becomeTeacherBtn = document.getElementById('become-teacher-btn');
    const enrollBtn = document.getElementById('enroll-class-btn');
    const createAssignmentBtn = document.getElementById('create-assignment-btn');
    const searchInput = document.getElementById('assignmentCourseSearch');

    if (becomeTeacherBtn) becomeTeacherBtn.addEventListener('click', becomeTeacher);
    if (enrollBtn) enrollBtn.addEventListener('click', enrollInClass);
    if (createAssignmentBtn) createAssignmentBtn.addEventListener('click', createAssignment);
    if (searchInput) {
        searchInput.addEventListener('input', window.debounce(searchAssignmentCourses, 300));
        // Also trigger on focus to ensure dropdown is populated
        searchInput.addEventListener('focus', () => {
            if (allCoursesForAssignment.length === 0) {
                populateAssignmentCourseDropdown();
            }
        });
    }

    // Update teacher/student UI when user loads
    if (currentUser) {
        // TEACHER: Show teacher panel, hide role management section
        if (currentUser.role === 'teacher') {
            document.getElementById('role-management-section').style.display = 'none';
            document.getElementById('teacher-panel').style.display = 'block';
            document.getElementById('student-enrollment').style.display = 'none';

            // Fetch and display class code from database
            fetchAndDisplayClassCode();
            loadTeacherClasses();
            loadUserCourses(); // Load courses for assignment dropdown
            populateAssignmentCourseDropdown(); // Populate course dropdown
        }
        // STUDENT/USER: Show enrollment, hide teacher panel
        else {
            document.getElementById('role-management-section').style.display = 'block';
            document.getElementById('teacher-panel').style.display = 'none';
            document.getElementById('student-enrollment').style.display = 'block';
            loadStudentAssignments();
        }
    }
}

// Fetch class code from database and display it
async function fetchAndDisplayClassCode() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/user/class-code`, {
            headers: { 'Authorization': `Bearer ${authToken}` },
            credentials: 'include'
        });

        const result = await response.json();
        if (result.success) {
            const classCodeSpan = document.getElementById('my-class-code');
            const statusDiv = document.getElementById('teacher-approval-status');

            if (classCodeSpan) {
                classCodeSpan.textContent = result.data.classCode;
                console.log('✔️ Class code displayed:', result.data.classCode);
            }

            // Update current user with fresh class code and approval status from server
            currentUser.class_code = result.data.classCode;
            currentUser.teacher_approved = result.data.approved;

            // Show approval status
            if (statusDiv) {
                if (result.data.approved) {
                    statusDiv.innerHTML = '<span style="color: #4ade80; font-weight: bold;">✅ Teacher approved! Students can join your class.</span>';
                } else {
                    statusDiv.innerHTML = '<span style="color: #ff9800; font-weight: bold;">⏳ Waiting for superadmin approval... Students cannot join yet.</span>';
                }
            }
        } else {
            console.log('ℹ️ Teacher approval pending');
            const classCodeSpan = document.getElementById('my-class-code');
            if (classCodeSpan) classCodeSpan.textContent = 'Pending superadmin approval...';
        }
    } catch (err) {
        console.error('Error fetching class code:', err);
    }
}

window.fetchAndDisplayClassCode = fetchAndDisplayClassCode;

// Export functions for onclick
window.submitAssignmentWork = submitAssignmentWork;
window.viewClassSubmissions = viewClassSubmissions;
window.closeClassManagement = closeClassManagement;
window.becomeTeacher = becomeTeacher;
window.enrollInClass = enrollInClass;
window.createAssignment = createAssignment;

// ===== GLOBAL SEARCH SYSTEM =====
document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('global-search-btn');
    const searchModal = document.getElementById('search-modal');
    const closeSearchBtn = document.getElementById('close-search-modal');
    const executeSearchBtn = document.getElementById('execute-search-btn');
    const searchInput = document.getElementById('global-search-input');

    if (searchBtn && searchModal && closeSearchBtn && executeSearchBtn && searchInput) {
        const openSearch = (e) => {
            if (e) e.preventDefault();
            searchModal.style.display = 'flex';
            searchModal.classList.add('is-open');
            searchModal.setAttribute('aria-hidden', 'false');
            const hint = document.getElementById('search-empty-hint');
            if (hint) hint.style.display = 'block';
            searchInput.focus();
        };
        const closeSearch = () => {
            searchModal.style.display = 'none';
            searchModal.classList.remove('is-open');
            searchModal.setAttribute('aria-hidden', 'true');
        };

        searchBtn.addEventListener('click', openSearch);
        closeSearchBtn.addEventListener('click', closeSearch);
        window.addEventListener('click', (e) => {
            if (e.target === searchModal) closeSearch();
        });
        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && searchModal.style.display === 'flex') closeSearch();
        });

        executeSearchBtn.addEventListener('click', performGlobalSearch);
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') performGlobalSearch();
        });
    }

    // Simulator sort buttons in search modal
    document.querySelectorAll('.sim-sort-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.sim-sort-btn').forEach(b => {
                b.classList.remove('active');
            });
            btn.classList.add('active');
            sortSearchSimulators(btn.dataset.sort);
        });
    });
});

let _cachedSearchSimulators = []; // cached for re-sorting without re-fetch

async function performGlobalSearch() {
    const searchInput = document.getElementById('global-search-input');
    const query = searchInput.value.trim();
    if (!query) {
        const hint = document.getElementById('search-empty-hint');
        if (hint) {
            hint.style.display = 'block';
            hint.textContent = 'Type a query and press Search or Enter.';
        }
        return;
    }

    const executeBtn = document.getElementById('execute-search-btn');
    const originalText = executeBtn.textContent;
    executeBtn.textContent = 'Searching...';
    executeBtn.disabled = true;

    const hint = document.getElementById('search-empty-hint');
    if (hint) hint.style.display = 'none';

    let courses = [];
    let simulators = [];

    try {
        const response = await fetch(`${API_BASE_URL}/api/search?q=${encodeURIComponent(query)}`, {
            headers: authToken ? { 'Authorization': `Bearer ${authToken}` } : {},
            credentials: 'include'
        });
        const result = await response.json();
        if (result.success) {
            courses = result.data.courses || [];
            simulators = result.data.simulators || [];
        }
    } catch (err) {
        console.warn('Search API failed, falling back to direct fetch:', err);
    }

    // Fallback: client-filter approved courses already loaded (incl. own units/masters)
    const localPool = (allApprovedCourses && allApprovedCourses.length)
        ? allApprovedCourses
        : availableCourses;
    if (courses.length === 0 && Array.isArray(localPool) && localPool.length) {
        const q = query.toLowerCase();
        courses = localPool.filter((c) =>
            (c.title || '').toLowerCase().includes(q) ||
            (c.description || '').toLowerCase().includes(q) ||
            (c.creator_email || '').toLowerCase().includes(q)
        );
    }

    if (simulators.length === 0) {
        try {
            const simRes = await fetch(`${API_BASE_URL}/api/simulators?limit=50&search=${encodeURIComponent(query)}`, {
                credentials: 'include'
            });
            const simData = await simRes.json();
            if (simData.success) {
                const allSims = simData.data?.simulators || (Array.isArray(simData.data) ? simData.data : []);
                const q = query.toLowerCase();
                simulators = allSims.filter(s =>
                    (s.title || '').toLowerCase().includes(q) ||
                    (s.description || '').toLowerCase().includes(q) ||
                    (s.tags || '').toLowerCase().includes(q)
                );
            }
        } catch (err2) {
            console.warn('Simulator fetch failed:', err2);
        }
    }

    _cachedSearchSimulators = simulators;
    renderSearchResults(courses, simulators);

    executeBtn.textContent = originalText;
    executeBtn.disabled = false;
}

function sortSearchSimulators(sortBy) {
    const sorted = [..._cachedSearchSimulators];
    switch (sortBy) {
        case 'most_liked':
            sorted.sort((a, b) => (b.like_count || b.likes || b.rating || 0) - (a.like_count || a.likes || a.rating || 0));
            break;
        case 'most_viewed':
            sorted.sort((a, b) => (b.downloads || b.download_count || b.views || 0) - (a.downloads || a.download_count || a.views || 0));
            break;
        case 'newest':
            sorted.sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0));
            break;
        case 'relevance':
        default:
            break;
    }
    renderSimulatorSearchList(sorted);
}

function renderSearchCourseCard(c, kind) {
    const grade = c.grade_level
        ? (c.grade_level === 13 ? 'College' : `Grade ${c.grade_level}`)
        : '';
    const badge =
        kind === 'master'
            ? '<span class="search-result-badge">Master</span>'
            : '<span class="search-result-badge unit-badge">Unit / Single</span>';
    const gradeBadge = grade ? `<span class="search-result-badge">${escapeHtml(grade)}</span>` : '';
    return `
        <div class="search-result-card ${kind}" onclick="viewCourseFromSearch(${c.id})" role="button" tabindex="0">
            <strong>${escapeHtml(c.title)}</strong>
            ${badge}${gradeBadge}
            <p>${escapeHtml(c.description || 'No description available.')}</p>
            <small>By ${escapeHtml(c.creator_email || 'Unknown')}${c.units_count ? ` · ${c.units_count} units` : ''}</small>
        </div>
    `;
}

function renderSearchResults(courses, simulators) {
    const coursesHeader = document.getElementById('search-courses-header');
    const coursesList = document.getElementById('search-courses-list');
    const simulatorsSection = document.getElementById('search-simulators-section');
    const hint = document.getElementById('search-empty-hint');
    if (hint) hint.style.display = 'none';

    const list = Array.isArray(courses) ? courses : [];
    const masterCourses = list.filter((c) => c.course_type === 'master');
    const singleCourses = list.filter((c) => c.course_type !== 'master');

    coursesHeader.style.display = 'block';
    let html = '';
    if (masterCourses.length > 0) {
        html += '<h4 class="search-section-title" style="font-size:0.95rem;border:none;margin:4px 0;">Master Courses</h4>';
        html += masterCourses.map((c) => renderSearchCourseCard(c, 'master')).join('');
    }
    if (singleCourses.length > 0) {
        html += '<h4 class="search-section-title" style="font-size:0.95rem;border:none;margin:12px 0 4px;">Units / Single Courses</h4>';
        html += singleCourses.map((c) => renderSearchCourseCard(c, 'unit')).join('');
    }
    if (!masterCourses.length && !singleCourses.length) {
        html = '<p class="search-empty-msg">No courses or units found for this query.</p>';
    }
    coursesList.innerHTML = html;

    if (simulators && simulators.length > 0) {
        simulatorsSection.style.display = 'block';
        renderSimulatorSearchList(simulators);
        document.querySelectorAll('.sim-sort-btn').forEach((btn) => {
            btn.classList.toggle('active', btn.dataset.sort === 'relevance');
        });
    } else {
        simulatorsSection.style.display = 'block';
        document.getElementById('search-simulators-list').innerHTML =
            '<p class="search-empty-msg">No simulators found for this query.</p>';
    }
}

function renderSimulatorSearchList(simulators) {
    const simulatorsList = document.getElementById('search-simulators-list');
    if (!simulators || simulators.length === 0) {
        simulatorsList.innerHTML = '<p class="search-empty-msg">No simulators found.</p>';
        return;
    }
    simulatorsList.innerHTML = simulators.map((s) => {
        const likes = s.like_count || s.likes || s.rating || 0;
        const views = s.downloads || s.download_count || s.views || 0;
        const viewUrl = s.url || `simulator-view.html?id=${s.id}`;
        return `
            <div class="search-result-card unit" onclick="window.open('${escapeHtml(viewUrl)}', '_blank')" role="button" tabindex="0">
                <strong>${escapeHtml(s.title)}</strong>
                <p>${escapeHtml(s.description || 'No description available.')}</p>
                <small>❤️ ${likes} · 👁 ${views} · By ${escapeHtml(s.creator_email || s.creator || 'Unknown')}</small>
            </div>
        `;
    }).join('');
}

function viewCourseFromSearch(courseId) {
    const modal = document.getElementById('search-modal');
    if (modal) {
        modal.style.display = 'none';
        modal.classList.remove('is-open');
        modal.setAttribute('aria-hidden', 'true');
    }

    if (typeof viewCourse === 'function') {
        viewCourse(courseId);
    } else {
        console.error('viewCourse is not available in this context.');
    }
}

// ===== COURSE LIKES FUNCTIONALITY =====

/**
 * Hide site navbar and apply the learner store theme while viewing a course.
 */
function enterCourseViewerMode(courseId) {
    document.body.classList.add("course-viewer-active");
    const profile = window.LearnerGamification?.getProfile?.();
    const shell = document.getElementById("learner-shell");
    const theme =
        shell?.getAttribute("data-learner-theme") ||
        profile?.dashboardTheme ||
        localStorage.getItem("learnerDashboardTheme") ||
        "warm";
    document.body.setAttribute("data-learner-theme", theme);
    requestAnimationFrame(() => {
        const bg = getComputedStyle(document.body).getPropertyValue("--ls-bg").trim();
        if (bg) document.body.style.background = bg;
    });
    if (courseId != null) syncViewerLikeButton(courseId);
}

function exitCourseViewerMode() {
    document.body.classList.remove("course-viewer-active");
    // Keep data-learner-theme on shell; clear body attr used only for viewer
    if (!document.body.classList.contains("learner-shell-active")) {
        document.body.removeAttribute("data-learner-theme");
    }
}

/**
 * Wire / refresh the like button in the course viewer header.
 */
async function syncViewerLikeButton(courseId) {
    const btn = document.getElementById("viewer-like-btn");
    if (!btn || courseId == null) return;

    btn.dataset.courseId = String(courseId);
    btn.onclick = () => toggleCourseLike(courseId, btn);

    const course =
        myCourses.find((c) => c.id === courseId) ||
        availableCourses.find((c) => c.id === courseId) ||
        pendingCourses.find((c) => c.id === courseId);

    let liked = !!(course && (course.is_liked || course.liked));
    let count = course?.like_count ?? course?.likes ?? null;

    const token = localStorage.getItem("token") || authToken;
    try {
        const headers = token ? { Authorization: `Bearer ${token}` } : {};
        const [countRes, likedRes] = await Promise.all([
            fetch(`${API_BASE_URL}/api/courses/${courseId}/likes`, { headers, credentials: "include" }),
            fetch(`${API_BASE_URL}/api/courses/${courseId}/liked`, { headers, credentials: "include" })
        ]);
        const countData = await countRes.json().catch(() => ({}));
        const likedData = await likedRes.json().catch(() => ({}));
        if (countData?.success && countData.data && typeof countData.data.like_count === "number") {
            count = countData.data.like_count;
        }
        if (likedData?.success && likedData.data) {
            if (typeof likedData.data.liked === "boolean") liked = likedData.data.liked;
            else if (typeof likedData.data.is_liked === "boolean") liked = likedData.data.is_liked;
        }
    } catch (e) {
        /* keep local fallbacks */
    }

    btn.dataset.liked = liked ? "true" : "false";
    btn.classList.toggle("course-action-like-active", liked);
    btn.classList.toggle("course-action-like", !liked);
    const labelCount = typeof count === "number" ? count : "";
    btn.textContent = liked
        ? `❤️ ${labelCount !== "" ? labelCount : "Liked"}`
        : `🤍 ${labelCount !== "" ? labelCount : "Like"}`;
}

/**
 * Toggle like/unlike a course
 */
async function toggleCourseLike(courseId, buttonElement) {
    try {
        const currentlyLiked = buttonElement.dataset.liked === 'true';
        const endpoint = `/api/courses/${courseId}/like`;
        const method = currentlyLiked ? 'DELETE' : 'POST';

        const token = localStorage.getItem('token');
        if (!token) {
            alert('Please log in to like courses');
            return;
        }

        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: method,
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            credentials: 'include'
        });

        const result = await response.json();

        if (!response.ok) {
            console.error('Like toggle error:', result.message);
            alert('Error: ' + result.message);
            return;
        }

        // Update the button state
        const isNowLiked = result.data.liked;
        buttonElement.dataset.liked = isNowLiked;

        // Get updated like count
        const likeCountResponse = await fetch(`${API_BASE_URL}/api/courses/${courseId}/likes`, {
            headers: {
                'Authorization': `Bearer ${token}`
            },
            credentials: 'include'
        });
        const likeCountResult = await likeCountResponse.json();
        const newLikeCount = likeCountResult.data.like_count;

        // Update button appearance
        const likeButtonText = isNowLiked ? `❤️ ${newLikeCount}` : `🤍 ${newLikeCount}`;
        buttonElement.textContent = likeButtonText;
        buttonElement.dataset.liked = isNowLiked ? "true" : "false";
        buttonElement.classList.toggle("course-action-like-active", isNowLiked);
        buttonElement.classList.toggle("course-action-like", !isNowLiked);
        if (!buttonElement.id || buttonElement.id !== "viewer-like-btn") {
            buttonElement.style.background = isNowLiked ? '#ec4899' : '#475569';
        }

        // Keep viewer header button in sync when liking from a list card
        const viewerBtn = document.getElementById("viewer-like-btn");
        if (viewerBtn && String(viewerBtn.dataset.courseId) === String(courseId) && viewerBtn !== buttonElement) {
            viewerBtn.dataset.liked = isNowLiked ? "true" : "false";
            viewerBtn.classList.toggle("course-action-like-active", isNowLiked);
            viewerBtn.classList.toggle("course-action-like", !isNowLiked);
            viewerBtn.textContent = likeButtonText;
        }

        // Update course data in arrays
        const courseInAvailable = availableCourses.find(c => c.id === courseId);
        if (courseInAvailable) {
            courseInAvailable.is_liked = isNowLiked;
            courseInAvailable.like_count = newLikeCount;
        }

        const courseInMy = myCourses.find(c => c.id === courseId);
        if (courseInMy) {
            courseInMy.like_count = newLikeCount;
        }

        if (window.logger) window.logger.debug(`✓ Course ${courseId} ${isNowLiked ? 'liked' : 'unliked'} successfully!`);
    } catch (error) {
        console.error('Error toggling course like:', error);
        alert('Failed to update like status. Please try again.');
    }
}

/**
 * Load courses with sorting applied
 */
function loadCoursesWithSort(sortBy = 'newest') {
    // Sort available courses locally (no API call needed — avoids 401 errors)
    const sorter = (a, b) => {
        switch (sortBy) {
            case 'most_liked':
                return (b.like_count || 0) - (a.like_count || 0);
            case 'trending':
                return ((b.like_count || 0) + (b.view_count || 0)) - ((a.like_count || 0) + (a.view_count || 0));
            case 'popular':
                return (b.view_count || 0) - (a.view_count || 0);
            case 'newest':
            default:
                return new Date(b.created_at || 0) - new Date(a.created_at || 0);
        }
    };
    availableCourses = [...availableCourses].sort(sorter);
    if (allApprovedCourses.length) {
        allApprovedCourses = [...allApprovedCourses].sort(sorter);
    }

    const searchBox = document.getElementById('availableCoursesSearch');
    renderAvailableCourses(searchBox ? searchBox.value : '');
    if (window.logger) window.logger.debug(`✓ Courses sorted locally by: ${sortBy}`);
}

/**
 * Initialize course sort dropdown listener
 */
function setupCourseSortListener() {
    const sortDropdown = document.getElementById('courseSortDropdown');
    if (sortDropdown) {
        sortDropdown.addEventListener('change', (e) => {
            const sortBy = e.target.value;
            loadCoursesWithSort(sortBy);
        });
    }
}

// Global active student status update helper
async function updateStudentActiveStatus(status) {
    if (!authToken || !currentUser || currentUser.role !== 'student') return;
    
    const activeAssignmentId = localStorage.getItem('activeAssignmentId') || window.currentAssignmentId;
    if (!activeAssignmentId) return;

    try {
        // Send via HTTP POST
        fetch(`${API_BASE_URL}/api/student/update-status`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                assignmentId: parseInt(activeAssignmentId),
                status: status
            })
        });

        // Send via WebSocket if connected
        if (window.ws && window.ws.readyState === WebSocket.OPEN) {
            window.ws.send(JSON.stringify({
                type: 'update_status',
                assignmentId: parseInt(activeAssignmentId),
                status: status
            }));
        }
    } catch (e) {
        console.warn('Failed to update student active status:', e);
    }
}
window.updateStudentActiveStatus = updateStudentActiveStatus;

// Expose for learner shell / gamification modules
window.API_BASE_URL = API_BASE_URL;
window.createNewCourse = createNewCourse;
window.viewCourse = viewCourse;
window.logout = logout;
window.saveCourse = saveCourse;
window.editCourse = editCourse;
window.renderCurrentPage = renderCurrentPage;
window.saveCurrentPageContent = saveCurrentPageContent;
window.changePage = changePage;
window.updatePageControls = updatePageControls;
window.cancelPlacementMode = cancelPlacementMode;
window.normalizeAbsoluteEmbeds = normalizeAbsoluteEmbeds;
Object.defineProperty(window, 'currentPageIndex', {
    get() { return currentPageIndex; },
    set(v) { currentPageIndex = v; },
    configurable: true
});
Object.defineProperty(window, 'isPlacementMode', {
    get() { return isPlacementMode; },
    configurable: true
});
window.__veelearnPushCourse = function (course) {
    if (!course || !course.id) return;
    if (!myCourses.some((c) => c.id === course.id)) myCourses.push(course);
    if (!availableCourses.some((c) => c.id === course.id)) availableCourses.push(course);
};
