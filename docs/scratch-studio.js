/**
 * Veelearn Scratch Studio — UI glue: Blockly workspace, sprites, assets, save/publish.
 */
(function () {
  'use strict';

  const API_BASE_URL = (() => {
    if (location.hostname.includes('veelearn.org')) return 'https://api.veelearn.org';
    if (location.hostname.includes('github.io')) return 'https://veelearn.onrender.com';
    if (location.hostname === 'localhost' || location.hostname === '127.0.0.1') return 'http://localhost:3000';
    return location.origin;
  })();

  function authHeaders() {
    const headers = { 'Content-Type': 'application/json' };
    const token = localStorage.getItem('token');
    if (token) headers['Authorization'] = `Bearer ${token}`;
    return headers;
  }

  let workspace = null;
  let stage = null;
  let runtime = null;
  let project = null;
  let selectedId = null; // sprite id or 'stage'
  let courseBlockId = null;
  let editingSimId = null;
  let projectTitle = null;
  let dirty = false;

  function uid(prefix) {
    return (prefix || 'id') + '_' + Math.random().toString(36).slice(2, 9);
  }

  function toast(msg) {
    const el = document.getElementById('toast');
    el.textContent = msg;
    el.style.display = 'block';
    setTimeout(() => { el.style.display = 'none'; }, 2200);
  }

  function emptyProject() {
    const costume = ScratchStageUtils.makeDefaultCostume('costume1', '#6366f1');
    const backdrop = ScratchStageUtils.makeDefaultBackdrop('backdrop1');
    return {
      format: 'veelearn-scratch-1',
      stage: {
        backdrops: [backdrop],
        currentBackdrop: 0,
        workspace: {},
        sounds: [],
        variables: {},
        lists: {}
      },
      sprites: [{
        id: uid('sprite'),
        name: 'Sprite1',
        x: 0,
        y: 0,
        direction: 90,
        size: 100,
        visible: true,
        costumes: [costume],
        currentCostume: 0,
        sounds: [],
        workspace: {},
        variables: {},
        lists: {},
        rotationStyle: 'all around',
        layer: 1
      }],
      globals: { variables: {}, lists: {} }
    };
  }

  function getSelectedSprite() {
    if (selectedId === 'stage') return null;
    return project.sprites.find(s => s.id === selectedId) || null;
  }

  function serializeCurrentWorkspace() {
    if (!workspace) return {};
    try {
      return Blockly.serialization.workspaces.save(workspace);
    } catch (e) {
      console.warn('serialize failed', e);
      return {};
    }
  }

  function loadWorkspaceIntoEditor(serialized) {
    workspace.clear();
    if (serialized && (serialized.blocks || serialized.variables)) {
      try {
        Blockly.serialization.workspaces.load(serialized, workspace);
      } catch (e) {
        console.warn('load workspace failed', e);
      }
    }
  }

  function saveCurrentTargetWorkspace() {
    const data = serializeCurrentWorkspace();
    if (selectedId === 'stage') {
      project.stage.workspace = data;
    } else {
      const s = getSelectedSprite();
      if (s) s.workspace = data;
    }
  }

  function selectTarget(id) {
    if (selectedId && workspace) saveCurrentTargetWorkspace();
    selectedId = id;
    if (id === 'stage') {
      loadWorkspaceIntoEditor(project.stage.workspace);
    } else {
      const s = project.sprites.find(sp => sp.id === id);
      if (s) loadWorkspaceIntoEditor(s.workspace);
    }
    renderSpriteList();
    updateToolbar();
    renderCostumes();
    renderSounds();
    redrawStagePreview();
  }

  function updateToolbar() {
    const isStage = selectedId === 'stage';
    const s = getSelectedSprite();
    document.getElementById('sprite-name').disabled = isStage;
    document.getElementById('sprite-x').disabled = isStage;
    document.getElementById('sprite-y').disabled = isStage;
    document.getElementById('sprite-size').disabled = isStage;
    document.getElementById('sprite-dir').disabled = isStage;
    document.getElementById('btn-show').disabled = isStage;
    document.getElementById('btn-hide').disabled = isStage;

    if (isStage) {
      document.getElementById('sprite-name').value = 'Stage';
      document.getElementById('sprite-x').value = 0;
      document.getElementById('sprite-y').value = 0;
      document.getElementById('sprite-size').value = 100;
      document.getElementById('sprite-dir').value = 90;
    } else if (s) {
      document.getElementById('sprite-name').value = s.name;
      document.getElementById('sprite-x').value = Math.round(s.x);
      document.getElementById('sprite-y').value = Math.round(s.y);
      document.getElementById('sprite-size').value = s.size;
      document.getElementById('sprite-dir').value = s.direction;
      document.getElementById('btn-show').classList.toggle('active', s.visible);
      document.getElementById('btn-hide').classList.toggle('active', !s.visible);
    }
  }

  function renderSpriteList() {
    const grid = document.getElementById('sprites-grid');
    grid.innerHTML = '';
    for (const s of project.sprites) {
      const card = document.createElement('div');
      card.className = 'sprite-card' + (selectedId === s.id ? ' selected' : '');
      const canvas = document.createElement('canvas');
      canvas.width = 64;
      canvas.height = 64;
      const costume = s.costumes[s.currentCostume || 0];
      if (costume) {
        const img = new Image();
        img.onload = () => {
          const ctx = canvas.getContext('2d');
          ctx.clearRect(0, 0, 64, 64);
          const scale = Math.min(64 / img.width, 64 / img.height);
          const w = img.width * scale, h = img.height * scale;
          ctx.drawImage(img, (64 - w) / 2, (64 - h) / 2, w, h);
        };
        img.src = costume.dataUrl;
      }
      const label = document.createElement('div');
      label.className = 'label';
      label.textContent = s.name;
      const trash = document.createElement('button');
      trash.className = 'trash';
      trash.textContent = '×';
      trash.title = 'Delete';
      trash.onclick = (e) => {
        e.stopPropagation();
        if (project.sprites.length <= 1) { toast('Need at least one sprite'); return; }
        if (!confirm('Delete ' + s.name + '?')) return;
        project.sprites = project.sprites.filter(x => x.id !== s.id);
        if (selectedId === s.id) selectTarget(project.sprites[0].id);
        else renderSpriteList();
        dirty = true;
        redrawStagePreview();
      };
      card.appendChild(canvas);
      card.appendChild(label);
      card.appendChild(trash);
      card.onclick = () => selectTarget(s.id);
      grid.appendChild(card);
    }
    const thumb = document.getElementById('stage-thumb');
    thumb.classList.toggle('selected', selectedId === 'stage');
    stage.drawStageThumb(thumb, project);
  }

  function redrawStagePreview() {
    if (runtime && runtime.running) return;
    // Build temp targets from project for preview
    const targets = project.sprites.map(s => ({
      ...s,
      effects: { ghost: 0, brightness: 0, color: 0 },
      bubble: null
    }));
    // Preload then draw
    Promise.all([
      ...project.stage.backdrops.map(b => stage.loadImage(b.dataUrl)),
      ...project.sprites.flatMap(s => s.costumes.map(c => stage.loadImage(c.dataUrl)))
    ]).then(() => {
      stage.draw(project, targets);
      stage.drawStageThumb(document.getElementById('stage-thumb'), project);
    });
  }

  function renderCostumes() {
    const grid = document.getElementById('costume-grid');
    grid.innerHTML = '';
    const isStage = selectedId === 'stage';
    const items = isStage ? project.stage.backdrops : (getSelectedSprite()?.costumes || []);
    const current = isStage ? project.stage.currentBackdrop : (getSelectedSprite()?.currentCostume || 0);

    items.forEach((c, i) => {
      const card = document.createElement('div');
      card.className = 'asset-card' + (i === current ? ' selected' : '');
      const img = document.createElement('img');
      img.src = c.dataUrl;
      const name = document.createElement('div');
      name.className = 'name';
      name.textContent = c.name;
      const meta = document.createElement('div');
      meta.className = 'meta';
      meta.textContent = `${c.width || '?'} × ${c.height || '?'}`;
      const del = document.createElement('button');
      del.className = 'del';
      del.textContent = '×';
      del.onclick = (e) => {
        e.stopPropagation();
        if (items.length <= 1) { toast('Need at least one'); return; }
        items.splice(i, 1);
        if (isStage) {
          project.stage.currentBackdrop = Math.min(project.stage.currentBackdrop, items.length - 1);
        } else {
          const s = getSelectedSprite();
          s.currentCostume = Math.min(s.currentCostume, items.length - 1);
        }
        renderCostumes();
        redrawStagePreview();
        dirty = true;
      };
      card.appendChild(img);
      card.appendChild(name);
      card.appendChild(meta);
      card.appendChild(del);
      card.onclick = () => {
        if (isStage) project.stage.currentBackdrop = i;
        else getSelectedSprite().currentCostume = i;
        renderCostumes();
        renderSpriteList();
        redrawStagePreview();
        dirty = true;
      };
      card.ondblclick = () => {
        const n = prompt('Rename', c.name);
        if (n) { c.name = n; renderCostumes(); dirty = true; }
      };
      grid.appendChild(card);
    });
  }

  function renderSounds() {
    const grid = document.getElementById('sound-grid');
    grid.innerHTML = '';
    const isStage = selectedId === 'stage';
    const items = isStage ? project.stage.sounds : (getSelectedSprite()?.sounds || []);
    items.forEach((s, i) => {
      const card = document.createElement('div');
      card.className = 'asset-card';
      card.innerHTML = `<div style="height:80px;display:flex;align-items:center;justify-content:center;font-size:32px;">🔊</div>`;
      const name = document.createElement('div');
      name.className = 'name';
      name.textContent = s.name;
      const del = document.createElement('button');
      del.className = 'del';
      del.textContent = '×';
      del.onclick = (e) => {
        e.stopPropagation();
        items.splice(i, 1);
        renderSounds();
        dirty = true;
      };
      card.appendChild(name);
      card.appendChild(del);
      card.onclick = () => {
        const a = new Audio(s.dataUrl);
        a.play().catch(() => {});
      };
      grid.appendChild(card);
    });
  }

  function switchTab(tab) {
    document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
    document.getElementById('code-pane').classList.toggle('pane-hidden', tab !== 'code');
    document.getElementById('assets-pane').classList.toggle('pane-hidden', tab !== 'assets');
    document.getElementById('sounds-pane').classList.toggle('pane-hidden', tab !== 'sounds');
    if (tab === 'assets') renderCostumes();
    if (tab === 'sounds') renderSounds();
    if (tab === 'code') {
      setTimeout(() => Blockly.svgResize(workspace), 50);
    }
  }

  function addSprite() {
    saveCurrentTargetWorkspace();
    const costume = ScratchStageUtils.makeDefaultCostume('costume1', '#' + Math.floor(Math.random() * 0xffffff).toString(16).padStart(6, '0'));
    const s = {
      id: uid('sprite'),
      name: 'Sprite' + (project.sprites.length + 1),
      x: 0, y: 0, direction: 90, size: 100, visible: true,
      costumes: [costume], currentCostume: 0, sounds: [],
      workspace: {}, variables: {}, lists: {},
      rotationStyle: 'all around', layer: project.sprites.length + 1
    };
    project.sprites.push(s);
    selectTarget(s.id);
    dirty = true;
  }

  function readFileAsDataURL(file) {
    return new Promise((resolve, reject) => {
      const r = new FileReader();
      r.onload = () => resolve(r.result);
      r.onerror = reject;
      r.readAsDataURL(file);
    });
  }

  async function uploadCostume(file) {
    const dataUrl = await readFileAsDataURL(file);
    const img = new Image();
    await new Promise((res, rej) => { img.onload = res; img.onerror = rej; img.src = dataUrl; });
    const costume = {
      name: file.name.replace(/\.[^.]+$/, '') || 'costume',
      dataUrl,
      width: img.width,
      height: img.height,
      rotationCenterX: img.width / 2,
      rotationCenterY: img.height / 2,
      bitmapResolution: 1
    };
    if (selectedId === 'stage') {
      project.stage.backdrops.push(costume);
      project.stage.currentBackdrop = project.stage.backdrops.length - 1;
    } else {
      const s = getSelectedSprite();
      s.costumes.push(costume);
      s.currentCostume = s.costumes.length - 1;
    }
    renderCostumes();
    renderSpriteList();
    redrawStagePreview();
    dirty = true;
    toast('Asset added');
  }

  async function uploadSound(file) {
    const dataUrl = await readFileAsDataURL(file);
    const sound = { name: file.name.replace(/\.[^.]+$/, '') || 'sound', dataUrl };
    if (selectedId === 'stage') project.stage.sounds.push(sound);
    else getSelectedSprite().sounds.push(sound);
    renderSounds();
    dirty = true;
    toast('Sound added');
  }

  function buildSavePayload() {
    saveCurrentTargetWorkspace();
    // Snapshot current sprite positions from toolbar into project
    return JSON.parse(JSON.stringify(project));
  }

  async function saveToParent() {
    const data = buildSavePayload();
    if (window.opener && courseBlockId) {
      window.opener.postMessage({
        type: 'save-simulator',
        data: {
          format: 'veelearn-scratch-1',
          project: data,
          blocks: data, // stored in courses.blocks as the project JSON
          connections: [],
          sim_type: 'scratch',
          timestamp: Date.now()
        },
        courseBlockId
      }, '*');
      toast('Saved to course');
      dirty = false;
      return;
    }

    const token = localStorage.getItem('token');
    if (!token) {
      alert('Please log in on the main Veelearn site first, then reopen the studio to save.');
      localStorage.setItem('veelearn-scratch-draft', JSON.stringify(data));
      toast('Draft saved locally — log in to save to server');
      dirty = false;
      return;
    }

    // Standalone: update existing sim, or create a new one with a name prompt
    if (editingSimId) {
      try {
        let title = projectTitle || 'My Simulation';
        if (!projectTitle || projectTitle === 'My Simulation' || projectTitle === 'Untitled') {
          const renamed = prompt('Simulator title:', title);
          if (renamed === null) return;
          if (renamed.trim()) {
            title = renamed.trim();
            projectTitle = title;
          }
        }
        const res = await fetch(`${API_BASE_URL}/api/simulators/${editingSimId}`, {
          method: 'PUT',
          headers: authHeaders(),
          credentials: 'include',
          body: JSON.stringify({
            title,
            blocks: data,
            connections: [],
            sim_type: 'scratch'
          })
        });
        const json = await res.json();
        if (json.success) {
          localStorage.setItem('veelearn-scratch-draft', JSON.stringify(data));
          try { localStorage.setItem('veelearn-sims-updated', String(Date.now())); } catch (e) { /* ignore */ }
          toast('Saved to server');
          dirty = false;
          return;
        }
        console.warn('Save failed:', json.message);
        alert('Save failed: ' + (json.message || 'Unknown error'));
      } catch (err) {
        console.error('Save error:', err);
        alert('Save failed — could not reach the backend.');
      }
      localStorage.setItem('veelearn-scratch-draft', JSON.stringify(data));
      toast('Save failed — draft kept locally');
      dirty = false;
      return;
    }

    // New simulator: ask for a name and POST to server
    const title = prompt('Simulator title:', projectTitle || 'My Simulation');
    if (!title) return;
    projectTitle = title.trim() || 'My Simulation';

    try {
      const res = await fetch(`${API_BASE_URL}/api/simulators`, {
        method: 'POST',
        headers: authHeaders(),
        credentials: 'include',
        body: JSON.stringify({
          title: projectTitle,
          description: '',
          blocks: data,
          connections: [],
          is_public: false,
          sim_type: 'scratch',
          preview_image: data.sprites?.[0]?.costumes?.[0]?.dataUrl || null
        })
      });
      const json = await res.json();
      if (json.success) {
        editingSimId = json.data?.simulatorId || json.data?.id || editingSimId;
        localStorage.setItem('veelearn-scratch-draft', JSON.stringify(data));
        try { localStorage.setItem('veelearn-sims-updated', String(Date.now())); } catch (e) { /* ignore */ }
        toast('Saved to server — it will show under Simulator Studio');
        dirty = false;
        return;
      }
      alert('Save failed: ' + (json.message || 'Unknown error') + (res.status === 401 || res.status === 403 ? '\n\nYour session may have expired — log in again on the main site.' : ''));
    } catch (err) {
      console.error(err);
      alert('Save failed — could not reach the backend. Check your connection and login.');
    }

    localStorage.setItem('veelearn-scratch-draft', JSON.stringify(data));
    toast('Draft saved locally');
    dirty = false;
  }

  async function publishSimulator() {
    const token = localStorage.getItem('token');
    if (!token) {
      alert('Please log in on the main Veelearn site first, then reopen the studio to publish.');
      return;
    }
    const title = prompt('Simulator title:', projectTitle || 'My Simulation');
    if (!title) return;
    projectTitle = title;
    const description = prompt('Description (optional):', '') || '';
    const data = buildSavePayload();

    try {
      const isUpdate = !!editingSimId;
      const url = isUpdate
        ? `${API_BASE_URL}/api/simulators/${editingSimId}`
        : `${API_BASE_URL}/api/simulators`;
      const res = await fetch(url, {
        method: isUpdate ? 'PUT' : 'POST',
        headers: authHeaders(),
        credentials: 'include',
        body: JSON.stringify({
          title,
          description,
          blocks: data,
          connections: [],
          is_public: true,
          sim_type: 'scratch',
          preview_image: data.sprites[0]?.costumes[0]?.dataUrl || null
        })
      });
      const json = await res.json();
      if (json.success) {
        if (!isUpdate) editingSimId = json.data?.simulatorId;
        // Ensure it's public
        if (editingSimId) {
          fetch(`${API_BASE_URL}/api/simulators/${editingSimId}/publish`, {
            method: 'POST',
            headers: authHeaders(),
            credentials: 'include',
            body: JSON.stringify({ is_public: true })
          }).catch(() => {});
        }
        try { localStorage.setItem('veelearn-sims-updated', String(Date.now())); } catch (e) { /* ignore */ }
        toast(isUpdate ? 'Updated on marketplace!' : 'Published to marketplace!');
        dirty = false;
        if (window.opener) {
          window.opener.postMessage({ type: 'simulator-published', simulatorId: editingSimId }, '*');
        }
      } else {
        alert('Publish failed: ' + (json.message || 'Unknown error') + (res.status === 401 || res.status === 403 ? '\n\nYour session may have expired — log in again on the main site.' : ''));
      }
    } catch (err) {
      console.error(err);
      alert('Publish failed — could not reach the backend. Check your connection and login.');
    }
  }

  async function exitStudio() {
    await saveToParent();
    if (window.opener) {
      window.opener.postMessage({ type: 'closeBlockSimulator' }, '*');
      window.close();
    } else {
      window.location.href = 'index.html';
    }
  }

  function greenFlag() {
    saveCurrentTargetWorkspace();
    const raw = buildSavePayload();
    // Convert each Blockly workspace serialize → flat blocks map for the runtime
    const prepared = JSON.parse(JSON.stringify(raw));
    prepared.stage.workspace = { blocks: ScratchRuntime.workspaceToBlocksMap(prepared.stage.workspace) };
    for (const s of prepared.sprites) {
      s.workspace = { blocks: ScratchRuntime.workspaceToBlocksMap(s.workspace) };
    }
    runtime.loadProject(prepared);
    // After loadProject clones, targets already have workspace maps from sprites
    for (let i = 0; i < runtime.targets.length; i++) {
      runtime.targets[i].workspace = prepared.sprites[i].workspace;
    }
    runtime.project.stage.workspace = prepared.stage.workspace;
    runtime.greenFlag();
  }

  function stopAll() {
    runtime.stop();
    redrawStagePreview();
  }

  function loadProjectData(data) {
    if (!data) {
      project = emptyProject();
    } else if (data.format === 'veelearn-scratch-1' && data.sprites && data.stage) {
      project = data;
    } else if (data.project && data.project.format === 'veelearn-scratch-1' && data.project.sprites) {
      project = data.project;
    } else if (data.blocks && data.blocks.format === 'veelearn-scratch-1' && data.blocks.sprites) {
      project = data.blocks;
    } else if (data.format === 'veelearn-scratch-1' || data.sim_type === 'scratch') {
      // New scratch marker without full project yet
      project = emptyProject();
    } else {
      // Legacy or empty — start fresh
      project = emptyProject();
    }
    // Ensure ids
    for (const s of project.sprites) {
      if (!s.id) s.id = uid('sprite');
      if (!s.costumes?.length) s.costumes = [ScratchStageUtils.makeDefaultCostume('costume1')];
    }
    if (!project.stage.backdrops?.length) {
      project.stage.backdrops = [ScratchStageUtils.makeDefaultBackdrop('backdrop1')];
    }
    if (!project.globals) project.globals = { variables: {}, lists: {} };
    selectedId = null;
    selectTarget(project.sprites[0].id);
    redrawStagePreview();
  }

  async function loadFromApi(simId) {
    try {
      const res = await fetch(`${API_BASE_URL}/api/simulators/${simId}`, {
        headers: authHeaders(),
        credentials: 'include'
      });
      const json = await res.json();
      if (!json.success) throw new Error(json.message);
      const sim = json.data;
      projectTitle = sim.title || null;
      let blocks = sim.blocks;
      if (typeof blocks === 'string') blocks = JSON.parse(blocks);
      if (blocks?.format === 'veelearn-scratch-1') loadProjectData(blocks);
      else if (blocks?.project) loadProjectData(blocks.project);
      else loadProjectData(null);
      editingSimId = simId;
    } catch (e) {
      console.error(e);
      toast('Failed to load simulator');
      loadProjectData(null);
    }
  }

  function initBlockly() {
    ScratchBlocks.defineBlocks();
    const theme = ScratchBlocks.createDarkTheme();
    workspace = Blockly.inject('blocklyDiv', {
      toolbox: ScratchBlocks.buildToolbox(),
      theme,
      renderer: 'zelos',
      grid: { spacing: 20, length: 3, colour: '#d3dce8', snap: true },
      zoom: { controls: true, wheel: true, startScale: 0.85, maxScale: 2, minScale: 0.4 },
      trashcan: true,
      move: { scrollbars: true, drag: true, wheel: true },
      media: 'https://unpkg.com/blockly@11.1.1/media/'
    });

    workspace.registerButtonCallback('CREATE_VARIABLE', () => {
      const name = prompt('New variable name:');
      if (!name) return;
      const scope = confirm('OK = global (for all sprites)\nCancel = for this sprite only') ? 'global' : 'sprite';
      if (scope === 'global') {
        project.globals.variables[name] = 0;
        try { workspace.createVariable(name); } catch (_) {}
        stage.setMonitor(name, 0, { mode: 'slider', visible: true, min: -100, max: 100 });
      } else {
        const s = getSelectedSprite();
        if (s) {
          s.variables[name] = 0;
          try { workspace.createVariable(name); } catch (_) {}
        }
      }
      dirty = true;
      toast('Variable "' + name + '" created — use it in set/change blocks');
    });
    workspace.registerButtonCallback('CREATE_LIST', () => {
      const name = prompt('New list name:');
      if (!name) return;
      project.globals.lists[name] = [];
      toast('List "' + name + '" created');
      dirty = true;
    });

    workspace.addChangeListener(() => { dirty = true; });
  }

  function bindUI() {
    document.querySelectorAll('.tab').forEach(t => t.addEventListener('click', () => switchTab(t.dataset.tab)));
    document.getElementById('btn-flag').onclick = greenFlag;
    document.getElementById('btn-flag-2').onclick = greenFlag;
    document.getElementById('btn-stop').onclick = stopAll;
    document.getElementById('btn-stop-2').onclick = stopAll;
    document.getElementById('btn-save').onclick = saveToParent;
    document.getElementById('btn-publish').onclick = publishSimulator;
    const mktBtn = document.getElementById('btn-marketplace');
    if (mktBtn) {
      mktBtn.onclick = async () => {
        if (dirty) {
          const saveFirst = confirm('Save your work before opening the Marketplace?');
          if (saveFirst) {
            try { await saveToParent(); } catch (e) { console.warn(e); }
          } else {
            const leave = confirm('Leave without saving and open Marketplace anyway?');
            if (!leave) return;
          }
        }
        window.location.href = 'simulator-marketplace.html';
      };
    }
    document.getElementById('btn-exit').onclick = exitStudio;
    document.getElementById('btn-add-sprite').onclick = addSprite;
    document.getElementById('stage-thumb').onclick = () => selectTarget('stage');
    document.getElementById('btn-add-backdrop').onclick = () => {
      selectTarget('stage');
      switchTab('assets');
      document.getElementById('costume-file').click();
    };
    document.getElementById('btn-upload-costume').onclick = () => document.getElementById('costume-file').click();
    document.getElementById('costume-file').onchange = (e) => {
      const f = e.target.files[0];
      if (f) uploadCostume(f);
      e.target.value = '';
    };
    document.getElementById('btn-paint-costume').onclick = () => {
      const costume = ScratchStageUtils.makeDefaultCostume('costume' + Date.now(), '#8b5cf6');
      if (selectedId === 'stage') {
        project.stage.backdrops.push(costume);
      } else {
        getSelectedSprite().costumes.push(costume);
      }
      renderCostumes();
      redrawStagePreview();
      dirty = true;
    };
    document.getElementById('btn-library-costume').onclick = () => {
      const kind = prompt('Starter: ball, box, arrow, character', 'ball');
      if (!kind) return;
      const costume = ScratchStageUtils.makeLibraryCostume(kind);
      if (selectedId === 'stage') project.stage.backdrops.push(costume);
      else getSelectedSprite().costumes.push(costume);
      renderCostumes();
      renderSpriteList();
      redrawStagePreview();
      dirty = true;
    };
    document.getElementById('btn-upload-sound').onclick = () => document.getElementById('sound-file').click();
    document.getElementById('sound-file').onchange = (e) => {
      const f = e.target.files[0];
      if (f) uploadSound(f);
      e.target.value = '';
    };
    document.getElementById('btn-fullscreen').onclick = () => {
      const wrap = document.getElementById('stage-wrap');
      if (!document.fullscreenElement) wrap.requestFullscreen?.();
      else document.exitFullscreen?.();
    };

    const bindNum = (id, prop, parse = Number) => {
      document.getElementById(id).addEventListener('change', (e) => {
        const s = getSelectedSprite();
        if (!s) return;
        s[prop] = parse(e.target.value);
        redrawStagePreview();
        dirty = true;
      });
    };
    bindNum('sprite-x', 'x');
    bindNum('sprite-y', 'y');
    bindNum('sprite-size', 'size');
    bindNum('sprite-dir', 'direction');
    document.getElementById('sprite-name').addEventListener('change', (e) => {
      const s = getSelectedSprite();
      if (!s) return;
      s.name = e.target.value || s.name;
      renderSpriteList();
      dirty = true;
    });
    document.getElementById('btn-show').onclick = () => {
      const s = getSelectedSprite();
      if (!s) return;
      s.visible = true;
      updateToolbar();
      redrawStagePreview();
    };
    document.getElementById('btn-hide').onclick = () => {
      const s = getSelectedSprite();
      if (!s) return;
      s.visible = false;
      updateToolbar();
      redrawStagePreview();
    };

    window.addEventListener('message', (e) => {
      if (!e.data || !e.data.type) return;
      if (e.data.type === 'load-simulator') {
        const payload = e.data.data || e.data;
        courseBlockId = e.data.courseBlockId || payload.courseBlockId;
        if (payload.format === 'veelearn-scratch-1' || payload.project || (payload.blocks && payload.blocks.format === 'veelearn-scratch-1')) {
          loadProjectData(payload.project || payload.blocks || payload);
        } else if (Array.isArray(payload.blocks) && payload.connections) {
          // Legacy graph — start fresh scratch project
          loadProjectData(null);
          toast('Opened new Scratch studio (legacy format not converted)');
        } else {
          loadProjectData(payload);
        }
        // Acknowledge so the parent stops retrying delivery
        if (e.source && typeof e.source.postMessage === 'function') {
          try { e.source.postMessage({ type: 'load-simulator-ack', courseBlockId }, '*'); } catch (_) {}
        }
      }
    });

    window.addEventListener('beforeunload', (e) => {
      if (dirty) { e.preventDefault(); e.returnValue = ''; }
    });

    window.addEventListener('resize', () => {
      if (workspace) Blockly.svgResize(workspace);
    });
  }

  function init() {
    const canvas = document.getElementById('stageCanvas');
    stage = new ScratchStage(canvas, document.getElementById('monitors'), document.getElementById('speech'));
    runtime = new ScratchRuntime(stage);
    initBlockly();
    bindUI();

    const params = new URLSearchParams(location.search);
    courseBlockId = params.get('courseBlockId');
    const simId = params.get('simId');

    if (simId) {
      loadFromApi(simId);
    } else {
      loadProjectData(null);
      // Tell the opener we're fully initialized so it can post the project.
      // A fixed timeout on the parent side loses the message when Blockly
      // (loaded from a CDN) takes longer than expected to initialize.
      if (window.opener) {
        try { window.opener.postMessage({ type: 'studio-ready', courseBlockId }, '*'); } catch (_) {}
      }
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Expose for debugging
  window.ScratchStudio = {
    getProject: () => project,
    getWorkspace: () => workspace,
    getRuntime: () => runtime,
    greenFlag,
    stopAll
  };
})();
