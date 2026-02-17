// ===== GLOBAL STATE =====
// Determine API base URL based on environment
const API_BASE_URL = (() => {
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
let authToken = null; // No longer stored in localStorage for security
let myCourses = [];
let coursePages = [""]; // Array to store content for each page
let currentPageIndex = 0;
let isPlacementMode = false; // Flag for cursor-based placement
let placementType = null; // 'visual-simulator', 'block-simulator', 'quiz'
let placementData = null; // Data to pass to insertion function
let availableCourses = [];
let allUsers = [];
let courseQuestions = [];
let pendingCourses = [];
let currentEditingQuestionId = null;
let lastDeletedQuestion = null; // Store last deleted question for undo
let savedSelection = null; // Save cursor position when editor loses focus

let courseTimerInterval = null;
let courseActiveSeconds = 0;
let lastActivityTime = Date.now();
let isTimerActive = false;
let keyPressLog = [];
let lastKeyPressed = null;
let sameKeyCount = 0;
let macroDetected = false;

// Global keyboard listener for Ctrl+Z undo
document.addEventListener('keydown', async (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'z' && lastDeletedQuestion) {
        e.preventDefault();
        console.log('↩️ Ctrl+Z pressed - Undoing quiz deletion');

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


// ===== INITIALIZATION =====
console.log("🚀 Veelearn Script v3 Loaded");

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

    // Create awesome wave transition
    createWaveTransition();
    createWaveBars();

    // Show new section with entrance animation
    setTimeout(() => {
        if (fromSection) fromSection.style.display = 'none';
        if (fromSection) fromSection.classList.remove('page-transition-out');

        toSection.style.display = 'block';
        toSection.classList.add('transition-in-active');

        // Stagger animate child sections
        setTimeout(() => {
            const sections = toSection.querySelectorAll('section');
            sections.forEach((section, index) => {
                section.style.animation = `contentFadeInScale 0.7s cubic-bezier(0.34, 1.56, 0.64, 1) ${index * 0.1}s forwards`;
                section.style.opacity = '0';
            });
        }, 100);

        // Remove animation class after it finishes
        setTimeout(() => {
            toSection.classList.remove('transition-in-active');
        }, 800);
    }, 400);
}

function initializeApp() {
    console.log("Initializing App...");
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

    if (document.cookie.includes('token=') || authToken) {
        fetchUserProfile();
    } else {
        showLandingPage();
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

function setupMessageListeners() {
    window.addEventListener("message", (e) => {
        if (e.data.type === "closeBlockSimulator") {
            showDashboard();
        } else if (e.data.type === "save-simulator") {
            // Receive simulator data from popup (block-simulator.html sends this)
            const { data } = e.data;
            console.log('💾 Received save-simulator message');
            console.log('   blocks:', data?.blocks?.length, 'connections:', data?.connections?.length);
            console.log('   currentEditingSimulatorBlockId:', currentEditingSimulatorBlockId);

            // Use the stored currentEditingSimulatorBlockId
            if (currentEditingSimulatorBlockId && data) {
                const blockIndex = courseBlocks.findIndex(b => b.id === currentEditingSimulatorBlockId);
                if (blockIndex !== -1) {
                    courseBlocks[blockIndex].data = {
                        blocks: data.blocks || [],
                        connections: data.connections || []
                    };
                    console.log('✅ Saved to block:', currentEditingSimulatorBlockId, 'at index:', blockIndex);
                } else {
                    console.warn('⚠️ Block not found:', currentEditingSimulatorBlockId);
                }
            }
        } else if (e.data.type === "saveBlockSimulator") {
            // Legacy support - receive simulator data
            const { courseBlockId, blocks, connections } = e.data;
            console.log('💾 Saving simulator data:', courseBlockId, 'Blocks:', blocks?.length, 'Connections:', connections?.length);

            const blockIndex = courseBlocks.findIndex(b => b.id === courseBlockId);
            if (blockIndex !== -1) {
                courseBlocks[blockIndex].data = {
                    blocks: blocks || [],
                    connections: connections || []
                };
                console.log('✅ Simulator data saved to courseBlocks[' + blockIndex + ']');
            } else {
                console.warn('⚠️ Block not found:', courseBlockId);
            }
        } else if (e.data.type === "saveVisualSimulator") {
            // Receive visual simulator code
            const { courseBlockId, code, variables } = e.data;
            console.log('💾 Saving visual simulator:', courseBlockId);

            const blockIndex = courseBlocks.findIndex(b => b.id === courseBlockId);
            if (blockIndex !== -1) {
                courseBlocks[blockIndex].data = {
                    code: code || "",
                    variables: variables || {}
                };
                console.log('✅ Visual simulator saved');
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

    fetch(`${API_BASE_URL}/api/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
        credentials: "include"
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                authToken = data.data.token;
                // localStorage.setItem("token", authToken); // DISABLED FOR SECURITY
                // Backend returns: {token, user: {id, email, role, shells}}
                const userData = data.data.user || data.data;
                currentUser = {
                    id: userData.id,
                    email: userData.email,
                    role: userData.role,
                    shells: userData.shells || 0
                };
                console.log("Login successful, currentUser set:", currentUser);
                // INSTANT: Show dashboard immediately without needing a reload
                showDashboard();
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
                }, 0);
            } else {
                errorMessage.textContent = data.message || "Login failed";
            }
        })
        .catch((err) => {
            console.error("Login error:", err);
            errorMessage.textContent =
                "Connection error. Is the backend API running?";
        });
}

function handleRegister() {
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;
    const errorMsg = document.getElementById("register-error-message");

    if (!email || !password) {
        errorMsg.textContent = "All fields required";
        return;
    }

    fetch(`${API_BASE_URL}/api/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
        credentials: "include"
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                alert("Registration successful! Please login.");
                document.getElementById("show-login").click();
            } else {
                errorMsg.textContent = data.message || "Registration failed";
            }
        })
        .catch((err) => {
            console.error("Register error:", err);
            errorMsg.textContent = "Connection error";
        });
}

function fetchUserProfile() {
    if (!authToken) return;

    fetch(`${API_BASE_URL}/api/users/profile`, {
        headers: { Authorization: `Bearer ${authToken}` },
        credentials: "include"
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                currentUser = data.data;
                showDashboard();
                // NOW setup teacher/student UI after currentUser is loaded
                setupTeacherStudentListeners();
            } else {
                logout();
            }
        })
        .catch((err) => {
            console.error("Profile fetch error:", err);
            logout();
        });
}

function handleLogout() {
    logout();
}

function logout() {
    console.log("LOGOUT CALLED - Token will be cleared!");

    // Call backend logout to clear cookie
    fetch(`${API_BASE_URL}/api/logout`, { method: 'POST', credentials: 'include' })
        .catch(err => console.warn('Logout API error:', err));

    authToken = null;
    currentUser = null;
    // localStorage.removeItem("token"); // DISABLED
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

        console.log("✅ Token is valid, expires at:", new Date(expiryTime).toISOString());
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

// ===== COURSE CREATION TIMER (ANTI-CHEAT) =====

function formatTimerDisplay(totalSeconds) {
    const h = Math.floor(totalSeconds / 3600);
    const m = Math.floor((totalSeconds % 3600) / 60);
    const s = totalSeconds % 60;
    return String(h).padStart(2, '0') + ':' + String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
}

function updateTimerUI() {
    const valueEl = document.getElementById('course-timer-value');
    const statusEl = document.getElementById('course-timer-status');
    if (valueEl) valueEl.textContent = formatTimerDisplay(courseActiveSeconds);
    if (statusEl) {
        if (macroDetected) {
            statusEl.textContent = '(paused - suspicious input)';
            statusEl.style.color = '#ef4444';
        } else if (Date.now() - lastActivityTime >= 60000) {
            statusEl.textContent = '(idle - paused)';
            statusEl.style.color = '#f59e0b';
        } else {
            statusEl.textContent = '(tracking...)';
            statusEl.style.color = '#999';
        }
    }
}

function startCourseTimer() {
    if (courseTimerInterval) clearInterval(courseTimerInterval);
    isTimerActive = true;
    lastActivityTime = Date.now();
    macroDetected = false;
    keyPressLog = [];
    lastKeyPressed = null;
    sameKeyCount = 0;
    updateTimerUI();

    courseTimerInterval = setInterval(() => {
        const idleMs = Date.now() - lastActivityTime;
        if (idleMs < 60000 && !macroDetected) {
            courseActiveSeconds++;
        }
        updateTimerUI();
    }, 1000);
}

function stopCourseTimer() {
    if (courseTimerInterval) {
        clearInterval(courseTimerInterval);
        courseTimerInterval = null;
    }
    isTimerActive = false;
    return courseActiveSeconds;
}

function resetCourseTimer() {
    stopCourseTimer();
    courseActiveSeconds = 0;
    lastActivityTime = Date.now();
    macroDetected = false;
    keyPressLog = [];
    lastKeyPressed = null;
    sameKeyCount = 0;
    updateTimerUI();
}

function handleTimerActivity(event) {
    lastActivityTime = Date.now();

    if (event.type === 'keydown') {
        const now = Date.now();
        keyPressLog.push(now);
        if (keyPressLog.length > 200) keyPressLog.shift();

        if (event.key === lastKeyPressed) {
            sameKeyCount++;
            if (sameKeyCount >= 50) {
                macroDetected = true;
                return;
            }
        } else {
            lastKeyPressed = event.key;
            sameKeyCount = 1;
        }

        const fiveSecondsAgo = now - 5000;
        const recentKeys = keyPressLog.filter(t => t >= fiveSecondsAgo);
        if (recentKeys.length > 100) {
            macroDetected = true;
            return;
        }

        if (macroDetected && recentKeys.length <= 100 && sameKeyCount < 50) {
            macroDetected = false;
        }
    } else {
        if (macroDetected && sameKeyCount < 50) {
            const now = Date.now();
            const fiveSecondsAgo = now - 5000;
            const recentKeys = keyPressLog.filter(t => t >= fiveSecondsAgo);
            if (recentKeys.length <= 100) {
                macroDetected = false;
            }
        }
    }
}

function attachTimerActivityListeners() {
    const editor = document.getElementById('course-content-editor');
    const titleInput = document.getElementById('course-title');
    const descInput = document.getElementById('course-description');
    const editorSection = document.getElementById('course-editor-section');

    const targets = [editor, titleInput, descInput, editorSection].filter(Boolean);
    const events = ['mousemove', 'keydown', 'click', 'scroll'];

    targets.forEach(target => {
        events.forEach(evt => {
            target.addEventListener(evt, handleTimerActivity, { passive: true });
        });
    });
}

function formatCreationTime(seconds) {
    if (!seconds || seconds <= 0) return '';
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    if (h > 0) return h + 'h ' + m + 'm';
    return m + 'm';
}

// ===== COURSE EDITOR LISTENERS =====
function setupCourseEditorListeners() {
    console.log("Setting up course editor listeners...");
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
        console.log("Add Page button found, attaching listener");
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
            console.log("📝 Save Draft button clicked - action: draft");
            saveCourse("draft");
        });
    }

    // Submit for approval button - DIRECTLY call saveCourse with "pending" action
    if (submitApprovalBtn) {
        submitApprovalBtn.addEventListener("click", (e) => {
            e.preventDefault();
            console.log("📋 Submit for Approval button clicked - action: pending");
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

    attachTimerActivityListeners();
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
    <div style="background: white; padding: 25px; border-radius: 8px; max-width: 700px; width: 90%; max-height: 90vh; overflow-y: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
      <h2 style="margin: 0 0 15px 0; color: #333;">Insert LaTeX Equation</h2>
      
      <div style="margin-bottom: 20px;">
        <label style="display: block; margin-bottom: 8px; font-weight: 500;">Equation Type:</label>
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
      
      <div style="margin-bottom: 20px;">
        <label style="display: block; margin-bottom: 8px; font-weight: 500;">LaTeX Code:</label>
        <textarea id="latex-input" placeholder="Enter your LaTeX equation here&#10;&#10;Examples:&#10;E = mc^2&#10;\\frac{a}{b}&#10;\\sum_{i=1}^{n} x_i&#10;x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}" 
          style="width: 100%; height: 150px; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-family: monospace; font-size: 14px; resize: vertical;"></textarea>
      </div>
      
      <div style="margin-bottom: 20px; padding: 15px; background: #f9f9f9; border-radius: 4px; border-left: 4px solid #667eea;">
        <strong style="display: block; margin-bottom: 10px;">Preview:</strong>
        <div id="latex-preview" style="padding: 10px; background: white; border-radius: 4px; min-height: 40px; font-size: 16px;">
          (preview will appear here)
        </div>
      </div>
      
      <div style="margin-bottom: 20px;">
        <strong style="display: block; margin-bottom: 10px;">Common Symbols:</strong>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 8px;">
          <button type="button" onclick="insertLatexSnippet('\\alpha')" class="latex-snippet-btn">α (alpha)</button>
          <button type="button" onclick="insertLatexSnippet('\\beta')" class="latex-snippet-btn">β (beta)</button>
          <button type="button" onclick="insertLatexSnippet('\\gamma')" class="latex-snippet-btn">γ (gamma)</button>
          <button type="button" onclick="insertLatexSnippet('\\Delta')" class="latex-snippet-btn">Δ (Delta)</button>
          <button type="button" onclick="insertLatexSnippet('\\frac{a}{b}')" class="latex-snippet-btn">a/b (fraction)</button>
          <button type="button" onclick="insertLatexSnippet('\\sqrt{x}')" class="latex-snippet-btn">√x (sqrt)</button>
          <button type="button" onclick="insertLatexSnippet('^{2}')" class="latex-snippet-btn">x² (power)</button>
          <button type="button" onclick="insertLatexSnippet('_{i}')" class="latex-snippet-btn">xᵢ (subscript)</button>
          <button type="button" onclick="insertLatexSnippet('\\sum_{i=1}^{n}')" class="latex-snippet-btn">Σ (sum)</button>
          <button type="button" onclick="insertLatexSnippet('\\int_a^b')" class="latex-snippet-btn">∫ (integral)</button>
          <button type="button" onclick="insertLatexSnippet('\\pm')" class="latex-snippet-btn">± (plus-minus)</button>
          <button type="button" onclick="insertLatexSnippet('\\times')" class="latex-snippet-btn">× (times)</button>
        </div>
      </div>
      
      <div style="margin-bottom: 20px;">
        <strong style="display: block; margin-bottom: 10px;">Common Equations:</strong>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 8px;">
          <button type="button" onclick="insertLatexSnippet('E = mc^2')" class="latex-template-btn">E = mc²</button>
          <button type="button" onclick="insertLatexSnippet('x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}')" class="latex-template-btn">Quadratic formula</button>
          <button type="button" onclick="insertLatexSnippet('\\lambda = \\frac{h}{p}')" class="latex-template-btn">de Broglie wavelength</button>
          <button type="button" onclick="insertLatexSnippet('\\Delta x \\cdot \\Delta p \\geq \\frac{h}{4\\pi}')" class="latex-template-btn">Uncertainty principle</button>
          <button type="button" onclick="insertLatexSnippet('\\int_0^\\infty e^{-x} dx = 1')" class="latex-template-btn">Integral example</button>
          <button type="button" onclick="insertLatexSnippet('F = ma')" class="latex-template-btn">Newton's 2nd law</button>
        </div>
      </div>
      
      <div style="display: flex; gap: 10px; justify-content: flex-end;">
        <button type="button" onclick="closeLatexEditorModal()" style="padding: 10px 20px; background: #999; color: white; border: none; border-radius: 4px; cursor: pointer;">Cancel</button>
        <button type="button" onclick="confirmLatexInsertion()" style="padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer;">Insert Equation</button>
      </div>
    </div>
  `;

    document.body.appendChild(modal);

    // Add event listeners for preview
    const input = document.getElementById('latex-input');
    const previewDiv = document.getElementById('latex-preview');
    const typeRadios = document.querySelectorAll('input[name="latex-type"]');

    input.addEventListener('input', updateLatexPreview);
    typeRadios.forEach(radio => radio.addEventListener('change', updateLatexPreview));

    input.focus();
}

function updateLatexPreview() {
    const input = document.getElementById('latex-input');
    const preview = document.getElementById('latex-preview');
    const type = document.querySelector('input[name="latex-type"]:checked').value;

    if (!input.value.trim()) {
        preview.innerHTML = '(preview will appear here)';
        return;
    }

    let latex = input.value.trim();
    if (type === 'display') {
        latex = '$$' + latex + '$$';
    } else {
        latex = '$' + latex + '$';
    }

    preview.innerHTML = latex;

    // Trigger MathJax to render preview
    if (window.MathJax) {
        window.MathJax.typesetPromise([preview]).catch(err => console.log('MathJax error:', err));
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

                // Move cursor after the equation
                range.setStartAfter(span);
                range.collapse(true);
                selection.removeAllRanges();
                selection.addRange(range);

                // Trigger MathJax to re-render
                if (window.MathJax && window.MathJax.typesetPromise) {
                    setTimeout(() => {
                        window.MathJax.typesetPromise([contentEditor]).catch(err => console.log('MathJax error:', err));
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
            window.MathJax.typesetPromise([contentEditor]).catch(err => console.log('MathJax error:', err));
        }, 100);
    }
}

// Process LaTeX in text - convert $...$ to rendered equations
// Preserves already-processed equations
function processLatexInEditor() {
    const contentEditor = document.getElementById('course-content-editor');
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
        setTimeout(() => {
            window.MathJax.typesetPromise([contentEditor]).catch(err => console.log('MathJax error:', err));
        }, 50);
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

function addBlockSimulator() {
    const blockId = Date.now();
    courseBlocks.push({
        id: blockId,
        type: "block-simulator",
        title: "Block-based Logic Simulator",
        data: { blocks: [], connections: [] },
    });

    // Start placement mode instead of direct insertion
    startPlacementMode('block-simulator', {
        id: blockId,
        title: "Block-based Logic",
        type: "Block-based Simulator"
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

    document.getElementById("simulator-link").style.display = "none";
    document.getElementById("marketplace-link").style.display = "none";
    document.getElementById("creator-link").style.display = "none";
    document.getElementById("dashboard-link").style.display = "none";
    document.getElementById("logout-button").style.display = "none";

    document.getElementById("login-link").style.display = "inline";
    document.getElementById("register-link").style.display = "inline";

    if (type === "register") {
        document.getElementById("login-form").style.display = "none";
        document.getElementById("register-form").style.display = "block";
        document.getElementById("forgot-password-form").style.display = "none";
    } else {
        document.getElementById("login-form").style.display = "block";
        document.getElementById("register-form").style.display = "none";
        document.getElementById("forgot-password-form").style.display = "none";
    }
}

function showDashboard() {
    stopCourseTimer();

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

    document.getElementById("simulator-link").style.display = "inline";
    document.getElementById("marketplace-link").style.display = "inline";
    document.getElementById("creator-link").style.display = "inline";
    document.getElementById("dashboard-link").style.display = "inline";
    document.getElementById("logout-button").style.display = "inline";

    document.getElementById("login-link").style.display = "none";
    document.getElementById("register-link").style.display = "none";

    document.getElementById("user-email").textContent =
        currentUser?.email || "User";

    // INSTANT: Show dashboard content immediately
    if (currentUser?.role === "superadmin") {
        showSuperadminDashboard();
    } else if (currentUser?.role === "admin") {
        showAdminDashboard();
    } else {
        showUserDashboard();
    }

    // INSTANT: Load all data asynchronously in background without blocking UI
    setTimeout(() => {
        loadVolunteerStats();
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
            <p>Role: ${escapeHtml(user.role)} ${user.class_code ? `| Class Code: ${escapeHtml(user.class_code)}` : ''} | ${user.teacher_approved ? '✅ Approved' : user.role === 'teacher' ? '⏳ Pending Approval' : ''} | Shells: ${user.shells} | Volunteer: ${(user.total_volunteer_hours || 0).toFixed(1)}h ${user.is_verified_creator ? '✅' : ''}</p>
            ${approveBtn}
            <button onclick="changeUserRole('${escapeHtml(user.email)}', 'admin')">Make Admin</button>
            <button onclick="changeUserRole('${escapeHtml(user.email)}', 'teacher')">Make Teacher</button>
            <button onclick="changeUserRole('${escapeHtml(user.email)}', 'user')">Make User</button>
            <button onclick="grantVolunteerHours(${user.id}, '${escapeHtml(user.email)}')" style="background: #4ade80; color: #000;">Grant Hours</button>
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
    console.log("=== LOADING USER COURSES ===");
    fetch(`${API_BASE_URL}/api/courses`, {
        headers: { Authorization: `Bearer ${authToken}` },
        credentials: "include"
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                const allCoursesFromServer = data.data || [];
                console.log("Total courses from API:", allCoursesFromServer.length);
                console.log("Current user ID:", currentUser.id);

                myCourses = allCoursesFromServer.filter(
                    (c) => c.creator_id === currentUser.id
                );
                console.log("Filtered user courses:", myCourses.length);
                // Clear search box
                const myCoursesSearch = document.getElementById('myCoursesSearch');
                if (myCoursesSearch) myCoursesSearch.value = '';
                renderUserCourses();

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
        .catch((err) => console.error("Error loading user courses:", err));
}

function loadAvailableCourses() {
    console.log("=== LOADING AVAILABLE COURSES ===");
    fetch(`${API_BASE_URL}/api/courses`, {
        headers: { Authorization: `Bearer ${authToken}` },
        credentials: "include"
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                const allCoursesFromServer = data.data || [];
                console.log("Total courses from API:", allCoursesFromServer.length);
                console.log(
                    "Course statuses:",
                    allCoursesFromServer.map((c) => ({
                        id: c.id,
                        title: c.title,
                        status: c.status,
                        creator_id: c.user_id,
                        currentUserId: currentUser.id,
                    }))
                );

                availableCourses = allCoursesFromServer.filter(
                    (c) => c.status === "approved" && c.creator_id !== currentUser.id
                );
                console.log("Filtered available courses:", availableCourses.length);
                // Clear search box
                const availableCoursesSearch = document.getElementById('availableCoursesSearch');
                if (availableCoursesSearch) availableCoursesSearch.value = '';
                renderAvailableCourses();
            }
        })
        .catch((err) => console.error("Error loading available courses:", err));
}



function filterCourseList(courseArray, searchText) {
    if (!searchText || searchText.trim() === "") {
        return courseArray;
    }

    const search = searchText.toLowerCase();
    return courseArray.filter((course) => {
        const titleMatch = course.title.toLowerCase().includes(search);
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

    // Filter courses based on search text
    const filteredCourses = filterCourseList(myCourses, searchText);

    lists.forEach((list) => {
        if (!list) return;

        // INSTANT: Clear existing list to prevent duplicates
        list.innerHTML = "";

        if (myCourses.length === 0) {
            list.innerHTML = "<li><em>No courses yet</em></li>";
            return;
        }

        if (filteredCourses.length === 0) {
            list.innerHTML = `<li><em>No courses found matching "${escapeHtml(searchText)}"</em></li>`;
            return;
        }

        // INSTANT: Build and append items one by one instead of replacing all
        filteredCourses.forEach((course) => {
            const li = document.createElement("li");
            const timeStr = formatCreationTime(course.creation_time);
            li.innerHTML = `
        <strong>${escapeHtml(course.title)}</strong>
        <p>${escapeHtml(course.description || "No description")}</p>
        ${timeStr ? `<span style="color: #999; font-size: 0.85em; display: block; margin: 4px 0;">⌛ Active creation time: ${escapeHtml(timeStr)}</span>` : ''}
        <span style="background: ${course.status === "pending" ? "#ff9800" : "#4caf50"
                }; color: white; padding: 4px 8px; border-radius: 3px; font-size: 0.9em;">
            ${escapeHtml(course.status?.toUpperCase()) || "UNKNOWN"}
        </span>
        <button onclick="editCourse(${course.id})">Edit</button>
        <button onclick="viewCourse(${course.id})">View</button>
        <button onclick="deleteCourse(${course.id})">Delete</button>
      `;
            list.appendChild(li);
        });
    });
}

function renderAvailableCourses(searchText) {
    const lists = [
        document.getElementById("available-courses-list-user"),
        document.getElementById("available-courses-list-admin"),
        document.getElementById("available-courses-list-superadmin"),
    ];

    // Filter courses based on search text
    const filteredCourses = filterCourseList(availableCourses, searchText);

    lists.forEach((list) => {
        if (!list) return;

        // INSTANT: Clear existing list to prevent duplicates
        list.innerHTML = "";

        if (availableCourses.length === 0) {
            list.innerHTML = "<li><em>No available courses</em></li>";
            return;
        }

        if (filteredCourses.length === 0) {
            list.innerHTML = `<li><em>No courses found matching "${escapeHtml(searchText)}"</em></li>`;
            return;
        }

        // INSTANT: Build and append items one by one instead of replacing all
        filteredCourses.forEach((course) => {
            const li = document.createElement("li");
            li.innerHTML = `
        <strong>${escapeHtml(course.title)}</strong>
        <p>${escapeHtml(course.description || "No description")}</p>
        <button onclick="viewCourse(${course.id})">View</button>
        <button onclick="enrollInCourse(${course.id})">Enroll</button>
      `;
            list.appendChild(li);
        });
    });
}

function createNewCourse() {
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
}

function editCourse(courseId) {
    currentEditingCourseId = courseId;
    const course = myCourses.find((c) => c.id === courseId);

    if (course) {
        document.getElementById("course-title").value = course.title;
        document.getElementById("course-description").value =
            course.description || "";

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

        console.log("✅ Course loaded with", courseBlocks.length, "blocks");
        console.log("  Blocks:", courseBlocks);

        // Load quiz questions for this course and re-render placeholders
        loadCourseQuestions(courseId).then(() => {
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
            updatePageControls();

            startCourseTimer(course.creation_time || 0);
        });
    }
}

function saveCourse(action = "draft") {
    const title = document.getElementById("course-title").value;
    const description = document.getElementById("course-description").value;

    // Save current page content before gathering all content
    saveCurrentPageContent();

    // Join all pages with delimiter
    const fullContent = coursePages.join('<hr class="page-break">');

    // DO NOT remove quiz placeholders. They are needed for the viewer to know where to render quizzes.
    // The viewer will replace them with interactive elements.
    const content = fullContent;

    if (!title.trim()) {
        alert("Please enter a course title");
        return;
    }

    // Set course status based on action
    const status = action === "pending" ? "pending" : "draft";

    console.log(`\n=== SAVE COURSE DEBUG ===`);
    console.log(`Action: ${action}`);
    console.log(`Status to save: ${status}`);
    console.log(`Title: "${title}"`);
    console.log(`Description: "${description}"`);
    console.log(`Content HTML length: ${content.length}`);
    console.log(`courseBlocks count: ${courseBlocks.length}`);
    console.log(`courseBlocks:`, courseBlocks);

    const url = currentEditingCourseId
        ? `${API_BASE_URL}/api/courses/${currentEditingCourseId}`
        : `${API_BASE_URL}/api/courses`;

    const method = currentEditingCourseId ? "PUT" : "POST";

    const courseData = {
        title,
        description,
        content,
        blocks: JSON.stringify(courseBlocks), // Save the blocks array
        status: status,
        creation_time: courseTimer.totalSeconds
    };

    console.log(`Sending ${method} request to ${url}`);
    console.log(`Payload:`, courseData);

    fetch(url, {
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
            console.log(`Response:`, data);
            if (data.success) {
                // Set currentEditingCourseId if this was a new course
                if (!currentEditingCourseId) {
                    currentEditingCourseId = data.data?.id || data.data;
                    console.log("✅ New course saved, currentEditingCourseId set to:", currentEditingCourseId);
                }

                const message =
                    action === "pending"
                        ? "Course submitted for approval!"
                        : "Course saved as draft!";
                alert(message);

                // INSTANT: Stay in editor, just reload course data in background
                loadUserCourses();
                if (action === "pending") {
                    loadPendingCourses();
                }

                // DON'T navigate away - stay in editor for seamless quiz editing
                // showDashboard(); // REMOVED - user wants to stay in editor
            } else {
                alert(`Error: ${data.message || "Failed to save course"}`);
            }
        })
        .catch((err) => {
            console.error("Error saving course:", err);
            alert("Error saving course. Check console for details.");
        });
}

// Global variables for tracking context
let currentAssignmentId = null;

async function viewCourse(courseId, assignmentId = null) {
    currentAssignmentId = assignmentId;
    const course = myCourses.find((c) => c.id === courseId) ||
        availableCourses.find((c) => c.id === courseId) ||
        pendingCourses.find((c) => c.id === courseId);

    if (!course) {
        alert("Course not found");
        return;
    }

    // Load questions first so hydration works
    await loadCourseQuestions(courseId);

    document.getElementById("dashboard-section").style.display = "none";
    document.getElementById("course-editor-section").style.display = "none";
    document.getElementById("course-viewer-section").style.display = "block";

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
        // We need to wait for DOM update
        setTimeout(() => {
            if (typeof setupViewerInteractions === 'function') {
                setupViewerInteractions(course.id);
            } else {
                console.error("setupViewerInteractions is NOT defined!");
            }
            // Convert simulator buttons for this page
            convertSimulatorButtonsForViewer(course.id, course);
            // Render LaTeX
            if (window.MathJax) {
                window.MathJax.typesetPromise([viewerContent]).catch(err => console.log('MathJax error:', err));
            }
        }, 0);
    };

    // Define setupViewerInteractions if it's not already defined globally
    // This function attaches event listeners to interactive elements in the viewer
    function setupViewerInteractions(courseId) {
        console.log("Setting up viewer interactions for course:", courseId);

        // Hydrate quiz placeholders first
        hydrateQuizPlaceholders();

        // Re-attach listeners for quizzes
        document.querySelectorAll(".quiz-submit-btn").forEach((btn) => {
            btn.addEventListener("click", (e) => {
                const questionId = e.target.dataset.questionId;
                submitQuizAnswer(questionId, courseId);
            });
        });

        // Re-attach listeners for simulators if needed
        // (Simulators usually have inline onclicks, so might be fine)
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
                    console.log(`Course finished, auto-submitting assignment ${currentAssignmentId}`);
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
                btn.style.background = '#4caf50';
                btn.onclick = () => runEmbeddedBlockSimulator(blockId, div.querySelector('strong')?.textContent || 'Simulator');
            } else if (btn.textContent.includes('Remove')) {
                btn.style.display = 'none';
            }
        });
    });
}

function runEmbeddedBlockSimulator(blockId, title) {
    // Find the block
    const block = courseBlocks.find((b) => b.id === blockId);
    if (!block) {
        alert("Simulator not found");
        return;
    }

    console.log('🎮 Running simulator:', blockId, 'Type:', block.type);
    console.log('   Simulator data:', block.data);

    if (block.type === 'block-simulator') {
        // Create popup window for block simulator
        const baseUrl = window.location.pathname.includes('github.io')
            ? 'https://virat-sisodiya.github.io/Veelearn/veelearn-frontend'
            : window.location.origin;
        const popup = window.open(
            `${baseUrl}/block-simulator.html?embedded=true&courseBlockId=${blockId}&t=${Date.now()}`,
            "block-simulator",
            "width=1200,height=800"
        );

        // Send the simulator's blocks and connections
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
    window.location.href = `http://localhost:5000/simulator-view.html?id=${simulatorId}`;
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

function handleEditSimulator(event, blockId) {
    event.preventDefault();
    event.stopPropagation();

    const block = courseBlocks.find((b) => b.id === blockId);
    if (!block) {
        console.error("Block not found:", blockId);
        return;
    }

    console.log("Opening simulator for editing:", block);
    currentEditingSimulatorBlockId = blockId; // Store for saving later

    if (block.type === "block-simulator") {
        const baseUrl = window.location.pathname.includes('github.io')
            ? 'https://virat-sisodiya.github.io/Veelearn/veelearn-frontend'
            : window.location.origin;
        const popup = window.open(
            `${baseUrl}/block-simulator.html?edit=true&courseBlockId=${blockId}&t=${Date.now()}`,
            "block-simulator-editor",
            "width=1400,height=900"
        );

        if (popup) {
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

    console.log("Simulator removed. Remaining blocks:", courseBlocks);
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
                console.log('🗑️ Modal delete button clicked for question:', currentEditingQuestionId);
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
            if (e.target.value === 'multiple_choice') {
                optionsContainer.style.display = 'block';
            } else {
                optionsContainer.style.display = 'none';
            }
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
                console.log(`🗑️ DELETE clicked for question:`, questionId);
                deleteQuizQuestion(questionId);
                return;
            }

            // Handle edit (click on placeholder, not on button)
            const placeholder = e.target.closest('.quiz-question-placeholder');
            if (placeholder && !e.target.closest('button')) {
                const questionId = placeholder.dataset.questionId;
                if (questionId) {
                    console.log(`📝 EDIT clicked for question:`, questionId);
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
    const questionText = document.getElementById('quiz-question-text').value.trim();
    const questionType = document.getElementById('quiz-question-type').value;
    const correctAnswer = document.getElementById('quiz-correct-answer').value.trim();
    const explanation = document.getElementById('quiz-explanation').value.trim();
    const points = parseInt(document.getElementById('quiz-points').value);

    if (!questionText || !correctAnswer) {
        alert('Please fill in the question text and correct answer');
        return;
    }

    let options = null;
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
                console.log('New question created with ID:', newQuestionId, 'result.data:', result.data);
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
    console.log(`🗑️ Delete button clicked for question ID:`, questionId);
    console.log(`   currentEditingCourseId:`, currentEditingCourseId);
    console.log(`   authToken exists:`, !!authToken);

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
        console.error('âŒ Error deleting question:', error);
        alert('Error deleting question: ' + error.message);
        lastDeletedQuestion = null; // Clear if error
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
        optionsHTML = '<div class="quiz-options">';
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
            } else {
                feedbackDiv.className = 'quiz-feedback incorrect';
                feedbackDiv.innerHTML = `
          <div>❌ Incorrect. The correct answer is: ${escapeHtml(result.data.correct_answer)}</div>
          ${result.data.explanation ? `<div class="quiz-explanation">${escapeHtml(result.data.explanation)}</div>` : ''}
        `;
            }

            const submitBtn = feedbackDiv.previousElementSibling;
            submitBtn.disabled = true;
            submitBtn.textContent = 'Answered';
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

function setupPhetModalListeners() {
    const modal = document.getElementById("phet-modal");
    const closeBtn = document.getElementById("close-phet-modal");
    const cancelBtn = document.getElementById("cancel-phet-modal");
    const searchInput = document.getElementById("phet-search");

    if (closeBtn) closeBtn.onclick = () => modal.style.display = "none";
    if (cancelBtn) cancelBtn.onclick = () => modal.style.display = "none";

    if (searchInput) {
        searchInput.addEventListener("input", (e) => {
            renderPhetList(e.target.value);
        });
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
    updatePageControls();

    // Re-attach listeners to new elements if needed
    // For example, simulator buttons
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
}

let currentViewerPageIndex = 0;
let viewerPages = [];

// ===== COURSE TIMER & ANTI-ABUSE =====
let courseTimer = {
    totalSeconds: 0,
    isRunning: false,
    lastKeyboardActivity: Date.now(),
    keyPressesInWindow: 0,
    lastKeyPressTime: 0,
    repeatedKeyCount: 0,
    lastKey: null,
    isIdle: false,
    intervalId: null
};

function startCourseTimer(initialSeconds = 0) {
    courseTimer.totalSeconds = initialSeconds;
    courseTimer.isRunning = true;
    courseTimer.isIdle = false;
    // Reset checking vars
    courseTimer.lastKeyboardActivity = Date.now();
    courseTimer.keyPressesInWindow = 0;

    // Clear existing interval if any
    if (courseTimer.intervalId) clearInterval(courseTimer.intervalId);

    updateTimerDisplay();

    courseTimer.intervalId = setInterval(() => {
        const now = Date.now();

        // Anti-idle check (60s timeout - Keyboard only as requested)
        if (now - courseTimer.lastKeyboardActivity > 60000) {
            courseTimer.isIdle = true;
        } else {
            courseTimer.isIdle = false;
        }

        if (courseTimer.isRunning && !courseTimer.isIdle) {
            courseTimer.totalSeconds++;
            updateTimerDisplay();
        }
    }, 1000);

    // Anti-macro window reset
    setInterval(() => {
        courseTimer.keyPressesInWindow = 0;
    }, 5000);
}

function stopCourseTimer() {
    courseTimer.isRunning = false;
    if (courseTimer.intervalId) clearInterval(courseTimer.intervalId);
    updateTimerDisplay();
}

function updateTimerDisplay() {
    const timerEl = document.getElementById('course-timer-display');
    const valueEl = document.getElementById('course-timer-value');
    const statusEl = document.getElementById('course-timer-status');

    if (!timerEl || !valueEl) return;

    const hours = Math.floor(courseTimer.totalSeconds / 3600);
    const minutes = Math.floor((courseTimer.totalSeconds % 3600) / 60);
    const seconds = courseTimer.totalSeconds % 60;

    const timeStr = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

    valueEl.textContent = timeStr;

    // Visual feedback
    if (courseTimer.isIdle) {
        statusEl.textContent = '(Idle - Press any key to resume)';
        valueEl.style.color = '#f59e0b'; // Amber
    } else if (!courseTimer.isRunning) {
        statusEl.textContent = '(Paused - Anti-abuse triggered)';
        valueEl.style.color = '#ef4444'; // Red
    } else {
        statusEl.textContent = '(Tracking active time)';
        valueEl.style.color = '#4ade80'; // Green
    }
}

// Global listener for Timer Anti-Abuse
document.addEventListener('keydown', (e) => {
    // Only track if editing a course
    if (!currentEditingCourseId || document.getElementById('course-editor-section').style.display === 'none') return;

    const now = Date.now();
    courseTimer.lastKeyboardActivity = now;
    courseTimer.isIdle = false; // Wake up

    // Anti-Macro: Check frequency
    courseTimer.keyPressesInWindow++;
    if (courseTimer.keyPressesInWindow > 100) {
        // Macro detected!
        courseTimer.isRunning = false;
        console.warn('Anti-Macro triggered: Too many keypresses');
        return;
    }

    // Anti-Keyboard Weight: Check repeats
    if (e.key === courseTimer.lastKey) {
        courseTimer.repeatedKeyCount++;
    } else {
        courseTimer.repeatedKeyCount = 0;
        courseTimer.lastKey = e.key;
    }

    if (courseTimer.repeatedKeyCount > 50) {
        // Weight detected!
        courseTimer.isRunning = false;
        console.warn('Anti-Weight triggered: Key held down/repeated too long');
        return;
    }

    // Resume if previously stopped/idle but now passing checks
    if (!courseTimer.isRunning && !courseTimer.isIdle && courseTimer.repeatedKeyCount < 50 && courseTimer.keyPressesInWindow < 100) {
        courseTimer.isRunning = true;
        updateTimerDisplay();
    }
});

// ===== COURSE MANAGEMENT VARIABLES =====

// ===== PLACEMENT LOGIC =====

function startPlacementMode(type, data) {
    console.log("Starting placement mode for:", type);
    isPlacementMode = true;
    placementType = type;
    placementData = data;

    const editor = document.getElementById("course-content-editor");
    // FORCE position relative to ensure absolute children work
    editor.style.position = "relative";
    editor.style.cursor = "crosshair";
    editor.classList.add("placement-mode");

    // Show a toast or message
    alert("Click anywhere in the editor to place the element.");
}

function handleEditorClick(e) {
    if (!isPlacementMode) return;

    const editor = document.getElementById("course-content-editor");

    // Ensure click is inside editor
    if (!editor.contains(e.target) && e.target !== editor) return;

    const rect = editor.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top + editor.scrollTop;

    console.log(`Placement click at: ${x}, ${y}`);
    console.log(`Rect: top=${rect.top}, left=${rect.left}, scrollTop=${editor.scrollTop}`);

    if (placementType === 'visual-simulator' || placementType === 'block-simulator') {
        insertSimulatorAtPosition(placementData.id, placementData.title, placementData.type, x, y);
    } else if (placementType === 'quiz') {
        insertQuizPlaceholderAtPosition(placementData.id, placementData.text, x, y);
    } else if (placementType === 'phet-simulator') {
        insertPhetSimAtPosition(placementData, x, y);
    }

    // Reset mode
    isPlacementMode = false;
    placementType = null;
    placementData = null;
    editor.style.cursor = "text";
    editor.classList.remove("placement-mode");
}

function insertSimulatorAtPosition(blockId, title, type, x, y) {
    console.log(`Inserting simulator at ${x}, ${y}`);

    // Ensure coordinates are numbers
    const safeX = Number.isFinite(x) ? x : 0;
    const safeY = Number.isFinite(y) ? y : 0;

    const contentEditor = document.getElementById("course-content-editor");
    const simulatorDiv = document.createElement("div");
    simulatorDiv.className = "simulator-block";
    simulatorDiv.dataset.blockId = blockId;
    simulatorDiv.contentEditable = 'false';

    // Use direct style properties for reliability
    simulatorDiv.style.position = 'absolute';
    simulatorDiv.style.left = `${safeX}px`;
    simulatorDiv.style.top = `${safeY}px`;
    simulatorDiv.style.width = '300px';
    simulatorDiv.style.background = '#f0f0f0';
    simulatorDiv.style.padding = '15px';
    simulatorDiv.style.borderLeft = '4px solid #667eea';
    simulatorDiv.style.borderRadius = '4px';
    simulatorDiv.style.zIndex = '10';
    simulatorDiv.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';

    // Force !important via cssText for critical properties
    simulatorDiv.style.cssText += `position: absolute !important; left: ${safeX}px !important; top: ${safeY}px !important;`;

    simulatorDiv.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong>${escapeHtml(type)}</strong>
                <p style="margin: 5px 0; color: #666;">${escapeHtml(title)}</p>
            </div>
            <div style="display: flex; gap: 10px;">
                <button type="button" onclick="openSliderConfigModal(${blockId})" style="padding: 5px 10px; background: #10b981; color: white; border: none; border-radius: 4px; cursor: pointer;">⚙️</button>
                <button type="button" onclick="handleEditSimulator(event, ${blockId})" style="padding: 5px 10px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer;">✏️</button>
                <button type="button" onclick="handleRemoveSimulator(event, ${blockId})" style="padding: 5px 10px; background: #f44336; color: white; border: none; border-radius: 4px; cursor: pointer;">🗑️</button>
            </div>
        </div>
    `;

    contentEditor.appendChild(simulatorDiv);

    // Make it draggable (basic implementation)
    makeElementDraggable(simulatorDiv);
}

function makeElementDraggable(elmnt) {
    let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

    elmnt.onmousedown = dragMouseDown;

    function dragMouseDown(e) {
        // Don't drag if clicking buttons
        if (e.target.tagName === 'BUTTON') return;

        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:
        elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
        // stop moving when mouse button is released:
        document.onmouseup = null;
        document.onmousemove = null;
    }
}

function insertQuizPlaceholderAtPosition(questionId, questionText, x, y) {
    const safeX = Number.isFinite(x) ? x : 0;
    const safeY = Number.isFinite(y) ? y : 0;

    const editor = document.getElementById('course-content-editor');
    const placeholder = document.createElement('div');
    placeholder.className = 'quiz-question-placeholder';
    placeholder.dataset.questionId = questionId;
    placeholder.contentEditable = 'false';

    // Explicit styles with !important
    placeholder.style.cssText = `
    position: absolute !important;
    left: ${safeX}px !important;
    top: ${safeY}px !important;
    width: 300px;
    background: rgba(102, 126, 234, 0.2); 
    border: 2px dashed var(--primary); 
    padding: 1em; 
    border-radius: 4px; 
    cursor: pointer; 
    user-select: none;
    z-index: 10;
  `;

    placeholder.innerHTML = `
    <strong>❓ Quiz Question:</strong> ${escapeHtml(questionText.substring(0, 100))}${questionText.length > 100 ? '...' : ''}
    <button type="button" class="quiz-placeholder-delete-btn" data-question-id="${questionId}" style="position: absolute; top: 5px; right: 5px; background: #e53e3e; color: white; border: none; border-radius: 4px; padding: 2px 6px; cursor: pointer; font-size: 0.8em; z-index: 10;">🗑️ Delete</button>
    <div style="font-size: 0.85em; color: #999; margin-top: 0.5em;">Click to edit</div>
  `;

    // Click handler for editing
    placeholder.addEventListener('click', (e) => {
        if (e.target.closest('button')) return;
        const qId = placeholder.dataset.questionId;
        if (qId) {
            openQuizModal(parseInt(qId));
        }
    });

    // Delete handler
    const deleteBtn = placeholder.querySelector('.quiz-placeholder-delete-btn');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const qId = parseInt(placeholder.dataset.questionId);
            if (qId && !isNaN(qId) && confirm('Delete this question?')) {
                deleteQuizQuestion(qId);
            }
        });
    }

    editor.appendChild(placeholder);
    makeElementDraggable(placeholder);
}

function insertPhetSimAtPosition(sim, x, y) {
    const safeX = Number.isFinite(x) ? x : 0;
    const safeY = Number.isFinite(y) ? y : 0;

    const contentEditor = document.getElementById("course-content-editor");
    const wrapper = document.createElement("div");
    wrapper.className = "phet-sim-wrapper";
    wrapper.contentEditable = "false";

    wrapper.style.cssText = `
    position: absolute !important;
    left: ${safeX}px !important;
    top: ${safeY}px !important;
    width: 600px; /* Fixed width for absolute positioning */
    border: 1px solid #ddd; 
    border-radius: 8px; 
    overflow: hidden; 
    background: #fff;
    z-index: 10;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  `;

    wrapper.innerHTML = `
        <div style="background: #f0f0f0; padding: 10px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #ddd; cursor: move;">
            <strong>⚛️ ${escapeHtml(sim.title)}</strong>
            <button class="phet-remove-btn" style="background: #ff4444; color: white; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer;">Remove</button>
        </div>
        <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
            <iframe src="${sim.url}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0; pointer-events: auto;" allowfullscreen></iframe>
        </div>
    `;

    // Remove handler
    wrapper.querySelector('.phet-remove-btn').addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent drag start
        if (confirm('Remove this simulator?')) {
            wrapper.remove();
        }
    });

    contentEditor.appendChild(wrapper);
    makeElementDraggable(wrapper);
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
                html += `<tr style="border: 1px solid #555;">
          <td style="padding: 10px; border: 1px solid #555;">${escapeHtml(sub.email)}</td>
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
        searchInput.addEventListener('input', searchAssignmentCourses);
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

