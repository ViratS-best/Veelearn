// ======= INTERACTIVE SLIDER CONFIGURATION =======
// Add these functions to the END of script.js (before the last line)

// Global variable to store current simulator being configured
let currentConfiguringSimulatorId = null;

// Open slider configuration modal
async function openSliderConfigModal(blockId) {
    if (!currentEditingCourseId) {
        alert('Please save the course first before configuring sliders.');
        return;
    }

    currentConfiguringSimulatorId = blockId;
    console.log('📊 Opening slider config for simulator block:', blockId);

    // Find the simulator block in courseBlocks
    const simBlock = courseBlocks.find(b => b.id === blockId);
    if (!simBlock) {
        alert('Simulator block not found');
        return;
    }

    // Simple modal using prompt for now (we'll make it prettier later)
    const message = `🎛️ SLIDER CONFIGURATION (Simulator Block ${blockId})

This feature will be fully implemented in the next update.
For now, sliders can be configured via the backend API.

Would you like to:
1. View existing slider configurations
2. Add a new slider parameter
3. Delete a slider configuration

Enter 1, 2, or 3 (or cancel to close)`;

    const choice = prompt(message);

    if (choice === '1') {
        await viewSliderConfigs();
    } else if (choice === '2') {
        await addSliderConfig();
    } else if (choice === '3') {
        await deleteSliderConfig();
    }
}

// View existing slider configurations
async function viewSliderConfigs() {
    try {
        const response = await fetch(`http://localhost:3000/api/courses/${currentEditingCourseId}/params`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        const result = await response.json();

        if (result.success && result.data.length > 0) {
            const configs = result.data
                .filter(p => p.simulator_block_id == currentConfiguringSimulatorId)
                .map(p => `• ${p.param_label || p.param_name}: ${p.min_value} to ${p.max_value} (step: ${p.step_value})`)
                .join('\n');
            alert(`✅ Configured Sliders:\n\n${configs || 'No sliders configured yet'}`);
        } else {
            alert('No slider configurations found for this simulator.');
        }
    } catch (error) {
        console.error('Error fetching slider configs:', error);
        alert('Error loading slider configurations');
    }
}

// Add new slider configuration (simplified version)
async function addSliderConfig() {
    const paramName = prompt('Enter parameter name (e.g., "radius", "speed", "mass"):');
    if (!paramName) return;

    const paramLabel = prompt(`Display label for "${paramName}":`, paramName);
    const minValue = prompt('Minimum value:', '0');
    const maxValue = prompt('Maximum value:', '100');
    const stepValue = prompt('Step value:', '1');
    const defaultValue = prompt('Default value:', '50');

    try {
        const response = await fetch(`http://localhost:3000/api/courses/${currentEditingCourseId}/simulators/${currentConfiguringSimulatorId}/params`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                block_id: 1, // You'll need to specify which block within the simulator
                param_name: paramName,
                param_label: paramLabel,
                min_value: parseFloat(minValue),
                max_value: parseFloat(maxValue),
                step_value: parseFloat(stepValue),
                default_value: parseFloat(defaultValue)
            })
        });

        const result = await response.json();
        if (result.success) {
            alert('✅ Slider configuration saved!');
        } else {
            alert('Error: ' + result.message);
        }
    } catch (error) {
        console.error('Error saving slider config:', error);
        alert('Error saving slider configuration');
    }
}

// Delete slider configuration
async function deleteSliderConfig() {
    try {
        // First, get all configs to show list
        const response = await fetch(`http://localhost:3000/api/courses/${currentEditingCourseId}/params`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        const result = await response.json();

        if (result.success && result.data.length > 0) {
            const configs = result.data.filter(p => p.simulator_block_id == currentConfiguringSimulatorId);
            if (configs.length === 0) {
                alert('No sliders to delete');
                return;
            }

            const list = configs.map((p, i) => `${i + 1}. ${p.param_label || p.param_name}`).join('\n');
            const index = prompt(`Select slider to delete:\n\n${list}\n\nEnter number:`);

            if (index && configs[parseInt(index) - 1]) {
                const paramId = configs[parseInt(index) - 1].id;
                const deleteResponse = await fetch(`http://localhost:3000/api/courses/${currentEditingCourseId}/params/${paramId}`, {
                    method: 'DELETE',
                    headers: { 'Authorization': `Bearer ${authToken}` }
                });

                const deleteResult = await deleteResponse.json();
                if (deleteResult.success) {
                    alert('✅ Slider configuration deleted!');
                } else {
                    alert('Error: ' + deleteResult.message);
                }
            }
        } else {
            alert('No slider configurations found');
        }
    } catch (error) {
        console.error('Error deleting slider config:', error);
        alert('Error deleting slider configuration');
    }
}

// Make function globally accessible
window.openSliderConfigModal = openSliderConfigModal;
