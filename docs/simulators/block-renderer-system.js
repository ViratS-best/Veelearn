/**
 * Block Renderer System - Canvas rendering and display blocks
 * Provides efficient rendering for physics simulations
 * ~420 lines
 */

const BlockRendererSystem = {
    // ===== RENDERER CONTEXT MANAGEMENT =====
    rendererState: {
        canvas: null,
        ctx: null,
        width: 400,
        height: 400,
        layers: {},
        trails: []
    },

    /**
     * Initialize renderer with canvas
     * @param {HTMLCanvasElement} canvas - Target canvas
     */
    init(canvas) {
        this.rendererState.canvas = canvas;
        this.rendererState.ctx = canvas.getContext('2d');
        this.rendererState.width = canvas.width;
        this.rendererState.height = canvas.height;
        this.rendererState.trails = [];
    },

    /**
     * Clear canvas
     */
    clear() {
        const ctx = this.rendererState.ctx;
        if (!ctx) return;
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, this.rendererState.width, this.rendererState.height);
    },

    /**
     * Draw grid background
     * @param {Number} cellSize - Size of grid cells
     * @param {String} color - Grid color
     * @param {Number} opacity - Grid opacity
     */
    drawGrid(cellSize, color = '#e0e0e0', opacity = 0.5) {
        const ctx = this.rendererState.ctx;
        if (!ctx) return;

        ctx.strokeStyle = color;
        ctx.globalAlpha = opacity;
        ctx.lineWidth = 1;

        // Vertical lines
        for (let x = 0; x < this.rendererState.width; x += cellSize) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, this.rendererState.height);
            ctx.stroke();
        }

        // Horizontal lines
        for (let y = 0; y < this.rendererState.height; y += cellSize) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(this.rendererState.width, y);
            ctx.stroke();
        }

        ctx.globalAlpha = 1;
    },

    // ===== RENDERING BLOCKS =====
    blocks: {
        shapeRenderer: {
            title: 'Draw Shape',
            category: 'Rendering',
            inputs: [
                { name: 'x', type: 'number', default: 200 },
                { name: 'y', type: 'number', default: 200 },
                { name: 'width', type: 'number', default: 50 },
                { name: 'height', type: 'number', default: 50 },
                { name: 'shape', type: 'text', default: 'circle' },
                { name: 'color', type: 'text', default: '#667eea' },
                { name: 'outline_color', type: 'text', default: '#333' },
                { name: 'outline_width', type: 'number', default: 2 },
                { name: 'rotation', type: 'number', default: 0 },
                { name: 'alpha', type: 'number', default: 1 }
            ],
            outputs: [],
            execute: (inputs, state, ctx) => {
                if (!ctx) return { state };

                ctx.save();
                ctx.globalAlpha = inputs.alpha;
                ctx.translate(inputs.x, inputs.y);
                ctx.rotate(inputs.rotation * Math.PI / 180);

                ctx.fillStyle = inputs.color;

                // Draw based on shape type
                switch (inputs.shape.toLowerCase()) {
                    case 'circle':
                        ctx.beginPath();
                        ctx.arc(0, 0, inputs.width, 0, Math.PI * 2);
                        ctx.fill();
                        break;

                    case 'rectangle':
                    case 'rect':
                        ctx.fillRect(-inputs.width / 2, -inputs.height / 2, inputs.width, inputs.height);
                        break;

                    case 'triangle':
                        ctx.beginPath();
                        ctx.moveTo(0, -inputs.height / 2);
                        ctx.lineTo(inputs.width / 2, inputs.height / 2);
                        ctx.lineTo(-inputs.width / 2, inputs.height / 2);
                        ctx.closePath();
                        ctx.fill();
                        break;

                    case 'polygon': {
                        const sides = Math.max(3, Math.round(inputs.width));
                        const radius = inputs.height;
                        ctx.beginPath();
                        for (let i = 0; i < sides; i++) {
                            const angle = (i / sides) * Math.PI * 2 - Math.PI / 2;
                            const px = Math.cos(angle) * radius;
                            const py = Math.sin(angle) * radius;
                            if (i === 0) ctx.moveTo(px, py);
                            else ctx.lineTo(px, py);
                        }
                        ctx.closePath();
                        ctx.fill();
                        break;
                    }
                }

                // Draw outline
                if (inputs.outline_width > 0) {
                    ctx.strokeStyle = inputs.outline_color;
                    ctx.lineWidth = inputs.outline_width;
                    ctx.stroke();
                }

                ctx.restore();
                return { state };
            }
        },

        textRenderer: {
            title: 'Draw Text',
            category: 'Rendering',
            inputs: [
                { name: 'text', type: 'text', default: 'Hello' },
                { name: 'x', type: 'number', default: 200 },
                { name: 'y', type: 'number', default: 200 },
                { name: 'font_size', type: 'number', default: 16 },
                { name: 'color', type: 'text', default: '#333' },
                { name: 'alignment', type: 'text', default: 'center' },
                { name: 'alpha', type: 'number', default: 1 }
            ],
            outputs: [],
            execute: (inputs, state, ctx) => {
                if (!ctx) return { state };

                ctx.save();
                ctx.globalAlpha = inputs.alpha;
                ctx.fillStyle = inputs.color;
                ctx.font = `${inputs.font_size}px Arial`;
                ctx.textAlign = inputs.alignment || 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(inputs.text, inputs.x, inputs.y);
                ctx.restore();

                return { state };
            }
        },

        particleRenderer: {
            title: 'Draw Particles',
            category: 'Rendering',
            inputs: [
                { name: 'particles', type: 'number', default: 0 },
                { name: 'size', type: 'number', default: 5 },
                { name: 'color', type: 'text', default: '#667eea' },
                { name: 'blend_mode', type: 'text', default: 'source-over' }
            ],
            outputs: [],
            execute: (inputs, state, ctx) => {
                if (!ctx || !Array.isArray(inputs.particles)) return { state };

                ctx.save();
                ctx.fillStyle = inputs.color;
                ctx.globalCompositeOperation = inputs.blend_mode;

                inputs.particles.forEach(p => {
                    ctx.globalAlpha = Math.max(0, 1 - (Date.now() - p.created) / p.lifetime);
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, inputs.size, 0, Math.PI * 2);
                    ctx.fill();
                });

                ctx.restore();
                return { state };
            }
        },

        trailRenderer: {
            title: 'Draw Trail',
            category: 'Rendering',
            inputs: [
                { name: 'x', type: 'number', default: 200 },
                { name: 'y', type: 'number', default: 200 },
                { name: 'color', type: 'text', default: '#ef4444' },
                { name: 'width', type: 'number', default: 2 },
                { name: 'lifetime', type: 'number', default: 1000 }
            ],
            outputs: [],
            execute: (inputs, state, ctx) => {
                const trails = BlockRendererSystem.rendererState.trails;
                
                // Add trail point
                trails.push({
                    x: inputs.x,
                    y: inputs.y,
                    created: Date.now(),
                    lifetime: inputs.lifetime,
                    color: inputs.color,
                    width: inputs.width
                });

                // Clean up old trails
                const now = Date.now();
                for (let i = trails.length - 1; i >= 0; i--) {
                    if (now - trails[i].created > trails[i].lifetime) {
                        trails.splice(i, 1);
                    }
                }

                // Draw trails
                if (ctx) {
                    for (let i = 0; i < trails.length - 1; i++) {
                        const t1 = trails[i];
                        const t2 = trails[i + 1];
                        const age = now - t1.created;
                        const alpha = 1 - (age / t1.lifetime);

                        ctx.save();
                        ctx.strokeStyle = t1.color;
                        ctx.lineWidth = t1.width;
                        ctx.globalAlpha = alpha;
                        ctx.beginPath();
                        ctx.moveTo(t1.x, t1.y);
                        ctx.lineTo(t2.x, t2.y);
                        ctx.stroke();
                        ctx.restore();
                    }
                }

                return { state };
            }
        },

        gridRenderer: {
            title: 'Draw Grid',
            category: 'Rendering',
            inputs: [
                { name: 'cell_size', type: 'number', default: 50 },
                { name: 'color', type: 'text', default: '#e0e0e0' },
                { name: 'opacity', type: 'number', default: 0.5 }
            ],
            outputs: [],
            execute: (inputs, state, ctx) => {
                if (!ctx) return { state };

                BlockRendererSystem.drawGrid(
                    inputs.cell_size,
                    inputs.color,
                    inputs.opacity
                );

                return { state };
            }
        },

        spriteRenderer: {
            title: 'Draw Sprite',
            category: 'Rendering',
            inputs: [
                { name: 'image_url', type: 'text', default: '' },
                { name: 'x', type: 'number', default: 200 },
                { name: 'y', type: 'number', default: 200 },
                { name: 'width', type: 'number', default: 50 },
                { name: 'height', type: 'number', default: 50 },
                { name: 'rotation', type: 'number', default: 0 },
                { name: 'alpha', type: 'number', default: 1 }
            ],
            outputs: [],
            execute: (inputs, state, ctx) => {
                if (!ctx || !inputs.image_url) return { state };

                // Load and cache image
                if (!BlockRendererSystem.imageCache) {
                    BlockRendererSystem.imageCache = {};
                }

                const cache = BlockRendererSystem.imageCache;
                if (!cache[inputs.image_url]) {
                    const img = new Image();
                    img.src = inputs.image_url;
                    cache[inputs.image_url] = img;
                }

                const img = cache[inputs.image_url];
                if (!img.complete) return { state }; // Wait for image to load

                ctx.save();
                ctx.translate(inputs.x, inputs.y);
                ctx.rotate(inputs.rotation * Math.PI / 180);
                ctx.globalAlpha = inputs.alpha;
                ctx.drawImage(img, -inputs.width / 2, -inputs.height / 2, inputs.width, inputs.height);
                ctx.restore();

                return { state };
            }
        },

        clearCanvas: {
            title: 'Clear Canvas',
            category: 'Rendering',
            inputs: [
                { name: 'color', type: 'text', default: '#ffffff' }
            ],
            outputs: [],
            execute: (inputs, state, ctx) => {
                if (!ctx) return { state };

                ctx.fillStyle = inputs.color;
                ctx.fillRect(0, 0, BlockRendererSystem.rendererState.width, BlockRendererSystem.rendererState.height);

                // Clear trails
                BlockRendererSystem.rendererState.trails = [];

                return { state };
            }
        }
    }
};

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BlockRendererSystem;
}
