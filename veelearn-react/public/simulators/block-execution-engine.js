/**
 * BLOCK EXECUTION ENGINE - FIXED & ENHANCED
 * Handles: dependency resolution, execution, validation, timeout protection, debugging
 * Features: Circular dependency detection, input validation, error handling, performance monitoring
 * Version: 2.1 - Production Ready
 */

class BlockExecutionEngine {
    constructor(timeout = 5000) {
        this.timeout = timeout; // 5 second default timeout
        this.executionHistory = [];
        this.blockStates = new Map();
        this.executionTimes = new Map();
        this.errors = [];
        this.maxIterations = 1000; // Prevent infinite loops
    }

    /**
     * Main execution method - Execute blocks in dependency order with full error handling
     * @param {Array} blocks - Array of block objects
     * @param {Object} initialState - Starting state
     * @param {Object} context - Rendering context {ctx, canvas, frameCount}
     * @returns {Promise<Object>} Final execution state
     */
    async executeBlocks(blocks, initialState = {}, context = {}) {
        try {
            // Validation phase
            this.validateBlocks(blocks);
            
            // Topological sort - order blocks by dependencies
            const sorted = this.topologicalSort(blocks);
            
            // Detect circular dependencies
            if (sorted.length !== blocks.length) {
                throw new Error('Circular dependency detected in blocks');
            }

            // Execute with timeout protection
            const result = await this.executeWithTimeout(() => {
                return this.executeSequentially(sorted, initialState, context, blocks);
            }, this.timeout);

            return result;
        } catch (error) {
            const errorObj = {
                timestamp: Date.now(),
                message: error.message,
                stack: error.stack,
                type: error.name || 'ExecutionError'
            };
            this.errors.push(errorObj);
            console.error('[BlockEngine] Execution failed:', errorObj);
            throw error;
        }
    }

    /**
     * Topological sort using Kahn's algorithm - Order blocks by dependencies
     * Detects cycles and returns blocks in execution order
     * @param {Array} blocks - Array of blocks with connections
     * @returns {Array} Sorted block array (same length if no cycle)
     */
    topologicalSort(blocks) {
        const adjacency = new Map();
        const inDegree = new Map();
        const blockMap = new Map();
        const blockIdSet = new Set();

        // Initialize data structures
        blocks.forEach(block => {
            blockMap.set(block.id, block);
            blockIdSet.add(block.id);
            adjacency.set(block.id, []);
            inDegree.set(block.id, 0);
        });

        // Build dependency graph from connections
        blocks.forEach(block => {
            if (block.connections && Array.isArray(block.connections)) {
                block.connections.forEach(conn => {
                    // Only add if both blocks exist
                    if (blockIdSet.has(block.id) && blockIdSet.has(conn.targetBlockId)) {
                        adjacency.get(block.id).push(conn.targetBlockId);
                        inDegree.set(conn.targetBlockId, (inDegree.get(conn.targetBlockId) || 0) + 1);
                    }
                });
            }
        });

        // Kahn's algorithm for topological sort
        const queue = [];
        inDegree.forEach((degree, blockId) => {
            if (degree === 0) {
                queue.push(blockId);
            }
        });

        const sorted = [];
        const visited = new Set();

        while (queue.length > 0) {
            const blockId = queue.shift();
            sorted.push(blockMap.get(blockId));
            visited.add(blockId);

            // Process neighbors
            (adjacency.get(blockId) || []).forEach(neighborId => {
                const newDegree = inDegree.get(neighborId) - 1;
                inDegree.set(neighborId, newDegree);
                if (newDegree === 0) {
                    queue.push(neighborId);
                }
            });
        }

        // Check for cycles
        if (sorted.length !== blocks.length) {
            const cycleBlocks = blocks.filter(b => !visited.has(b.id));
            console.error('[BlockEngine] Cycle detected in blocks:', cycleBlocks.map(b => b.id));
        }

        return sorted;
    }

    /**
     * Execute blocks sequentially in order
     * @private
     */
    executeSequentially(sortedBlocks, initialState, context, allBlocks) {
        const blockValues = new Map(); // Store output values from each block
        let iterationCount = 0;

        for (const block of sortedBlocks) {
            if (iterationCount++ > this.maxIterations) {
                throw new Error('Max iteration count exceeded - possible infinite loop');
            }

            // Resolve all inputs for this block
            const resolvedInputs = this.resolveInputs(block, blockValues, allBlocks);

            // Execute the block
            const startTime = performance.now();
            let outputs = {};

            try {
                // Get template for this block type
                const template = blockTemplates ? blockTemplates[block.type] : null;
                
                if (!template) {
                    console.warn(`[BlockEngine] No template for block type: ${block.type}`);
                    continue;
                }

                // Validate inputs against template
                this.validateBlockInputs(block, template, resolvedInputs);

                // Execute with context (canvas, ctx, frameCount, etc)
                outputs = template.execute(resolvedInputs, context) || {};

                const executionTime = performance.now() - startTime;
                this.executionTimes.set(block.id, executionTime);

                // Warn if block takes too long
                if (executionTime > 16) {
                    console.warn(`[BlockEngine] Block ${block.id} took ${executionTime.toFixed(2)}ms (>16ms for 60FPS)`);
                }

            } catch (error) {
                console.error(`[BlockEngine] Error executing block ${block.id}:`, error);
                throw new Error(`Block ${block.type} (${block.id}) failed: ${error.message}`);
            }

            // Store outputs for dependent blocks
            if (template && template.outputs && template.outputs.length > 0) {
                blockValues.set(block.id, outputs);
            }
        }

        return { state: initialState, blockValues: Object.fromEntries(blockValues) };
    }

    /**
     * Resolve block inputs from either connections or default values
     * @private
     */
    resolveInputs(block, blockValues, allBlocks) {
        const resolved = {};
        const template = blockTemplates ? blockTemplates[block.type] : null;

        if (!template || !template.inputs) {
            return block.inputs || {};
        }

        template.inputs.forEach(inputDef => {
            const inputName = inputDef.name;
            
            // Check if there's a connection for this input
            let hasConnection = false;
            if (block.connections) {
                block.connections.forEach(conn => {
                    if (conn.toInput === inputName || conn.toInputType === inputName) {
                        hasConnection = true;
                        const fromBlock = allBlocks.find(b => b.id === conn.from || b.id === conn.fromBlockId);
                        const fromTemplate = blockTemplates ? blockTemplates[fromBlock?.type] : null;
                        const fromOutputs = blockValues.get(conn.from || conn.fromBlockId);

                        if (fromOutputs && fromTemplate?.outputs) {
                            const outputName = fromTemplate.outputs[0]; // First output
                            resolved[inputName] = fromOutputs[outputName];
                        } else {
                            resolved[inputName] = block.inputs?.[inputName] || inputDef.default || 0;
                        }
                    }
                });
            }

            // If no connection, use default or block's input value
            if (!hasConnection) {
                resolved[inputName] = block.inputs?.[inputName] ?? inputDef.default ?? 0;
            }
        });

        return resolved;
    }

    /**
     * Validate all blocks before execution
     * @private
     */
    validateBlocks(blocks) {
        if (!Array.isArray(blocks)) {
            throw new Error('Blocks must be an array');
        }

        if (blocks.length === 0) {
            throw new Error('No blocks to execute');
        }

        blocks.forEach((block, index) => {
            if (!block.id) throw new Error(`Block ${index} has no id`);
            if (!block.type) throw new Error(`Block ${index} has no type`);
            if (!blockTemplates || !blockTemplates[block.type]) {
                console.warn(`[BlockEngine] Unknown block type: ${block.type}`);
            }
        });
    }

    /**
     * Validate block inputs against template
     * @private
     */
    validateBlockInputs(block, template, inputs) {
        if (!template.inputs) return;

        template.inputs.forEach(inputDef => {
            const value = inputs[inputDef.name];
            
            // Type checking
            if (inputDef.type === 'number' && typeof value !== 'number' && value !== undefined) {
                console.warn(`[BlockEngine] Block ${block.id}: Input "${inputDef.name}" expected number, got ${typeof value}`);
            }
        });
    }

    /**
     * Execute function with timeout protection
     * @private
     */
    executeWithTimeout(fn, timeout = 5000) {
        return new Promise((resolve, reject) => {
            let completed = false;
            const timeoutId = setTimeout(() => {
                if (!completed) {
                    completed = true;
                    reject(new Error(`Execution timeout after ${timeout}ms - blocks may have infinite loop`));
                }
            }, timeout);

            try {
                const result = fn();
                if (result instanceof Promise) {
                    result
                        .then(res => {
                            if (!completed) {
                                completed = true;
                                clearTimeout(timeoutId);
                                resolve(res);
                            }
                        })
                        .catch(err => {
                            if (!completed) {
                                completed = true;
                                clearTimeout(timeoutId);
                                reject(err);
                            }
                        });
                } else {
                    if (!completed) {
                        completed = true;
                        clearTimeout(timeoutId);
                        resolve(result);
                    }
                }
            } catch (error) {
                if (!completed) {
                    completed = true;
                    clearTimeout(timeoutId);
                    reject(error);
                }
            }
        });
    }

    /**
     * Debug a specific block
     * @param {String} blockId - Block ID to debug
     * @param {Object} inputs - Resolved inputs
     * @param {Object} outputs - Block outputs
     */
    debugBlock(blockId, inputs, outputs) {
        const entry = {
            timestamp: Date.now(),
            blockId,
            inputs,
            outputs,
            executionTime: this.executionTimes.get(blockId)
        };
        this.executionHistory.push(entry);
        console.log('[BlockEngine] Debug:', entry);
        return entry;
    }

    /**
     * Get execution statistics
     */
    getStats() {
        const times = Array.from(this.executionTimes.values());
        return {
            totalBlocks: this.executionTimes.size,
            totalTime: times.reduce((a, b) => a + b, 0),
            avgTime: times.length > 0 ? times.reduce((a, b) => a + b, 0) / times.length : 0,
            maxTime: Math.max(...times, 0),
            minTime: times.length > 0 ? Math.min(...times) : 0,
            errors: this.errors.length
        };
    }

    /**
     * Clear history and errors
     */
    reset() {
        this.executionHistory = [];
        this.blockStates.clear();
        this.executionTimes.clear();
        this.errors = [];
    }
}

// Export for use in browser
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BlockExecutionEngine;
}
