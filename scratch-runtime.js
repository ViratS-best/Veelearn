/**
 * Veelearn Scratch runtime: compile Blockly JSON → cooperative generator threads.
 */
(function (global) {
  'use strict';

  const HAT_TYPES = new Set([
    'event_whenflagclicked',
    'event_whenkeypressed',
    'event_whenthisspriteclicked',
    'event_whenbackdropswitchesto',
    'event_whenbroadcastreceived',
    'control_start_as_clone',
    'procedures_definition'
  ]);

  function degToRad(d) { return d * Math.PI / 180; }
  function wrapDir(d) {
    while (d > 180) d -= 360;
    while (d <= -180) d += 360;
    return d;
  }

  class ScratchRuntime {
    constructor(stage) {
      this.stage = stage;
      this.project = null;
      this.targets = []; // live runtime targets (sprites + clones)
      this.threads = [];
      this.running = false;
      this.raf = null;
      this.globals = { variables: {}, lists: {} };
      this.procedures = new Map(); // name -> {workspaceId, hatBlockId} per target
      this.broadcastWaiters = [];
      this.audioElements = [];
      this.volume = 100;
      this._keyHatsFired = new Set();
      this._onClick = null;

      stage.onSliderChange = (name, value) => {
        this.setVar(null, name, value);
      };
    }

    loadProject(project) {
      this.stop();
      this.project = JSON.parse(JSON.stringify(project));
      this.globals = {
        variables: { ...(project.globals?.variables || {}) },
        lists: Object.fromEntries(
          Object.entries(project.globals?.lists || {}).map(([k, v]) => [k, [...(v || [])]])
        )
      };
      this.targets = [];
      // Stage as target 0 conceptually — sprites only for drawing
      for (const s of this.project.sprites) {
        this.targets.push(this._makeTarget(s, false));
      }
      this._preloadImages();
      this.stage.draw(this.project, this.targets);
      this._syncMonitors();
    }

    _makeTarget(spriteData, isClone) {
      return {
        id: spriteData.id || ('sprite_' + Math.random().toString(36).slice(2)),
        name: spriteData.name,
        x: spriteData.x || 0,
        y: spriteData.y || 0,
        direction: spriteData.direction ?? 90,
        size: spriteData.size ?? 100,
        visible: spriteData.visible !== false,
        costumes: spriteData.costumes || [],
        sounds: spriteData.sounds || [],
        currentCostume: spriteData.currentCostume || 0,
        rotationStyle: spriteData.rotationStyle || 'all around',
        effects: { ghost: 0, brightness: 0, color: 0 },
        layer: spriteData.layer || 0,
        variables: { ...(spriteData.variables || {}) },
        lists: Object.fromEntries(
          Object.entries(spriteData.lists || {}).map(([k, v]) => [k, [...(v || [])]])
        ),
        workspace: spriteData.workspace || {},
        bubble: null,
        isClone,
        draggable: false,
        volume: 100
      };
    }

    async _preloadImages() {
      for (const bd of this.project.stage.backdrops || []) {
        await this.stage.loadImage(bd.dataUrl);
      }
      for (const t of this.targets) {
        for (const c of t.costumes) {
          await this.stage.loadImage(c.dataUrl);
        }
      }
    }

    _syncMonitors() {
      for (const [name, val] of Object.entries(this.globals.variables)) {
        const mon = this.stage.monitors.get(name);
        if (mon && mon.visible !== false) {
          this.stage.setMonitor(name, val, { mode: mon.mode });
        }
      }
    }

    getVar(target, name) {
      if (target && Object.prototype.hasOwnProperty.call(target.variables, name)) {
        return target.variables[name];
      }
      if (Object.prototype.hasOwnProperty.call(this.globals.variables, name)) {
        return this.globals.variables[name];
      }
      // Auto-create global
      this.globals.variables[name] = 0;
      return 0;
    }

    setVar(target, name, value) {
      if (target && Object.prototype.hasOwnProperty.call(target.variables, name)) {
        target.variables[name] = value;
      } else {
        this.globals.variables[name] = value;
      }
      const mon = this.stage.monitors.get(name);
      if (mon && mon.visible !== false) {
        this.stage.setMonitor(name, value);
      }
    }

    getList(target, name) {
      if (target && target.lists[name]) return target.lists[name];
      if (!this.globals.lists[name]) this.globals.lists[name] = [];
      return this.globals.lists[name];
    }

    greenFlag() {
      this.stop(false);
      this.running = true;
      this.stage.resetTimer();
      this.threads = [];
      this._keyHatsFired.clear();

      // Reset sprites to saved positions from project (not clones)
      this.targets = this.targets.filter(t => !t.isClone);
      for (let i = 0; i < this.project.sprites.length; i++) {
        const src = this.project.sprites[i];
        const t = this.targets[i];
        if (!t) continue;
        t.x = src.x || 0;
        t.y = src.y || 0;
        t.direction = src.direction ?? 90;
        t.size = src.size ?? 100;
        t.visible = src.visible !== false;
        t.currentCostume = src.currentCostume || 0;
        t.effects = { ghost: 0, brightness: 0, color: 0 };
        t.bubble = null;
        t.variables = { ...(src.variables || {}) };
      }

      for (const t of this.targets) {
        this._startHats(t, 'event_whenflagclicked');
      }
      // Stage hats
      this._startStageHats('event_whenflagclicked');

      this._bindRuntimeEvents();
      this._loop();
    }

    stop(clearRunning = true) {
      if (clearRunning) this.running = false;
      this.threads = [];
      if (this.raf) {
        cancelAnimationFrame(this.raf);
        this.raf = null;
      }
      for (const a of this.audioElements) {
        try { a.pause(); } catch (_) {}
      }
      this.audioElements = [];
      this._unbindRuntimeEvents();
      for (const t of this.targets) t.bubble = null;
      if (this.project) this.stage.draw(this.project, this.targets);
    }

    _bindRuntimeEvents() {
      this._onKeyDown = (e) => {
        if (!this.running) return;
        const k = this.stage.normalizeKey(e.key);
        if (!k) return;
        const fireKey = (key) => {
          for (const t of this.targets) {
            this._startHats(t, 'event_whenkeypressed', (b) => {
              const opt = b.fields?.KEY_OPTION;
              return opt === key || opt === 'any';
            });
          }
          this._startStageHats('event_whenkeypressed', (b) => {
            const opt = b.fields?.KEY_OPTION;
            return opt === key || opt === 'any';
          });
        };
        fireKey(k);
      };
      this._onCanvasClick = (e) => {
        if (!this.running) return;
        const rect = this.stage.canvas.getBoundingClientRect();
        const cx = ((e.clientX - rect.left) / rect.width) * 480;
        const cy = ((e.clientY - rect.top) / rect.height) * 360;
        const p = global.ScratchStageUtils.canvasToScratch(cx, cy);
        // Topmost sprite under point
        const sorted = [...this.targets].filter(t => t.visible).sort((a, b) => (b.layer || 0) - (a.layer || 0));
        for (const t of sorted) {
          if (this.stage.touchingMouse({ ...t, x: t.x, y: t.y }) || this._pointInTarget(t, p.x, p.y)) {
            this._startHats(t, 'event_whenthisspriteclicked');
            break;
          }
        }
      };
      window.addEventListener('keydown', this._onKeyDown);
      this.stage.canvas.addEventListener('click', this._onCanvasClick);
    }

    _unbindRuntimeEvents() {
      if (this._onKeyDown) window.removeEventListener('keydown', this._onKeyDown);
      if (this._onCanvasClick) this.stage.canvas.removeEventListener('click', this._onCanvasClick);
    }

    _pointInTarget(t, x, y) {
      const b = this.stage.getTargetBounds(t);
      return x >= b.left && x <= b.right && y >= b.bottom && y <= b.top;
    }

    _startStageHats(type, filter) {
      const ws = this.project.stage.workspace;
      if (!ws || !ws.blocks) return;
      const stageTarget = {
        id: 'stage',
        name: 'Stage',
        isStage: true,
        x: 0, y: 0, direction: 90, size: 100, visible: true,
        costumes: this.project.stage.backdrops,
        sounds: this.project.stage.sounds || [],
        currentCostume: this.project.stage.currentBackdrop || 0,
        variables: {},
        lists: {},
        workspace: ws,
        effects: {},
        bubble: null
      };
      this._startHats(stageTarget, type, filter);
    }

    _startHats(target, hatType, filterFn) {
      const blocks = this._getBlocksMap(target.workspace);
      for (const id of Object.keys(blocks)) {
        const b = blocks[id];
        if (b.type !== hatType) continue;
        if (filterFn && !filterFn(b)) continue;
        const nextId = b.next;
        if (!nextId) continue;
        const gen = this._runStack(target, nextId, blocks);
        this.threads.push({
          target,
          gen,
          waiting: null,
          hatType,
          stopped: false
        });
      }
    }

    _getBlocksMap(workspace) {
      if (!workspace) return {};
      if (workspace.blocks) return workspace.blocks;
      // Blockly serialization format: { blocks: { blocks: [...] } } or flat
      if (workspace.blocks?.blocks) {
        return this._arrayToMap(workspace.blocks.blocks);
      }
      return {};
    }

    /**
     * Convert Blockly serialize({workspace}) output into a flat id→block map
     * with next / inputs references.
     */
    static workspaceToBlocksMap(serialized) {
      // Blockly 10+ serialize returns { blocks: { languageVersion, blocks: [...] }, variables: [...] }
      const root = serialized?.blocks?.blocks || serialized?.blocks || [];
      if (!Array.isArray(root)) return serialized?.blocks || {};
      const map = {};
      const walk = (block, parentNext) => {
        if (!block) return null;
        const id = block.id || ('b_' + Math.random().toString(36).slice(2));
        const node = {
          id,
          type: block.type,
          fields: block.fields || {},
          inputs: {},
          next: null,
          extraState: block.extraState
        };
        map[id] = node;
        if (block.inputs) {
          for (const [iname, ival] of Object.entries(block.inputs)) {
            if (ival.block) {
              const childId = walk(ival.block);
              node.inputs[iname] = { block: childId };
            } else if (ival.shadow) {
              const childId = walk(ival.shadow);
              node.inputs[iname] = { shadow: childId, block: childId };
            }
          }
        }
        if (block.next?.block) {
          node.next = walk(block.next.block);
        }
        return id;
      };
      for (const top of root) walk(top);
      return map;
    }

    _arrayToMap(arr) {
      return ScratchRuntime.workspaceToBlocksMap({ blocks: { blocks: arr } });
    }

    compileWorkspace(serialized) {
      return ScratchRuntime.workspaceToBlocksMap(serialized);
    }

    *_runStack(target, blockId, blocks) {
      let id = blockId;
      while (id && this.running) {
        const block = blocks[id];
        if (!block) break;
        yield* this._execBlock(target, block, blocks);
        id = block.next;
      }
    }

    *_execBlock(target, block, blocks) {
      const type = block.type;
      const val = (inputName) => this._evalInput(target, block, inputName, blocks);
      const field = (name) => block.fields?.[name];

      switch (type) {
        case 'motion_movesteps': {
          const steps = Number(val('STEPS')) || 0;
          const rad = degToRad(target.direction);
          // Scratch: 90 = up, so cos/sin swapped vs math
          target.x += steps * Math.sin(rad);
          target.y += steps * Math.cos(rad);
          break;
        }
        case 'motion_turnright':
          target.direction = wrapDir((target.direction || 90) + (Number(val('DEGREES')) || 0));
          break;
        case 'motion_turnleft':
          target.direction = wrapDir((target.direction || 90) - (Number(val('DEGREES')) || 0));
          break;
        case 'motion_gotoxy':
          target.x = Number(val('X')) || 0;
          target.y = Number(val('Y')) || 0;
          break;
        case 'motion_goto': {
          const to = field('TO');
          if (to === '_random_') {
            target.x = Math.random() * 480 - 240;
            target.y = Math.random() * 360 - 180;
          } else if (to === '_mouse_') {
            target.x = this.stage.mouse.x;
            target.y = this.stage.mouse.y;
          }
          break;
        }
        case 'motion_glidesecstoxy': {
          const secs = Math.max(0, Number(val('SECS')) || 0);
          const tx = Number(val('X')) || 0;
          const ty = Number(val('Y')) || 0;
          yield* this._glide(target, secs, tx, ty);
          break;
        }
        case 'motion_glideto': {
          const secs = Math.max(0, Number(val('SECS')) || 0);
          let tx = target.x, ty = target.y;
          const to = field('TO');
          if (to === '_random_') { tx = Math.random() * 480 - 240; ty = Math.random() * 360 - 180; }
          else if (to === '_mouse_') { tx = this.stage.mouse.x; ty = this.stage.mouse.y; }
          yield* this._glide(target, secs, tx, ty);
          break;
        }
        case 'motion_pointindirection':
          target.direction = wrapDir(Number(val('DIRECTION')) || 90);
          break;
        case 'motion_pointtowards': {
          const dx = this.stage.mouse.x - target.x;
          const dy = this.stage.mouse.y - target.y;
          target.direction = wrapDir(Math.atan2(dx, dy) * 180 / Math.PI);
          break;
        }
        case 'motion_changexby':
          target.x += Number(val('DX')) || 0;
          break;
        case 'motion_setx':
          target.x = Number(val('X')) || 0;
          break;
        case 'motion_changeyby':
          target.y += Number(val('DY')) || 0;
          break;
        case 'motion_sety':
          target.y = Number(val('Y')) || 0;
          break;
        case 'motion_ifonedgebounce': {
          const b = this.stage.getTargetBounds(target);
          if (b.left <= -240) { target.x += -240 - b.left; target.direction = wrapDir(-target.direction); }
          if (b.right >= 240) { target.x -= b.right - 240; target.direction = wrapDir(-target.direction); }
          if (b.top >= 180) { target.y -= b.top - 180; target.direction = wrapDir(180 - target.direction); }
          if (b.bottom <= -180) { target.y += -180 - b.bottom; target.direction = wrapDir(180 - target.direction); }
          break;
        }
        case 'motion_setrotationstyle':
          target.rotationStyle = field('STYLE') || 'all around';
          break;

        case 'looks_say':
          target.bubble = { text: String(val('MESSAGE') ?? ''), think: false };
          break;
        case 'looks_think':
          target.bubble = { text: String(val('MESSAGE') ?? ''), think: true };
          break;
        case 'looks_sayforsecs': {
          target.bubble = { text: String(val('MESSAGE') ?? ''), think: false };
          yield* this._wait(Number(val('SECS')) || 0);
          target.bubble = null;
          break;
        }
        case 'looks_thinkforsecs': {
          target.bubble = { text: String(val('MESSAGE') ?? ''), think: true };
          yield* this._wait(Number(val('SECS')) || 0);
          target.bubble = null;
          break;
        }
        case 'looks_switchcostumeto': {
          const name = String(val('COSTUME') ?? '');
          const idx = target.costumes.findIndex(c => c.name === name || String(c.name) === name);
          if (idx >= 0) target.currentCostume = idx;
          else {
            const n = parseInt(name, 10);
            if (!isNaN(n) && n >= 1 && n <= target.costumes.length) target.currentCostume = n - 1;
          }
          break;
        }
        case 'looks_nextcostume':
          if (target.costumes.length) target.currentCostume = (target.currentCostume + 1) % target.costumes.length;
          break;
        case 'looks_switchbackdropto': {
          const name = String(val('BACKDROP') ?? '');
          const bds = this.project.stage.backdrops;
          const idx = bds.findIndex(c => c.name === name);
          if (idx >= 0) {
            this.project.stage.currentBackdrop = idx;
            this._startHatsForBackdrop(name);
          }
          break;
        }
        case 'looks_changesizeby':
          target.size = Math.max(1, (target.size || 100) + (Number(val('CHANGE')) || 0));
          break;
        case 'looks_setsizeto':
          target.size = Math.max(1, Number(val('SIZE')) || 100);
          break;
        case 'looks_changeeffectby': {
          const eff = field('EFFECT') || 'ghost';
          target.effects[eff] = (target.effects[eff] || 0) + (Number(val('CHANGE')) || 0);
          break;
        }
        case 'looks_seteffectto': {
          const eff = field('EFFECT') || 'ghost';
          target.effects[eff] = Number(val('VALUE')) || 0;
          break;
        }
        case 'looks_cleargraphiceffects':
          target.effects = { ghost: 0, brightness: 0, color: 0 };
          break;
        case 'looks_show':
          target.visible = true;
          break;
        case 'looks_hide':
          target.visible = false;
          break;
        case 'looks_gotofrontback':
          if (field('FRONT_BACK') === 'front') target.layer = 999;
          else target.layer = -999;
          break;
        case 'looks_goforwardbackwardlayers': {
          const n = Number(val('NUM')) || 1;
          target.layer = (target.layer || 0) + (field('FORWARD_BACKWARD') === 'forward' ? n : -n);
          break;
        }

        case 'sound_play':
        case 'sound_playuntildone': {
          const name = String(val('SOUND_MENU') ?? '');
          const snd = (target.sounds || []).find(s => s.name === name) ||
            (this.project.stage.sounds || []).find(s => s.name === name);
          if (snd?.dataUrl) {
            const a = new Audio(snd.dataUrl);
            a.volume = Math.max(0, Math.min(1, (target.volume ?? this.volume) / 100));
            this.audioElements.push(a);
            const p = a.play();
            if (type === 'sound_playuntildone') {
              yield* this._waitPromise(new Promise(res => {
                a.onended = res;
                a.onerror = res;
              }));
            }
          }
          break;
        }
        case 'sound_stopallsounds':
          for (const a of this.audioElements) try { a.pause(); } catch (_) {}
          this.audioElements = [];
          break;
        case 'sound_changevolumeby':
          target.volume = Math.max(0, Math.min(100, (target.volume ?? 100) + (Number(val('VOLUME')) || 0)));
          break;
        case 'sound_setvolumeto':
          target.volume = Math.max(0, Math.min(100, Number(val('VOLUME')) || 0));
          break;

        case 'event_broadcast': {
          const msg = String(val('BROADCAST_INPUT') ?? field('BROADCAST_OPTION') ?? '');
          this._broadcast(msg);
          break;
        }
        case 'event_broadcastandwait': {
          const msg = String(val('BROADCAST_INPUT') ?? '');
          const started = this._broadcast(msg);
          while (started.some(th => this.threads.includes(th) && !th.done)) {
            yield;
          }
          break;
        }

        case 'control_wait':
          yield* this._wait(Number(val('DURATION')) || 0);
          break;
        case 'control_repeat': {
          const times = Math.floor(Number(val('TIMES')) || 0);
          const sub = block.inputs?.SUBSTACK?.block;
          for (let i = 0; i < times; i++) {
            if (sub) yield* this._runStack(target, sub, blocks);
            yield;
          }
          break;
        }
        case 'control_forever': {
          const sub = block.inputs?.SUBSTACK?.block;
          while (this.running) {
            if (sub) yield* this._runStack(target, sub, blocks);
            yield;
          }
          break;
        }
        case 'control_if': {
          if (val('CONDITION')) {
            const sub = block.inputs?.SUBSTACK?.block;
            if (sub) yield* this._runStack(target, sub, blocks);
          }
          break;
        }
        case 'control_if_else': {
          if (val('CONDITION')) {
            const sub = block.inputs?.SUBSTACK?.block;
            if (sub) yield* this._runStack(target, sub, blocks);
          } else {
            const sub2 = block.inputs?.SUBSTACK2?.block;
            if (sub2) yield* this._runStack(target, sub2, blocks);
          }
          break;
        }
        case 'control_wait_until':
          while (!val('CONDITION')) yield;
          break;
        case 'control_repeat_until': {
          const sub = block.inputs?.SUBSTACK?.block;
          while (!val('CONDITION')) {
            if (sub) yield* this._runStack(target, sub, blocks);
            yield;
          }
          break;
        }
        case 'control_stop': {
          const opt = field('STOP_OPTION');
          if (opt === 'all') this.stop();
          else if (opt === 'this script') return;
          else if (opt === 'other scripts') {
            this.threads = this.threads.filter(th => th.target !== target || th === this._currentThread);
          }
          break;
        }
        case 'control_create_clone_of': {
          const opt = field('CLONE_OPTION');
          let src = target;
          if (opt && opt !== '_myself_') {
            src = this.targets.find(t => t.name === opt) || target;
          }
          const clone = this._makeTarget({
            ...src,
            id: 'clone_' + Math.random().toString(36).slice(2),
            workspace: src.workspace,
            costumes: src.costumes,
            sounds: src.sounds
          }, true);
          clone.x = src.x; clone.y = src.y; clone.direction = src.direction;
          clone.size = src.size; clone.visible = src.visible;
          clone.currentCostume = src.currentCostume;
          clone.layer = (src.layer || 0) + 1;
          this.targets.push(clone);
          this._startHats(clone, 'control_start_as_clone');
          break;
        }
        case 'control_delete_this_clone':
          if (target.isClone) {
            this.targets = this.targets.filter(t => t !== target);
            this.threads = this.threads.filter(th => th.target !== target);
          }
          return;

        case 'sensing_askandwait': {
          const q = String(val('QUESTION') ?? '');
          const ans = prompt(q);
          this.stage.answer = ans == null ? '' : ans;
          yield;
          break;
        }
        case 'sensing_resettimer':
          this.stage.resetTimer();
          break;
        case 'sensing_setdragmode':
          target.draggable = field('DRAG_MODE') === 'draggable';
          break;

        case 'data_setvariableto':
          this.setVar(target.isStage ? null : target, field('VARIABLE'), val('VALUE'));
          break;
        case 'data_changevariableby': {
          const name = field('VARIABLE');
          const cur = Number(this.getVar(target.isStage ? null : target, name)) || 0;
          this.setVar(target.isStage ? null : target, name, cur + (Number(val('VALUE')) || 0));
          break;
        }
        case 'data_showvariable': {
          const name = field('VARIABLE');
          this.stage.setMonitor(name, this.getVar(target.isStage ? null : target, name), { visible: true, mode: 'slider' });
          break;
        }
        case 'data_hidevariable':
          this.stage.hideMonitor(field('VARIABLE'));
          break;
        case 'data_addtolist':
          this.getList(target.isStage ? null : target, field('LIST')).push(val('ITEM'));
          break;
        case 'data_deleteoflist': {
          const list = this.getList(target.isStage ? null : target, field('LIST'));
          const idx = Math.floor(Number(val('INDEX'))) - 1;
          if (idx >= 0 && idx < list.length) list.splice(idx, 1);
          break;
        }
        case 'data_deletealloflist':
          this.getList(target.isStage ? null : target, field('LIST')).length = 0;
          break;
        case 'data_insertatlist': {
          const list = this.getList(target.isStage ? null : target, field('LIST'));
          const idx = Math.floor(Number(val('INDEX'))) - 1;
          list.splice(Math.max(0, idx), 0, val('ITEM'));
          break;
        }
        case 'data_replaceitemoflist': {
          const list = this.getList(target.isStage ? null : target, field('LIST'));
          const idx = Math.floor(Number(val('INDEX'))) - 1;
          if (idx >= 0 && idx < list.length) list[idx] = val('ITEM');
          break;
        }
        case 'data_showlist':
        case 'data_hidelist':
          break;

        case 'procedures_call': {
          const name = field('NAME');
          const defBlocks = this._getBlocksMap(target.workspace);
          for (const id of Object.keys(defBlocks)) {
            const b = defBlocks[id];
            if (b.type === 'procedures_definition' && b.fields?.NAME === name && b.next) {
              yield* this._runStack(target, b.next, defBlocks);
              break;
            }
          }
          break;
        }

        default:
          break;
      }
    }

    _evalInput(target, block, inputName, blocks) {
      const inp = block.inputs?.[inputName];
      if (!inp) return null;
      const childId = inp.block || inp.shadow;
      if (!childId) return null;
      const child = blocks[childId];
      if (!child) return null;
      return this._evalReporter(target, child, blocks);
    }

    _evalReporter(target, block, blocks) {
      const type = block.type;
      const val = (n) => this._evalInput(target, block, n, blocks);
      const field = (n) => block.fields?.[n];

      switch (type) {
        case 'math_number': return Number(field('NUM')) || 0;
        case 'text': return field('TEXT') ?? '';
        case 'text_broadcast': return field('TEXT') ?? '';
        case 'motion_xposition': return target.x;
        case 'motion_yposition': return target.y;
        case 'motion_direction': return target.direction;
        case 'looks_size': return target.size;
        case 'looks_costumenumbername':
          return field('NUMBER_NAME') === 'name'
            ? (target.costumes[target.currentCostume]?.name || '')
            : (target.currentCostume + 1);
        case 'sound_volume': return target.volume ?? this.volume;
        case 'sensing_touchingobject': {
          const menu = field('TOUCHINGOBJECTMENU');
          if (menu === '_mouse_') return this.stage.touchingMouse(target);
          if (menu === '_edge_') return this.stage.touchingEdge(target);
          const other = this.targets.find(t => t.name === menu);
          return this.stage.touchingSprite(target, other);
        }
        case 'sensing_touchingcolor':
          return false; // simplified
        case 'sensing_distanceto':
          return this.stage.distanceToMouse(target);
        case 'sensing_answer': return this.stage.answer;
        case 'sensing_keypressed': return this.stage.isKeyPressed(field('KEY_OPTION'));
        case 'sensing_mousedown': return this.stage.mouse.down;
        case 'sensing_mousex': return this.stage.mouse.x;
        case 'sensing_mousey': return this.stage.mouse.y;
        case 'sensing_timer': return this.stage.timer();
        case 'sensing_loudness': return 0;
        case 'operator_add': return (Number(val('NUM1')) || 0) + (Number(val('NUM2')) || 0);
        case 'operator_subtract': return (Number(val('NUM1')) || 0) - (Number(val('NUM2')) || 0);
        case 'operator_multiply': return (Number(val('NUM1')) || 0) * (Number(val('NUM2')) || 0);
        case 'operator_divide': {
          const d = Number(val('NUM2')) || 0;
          return d === 0 ? Infinity : (Number(val('NUM1')) || 0) / d;
        }
        case 'operator_random': {
          const a = Number(val('FROM')) || 0;
          const b = Number(val('TO')) || 0;
          const lo = Math.min(a, b), hi = Math.max(a, b);
          if (Number.isInteger(lo) && Number.isInteger(hi)) {
            return Math.floor(Math.random() * (hi - lo + 1)) + lo;
          }
          return Math.random() * (hi - lo) + lo;
        }
        case 'operator_lt': return (val('OPERAND1') ?? '') < (val('OPERAND2') ?? '') || Number(val('OPERAND1')) < Number(val('OPERAND2'));
        case 'operator_gt': return Number(val('OPERAND1')) > Number(val('OPERAND2'));
        case 'operator_equals': return String(val('OPERAND1')) == String(val('OPERAND2'));
        case 'operator_and': return !!(val('OPERAND1') && val('OPERAND2'));
        case 'operator_or': return !!(val('OPERAND1') || val('OPERAND2'));
        case 'operator_not': return !val('OPERAND');
        case 'operator_join': return String(val('STRING1') ?? '') + String(val('STRING2') ?? '');
        case 'operator_letter_of': {
          const s = String(val('STRING') ?? '');
          const i = Math.floor(Number(val('LETTER')) || 1) - 1;
          return s.charAt(i) || '';
        }
        case 'operator_length': return String(val('STRING') ?? '').length;
        case 'operator_contains': return String(val('STRING1') ?? '').includes(String(val('STRING2') ?? ''));
        case 'operator_mod': return (Number(val('NUM1')) || 0) % (Number(val('NUM2')) || 1);
        case 'operator_round': return Math.round(Number(val('NUM')) || 0);
        case 'operator_mathop': {
          const n = Number(val('NUM')) || 0;
          const op = field('OPERATOR');
          const map = {
            abs: Math.abs, floor: Math.floor, ceiling: Math.ceil, sqrt: Math.sqrt,
            sin: (x) => Math.sin(x * Math.PI / 180),
            cos: (x) => Math.cos(x * Math.PI / 180),
            tan: (x) => Math.tan(x * Math.PI / 180),
            asin: (x) => Math.asin(x) * 180 / Math.PI,
            acos: (x) => Math.acos(x) * 180 / Math.PI,
            atan: (x) => Math.atan(x) * 180 / Math.PI,
            ln: Math.log, log: Math.log10,
            'e ^': Math.exp, '10 ^': (x) => Math.pow(10, x)
          };
          return (map[op] || ((x) => x))(n);
        }
        case 'data_variable': return this.getVar(target.isStage ? null : target, field('VARIABLE'));
        case 'data_listcontents': return this.getList(target.isStage ? null : target, field('LIST')).join(' ');
        case 'data_itemoflist': {
          const list = this.getList(target.isStage ? null : target, field('LIST'));
          const idx = Math.floor(Number(val('INDEX'))) - 1;
          return list[idx] ?? '';
        }
        case 'data_itemnumoflist': {
          const list = this.getList(target.isStage ? null : target, field('LIST'));
          const item = val('ITEM');
          const idx = list.findIndex(x => String(x) === String(item));
          return idx < 0 ? 0 : idx + 1;
        }
        case 'data_lengthoflist': return this.getList(target.isStage ? null : target, field('LIST')).length;
        case 'data_listcontainsitem': {
          const list = this.getList(target.isStage ? null : target, field('LIST'));
          return list.some(x => String(x) === String(val('ITEM')));
        }
        default: return null;
      }
    }

    *_glide(target, secs, tx, ty) {
      if (secs <= 0) { target.x = tx; target.y = ty; return; }
      const sx = target.x, sy = target.y;
      const start = performance.now();
      while (true) {
        const t = Math.min(1, (performance.now() - start) / (secs * 1000));
        target.x = sx + (tx - sx) * t;
        target.y = sy + (ty - sy) * t;
        if (t >= 1) break;
        yield;
      }
    }

    *_wait(secs) {
      if (secs <= 0) { yield; return; }
      const end = performance.now() + secs * 1000;
      while (performance.now() < end) yield;
    }

    *_waitPromise(p) {
      let done = false;
      p.then(() => { done = true; });
      while (!done) yield;
    }

    _broadcast(msg) {
      const started = [];
      for (const t of this.targets) {
        const before = this.threads.length;
        this._startHats(t, 'event_whenbroadcastreceived', (b) => b.fields?.BROADCAST_OPTION === msg);
        for (let i = before; i < this.threads.length; i++) started.push(this.threads[i]);
      }
      this._startStageHats('event_whenbroadcastreceived', (b) => b.fields?.BROADCAST_OPTION === msg);
      return started;
    }

    _startHatsForBackdrop(name) {
      for (const t of this.targets) {
        this._startHats(t, 'event_whenbackdropswitchesto', (b) => b.fields?.BACKDROP === name);
      }
      this._startStageHats('event_whenbackdropswitchesto', (b) => b.fields?.BACKDROP === name);
    }

    _loop() {
      if (!this.running) return;
      const frameStart = performance.now();
      // Step all threads cooperatively
      for (const th of [...this.threads]) {
        if (th.stopped) continue;
        this._currentThread = th;
        try {
          const r = th.gen.next();
          if (r.done) {
            th.done = true;
            this.threads = this.threads.filter(x => x !== th);
          }
        } catch (err) {
          console.error('Script error:', err);
          this.threads = this.threads.filter(x => x !== th);
        }
      }
      this.stage.draw(this.project, this.targets.filter(t => !t.isStage));
      this._syncMonitors();

      // Cap work per frame; always schedule next
      this.raf = requestAnimationFrame(() => this._loop());
    }

    /** Prepare project workspaces: convert Blockly serialize → blocks map on each sprite */
    static prepareProjectForRuntime(project) {
      const prep = (ws) => {
        if (!ws) return { blocks: {} };
        if (ws.blocks && !Array.isArray(ws.blocks) && !ws.blocks.blocks) {
          // already a map
          return ws;
        }
        return { blocks: ScratchRuntime.workspaceToBlocksMap(ws), _raw: ws };
      };
      const out = JSON.parse(JSON.stringify(project));
      out.stage.workspace = prep(out.stage.workspace);
      for (const s of out.sprites) {
        s.workspace = prep(s.workspace);
      }
      return out;
    }
  }

  global.ScratchRuntime = ScratchRuntime;
})(window);
