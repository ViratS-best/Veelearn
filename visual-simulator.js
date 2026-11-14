import React, { useState, useRef, useEffect } from 'react';
import { Play, Square, Save, Trash2, Plus, Copy, Loader } from 'lucide-react';

const BlockSimulatorCreator = () => {
  const [blocks, setBlocks] = useState([]);
  const [sprites, setSprites] = useState([]);
  const [variables, setVariables] = useState({});
  const [isRunning, setIsRunning] = useState(false);
  const [selectedSprite, setSelectedSprite] = useState(null);
  const [console, setConsole] = useState([]);
  const canvasRef = useRef(null);
  const animationRef = useRef(null);

  const blockCategories = {
    motion: {
      name: 'Motion',
      color: '#4C97FF',
      blocks: [
        { id: 'move', label: 'Move [10] steps', params: ['steps:10'] },
        { id: 'turn_right', label: 'Turn right [15] degrees', params: ['degrees:15'] },
        { id: 'turn_left', label: 'Turn left [15] degrees', params: ['degrees:15'] },
        { id: 'goto', label: 'Go to x:[0] y:[0]', params: ['x:0', 'y:0'] },
        { id: 'glide', label: 'Glide [1] secs to x:[0] y:[0]', params: ['duration:1', 'x:0', 'y:0'] },
        { id: 'point_direction', label: 'Point in direction [90]', params: ['direction:90'] },
        { id: 'change_x', label: 'Change x by [10]', params: ['dx:10'] },
        { id: 'change_y', label: 'Change y by [10]', params: ['dy:10'] },
        { id: 'set_x', label: 'Set x to [0]', params: ['x:0'] },
        { id: 'set_y', label: 'Set y to [0]', params: ['y:0'] }
      ]
    },
    looks: {
      name: 'Looks',
      color: '#9966FF',
      blocks: [
        { id: 'say', label: 'Say [Hello!]', params: ['text:Hello!'] },
        { id: 'think', label: 'Think [Hmm...]', params: ['text:Hmm...'] },
        { id: 'show', label: 'Show', params: [] },
        { id: 'hide', label: 'Hide', params: [] },
        { id: 'set_size', label: 'Set size to [100]%', params: ['size:100'] },
        { id: 'change_size', label: 'Change size by [10]', params: ['delta:10'] },
        { id: 'set_color', label: 'Set color to [#FF0000]', params: ['color:#FF0000'] },
        { id: 'clear_graphics', label: 'Clear graphics', params: [] }
      ]
    },
    control: {
      name: 'Control',
      color: '#FFAB19',
      blocks: [
        { id: 'wait', label: 'Wait [1] seconds', params: ['duration:1'] },
        { id: 'repeat', label: 'Repeat [10]', params: ['times:10'], container: true },
        { id: 'forever', label: 'Forever', params: [], container: true },
        { id: 'if', label: 'If [x > 0]', params: ['condition:x > 0'], container: true },
        { id: 'if_else', label: 'If [x > 0] Else', params: ['condition:x > 0'], container: true, hasElse: true },
        { id: 'repeat_until', label: 'Repeat until [x > 100]', params: ['condition:x > 100'], container: true },
        { id: 'stop', label: 'Stop all', params: [] },
        { id: 'stop_script', label: 'Stop this script', params: [] }
      ]
    },
    sensing: {
      name: 'Sensing',
      color: '#5CB1D6',
      blocks: [
        { id: 'touching', label: 'Touching [sprite]?', params: ['sprite:sprite1'] },
        { id: 'distance_to', label: 'Distance to [sprite]', params: ['sprite:sprite1'] },
        { id: 'mouse_x', label: 'Mouse X', params: [] },
        { id: 'mouse_y', label: 'Mouse Y', params: [] },
        { id: 'key_pressed', label: 'Key [space] pressed?', params: ['key:space'] }
      ]
    },
    operators: {
      name: 'Operators',
      color: '#59C059',
      blocks: [
        { id: 'add', label: '[0] + [0]', params: ['a:0', 'b:0'] },
        { id: 'subtract', label: '[0] - [0]', params: ['a:0', 'b:0'] },
        { id: 'multiply', label: '[0] * [0]', params: ['a:0', 'b:0'] },
        { id: 'divide', label: '[0] / [0]', params: ['a:1', 'b:1'] },
        { id: 'random', label: 'Pick random [1] to [10]', params: ['min:1', 'max:10'] },
        { id: 'greater', label: '[0] > [0]', params: ['a:0', 'b:0'] },
        { id: 'less', label: '[0] < [0]', params: ['a:0', 'b:0'] },
        { id: 'equals', label: '[0] = [0]', params: ['a:0', 'b:0'] },
        { id: 'and', label: '[true] and [true]', params: ['a:true', 'b:true'] },
        { id: 'or', label: '[true] or [false]', params: ['a:true', 'b:false'] },
        { id: 'not', label: 'Not [false]', params: ['value:false'] },
        { id: 'mod', label: '[0] mod [0]', params: ['a:0', 'b:1'] },
        { id: 'round', label: 'Round [0]', params: ['value:0'] },
        { id: 'abs', label: 'Abs [0]', params: ['value:0'] },
        { id: 'sqrt', label: 'Sqrt [0]', params: ['value:0'] }
      ]
    },
    variables: {
      name: 'Variables',
      color: '#FF8C1A',
      blocks: [
        { id: 'set_var', label: 'Set [myVar] to [0]', params: ['name:myVar', 'value:0'] },
        { id: 'change_var', label: 'Change [myVar] by [1]', params: ['name:myVar', 'delta:1'] },
        { id: 'get_var', label: 'Get [myVar]', params: ['name:myVar'] }
      ]
    },
    pen: {
      name: 'Pen',
      color: '#0FBD8C',
      blocks: [
        { id: 'pen_down', label: 'Pen down', params: [] },
        { id: 'pen_up', label: 'Pen up', params: [] },
        { id: 'pen_color', label: 'Set pen color to [#000000]', params: ['color:#000000'] },
        { id: 'pen_size', label: 'Set pen size to [1]', params: ['size:1'] },
        { id: 'stamp', label: 'Stamp', params: [] },
        { id: 'clear_pen', label: 'Clear pen', params: [] }
      ]
    }
  };

  const addBlock = (blockDef, category) => {
    const newBlock = {
      id: Date.now(),
      type: blockDef.id,
      category: category,
      params: blockDef.params.map(p => {
        const [name, defaultValue] = p.split(':');
        return { name, value: defaultValue };
      }),
      container: blockDef.container || false,
      hasElse: blockDef.hasElse || false,
      children: [],
      elseChildren: []
    };
    setBlocks([...blocks, newBlock]);
    log(`Added ${blockDef.label} block`);
  };

  const addSprite = () => {
    const spriteName = prompt('Sprite name:', `Sprite${sprites.length + 1}`);
    if (!spriteName) return;
    
    const newSprite = {
      id: Date.now(),
      name: spriteName,
      x: 300,
      y: 200,
      direction: 90,
      size: 100,
      color: '#FF6B6B',
      visible: true,
      penDown: false,
      penColor: '#000000',
      penSize: 2,
      shape: 'circle'
    };
    setSprites([...sprites, newSprite]);
    setSelectedSprite(newSprite.id);
    log(`Created sprite: ${spriteName}`);
  };

  const updateBlockParam = (blockId, paramName, value) => {
    setBlocks(blocks.map(block => {
      if (block.id === blockId) {
        return {
          ...block,
          params: block.params.map(p => 
            p.name === paramName ? { ...p, value } : p
          )
        };
      }
      return block;
    }));
  };

  const deleteBlock = (blockId) => {
    setBlocks(blocks.filter(b => b.id !== blockId));
  };

  const log = (message, type = 'info') => {
    setConsole(prev => [...prev.slice(-20), { message, type, time: Date.now() }]);
  };

  const evaluateExpression = (expr, context) => {
    try {
      // Simple expression evaluator
      const func = new Function(...Object.keys(context), `return ${expr}`);
      return func(...Object.values(context));
    } catch (e) {
      log(`Expression error: ${e.message}`, 'error');
      return false;
    }
  };

  const executeBlock = async (block, sprite, context) => {
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext('2d');
    if (!ctx || !sprite) return;

    const getParam = (name) => {
      const param = block.params.find(p => p.name === name);
      if (!param) return 0;
      
      // Try to evaluate as variable or expression
      if (isNaN(param.value)) {
        if (context[param.value] !== undefined) {
          return context[param.value];
        }
        return param.value;
      }
      return parseFloat(param.value);
    };

    switch (block.type) {
      case 'move':
        const steps = getParam('steps');
        const rad = (sprite.direction - 90) * Math.PI / 180;
        sprite.x += Math.cos(rad) * steps;
        sprite.y += Math.sin(rad) * steps;
        
        if (sprite.penDown) {
          ctx.strokeStyle = sprite.penColor;
          ctx.lineWidth = sprite.penSize;
          ctx.beginPath();
          ctx.moveTo(sprite.x - Math.cos(rad) * steps, sprite.y - Math.sin(rad) * steps);
          ctx.lineTo(sprite.x, sprite.y);
          ctx.stroke();
        }
        break;

      case 'turn_right':
        sprite.direction += getParam('degrees');
        break;

      case 'turn_left':
        sprite.direction -= getParam('degrees');
        break;

      case 'goto':
        sprite.x = getParam('x');
        sprite.y = getParam('y');
        break;

      case 'set_x':
        sprite.x = getParam('x');
        break;

      case 'set_y':
        sprite.y = getParam('y');
        break;

      case 'change_x':
        sprite.x += getParam('dx');
        break;

      case 'change_y':
        sprite.y += getParam('dy');
        break;

      case 'point_direction':
        sprite.direction = getParam('direction');
        break;

      case 'show':
        sprite.visible = true;
        break;

      case 'hide':
        sprite.visible = false;
        break;

      case 'set_size':
        sprite.size = getParam('size');
        break;

      case 'change_size':
        sprite.size += getParam('delta');
        break;

      case 'set_color':
        sprite.color = getParam('color');
        break;

      case 'pen_down':
        sprite.penDown = true;
        break;

      case 'pen_up':
        sprite.penDown = false;
        break;

      case 'pen_color':
        sprite.penColor = getParam('color');
        break;

      case 'pen_size':
        sprite.penSize = getParam('size');
        break;

      case 'clear_pen':
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        break;

      case 'set_var':
        context[getParam('name')] = getParam('value');
        break;

      case 'change_var':
        const varName = getParam('name');
        context[varName] = (context[varName] || 0) + getParam('delta');
        break;

      case 'repeat':
        const times = getParam('times');
        for (let i = 0; i < times && isRunning; i++) {
          for (const child of block.children) {
            await executeBlock(child, sprite, context);
          }
        }
        break;

      case 'if':
        const condition = getParam('condition');
        if (evaluateExpression(condition, context)) {
          for (const child of block.children) {
            await executeBlock(child, sprite, context);
          }
        }
        break;

      case 'wait':
        await new Promise(resolve => setTimeout(resolve, getParam('duration') * 1000));
        break;
    }
  };

  const runSimulation = async () => {
    if (!canvasRef.current) return;
    
    setIsRunning(true);
    log('Starting simulation...');
    
    const sprite = sprites.find(s => s.id === selectedSprite);
    if (!sprite) {
      log('No sprite selected!', 'error');
      setIsRunning(false);
      return;
    }

    const context = { ...variables };

    try {
      for (const block of blocks) {
        if (!isRunning) break;
        await executeBlock(block, sprite, context);
      }
      log('Simulation complete!');
    } catch (error) {
      log(`Error: ${error.message}`, 'error');
    }

    setIsRunning(false);
  };

  const stopSimulation = () => {
    setIsRunning(false);
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
    }
    log('Stopped');
  };

  const saveSimulator = () => {
    const data = { blocks, sprites, variables };
    
    if (window.opener) {
      window.opener.postMessage({
        type: 'visual-simulator-save',
        data
      }, '*');
      alert('Saved! You can close this window.');
    } else {
      const json = JSON.stringify(data, null, 2);
      const blob = new Blob([json], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `simulator-${Date.now()}.json`;
      a.click();
      URL.revokeObjectURL(url);
    }
    log('Saved!');
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw grid
    ctx.strokeStyle = '#e5e7eb';
    ctx.lineWidth = 1;
    for (let i = 0; i < canvas.width; i += 50) {
      ctx.beginPath();
      ctx.moveTo(i, 0);
      ctx.lineTo(i, canvas.height);
      ctx.stroke();
    }
    for (let i = 0; i < canvas.height; i += 50) {
      ctx.beginPath();
      ctx.moveTo(0, i);
      ctx.lineTo(canvas.width, i);
      ctx.stroke();
    }
    
    // Draw sprites
    sprites.forEach(sprite => {
      if (!sprite.visible) return;
      
      const size = sprite.size / 100 * 30;
      ctx.fillStyle = sprite.color;
      ctx.beginPath();
      ctx.arc(sprite.x, sprite.y, size, 0, Math.PI * 2);
      ctx.fill();
      
      // Draw direction indicator
      const rad = (sprite.direction - 90) * Math.PI / 180;
      ctx.strokeStyle = '#000';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(sprite.x, sprite.y);
      ctx.lineTo(sprite.x + Math.cos(rad) * size, sprite.y + Math.sin(rad) * size);
      ctx.stroke();
      
      // Draw name
      ctx.fillStyle = '#000';
      ctx.font = '12px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(sprite.name, sprite.x, sprite.y - size - 5);
    });
  }, [sprites]);

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      {/* Block Palette */}
      <div className="w-64 bg-gray-800 overflow-y-auto p-4 border-r border-gray-700">
        <h2 className="text-xl font-bold mb-4 text-blue-400">Block Palette</h2>
        
        {Object.entries(blockCategories).map(([key, category]) => (
          <div key={key} className="mb-4">
            <h3 className="font-semibold mb-2 text-sm uppercase tracking-wide" style={{ color: category.color }}>
              {category.name}
            </h3>
            <div className="space-y-2">
              {category.blocks.map(block => (
                <button
                  key={block.id}
                  onClick={() => addBlock(block, key)}
                  className="w-full text-left px-3 py-2 rounded text-sm hover:opacity-80 transition"
                  style={{ backgroundColor: category.color }}
                >
                  {block.label}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Main Area */}
      <div className="flex-1 flex flex-col">
        {/* Toolbar */}
        <div className="bg-gray-800 p-3 border-b border-gray-700 flex gap-2 items-center">
          <button onClick={runSimulation} disabled={isRunning} className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded flex items-center gap-2 disabled:opacity-50">
            {isRunning ? <Loader className="animate-spin" size={16} /> : <Play size={16} />}
            Run
          </button>
          <button onClick={stopSimulation} className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded flex items-center gap-2">
            <Square size={16} /> Stop
          </button>
          <button onClick={saveSimulator} className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded flex items-center gap-2">
            <Save size={16} /> Save
          </button>
          <button onClick={() => setBlocks([])} className="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded flex items-center gap-2">
            <Trash2 size={16} /> Clear
          </button>
          <button onClick={addSprite} className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded flex items-center gap-2 ml-auto">
            <Plus size={16} /> Add Sprite
          </button>
        </div>

        <div className="flex flex-1 overflow-hidden">
          {/* Code Area */}
          <div className="flex-1 overflow-y-auto p-4 bg-gray-850">
            <h3 className="text-lg font-semibold mb-4">Your Code</h3>
            <div className="space-y-2">
              {blocks.map(block => {
                const category = blockCategories[block.category];
                return (
                  <div key={block.id} className="p-3 rounded flex items-center gap-2" style={{ backgroundColor: category.color }}>
                    <div className="flex-1">
                      {block.params.map((param, i) => (
                        <input
                          key={i}
                          type="text"
                          value={param.value}
                          onChange={(e) => updateBlockParam(block.id, param.name, e.target.value)}
                          className="bg-white/20 px-2 py-1 rounded text-sm mx-1 w-20"
                          placeholder={param.name}
                        />
                      ))}
                    </div>
                    <button onClick={() => deleteBlock(block.id)} className="text-white/70 hover:text-white">
                      <Trash2 size={16} />
                    </button>
                  </div>
                );
              })}
              {blocks.length === 0 && (
                <p className="text-gray-400 text-center py-8">Click blocks on the left to add them here</p>
              )}
            </div>
          </div>

          {/* Canvas Area */}
          <div className="w-1/2 bg-gray-900 p-4 flex flex-col border-l border-gray-700">
            <div className="mb-4">
              <h3 className="text-lg font-semibold mb-2">Stage</h3>
              <div className="flex gap-2 mb-2">
                {sprites.map(sprite => (
                  <button
                    key={sprite.id}
                    onClick={() => setSelectedSprite(sprite.id)}
                    className={`px-3 py-1 rounded ${selectedSprite === sprite.id ? 'bg-blue-600' : 'bg-gray-700'}`}
                  >
                    {sprite.name}
                  </button>
                ))}
              </div>
            </div>
            <canvas
              ref={canvasRef}
              width={600}
              height={400}
              className="border-2 border-gray-700 rounded bg-white mb-4"
            />
            
            {/* Console */}
            <div className="bg-black rounded p-3 h-32 overflow-y-auto font-mono text-xs">
              {console.map((entry, i) => (
                <div key={i} className={entry.type === 'error' ? 'text-red-400' : 'text-green-400'}>
                  &gt; {entry.message}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BlockSimulatorCreator;