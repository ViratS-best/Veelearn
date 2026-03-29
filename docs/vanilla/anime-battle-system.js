/**
 * ============================================
 * PROFESSIONAL ANIME BATTLE SYSTEM v3
 * ============================================
 * FULL COMBAT CHOREOGRAPHY WITH:
 * - Dynamic character animations (arms, body, reactions)
 * - Weapon swing effects with white column attacks
 * - Hit reactions and pain expressions
 * - Immediate end on completion (no delay)
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
        this.heroHitReaction = 0;
        this.enemyHitReaction = 0;
        this.heroArmSwing = 0;
        this.enemyArmSwing = 0;
        this.isComplete = false;
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

        // Update particles
        this.updateParticles();
        this.drawParticles();
        this.drawSlashes();

        // Decay hit reactions
        this.heroHitReaction *= 0.85;
        this.enemyHitReaction *= 0.85;
        this.heroArmSwing *= 0.92;
        this.enemyArmSwing *= 0.92;

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

        const gradient = this.ctx.createLinearGradient(0, 0, 0, h);
        gradient.addColorStop(0, env.skyColor);
        gradient.addColorStop(1, env.groundColor);
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, w, h);

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

        this.ctx.fillStyle = 'rgba(30, 60, 20, 0.3)';
        for (let i = 0; i < 3; i++) {
            const x = (w * 0.2) + (i * w * 0.3) + Math.sin(this.time / 3000) * 20;
            this.drawTreeShape(x, h * 0.25, 80, 0.3);
        }

        this.ctx.fillStyle = 'rgba(45, 90, 35, 0.5)';
        for (let i = 0; i < 4; i++) {
            const x = (i * w * 0.25) + Math.sin(this.time / 2000 + i) * 10;
            this.drawTreeShape(x, h * 0.45, 120, 0.5);
        }

        this.ctx.fillStyle = env.accent1;
        for (let i = 0; i < 5; i++) {
            const x = (i * w * 0.2);
            this.drawTreeShape(x, h * 0.65, 150, 0.8);
        }

        const mistGradient = this.ctx.createLinearGradient(0, h * 0.7, 0, h);
        mistGradient.addColorStop(0, 'rgba(100, 150, 100, 0)');
        mistGradient.addColorStop(1, 'rgba(50, 80, 50, 0.3)');
        this.ctx.fillStyle = mistGradient;
        this.ctx.fillRect(0, h * 0.7, w, h * 0.3);
    }

    drawVolcanoEnvironment() {
        const w = this.canvas.width;
        const h = this.canvas.height;

        this.ctx.fillStyle = 'rgba(80, 40, 20, 0.3)';
        for (let i = 0; i < 5; i++) {
            const x = (i * w * 0.25) + Math.sin(this.time / 1500 + i) * 40;
            const y = h * 0.2 + Math.cos(this.time / 2000 + i) * 30;
            this.drawSmoke(x, y, 100 + i * 10);
        }

        const glowIntensity = Math.sin(this.time / 800) * 0.2 + 0.6;
        this.ctx.fillStyle = `rgba(255, 100, 0, ${0.15 * glowIntensity})`;
        this.ctx.fillRect(0, h * 0.4, w, h * 0.6);

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

        this.ctx.fillStyle = 'rgba(30, 50, 70, 0.4)';
        for (let i = 0; i < 4; i++) {
            const x = (i * w * 0.3) + Math.sin(this.time / 3000 + i) * 50;
            const y = h * 0.12 + Math.cos(this.time / 4000 + i) * 20;
            this.drawStormCloud(x, y, 120);
        }

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

        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.15)';
        this.ctx.fillRect(0, h * 0.55, w, 20);
    }

    drawCastleEnvironment() {
        const w = this.canvas.width;
        const h = this.canvas.height;

        for (let i = 0; i < 30; i++) {
            const seed = i * 123;
            const x = Math.sin(seed) * w * 0.5 + w * 0.5;
            const y = Math.cos(seed) * h * 0.35 + h * 0.1;
            const brightness = Math.sin(this.time / 800 + seed) * 0.3 + 0.5;
            this.ctx.fillStyle = `rgba(255, 255, 200, ${brightness * 0.6})`;
            this.drawStar(x, y, 3);
        }

        this.ctx.fillStyle = '#5a5a5a';
        this.drawPerspectiveWall(w * 0.1, h * 0.35, w * 0.25, h * 0.55, 0.3);

        this.ctx.fillStyle = '#6a6a6a';
        this.drawPerspectiveWall(w * 0.35, h * 0.3, w * 0.3, h * 0.6, 0.35);

        this.ctx.fillStyle = '#4a4a4a';
        this.drawPerspectiveWall(w * 0.65, h * 0.35, w * 0.25, h * 0.55, 0.3);

        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
        this.ctx.fillRect(0, h * 0.8, w, h * 0.2);
    }

    drawSkyEnvironment() {
        const w = this.canvas.width;
        const h = this.canvas.height;

        for (let i = 0; i < 3; i++) {
            const x = (w * 0.2) + (i * w * 0.35);
            const y = h * 0.2 + (i * 30);
            const size = 100 + i * 20;

            this.ctx.fillStyle = 'rgba(0, 0, 0, 0.15)';
            this.drawIsland(x, y + 20, size);

            this.ctx.fillStyle = '#6b8e23';
            this.drawIsland(x, y, size);

            this.ctx.strokeStyle = `rgba(100, 180, 200, ${0.3 + Math.sin(this.time / 2000 + i) * 0.2})`;
            this.ctx.lineWidth = 3;
            this.drawIslandOutline(x, y, size);
        }

        for (let i = 0; i < 5; i++) {
            const alpha = 0.3 + (i * 0.1);
            this.ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
            const x = (i * w * 0.25) + Math.sin(this.time / 4000 + i) * 30;
            const y = h * 0.15 + (i * 20);
            this.drawCloud(x, y, 80 + i * 10);
        }
    }

    // ===== CHARACTER DRAWING WITH ANIMATIONS =====

    drawHeroCharacter(x, y, scale, hero, attackPhase, hitReaction) {
        this.ctx.save();
        this.ctx.translate(x, y);
        this.ctx.scale(scale, scale);

        // Hit reaction knockback
        if (hitReaction > 0) {
            this.ctx.translate(hitReaction * 15, -hitReaction * 10);
        }

        const headX = 0;
        const headY = -35;
        const bodyY = 0;
        const bodyWidth = 40;
        const bodyHeight = 50;

        // Aura
        if (attackPhase > 0.3) {
            this.ctx.strokeStyle = `rgba(${this.hexToRgb(hero.accent).r}, ${this.hexToRgb(hero.accent).g}, ${this.hexToRgb(hero.accent).b}, ${0.4 * attackPhase})`;
            this.ctx.lineWidth = 8;
            this.drawCircle(0, bodyY, 80);

            this.ctx.strokeStyle = `rgba(${this.hexToRgb(hero.accent).r}, ${this.hexToRgb(hero.accent).g}, ${this.hexToRgb(hero.accent).b}, ${0.2 * attackPhase})`;
            this.ctx.lineWidth = 4;
            this.drawCircle(0, bodyY, 100);
        }

        // Body
        const bodyGradient = this.ctx.createLinearGradient(-bodyWidth / 2, bodyY - bodyHeight / 2, -bodyWidth / 2, bodyY + bodyHeight / 2);
        bodyGradient.addColorStop(0, this.lighten(hero.color, 1.3));
        bodyGradient.addColorStop(0.5, hero.color);
        bodyGradient.addColorStop(1, this.lighten(hero.color, 0.8));
        this.ctx.fillStyle = bodyGradient;
        this.roundRect(this.ctx, -bodyWidth / 2, bodyY - bodyHeight / 2, bodyWidth, bodyHeight, 8);
        this.ctx.fill();

        this.ctx.strokeStyle = this.darken(hero.color, 0.6);
        this.ctx.lineWidth = 2;
        this.roundRect(this.ctx, -bodyWidth / 2, bodyY - bodyHeight / 2, bodyWidth, bodyHeight, 8);
        this.ctx.stroke();

        // Head with pain expression
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

        // Eyes - pain expression if hit
        if (hitReaction > 0.2) {
            // Squinting eyes (pain)
            this.ctx.strokeStyle = '#000';
            this.ctx.lineWidth = 3;
            this.ctx.beginPath();
            this.ctx.arc(headX - 8, headY - 3, 4, 0.2, Math.PI - 0.2);
            this.ctx.stroke();
            this.ctx.beginPath();
            this.ctx.arc(headX + 8, headY - 3, 4, 0.2, Math.PI - 0.2);
            this.ctx.stroke();

            // Pain marks (x marks)
            this.ctx.strokeStyle = 'rgba(255, 0, 0, 0.5)';
            this.ctx.lineWidth = 2;
            this.ctx.beginPath();
            this.ctx.moveTo(headX - 12, headY - 8);
            this.ctx.lineTo(headX - 8, headY - 4);
            this.ctx.moveTo(headX - 8, headY - 8);
            this.ctx.lineTo(headX - 12, headY - 4);
            this.ctx.stroke();
        } else {
            // Normal eyes
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

            this.ctx.fillStyle = '#4dd0ff';
            this.ctx.beginPath();
            this.ctx.arc(headX - 7.5, headY - 2.5, 1.5, 0, Math.PI * 2);
            this.ctx.arc(headX + 8.5, headY - 2.5, 1.5, 0, Math.PI * 2);
            this.ctx.fill();
        }

        // Arms with attack animation
        const armAngle = Math.sin(this.heroArmSwing * Math.PI) * 0.8;
        this.drawHeroArm(this.ctx, -bodyWidth / 2 - 5, bodyY - 10, hero.color, armAngle);
        this.drawHeroArm(this.ctx, bodyWidth / 2 + 5, bodyY - 10, hero.color, 0);

        // Weapon with swing animation
        this.ctx.save();
        const weaponRotation = Math.sin(this.heroArmSwing * Math.PI) * 0.6;
        this.ctx.translate(30, bodyY - 20);
        this.ctx.rotate(weaponRotation);

        // White column attack effect (when swinging)
        if (this.heroArmSwing > 0.4 && this.heroArmSwing < 0.6) {
            const intensity = Math.sin((this.heroArmSwing - 0.4) * Math.PI * 2.5) * 0.8;
            // White column
            this.ctx.fillStyle = `rgba(255, 255, 255, ${0.4 * intensity})`;
            this.ctx.fillRect(-5, -80, 10, 160);

            // Bright inner column
            this.ctx.fillStyle = `rgba(255, 255, 200, ${0.8 * intensity})`;
            this.ctx.fillRect(-2, -70, 4, 140);

            // Glow
            this.ctx.shadowColor = `rgba(255, 255, 200, ${intensity})`;
            this.ctx.shadowBlur = 30;
            this.ctx.fillRect(-5, -80, 10, 160);
            this.ctx.shadowColor = 'transparent';
        }

        // Sword glow
        this.ctx.shadowColor = `rgba(${this.hexToRgb(hero.accent).r}, ${this.hexToRgb(hero.accent).g}, ${this.hexToRgb(hero.accent).b}, 0.6)`;
        this.ctx.shadowBlur = 15;

        this.ctx.strokeStyle = this.lighten(hero.accent, 1.2);
        this.ctx.lineWidth = 6;
        this.ctx.beginPath();
        this.ctx.moveTo(0, 0);
        this.ctx.lineTo(0, -70);
        this.ctx.stroke();

        this.ctx.strokeStyle = hero.accent;
        this.ctx.lineWidth = 3;
        this.ctx.stroke();

        this.ctx.strokeStyle = '#fff';
        this.ctx.lineWidth = 1;
        this.ctx.stroke();

        this.ctx.shadowColor = 'transparent';
        this.ctx.restore();

        // Legs
        this.drawLeg(this.ctx, -bodyWidth / 4, bodyY + bodyHeight / 2, hero.color);
        this.drawLeg(this.ctx, bodyWidth / 4, bodyY + bodyHeight / 2, hero.color);

        this.ctx.restore();
    }

    drawEnemyCharacter(x, y, scale, enemy, attackPhase, hitReaction) {
        this.ctx.save();
        this.ctx.translate(x, y);
        this.ctx.scale(scale, scale);

        // Hit reaction knockback
        if (hitReaction > 0) {
            this.ctx.translate(-hitReaction * 20, -hitReaction * 15);
        }

        const headX = 0;
        const headY = -35;
        const bodyY = 0;
        const bodyWidth = 45;
        const bodyHeight = 55;

        // Dark aura
        this.ctx.strokeStyle = `rgba(${this.hexToRgb(enemy.accent).r}, 50, 50, ${0.3 + attackPhase * 0.3})`;
        this.ctx.lineWidth = 10;
        this.drawCircle(0, bodyY, 90);

        if (attackPhase > 0.4) {
            this.ctx.strokeStyle = `rgba(${this.hexToRgb(enemy.accent).r}, 100, 100, 0.2)`;
            this.ctx.lineWidth = 6;
            this.drawCircle(0, bodyY, 120);
        }

        // Body
        const bodyGradient = this.ctx.createLinearGradient(-bodyWidth / 2, bodyY - bodyHeight / 2, -bodyWidth / 2, bodyY + bodyHeight / 2);
        bodyGradient.addColorStop(0, this.lighten(enemy.color, 0.9));
        bodyGradient.addColorStop(0.5, enemy.color);
        bodyGradient.addColorStop(1, this.darken(enemy.color, 0.4));
        this.ctx.fillStyle = bodyGradient;
        this.roundRect(this.ctx, -bodyWidth / 2, bodyY - bodyHeight / 2, bodyWidth, bodyHeight, 8);
        this.ctx.fill();

        this.ctx.strokeStyle = this.darken(enemy.color, 1.2);
        this.ctx.lineWidth = 3;
        this.roundRect(this.ctx, -bodyWidth / 2, bodyY - bodyHeight / 2, bodyWidth, bodyHeight, 8);
        this.ctx.stroke();

        // Head
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

        // Eyes - pain expression if hit
        this.ctx.shadowColor = 'rgba(255, 100, 100, 0.8)';
        this.ctx.shadowBlur = 20;

        if (hitReaction > 0.2) {
            // Damage/pain state
            this.ctx.fillStyle = '#ff6666';
            this.ctx.beginPath();
            this.ctx.arc(headX - 8, headY - 2, 6, 0, Math.PI * 2);
            this.ctx.arc(headX + 8, headY - 2, 6, 0, Math.PI * 2);
            this.ctx.fill();

            this.ctx.fillStyle = '#ffff00';
            this.ctx.beginPath();
            this.ctx.arc(headX - 8, headY - 2, 3, 0, Math.PI * 2);
            this.ctx.arc(headX + 8, headY - 2, 3, 0, Math.PI * 2);
            this.ctx.fill();

            // Pain X eyes
            this.ctx.strokeStyle = '#fff';
            this.ctx.lineWidth = 2;
            this.ctx.beginPath();
            this.ctx.moveTo(headX - 11, headY - 5);
            this.ctx.lineTo(headX - 5, headY + 1);
            this.ctx.moveTo(headX - 5, headY - 5);
            this.ctx.lineTo(headX - 11, headY + 1);
            this.ctx.stroke();
            this.ctx.beginPath();
            this.ctx.moveTo(headX + 5, headY - 5);
            this.ctx.lineTo(headX + 11, headY + 1);
            this.ctx.moveTo(headX + 11, headY - 5);
            this.ctx.lineTo(headX + 5, headY + 1);
            this.ctx.stroke();
        } else {
            // Normal angry eyes
            this.ctx.fillStyle = '#ff4444';
            this.ctx.beginPath();
            this.ctx.arc(headX - 8, headY - 2, 6, 0, Math.PI * 2);
            this.ctx.arc(headX + 8, headY - 2, 6, 0, Math.PI * 2);
            this.ctx.fill();

            this.ctx.fillStyle = '#ffff00';
            this.ctx.beginPath();
            this.ctx.arc(headX - 8, headY - 2, 3, 0, Math.PI * 2);
            this.ctx.arc(headX + 8, headY - 2, 3, 0, Math.PI * 2);
            this.ctx.fill();
        }

        this.ctx.shadowColor = 'transparent';

        // Dark energy attacks
        if (attackPhase > 0.4) {
            this.ctx.strokeStyle = `rgba(255, 50, 50, ${0.5 * attackPhase})`;
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

        // Arms with attack animation
        const armAngle = Math.sin(this.enemyArmSwing * Math.PI) * 0.9;
        this.drawEnemyArm(this.ctx, -bodyWidth / 2 - 8, bodyY - 5, enemy.color, armAngle);
        this.drawEnemyArm(this.ctx, bodyWidth / 2 + 8, bodyY - 5, enemy.color, 0);

        // Legs
        this.drawLeg(this.ctx, -bodyWidth / 4, bodyY + bodyHeight / 2, enemy.color, true);
        this.drawLeg(this.ctx, bodyWidth / 4, bodyY + bodyHeight / 2, enemy.color, true);

        this.ctx.restore();
    }

    drawHeroArm(ctx, x, y, color, rotation) {
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(rotation);

        const armColor = this.lighten(color, 0.5);
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

    drawEnemyArm(ctx, x, y, color, rotation) {
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(rotation);

        const armColor = this.darken(color, 0.3);
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
            p.vy += 0.05;
            p.life -= 0.02;
            return p.life > 0;
        });
    }

    drawParticles() {
        this.particles.forEach(p => {
            const alpha = Math.max(0, p.life);
            const color = p.color.includes('hsl') ? p.color : p.color;
            this.ctx.fillStyle = p.color.replace(')', `, ${alpha})`).replace('rgba', 'rgba');
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, 3 + Math.random() * 2, 0, Math.PI * 2);
            this.ctx.fill();
        });
    }

    drawSlashes() {
        this.slashes = this.slashes.filter(s => {
            s.progress += 16.67 / s.duration;
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

    // ===== BACKSTORY =====

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
            this.drawHeroCharacter(x - 150, y, 0.6, this.setup.hero, 0, 0);
            this.ctx.fillStyle = 'rgba(150, 150, 150, 0.3)';
            this.drawCircle(x - 150, y, 200);

            for (let i = 0; i < 5; i++) {
                const px = x - 150 + Math.cos(progress * Math.PI + i) * 120;
                const py = y - 100 + Math.sin(progress * Math.PI * 2 + i) * 100;
                this.ctx.fillStyle = `rgba(255, 200, 100, ${0.3 * (1 - progress)})`;
                this.drawCircle(px, py, 5);
            }
        } else if (sceneNum === 2) {
            this.drawHeroCharacter(x - 150, y, 0.8, this.setup.hero, progress, 0);

            const energySize = 50 + progress * 50;
            this.ctx.strokeStyle = `rgba(255, 150, 0, ${0.5 * (1 - progress)})`;
            this.ctx.lineWidth = 4;
            this.drawCircle(x - 150, y, energySize);

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
            this.drawHeroCharacter(x - 150, y, 1, this.setup.hero, 0.7, 0);

            for (let i = 0; i < 3; i++) {
                const enemyX = x + 50 + i * 100;
                const enemyAlpha = Math.max(0, 1 - progress);
                this.ctx.globalAlpha = enemyAlpha * 0.5;
                this.drawEnemyCharacter(enemyX, y + 20, 0.7, this.setup.enemy, 0, 0);
                this.ctx.globalAlpha = 1;
            }
        } else {
            const scale = 0.9 + progress * 0.2;
            this.drawHeroCharacter(x - 150, y - progress * 50, scale, this.setup.hero, 0, 0);

            for (let i = 0; i < 3; i++) {
                const ringSize = 100 + (i * 50) + progress * 100;
                this.ctx.strokeStyle = `rgba(255, 200, 0, ${0.6 * progress})`;
                this.ctx.lineWidth = 4;
                this.drawCircle(x - 150, y, ringSize);
            }

            for (let i = 0; i < 10; i++) {
                const px = x - 150 + (Math.random() - 0.5) * 80;
                const py = y - (progress * 200 + Math.random() * 50);
                this.ctx.fillStyle = `rgba(255, 200, 100, ${0.5 * (1 - progress)})`;
                this.drawCircle(px, py, 3);
            }
        }
    }

    // ===== FIGHT =====

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

        // Combat choreography
        if (progress < 0.15) {
            // Entrance
            const phaseProgress = progress * 6.67;
            const heroX = -200 + phaseProgress * (w * 0.35 + 200);
            const enemyX = w + 200 - phaseProgress * (w * 0.35 - (w * 0.75) + 200);

            this.drawHeroCharacter(heroX, h * 0.6, 1.2, this.setup.hero, 0, 0);
            this.drawEnemyCharacter(enemyX, h * 0.55, 1.2 * this.setup.enemy.size, this.setup.enemy, 0, 0);

            if (phaseProgress > 0.8) {
                this.createExplosion(w * 0.5, h * 0.5, 30);
                const flashAlpha = (phaseProgress - 0.8) * 5;
                this.ctx.fillStyle = `rgba(255, 255, 200, ${Math.min(flashAlpha * 0.3, 0.5)})`;
                this.ctx.fillRect(0, 0, w, h);
            }
        } else if (progress < 0.4) {
            // Hero attacks
            const phaseProgress = (progress - 0.15) * 3.33;
            const heroX = w * 0.25;
            const enemyX = w * 0.75 - phaseProgress * 40;

            this.heroArmSwing = phaseProgress % 0.5;
            this.drawHeroCharacter(heroX, h * 0.6, 1.1, this.setup.hero, phaseProgress, 0);
            this.drawEnemyCharacter(enemyX, h * 0.55, 1.1 * this.setup.enemy.size, this.setup.enemy, 0, Math.max(0, phaseProgress - 0.4));

            if (phaseProgress > 0.4 && phaseProgress < 0.6) {
                this.createSlash(heroX + 50, h * 0.5, enemyX - 20, h * 0.4);
                this.createExplosion(enemyX - 20, h * 0.4, 15);
            }

            if (phaseProgress > 0.4) {
                this.enemyHitReaction = Math.max(this.enemyHitReaction, (phaseProgress - 0.4) * 2.5);
                this.cameraShakeIntensity = 0.3;
            }
        } else if (progress < 0.65) {
            // Enemy counter
            const phaseProgress = (progress - 0.4) * 4;
            const heroX = w * 0.25 + phaseProgress * 30;
            const enemyX = w * 0.75;

            this.enemyArmSwing = phaseProgress % 0.5;
            this.drawHeroCharacter(heroX, h * 0.6, 1.1, this.setup.hero, 0, Math.max(0, phaseProgress - 0.4));
            this.drawEnemyCharacter(enemyX, h * 0.55, 1.1 * this.setup.enemy.size, this.setup.enemy, phaseProgress, 0);

            if (phaseProgress > 0.4 && phaseProgress < 0.6) {
                this.createExplosion(heroX + 30, h * 0.5, 15);
            }

            if (phaseProgress > 0.4) {
                this.heroHitReaction = Math.max(this.heroHitReaction, (phaseProgress - 0.4) * 2.5);
                this.cameraShakeIntensity = 0.3;
            }
        } else if (progress < 0.85) {
            // Intense rapid combat
            const phaseProgress = (progress - 0.65) * 4;
            const heroX = w * 0.25 + Math.sin(phaseProgress * Math.PI * 6) * 40;
            const enemyX = w * 0.75 - Math.sin(phaseProgress * Math.PI * 6) * 50;

            this.heroArmSwing = phaseProgress % 0.3;
            this.enemyArmSwing = (phaseProgress + 0.15) % 0.3;

            this.drawHeroCharacter(heroX, h * 0.6, 1.2, this.setup.hero, 0.8, this.enemyHitReaction);
            this.drawEnemyCharacter(enemyX, h * 0.55, 1.2 * this.setup.enemy.size, this.setup.enemy, 0.8, this.heroHitReaction);

            if (Math.floor(phaseProgress * 20) % 4 === 0) {
                this.createExplosion(enemyX, h * 0.5, 10);
            }
            if (Math.floor(phaseProgress * 20) % 4 === 2) {
                this.createExplosion(heroX, h * 0.5, 10);
            }

            this.cameraShakeIntensity = 0.5;
        } else {
            // Final strike
            const phaseProgress = (progress - 0.85) * 6.67;
            const heroX = w * 0.25 + phaseProgress * (w * 0.4);
            const enemyX = w * 0.75 - phaseProgress * (w * 0.25);

            this.heroArmSwing = Math.min(1, phaseProgress * 1.5);
            this.drawHeroCharacter(heroX, h * 0.6, 1.3, this.setup.hero, 1, 0);
            this.drawEnemyCharacter(enemyX, h * 0.55, 1.3 * this.setup.enemy.size, this.setup.enemy, 0.5, Math.max(0, (phaseProgress - 0.5) * 2));

            this.createSlash(heroX + 100, h * 0.5, enemyX - 20, h * 0.4);
            this.createExplosion(enemyX, h * 0.5, 30);

            this.cameraShakeIntensity = 0.8 * (1 - phaseProgress);

            if (phaseProgress > 0.7) {
                this.ctx.fillStyle = `rgba(255, 255, 255, ${(phaseProgress - 0.7) * 5})`;
                this.ctx.fillRect(0, 0, w, h);
            }
        }

        // Camera shake
        if (this.cameraShakeIntensity > 0) {
            const shake = this.cameraShakeIntensity;
            this.ctx.translate((Math.random() - 0.5) * shake * 20, (Math.random() - 0.5) * shake * 20);
        }
    }

    // ===== VICTORY =====

    updateVictory() {
        const victoryDuration = 2000; // Reduced from 3000 for faster completion

        if (this.time > victoryDuration) {
            this.isComplete = true;
            return;
        }

        const progress = this.time / victoryDuration;
        const w = this.canvas.width;
        const h = this.canvas.height;

        const heroScale = 1 + progress * 0.4;
        const heroY = h * 0.6 - progress * 150;

        this.drawHeroCharacter(w * 0.5, heroY, heroScale, this.setup.hero, 1, 0);

        const glowSize = 200 + progress * 400;
        this.ctx.strokeStyle = `rgba(255, 200, 0, ${0.8 * (1 - progress)})`;
        this.ctx.lineWidth = 6;
        this.drawCircle(w * 0.5, heroY, glowSize);

        if (Math.floor(progress * 100) % 3 === 0) {
            this.createExplosion(w * 0.5, heroY, 10);
        }
    }

    // ===== HELPERS =====

    drawTreeShape(x, y, height, opacity) {
        this.ctx.save();
        this.ctx.globalAlpha = opacity;

        this.ctx.fillStyle = '#6b4423';
        this.ctx.fillRect(x - height * 0.12, y, height * 0.24, height * 0.35);

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

    drawCircle(x, y, radius) {
        this.ctx.beginPath();
        this.ctx.arc(x, y, radius, 0, Math.PI * 2);
        this.ctx.fill();
    }

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
