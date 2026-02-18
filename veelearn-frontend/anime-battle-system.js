/**
 * ============================================
 * PROFESSIONAL ANIME-STYLE BATTLE SYSTEM v2
 * ============================================
 * 
 * Professional artistic battle animations with:
 * - High-quality character rendering with proper proportions
 * - Artistic strokes and shading
 * - Dynamic particle systems
 * - Professional visual effects
 * - Smooth easing and transitions
 * - Beautiful background art
 */

class AnimeBattleSystem {
    constructor(setup) {
        this.setup = setup;
        this.canvas = null;
        this.ctx = null;
        this.time = 0;
        this.phase = 'backstory';
        this.cameraShakeIntensity = 0;
        this.particles = [];
        this.slashes = [];
        this.magic = [];
    }

    init(container) {
        this.canvas = document.createElement('canvas');
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        this.canvas.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: block;
        `;
        container.appendChild(this.canvas);
        this.ctx = this.canvas.getContext('2d');
        this.ctx.imageSmoothingEnabled = true;
        this.ctx.imageSmoothingQuality = 'high';
        this.ctx.lineCap = 'round';
        this.ctx.lineJoin = 'round';
    }

    animate(deltaTime) {
        this.time += deltaTime;

        // Clear canvas
        this.ctx.fillStyle = this.getBackgroundColor();
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw environment
        this.drawEnvironment();

        if (this.phase === 'backstory') {
            this.updateBackstory();
        } else if (this.phase === 'fight') {
            this.updateFight();
        } else if (this.phase === 'victory') {
            this.updateVictory();
        }

        // Update and draw particles
        this.updateParticles();
        this.drawParticles();
        this.drawSlashes();
        this.drawMagicEffects();

        // Apply camera shake
        if (this.cameraShakeIntensity > 0) {
            this.cameraShakeIntensity *= 0.92;
        }
    }

    getBackgroundColor() {
        const env = this.setup.environment;
        return env.skyColor || '#1a1a2e';
    }

    drawEnvironment() {
        const env = this.setup.environment;
        const w = this.canvas.width;
        const h = this.canvas.height;

        // Gradient background
        const gradient = this.ctx.createLinearGradient(0, 0, 0, h);
        gradient.addColorStop(0, env.skyColor);
        gradient.addColorStop(1, env.groundColor);
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, w, h);

        // Environment-specific details
        if (env.id === 'forest') {
            this.drawForestEnvironment();
        } else if (env.id === 'volcano') {
            this.drawVolcanoEnvironment();
        } else if (env.id === 'ocean') {
            this.drawOceanEnvironment();
        } else if (env.id === 'castle') {
            this.drawCastleEnvironment();
        } else if (env.id === 'sky') {
            this.drawSkyEnvironment();
        }
    }

    drawForestEnvironment() {
        const w = this.canvas.width;
        const h = this.canvas.height;
        const env = this.setup.environment;

        // Distant trees (parallax layer 1)
        this.ctx.fillStyle = 'rgba(30, 60, 20, 0.3)';
        for (let i = 0; i < 3; i++) {
            const x = (w * 0.2) + (i * w * 0.3) + Math.sin(this.time / 3000) * 20;
            this.drawTreeShape(x, h * 0.25, 80, 0.3);
        }

        // Mid trees (parallax layer 2)
        this.ctx.fillStyle = 'rgba(45, 90, 35, 0.5)';
        for (let i = 0; i < 4; i++) {
            const x = (i * w * 0.25) + Math.sin(this.time / 2000 + i) * 10;
            this.drawTreeShape(x, h * 0.45, 120, 0.5);
        }

        // Foreground trees
        this.ctx.fillStyle = env.accent1;
        for (let i = 0; i < 5; i++) {
            const x = (i * w * 0.2);
            this.drawTreeShape(x, h * 0.65, 150, 0.8);
        }

        // Ground mist
        const mistGradient = this.ctx.createLinearGradient(0, h * 0.7, 0, h);
        mistGradient.addColorStop(0, 'rgba(100, 150, 100, 0)');
        mistGradient.addColorStop(1, 'rgba(50, 80, 50, 0.3)');
        this.ctx.fillStyle = mistGradient;
        this.ctx.fillRect(0, h * 0.7, w, h * 0.3);
    }

    drawVolcanoEnvironment() {
        const w = this.canvas.width;
        const h = this.canvas.height;

        // Smoke clouds
        this.ctx.fillStyle = 'rgba(80, 40, 20, 0.3)';
        for (let i = 0; i < 5; i++) {
            const x = (i * w * 0.25) + Math.sin(this.time / 1500 + i) * 40;
            const y = h * 0.2 + Math.cos(this.time / 2000 + i) * 30;
            this.drawSmoke(x, y, 100 + i * 10);
        }

        // Lava glow
        const glowIntensity = Math.sin(this.time / 800) * 0.2 + 0.6;
        this.ctx.fillStyle = `rgba(255, 100, 0, ${0.15 * glowIntensity})`;
        this.ctx.fillRect(0, h * 0.4, w, h * 0.6);

        // Volcanic rocks/ground
        this.ctx.fillStyle = '#6b3410';
        for (let i = 0; i < 4; i++) {
            const x = (i * w * 0.25) + w * 0.1;
            const y = h * 0.7;
            this.drawRock(x, y, 80 + i * 20);
        }
    }

    drawOceanEnvironment() {
        const w = this.canvas.width;
        const h = this.canvas.height;

        // Storm clouds
        this.ctx.fillStyle = 'rgba(30, 50, 70, 0.4)';
        for (let i = 0; i < 4; i++) {
            const x = (i * w * 0.3) + Math.sin(this.time / 3000 + i) * 50;
            const y = h * 0.12 + Math.cos(this.time / 4000 + i) * 20;
            this.drawStormCloud(x, y, 120);
        }

        // Waves with perspective
        this.ctx.strokeStyle = 'rgba(93, 173, 226, 0.4)';
        this.ctx.lineWidth = 3;
        for (let layer = 0; layer < 3; layer++) {
            this.ctx.beginPath();
            const wavePhase = (this.time / 800) % (Math.PI * 2);
            const baseY = h * 0.55 + (layer * 50);
            for (let x = 0; x <= w; x += 30) {
                const y = baseY + Math.sin((x / 150) + wavePhase + layer) * (20 - layer * 5);
                if (x === 0) this.ctx.moveTo(x, y);
                else this.ctx.lineTo(x, y);
            }
            this.ctx.stroke();
        }

        // Ocean foam
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.15)';
        this.ctx.fillRect(0, h * 0.55, w, 20);
    }

    drawCastleEnvironment() {
        const w = this.canvas.width;
        const h = this.canvas.height;

        // Twinkling stars
        for (let i = 0; i < 30; i++) {
            const seed = i * 123;
            const x = Math.sin(seed) * w * 0.5 + w * 0.5;
            const y = Math.cos(seed) * h * 0.35 + h * 0.1;
            const brightness = Math.sin(this.time / 800 + seed) * 0.3 + 0.5;
            this.ctx.fillStyle = `rgba(255, 255, 200, ${brightness * 0.6})`;
            this.drawStar(x, y, 3);
        }

        // Castle walls with perspective
        this.ctx.fillStyle = '#5a5a5a';
        this.drawPerspectiveWall(w * 0.1, h * 0.35, w * 0.25, h * 0.55, 0.3);

        this.ctx.fillStyle = '#6a6a6a';
        this.drawPerspectiveWall(w * 0.35, h * 0.3, w * 0.3, h * 0.6, 0.35);

        this.ctx.fillStyle = '#4a4a4a';
        this.drawPerspectiveWall(w * 0.65, h * 0.35, w * 0.25, h * 0.55, 0.3);

        // Ground shadows
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
        this.ctx.fillRect(0, h * 0.8, w, h * 0.2);
    }

    drawSkyEnvironment() {
        const w = this.canvas.width;
        const h = this.canvas.height;

        // Floating islands with shadow
        for (let i = 0; i < 3; i++) {
            const x = (w * 0.2) + (i * w * 0.35);
            const y = h * 0.2 + (i * 30);
            const size = 100 + i * 20;

            // Island shadow
            this.ctx.fillStyle = 'rgba(0, 0, 0, 0.15)';
            this.drawIsland(x, y + 20, size);

            // Island
            this.ctx.fillStyle = '#6b8e23';
            this.drawIsland(x, y, size);

            // Island glow
            this.ctx.strokeStyle = `rgba(100, 180, 200, ${0.3 + Math.sin(this.time / 2000 + i) * 0.2})`;
            this.ctx.lineWidth = 3;
            this.drawIslandOutline(x, y, size);
        }

        // Clouds with depth
        for (let i = 0; i < 5; i++) {
            const alpha = 0.3 + (i * 0.1);
            this.ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
            const x = (i * w * 0.25) + Math.sin(this.time / 4000 + i) * 30;
            const y = h * 0.15 + (i * 20);
            this.drawCloud(x, y, 80 + i * 10);
        }
    }

    // ===== CHARACTER DRAWING =====

    drawHeroCharacter(x, y, scale, hero, isAttacking) {
        this.ctx.save();
        this.ctx.translate(x, y);
        this.ctx.scale(scale, scale);

        const headX = 0;
        const headY = -35;
        const bodyY = 0;
        const bodyWidth = 40;
        const bodyHeight = 50;

        // Aura (when attacking)
        if (isAttacking) {
            this.ctx.strokeStyle = `rgba(${this.hexToRgb(hero.accent).r}, ${this.hexToRgb(hero.accent).g}, ${this.hexToRgb(hero.accent).b}, 0.4)`;
            this.ctx.lineWidth = 8;
            this.drawAura(0, bodyY, 80);

            this.ctx.strokeStyle = `rgba(${this.hexToRgb(hero.accent).r}, ${this.hexToRgb(hero.accent).g}, ${this.hexToRgb(hero.accent).b}, 0.2)`;
            this.ctx.lineWidth = 4;
            this.drawAura(0, bodyY, 100);
        }

        // Body with gradient
        const bodyGradient = this.ctx.createLinearGradient(-bodyWidth / 2, bodyY - bodyHeight / 2, -bodyWidth / 2, bodyY + bodyHeight / 2);
        bodyGradient.addColorStop(0, this.lighten(hero.color, 1.3));
        bodyGradient.addColorStop(0.5, hero.color);
        bodyGradient.addColorStop(1, this.lighten(hero.color, 0.8));
        this.ctx.fillStyle = bodyGradient;
        this.roundRect(this.ctx, -bodyWidth / 2, bodyY - bodyHeight / 2, bodyWidth, bodyHeight, 8);
        this.ctx.fill();

        // Outline
        this.ctx.strokeStyle = this.darken(hero.color, 0.6);
        this.ctx.lineWidth = 2;
        this.roundRect(this.ctx, -bodyWidth / 2, bodyY - bodyHeight / 2, bodyWidth, bodyHeight, 8);
        this.ctx.stroke();

        // Head
        const headGradient = this.ctx.createRadialGradient(headX, headY, 0, headX, headY, 22);
        headGradient.addColorStop(0, this.lighten(hero.color, 1.2));
        headGradient.addColorStop(1, hero.color);
        this.ctx.fillStyle = headGradient;
        this.ctx.beginPath();
        this.ctx.arc(headX, headY, 22, 0, Math.PI * 2);
        this.ctx.fill();

        this.ctx.strokeStyle = this.darken(hero.color, 0.6);
        this.ctx.lineWidth = 2;
        this.ctx.stroke();

        // Eyes with shine
        this.ctx.fillStyle = '#fff';
        this.ctx.beginPath();
        this.ctx.arc(headX - 8, headY - 3, 5, 0, Math.PI * 2);
        this.ctx.arc(headX + 8, headY - 3, 5, 0, Math.PI * 2);
        this.ctx.fill();

        this.ctx.fillStyle = '#000';
        this.ctx.beginPath();
        this.ctx.arc(headX - 8, headY - 2, 3, 0, Math.PI * 2);
        this.ctx.arc(headX + 8, headY - 2, 3, 0, Math.PI * 2);
        this.ctx.fill();

        // Pupils with shine
        this.ctx.fillStyle = '#4dd0ff';
        this.ctx.beginPath();
        this.ctx.arc(headX - 7.5, headY - 2.5, 1.5, 0, Math.PI * 2);
        this.ctx.arc(headX + 8.5, headY - 2.5, 1.5, 0, Math.PI * 2);
        this.ctx.fill();

        // Weapon/sword with glow
        this.ctx.save();
        if (isAttacking) {
            this.ctx.rotate(0.3);
        }
        
        // Sword glow
        this.ctx.shadowColor = `rgba(${this.hexToRgb(hero.accent).r}, ${this.hexToRgb(hero.accent).g}, ${this.hexToRgb(hero.accent).b}, 0.6)`;
        this.ctx.shadowBlur = 15;
        
        this.ctx.strokeStyle = this.lighten(hero.accent, 1.2);
        this.ctx.lineWidth = 6;
        this.ctx.beginPath();
        this.ctx.moveTo(30, bodyY - 20);
        this.ctx.lineTo(70, bodyY - 70);
        this.ctx.stroke();

        this.ctx.strokeStyle = hero.accent;
        this.ctx.lineWidth = 3;
        this.ctx.stroke();

        // Blade shine
        this.ctx.strokeStyle = '#fff';
        this.ctx.lineWidth = 1;
        this.ctx.stroke();

        this.ctx.shadowColor = 'transparent';
        this.ctx.restore();

        // Arms
        this.drawArm(this.ctx, -bodyWidth / 2 - 5, bodyY - 10, hero.color, isAttacking ? 0.4 : 0);
        this.drawArm(this.ctx, bodyWidth / 2 + 5, bodyY - 10, hero.color, 0);

        // Legs
        this.drawLeg(this.ctx, -bodyWidth / 4, bodyY + bodyHeight / 2, hero.color);
        this.drawLeg(this.ctx, bodyWidth / 4, bodyY + bodyHeight / 2, hero.color);

        this.ctx.restore();
    }

    drawEnemyCharacter(x, y, scale, enemy, isAttacking) {
        this.ctx.save();
        this.ctx.translate(x, y);
        this.ctx.scale(scale, scale);

        const headX = 0;
        const headY = -35;
        const bodyY = 0;
        const bodyWidth = 45;
        const bodyHeight = 55;

        // Dark aura (menacing)
        this.ctx.strokeStyle = `rgba(${this.hexToRgb(enemy.accent).r}, 50, 50, ${isAttacking ? 0.6 : 0.3})`;
        this.ctx.lineWidth = 10;
        this.drawAura(0, bodyY, 90);

        if (isAttacking) {
            this.ctx.strokeStyle = `rgba(${this.hexToRgb(enemy.accent).r}, 100, 100, 0.2)`;
            this.ctx.lineWidth = 6;
            this.drawAura(0, bodyY, 120);
        }

        // Body (darker, more menacing)
        const bodyGradient = this.ctx.createLinearGradient(-bodyWidth / 2, bodyY - bodyHeight / 2, -bodyWidth / 2, bodyY + bodyHeight / 2);
        bodyGradient.addColorStop(0, this.lighten(enemy.color, 0.9));
        bodyGradient.addColorStop(0.5, enemy.color);
        bodyGradient.addColorStop(1, this.darken(enemy.color, 0.4));
        this.ctx.fillStyle = bodyGradient;
        this.roundRect(this.ctx, -bodyWidth / 2, bodyY - bodyHeight / 2, bodyWidth, bodyHeight, 8);
        this.ctx.fill();

        // Dark outline
        this.ctx.strokeStyle = this.darken(enemy.color, 1.2);
        this.ctx.lineWidth = 3;
        this.roundRect(this.ctx, -bodyWidth / 2, bodyY - bodyHeight / 2, bodyWidth, bodyHeight, 8);
        this.ctx.stroke();

        // Head (larger, more menacing)
        const headGradient = this.ctx.createRadialGradient(headX, headY, 0, headX, headY, 25);
        headGradient.addColorStop(0, this.lighten(enemy.accent, 0.8));
        headGradient.addColorStop(1, enemy.accent);
        this.ctx.fillStyle = headGradient;
        this.ctx.beginPath();
        this.ctx.arc(headX, headY, 25, 0, Math.PI * 2);
        this.ctx.fill();

        this.ctx.strokeStyle = this.darken(enemy.accent, 1);
        this.ctx.lineWidth = 3;
        this.ctx.stroke();

        // Glowing red eyes (menacing)
        this.ctx.shadowColor = 'rgba(255, 100, 100, 0.8)';
        this.ctx.shadowBlur = 20;

        this.ctx.fillStyle = '#ff4444';
        this.ctx.beginPath();
        this.ctx.arc(headX - 8, headY - 2, 6, 0, Math.PI * 2);
        this.ctx.arc(headX + 8, headY - 2, 6, 0, Math.PI * 2);
        this.ctx.fill();

        // Inner glow
        this.ctx.fillStyle = '#ffff00';
        this.ctx.beginPath();
        this.ctx.arc(headX - 8, headY - 2, 3, 0, Math.PI * 2);
        this.ctx.arc(headX + 8, headY - 2, 3, 0, Math.PI * 2);
        this.ctx.fill();

        this.ctx.shadowColor = 'transparent';

        // Dark energy radiates from body when attacking
        if (isAttacking) {
            this.ctx.strokeStyle = `rgba(255, 50, 50, 0.5)`;
            this.ctx.lineWidth = 2;
            for (let i = 0; i < 6; i++) {
                const angle = (i / 6) * Math.PI * 2 + this.time / 500;
                this.ctx.beginPath();
                this.ctx.moveTo(0, bodyY);
                const px = Math.cos(angle) * 70;
                const py = Math.sin(angle) * 70;
                this.ctx.lineTo(px, bodyY + py);
                this.ctx.stroke();
            }
        }

        // Arms
        this.drawArm(this.ctx, -bodyWidth / 2 - 8, bodyY - 5, enemy.color, isAttacking ? 0.5 : 0, true);
        this.drawArm(this.ctx, bodyWidth / 2 + 8, bodyY - 5, enemy.color, 0, true);

        // Legs
        this.drawLeg(this.ctx, -bodyWidth / 4, bodyY + bodyHeight / 2, enemy.color, true);
        this.drawLeg(this.ctx, bodyWidth / 4, bodyY + bodyHeight / 2, enemy.color, true);

        this.ctx.restore();
    }

    drawArm(ctx, x, y, color, rotation, isEnemy = false) {
        ctx.save();
        ctx.translate(x, y);
        if (rotation) ctx.rotate(rotation);

        const armColor = isEnemy ? this.darken(color, 0.3) : this.lighten(color, 0.5);
        const gradient = ctx.createLinearGradient(0, 0, 0, 30);
        gradient.addColorStop(0, this.lighten(armColor, 1.2));
        gradient.addColorStop(1, armColor);

        ctx.fillStyle = gradient;
        this.roundRect(ctx, -4, 0, 8, 35, 4);
        ctx.fill();

        ctx.strokeStyle = this.darken(color, 0.5);
        ctx.lineWidth = 1;
        this.roundRect(ctx, -4, 0, 8, 35, 4);
        ctx.stroke();

        ctx.restore();
    }

    drawLeg(ctx, x, y, color, isEnemy = false) {
        ctx.save();
        ctx.translate(x, y);

        const legColor = isEnemy ? this.darken(color, 0.5) : this.lighten(color, 0.3);
        const gradient = ctx.createLinearGradient(0, 0, 0, 40);
        gradient.addColorStop(0, legColor);
        gradient.addColorStop(1, this.darken(legColor, 0.3));

        ctx.fillStyle = gradient;
        this.roundRect(ctx, -5, 0, 10, 40, 5);
        ctx.fill();

        ctx.strokeStyle = this.darken(color, 0.6);
        ctx.lineWidth = 1;
        this.roundRect(ctx, -5, 0, 10, 40, 5);
        ctx.stroke();

        ctx.restore();
    }

    // ===== EFFECTS =====

    createSlash(x, y, targetX, targetY) {
        this.slashes.push({
            startX: x,
            startY: y,
            targetX: targetX,
            targetY: targetY,
            progress: 0,
            duration: 300,
            color: 'rgba(255, 150, 100, 0.8)'
        });
    }

    createMagicEffect(x, y, color) {
        for (let i = 0; i < 20; i++) {
            const angle = (i / 20) * Math.PI * 2;
            const speed = 1 + Math.random() * 2;
            this.particles.push({
                x: x,
                y: y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                life: 1,
                color: color,
                type: 'magic'
            });
        }
    }

    createExplosion(x, y, particleCount = 50) {
        for (let i = 0; i < particleCount; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = 2 + Math.random() * 4;
            this.particles.push({
                x: x,
                y: y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                life: 1,
                color: `hsl(${Math.random() * 60 + 20}, 100%, 60%)`,
                type: 'explosion'
            });
        }
    }

    updateParticles() {
        this.particles = this.particles.filter(p => {
            p.x += p.vx;
            p.y += p.vy;
            p.vy += 0.05; // gravity
            p.life -= 0.02;
            return p.life > 0;
        });
    }

    drawParticles() {
        this.particles.forEach(p => {
            this.ctx.fillStyle = p.color.replace(')', `, ${p.life})`).replace('rgba', 'rgba');
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, 3 + Math.random() * 2, 0, Math.PI * 2);
            this.ctx.fill();
        });
    }

    drawSlashes() {
        this.slashes = this.slashes.filter(s => {
            s.progress += 16.67 / s.duration; // 60 FPS
            if (s.progress > 1) return false;

            const x = s.startX + (s.targetX - s.startX) * s.progress;
            const y = s.startY + (s.targetY - s.startY) * s.progress;
            const length = 80 * (1 - Math.abs(s.progress - 0.5) * 2);

            this.ctx.strokeStyle = s.color.replace('0.8', String(0.8 * (1 - s.progress)));
            this.ctx.lineWidth = 8;
            this.ctx.beginPath();
            this.ctx.moveTo(x - 40, y + 40);
            this.ctx.lineTo(x + 40, y - 40);
            this.ctx.stroke();

            return true;
        });
    }

    drawMagicEffects() {
        // Draw magic spirals
    }

    // ===== BACKSTORY (5 SECONDS) =====

    updateBackstory() {
        const backstoryDuration = 5000;

        if (this.time > backstoryDuration) {
            this.phase = 'fight';
            this.time = 0;
            return;
        }

        const progress = this.time / backstoryDuration;
        const scene = Math.floor(progress * 4);

        this.ctx.globalAlpha = 0.7 + Math.sin(this.time / 500) * 0.2;

        if (scene === 0) {
            this.drawBackstoryScene(1, progress * 4);
        } else if (scene === 1) {
            this.drawBackstoryScene(2, (progress * 4) - 1);
        } else if (scene === 2) {
            this.drawBackstoryScene(3, (progress * 4) - 2);
        } else {
            this.drawBackstoryScene(4, (progress * 4) - 3);
        }

        this.ctx.globalAlpha = 1;
    }

    drawBackstoryScene(sceneNum, progress) {
        const x = this.canvas.width * 0.5;
        const y = this.canvas.height * 0.5;

        if (sceneNum === 1) {
            // Beginning
            this.drawHeroCharacter(x - 150, y, 0.6, this.setup.hero, false);
            this.ctx.fillStyle = 'rgba(150, 150, 150, 0.3)';
            this.drawCircle(x - 150, y, 200);

            // Floating memories
            for (let i = 0; i < 5; i++) {
                const px = x - 150 + Math.cos(progress * Math.PI + i) * 120;
                const py = y - 100 + Math.sin(progress * Math.PI * 2 + i) * 100;
                this.ctx.fillStyle = `rgba(255, 200, 100, ${0.3 * (1 - progress)})`;
                this.drawCircle(px, py, 5);
            }
        } else if (sceneNum === 2) {
            // Training
            this.drawHeroCharacter(x - 150, y, 0.8, this.setup.hero, false);

            const energySize = 50 + progress * 50;
            this.ctx.strokeStyle = `rgba(255, 150, 0, ${0.5 * (1 - progress)})`;
            this.ctx.lineWidth = 4;
            this.drawCircle(x - 150, y, energySize);

            // Energy rays
            for (let i = 0; i < 8; i++) {
                const angle = (i / 8) * Math.PI * 2;
                this.ctx.strokeStyle = `rgba(255, 150, 0, ${0.3 * (1 - progress)})`;
                this.ctx.lineWidth = 2;
                this.ctx.beginPath();
                this.ctx.moveTo(x - 150 + Math.cos(angle) * energySize, y + Math.sin(angle) * energySize);
                this.ctx.lineTo(x - 150 + Math.cos(angle) * (energySize + 40), y + Math.sin(angle) * (energySize + 40));
                this.ctx.stroke();
            }
        } else if (sceneNum === 3) {
            // Previous battles
            this.drawHeroCharacter(x - 150, y, 1, this.setup.hero, true);

            for (let i = 0; i < 3; i++) {
                const enemyX = x + 50 + i * 100;
                const enemyAlpha = Math.max(0, 1 - progress);
                this.ctx.globalAlpha = enemyAlpha * 0.5;
                this.drawEnemyCharacter(enemyX, y + 20, 0.7, this.setup.enemy, false);
                this.ctx.globalAlpha = 1;
            }
        } else {
            // Rising power
            const scale = 0.9 + progress * 0.2;
            this.drawHeroCharacter(x - 150, y - progress * 50, scale, this.setup.hero, false);

            // Aura rings
            for (let i = 0; i < 3; i++) {
                const ringSize = 100 + (i * 50) + progress * 100;
                this.ctx.strokeStyle = `rgba(255, 200, 0, ${0.6 * progress})`;
                this.ctx.lineWidth = 4;
                this.drawCircle(x - 150, y, ringSize);
            }

            // Rising light particles
            for (let i = 0; i < 10; i++) {
                const px = x - 150 + (Math.random() - 0.5) * 80;
                const py = y - (progress * 200 + Math.random() * 50);
                this.ctx.fillStyle = `rgba(255, 200, 100, ${0.5 * (1 - progress)})`;
                this.drawCircle(px, py, 3);
            }
        }
    }

    // ===== FIGHT (15-20 SECONDS) =====

    updateFight() {
        const fightDuration = (this.setup.isEpic ? 20000 : 15000) - 5000;

        if (this.time > fightDuration) {
            this.phase = 'victory';
            this.time = 0;
            return;
        }

        const progress = this.time / fightDuration;
        const w = this.canvas.width;
        const h = this.canvas.height;

        // Different phases
        if (progress < 0.2) {
            // Entrance/Clash
            const phaseProgress = progress * 5;
            const heroX = -200 + phaseProgress * (w * 0.35 + 200);
            const enemyX = w + 200 - phaseProgress * (w * 0.35 - (w * 0.75) + 200);

            this.drawHeroCharacter(heroX, h * 0.6, 1.2, this.setup.hero, false);
            this.drawEnemyCharacter(enemyX, h * 0.55, 1.2 * this.setup.enemy.size, this.setup.enemy, false);

            if (phaseProgress > 0.8) {
                this.createExplosion(w * 0.5, h * 0.5, 30);
                const flashAlpha = (phaseProgress - 0.8) * 5;
                this.ctx.fillStyle = `rgba(255, 255, 200, ${Math.min(flashAlpha * 0.3, 0.5)})`;
                this.ctx.fillRect(0, 0, w, h);
            }
        } else if (progress < 0.5) {
            // Exchange
            const phaseProgress = (progress - 0.2) * 3.33;
            const heroX = w * 0.25 + Math.sin(phaseProgress * Math.PI) * 40;
            const enemyX = w * 0.75 - Math.sin(phaseProgress * Math.PI) * 60;

            this.drawHeroCharacter(heroX, h * 0.6, 1.1, this.setup.hero, phaseProgress % 0.5 < 0.25);
            this.drawEnemyCharacter(enemyX, h * 0.55, 1.1 * this.setup.enemy.size, this.setup.enemy, phaseProgress % 0.5 >= 0.25);

            // Attack effects
            if (phaseProgress % 0.5 < 0.25) {
                this.createSlash(heroX + 50, h * 0.5, heroX + 150, h * 0.4);
            }
        } else if (progress < 0.8) {
            // Intense
            const phaseProgress = (progress - 0.5) * 3.33;
            const heroX = w * 0.25 + Math.sin(phaseProgress * Math.PI * 4) * 60;
            const enemyX = w * 0.75 + Math.sin(phaseProgress * Math.PI * 4 + Math.PI) * 80;

            this.drawHeroCharacter(heroX, h * 0.6, 1.2, this.setup.hero, true);
            this.drawEnemyCharacter(enemyX, h * 0.55, 1.2 * this.setup.enemy.size, this.setup.enemy, true);

            this.cameraShakeIntensity = 0.4;

            // Multiple effects
            if (Math.floor(phaseProgress * 10) % 3 === 0) {
                this.createSlash(heroX + 60, h * 0.4, heroX + 160, h * 0.3);
                this.createMagicEffect(enemyX - 60, h * 0.4, 'rgba(100, 150, 255, 0.6)');
            }
        } else {
            // Final strike
            const phaseProgress = (progress - 0.8) * 5;
            const heroX = w * 0.25 + phaseProgress * (w * 0.4);
            const enemyX = w * 0.75 - phaseProgress * (w * 0.25);

            this.drawHeroCharacter(heroX, h * 0.6, 1.3, this.setup.hero, true);
            this.drawEnemyCharacter(enemyX, h * 0.55, 1.3 * this.setup.enemy.size, this.setup.enemy, true);

            this.createSlash(heroX + 100, h * 0.5, heroX + 250, h * 0.3);
            this.cameraShakeIntensity = 0.8 * (1 - phaseProgress);

            if (phaseProgress > 0.7) {
                this.ctx.fillStyle = `rgba(255, 255, 255, ${(phaseProgress - 0.7) * 5})`;
                this.ctx.fillRect(0, 0, w, h);
            }
        }

        // Apply camera shake
        if (this.cameraShakeIntensity > 0) {
            const shake = this.cameraShakeIntensity;
            this.ctx.translate((Math.random() - 0.5) * shake * 20, (Math.random() - 0.5) * shake * 20);
        }
    }

    // ===== VICTORY =====

    updateVictory() {
        const victoryDuration = 3000;

        if (this.time > victoryDuration) {
            return;
        }

        const progress = this.time / victoryDuration;
        const w = this.canvas.width;
        const h = this.canvas.height;

        const heroScale = 1 + progress * 0.4;
        const heroY = h * 0.6 - progress * 150;

        this.drawHeroCharacter(w * 0.5, heroY, heroScale, this.setup.hero, false);

        // Victory glow
        const glowSize = 200 + progress * 400;
        this.ctx.strokeStyle = `rgba(255, 200, 0, ${0.8 * (1 - progress)})`;
        this.ctx.lineWidth = 6;
        this.drawCircle(w * 0.5, heroY, glowSize);

        // Celebration particles
        if (Math.floor(progress * 100) % 3 === 0) {
            this.createExplosion(w * 0.5, heroY, 10);
        }
    }

    // ===== HELPER FUNCTIONS =====

    drawTreeShape(x, y, height, opacity) {
        this.ctx.save();
        this.ctx.globalAlpha = opacity;

        // Trunk
        this.ctx.fillStyle = '#6b4423';
        this.ctx.fillRect(x - height * 0.12, y, height * 0.24, height * 0.35);

        // Foliage (triangle)
        this.ctx.beginPath();
        this.ctx.moveTo(x, y - height * 0.4);
        this.ctx.lineTo(x - height * 0.35, y);
        this.ctx.lineTo(x + height * 0.35, y);
        this.ctx.closePath();
        this.ctx.fill();

        this.ctx.restore();
    }

    drawSmoke(x, y, size) {
        this.ctx.beginPath();
        this.ctx.arc(x - size / 3, y, size / 3, 0, Math.PI * 2);
        this.ctx.arc(x, y - size / 4, size / 2.5, 0, Math.PI * 2);
        this.ctx.arc(x + size / 3, y, size / 3, 0, Math.PI * 2);
        this.ctx.fill();
    }

    drawRock(x, y, size) {
        this.ctx.beginPath();
        for (let i = 0; i < 8; i++) {
            const angle = (i / 8) * Math.PI * 2;
            const r = size * (0.7 + Math.sin(i) * 0.3);
            const px = x + Math.cos(angle) * r;
            const py = y + Math.sin(angle) * r;
            if (i === 0) this.ctx.moveTo(px, py);
            else this.ctx.lineTo(px, py);
        }
        this.ctx.closePath();
        this.ctx.fill();
    }

    drawStormCloud(x, y, size) {
        this.ctx.beginPath();
        this.ctx.arc(x - size / 3, y, size / 3, 0, Math.PI * 2);
        this.ctx.arc(x, y - size / 4, size / 2.5, 0, Math.PI * 2);
        this.ctx.arc(x + size / 3, y, size / 3, 0, Math.PI * 2);
        this.ctx.fill();
    }

    drawCloud(x, y, size) {
        this.ctx.beginPath();
        this.ctx.arc(x - size / 3, y, size / 3, 0, Math.PI * 2);
        this.ctx.arc(x, y - size / 4, size / 2.5, 0, Math.PI * 2);
        this.ctx.arc(x + size / 3, y, size / 3, 0, Math.PI * 2);
        this.ctx.fill();
    }

    drawIsland(x, y, size) {
        this.ctx.beginPath();
        this.ctx.ellipse(x, y, size, size * 0.6, 0, 0, Math.PI * 2);
        this.ctx.fill();
    }

    drawIslandOutline(x, y, size) {
        this.ctx.beginPath();
        this.ctx.ellipse(x, y, size, size * 0.6, 0, 0, Math.PI * 2);
        this.ctx.stroke();
    }

    drawStar(x, y, size) {
        const points = 5;
        const outerRadius = size;
        const innerRadius = size * 0.4;

        this.ctx.beginPath();
        for (let i = 0; i < points * 2; i++) {
            const radius = i % 2 === 0 ? outerRadius : innerRadius;
            const angle = (i / (points * 2)) * Math.PI * 2 - Math.PI / 2;
            const px = x + Math.cos(angle) * radius;
            const py = y + Math.sin(angle) * radius;
            if (i === 0) this.ctx.moveTo(px, py);
            else this.ctx.lineTo(px, py);
        }
        this.ctx.closePath();
        this.ctx.fill();
    }

    drawPerspectiveWall(x, y, width, height, shift) {
        this.ctx.beginPath();
        this.ctx.moveTo(x, y);
        this.ctx.lineTo(x + width + shift * 30, y);
        this.ctx.lineTo(x + width + shift * 30, y + height);
        this.ctx.lineTo(x, y + height);
        this.ctx.closePath();
        this.ctx.fill();
    }

    drawAura(x, y, radius) {
        this.ctx.beginPath();
        this.ctx.arc(x, y, radius, 0, Math.PI * 2);
        this.ctx.stroke();
    }

    drawCircle(x, y, radius) {
        this.ctx.beginPath();
        this.ctx.arc(x, y, radius, 0, Math.PI * 2);
        this.ctx.fill();
    }

    // Utility functions
    roundRect(ctx, x, y, width, height, radius) {
        ctx.beginPath();
        ctx.moveTo(x + radius, y);
        ctx.lineTo(x + width - radius, y);
        ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
        ctx.lineTo(x + width, y + height - radius);
        ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
        ctx.lineTo(x + radius, y + height);
        ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
        ctx.lineTo(x, y + radius);
        ctx.quadraticCurveTo(x, y, x + radius, y);
        ctx.closePath();
    }

    hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : { r: 0, g: 0, b: 0 };
    }

    lighten(hex, factor) {
        const rgb = this.hexToRgb(hex);
        const r = Math.min(255, rgb.r * factor);
        const g = Math.min(255, rgb.g * factor);
        const b = Math.min(255, rgb.b * factor);
        return `rgb(${Math.round(r)}, ${Math.round(g)}, ${Math.round(b)})`;
    }

    darken(hex, factor) {
        const rgb = this.hexToRgb(hex);
        const r = rgb.r / factor;
        const g = rgb.g / factor;
        const b = rgb.b / factor;
        return `rgb(${Math.round(r)}, ${Math.round(g)}, ${Math.round(b)})`;
    }
}

if (typeof window !== 'undefined') {
    window.AnimeBattleSystem = AnimeBattleSystem;
}
