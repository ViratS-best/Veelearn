// Veelearn Server Loading Screen Logic

class ServerLoadingManager {
    constructor() {
        this.startTime = Date.now();
        this.maxWaitTime = 120000; // 2 minutes max wait
        this.checkInterval = 2000; // Check every 2 seconds
        this.progressInterval = null;
        this.serverCheckInterval = null;
        this.isServerReady = false;
        this.attemptCount = 0;
        this.maxAttempts = 60; // 2 minutes / 2 seconds
        
        // DOM elements
        this.loadingMessage = document.getElementById('loading-message');
        this.loadingSubmessage = document.getElementById('loading-submessage');
        this.progressFill = document.getElementById('progress-fill');
        this.progressPercentage = document.getElementById('progress-percentage');
        this.progressTime = document.getElementById('progress-time');
        this.statusDot = document.getElementById('status-dot');
        this.statusText = document.getElementById('status-text');
        
        this.init();
    }
    
    init() {
        this.startProgressAnimation();
        this.startServerHealthCheck();
        this.updateLoadingMessages();
    }
    
    startProgressAnimation() {
        let progress = 0;
        const totalTime = this.maxWaitTime;
        
        this.progressInterval = setInterval(() => {
            const elapsed = Date.now() - this.startTime;
            progress = Math.min((elapsed / totalTime) * 100, 95); // Cap at 95% until server is ready
            
            this.updateProgress(progress);
            
            if (progress >= 95 && !this.isServerReady) {
                this.showTimeoutWarning();
            }
        }, 500);
    }
    
    updateProgress(percentage) {
        this.progressFill.style.width = `${percentage}%`;
        this.progressPercentage.textContent = `${Math.round(percentage)}%`;
        
        const elapsed = Date.now() - this.startTime;
        const remaining = Math.max(0, this.maxWaitTime - elapsed);
        const remainingSeconds = Math.ceil(remaining / 1000);
        
        if (remainingSeconds > 60) {
            this.progressTime.textContent = `~${Math.ceil(remainingSeconds / 60)}m remaining`;
        } else {
            this.progressTime.textContent = `~${remainingSeconds}s remaining`;
        }
    }
    
    updateLoadingMessages() {
        const elapsed = Date.now() - this.startTime;
        const phases = [
            { time: 0, message: "Connecting to Veelearn...", submessage: "Establishing secure connection" },
            { time: 5000, message: "Server waking up...", submessage: "Free servers need time to start (this is normal)" },
            { time: 15000, message: "Initializing learning environment...", submessage: "Loading STEM simulations and courses" },
            { time: 30000, message: "Almost ready...", submessage: "Preparing your personalized learning experience" },
            { time: 60000, message: "Final preparations...", submessage: "Server is starting up - please stay with us" }
        ];
        
        const currentPhase = phases.reduce((prev, curr) => 
            elapsed >= curr.time ? curr : prev
        );
        
        this.loadingMessage.textContent = currentPhase.message;
        this.loadingSubmessage.textContent = currentPhase.submessage;
    }
    
    async startServerHealthCheck() {
        this.serverCheckInterval = setInterval(async () => {
            this.attemptCount++;
            this.updateLoadingMessages();
            
            try {
                const response = await fetch('/api/health', {
                    method: 'GET',
                    timeout: 5000,
                    headers: {
                        'Cache-Control': 'no-cache',
                        'Pragma': 'no-cache'
                    }
                });
                
                if (response.ok) {
                    const data = await response.json();
                    if (data.status === 'ok') {
                        this.onServerReady();
                        return;
                    }
                }
            } catch (error) {
                // Expected during server wake-up
                console.log(`Health check attempt ${this.attemptCount} failed:`, error.message);
            }
            
            if (this.attemptCount >= this.maxAttempts) {
                this.onTimeout();
            }
        }, this.checkInterval);
    }
    
    onServerReady() {
        if (this.isServerReady) return;
        
        this.isServerReady = true;
        clearInterval(this.progressInterval);
        clearInterval(this.serverCheckInterval);
        
        // Update UI to show success
        this.progressFill.style.width = '100%';
        this.progressPercentage.textContent = '100%';
        this.progressTime.textContent = 'Complete!';
        
        this.loadingMessage.textContent = 'Welcome to Veelearn!';
        this.loadingSubmessage.textContent = 'Server is ready - Redirecting you now...';
        
        this.statusDot.className = 'status-dot ready';
        this.statusText.textContent = 'Server ready';
        
        // Add success animation
        document.querySelector('.loading-container').style.animation = 'fadeInUp 0.5s ease-out reverse';
        
        // Redirect after brief delay
        setTimeout(() => {
            this.redirectToTarget();
        }, 1500);
    }
    
    onTimeout() {
        clearInterval(this.progressInterval);
        clearInterval(this.serverCheckInterval);
        
        this.loadingMessage.textContent = 'Server Taking Longer Than Expected';
        this.loadingSubmessage.textContent = 'Please try refreshing the page or contact support if this persists';
        
        this.statusDot.className = 'status-dot error';
        this.statusText.textContent = 'Connection timeout';
        
        // Show retry button
        this.showRetryButton();
    }
    
    showTimeoutWarning() {
        if (this.isServerReady) return;
        
        this.loadingSubmessage.textContent = 'Server is taking longer than usual - this sometimes happens with free hosting';
    }
    
    showRetryButton() {
        const retryButton = document.createElement('button');
        retryButton.textContent = 'Try Again';
        retryButton.className = 'retry-button';
        retryButton.style.cssText = `
            margin-top: 20px;
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease;
        `;
        
        retryButton.addEventListener('click', () => {
            window.location.reload();
        });
        
        retryButton.addEventListener('mouseenter', () => {
            retryButton.style.transform = 'scale(1.05)';
        });
        
        retryButton.addEventListener('mouseleave', () => {
            retryButton.style.transform = 'scale(1)';
        });
        
        document.querySelector('.loading-container').appendChild(retryButton);
    }
    
    redirectToTarget() {
        // Get the original destination from URL parameters or default to login
        const urlParams = new URLSearchParams(window.location.search);
        const target = urlParams.get('target') || 'login';
        
        if (target === 'login') {
            window.location.href = 'index.html#auth-section';
        } else if (target === 'register') {
            window.location.href = 'index.html#auth-section?mode=register';
        } else {
            window.location.href = target;
        }
    }
    
    // Public method to manually trigger loading screen
    static show(target = 'login') {
        // Create loading overlay if it doesn't exist
        let overlay = document.getElementById('loading-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'loading-overlay';
            document.body.appendChild(overlay);
            
            // Load the loading screen content
            fetch('loading-overlay.html')
                .then(response => response.text())
                .then(html => {
                    overlay.innerHTML = html;
                    new ServerLoadingManager();
                })
                .catch(error => {
                    console.error('Failed to load loading screen:', error);
                    // Fallback: simple loading message
                    overlay.innerHTML = `
                        <div style="display: flex; align-items: center; justify-content: center; height: 100vh; background: #0f172a; color: white; font-family: Arial, sans-serif;">
                            <div style="text-align: center;">
                                <h2>Veelearn</h2>
                                <p>Server waking up... Please wait.</p>
                            </div>
                        </div>
                    `;
                });
        }
    }
    
    // Public method to hide loading screen
    static hide() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.style.animation = 'fadeOut 0.3s ease-out';
            setTimeout(() => {
                overlay.remove();
            }, 300);
        }
    }
}

// Auto-initialize if this is the loading overlay page
if (window.location.pathname.includes('loading-overlay.html')) {
    document.addEventListener('DOMContentLoaded', () => {
        new ServerLoadingManager();
    });
}

// Export for use in other scripts
window.ServerLoadingManager = ServerLoadingManager;
