/**
 * Physics Engine Library - Vector math, collision detection, integration
 * Provides utilities for physics simulations in block systems
 * ~500 lines
 */

// ===== VECTOR CLASS =====
class Vector {
    constructor(x = 0, y = 0) {
        this.x = x;
        this.y = y;
    }

    // Vector operations
    add(v) {
        return new Vector(this.x + v.x, this.y + v.y);
    }

    subtract(v) {
        return new Vector(this.x - v.x, this.y - v.y);
    }

    scale(scalar) {
        return new Vector(this.x * scalar, this.y * scalar);
    }

    dot(v) {
        return this.x * v.x + this.y * v.y;
    }

    cross(v) {
        return this.x * v.y - this.y * v.x;
    }

    magnitude() {
        return Math.sqrt(this.x * this.x + this.y * this.y);
    }

    magnitudeSquared() {
        return this.x * this.x + this.y * this.y;
    }

    normalize() {
        const mag = this.magnitude();
        if (mag === 0) return new Vector(0, 0);
        return this.scale(1 / mag);
    }

    distance(v) {
        return this.subtract(v).magnitude();
    }

    angle() {
        return Math.atan2(this.y, this.x);
    }

    rotate(angle) {
        const cos = Math.cos(angle);
        const sin = Math.sin(angle);
        return new Vector(
            this.x * cos - this.y * sin,
            this.x * sin + this.y * cos
        );
    }

    clone() {
        return new Vector(this.x, this.y);
    }

    copy() {
        return new Vector(this.x, this.y);
    }

    // Static methods
    static add(v1, v2) {
        return v1.add(v2);
    }

    static subtract(v1, v2) {
        return v1.subtract(v2);
    }

    static dot(v1, v2) {
        return v1.dot(v2);
    }

    static cross(v1, v2) {
        return v1.cross(v2);
    }

    static distance(v1, v2) {
        return v1.distance(v2);
    }

    static normalize(v) {
        return v.normalize();
    }

    static lerp(v1, v2, t) {
        return new Vector(
            v1.x + (v2.x - v1.x) * t,
            v1.y + (v2.y - v1.y) * t
        );
    }

    static zero() {
        return new Vector(0, 0);
    }

    static one() {
        return new Vector(1, 1);
    }

    static fromAngle(angle, magnitude = 1) {
        return new Vector(
            Math.cos(angle) * magnitude,
            Math.sin(angle) * magnitude
        );
    }
}

// ===== COLLISION DETECTION =====
const Collision = {
    /**
     * Circle-circle collision detection
     * @param {Object} c1 - Circle 1 {x, y, r}
     * @param {Object} c2 - Circle 2 {x, y, r}
     * @returns {Object} Collision info {colliding, distance, overlap, normal}
     */
    circleCircle(c1, c2) {
        const dx = c2.x - c1.x;
        const dy = c2.y - c1.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        const minDistance = c1.r + c2.r;
        const colliding = distance < minDistance;

        return {
            colliding,
            distance,
            overlap: Math.max(0, minDistance - distance),
            normal: distance > 0 ? new Vector(dx / distance, dy / distance) : new Vector(1, 0),
            mtv: colliding ? new Vector(dx / distance * (minDistance - distance), dy / distance * (minDistance - distance)) : new Vector(0, 0)
        };
    },

    /**
     * AABB (axis-aligned bounding box) collision
     * @param {Object} r1 - Rectangle 1 {x, y, w, h}
     * @param {Object} r2 - Rectangle 2 {x, y, w, h}
     * @returns {Object} Collision info {colliding, overlap}
     */
    aabb(r1, r2) {
        const colliding = r1.x < r2.x + r2.w &&
                         r1.x + r1.w > r2.x &&
                         r1.y < r2.y + r2.h &&
                         r1.y + r1.h > r2.y;

        if (!colliding) {
            return { colliding: false, overlap: 0 };
        }

        const overlapX = Math.min(r1.x + r1.w, r2.x + r2.w) - Math.max(r1.x, r2.x);
        const overlapY = Math.min(r1.y + r1.h, r2.y + r2.h) - Math.max(r1.y, r2.y);
        const overlap = Math.min(overlapX, overlapY);

        return {
            colliding: true,
            overlap,
            overlapX,
            overlapY
        };
    },

    /**
     * Point in circle detection
     * @param {Object} point - Point {x, y}
     * @param {Object} circle - Circle {x, y, r}
     * @returns {Boolean} Is point in circle
     */
    pointCircle(point, circle) {
        const dx = point.x - circle.x;
        const dy = point.y - circle.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        return distance <= circle.r;
    },

    /**
     * Point in rectangle detection
     * @param {Object} point - Point {x, y}
     * @param {Object} rect - Rectangle {x, y, w, h}
     * @returns {Boolean} Is point in rectangle
     */
    pointRect(point, rect) {
        return point.x >= rect.x &&
               point.x <= rect.x + rect.w &&
               point.y >= rect.y &&
               point.y <= rect.y + rect.h;
    },

    /**
     * Line-circle intersection
     * @param {Vector} p1 - Line start
     * @param {Vector} p2 - Line end
     * @param {Object} circle - Circle {x, y, r}
     * @returns {Object} Intersection info {intersects, points, distance}
     */
    lineCircle(p1, p2, circle) {
        const c = new Vector(circle.x, circle.y);
        const d = p2.subtract(p1);
        const f = p1.subtract(c);
        
        const a = d.dot(d);
        const b = 2 * f.dot(d);
        const c_coef = f.dot(f) - circle.r * circle.r;
        const discriminant = b * b - 4 * a * c_coef;

        if (discriminant < 0) {
            return { intersects: false, points: [] };
        }

        const t1 = (-b - Math.sqrt(discriminant)) / (2 * a);
        const t2 = (-b + Math.sqrt(discriminant)) / (2 * a);

        const points = [];
        if (t1 >= 0 && t1 <= 1) {
            points.push(p1.add(d.scale(t1)));
        }
        if (t2 >= 0 && t2 <= 1) {
            points.push(p1.add(d.scale(t2)));
        }

        return {
            intersects: points.length > 0,
            points,
            distance: points.length > 0 ? p1.distance(points[0]) : Infinity
        };
    }
};

// ===== PHYSICS INTEGRATORS =====
const Physics = {
    /**
     * Euler integration (basic)
     * @param {Vector} pos - Current position
     * @param {Vector} vel - Current velocity
     * @param {Vector} acc - Current acceleration
     * @param {Number} dt - Delta time
     * @returns {Object} {newPos, newVel}
     */
    eulerIntegrate(pos, vel, acc, dt) {
        const newVel = vel.add(acc.scale(dt));
        const newPos = pos.add(newVel.scale(dt));
        return { newPos, newVel };
    },

    /**
     * Semi-implicit Euler (more stable)
     * @param {Vector} pos - Current position
     * @param {Vector} vel - Current velocity
     * @param {Vector} acc - Current acceleration
     * @param {Number} dt - Delta time
     * @returns {Object} {newPos, newVel}
     */
    semiImplicitEuler(pos, vel, acc, dt) {
        const newVel = vel.add(acc.scale(dt));
        const newPos = pos.add(newVel.scale(dt));
        return { newPos, newVel };
    },

    /**
     * Verlet integration (momentum-based, good for constraints)
     * @param {Vector} pos - Current position
     * @param {Vector} prevPos - Previous position
     * @param {Vector} acc - Acceleration
     * @param {Number} dt - Delta time
     * @returns {Vector} New position
     */
    verletIntegrate(pos, prevPos, acc, dt) {
        const vel = pos.subtract(prevPos);
        const newPos = pos.add(vel).add(acc.scale(dt * dt));
        return newPos;
    },

    /**
     * Apply damping (friction)
     * @param {Vector} vel - Velocity
     * @param {Number} damping - Damping factor (0-1)
     * @param {Number} dt - Delta time
     * @returns {Vector} Damped velocity
     */
    applyDamping(vel, damping, dt) {
        const factor = Math.pow(1 - damping, dt);
        return vel.scale(factor);
    },

    /**
     * Calculate spring force
     * @param {Vector} pos - Current position
     * @param {Vector} targetPos - Target position
     * @param {Number} k - Spring constant
     * @param {Number} c - Damping coefficient
     * @param {Vector} vel - Current velocity
     * @returns {Vector} Force
     */
    springForce(pos, targetPos, k, c, vel) {
        const offset = targetPos.subtract(pos);
        const force = offset.scale(k).subtract(vel.scale(c));
        return force;
    },

    /**
     * Calculate gravity force
     * @param {Number} mass - Object mass
     * @param {Number} g - Gravity (default 9.8)
     * @returns {Vector} Gravity force
     */
    gravity(mass, g = 9.8) {
        return new Vector(0, mass * g);
    },

    /**
     * Calculate air resistance
     * @param {Vector} vel - Velocity
     * @param {Number} dragCoefficient - Drag coefficient
     * @param {Number} area - Cross-sectional area
     * @returns {Vector} Drag force
     */
    drag(vel, dragCoefficient = 0.5, area = 1) {
        const speed = vel.magnitude();
        if (speed === 0) return new Vector(0, 0);
        const dragMagnitude = 0.5 * dragCoefficient * area * speed * speed;
        return vel.normalize().scale(-dragMagnitude);
    }
};

// ===== CONSTRAINTS =====
const Constraint = {
    /**
     * Clamp value between min and max
     * @param {Number} value - Value to clamp
     * @param {Number} min - Minimum value
     * @param {Number} max - Maximum value
     * @returns {Number} Clamped value
     */
    clamp(value, min, max) {
        return Math.max(min, Math.min(max, value));
    },

    /**
     * Clamp vector
     * @param {Vector} v - Vector to clamp
     * @param {Number} maxMagnitude - Maximum magnitude
     * @returns {Vector} Clamped vector
     */
    clampVector(v, maxMagnitude) {
        const mag = v.magnitude();
        if (mag > maxMagnitude) {
            return v.normalize().scale(maxMagnitude);
        }
        return v;
    },

    /**
     * Pin constraint - keep position close to target
     * @param {Vector} pos - Current position
     * @param {Vector} targetPos - Target position
     * @param {Number} stiffness - Constraint stiffness (0-1)
     * @returns {Vector} Corrected position
     */
    pin(pos, targetPos, stiffness = 1) {
        const offset = targetPos.subtract(pos);
        return pos.add(offset.scale(stiffness));
    },

    /**
     * Distance constraint - maintain distance between objects
     * @param {Vector} pos1 - Position 1
     * @param {Vector} pos2 - Position 2
     * @param {Number} distance - Desired distance
     * @param {Number} stiffness - Constraint stiffness
     * @returns {Object} {correctedPos1, correctedPos2}
     */
    distance(pos1, pos2, distance, stiffness = 1) {
        const delta = pos2.subtract(pos1);
        const currentDist = delta.magnitude();
        
        if (currentDist === 0) return { correctedPos1: pos1, correctedPos2: pos2 };

        const correction = (currentDist - distance) / 2;
        const correctionDir = delta.normalize().scale(correction * stiffness);

        return {
            correctedPos1: pos1.add(correctionDir),
            correctedPos2: pos2.subtract(correctionDir)
        };
    },

    /**
     * Angle constraint - keep angle between three points
     * @param {Vector} p1 - First point
     * @param {Vector} pivot - Pivot point
     * @param {Vector} p2 - Third point
     * @param {Number} targetAngle - Desired angle (radians)
     * @param {Number} stiffness - Constraint stiffness
     * @returns {Vector} Corrected p2 position
     */
    angle(p1, pivot, p2, targetAngle, stiffness = 1) {
        const v1 = p1.subtract(pivot);
        const v2 = p2.subtract(pivot);
        
        const angle1 = Math.atan2(v1.y, v1.x);
        const angle2 = Math.atan2(v2.y, v2.x);
        let angleDiff = angle2 - angle1;

        // Normalize angle difference
        while (angleDiff > Math.PI) angleDiff -= 2 * Math.PI;
        while (angleDiff < -Math.PI) angleDiff += 2 * Math.PI;

        const correction = angleDiff - targetAngle;
        const correctedAngle = angle2 - correction * stiffness;

        const distance = v2.magnitude();
        return pivot.add(Vector.fromAngle(correctedAngle, distance));
    }
};

// ===== UTILITY FUNCTIONS =====
const PhysicsUtils = {
    /**
     * Calculate kinetic energy
     * @param {Number} mass - Mass
     * @param {Vector} vel - Velocity
     * @returns {Number} Kinetic energy
     */
    kineticEnergy(mass, vel) {
        const vMag = vel.magnitude();
        return 0.5 * mass * vMag * vMag;
    },

    /**
     * Calculate potential energy
     * @param {Number} mass - Mass
     * @param {Number} height - Height
     * @param {Number} g - Gravity
     * @returns {Number} Potential energy
     */
    potentialEnergy(mass, height, g = 9.8) {
        return mass * g * height;
    },

    /**
     * Calculate momentum
     * @param {Number} mass - Mass
     * @param {Vector} vel - Velocity
     * @returns {Vector} Momentum
     */
    momentum(mass, vel) {
        return vel.scale(mass);
    },

    /**
     * Elastic collision response
     * @param {Object} obj1 - Object 1 {mass, vel}
     * @param {Object} obj2 - Object 2 {mass, vel}
     * @returns {Object} {vel1, vel2} - New velocities
     */
    elasticCollision(obj1, obj2) {
        const m1 = obj1.mass;
        const m2 = obj2.mass;
        const v1 = obj1.vel;
        const v2 = obj2.vel;

        const newV1 = v1.scale((m1 - m2) / (m1 + m2)).add(v2.scale(2 * m2 / (m1 + m2)));
        const newV2 = v2.scale((m2 - m1) / (m1 + m2)).add(v1.scale(2 * m1 / (m1 + m2)));

        return { vel1: newV1, vel2: newV2 };
    },

    /**
     * Inelastic collision response
     * @param {Object} obj1 - Object 1 {mass, vel}
     * @param {Object} obj2 - Object 2 {mass, vel}
     * @param {Number} restitution - Bounciness (0-1)
     * @returns {Object} {vel1, vel2} - New velocities
     */
    inelasticCollision(obj1, obj2, restitution = 0.8) {
        const m1 = obj1.mass;
        const m2 = obj2.mass;
        const v1 = obj1.vel;
        const v2 = obj2.vel;

        const newV1 = v1.scale((m1 - restitution * m2) / (m1 + m2)).add(v2.scale(m2 * (1 + restitution) / (m1 + m2)));
        const newV2 = v2.scale((m2 - restitution * m1) / (m1 + m2)).add(v1.scale(m1 * (1 + restitution) / (m1 + m2)));

        return { vel1: newV1, vel2: newV2 };
    }
};

// Export for use in Node/browser environments
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        Vector,
        Collision,
        Physics,
        Constraint,
        PhysicsUtils
    };
}
