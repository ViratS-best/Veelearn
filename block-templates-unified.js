/**
 * UNIFIED BLOCK TEMPLATES - Master definition file
 * Contains ALL 40+ block types for Veelearn simulator
 * Merges physics, animation, rendering, logic, and math blocks
 * Updated: November 9, 2025
 */

// Global block templates object - used by block-simulator.html
const blockTemplates = {
    // ===== LOGIC & DATA BLOCKS =====
    variable: {
        title: "Variable",
        category: "Logic",
        inputs: [
            { name: "name", label: "Variable Name", type: "text", default: "myVar" },
            { name: "value", label: "Initial Value", type: "number", default: 0 }
        ],
        outputs: ["value"],
        description: "Store and retrieve a variable value",
        execute: (inputs) => ({ value: inputs.value })
    },

    "set-variable": {
        title: "Set Variable",
        category: "Logic",
        inputs: [
            { name: "name", label: "Variable Name", type: "text", default: "myVar" },
            { name: "value", label: "Value", type: "number", default: 0 }
        ],
        outputs: [],
        description: "Set a variable to a new value",
        execute: (inputs) => ({})
    },

    "if-condition": {
        title: "If Condition",
        category: "Logic",
        inputs: [
            { name: "value1", label: "Value 1", type: "number", default: 0 },
            { name: "operator", label: "Operator (>/</==/!=/etc)", type: "text", default: ">" },
            { name: "value2", label: "Value 2", type: "number", default: 0 }
        ],
        outputs: ["result", "then_branch", "else_branch"],
        description: "Execute conditional logic",
        execute: (inputs) => {
            let result = false;
            switch (inputs.operator) {
                case '>': result = inputs.value1 > inputs.value2; break;
                case '<': result = inputs.value1 < inputs.value2; break;
                case '==': result = inputs.value1 == inputs.value2; break;
                case '===': result = inputs.value1 === inputs.value2; break;
                case '!==': result = inputs.value1 !== inputs.value2; break;
                case '>=': result = inputs.value1 >= inputs.value2; break;
                case '<=': result = inputs.value1 <= inputs.value2; break;
            }
            return { result, then_branch: result, else_branch: !result };
        }
    },

    "condition-trigger": {
        title: "Condition Trigger",
        category: "Logic",
        inputs: [
            { name: "condition", label: "Condition (true/false)", type: "number", default: 0 },
            { name: "onTrue", label: "Value if true", type: "number", default: 1 },
            { name: "onFalse", label: "Value if false", type: "number", default: 0 }
        ],
        outputs: ["result"],
        description: "Trigger output based on condition",
        execute: (inputs) => ({ result: inputs.condition ? inputs.onTrue : inputs.onFalse })
    },

    "range-mapper": {
        title: "Range Mapper",
        category: "Logic",
        inputs: [
            { name: "value", label: "Input Value", type: "number", default: 50 },
            { name: "inMin", label: "Input Min", type: "number", default: 0 },
            { name: "inMax", label: "Input Max", type: "number", default: 100 },
            { name: "outMin", label: "Output Min", type: "number", default: 0 },
            { name: "outMax", label: "Output Max", type: "number", default: 1 }
        ],
        outputs: ["result"],
        description: "Map value from input range to output range",
        execute: (inputs) => {
            const ratio = (inputs.value - inputs.inMin) / (inputs.inMax - inputs.inMin);
            return { result: inputs.outMin + ratio * (inputs.outMax - inputs.outMin) };
        }
    },

    // ===== MATH BLOCKS =====
    add: {
        title: "Add",
        category: "Math",
        inputs: [
            { name: "a", label: "A", type: "number", default: 0 },
            { name: "b", label: "B", type: "number", default: 0 }
        ],
        outputs: ["result"],
        description: "Add two numbers: A + B",
        execute: (inputs) => ({ result: inputs.a + inputs.b })
    },

    subtract: {
        title: "Subtract",
        category: "Math",
        inputs: [
            { name: "a", label: "A", type: "number", default: 10 },
            { name: "b", label: "B", type: "number", default: 3 }
        ],
        outputs: ["result"],
        description: "Subtract two numbers: A - B",
        execute: (inputs) => ({ result: inputs.a - inputs.b })
    },

    multiply: {
        title: "Multiply",
        category: "Math",
        inputs: [
            { name: "a", label: "A", type: "number", default: 1 },
            { name: "b", label: "B", type: "number", default: 1 }
        ],
        outputs: ["result"],
        description: "Multiply two numbers: A × B",
        execute: (inputs) => ({ result: inputs.a * inputs.b })
    },

    divide: {
        title: "Divide",
        category: "Math",
        inputs: [
            { name: "a", label: "Numerator", type: "number", default: 10 },
            { name: "b", label: "Denominator", type: "number", default: 2 }
        ],
        outputs: ["result"],
        description: "Divide two numbers: A ÷ B",
        execute: (inputs) => ({ result: inputs.b !== 0 ? inputs.a / inputs.b : 0 })
    },

    power: {
        title: "Power",
        category: "Math",
        inputs: [
            { name: "base", label: "Base", type: "number", default: 2 },
            { name: "exponent", label: "Exponent", type: "number", default: 2 }
        ],
        outputs: ["result"],
        description: "Raise base to power: A^B",
        execute: (inputs) => ({ result: Math.pow(inputs.base, inputs.exponent) })
    },

    sqrt: {
        title: "Square Root",
        category: "Math",
        inputs: [
            { name: "value", label: "Value", type: "number", default: 4 }
        ],
        outputs: ["result"],
        description: "Get square root of value: √x",
        execute: (inputs) => ({ result: Math.sqrt(inputs.value) })
    },

    modulo: {
        title: "Modulo",
        category: "Math",
        inputs: [
            { name: "a", label: "A", type: "number", default: 10 },
            { name: "b", label: "B", type: "number", default: 3 }
        ],
        outputs: ["result"],
        description: "Get remainder: A % B",
        execute: (inputs) => ({ result: inputs.a % inputs.b })
    },

    "absolute": {
        title: "Absolute Value",
        category: "Math",
        inputs: [
            { name: "value", label: "Value", type: "number", default: -5 }
        ],
        outputs: ["result"],
        description: "Get absolute value: |x|",
        execute: (inputs) => ({ result: Math.abs(inputs.value) })
    },

    "min-max": {
        title: "Min/Max",
        category: "Math",
        inputs: [
            { name: "a", label: "A", type: "number", default: 5 },
            { name: "b", label: "B", type: "number", default: 10 },
            { name: "mode", label: "Mode (min/max)", type: "text", default: "min" }
        ],
        outputs: ["result"],
        description: "Get minimum or maximum of two values",
        execute: (inputs) => ({
            result: inputs.mode === 'min' ? Math.min(inputs.a, inputs.b) : Math.max(inputs.a, inputs.b)
        })
    },

    "clamp": {
        title: "Clamp Value",
        category: "Math",
        inputs: [
            { name: "value", label: "Value", type: "number", default: 50 },
            { name: "min", label: "Minimum", type: "number", default: 0 },
            { name: "max", label: "Maximum", type: "number", default: 100 }
        ],
        outputs: ["result"],
        description: "Clamp value between min and max",
        execute: (inputs) => ({
            result: Math.max(inputs.min, Math.min(inputs.max, inputs.value))
        })
    },

    "trigonometry": {
        title: "Trigonometry",
        category: "Math",
        inputs: [
            { name: "angle", label: "Angle (degrees)", type: "number", default: 45 },
            { name: "function", label: "Function (sin/cos/tan/asin/acos/atan)", type: "text", default: "sin" }
        ],
        outputs: ["result"],
        description: "Calculate trigonometric function",
        execute: (inputs) => {
            const rad = inputs.angle * Math.PI / 180;
            let result = 0;
            switch (inputs.function) {
                case 'sin': result = Math.sin(rad); break;
                case 'cos': result = Math.cos(rad); break;
                case 'tan': result = Math.tan(rad); break;
                case 'asin': result = Math.asin(rad) * 180 / Math.PI; break;
                case 'acos': result = Math.acos(rad) * 180 / Math.PI; break;
                case 'atan': result = Math.atan(rad) * 180 / Math.PI; break;
            }
            return { result };
        }
    },

    "random-number": {
        title: "Random Number",
        category: "Math",
        inputs: [
            { name: "min", label: "Min", type: "number", default: 0 },
            { name: "max", label: "Max", type: "number", default: 100 },
            { name: "type", label: "Type (int/float)", type: "text", default: "float" }
        ],
        outputs: ["result"],
        description: "Generate random number in range",
        execute: (inputs) => {
            const rand = Math.random() * (inputs.max - inputs.min) + inputs.min;
            return { result: inputs.type === 'int' ? Math.floor(rand) : rand };
        }
    },

    // ===== DRAWING BLOCKS =====
    "draw-circle": {
        title: "Draw Circle",
        category: "Drawing",
        inputs: [
            { name: "x", label: "X Position", type: "number", default: 184 },
            { name: "y", label: "Y Position", type: "number", default: 200 },
            { name: "radius", label: "Radius", type: "number", default: 50 },
            { name: "color", label: "Color (hex or name)", type: "text", default: "#667eea" }
        ],
        outputs: [],
        description: "Draw a filled circle",
        execute: (inputs, state) => {
            if (state.ctx) {
                state.ctx.fillStyle = inputs.color;
                state.ctx.beginPath();
                state.ctx.arc(inputs.x, inputs.y, inputs.radius, 0, Math.PI * 2);
                state.ctx.fill();
            }
            return {};
        }
    },

    "draw-rectangle": {
        title: "Draw Rectangle",
        category: "Drawing",
        inputs: [
            { name: "x", label: "X Position", type: "number", default: 50 },
            { name: "y", label: "Y Position", type: "number", default: 150 },
            { name: "width", label: "Width", type: "number", default: 100 },
            { name: "height", label: "Height", type: "number", default: 80 },
            { name: "color", label: "Color (hex or name)", type: "text", default: "#10b981" }
        ],
        outputs: [],
        description: "Draw a filled rectangle",
        execute: (inputs, state) => {
            if (state.ctx) {
                state.ctx.fillStyle = inputs.color;
                state.ctx.fillRect(inputs.x, inputs.y, inputs.width, inputs.height);
            }
            return {};
        }
    },

    "draw-line": {
        title: "Draw Line",
        category: "Drawing",
        inputs: [
            { name: "x1", label: "Start X", type: "number", default: 50 },
            { name: "y1", label: "Start Y", type: "number", default: 50 },
            { name: "x2", label: "End X", type: "number", default: 300 },
            { name: "y2", label: "End Y", type: "number", default: 350 },
            { name: "color", label: "Color", type: "text", default: "#333" },
            { name: "width", label: "Width", type: "number", default: 2 }
        ],
        outputs: [],
        description: "Draw a line",
        execute: (inputs, state) => {
            if (state.ctx) {
                state.ctx.strokeStyle = inputs.color;
                state.ctx.lineWidth = inputs.width;
                state.ctx.beginPath();
                state.ctx.moveTo(inputs.x1, inputs.y1);
                state.ctx.lineTo(inputs.x2, inputs.y2);
                state.ctx.stroke();
            }
            return {};
        }
    },

    "draw-text": {
        title: "Draw Text",
        category: "Drawing",
        inputs: [
            { name: "text", label: "Text", type: "text", default: "Hello" },
            { name: "x", label: "X Position", type: "number", default: 100 },
            { name: "y", label: "Y Position", type: "number", default: 200 },
            { name: "color", label: "Color", type: "text", default: "#000" },
            { name: "size", label: "Font Size", type: "number", default: 16 }
        ],
        outputs: [],
        description: "Draw text on canvas",
        execute: (inputs, state) => {
            if (state.ctx) {
                state.ctx.fillStyle = inputs.color;
                state.ctx.font = `${inputs.size}px Arial`;
                state.ctx.fillText(String(inputs.text), inputs.x, inputs.y);
            }
            return {};
        }
    },

    "draw-polygon": {
        title: "Draw Polygon",
        category: "Drawing",
        inputs: [
            { name: "cx", label: "Center X", type: "number", default: 184 },
            { name: "cy", label: "Center Y", type: "number", default: 200 },
            { name: "sides", label: "Sides", type: "number", default: 6 },
            { name: "radius", label: "Radius", type: "number", default: 50 },
            { name: "color", label: "Color", type: "text", default: "#667eea" }
        ],
        outputs: [],
        description: "Draw a polygon with N sides",
        execute: (inputs, state) => {
            if (state.ctx) {
                state.ctx.fillStyle = inputs.color;
                state.ctx.beginPath();
                for (let i = 0; i < inputs.sides; i++) {
                    const angle = (i / inputs.sides) * Math.PI * 2;
                    const x = inputs.cx + Math.cos(angle) * inputs.radius;
                    const y = inputs.cy + Math.sin(angle) * inputs.radius;
                    if (i === 0) state.ctx.moveTo(x, y);
                    else state.ctx.lineTo(x, y);
                }
                state.ctx.closePath();
                state.ctx.fill();
            }
            return {};
        }
    },

    "draw-arc": {
        title: "Draw Arc",
        category: "Drawing",
        inputs: [
            { name: "x", label: "Center X", type: "number", default: 184 },
            { name: "y", label: "Center Y", type: "number", default: 200 },
            { name: "radius", label: "Radius", type: "number", default: 50 },
            { name: "startAngle", label: "Start Angle (degrees)", type: "number", default: 0 },
            { name: "endAngle", label: "End Angle (degrees)", type: "number", default: 180 },
            { name: "color", label: "Color", type: "text", default: "#667eea" }
        ],
        outputs: [],
        description: "Draw an arc",
        execute: (inputs, state) => {
            if (state.ctx) {
                state.ctx.strokeStyle = inputs.color;
                state.ctx.lineWidth = 2;
                state.ctx.beginPath();
                const start = inputs.startAngle * Math.PI / 180;
                const end = inputs.endAngle * Math.PI / 180;
                state.ctx.arc(inputs.x, inputs.y, inputs.radius, start, end);
                state.ctx.stroke();
            }
            return {};
        }
    },

    "draw-gradient-rect": {
        title: "Gradient Rectangle",
        category: "Drawing",
        inputs: [
            { name: "x", label: "X", type: "number", default: 50 },
            { name: "y", label: "Y", type: "number", default: 100 },
            { name: "width", label: "Width", type: "number", default: 200 },
            { name: "height", label: "Height", type: "number", default: 100 },
            { name: "color1", label: "Color 1", type: "text", default: "#667eea" },
            { name: "color2", label: "Color 2", type: "text", default: "#764ba2" }
        ],
        outputs: [],
        description: "Draw rectangle with gradient",
        execute: (inputs, state) => {
            if (state.ctx) {
                const grad = state.ctx.createLinearGradient(inputs.x, inputs.y, inputs.x + inputs.width, inputs.y);
                grad.addColorStop(0, inputs.color1);
                grad.addColorStop(1, inputs.color2);
                state.ctx.fillStyle = grad;
                state.ctx.fillRect(inputs.x, inputs.y, inputs.width, inputs.height);
            }
            return {};
        }
    },

    "trace-path": {
        title: "Trace Path",
        category: "Drawing",
        inputs: [
            { name: "x", label: "X", type: "number", default: 100 },
            { name: "y", label: "Y", type: "number", default: 100 },
            { name: "color", label: "Color", type: "text", default: "#667eea" },
            { name: "size", label: "Size", type: "number", default: 2 }
        ],
        outputs: [],
        description: "Leave a trace as object moves",
        execute: (inputs, state) => {
            if (state.ctx) {
                state.ctx.fillStyle = inputs.color;
                state.ctx.beginPath();
                state.ctx.arc(inputs.x, inputs.y, inputs.size, 0, Math.PI * 2);
                state.ctx.fill();
            }
            return {};
        }
    },

    "clear-canvas": {
        title: "Clear Canvas",
        category: "Drawing",
        inputs: [
            { name: "color", label: "Background Color", type: "text", default: "white" }
        ],
        outputs: [],
        description: "Clear the canvas",
        execute: (inputs, state) => {
            if (state.ctx && state.canvas) {
                state.ctx.fillStyle = inputs.color;
                state.ctx.fillRect(0, 0, state.canvas.width, state.canvas.height);
            }
            return {};
        }
    },

    // ===== PHYSICS BLOCKS =====
    "gravity": {
        title: "Apply Gravity",
        category: "Physics",
        inputs: [
            { name: "mass", label: "Mass (kg)", type: "number", default: 1 },
            { name: "g", label: "Gravity (m/s²)", type: "number", default: 9.8 },
            { name: "damping", label: "Damping", type: "number", default: 0.99 }
        ],
        outputs: ["force", "acceleration"],
        description: "Apply gravitational force",
        execute: (inputs) => {
            const force = inputs.mass * inputs.g;
            const acceleration = force / inputs.mass;
            return { force, acceleration };
        }
    },

    "velocity": {
        title: "Set Velocity",
        category: "Physics",
        inputs: [
            { name: "vx", label: "Velocity X", type: "number", default: 0 },
            { name: "vy", label: "Velocity Y", type: "number", default: 0 },
            { name: "duration", label: "Duration (s)", type: "number", default: 1 }
        ],
        outputs: ["vx", "vy", "distance"],
        description: "Set object velocity",
        execute: (inputs) => {
            const distance = Math.sqrt(inputs.vx ** 2 + inputs.vy ** 2) * inputs.duration;
            return { vx: inputs.vx, vy: inputs.vy, distance };
        }
    },

    "collision-detection": {
        title: "Detect Collision",
        category: "Physics",
        inputs: [
            { name: "x1", label: "Object 1 X", type: "number", default: 100 },
            { name: "y1", label: "Object 1 Y", type: "number", default: 100 },
            { name: "r1", label: "Object 1 Radius", type: "number", default: 20 },
            { name: "x2", label: "Object 2 X", type: "number", default: 200 },
            { name: "y2", label: "Object 2 Y", type: "number", default: 100 },
            { name: "r2", label: "Object 2 Radius", type: "number", default: 20 }
        ],
        outputs: ["colliding", "distance", "overlap"],
        description: "Detect collision between two circles",
        execute: (inputs) => {
            const distance = Math.sqrt((inputs.x2 - inputs.x1) ** 2 + (inputs.y2 - inputs.y1) ** 2);
            const colliding = distance < (inputs.r1 + inputs.r2);
            const overlap = (inputs.r1 + inputs.r2) - distance;
            return { colliding, distance, overlap };
        }
    },

    "spring-physics": {
        title: "Spring Physics",
        category: "Physics",
        inputs: [
            { name: "x", label: "Current Position", type: "number", default: 0 },
            { name: "target", label: "Target Position", type: "number", default: 100 },
            { name: "stiffness", label: "Stiffness (k)", type: "number", default: 0.1 },
            { name: "damping", label: "Damping (c)", type: "number", default: 0.05 }
        ],
        outputs: ["force", "newPosition"],
        description: "Apply spring force",
        execute: (inputs) => {
            const displacement = inputs.target - inputs.x;
            const force = inputs.stiffness * displacement;
            const newPosition = inputs.x + force;
            return { force, newPosition };
        }
    },

    "particle-system": {
        title: "Particle System",
        category: "Physics",
        inputs: [
            { name: "x", label: "Emitter X", type: "number", default: 184 },
            { name: "y", label: "Emitter Y", type: "number", default: 200 },
            { name: "count", label: "Particle Count", type: "number", default: 10 },
            { name: "speed", label: "Speed", type: "number", default: 5 },
            { name: "color", label: "Color", type: "text", default: "#ff00ff" }
        ],
        outputs: ["particles"],
        description: "Emit particles from position",
        execute: (inputs) => {
            const particles = [];
            for (let i = 0; i < inputs.count; i++) {
                const angle = (Math.random() * Math.PI * 2);
                particles.push({
                    x: inputs.x,
                    y: inputs.y,
                    vx: Math.cos(angle) * inputs.speed,
                    vy: Math.sin(angle) * inputs.speed,
                    lifetime: 1.0,
                    color: inputs.color
                });
            }
            return { particles };
        }
    },

    "gravity-simulation": {
        title: "Gravity Simulation",
        category: "Physics",
        inputs: [
            { name: "vy", label: "Vertical Velocity", type: "number", default: 0 },
            { name: "g", label: "Gravity", type: "number", default: 9.8 },
            { name: "dt", label: "Delta Time", type: "number", default: 0.016 }
        ],
        outputs: ["newVy", "newY"],
        description: "Simulate gravity on object",
        execute: (inputs) => {
            const newVy = inputs.vy + inputs.g * inputs.dt;
            const newY = inputs.vy * inputs.dt + 0.5 * inputs.g * inputs.dt * inputs.dt;
            return { newVy, newY };
        }
    },

    // ===== ANIMATION BLOCKS =====
    "animation-loop": {
        title: "Animation Loop",
        category: "Animation",
        inputs: [
            { name: "duration", label: "Duration (ms)", type: "number", default: 1000 },
            { name: "repeat", label: "Repeat (0 = infinite)", type: "number", default: 1 }
        ],
        outputs: ["progress", "frameCount"],
        description: "Create animation loop",
        execute: (inputs, state) => {
            const progress = (state.frameCount || 0) % inputs.duration / inputs.duration;
            return { progress, frameCount: state.frameCount || 0 };
        }
    },

    "frame-counter": {
        title: "Frame Counter",
        category: "Animation",
        inputs: [
            { name: "reset", label: "Reset", type: "number", default: 0 }
        ],
        outputs: ["count", "time"],
        description: "Count animation frames",
        execute: (inputs, state) => {
            const count = inputs.reset ? 0 : (state.frameCount || 0) + 1;
            const time = count * 0.016; // ~60 FPS
            return { count, time };
        }
    },

    "easing-function": {
        title: "Easing Function",
        category: "Animation",
        inputs: [
            { name: "t", label: "Time (0-1)", type: "number", default: 0.5 },
            { name: "type", label: "Type (linear/ease-in/ease-out/ease-inout)", type: "text", default: "linear" }
        ],
        outputs: ["value"],
        description: "Apply easing function",
        execute: (inputs) => {
            let value = inputs.t;
            switch (inputs.type) {
                case 'ease-in':
                    value = inputs.t * inputs.t;
                    break;
                case 'ease-out':
                    value = 1 - (1 - inputs.t) * (1 - inputs.t);
                    break;
                case 'ease-inout':
                    value = inputs.t < 0.5 ? 2 * inputs.t * inputs.t : -1 + (4 - 2 * inputs.t) * inputs.t;
                    break;
                case 'linear':
                default:
                    value = inputs.t;
            }
            return { value };
        }
    },

    // ===== ADVANCED BLOCKS =====
    "vector-operation": {
        title: "Vector Operation",
        category: "Advanced",
        inputs: [
            { name: "x1", label: "Vector 1 X", type: "number", default: 1 },
            { name: "y1", label: "Vector 1 Y", type: "number", default: 0 },
            { name: "x2", label: "Vector 2 X", type: "number", default: 0 },
            { name: "y2", label: "Vector 2 Y", type: "number", default: 1 },
            { name: "operation", label: "Operation (dot/cross/magnitude)", type: "text", default: "dot" }
        ],
        outputs: ["result", "resultX", "resultY"],
        description: "Vector math operations",
        execute: (inputs) => {
            let result = 0;
            let resultX = 0;
            let resultY = 0;
            switch (inputs.operation) {
                case 'dot':
                    result = inputs.x1 * inputs.x2 + inputs.y1 * inputs.y2;
                    break;
                case 'cross':
                    result = inputs.x1 * inputs.y2 - inputs.y1 * inputs.x2;
                    break;
                case 'magnitude':
                    result = Math.sqrt(inputs.x1 * inputs.x1 + inputs.y1 * inputs.y1);
                    break;
                case 'add':
                    resultX = inputs.x1 + inputs.x2;
                    resultY = inputs.y1 + inputs.y2;
                    break;
                case 'subtract':
                    resultX = inputs.x1 - inputs.x2;
                    resultY = inputs.y1 - inputs.y2;
                    break;
            }
            return { result, resultX, resultY };
        }
    },

    "rotation": {
        title: "2D Rotation",
        category: "Advanced",
        inputs: [
            { name: "x", label: "Point X", type: "number", default: 100 },
            { name: "y", label: "Point Y", type: "number", default: 0 },
            { name: "cx", label: "Center X", type: "number", default: 0 },
            { name: "cy", label: "Center Y", type: "number", default: 0 },
            { name: "angle", label: "Angle (degrees)", type: "number", default: 45 }
        ],
        outputs: ["newX", "newY"],
        description: "Rotate point around center",
        execute: (inputs) => {
            const rad = inputs.angle * Math.PI / 180;
            const cos = Math.cos(rad);
            const sin = Math.sin(rad);
            const px = inputs.x - inputs.cx;
            const py = inputs.y - inputs.cy;
            return {
                newX: inputs.cx + px * cos - py * sin,
                newY: inputs.cy + px * sin + py * cos
            };
        }
    },

    "raycast": {
        title: "Raycast",
        category: "Advanced",
        inputs: [
            { name: "x", label: "Ray Start X", type: "number", default: 0 },
            { name: "y", label: "Ray Start Y", type: "number", default: 0 },
            { name: "angle", label: "Ray Angle (degrees)", type: "number", default: 0 },
            { name: "maxDistance", label: "Max Distance", type: "number", default: 500 },
            { name: "targetX", label: "Target X", type: "number", default: 200 },
            { name: "targetY", label: "Target Y", type: "number", default: 200 },
            { name: "targetRadius", label: "Target Radius", type: "number", default: 20 }
        ],
        outputs: ["hit", "distance"],
        description: "Cast ray and detect collisions",
        execute: (inputs) => {
            const rad = inputs.angle * Math.PI / 180;
            const rayX = Math.cos(rad);
            const rayY = Math.sin(rad);
            
            // Simple sphere intersection
            const toTargetX = inputs.targetX - inputs.x;
            const toTargetY = inputs.targetY - inputs.y;
            const projection = toTargetX * rayX + toTargetY * rayY;
            
            const distance = Math.sqrt(toTargetX * toTargetX + toTargetY * toTargetY);
            const hit = distance <= inputs.targetRadius && projection > 0 && projection < inputs.maxDistance;
            
            return { hit, distance };
        }
    },

    // ===== INPUT BLOCKS =====
    "slider": {
        title: "Slider Input",
        category: "Input",
        inputs: [
            { name: "min", label: "Min", type: "number", default: 0 },
            { name: "max", label: "Max", type: "number", default: 100 },
            { name: "default", label: "Default", type: "number", default: 50 }
        ],
        outputs: ["value"],
        description: "Interactive slider input",
        execute: (inputs) => ({ value: inputs.default })
    }
};

// Export for node.js / CommonJS if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { blockTemplates };
}
