# Example Simulators - Ready to Use

This guide contains ready-to-use simulator configurations that can be imported into Veelearn courses.

## 1. Gravity & Falling Objects Simulator

### Purpose
Demonstrate gravitational force effects on objects falling from various heights.

### Blocks Configuration
```json
{
  "title": "Gravity Simulator",
  "description": "Simulate gravity effects on falling objects with adjustable mass and initial height",
  "blocks": [
    {
      "id": 1,
      "type": "clear-canvas",
      "x": 50,
      "y": 50,
      "inputs": {}
    },
    {
      "id": 2,
      "type": "slider",
      "x": 50,
      "y": 120,
      "inputs": {
        "label": "Object Height",
        "min": 50,
        "max": 400,
        "default": 200
      }
    },
    {
      "id": 3,
      "type": "slider",
      "x": 50,
      "y": 190,
      "inputs": {
        "label": "Object Mass",
        "min": 1,
        "max": 10,
        "default": 1
      }
    },
    {
      "id": 4,
      "type": "variable",
      "x": 300,
      "y": 50,
      "inputs": {
        "name": "gravity",
        "value": 9.8
      }
    },
    {
      "id": 5,
      "type": "gravity",
      "x": 300,
      "y": 120,
      "inputs": {
        "mass": 5,
        "g": 9.8
      }
    },
    {
      "id": 6,
      "type": "draw-circle",
      "x": 300,
      "y": 200,
      "inputs": {
        "x": 300,
        "y": 200,
        "radius": 15,
        "color": "#667eea"
      }
    },
    {
      "id": 7,
      "type": "draw-text",
      "x": 500,
      "y": 120,
      "inputs": {
        "text": "F = mg",
        "x": 50,
        "y": 30,
        "color": "#333",
        "size": 16
      }
    }
  ],
  "connections": [
    { "from": 2, "to": 6 },
    { "from": 3, "to": 5 },
    { "from": 5, "to": 7 }
  ],
  "tags": "physics,gravity,force,education"
}
```

## 2. Projectile Motion Simulator

### Purpose
Teach projectile motion with adjustable launch angle, velocity, and gravity.

### Blocks Configuration
```json
{
  "title": "Projectile Motion",
  "description": "Interactive projectile motion simulator with angle and velocity controls",
  "blocks": [
    {
      "id": 1,
      "type": "clear-canvas",
      "x": 50,
      "y": 50,
      "inputs": {}
    },
    {
      "id": 2,
      "type": "slider",
      "x": 50,
      "y": 120,
      "inputs": {
        "label": "Launch Angle",
        "min": 0,
        "max": 90,
        "default": 45
      }
    },
    {
      "id": 3,
      "type": "slider",
      "x": 50,
      "y": 190,
      "inputs": {
        "label": "Initial Velocity",
        "min": 5,
        "max": 50,
        "default": 25
      }
    },
    {
      "id": 4,
      "type": "trigonometry",
      "x": 250,
      "y": 120,
      "inputs": {
        "angle": 45,
        "function": "sin"
      }
    },
    {
      "id": 5,
      "type": "trigonometry",
      "x": 250,
      "y": 190,
      "inputs": {
        "angle": 45,
        "function": "cos"
      }
    },
    {
      "id": 6,
      "type": "velocity",
      "x": 450,
      "y": 155,
      "inputs": {
        "vx": 20,
        "vy": 20,
        "duration": 1
      }
    },
    {
      "id": 7,
      "type": "motion",
      "x": 600,
      "y": 155,
      "inputs": {
        "x": 100,
        "y": 300,
        "vx": 20,
        "vy": -20,
        "dt": 0.016
      }
    },
    {
      "id": 8,
      "type": "draw-circle",
      "x": 750,
      "y": 155,
      "inputs": {
        "x": 100,
        "y": 300,
        "radius": 8,
        "color": "#ef4444"
      }
    },
    {
      "id": 9,
      "type": "draw-trail",
      "x": 750,
      "y": 220,
      "inputs": {
        "x1": 100,
        "y1": 300,
        "x2": 120,
        "y2": 280,
        "color": "#10b981",
        "width": 1
      }
    }
  ],
  "connections": [
    { "from": 2, "to": 4 },
    { "from": 2, "to": 5 },
    { "from": 4, "to": 6 },
    { "from": 5, "to": 6 },
    { "from": 3, "to": 6 },
    { "from": 6, "to": 7 },
    { "from": 7, "to": 8 },
    { "from": 7, "to": 9 }
  ],
  "tags": "physics,projectile,motion,kinematics"
}
```

## 3. Collision Detection Simulator

### Purpose
Demonstrate collision detection between moving objects.

### Blocks Configuration
```json
{
  "title": "Collision Detector",
  "description": "Interactive collision detection between two objects",
  "blocks": [
    {
      "id": 1,
      "type": "clear-canvas",
      "x": 50,
      "y": 50,
      "inputs": {}
    },
    {
      "id": 2,
      "type": "slider",
      "x": 50,
      "y": 120,
      "inputs": {
        "label": "Object 1 Position",
        "min": 50,
        "max": 500,
        "default": 200
      }
    },
    {
      "id": 3,
      "type": "slider",
      "x": 50,
      "y": 190,
      "inputs": {
        "label": "Object 2 Position",
        "min": 50,
        "max": 500,
        "default": 400
      }
    },
    {
      "id": 4,
      "type": "collision",
      "x": 300,
      "y": 155,
      "inputs": {
        "x1": 200,
        "y1": 200,
        "r1": 20,
        "x2": 400,
        "y2": 200,
        "r2": 20
      }
    },
    {
      "id": 5,
      "type": "condition",
      "x": 500,
      "y": 155,
      "inputs": {
        "value1": 0,
        "operator": ">",
        "value2": 0
      }
    },
    {
      "id": 6,
      "type": "draw-circle",
      "x": 650,
      "y": 80,
      "inputs": {
        "x": 200,
        "y": 200,
        "radius": 20,
        "color": "#667eea"
      }
    },
    {
      "id": 7,
      "type": "draw-circle",
      "x": 650,
      "y": 150,
      "inputs": {
        "x": 400,
        "y": 200,
        "radius": 20,
        "color": "#10b981"
      }
    },
    {
      "id": 8,
      "type": "draw-text",
      "x": 650,
      "y": 220,
      "inputs": {
        "text": "No Collision",
        "x": 100,
        "y": 50,
        "color": "#333",
        "size": 14
      }
    }
  ],
  "connections": [
    { "from": 2, "to": 4 },
    { "from": 3, "to": 4 },
    { "from": 4, "to": 5 },
    { "from": 5, "to": 8 }
  ],
  "tags": "physics,collision,detection,geometry"
}
```

## 4. Mathematical Function Visualizer

### Purpose
Visualize mathematical functions with adjustable parameters.

### Blocks Configuration
```json
{
  "title": "Function Visualizer",
  "description": "Visualize sine, cosine, and polynomial functions",
  "blocks": [
    {
      "id": 1,
      "type": "clear-canvas",
      "x": 50,
      "y": 50,
      "inputs": {}
    },
    {
      "id": 2,
      "type": "slider",
      "x": 50,
      "y": 120,
      "inputs": {
        "label": "Frequency",
        "min": 0.5,
        "max": 5,
        "default": 1
      }
    },
    {
      "id": 3,
      "type": "slider",
      "x": 50,
      "y": 190,
      "inputs": {
        "label": "Amplitude",
        "min": 10,
        "max": 100,
        "default": 50
      }
    },
    {
      "id": 4,
      "type": "loop",
      "x": 300,
      "y": 120,
      "inputs": {
        "start": 0,
        "end": 600,
        "step": 10
      }
    },
    {
      "id": 5,
      "type": "trigonometry",
      "x": 450,
      "y": 120,
      "inputs": {
        "angle": 0,
        "function": "sin"
      }
    },
    {
      "id": 6,
      "type": "multiply",
      "x": 600,
      "y": 120,
      "inputs": {
        "a": 1,
        "b": 50
      }
    },
    {
      "id": 7,
      "type": "draw-line",
      "x": 750,
      "y": 120,
      "inputs": {
        "x1": 0,
        "y1": 200,
        "x2": 10,
        "y2": 190,
        "color": "#667eea",
        "width": 2
      }
    },
    {
      "id": 8,
      "type": "draw-text",
      "x": 50,
      "y": 280,
      "inputs": {
        "text": "y = sin(x)",
        "x": 10,
        "y": 30,
        "color": "#667eea",
        "size": 16
      }
    }
  ],
  "connections": [
    { "from": 2, "to": 5 },
    { "from": 3, "to": 6 },
    { "from": 4, "to": 5 },
    { "from": 5, "to": 6 },
    { "from": 6, "to": 7 }
  ],
  "tags": "mathematics,trigonometry,visualization,calculus"
}
```

## 5. Particle System Simulator

### Purpose
Simulate and visualize particle systems with physics.

### Blocks Configuration
```json
{
  "title": "Particle System",
  "description": "Interactive particle system with gravity and collision",
  "blocks": [
    {
      "id": 1,
      "type": "clear-canvas",
      "x": 50,
      "y": 50,
      "inputs": {}
    },
    {
      "id": 2,
      "type": "slider",
      "x": 50,
      "y": 120,
      "inputs": {
        "label": "Particle Count",
        "min": 10,
        "max": 100,
        "default": 30
      }
    },
    {
      "id": 3,
      "type": "slider",
      "x": 50,
      "y": 190,
      "inputs": {
        "label": "Gravity Strength",
        "min": 0,
        "max": 20,
        "default": 9.8
      }
    },
    {
      "id": 4,
      "type": "array",
      "x": 300,
      "y": 120,
      "inputs": {
        "size": 30,
        "value": 0
      }
    },
    {
      "id": 5,
      "type": "loop",
      "x": 450,
      "y": 120,
      "inputs": {
        "start": 0,
        "end": 30,
        "step": 1
      }
    },
    {
      "id": 6,
      "type": "random",
      "x": 600,
      "y": 50,
      "inputs": {
        "min": 50,
        "max": 550
      }
    },
    {
      "id": 7,
      "type": "random",
      "x": 600,
      "y": 120,
      "inputs": {
        "min": 50,
        "max": 450
      }
    },
    {
      "id": 8,
      "type": "velocity",
      "x": 600,
      "y": 190,
      "inputs": {
        "vx": 5,
        "vy": -10,
        "duration": 0.016
      }
    },
    {
      "id": 9,
      "type": "gravity",
      "x": 750,
      "y": 120,
      "inputs": {
        "mass": 1,
        "g": 9.8
      }
    },
    {
      "id": 10,
      "type": "draw-particle",
      "x": 900,
      "y": 120,
      "inputs": {
        "x": 300,
        "y": 200,
        "radius": 5,
        "color": "#667eea",
        "alpha": 0.8
      }
    }
  ],
  "connections": [
    { "from": 2, "to": 4 },
    { "from": 3, "to": 9 },
    { "from": 4, "to": 5 },
    { "from": 5, "to": 6 },
    { "from": 5, "to": 7 },
    { "from": 6, "to": 10 },
    { "from": 7, "to": 10 },
    { "from": 8, "to": 10 },
    { "from": 9, "to": 8 }
  ],
  "tags": "particles,physics,animation,effects"
}
```

## How to Import These Simulators

### Method 1: Manual Creation
1. Go to course editor
2. Click "Insert Block-based Simulator"
3. Copy the blocks from above
4. Paste configuration into block editor
5. Connect blocks as specified
6. Save course

### Method 2: JSON Import (Future Feature)
```javascript
// Coming soon: Import simulator from JSON file
fetch('/import-simulator', {
    method: 'POST',
    body: simulatorJSON
})
```

### Method 3: Clone from Marketplace
1. Visit marketplace.html
2. Search for simulator
3. Click "Use in Course"
4. Customize if needed

## Learning Objectives

### Gravity Simulator
- Understand gravitational force equation (F = mg)
- Observe force-mass relationship
- Calculate work and energy

### Projectile Motion
- Understand trajectory calculations
- Learn about initial velocity components
- Analyze range and maximum height

### Collision Detection
- Learn distance formulas
- Understand collision boundaries
- Apply physics to game development

### Function Visualizer
- Understand function transformations
- Learn trigonometric relationships
- Visualize function properties

### Particle System
- Understand complex systems
- Learn animation principles
- Apply multiple physics rules

## Customization Tips

1. **Adjust Colors**: Change `color` parameter in draw blocks
2. **Change Speed**: Modify `dt` (delta time) in motion blocks
3. **Adjust Ranges**: Modify slider min/max values
4. **Add More Particles**: Increase `size` in array block
5. **Change Physics**: Adjust gravity and mass values

## Performance Considerations

- Keep block count under 50 for smooth animation
- Use lower particle counts (< 100) on older devices
- Simplify collision detection for large systems
- Cache calculated values when possible

## Troubleshooting

### Simulator Won't Run
- Check all blocks have required inputs
- Verify block connections are valid
- Clear browser cache

### Animation Too Slow
- Reduce particle count
- Simplify block logic
- Use more efficient block types

### Canvas Appears Blank
- Verify draw blocks are included
- Check canvas coordinates
- Ensure clear-canvas isn't hiding content

## Next Steps

1. Create your own simulator variations
2. Share simulators with the community
3. Rate and comment on others' simulators
4. Build upon existing examples
5. Create tutorial simulators for your courses

---

*These examples are educational tools. Feel free to modify, remix, and share!*
