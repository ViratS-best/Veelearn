/**
 * Simulator Fork/Remix System - Handle forking and version tracking
 * ~150 lines
 */

class SimulatorForkSystem {
    constructor(api) {
        this.api = api;
        this.forkHistory = new Map();
    }

    /**
     * Fork a simulator
     * @param {Object} originalSimulator - Original simulator object
     * @param {String} newTitle - Title for fork
     * @param {String} description - Description (optional)
     * @returns {Promise<Object>} Forked simulator
     */
    async forkSimulator(originalSimulator, newTitle, description = '') {
        try {
            if (!originalSimulator || !originalSimulator.id) {
                throw new Error('Invalid simulator to fork');
            }

            const forkData = {
                title: newTitle || `${originalSimulator.title} (Remix)`,
                description: description || `Forked from: ${originalSimulator.title}`,
                blocks: JSON.parse(JSON.stringify(originalSimulator.blocks || [])),
                connections: JSON.parse(JSON.stringify(originalSimulator.connections || [])),
                tags: [...(originalSimulator.tags || []), 'forked'],
                originalSimulatorId: originalSimulator.id,
                originalCreatorId: originalSimulator.creator_id || originalSimulator.creatorId
            };

            // Create the fork via API
            const forked = await this.api.createSimulator(forkData);

            // Track fork relationship
            this.trackFork(originalSimulator.id, forked.id, {
                originalTitle: originalSimulator.title,
                forkTitle: newTitle,
                timestamp: Date.now(),
                forkedBlocks: forkData.blocks.length,
                forkedConnections: forkData.connections.length
            });

            return forked;
        } catch (error) {
            console.error('Failed to fork simulator:', error);
            throw error;
        }
    }

    /**
     * Track fork relationship
     * @param {Number} originalId - Original simulator ID
     * @param {Number} forkedId - Forked simulator ID
     * @param {Object} metadata - Fork metadata
     * @private
     */
    trackFork(originalId, forkedId, metadata = {}) {
        if (!this.forkHistory.has(originalId)) {
            this.forkHistory.set(originalId, []);
        }

        this.forkHistory.get(originalId).push({
            forkedId,
            ...metadata
        });

        // Save to localStorage for persistence
        localStorage.setItem(`fork_history_${originalId}`, JSON.stringify(this.forkHistory.get(originalId)));
    }

    /**
     * Get fork history for a simulator
     * @param {Number} simulatorId - Simulator ID
     * @returns {Array} Fork history
     */
    getForkHistory(simulatorId) {
        const history = this.forkHistory.get(simulatorId);
        if (history) return history;

        // Try to load from localStorage
        const stored = localStorage.getItem(`fork_history_${simulatorId}`);
        if (stored) {
            const parsed = JSON.parse(stored);
            this.forkHistory.set(simulatorId, parsed);
            return parsed;
        }

        return [];
    }

    /**
     * Get all forks of a simulator
     * @param {Number} simulatorId - Original simulator ID
     * @returns {Promise<Array>} All forks
     */
    async getAllForks(simulatorId) {
        try {
            return await this.api.getSimulatorForks(simulatorId);
        } catch (error) {
            console.error('Failed to get forks:', error);
            return [];
        }
    }

    /**
     * Get original simulator (for a forked simulator)
     * @param {Number} forkedId - Forked simulator ID
     * @returns {Promise<Object>} Original simulator
     */
    async getOriginalSimulator(forkedId) {
        try {
            return await this.api.getOriginalSimulator(forkedId);
        } catch (error) {
            console.error('Failed to get original simulator:', error);
            return null;
        }
    }

    /**
     * Create version of simulator
     * @param {Number} simulatorId - Simulator ID
     * @param {String} versionNumber - Version number (e.g., "1.1.0")
     * @param {Object} data - Simulator data
     * @param {String} changelog - Change description
     * @returns {Promise<Object>} Version record
     */
    async createVersion(simulatorId, versionNumber, data, changelog = '') {
        try {
            // In a real implementation, this would call an API endpoint
            // For now, save to localStorage
            const versionKey = `simulator_v_${simulatorId}_${versionNumber}`;
            localStorage.setItem(versionKey, JSON.stringify({
                simulatorId,
                version: versionNumber,
                data,
                changelog,
                createdAt: new Date().toISOString()
            }));

            return {
                simulatorId,
                version: versionNumber,
                changelog,
                createdAt: new Date().toISOString()
            };
        } catch (error) {
            console.error('Failed to create version:', error);
            throw error;
        }
    }

    /**
     * Get version of simulator
     * @param {Number} simulatorId - Simulator ID
     * @param {String} versionNumber - Version number
     * @returns {Object} Version data
     */
    getVersion(simulatorId, versionNumber) {
        try {
            const versionKey = `simulator_v_${simulatorId}_${versionNumber}`;
            const stored = localStorage.getItem(versionKey);
            if (stored) {
                return JSON.parse(stored);
            }
            return null;
        } catch (error) {
            console.error('Failed to get version:', error);
            return null;
        }
    }

    /**
     * Get all versions of simulator
     * @param {Number} simulatorId - Simulator ID
     * @returns {Array} All versions
     */
    getAllVersions(simulatorId) {
        const versions = [];
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && key.startsWith(`simulator_v_${simulatorId}_`)) {
                const version = JSON.parse(localStorage.getItem(key));
                versions.push(version);
            }
        }
        return versions.sort((a, b) => b.createdAt.localeCompare(a.createdAt));
    }

    /**
     * Restore from version
     * @param {Number} simulatorId - Simulator ID
     * @param {String} versionNumber - Version number to restore
     * @returns {Object} Restored simulator data
     */
    restoreFromVersion(simulatorId, versionNumber) {
        try {
            const version = this.getVersion(simulatorId, versionNumber);
            if (!version) {
                throw new Error('Version not found');
            }
            return version.data;
        } catch (error) {
            console.error('Failed to restore version:', error);
            throw error;
        }
    }

    /**
     * Compare two versions
     * @param {Number} simulatorId - Simulator ID
     * @param {String} v1 - Version 1
     * @param {String} v2 - Version 2
     * @returns {Object} Comparison results
     */
    compareVersions(simulatorId, v1, v2) {
        const version1 = this.getVersion(simulatorId, v1);
        const version2 = this.getVersion(simulatorId, v2);

        if (!version1 || !version2) {
            throw new Error('One or both versions not found');
        }

        const data1 = version1.data;
        const data2 = version2.data;

        return {
            blocksAdded: (data2.blocks || []).length - (data1.blocks || []).length,
            blocksRemoved: (data1.blocks || []).length - (data2.blocks || []).length,
            connectionsAdded: (data2.connections || []).length - (data1.connections || []).length,
            connectionsRemoved: (data1.connections || []).length - (data2.connections || []).length,
            v1: v1,
            v2: v2,
            v1Blocks: data1.blocks ? data1.blocks.length : 0,
            v2Blocks: data2.blocks ? data2.blocks.length : 0,
            v1Connections: data1.connections ? data1.connections.length : 0,
            v2Connections: data2.connections ? data2.connections.length : 0
        };
    }

    /**
     * Create version snapshot
     * @param {Number} simulatorId - Simulator ID
     * @param {Object} simulatorData - Full simulator data
     * @returns {String} Version number (auto-generated)
     */
    createSnapshot(simulatorId, simulatorData) {
        const timestamp = Date.now();
        const version = `snap_${timestamp}`;
        this.createVersion(simulatorId, version, simulatorData, `Auto-snapshot at ${new Date().toISOString()}`);
        return version;
    }

    /**
     * Get fork attribution
     * @param {Number} simulatorId - Forked simulator ID
     * @returns {Object} Attribution info
     */
    async getForkAttribution(simulatorId) {
        try {
            const original = await this.getOriginalSimulator(simulatorId);
            if (!original) return null;

            return {
                originallSimulatorId: original.id,
                originalTitle: original.title,
                originalCreator: original.creator || { name: 'Unknown' },
                originalCreatedAt: original.created_at,
                forkedSimulatorId: simulatorId
            };
        } catch (error) {
            console.error('Failed to get fork attribution:', error);
            return null;
        }
    }

    /**
     * Clear fork history
     * @param {Number} simulatorId - Simulator ID (optional - clears all if not provided)
     */
    clearHistory(simulatorId = null) {
        if (simulatorId) {
            this.forkHistory.delete(simulatorId);
            localStorage.removeItem(`fork_history_${simulatorId}`);
        } else {
            this.forkHistory.clear();
            const keys = [];
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                if (key && key.startsWith('fork_history_')) {
                    keys.push(key);
                }
            }
            keys.forEach(key => localStorage.removeItem(key));
        }
    }

    /**
     * Export simulator for sharing
     * @param {Object} simulator - Simulator to export
     * @returns {String} JSON string
     */
    exportSimulator(simulator) {
        const data = {
            title: simulator.title,
            description: simulator.description,
            blocks: simulator.blocks,
            connections: simulator.connections,
            tags: simulator.tags,
            preview: simulator.preview_image,
            exportedAt: new Date().toISOString()
        };
        return JSON.stringify(data, null, 2);
    }

    /**
     * Import simulator from JSON
     * @param {String} jsonStr - JSON string
     * @returns {Object} Imported simulator data
     */
    importSimulator(jsonStr) {
        try {
            const data = JSON.parse(jsonStr);
            return {
                title: data.title || 'Imported Simulator',
                description: data.description || '',
                blocks: data.blocks || [],
                connections: data.connections || [],
                tags: [...(data.tags || []), 'imported'],
                preview_image: data.preview
            };
        } catch (error) {
            console.error('Failed to import simulator:', error);
            throw new Error('Invalid simulator JSON');
        }
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SimulatorForkSystem;
}
