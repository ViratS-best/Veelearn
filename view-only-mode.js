// ===== VIEW-ONLY / EMBEDDED MODE =====
// ADD THIS CODE to block-simulator.html right BEFORE the line "// Initialize"
// (around line 1031, after the message listeners)

const urlParams = new URLSearchParams(window.location.search);
const isEmbedded = urlParams.get('embedded') === 'true';

if (isEmbedded) {
    console.log('🎬 Running in EMBEDDED VIEW-ONLY mode');

    // Hide sidebar/palette
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) sidebar.style.display = 'none';

    // Adjust main content to full width
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.style.marginLeft = '0';
        mainContent.style.width = '100%';
    }

    // Hide editing buttons (keep only Run/Stop)
    const editButtons = ['clearWorkspace', 'saveSimulator', 'publishSimulator'];
    editButtons.forEach(btnFuncName => {
        const buttons = document.querySelectorAll(`button[onclick*="${btnFuncName}"]`);
        buttons.forEach(btn => btn.style.display = 'none');
    });

    // Change Exit button to Close
    const exitBtn = document.querySelector('button[onclick="exitSimulator()"]');
    if (exitBtn) {
        exitBtn.textContent = '✕ Close';
        exitBtn.style.background = '#6b7280';
    }

    // Make blocks non-draggable and inputs readonly
    const originalRenderBlock = renderBlock;
    renderBlock = function (block, template) {
        originalRenderBlock(block, template);
        const blockEl = workspaceEl.querySelector(`[data-id="${block.id}"]`);
        if (blockEl) {
            blockEl.style.cursor = 'default';
            blockEl.querySelectorAll('input').forEach(input => {
                input.readOnly = true;
                input.style.cursor = 'default';
                input.style.background = '#2a2a3e';
            });
            const deleteBtn = blockEl.querySelector('button');
            if (deleteBtn) deleteBtn.style.display = 'none';
        }
    };

    // Override loadSimulator to auto-run after loading
    const originalLoadSimulator = loadSimulator;
    loadSimulator = function (data) {
        originalLoadSimulator(data);
        // Auto-run simulation after loading
        setTimeout(() => {
            console.log('🚀 Auto-running simulation in view mode');
            runSimulation();
        }, 500);
    };

    logToConsole('🎬 View-only mode active - simulation will auto-run');
}
