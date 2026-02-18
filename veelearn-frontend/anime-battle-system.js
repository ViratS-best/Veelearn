/**
 * ============================================
 * PROFESSIONAL ANIME-STYLE BATTLE SYSTEM
 * ============================================
 * 
 * This module provides a complete professional battle animation system with:
 * - Drawn character rendering (canvas-based)
 * - 5-second backstory montage (no text, animated character life)
 * - 15-20 second epic anime fight
 * - Camera shake effects
 * - Perspective-shifting backgrounds
 * - No HUD elements (zero UI clutter)
 * 
 * Integration:
 * 1. Include this file in index.html BEFORE script.js
 * 2. Call initializeAnimeSystemBattle() from createBattleScene()
 */

class AnimeBattleSystem {
    constructor(setup) {
        this.setup = setup;
        this.canvas = null;
        this.ctx = null;
        this.animationFrame = null;
        this.time = 0;
        this.phase = 'backstory'; // 'backstory' -> 'fight' -> 'victory'
        this.cameraShakeIntensity = 0;
        this.backgroundPerspective = 0; // 0-100 for parallax
    }

    /**
     * Initialize the anime battle system
     */
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
        
        // Handle window resize
        window.addEventListener('resize', () => this.handleResize());
    }

    handleResize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    /**
     * Main animation loop
     */
    animate(deltaTime) {
        this.time += deltaTime;

        // Clear with environment background
        this.drawEnvironmentBackground();

        if (this.phase === 'backstory') {
            this.updateBackstory();
        } else if (this.phase === 'fight') {
            this.updateFight();
        } else if (this.phase === 'victory') {
            this.updateVictory();
        }

        // Apply camera shake
        if (this.cameraShakeIntensity > 0) {
            this.cameraShakeIntensity -= 0.01;
        }
    }

    /**
     * Draw the perspective-shifting background
     */
    drawEnvironmentBackground() {
        const env = this.setup.environment;
        const w = this.canvas.width;
        const h = this.canvas.height;

        // Draw environment-specific background
        if (env.id === 'forest') {
            this.drawForestBackground();
        } else if (env.id === 'volcano') {
            this.drawVolcanoBackground();
        } else if (env.id === 'ocean') {
            this.drawOceanBackground();
        } else if (env.id === 'castle') {
            this.drawCastleBackground();
        } else if (env.id === 'sky') {
            this.drawSkyBackground();
        }
    }

    drawForestBackground() {
        const w = this.canvas.width;
        const h = this.canvas.height;
        const env = this.setup.environment;

        // Sky with gradient
        const skyGradient = this.ctx.createLinearGradient(0, 0, 0, h * 0.4);
        skyGradient.addColorStop(0, '#3a6b35');
        skyGradient.addColorStop(1, '#2d5016');
        this.ctx.fillStyle = skyGradient;
        this.ctx.fillRect(0, 0, w, h * 0.4);

        // Ground with subtle perspective shift
        const perspective = Math.sin(this.time / 2000) * 10;
        this.ctx.fillStyle = env.groundColor;
        this.ctx.fillRect(0, h * 0.4, w, h * 0.6);

        // Distant trees (parallax)
        this.ctx.fillStyle = 'rgba(29, 53, 13, 0.4)';
        for (let i = 0; i < 3; i++) {
            const treeX = (w * 0.25) + (i * w * 0.25) + perspective * 5;
            this.drawTreeShape(treeX, h * 0.35, 40);
        }

        // Mid-ground trees
        this.ctx.fillStyle = 'rgba(45, 106, 79, 0.6)';
        for (let i = 0; i < 5; i++) {
            const treeX = (i * w * 0.2) + perspective * 2;
            this.drawTreeShape(treeX, h * 0.5, 80);
        }

        // Foreground trees
        this.ctx.fillStyle = 'rgba(82, 183, 136, 0.8)';
        for (let i = 0; i < 7; i++) {
            const treeX = (i * w * 0.15) - perspective;
            this.drawTreeShape(treeX, h * 0.65, 120);
        }

        // Ground shadows for depth
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
        this.ctx.fillRect(0, h * 0.8, w, h * 0.2);
    }

    drawVolcanoBackground() {
        const w = this.canvas.width;
        const h = this.canvas.height;

        // Lava sky with glow
        const skyGradient = this.ctx.createLinearGradient(0, 0, 0, h * 0.3);
        skyGradient.addColorStop(0, '#5c2e1a');
        skyGradient.addColorStop(1, '#8b3a1a');
        this.ctx.fillStyle = skyGradient;
        this.ctx.fillRect(0, 0, w, h * 0.3);

        // Smoke/ash particles
        this.ctx.fillStyle = 'rgba(100, 50, 30, 0.3)';
        for (let i = 0; i < 8; i++) {
            const x = (i * w * 0.15) + Math.sin(this.time / 1000 + i) * 50;
            const y = Math.cos(this.time / 2000 + i) * 30 + h * 0.15;
            this.drawCircle(x, y, 30, true);
        }

        // Lava ground
        const groundGradient = this.ctx.createLinearGradient(0, h * 0.3, 0, h);
        groundGradient.addColorStop(0, '#ff4500');
        groundGradient.addColorStop(0.5, '#8b0000');
        groundGradient.addColorStop(1, '#5c0000');
        this.ctx.fillStyle = groundGradient;
        this.ctx.fillRect(0, h * 0.3, w, h * 0.7);

        // Lava glow pulses
        const glowIntensity = Math.sin(this.time / 500) * 0.3 + 0.7;
        this.ctx.fillStyle = `rgba(255, 100, 0, ${0.2 * glowIntensity})`;
        this.ctx.fillRect(0, h * 0.3, w, h * 0.7);

        // Volcanic rocks
        this.ctx.fillStyle = '#4a2a1a';
        for (let i = 0; i < 4; i++) {
            const x = (i * w * 0.25) + w * 0.1;
            const y = h * 0.7;
            this.drawPolygon(x, y, 50, 6);
        }
    }

    drawOceanBackground() {
        const w = this.canvas.width;
        const h = this.canvas.height;

        // Storm sky
        const skyGradient = this.ctx.createLinearGradient(0, 0, 0, h * 0.5);
        skyGradient.addColorStop(0, '#0a3d62');
        skyGradient.addColorStop(1, '#1c5aa0');
        this.ctx.fillStyle = skyGradient;
        this.ctx.fillRect(0, 0, w, h * 0.5);

        // Dark clouds
        this.ctx.fillStyle = 'rgba(20, 40, 60, 0.4)';
        for (let i = 0; i < 4; i++) {
            const cloudX = (i * w * 0.3) + Math.sin(this.time / 3000 + i) * 50;
            this.drawCloud(cloudX, h * 0.15, 100);
        }

        // Ocean
        const oceanGradient = this.ctx.createLinearGradient(0, h * 0.5, 0, h);
        oceanGradient.addColorStop(0, '#1c5aa0');
        oceanGradient.addColorStop(1, '#0a3d62');
        this.ctx.fillStyle = oceanGradient;
        this.ctx.fillRect(0, h * 0.5, w, h * 0.5);

        // Wave lines
        this.ctx.strokeStyle = 'rgba(93, 173, 226, 0.3)';
        this.ctx.lineWidth = 2;
        for (let i = 0; i < 3; i++) {
            this.ctx.beginPath();
            const waveOffset = (this.time / 500) % (2 * Math.PI);
            const baseY = h * 0.5 + (i * 40);
            for (let x = 0; x <= w; x += 20) {
                const y = baseY + Math.sin((x / 100) + waveOffset) * 15;
                if (x === 0) this.ctx.moveTo(x, y);
                else this.ctx.lineTo(x, y);
            }
            this.ctx.stroke();
        }

        // Foam
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
        this.ctx.fillRect(0, h * 0.5 - 5, w, 10);
    }

    drawCastleBackground() {
        const w = this.canvas.width;
        const h = this.canvas.height;

        // Dark sky with stars
        this.ctx.fillStyle = '#2a2a2a';
        this.ctx.fillRect(0, 0, w, h * 0.5);

        // Stars
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
        for (let i = 0; i < 20; i++) {
            const x = Math.sin(i * 123) * w * 0.5 + w * 0.5;
            const y = Math.cos(i * 456) * h * 0.25 + h * 0.1;
            const size = Math.sin(this.time / 1000 + i) * 2 + 2;
            this.drawCircle(x, y, size, true);
        }

        // Ruined castle walls
        this.ctx.fillStyle = '#4a4a4a';
        this.drawRectWithPerspective(0, h * 0.4, w * 0.3, h * 0.6, 0.3);

        this.ctx.fillStyle = '#5a5a5a';
        this.drawRectWithPerspective(w * 0.4, h * 0.35, w * 0.2, h * 0.65, 0.35);

        this.ctx.fillStyle = '#3a3a3a';
        this.drawRectWithPerspective(w * 0.7, h * 0.4, w * 0.3, h * 0.6, 0.3);

        // Ground
        this.ctx.fillStyle = '#2a2a2a';
        this.ctx.fillRect(0, h, w, 0);
    }

    drawSkyBackground() {
        const w = this.canvas.width;
        const h = this.canvas.height;

        // Sky gradient (dawn colors)
        const skyGradient = this.ctx.createLinearGradient(0, 0, 0, h);
        skyGradient.addColorStop(0, '#4a90e2');
        skyGradient.addColorStop(0.5, '#87ceeb');
        skyGradient.addColorStop(1, '#87ceeb');
        this.ctx.fillStyle = skyGradient;
        this.ctx.fillRect(0, 0, w, h);

        // Floating islands in perspective
        this.ctx.fillStyle = 'rgba(100, 180, 200, 0.4)';
        this.drawFloatingIsland(w * 0.1, h * 0.2, 60, 0.4);
        this.drawFloatingIsland(w * 0.8, h * 0.25, 50, 0.45);

        // Clouds
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        for (let i = 0; i < 5; i++) {
            const cloudX = (i * w * 0.25) + Math.sin(this.time / 4000 + i) * 30;
            this.drawCloud(cloudX, h * 0.15 + i * 20, 80 + i * 10);
        }
    }

    /**
     * 5-second backstory montage
     */
    updateBackstory() {
        const backstoryDuration = 5000;
        const hero = this.setup.hero;

        if (this.time > backstoryDuration) {
            this.phase = 'fight';
            this.time = 0;
            return;
        }

        const progress = this.time / backstoryDuration;
        const scene = Math.floor(progress * 4); // 4 scenes in 5 seconds

        this.ctx.save();
        this.ctx.globalAlpha = 0.6 + Math.sin(this.time / 500) * 0.2; // Pulsing effect

        if (scene === 0) {
            // Scene 1: Character's humble beginning (0-1.25s)
            this.drawBackstoryScene1(progress * 4);
        } else if (scene === 1) {
            // Scene 2: Training / Growth (1.25-2.5s)
            this.drawBackstoryScene2((progress * 4) - 1);
        } else if (scene === 2) {
            // Scene 3: Previous battles / Trials (2.5-3.75s)
            this.drawBackstoryScene3((progress * 4) - 2);
        } else {
            // Scene 4: Final preparation / Rising power (3.75-5s)
            this.drawBackstoryScene4((progress * 4) - 3);
        }

        this.ctx.restore();

        // Fade to next phase
        if (progress > 0.9) {
            this.ctx.fillStyle = `rgba(0, 0, 0, ${(progress - 0.9) * 10})`;
            this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        }
    }

    drawBackstoryScene1(progress) {
        // Young hero in village/home setting
        const x = this.canvas.width * 0.5;
        const y = this.canvas.height * 0.5;

        // Draw smaller, younger version of hero
        this.drawHeroCharacter(x - 100, y, 0.6, this.setup.hero, false);

        // Surrounding environment (hint of home)
        this.ctx.fillStyle = 'rgba(100, 100, 100, 0.3)';
        this.ctx.fillRect(x - 200, y - 150, 400, 300);

        // Floating particles (memories)
        for (let i = 0; i < 5; i++) {
            const px = x - 100 + Math.cos(progress * Math.PI + i) * 100;
            const py = y - 100 + Math.sin(progress * Math.PI * 2 + i) * 80;
            this.ctx.fillStyle = `rgba(255, 200, 100, ${0.3 * (1 - progress)})`;
            this.drawCircle(px, py, 5, true);
        }
    }

    drawBackstoryScene2(progress) {
        // Training montage
        const x = this.canvas.width * 0.5;
        const y = this.canvas.height * 0.5;

        // Draw hero in training pose
        this.drawHeroCharacter(x - 100, y, 0.8, this.setup.hero, false);
        
        // Energy/power visualization
        const energyX = x - 100;
        const energyY = y;
        const energySize = 50 + progress * 30;
        
        this.ctx.strokeStyle = `rgba(255, 150, 0, ${0.5 * (1 - progress)})`;
        this.ctx.lineWidth = 3;
        this.drawCircle(energyX, energyY, energySize, false);
        
        // Radiating energy lines
        for (let i = 0; i < 8; i++) {
            const angle = (i / 8) * Math.PI * 2 + progress * Math.PI;
            const x1 = energyX + Math.cos(angle) * energySize;
            const y1 = energyY + Math.sin(angle) * energySize;
            const x2 = energyX + Math.cos(angle) * (energySize + 30);
            const y2 = energyY + Math.sin(angle) * (energySize + 30);
            
            this.ctx.strokeStyle = `rgba(255, 150, 0, ${0.3 * (1 - progress)})`;
            this.ctx.beginPath();
            this.ctx.moveTo(x1, y1);
            this.ctx.lineTo(x2, y2);
            this.ctx.stroke();
        }
    }

    drawBackstoryScene3(progress) {
        // Previous battles
        const x = this.canvas.width * 0.5;
        const y = this.canvas.height * 0.5;

        // Hero in combat stance
        this.drawHeroCharacter(x - 100, y, 1, this.setup.hero, true);
        
        // Enemy silhouettes
        for (let i = 0; i < 3; i++) {
            const enemyX = x + 100 + i * 80;
            const enemyY = y + 20;
            const enemyAlpha = Math.max(0, 1 - progress);
            
            this.ctx.fillStyle = `rgba(100, 0, 0, ${0.4 * enemyAlpha})`;
            this.drawEnemyCharacter(enemyX, enemyY, 0.7, this.setup.enemy, false);
        }

        // Slash effects
        for (let i = 0; i < 4; i++) {
            const slashX = x - 50 + Math.random() * 200;
            const slashY = y - 50 + Math.random() * 200;
            const slashAlpha = Math.sin(progress * Math.PI) * 0.5;
            
            this.ctx.strokeStyle = `rgba(255, 100, 100, ${slashAlpha})`;
            this.ctx.lineWidth = 4;
            this.ctx.beginPath();
            this.ctx.moveTo(slashX, slashY);
            this.ctx.lineTo(slashX + 40, slashY + 40);
            this.ctx.stroke();
        }
    }

    drawBackstoryScene4(progress) {
        // Final preparation - rising power
        const x = this.canvas.width * 0.5;
        const y = this.canvas.height * 0.5;
        const scale = 0.9 + progress * 0.15;

        // Hero standing tall
        this.drawHeroCharacter(x - 100, y, scale, this.setup.hero, false);

        // Powerful aura
        const auraSize = 150 + progress * 100;
        this.ctx.strokeStyle = `rgba(255, 200, 0, ${0.6 * progress})`;
        this.ctx.lineWidth = 5;
        this.drawCircle(x - 100, y, auraSize, false);

        // Multiple aura rings
        for (let i = 0; i < 3; i++) {
            const ringSize = auraSize * (0.7 - i * 0.2) + progress * 50;
            this.ctx.strokeStyle = `rgba(255, 150, 0, ${0.3 * progress})`;
            this.ctx.lineWidth = 2;
            this.drawCircle(x - 100, y, ringSize, false);
        }

        // Light particles streaming upward
        for (let i = 0; i < 10; i++) {
            const px = x - 100 + (Math.random() - 0.5) * 100;
            const py = y - (progress * 150 + Math.random() * 50);
            this.ctx.fillStyle = `rgba(255, 200, 100, ${0.5 * (1 - progress)})`;
            this.drawCircle(px, py, 3 + Math.random() * 3, true);
        }
    }

    /**
     * Epic 15-20 second anime fight
     */
    updateFight() {
        const hero = this.setup.hero;
        const enemy = this.setup.enemy;
        const fightDuration = (this.setup.isEpic ? 20000 : 15000) - 5000; // Subtract backstory time
        
        if (this.time > fightDuration) {
            this.phase = 'victory';
            this.time = 0;
            return;
        }

        const progress = this.time / fightDuration;
        
        // Different fight phases
        if (progress < 0.2) {
            // Phase 1: Entrance/Clash (0-20%)
            this.drawFightPhase1(progress * 5);
        } else if (progress < 0.5) {
            // Phase 2: Exchange (20-50%)
            this.drawFightPhase2((progress - 0.2) * 3.33);
        } else if (progress < 0.8) {
            // Phase 3: Intense combat (50-80%)
            this.drawFightPhase3((progress - 0.5) * 3.33);
        } else {
            // Phase 4: Final strike (80-100%)
            this.drawFightPhase4((progress - 0.8) * 5);
        }

        // Screen shake during combat
        if (progress > 0.15) {
            this.cameraShakeIntensity = 0.3 * Math.sin(this.time / 100);
        }
    }

    drawFightPhase1(progress) {
        // Hero entrance from left, enemy from right
        const w = this.canvas.width;
        const h = this.canvas.height;
        const heroStartX = -200;
        const heroEndX = w * 0.25;
        const enemyStartX = w + 200;
        const enemyEndX = w * 0.75;

        const heroX = heroStartX + (heroEndX - heroStartX) * progress;
        const enemyX = enemyStartX - (enemyStartX - enemyEndX) * progress;

        this.drawHeroCharacter(heroX, h * 0.6, 1.2, this.setup.hero, false);
        this.drawEnemyCharacter(enemyX, h * 0.55, 1.2 * this.setup.enemy.size, this.setup.enemy, false);

        // Clash effect
        if (progress > 0.8) {
            const clashIntensity = (progress - 0.8) * 5;
            this.ctx.fillStyle = `rgba(255, 255, 200, ${clashIntensity * 0.3})`;
            this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

            // Light burst
            this.drawLightBurst(w * 0.5, h * 0.5, 200 * clashIntensity);
        }
    }

    drawFightPhase2(progress) {
        // Exchange of blows
        const w = this.canvas.width;
        const h = this.canvas.height;
        const heroX = w * 0.25 + Math.sin(progress * Math.PI) * 30;
        const enemyX = w * 0.75 - Math.sin(progress * Math.PI) * 40;

        const isHeroAttacking = Math.floor(progress * 4) % 2 === 0;

        this.drawHeroCharacter(heroX, h * 0.6, 1.1, this.setup.hero, isHeroAttacking);
        this.drawEnemyCharacter(enemyX, h * 0.55, 1.1 * this.setup.enemy.size, this.setup.enemy, !isHeroAttacking);

        // Attack effects
        if (isHeroAttacking && progress % 0.5 < 0.25) {
            this.drawSlashEffect(heroX + 100, h * 0.5, progress * 200);
        }
        if (!isHeroAttacking && progress % 0.5 < 0.25) {
            this.drawMagicEffect(enemyX - 100, h * 0.5, progress * 200);
        }
    }

    drawFightPhase3(progress) {
        // Intense combat with rapid exchanges
        const w = this.canvas.width;
        const h = this.canvas.height;
        const heroX = w * 0.25 + Math.sin(progress * Math.PI * 4) * 50;
        const enemyX = w * 0.75 + Math.sin(progress * Math.PI * 4 + Math.PI) * 60;

        this.drawHeroCharacter(heroX, h * 0.6, 1.2, this.setup.hero, true);
        this.drawEnemyCharacter(enemyX, h * 0.55, 1.2 * this.setup.enemy.size, this.setup.enemy, true);

        // Multiple effects
        for (let i = 0; i < 3; i++) {
            if ((this.time + i * 100) % 300 < 150) {
                this.drawSlashEffect(heroX + 100, h * 0.4 + i * 50, 150);
                this.drawMagicEffect(enemyX - 100, h * 0.4 + i * 50, 150);
            }
        }

        // Screen shake
        this.cameraShakeIntensity = 0.5;
    }

    drawFightPhase4(progress) {
        // Final strike animation
        const w = this.canvas.width;
        const h = this.canvas.height;
        
        // Hero moves forward for final attack
        const heroX = w * 0.25 + progress * (w * 0.5);
        const enemyX = w * 0.75 - progress * (w * 0.3);

        this.drawHeroCharacter(heroX, h * 0.6, 1.3, this.setup.hero, true);
        this.drawEnemyCharacter(enemyX, h * 0.55, 1.3 * this.setup.enemy.size, this.setup.enemy, true);

        // Massive final slash
        this.drawSlashEffect(heroX + 150, h * 0.5, 300 + progress * 200);

        // Screen shake intense
        this.cameraShakeIntensity = 0.8 * (1 - progress);

        // Flash white for impact
        if (progress > 0.7) {
            this.ctx.fillStyle = `rgba(255, 255, 255, ${(progress - 0.7) * 5})`;
            this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        }
    }

    /**
     * Victory sequence (3 seconds)
     */
    updateVictory() {
        const victoryDuration = 3000;

        if (this.time > victoryDuration) {
            return; // Signal completion
        }

        const progress = this.time / victoryDuration;
        const w = this.canvas.width;
        const h = this.canvas.height;

        // Hero rises in victory
        const heroScale = 1 + progress * 0.3;
        const heroY = h * 0.6 - progress * 100;

        this.drawHeroCharacter(w * 0.5, heroY, heroScale, this.setup.hero, false);

        // Victory glow expands
        const glowSize = 200 + progress * 300;
        this.ctx.strokeStyle = `rgba(255, 200, 0, ${0.8 * (1 - progress)})`;
        this.ctx.lineWidth = 5;
        this.drawCircle(w * 0.5, heroY, glowSize, false);

        // Victory particles explode outward
        for (let i = 0; i < 50; i++) {
            const angle = (i / 50) * Math.PI * 2;
            const distance = progress * 400;
            const px = w * 0.5 + Math.cos(angle) * distance;
            const py = heroY + Math.sin(angle) * distance;
            
            this.ctx.fillStyle = `rgba(255, 150, 0, ${0.6 * (1 - progress)})`;
            this.drawCircle(px, py, 3 + Math.random() * 5, true);
        }
    }

    /**
     * Character rendering functions
     */
    drawHeroCharacter(x, y, scale, hero, isAttacking) {
        this.ctx.save();

        const width = 60 * scale;
        const height = 100 * scale;

        // Body
        this.ctx.fillStyle = hero.color;
        this.ctx.fillRect(x - width / 2, y - height / 2, width, height);

        // Head
        this.ctx.fillStyle = hero.color;
        this.drawCircle(x, y - height / 2 - 20 * scale, 25 * scale, true);

        // Eyes
        this.ctx.fillStyle = '#fff';
        this.drawCircle(x - 12 * scale, y - height / 2 - 25 * scale, 4 * scale, true);
        this.drawCircle(x + 12 * scale, y - height / 2 - 25 * scale, 4 * scale, true);

        // Weapon glow
        this.ctx.strokeStyle = hero.accent;
        this.ctx.lineWidth = 3;
        this.ctx.beginPath();
        const weaponX = x + width / 2 + (isAttacking ? 30 * scale : 10 * scale);
        const weaponY = y;
        this.ctx.moveTo(x, weaponY);
        this.ctx.lineTo(weaponX, weaponY - 40 * scale);
        this.ctx.stroke();

        // Aura
        if (isAttacking) {
            this.ctx.strokeStyle = `rgba(255, 150, 0, 0.5)`;
            this.ctx.lineWidth = 2;
            this.drawCircle(x, y - height / 4, width * 0.6, false);
        }

        this.ctx.restore();
    }

    drawEnemyCharacter(x, y, scale, enemy, isAttacking) {
        this.ctx.save();

        const width = 70 * scale;
        const height = 110 * scale;

        // Body
        this.ctx.fillStyle = enemy.color;
        this.ctx.fillRect(x - width / 2, y - height / 2, width, height);

        // Head (larger/more menacing)
        this.ctx.fillStyle = enemy.accent;
        this.drawCircle(x, y - height / 2 - 25 * scale, 30 * scale, true);

        // Eyes (glowing red/bright)
        this.ctx.fillStyle = '#ff4444';
        this.drawCircle(x - 14 * scale, y - height / 2 - 30 * scale, 5 * scale, true);
        this.drawCircle(x + 14 * scale, y - height / 2 - 30 * scale, 5 * scale, true);

        // Eye glow
        this.ctx.fillStyle = `rgba(255, 100, 100, 0.6)`;
        this.drawCircle(x - 14 * scale, y - height / 2 - 30 * scale, 7 * scale, true);
        this.drawCircle(x + 14 * scale, y - height / 2 - 30 * scale, 7 * scale, true);

        // Menacing aura
        this.ctx.strokeStyle = `rgba(${parseInt(enemy.color.slice(1, 3), 16)}, 0, 0, 0.6)`;
        this.ctx.lineWidth = 3;
        this.drawCircle(x, y - height / 4, width * 0.7, false);

        // Dark energy radiates when attacking
        if (isAttacking) {
            for (let i = 0; i < 4; i++) {
                const angle = (i / 4) * Math.PI * 2;
                this.ctx.strokeStyle = `rgba(255, 50, 50, 0.4)`;
                this.ctx.lineWidth = 2;
                this.ctx.beginPath();
                const px = x + Math.cos(angle) * width * 0.6;
                const py = y + Math.sin(angle) * height * 0.5;
                this.ctx.moveTo(x, y);
                this.ctx.lineTo(px, py);
                this.ctx.stroke();
            }
        }

        this.ctx.restore();
    }

    /**
     * Effect rendering
     */
    drawSlashEffect(x, y, length) {
        this.ctx.save();
        this.ctx.strokeStyle = `rgba(255, 100, 100, 0.8)`;
        this.ctx.lineWidth = 8;
        this.ctx.lineCap = 'round';

        // Diagonal slash
        this.ctx.beginPath();
        this.ctx.moveTo(x - length / 2, y + length / 2);
        this.ctx.lineTo(x + length / 2, y - length / 2);
        this.ctx.stroke();

        // Secondary slash (crossed)
        this.ctx.strokeStyle = `rgba(255, 150, 100, 0.5)`;
        this.ctx.lineWidth = 4;
        this.ctx.beginPath();
        this.ctx.moveTo(x - length / 3, y - length / 3);
        this.ctx.lineTo(x + length / 3, y + length / 3);
        this.ctx.stroke();

        this.ctx.restore();
    }

    drawMagicEffect(x, y, size) {
        this.ctx.save();

        // Magical spiral
        this.ctx.strokeStyle = `rgba(100, 150, 255, 0.7)`;
        this.ctx.lineWidth = 3;
        this.ctx.beginPath();
        for (let i = 0; i < 20; i++) {
            const angle = (i / 20) * Math.PI * 2 * 3;
            const dist = (i / 20) * size;
            const px = x + Math.cos(angle) * dist;
            const py = y + Math.sin(angle) * dist;
            if (i === 0) this.ctx.moveTo(px, py);
            else this.ctx.lineTo(px, py);
        }
        this.ctx.stroke();

        // Radiating energy bursts
        for (let i = 0; i < 6; i++) {
            const angle = (i / 6) * Math.PI * 2;
            this.ctx.strokeStyle = `rgba(100, 150, 255, 0.5)`;
            this.ctx.lineWidth = 2;
            this.ctx.beginPath();
            this.ctx.moveTo(x, y);
            this.ctx.lineTo(x + Math.cos(angle) * size, y + Math.sin(angle) * size);
            this.ctx.stroke();
        }

        this.ctx.restore();
    }

    drawLightBurst(x, y, radius) {
        this.ctx.save();

        // Radial gradient burst
        const gradient = this.ctx.createRadialGradient(x, y, 0, x, y, radius);
        gradient.addColorStop(0, 'rgba(255, 255, 200, 0.8)');
        gradient.addColorStop(1, 'rgba(255, 200, 0, 0)');

        this.ctx.fillStyle = gradient;
        this.drawCircle(x, y, radius, true);

        this.ctx.restore();
    }

    /**
     * Helper drawing functions
     */
    drawCircle(x, y, radius, fill) {
        this.ctx.beginPath();
        this.ctx.arc(x, y, radius, 0, Math.PI * 2);
        if (fill) this.ctx.fill();
        else this.ctx.stroke();
    }

    drawCloud(x, y, size) {
        this.ctx.beginPath();
        this.ctx.arc(x - size / 3, y, size / 3, 0, Math.PI * 2);
        this.ctx.arc(x, y - size / 4, size / 2.5, 0, Math.PI * 2);
        this.ctx.arc(x + size / 3, y, size / 3, 0, Math.PI * 2);
        this.ctx.fill();
    }

    drawTreeShape(x, y, height) {
        // Trunk
        this.ctx.fillRect(x - height * 0.15, y, height * 0.3, height * 0.4);

        // Foliage (triangle)
        this.ctx.beginPath();
        this.ctx.moveTo(x, y - height * 0.4);
        this.ctx.lineTo(x - height * 0.4, y);
        this.ctx.lineTo(x + height * 0.4, y);
        this.ctx.closePath();
        this.ctx.fill();
    }

    drawPolygon(x, y, size, sides) {
        this.ctx.beginPath();
        for (let i = 0; i < sides; i++) {
            const angle = (i / sides) * Math.PI * 2;
            const px = x + Math.cos(angle) * size;
            const py = y + Math.sin(angle) * size;
            if (i === 0) this.ctx.moveTo(px, py);
            else this.ctx.lineTo(px, py);
        }
        this.ctx.closePath();
        this.ctx.fill();
    }

    drawRectWithPerspective(x, y, width, height, perspectiveShift) {
        this.ctx.beginPath();
        this.ctx.moveTo(x, y);
        this.ctx.lineTo(x + width + perspectiveShift * 30, y);
        this.ctx.lineTo(x + width + perspectiveShift * 30, y + height);
        this.ctx.lineTo(x, y + height);
        this.ctx.closePath();
        this.ctx.fill();
    }

    drawFloatingIsland(x, y, size, opacity) {
        const oldAlpha = this.ctx.globalAlpha;
        this.ctx.globalAlpha = opacity;

        // Island shape
        this.ctx.beginPath();
        this.ctx.ellipse(x, y, size, size * 0.6, 0, 0, Math.PI * 2);
        this.ctx.fill();

        this.ctx.globalAlpha = oldAlpha;
    }
}

// Export for use in script.js
if (typeof window !== 'undefined') {
    window.AnimeBattleSystem = AnimeBattleSystem;
}
