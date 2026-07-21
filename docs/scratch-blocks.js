/**
 * Veelearn Scratch-style Blockly block definitions + toolbox.
 * Uses Zelos renderer (Scratch 3 look) via Blockly.
 */
(function (global) {
  'use strict';

  const COLORS = {
    motion: '#4C97FF',
    looks: '#9966FF',
    sound: '#CF63CF',
    events: '#FFBF00',
    control: '#FFAB19',
    sensing: '#5CB1D6',
    operators: '#59C059',
    variables: '#FF8C1A',
    myblocks: '#FF6680'
  };

  const KEY_OPTIONS = [
    ['space', 'space'],
    ['left arrow', 'left arrow'],
    ['right arrow', 'right arrow'],
    ['up arrow', 'up arrow'],
    ['down arrow', 'down arrow'],
    ['any', 'any'],
    ['a', 'a'], ['b', 'b'], ['c', 'c'], ['d', 'd'], ['e', 'e'],
    ['f', 'f'], ['g', 'g'], ['h', 'h'], ['i', 'i'], ['j', 'j'],
    ['k', 'k'], ['l', 'l'], ['m', 'm'], ['n', 'n'], ['o', 'o'],
    ['p', 'p'], ['q', 'q'], ['r', 'r'], ['s', 's'], ['t', 't'],
    ['u', 'u'], ['v', 'v'], ['w', 'w'], ['x', 'x'], ['y', 'y'], ['z', 'z'],
    ['0', '0'], ['1', '1'], ['2', '2'], ['3', '3'], ['4', '4'],
    ['5', '5'], ['6', '6'], ['7', '7'], ['8', '8'], ['9', '9']
  ];

  function num(name, def) {
    return { type: 'input_value', name, check: 'Number' };
  }

  function defineBlocks() {
    const B = Blockly.common ? Blockly.common.defineBlocksWithJsonArray : Blockly.defineBlocksWithJsonArray;

    B([
      // ——— MOTION ———
      { type: 'motion_movesteps', message0: 'move %1 steps', args0: [{ type: 'input_value', name: 'STEPS', check: 'Number' }], previousStatement: null, nextStatement: null, colour: COLORS.motion, inputsInline: true },
      { type: 'motion_turnright', message0: 'turn ↻ %1 degrees', args0: [{ type: 'input_value', name: 'DEGREES', check: 'Number' }], previousStatement: null, nextStatement: null, colour: COLORS.motion, inputsInline: true },
      { type: 'motion_turnleft', message0: 'turn ↺ %1 degrees', args0: [{ type: 'input_value', name: 'DEGREES', check: 'Number' }], previousStatement: null, nextStatement: null, colour: COLORS.motion, inputsInline: true },
      { type: 'motion_goto', message0: 'go to %1', args0: [{ type: 'field_dropdown', name: 'TO', options: [['random position', '_random_'], ['mouse-pointer', '_mouse_']] }], previousStatement: null, nextStatement: null, colour: COLORS.motion, inputsInline: true },
      { type: 'motion_gotoxy', message0: 'go to x: %1 y: %2', args0: [{ type: 'input_value', name: 'X', check: 'Number' }, { type: 'input_value', name: 'Y', check: 'Number' }], previousStatement: null, nextStatement: null, colour: COLORS.motion, inputsInline: true },
      { type: 'motion_glideto', message0: 'glide %1 secs to %2', args0: [{ type: 'input_value', name: 'SECS', check: 'Number' }, { type: 'field_dropdown', name: 'TO', options: [['random position', '_random_'], ['mouse-pointer', '_mouse_']] }], previousStatement: null, nextStatement: null, colour: COLORS.motion, inputsInline: true },
      { type: 'motion_glidesecstoxy', message0: 'glide %1 secs to x: %2 y: %3', args0: [{ type: 'input_value', name: 'SECS', check: 'Number' }, { type: 'input_value', name: 'X', check: 'Number' }, { type: 'input_value', name: 'Y', check: 'Number' }], previousStatement: null, nextStatement: null, colour: COLORS.motion, inputsInline: true },
      { type: 'motion_pointindirection', message0: 'point in direction %1', args0: [{ type: 'input_value', name: 'DIRECTION', check: 'Number' }], previousStatement: null, nextStatement: null, colour: COLORS.motion, inputsInline: true },
      { type: 'motion_pointtowards', message0: 'point towards %1', args0: [{ type: 'field_dropdown', name: 'TOWARDS', options: [['mouse-pointer', '_mouse_']] }], previousStatement: null, nextStatement: null, colour: COLORS.motion, inputsInline: true },
      { type: 'motion_changexby', message0: 'change x by %1', args0: [{ type: 'input_value', name: 'DX', check: 'Number' }], previousStatement: null, nextStatement: null, colour: COLORS.motion, inputsInline: true },
      { type: 'motion_setx', message0: 'set x to %1', args0: [{ type: 'input_value', name: 'X', check: 'Number' }], previousStatement: null, nextStatement: null, colour: COLORS.motion, inputsInline: true },
      { type: 'motion_changeyby', message0: 'change y by %1', args0: [{ type: 'input_value', name: 'DY', check: 'Number' }], previousStatement: null, nextStatement: null, colour: COLORS.motion, inputsInline: true },
      { type: 'motion_sety', message0: 'set y to %1', args0: [{ type: 'input_value', name: 'Y', check: 'Number' }], previousStatement: null, nextStatement: null, colour: COLORS.motion, inputsInline: true },
      { type: 'motion_ifonedgebounce', message0: 'if on edge, bounce', previousStatement: null, nextStatement: null, colour: COLORS.motion },
      { type: 'motion_setrotationstyle', message0: 'set rotation style %1', args0: [{ type: 'field_dropdown', name: 'STYLE', options: [['left-right', 'left-right'], ["don't rotate", "don't rotate"], ['all around', 'all around']] }], previousStatement: null, nextStatement: null, colour: COLORS.motion, inputsInline: true },
      { type: 'motion_xposition', message0: 'x position', output: 'Number', colour: COLORS.motion },
      { type: 'motion_yposition', message0: 'y position', output: 'Number', colour: COLORS.motion },
      { type: 'motion_direction', message0: 'direction', output: 'Number', colour: COLORS.motion },

      // ——— LOOKS ———
      { type: 'looks_sayforsecs', message0: 'say %1 for %2 seconds', args0: [{ type: 'input_value', name: 'MESSAGE' }, { type: 'input_value', name: 'SECS', check: 'Number' }], previousStatement: null, nextStatement: null, colour: COLORS.looks, inputsInline: true },
      { type: 'looks_say', message0: 'say %1', args0: [{ type: 'input_value', name: 'MESSAGE' }], previousStatement: null, nextStatement: null, colour: COLORS.looks, inputsInline: true },
      { type: 'looks_thinkforsecs', message0: 'think %1 for %2 seconds', args0: [{ type: 'input_value', name: 'MESSAGE' }, { type: 'input_value', name: 'SECS', check: 'Number' }], previousStatement: null, nextStatement: null, colour: COLORS.looks, inputsInline: true },
      { type: 'looks_think', message0: 'think %1', args0: [{ type: 'input_value', name: 'MESSAGE' }], previousStatement: null, nextStatement: null, colour: COLORS.looks, inputsInline: true },
      { type: 'looks_switchcostumeto', message0: 'switch costume to %1', args0: [{ type: 'input_value', name: 'COSTUME' }], previousStatement: null, nextStatement: null, colour: COLORS.looks, inputsInline: true },
      { type: 'looks_nextcostume', message0: 'next costume', previousStatement: null, nextStatement: null, colour: COLORS.looks },
      { type: 'looks_switchbackdropto', message0: 'switch backdrop to %1', args0: [{ type: 'input_value', name: 'BACKDROP' }], previousStatement: null, nextStatement: null, colour: COLORS.looks, inputsInline: true },
      { type: 'looks_changesizeby', message0: 'change size by %1', args0: [{ type: 'input_value', name: 'CHANGE', check: 'Number' }], previousStatement: null, nextStatement: null, colour: COLORS.looks, inputsInline: true },
      { type: 'looks_setsizeto', message0: 'set size to %1 %', args0: [{ type: 'input_value', name: 'SIZE', check: 'Number' }], previousStatement: null, nextStatement: null, colour: COLORS.looks, inputsInline: true },
      { type: 'looks_changeeffectby', message0: 'change %1 effect by %2', args0: [{ type: 'field_dropdown', name: 'EFFECT', options: [['color', 'color'], ['fisheye', 'fisheye'], ['whirl', 'whirl'], ['pixelate', 'pixelate'], ['mosaic', 'mosaic'], ['brightness', 'brightness'], ['ghost', 'ghost']] }, { type: 'input_value', name: 'CHANGE', check: 'Number' }], previousStatement: null, nextStatement: null, colour: COLORS.looks, inputsInline: true },
      { type: 'looks_seteffectto', message0: 'set %1 effect to %2', args0: [{ type: 'field_dropdown', name: 'EFFECT', options: [['color', 'color'], ['fisheye', 'fisheye'], ['whirl', 'whirl'], ['pixelate', 'pixelate'], ['mosaic', 'mosaic'], ['brightness', 'brightness'], ['ghost', 'ghost']] }, { type: 'input_value', name: 'VALUE', check: 'Number' }], previousStatement: null, nextStatement: null, colour: COLORS.looks, inputsInline: true },
      { type: 'looks_cleargraphiceffects', message0: 'clear graphic effects', previousStatement: null, nextStatement: null, colour: COLORS.looks },
      { type: 'looks_show', message0: 'show', previousStatement: null, nextStatement: null, colour: COLORS.looks },
      { type: 'looks_hide', message0: 'hide', previousStatement: null, nextStatement: null, colour: COLORS.looks },
      { type: 'looks_gotofrontback', message0: 'go to %1 layer', args0: [{ type: 'field_dropdown', name: 'FRONT_BACK', options: [['front', 'front'], ['back', 'back']] }], previousStatement: null, nextStatement: null, colour: COLORS.looks, inputsInline: true },
      { type: 'looks_goforwardbackwardlayers', message0: 'go %1 %2 layers', args0: [{ type: 'field_dropdown', name: 'FORWARD_BACKWARD', options: [['forward', 'forward'], ['backward', 'backward']] }, { type: 'input_value', name: 'NUM', check: 'Number' }], previousStatement: null, nextStatement: null, colour: COLORS.looks, inputsInline: true },
      { type: 'looks_costumenumbername', message0: 'costume %1', args0: [{ type: 'field_dropdown', name: 'NUMBER_NAME', options: [['number', 'number'], ['name', 'name']] }], output: null, colour: COLORS.looks, inputsInline: true },
      { type: 'looks_size', message0: 'size', output: 'Number', colour: COLORS.looks },

      // ——— SOUND ———
      { type: 'sound_play', message0: 'start sound %1', args0: [{ type: 'input_value', name: 'SOUND_MENU' }], previousStatement: null, nextStatement: null, colour: COLORS.sound, inputsInline: true },
      { type: 'sound_playuntildone', message0: 'play sound %1 until done', args0: [{ type: 'input_value', name: 'SOUND_MENU' }], previousStatement: null, nextStatement: null, colour: COLORS.sound, inputsInline: true },
      { type: 'sound_stopallsounds', message0: 'stop all sounds', previousStatement: null, nextStatement: null, colour: COLORS.sound },
      { type: 'sound_changevolumeby', message0: 'change volume by %1', args0: [{ type: 'input_value', name: 'VOLUME', check: 'Number' }], previousStatement: null, nextStatement: null, colour: COLORS.sound, inputsInline: true },
      { type: 'sound_setvolumeto', message0: 'set volume to %1 %', args0: [{ type: 'input_value', name: 'VOLUME', check: 'Number' }], previousStatement: null, nextStatement: null, colour: COLORS.sound, inputsInline: true },
      { type: 'sound_volume', message0: 'volume', output: 'Number', colour: COLORS.sound },

      // ——— EVENTS ———
      { type: 'event_whenflagclicked', message0: 'when ⚑ clicked', nextStatement: null, colour: COLORS.events, hat: 'cap' },
      { type: 'event_whenkeypressed', message0: 'when %1 key pressed', args0: [{ type: 'field_dropdown', name: 'KEY_OPTION', options: KEY_OPTIONS }], nextStatement: null, colour: COLORS.events, hat: 'cap' },
      { type: 'event_whenthisspriteclicked', message0: 'when this sprite clicked', nextStatement: null, colour: COLORS.events, hat: 'cap' },
      { type: 'event_whenbackdropswitchesto', message0: 'when backdrop switches to %1', args0: [{ type: 'field_input', name: 'BACKDROP', text: 'backdrop1' }], nextStatement: null, colour: COLORS.events, hat: 'cap' },
      { type: 'event_whenbroadcastreceived', message0: 'when I receive %1', args0: [{ type: 'field_input', name: 'BROADCAST_OPTION', text: 'message1' }], nextStatement: null, colour: COLORS.events, hat: 'cap' },
      { type: 'event_broadcast', message0: 'broadcast %1', args0: [{ type: 'input_value', name: 'BROADCAST_INPUT' }], previousStatement: null, nextStatement: null, colour: COLORS.events, inputsInline: true },
      { type: 'event_broadcastandwait', message0: 'broadcast %1 and wait', args0: [{ type: 'input_value', name: 'BROADCAST_INPUT' }], previousStatement: null, nextStatement: null, colour: COLORS.events, inputsInline: true },

      // ——— CONTROL ———
      { type: 'control_wait', message0: 'wait %1 seconds', args0: [{ type: 'input_value', name: 'DURATION', check: 'Number' }], previousStatement: null, nextStatement: null, colour: COLORS.control, inputsInline: true },
      { type: 'control_repeat', message0: 'repeat %1 %2', args0: [{ type: 'input_value', name: 'TIMES', check: 'Number' }, { type: 'input_statement', name: 'SUBSTACK' }], previousStatement: null, nextStatement: null, colour: COLORS.control, inputsInline: true },
      { type: 'control_forever', message0: 'forever %1', args0: [{ type: 'input_statement', name: 'SUBSTACK' }], previousStatement: null, colour: COLORS.control },
      { type: 'control_if', message0: 'if %1 then %2', args0: [{ type: 'input_value', name: 'CONDITION', check: 'Boolean' }, { type: 'input_statement', name: 'SUBSTACK' }], previousStatement: null, nextStatement: null, colour: COLORS.control },
      { type: 'control_if_else', message0: 'if %1 then %2 else %3', args0: [{ type: 'input_value', name: 'CONDITION', check: 'Boolean' }, { type: 'input_statement', name: 'SUBSTACK' }, { type: 'input_statement', name: 'SUBSTACK2' }], previousStatement: null, nextStatement: null, colour: COLORS.control },
      { type: 'control_wait_until', message0: 'wait until %1', args0: [{ type: 'input_value', name: 'CONDITION', check: 'Boolean' }], previousStatement: null, nextStatement: null, colour: COLORS.control, inputsInline: true },
      { type: 'control_repeat_until', message0: 'repeat until %1 %2', args0: [{ type: 'input_value', name: 'CONDITION', check: 'Boolean' }, { type: 'input_statement', name: 'SUBSTACK' }], previousStatement: null, nextStatement: null, colour: COLORS.control },
      { type: 'control_stop', message0: 'stop %1', args0: [{ type: 'field_dropdown', name: 'STOP_OPTION', options: [['all', 'all'], ['this script', 'this script'], ['other scripts in sprite', 'other scripts']] }], previousStatement: null, colour: COLORS.control, inputsInline: true },
      { type: 'control_create_clone_of', message0: 'create clone of %1', args0: [{ type: 'field_dropdown', name: 'CLONE_OPTION', options: [['myself', '_myself_']] }], previousStatement: null, nextStatement: null, colour: COLORS.control, inputsInline: true },
      { type: 'control_start_as_clone', message0: 'when I start as a clone', nextStatement: null, colour: COLORS.control, hat: 'cap' },
      { type: 'control_delete_this_clone', message0: 'delete this clone', previousStatement: null, colour: COLORS.control },

      // ——— SENSING ———
      { type: 'sensing_touchingobject', message0: 'touching %1 ?', args0: [{ type: 'field_dropdown', name: 'TOUCHINGOBJECTMENU', options: [['mouse-pointer', '_mouse_'], ['edge', '_edge_']] }], output: 'Boolean', colour: COLORS.sensing, inputsInline: true },
      { type: 'sensing_touchingcolor', message0: 'touching color %1 ?', args0: [{ type: 'field_colour', name: 'COLOR', colour: '#ff0000' }], output: 'Boolean', colour: COLORS.sensing, inputsInline: true },
      { type: 'sensing_distanceto', message0: 'distance to %1', args0: [{ type: 'field_dropdown', name: 'DISTANCETOMENU', options: [['mouse-pointer', '_mouse_']] }], output: 'Number', colour: COLORS.sensing, inputsInline: true },
      { type: 'sensing_askandwait', message0: 'ask %1 and wait', args0: [{ type: 'input_value', name: 'QUESTION' }], previousStatement: null, nextStatement: null, colour: COLORS.sensing, inputsInline: true },
      { type: 'sensing_answer', message0: 'answer', output: 'String', colour: COLORS.sensing },
      { type: 'sensing_keypressed', message0: 'key %1 pressed?', args0: [{ type: 'field_dropdown', name: 'KEY_OPTION', options: KEY_OPTIONS }], output: 'Boolean', colour: COLORS.sensing, inputsInline: true },
      { type: 'sensing_mousedown', message0: 'mouse down?', output: 'Boolean', colour: COLORS.sensing },
      { type: 'sensing_mousex', message0: 'mouse x', output: 'Number', colour: COLORS.sensing },
      { type: 'sensing_mousey', message0: 'mouse y', output: 'Number', colour: COLORS.sensing },
      { type: 'sensing_setdragmode', message0: 'set drag mode %1', args0: [{ type: 'field_dropdown', name: 'DRAG_MODE', options: [['draggable', 'draggable'], ['not draggable', 'not draggable']] }], previousStatement: null, nextStatement: null, colour: COLORS.sensing, inputsInline: true },
      { type: 'sensing_loudness', message0: 'loudness', output: 'Number', colour: COLORS.sensing },
      { type: 'sensing_timer', message0: 'timer', output: 'Number', colour: COLORS.sensing },
      { type: 'sensing_resettimer', message0: 'reset timer', previousStatement: null, nextStatement: null, colour: COLORS.sensing },

      // ——— OPERATORS ———
      { type: 'operator_add', message0: '%1 + %2', args0: [{ type: 'input_value', name: 'NUM1', check: 'Number' }, { type: 'input_value', name: 'NUM2', check: 'Number' }], output: 'Number', colour: COLORS.operators, inputsInline: true },
      { type: 'operator_subtract', message0: '%1 − %2', args0: [{ type: 'input_value', name: 'NUM1', check: 'Number' }, { type: 'input_value', name: 'NUM2', check: 'Number' }], output: 'Number', colour: COLORS.operators, inputsInline: true },
      { type: 'operator_multiply', message0: '%1 × %2', args0: [{ type: 'input_value', name: 'NUM1', check: 'Number' }, { type: 'input_value', name: 'NUM2', check: 'Number' }], output: 'Number', colour: COLORS.operators, inputsInline: true },
      { type: 'operator_divide', message0: '%1 ÷ %2', args0: [{ type: 'input_value', name: 'NUM1', check: 'Number' }, { type: 'input_value', name: 'NUM2', check: 'Number' }], output: 'Number', colour: COLORS.operators, inputsInline: true },
      { type: 'operator_random', message0: 'pick random %1 to %2', args0: [{ type: 'input_value', name: 'FROM', check: 'Number' }, { type: 'input_value', name: 'TO', check: 'Number' }], output: 'Number', colour: COLORS.operators, inputsInline: true },
      { type: 'operator_lt', message0: '%1 < %2', args0: [{ type: 'input_value', name: 'OPERAND1' }, { type: 'input_value', name: 'OPERAND2' }], output: 'Boolean', colour: COLORS.operators, inputsInline: true },
      { type: 'operator_equals', message0: '%1 = %2', args0: [{ type: 'input_value', name: 'OPERAND1' }, { type: 'input_value', name: 'OPERAND2' }], output: 'Boolean', colour: COLORS.operators, inputsInline: true },
      { type: 'operator_gt', message0: '%1 > %2', args0: [{ type: 'input_value', name: 'OPERAND1' }, { type: 'input_value', name: 'OPERAND2' }], output: 'Boolean', colour: COLORS.operators, inputsInline: true },
      { type: 'operator_and', message0: '%1 and %2', args0: [{ type: 'input_value', name: 'OPERAND1', check: 'Boolean' }, { type: 'input_value', name: 'OPERAND2', check: 'Boolean' }], output: 'Boolean', colour: COLORS.operators, inputsInline: true },
      { type: 'operator_or', message0: '%1 or %2', args0: [{ type: 'input_value', name: 'OPERAND1', check: 'Boolean' }, { type: 'input_value', name: 'OPERAND2', check: 'Boolean' }], output: 'Boolean', colour: COLORS.operators, inputsInline: true },
      { type: 'operator_not', message0: 'not %1', args0: [{ type: 'input_value', name: 'OPERAND', check: 'Boolean' }], output: 'Boolean', colour: COLORS.operators, inputsInline: true },
      { type: 'operator_join', message0: 'join %1 %2', args0: [{ type: 'input_value', name: 'STRING1' }, { type: 'input_value', name: 'STRING2' }], output: 'String', colour: COLORS.operators, inputsInline: true },
      { type: 'operator_letter_of', message0: 'letter %1 of %2', args0: [{ type: 'input_value', name: 'LETTER', check: 'Number' }, { type: 'input_value', name: 'STRING' }], output: 'String', colour: COLORS.operators, inputsInline: true },
      { type: 'operator_length', message0: 'length of %1', args0: [{ type: 'input_value', name: 'STRING' }], output: 'Number', colour: COLORS.operators, inputsInline: true },
      { type: 'operator_contains', message0: '%1 contains %2 ?', args0: [{ type: 'input_value', name: 'STRING1' }, { type: 'input_value', name: 'STRING2' }], output: 'Boolean', colour: COLORS.operators, inputsInline: true },
      { type: 'operator_mod', message0: '%1 mod %2', args0: [{ type: 'input_value', name: 'NUM1', check: 'Number' }, { type: 'input_value', name: 'NUM2', check: 'Number' }], output: 'Number', colour: COLORS.operators, inputsInline: true },
      { type: 'operator_round', message0: 'round %1', args0: [{ type: 'input_value', name: 'NUM', check: 'Number' }], output: 'Number', colour: COLORS.operators, inputsInline: true },
      { type: 'operator_mathop', message0: '%1 of %2', args0: [{ type: 'field_dropdown', name: 'OPERATOR', options: [['abs', 'abs'], ['floor', 'floor'], ['ceiling', 'ceiling'], ['sqrt', 'sqrt'], ['sin', 'sin'], ['cos', 'cos'], ['tan', 'tan'], ['asin', 'asin'], ['acos', 'acos'], ['atan', 'atan'], ['ln', 'ln'], ['log', 'log'], ['e ^', 'e ^'], ['10 ^', '10 ^']] }, { type: 'input_value', name: 'NUM', check: 'Number' }], output: 'Number', colour: COLORS.operators, inputsInline: true },

      // ——— VARIABLES / LISTS ———
      { type: 'data_variable', message0: '%1', args0: [{ type: 'field_input', name: 'VARIABLE', text: 'my variable' }], output: null, colour: COLORS.variables },
      { type: 'data_setvariableto', message0: 'set %1 to %2', args0: [{ type: 'field_input', name: 'VARIABLE', text: 'my variable' }, { type: 'input_value', name: 'VALUE' }], previousStatement: null, nextStatement: null, colour: COLORS.variables, inputsInline: true },
      { type: 'data_changevariableby', message0: 'change %1 by %2', args0: [{ type: 'field_input', name: 'VARIABLE', text: 'my variable' }, { type: 'input_value', name: 'VALUE', check: 'Number' }], previousStatement: null, nextStatement: null, colour: COLORS.variables, inputsInline: true },
      { type: 'data_showvariable', message0: 'show variable %1', args0: [{ type: 'field_input', name: 'VARIABLE', text: 'my variable' }], previousStatement: null, nextStatement: null, colour: COLORS.variables, inputsInline: true },
      { type: 'data_hidevariable', message0: 'hide variable %1', args0: [{ type: 'field_input', name: 'VARIABLE', text: 'my variable' }], previousStatement: null, nextStatement: null, colour: COLORS.variables, inputsInline: true },
      { type: 'data_listcontents', message0: '%1', args0: [{ type: 'field_input', name: 'LIST', text: 'list' }], output: null, colour: COLORS.variables },
      { type: 'data_addtolist', message0: 'add %1 to %2', args0: [{ type: 'input_value', name: 'ITEM' }, { type: 'field_input', name: 'LIST', text: 'list' }], previousStatement: null, nextStatement: null, colour: COLORS.variables, inputsInline: true },
      { type: 'data_deleteoflist', message0: 'delete %1 of %2', args0: [{ type: 'input_value', name: 'INDEX' }, { type: 'field_input', name: 'LIST', text: 'list' }], previousStatement: null, nextStatement: null, colour: COLORS.variables, inputsInline: true },
      { type: 'data_deletealloflist', message0: 'delete all of %1', args0: [{ type: 'field_input', name: 'LIST', text: 'list' }], previousStatement: null, nextStatement: null, colour: COLORS.variables, inputsInline: true },
      { type: 'data_insertatlist', message0: 'insert %1 at %2 of %3', args0: [{ type: 'input_value', name: 'ITEM' }, { type: 'input_value', name: 'INDEX' }, { type: 'field_input', name: 'LIST', text: 'list' }], previousStatement: null, nextStatement: null, colour: COLORS.variables, inputsInline: true },
      { type: 'data_replaceitemoflist', message0: 'replace item %1 of %2 with %3', args0: [{ type: 'input_value', name: 'INDEX' }, { type: 'field_input', name: 'LIST', text: 'list' }, { type: 'input_value', name: 'ITEM' }], previousStatement: null, nextStatement: null, colour: COLORS.variables, inputsInline: true },
      { type: 'data_itemoflist', message0: 'item %1 of %2', args0: [{ type: 'input_value', name: 'INDEX' }, { type: 'field_input', name: 'LIST', text: 'list' }], output: null, colour: COLORS.variables, inputsInline: true },
      { type: 'data_itemnumoflist', message0: 'item # of %1 in %2', args0: [{ type: 'input_value', name: 'ITEM' }, { type: 'field_input', name: 'LIST', text: 'list' }], output: 'Number', colour: COLORS.variables, inputsInline: true },
      { type: 'data_lengthoflist', message0: 'length of %1', args0: [{ type: 'field_input', name: 'LIST', text: 'list' }], output: 'Number', colour: COLORS.variables, inputsInline: true },
      { type: 'data_listcontainsitem', message0: '%1 contains %2 ?', args0: [{ type: 'field_input', name: 'LIST', text: 'list' }, { type: 'input_value', name: 'ITEM' }], output: 'Boolean', colour: COLORS.variables, inputsInline: true },
      { type: 'data_showlist', message0: 'show list %1', args0: [{ type: 'field_input', name: 'LIST', text: 'list' }], previousStatement: null, nextStatement: null, colour: COLORS.variables, inputsInline: true },
      { type: 'data_hidelist', message0: 'hide list %1', args0: [{ type: 'field_input', name: 'LIST', text: 'list' }], previousStatement: null, nextStatement: null, colour: COLORS.variables, inputsInline: true },

      // ——— MY BLOCKS (custom) ———
      { type: 'procedures_definition', message0: 'define %1', args0: [{ type: 'field_input', name: 'NAME', text: 'my block' }], nextStatement: null, colour: COLORS.myblocks, hat: 'cap' },
      { type: 'procedures_call', message0: '%1', args0: [{ type: 'field_input', name: 'NAME', text: 'my block' }], previousStatement: null, nextStatement: null, colour: COLORS.myblocks, inputsInline: true },

      // Shadow helpers
      { type: 'math_number', message0: '%1', args0: [{ type: 'field_number', name: 'NUM', value: 0 }], output: 'Number', colour: COLORS.operators },
      { type: 'text', message0: '%1', args0: [{ type: 'field_input', name: 'TEXT', text: '' }], output: 'String', colour: COLORS.operators },
      { type: 'text_broadcast', message0: '%1', args0: [{ type: 'field_input', name: 'TEXT', text: 'message1' }], output: 'String', colour: COLORS.events }
    ]);
  }

  function shadowNumber(val) {
    return `<shadow type="math_number"><field name="NUM">${val}</field></shadow>`;
  }
  function shadowText(val) {
    return `<shadow type="text"><field name="TEXT">${val}</field></shadow>`;
  }
  function shadowBroadcast(val) {
    return `<shadow type="text_broadcast"><field name="TEXT">${val}</field></shadow>`;
  }

  function buildToolbox() {
    return {
      kind: 'categoryToolbox',
      contents: [
        {
          kind: 'category', name: 'Motion', colour: COLORS.motion,
          contents: [
            { kind: 'block', type: 'motion_movesteps', inputs: { STEPS: { shadow: { type: 'math_number', fields: { NUM: 10 } } } } },
            { kind: 'block', type: 'motion_turnright', inputs: { DEGREES: { shadow: { type: 'math_number', fields: { NUM: 15 } } } } },
            { kind: 'block', type: 'motion_turnleft', inputs: { DEGREES: { shadow: { type: 'math_number', fields: { NUM: 15 } } } } },
            { kind: 'block', type: 'motion_goto' },
            { kind: 'block', type: 'motion_gotoxy', inputs: { X: { shadow: { type: 'math_number', fields: { NUM: 0 } } }, Y: { shadow: { type: 'math_number', fields: { NUM: 0 } } } } },
            { kind: 'block', type: 'motion_glideto', inputs: { SECS: { shadow: { type: 'math_number', fields: { NUM: 1 } } } } },
            { kind: 'block', type: 'motion_glidesecstoxy', inputs: { SECS: { shadow: { type: 'math_number', fields: { NUM: 1 } } }, X: { shadow: { type: 'math_number', fields: { NUM: 0 } } }, Y: { shadow: { type: 'math_number', fields: { NUM: 0 } } } } },
            { kind: 'block', type: 'motion_pointindirection', inputs: { DIRECTION: { shadow: { type: 'math_number', fields: { NUM: 90 } } } } },
            { kind: 'block', type: 'motion_pointtowards' },
            { kind: 'block', type: 'motion_changexby', inputs: { DX: { shadow: { type: 'math_number', fields: { NUM: 10 } } } } },
            { kind: 'block', type: 'motion_setx', inputs: { X: { shadow: { type: 'math_number', fields: { NUM: 0 } } } } },
            { kind: 'block', type: 'motion_changeyby', inputs: { DY: { shadow: { type: 'math_number', fields: { NUM: 10 } } } } },
            { kind: 'block', type: 'motion_sety', inputs: { Y: { shadow: { type: 'math_number', fields: { NUM: 0 } } } } },
            { kind: 'block', type: 'motion_ifonedgebounce' },
            { kind: 'block', type: 'motion_setrotationstyle' },
            { kind: 'block', type: 'motion_xposition' },
            { kind: 'block', type: 'motion_yposition' },
            { kind: 'block', type: 'motion_direction' }
          ]
        },
        {
          kind: 'category', name: 'Looks', colour: COLORS.looks,
          contents: [
            { kind: 'block', type: 'looks_sayforsecs', inputs: { MESSAGE: { shadow: { type: 'text', fields: { TEXT: 'Hello!' } } }, SECS: { shadow: { type: 'math_number', fields: { NUM: 2 } } } } },
            { kind: 'block', type: 'looks_say', inputs: { MESSAGE: { shadow: { type: 'text', fields: { TEXT: 'Hello!' } } } } },
            { kind: 'block', type: 'looks_thinkforsecs', inputs: { MESSAGE: { shadow: { type: 'text', fields: { TEXT: 'Hmm...' } } }, SECS: { shadow: { type: 'math_number', fields: { NUM: 2 } } } } },
            { kind: 'block', type: 'looks_think', inputs: { MESSAGE: { shadow: { type: 'text', fields: { TEXT: 'Hmm...' } } } } },
            { kind: 'block', type: 'looks_switchcostumeto', inputs: { COSTUME: { shadow: { type: 'text', fields: { TEXT: 'costume1' } } } } },
            { kind: 'block', type: 'looks_nextcostume' },
            { kind: 'block', type: 'looks_switchbackdropto', inputs: { BACKDROP: { shadow: { type: 'text', fields: { TEXT: 'backdrop1' } } } } },
            { kind: 'block', type: 'looks_changesizeby', inputs: { CHANGE: { shadow: { type: 'math_number', fields: { NUM: 10 } } } } },
            { kind: 'block', type: 'looks_setsizeto', inputs: { SIZE: { shadow: { type: 'math_number', fields: { NUM: 100 } } } } },
            { kind: 'block', type: 'looks_changeeffectby', inputs: { CHANGE: { shadow: { type: 'math_number', fields: { NUM: 25 } } } } },
            { kind: 'block', type: 'looks_seteffectto', inputs: { VALUE: { shadow: { type: 'math_number', fields: { NUM: 0 } } } } },
            { kind: 'block', type: 'looks_cleargraphiceffects' },
            { kind: 'block', type: 'looks_show' },
            { kind: 'block', type: 'looks_hide' },
            { kind: 'block', type: 'looks_gotofrontback' },
            { kind: 'block', type: 'looks_goforwardbackwardlayers', inputs: { NUM: { shadow: { type: 'math_number', fields: { NUM: 1 } } } } },
            { kind: 'block', type: 'looks_costumenumbername' },
            { kind: 'block', type: 'looks_size' }
          ]
        },
        {
          kind: 'category', name: 'Sound', colour: COLORS.sound,
          contents: [
            { kind: 'block', type: 'sound_play', inputs: { SOUND_MENU: { shadow: { type: 'text', fields: { TEXT: 'pop' } } } } },
            { kind: 'block', type: 'sound_playuntildone', inputs: { SOUND_MENU: { shadow: { type: 'text', fields: { TEXT: 'pop' } } } } },
            { kind: 'block', type: 'sound_stopallsounds' },
            { kind: 'block', type: 'sound_changevolumeby', inputs: { VOLUME: { shadow: { type: 'math_number', fields: { NUM: -10 } } } } },
            { kind: 'block', type: 'sound_setvolumeto', inputs: { VOLUME: { shadow: { type: 'math_number', fields: { NUM: 100 } } } } },
            { kind: 'block', type: 'sound_volume' }
          ]
        },
        {
          kind: 'category', name: 'Events', colour: COLORS.events,
          contents: [
            { kind: 'block', type: 'event_whenflagclicked' },
            { kind: 'block', type: 'event_whenkeypressed' },
            { kind: 'block', type: 'event_whenthisspriteclicked' },
            { kind: 'block', type: 'event_whenbackdropswitchesto' },
            { kind: 'block', type: 'event_whenbroadcastreceived' },
            { kind: 'block', type: 'event_broadcast', inputs: { BROADCAST_INPUT: { shadow: { type: 'text_broadcast', fields: { TEXT: 'message1' } } } } },
            { kind: 'block', type: 'event_broadcastandwait', inputs: { BROADCAST_INPUT: { shadow: { type: 'text_broadcast', fields: { TEXT: 'message1' } } } } }
          ]
        },
        {
          kind: 'category', name: 'Control', colour: COLORS.control,
          contents: [
            { kind: 'block', type: 'control_wait', inputs: { DURATION: { shadow: { type: 'math_number', fields: { NUM: 1 } } } } },
            { kind: 'block', type: 'control_repeat', inputs: { TIMES: { shadow: { type: 'math_number', fields: { NUM: 10 } } } } },
            { kind: 'block', type: 'control_forever' },
            { kind: 'block', type: 'control_if' },
            { kind: 'block', type: 'control_if_else' },
            { kind: 'block', type: 'control_wait_until' },
            { kind: 'block', type: 'control_repeat_until' },
            { kind: 'block', type: 'control_stop' },
            { kind: 'block', type: 'control_create_clone_of' },
            { kind: 'block', type: 'control_start_as_clone' },
            { kind: 'block', type: 'control_delete_this_clone' }
          ]
        },
        {
          kind: 'category', name: 'Sensing', colour: COLORS.sensing,
          contents: [
            { kind: 'block', type: 'sensing_touchingobject' },
            { kind: 'block', type: 'sensing_touchingcolor' },
            { kind: 'block', type: 'sensing_distanceto' },
            { kind: 'block', type: 'sensing_askandwait', inputs: { QUESTION: { shadow: { type: 'text', fields: { TEXT: "What's your name?" } } } } },
            { kind: 'block', type: 'sensing_answer' },
            { kind: 'block', type: 'sensing_keypressed' },
            { kind: 'block', type: 'sensing_mousedown' },
            { kind: 'block', type: 'sensing_mousex' },
            { kind: 'block', type: 'sensing_mousey' },
            { kind: 'block', type: 'sensing_setdragmode' },
            { kind: 'block', type: 'sensing_timer' },
            { kind: 'block', type: 'sensing_resettimer' }
          ]
        },
        {
          kind: 'category', name: 'Operators', colour: COLORS.operators,
          contents: [
            { kind: 'block', type: 'operator_add', inputs: { NUM1: { shadow: { type: 'math_number', fields: { NUM: '' } } }, NUM2: { shadow: { type: 'math_number', fields: { NUM: '' } } } } },
            { kind: 'block', type: 'operator_subtract', inputs: { NUM1: { shadow: { type: 'math_number', fields: { NUM: '' } } }, NUM2: { shadow: { type: 'math_number', fields: { NUM: '' } } } } },
            { kind: 'block', type: 'operator_multiply', inputs: { NUM1: { shadow: { type: 'math_number', fields: { NUM: '' } } }, NUM2: { shadow: { type: 'math_number', fields: { NUM: '' } } } } },
            { kind: 'block', type: 'operator_divide', inputs: { NUM1: { shadow: { type: 'math_number', fields: { NUM: '' } } }, NUM2: { shadow: { type: 'math_number', fields: { NUM: '' } } } } },
            { kind: 'block', type: 'operator_random', inputs: { FROM: { shadow: { type: 'math_number', fields: { NUM: 1 } } }, TO: { shadow: { type: 'math_number', fields: { NUM: 10 } } } } },
            { kind: 'block', type: 'operator_gt', inputs: { OPERAND1: { shadow: { type: 'text', fields: { TEXT: '' } } }, OPERAND2: { shadow: { type: 'text', fields: { TEXT: '50' } } } } },
            { kind: 'block', type: 'operator_lt', inputs: { OPERAND1: { shadow: { type: 'text', fields: { TEXT: '' } } }, OPERAND2: { shadow: { type: 'text', fields: { TEXT: '50' } } } } },
            { kind: 'block', type: 'operator_equals', inputs: { OPERAND1: { shadow: { type: 'text', fields: { TEXT: '' } } }, OPERAND2: { shadow: { type: 'text', fields: { TEXT: '50' } } } } },
            { kind: 'block', type: 'operator_and' },
            { kind: 'block', type: 'operator_or' },
            { kind: 'block', type: 'operator_not' },
            { kind: 'block', type: 'operator_join', inputs: { STRING1: { shadow: { type: 'text', fields: { TEXT: 'apple ' } } }, STRING2: { shadow: { type: 'text', fields: { TEXT: 'banana' } } } } },
            { kind: 'block', type: 'operator_letter_of', inputs: { LETTER: { shadow: { type: 'math_number', fields: { NUM: 1 } } }, STRING: { shadow: { type: 'text', fields: { TEXT: 'apple' } } } } },
            { kind: 'block', type: 'operator_length', inputs: { STRING: { shadow: { type: 'text', fields: { TEXT: 'apple' } } } } },
            { kind: 'block', type: 'operator_contains', inputs: { STRING1: { shadow: { type: 'text', fields: { TEXT: 'apple' } } }, STRING2: { shadow: { type: 'text', fields: { TEXT: 'a' } } } } },
            { kind: 'block', type: 'operator_mod', inputs: { NUM1: { shadow: { type: 'math_number', fields: { NUM: '' } } }, NUM2: { shadow: { type: 'math_number', fields: { NUM: '' } } } } },
            { kind: 'block', type: 'operator_round', inputs: { NUM: { shadow: { type: 'math_number', fields: { NUM: '' } } } } },
            { kind: 'block', type: 'operator_mathop', inputs: { NUM: { shadow: { type: 'math_number', fields: { NUM: '' } } } } }
          ]
        },
        {
          kind: 'category', name: 'Variables', colour: COLORS.variables,
          contents: [
            { kind: 'button', text: 'Make a Variable', callbackKey: 'CREATE_VARIABLE' },
            { kind: 'block', type: 'data_setvariableto', inputs: { VALUE: { shadow: { type: 'math_number', fields: { NUM: 0 } } } } },
            { kind: 'block', type: 'data_changevariableby', inputs: { VALUE: { shadow: { type: 'math_number', fields: { NUM: 1 } } } } },
            { kind: 'block', type: 'data_showvariable' },
            { kind: 'block', type: 'data_hidevariable' },
            { kind: 'block', type: 'data_variable' },
            { kind: 'button', text: 'Make a List', callbackKey: 'CREATE_LIST' },
            { kind: 'block', type: 'data_addtolist', inputs: { ITEM: { shadow: { type: 'text', fields: { TEXT: 'thing' } } } } },
            { kind: 'block', type: 'data_deleteoflist', inputs: { INDEX: { shadow: { type: 'math_number', fields: { NUM: 1 } } } } },
            { kind: 'block', type: 'data_deletealloflist' },
            { kind: 'block', type: 'data_insertatlist', inputs: { ITEM: { shadow: { type: 'text', fields: { TEXT: 'thing' } } }, INDEX: { shadow: { type: 'math_number', fields: { NUM: 1 } } } } },
            { kind: 'block', type: 'data_replaceitemoflist', inputs: { INDEX: { shadow: { type: 'math_number', fields: { NUM: 1 } } }, ITEM: { shadow: { type: 'text', fields: { TEXT: 'thing' } } } } },
            { kind: 'block', type: 'data_itemoflist', inputs: { INDEX: { shadow: { type: 'math_number', fields: { NUM: 1 } } } } },
            { kind: 'block', type: 'data_itemnumoflist', inputs: { ITEM: { shadow: { type: 'text', fields: { TEXT: 'thing' } } } } },
            { kind: 'block', type: 'data_lengthoflist' },
            { kind: 'block', type: 'data_listcontainsitem', inputs: { ITEM: { shadow: { type: 'text', fields: { TEXT: 'thing' } } } } },
            { kind: 'block', type: 'data_showlist' },
            { kind: 'block', type: 'data_hidelist' }
          ]
        },
        {
          kind: 'category', name: 'My Blocks', colour: COLORS.myblocks,
          contents: [
            { kind: 'block', type: 'procedures_definition' },
            { kind: 'block', type: 'procedures_call' }
          ]
        }
      ]
    };
  }

  /** Custom Variables category flyout callback */
  function variablesFlyoutCallback(workspace) {
    const xmlList = [];
    const button = document.createElement('button');
    button.setAttribute('text', 'Make a Variable');
    button.setAttribute('callbackKey', 'CREATE_VARIABLE');
    xmlList.push(button);

    const vars = workspace.getAllVariables();
    if (vars.length) {
      const blockTypes = [
        'data_setvariableto', 'data_changevariableby', 'data_showvariable', 'data_hidevariable', 'data_variable'
      ];
      // Use JSON blocks via Blockly.utils.xml
      for (const v of vars) {
        const name = v.name;
        xmlList.push(Blockly.utils.xml.textToDom(
          `<block type="data_setvariableto"><field name="VARIABLE">${name}</field><value name="VALUE"><shadow type="math_number"><field name="NUM">0</field></shadow></value></block>`
        ));
        xmlList.push(Blockly.utils.xml.textToDom(
          `<block type="data_changevariableby"><field name="VARIABLE">${name}</field><value name="VALUE"><shadow type="math_number"><field name="NUM">1</field></shadow></value></block>`
        ));
        xmlList.push(Blockly.utils.xml.textToDom(
          `<block type="data_showvariable"><field name="VARIABLE">${name}</field></block>`
        ));
        xmlList.push(Blockly.utils.xml.textToDom(
          `<block type="data_hidevariable"><field name="VARIABLE">${name}</field></block>`
        ));
        xmlList.push(Blockly.utils.xml.textToDom(
          `<block type="data_variable"><field name="VARIABLE">${name}</field></block>`
        ));
      }
    }

    // Lists
    const listBtn = document.createElement('button');
    listBtn.setAttribute('text', 'Make a List');
    listBtn.setAttribute('callbackKey', 'CREATE_LIST');
    xmlList.push(listBtn);

    return xmlList;
  }

  function createDarkTheme() {
    return Blockly.Theme.defineTheme('veelearn_light', {
      base: Blockly.Themes.Classic,
      componentStyles: {
        workspaceBackgroundColour: '#f8fafc',
        toolboxBackgroundColour: '#ffffff',
        toolboxForegroundColour: '#1e293b',
        flyoutBackgroundColour: '#eef2f7',
        flyoutForegroundColour: '#1e293b',
        flyoutOpacity: 1,
        scrollbarColour: '#cbd5e1',
        insertionMarkerColour: '#2563eb',
        insertionMarkerOpacity: 0.5,
        scrollbarOpacity: 0.6,
        cursorColour: '#2563eb'
      }
    });
  }

  global.ScratchBlocks = {
    COLORS,
    KEY_OPTIONS,
    defineBlocks,
    buildToolbox,
    variablesFlyoutCallback,
    createDarkTheme
  };
})(window);
