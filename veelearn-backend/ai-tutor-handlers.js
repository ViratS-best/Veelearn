/**
 * Study coach: OpenRouter-backed chat with Socratic constraints,
 * validated course recommendations, and declarative widgetSpecs.
 */

const WIDGET_PRESETS = new Set([
    'function_plot',
    'desmos_graph',
    'geometry_board',
    'coordinate_plane',
    'number_line',
    'unit_circle',
    'triangle_lab',
    'area_shade',
    'parametric_plot',
    'inequality_region',
    'transformation_lab',
    'counting_grid',
    'spinning_box',
    'orbit_mesh',
    'scene3d',
    'particles2d',
    'fusion_dt',
    'projectile',
    'gravity_orbit',
    'pendulum',
    'spring_mass',
    'collision_1d',
    'wave_1d'
]);

const VIEW_TYPES = new Set([
    'function',
    'geometry',
    'desmos',
    'scene3d',
    'sim3d',
    'particles2d',
    'canvas2d'
]);

const INPUT_TYPES = new Set(['slider', 'select', 'toggle', 'button', 'number']);
const OUTPUT_TYPES = new Set(['stat', 'sparkline', 'text']);

const SOCRATIC_SYSTEM = `You are a study coach for Veelearn. Your job is to help students learn using real courses on this platform, not to do their work for them.

Rules (strict):
- Never give final numeric answers, final multiple-choice answers, or copy-paste solutions.
- Never provide complete code that solves an assignment; at most a tiny illustrative snippet with placeholders, or describe the algorithm in words.
- Give at most ONE clear next step: a question to ask themselves, a hint about which concept to review, or how to set up the problem.
- If they demand the answer, briefly refuse and offer a learning step instead.
- Keep text concise (under 180 words unless they ask for more detail on the method). Widget JSON does not count toward that limit.
- Match their level. If they say they are in grades 1–3 / elementary / don't know basic math, do NOT suggest algebra, competition math, or advanced topics. Prefer AVAILABLE_COURSES whose grade_level and title/description match their request.
- NEVER invent course titles. Only recommend courses that appear in AVAILABLE_COURSES. If the list is empty, say so and coach without naming fake courses.
- Use LaTeX with $...$ or $$...$$ for math in your prose.

Course recommendations (required when relevant):
- When the learner asks for a course, says what they want to learn, mentions a grade/level, or is clearly looking for where to start, you MUST recommend 2–3 courses from AVAILABLE_COURSES (or 1 if only one fits).
- Prefer higher like_count when several fit. Prefer matching grade_level. Mix single and master when both fit.
- Always end those turns with a new line exactly:
VEELEARN_RECOMMEND_JSON:
followed by a single JSON array like [{"courseId":123,"title":"Exact title from list","reason":"one short sentence"}].
- Use only courseIds from AVAILABLE_COURSES. If nothing fits, omit VEELEARN_RECOMMEND_JSON and say nothing in the catalog matches yet.

Interactive visualizations (required when relevant):
- When the learner asks to visualize, graph, plot, draw, simulate, make an interactive tool, or pastes geometry / AMC / Mathcounts / algebra problems where a figure helps, you MUST emit one or more widgetSpecs.
- Prefer widgets over saying you cannot draw. Do not invent fake course names instead of a figure.
- After your coaching text, emit exactly:
VEELEARN_WIDGET_JSON:
followed by a JSON array of widgetSpec objects.
- Each widgetSpec shape:
  {"id":"string","title":"string","objective":"string","view":{"type":"desmos|function|geometry|sim3d|scene3d|particles2d|canvas2d","width":520,"height":320},"state":{},"inputs":[{"key":"k","type":"slider|select|toggle|button|number","label":"...","min":0,"max":10,"step":0.1,"options":["a"]}],"outputs":[{"key":"k","type":"stat|sparkline|text","label":"..."}],"behavior":{"preset":"PRESET","params":{},"bindings":[{"from":"key","to":"target"}]}}
- Allowed presets: function_plot, desmos_graph, geometry_board, coordinate_plane, number_line, unit_circle, triangle_lab, area_shade, parametric_plot, inequality_region, transformation_lab, counting_grid, spinning_box, orbit_mesh, scene3d, particles2d, fusion_dt, projectile, gravity_orbit, pendulum, spring_mass, collision_1d, wave_1d
- Contest math: use geometry_board / desmos_graph / function_plot / coordinate_plane / triangle_lab / area_shade. Put figure elements in behavior.params.elements (points, segments, circles, polygons, functions). Put graph expressions in behavior.params.expressions as strings.
- 3D toys: spinning_box or orbit_mesh with size/color/rotationSpeed in state + slider inputs.
- Physics: fusion_dt, projectile, gravity_orbit, pendulum, spring_mass, collision_1d, wave_1d, particles2d.
- Never emit executable JavaScript. Only declarative JSON.`;

function guardSocraticReply(text) {
    if (!text || typeof text !== 'string') return text;
    const t = text.trim();
    if (/^\d+(\.\d+)?$/.test(t)) {
        return "I can't give a final answer like that. What is the first relationship or formula that applies? Try writing what you know and what you need to find.";
    }
    return text;
}

function tryParseJson(jsonPart) {
    if (!jsonPart) return null;
    let s = String(jsonPart)
        .replace(/^```(?:json)?\s*/i, '')
        .replace(/\s*```$/i, '')
        .trim();
    try {
        return JSON.parse(s);
    } catch (_) {
        const arrMatch = s.match(/\[[\s\S]*\]/);
        if (arrMatch) {
            try {
                return JSON.parse(arrMatch[0]);
            } catch (__) {
                /* ignore */
            }
        }
        const objMatch = s.match(/\{[\s\S]*\}/);
        if (objMatch) {
            try {
                return JSON.parse(objMatch[0]);
            } catch (__) {
                /* ignore */
            }
        }
    }
    return null;
}

function splitReplyAndPayloads(raw) {
    if (!raw || typeof raw !== 'string') {
        return { replyText: '', rawRecs: [], rawWidgets: [] };
    }

    const markers = [];
    const recRe = /VEELEARN_RECOMMEND_JSON:\s*/gi;
    const widRe = /VEELEARN_WIDGET_JSON:\s*/gi;
    let m;
    while ((m = recRe.exec(raw)) !== null) {
        markers.push({ type: 'rec', index: m.index, len: m[0].length });
    }
    while ((m = widRe.exec(raw)) !== null) {
        markers.push({ type: 'widget', index: m.index, len: m[0].length });
    }
    markers.sort((a, b) => a.index - b.index);

    if (!markers.length) {
        let replyText = raw;
        let rawRecs = [];
        let rawWidgets = [];
        const bareRec = raw.match(/(\[[\s\S]*"courseId"[\s\S]*\])/);
        if (bareRec) {
            const parsed = tryParseJson(bareRec[1]);
            if (Array.isArray(parsed)) {
                rawRecs = parsed;
                replyText = raw.replace(bareRec[0], '').trim();
            }
        }
        const bareWid = raw.match(/(\[[\s\S]*"behavior"[\s\S]*"preset"[\s\S]*\])/);
        if (bareWid) {
            const parsed = tryParseJson(bareWid[1]);
            if (Array.isArray(parsed)) {
                rawWidgets = parsed;
                replyText = replyText.replace(bareWid[0], '').trim();
            }
        }
        return { replyText: replyText.trim(), rawRecs, rawWidgets };
    }

    const replyText = raw.slice(0, markers[0].index).trim();
    let rawRecs = [];
    let rawWidgets = [];

    for (let i = 0; i < markers.length; i++) {
        const start = markers[i].index + markers[i].len;
        const end = i + 1 < markers.length ? markers[i + 1].index : raw.length;
        const parsed = tryParseJson(raw.slice(start, end));
        if (markers[i].type === 'rec' && Array.isArray(parsed)) {
            rawRecs = parsed;
        } else if (markers[i].type === 'widget') {
            if (Array.isArray(parsed)) rawWidgets = parsed;
            else if (parsed && typeof parsed === 'object') rawWidgets = [parsed];
        }
    }

    return { replyText: replyText.trim(), rawRecs, rawWidgets };
}

/** Back-compat alias used by older call sites / tests */
function splitReplyAndRecommendations(raw) {
    const { replyText, rawRecs } = splitReplyAndPayloads(raw);
    return { replyText, rawRecs };
}

function validateRecommendations(rawRecs, allowedCatalog) {
    const byId = new Map(allowedCatalog.map((c) => [Number(c.id), c]));
    const out = [];
    const seen = new Set();
    for (const r of rawRecs) {
        const id = parseInt(r?.courseId ?? r?.id, 10);
        if (Number.isNaN(id) || seen.has(id)) continue;
        const row = byId.get(id);
        if (!row) continue;
        seen.add(id);
        out.push({
            courseId: id,
            title: row.title,
            courseType: row.course_type || 'single',
            gradeLevel: row.grade_level != null ? Number(row.grade_level) : null,
            likeCount: Number(row.like_count) || 0,
            reason: typeof r.reason === 'string' ? r.reason.slice(0, 240) : 'A good match from Veelearn for what you asked.'
        });
        if (out.length >= 3) break;
    }
    return out;
}

function clampNum(n, lo, hi, fallback) {
    const v = Number(n);
    if (!Number.isFinite(v)) return fallback;
    return Math.min(hi, Math.max(lo, v));
}

function sanitizeExpr(expr) {
    if (typeof expr !== 'string') return null;
    const s = expr.trim().slice(0, 200);
    if (!s) return null;
    // Allow common math tokens; reject obvious script payloads
    if (/[;{}`\\]|<|>|script|function|=>|eval|window|document/i.test(s)) return null;
    if (!/^[\d\sA-Za-z_+\-*/^().,=<>!|&πθαβγ√]+$/.test(s)) return null;
    return s;
}

function sanitizeElements(elements) {
    if (!Array.isArray(elements)) return [];
    const allowedTypes = new Set([
        'point',
        'line',
        'segment',
        'circle',
        'polygon',
        'intersection',
        'tangent',
        'function',
        'text',
        'angle',
        'arc',
        'vector',
        'glider',
        'perpendicular',
        'parallel',
        'midpoint',
        'ray'
    ]);
    return elements.slice(0, 40).map((el, i) => {
        if (!el || typeof el !== 'object') return null;
        const type = String(el.type || '').toLowerCase();
        if (!allowedTypes.has(type)) return null;
        const out = { type };
        if (el.name != null) out.name = String(el.name).slice(0, 24);
        if (el.label != null) out.label = String(el.label).slice(0, 48);
        if (el.color != null) out.color = String(el.color).slice(0, 24);
        if (el.from != null) out.from = String(el.from).slice(0, 24);
        if (el.to != null) out.to = String(el.to).slice(0, 24);
        if (el.center != null) out.center = String(el.center).slice(0, 24);
        if (el.through != null) out.through = String(el.through).slice(0, 24);
        if (el.radius != null) out.radius = clampNum(el.radius, 0, 1000, 1);
        if (el.x != null) out.x = clampNum(el.x, -1000, 1000, 0);
        if (el.y != null) out.y = clampNum(el.y, -1000, 1000, 0);
        if (el.x2 != null) out.x2 = clampNum(el.x2, -1000, 1000, 0);
        if (el.y2 != null) out.y2 = clampNum(el.y2, -1000, 1000, 0);
        if (Array.isArray(el.points)) {
            out.points = el.points.slice(0, 16).map((p) => String(p).slice(0, 24));
        }
        if (el.expr != null) {
            const e = sanitizeExpr(el.expr);
            if (e) out.expr = e;
        }
        if (el.text != null) out.text = String(el.text).slice(0, 120);
        if (!out.name) out.name = `${type}_${i}`;
        return out;
    }).filter(Boolean);
}

function sanitizeParams(params) {
    if (!params || typeof params !== 'object' || Array.isArray(params)) return {};
    const out = {};
    for (const [k, v] of Object.entries(params)) {
        const key = String(k).slice(0, 48);
        if (key === 'elements') {
            out.elements = sanitizeElements(v);
            continue;
        }
        if (key === 'expressions' && Array.isArray(v)) {
            out.expressions = v.map(sanitizeExpr).filter(Boolean).slice(0, 12);
            continue;
        }
        if (key === 'objects' && Array.isArray(v)) {
            out.objects = v.slice(0, 24).map((o) => {
                if (!o || typeof o !== 'object') return null;
                return {
                    type: String(o.type || 'box').slice(0, 24),
                    color: o.color != null ? String(o.color).slice(0, 24) : undefined,
                    x: clampNum(o.x, -100, 100, 0),
                    y: clampNum(o.y, -100, 100, 0),
                    z: clampNum(o.z, -100, 100, 0),
                    size: clampNum(o.size, 0.01, 50, 1),
                    expr: sanitizeExpr(o.expr) || undefined
                };
            }).filter(Boolean);
            continue;
        }
        if (key === 'boundingbox' && Array.isArray(v) && v.length === 4) {
            out.boundingbox = v.map((n) => clampNum(n, -1000, 1000, 0));
            continue;
        }
        if (typeof v === 'number' && Number.isFinite(v)) {
            out[key] = clampNum(v, -1e6, 1e6, 0);
        } else if (typeof v === 'boolean') {
            out[key] = v;
        } else if (typeof v === 'string') {
            const e = sanitizeExpr(v);
            out[key] = e != null ? e : String(v).slice(0, 120);
        } else if (Array.isArray(v) && v.every((x) => typeof x === 'number')) {
            out[key] = v.slice(0, 8).map((n) => clampNum(n, -1e6, 1e6, 0));
        }
    }
    return out;
}

function sanitizeState(state) {
    if (!state || typeof state !== 'object' || Array.isArray(state)) return {};
    const out = {};
    for (const [k, v] of Object.entries(state)) {
        const key = String(k).slice(0, 48);
        if (typeof v === 'number' && Number.isFinite(v)) out[key] = clampNum(v, -1e9, 1e9, 0);
        else if (typeof v === 'boolean') out[key] = v;
        else if (typeof v === 'string') out[key] = String(v).slice(0, 64);
        else if (Array.isArray(v) && v.every((x) => typeof x === 'number') && v.length <= 64) {
            out[key] = v.map((n) => clampNum(n, -1e9, 1e9, 0));
        }
    }
    return out;
}

function sanitizeInputs(inputs) {
    if (!Array.isArray(inputs)) return [];
    return inputs.slice(0, 12).map((inp) => {
        if (!inp || typeof inp !== 'object') return null;
        const type = String(inp.type || 'slider').toLowerCase();
        if (!INPUT_TYPES.has(type)) return null;
        const key = String(inp.key || '').slice(0, 48);
        if (!key) return null;
        const out = {
            key,
            type,
            label: String(inp.label || key).slice(0, 64)
        };
        if (type === 'slider' || type === 'number') {
            out.min = clampNum(inp.min, -1e6, 1e6, 0);
            out.max = clampNum(inp.max, -1e6, 1e6, 100);
            out.step = clampNum(inp.step, 0.0001, 1e6, 1);
            if (out.min > out.max) {
                const t = out.min;
                out.min = out.max;
                out.max = t;
            }
        }
        if (type === 'select' && Array.isArray(inp.options)) {
            out.options = inp.options.map((o) => String(o).slice(0, 32)).slice(0, 16);
        }
        if (type === 'button' && inp.action != null) {
            out.action = String(inp.action).slice(0, 32);
        }
        return out;
    }).filter(Boolean);
}

function sanitizeOutputs(outputs) {
    if (!Array.isArray(outputs)) return [];
    return outputs.slice(0, 8).map((o) => {
        if (!o || typeof o !== 'object') return null;
        const type = String(o.type || 'stat').toLowerCase();
        if (!OUTPUT_TYPES.has(type)) return null;
        const key = String(o.key || '').slice(0, 48);
        if (!key) return null;
        return {
            key,
            type,
            label: String(o.label || key).slice(0, 64)
        };
    }).filter(Boolean);
}

function validateWidgetSpecs(rawWidgets) {
    if (!Array.isArray(rawWidgets)) return [];
    const out = [];
    for (const w of rawWidgets.slice(0, 3)) {
        if (!w || typeof w !== 'object') continue;
        const preset = String(w.behavior?.preset || w.preset || '').trim();
        if (!WIDGET_PRESETS.has(preset)) continue;

        let viewType = String(w.view?.type || '').toLowerCase();
        if (!VIEW_TYPES.has(viewType)) {
            // Infer view from preset
            if (preset === 'desmos_graph') viewType = 'desmos';
            else if (
                [
                    'function_plot',
                    'geometry_board',
                    'coordinate_plane',
                    'number_line',
                    'unit_circle',
                    'triangle_lab',
                    'area_shade',
                    'parametric_plot',
                    'inequality_region',
                    'transformation_lab',
                    'counting_grid'
                ].includes(preset)
            ) {
                viewType = preset === 'desmos_graph' ? 'desmos' : preset.includes('geometry') || preset === 'triangle_lab' ? 'geometry' : 'function';
            } else if (preset === 'spinning_box' || preset === 'orbit_mesh' || preset === 'scene3d') {
                viewType = preset === 'scene3d' ? 'scene3d' : 'sim3d';
            } else if (preset === 'particles2d' || preset === 'fusion_dt') {
                viewType = 'particles2d';
            } else {
                viewType = 'canvas2d';
            }
        }

        const view = {
            type: viewType,
            width: clampNum(w.view?.width, 240, 900, 520),
            height: clampNum(w.view?.height, 180, 700, 320)
        };

        const behavior = {
            preset,
            params: sanitizeParams(w.behavior?.params || w.params || {}),
            bindings: Array.isArray(w.behavior?.bindings)
                ? w.behavior.bindings.slice(0, 20).map((b) => ({
                      from: String(b.from || '').slice(0, 48),
                      to: String(b.to || '').slice(0, 48)
                  })).filter((b) => b.from && b.to)
                : []
        };

        out.push({
            id: String(w.id || `w${out.length + 1}`).slice(0, 48),
            title: String(w.title || behavior.preset).slice(0, 80),
            objective: w.objective != null ? String(w.objective).slice(0, 200) : '',
            view,
            state: sanitizeState(w.state),
            inputs: sanitizeInputs(w.inputs),
            outputs: sanitizeOutputs(w.outputs),
            behavior
        });
    }
    return out;
}

function extractGradeHints(message) {
    const msg = String(message || '').toLowerCase();
    const grades = new Set();

    const range = msg.match(/\b(?:grades?\s*)?(\d{1,2})\s*[-–to]+\s*(\d{1,2})(?:\s*(?:st|nd|rd|th)?\s*grade)?\b/);
    if (range) {
        const a = parseInt(range[1], 10);
        const b = parseInt(range[2], 10);
        if (!Number.isNaN(a) && !Number.isNaN(b)) {
            const lo = Math.min(a, b);
            const hi = Math.max(a, b);
            for (let g = lo; g <= hi && g <= 13; g++) grades.add(g);
        }
    }

    const singles = msg.matchAll(/\b(?:grade\s*)?(\d{1,2})(?:st|nd|rd|th)?\s*grade\b/g);
    for (const m of singles) {
        const g = parseInt(m[1], 10);
        if (!Number.isNaN(g) && g >= 1 && g <= 13) grades.add(g);
    }

    if (/\b(elementary|primary|k-?5|kindergarten)\b/.test(msg)) {
        [1, 2, 3, 4, 5].forEach((g) => grades.add(g));
    }
    if (/\b(middle\s*school|junior\s*high)\b/.test(msg)) {
        [6, 7, 8].forEach((g) => grades.add(g));
    }
    if (/\b(high\s*school|secondary)\b/.test(msg)) {
        [9, 10, 11, 12].forEach((g) => grades.add(g));
    }
    if (/\b(1st|first)\s*grade\b/.test(msg)) grades.add(1);
    if (/\b(2nd|second)\s*grade\b/.test(msg)) grades.add(2);
    if (/\b(3rd|third)\s*grade\b/.test(msg)) grades.add(3);

    return [...grades];
}

function tokenizeForMatch(text) {
    return String(text || '')
        .toLowerCase()
        .replace(/[^a-z0-9\s+#]/g, ' ')
        .split(/\s+/)
        .filter((w) => w.length > 2 && !['the', 'and', 'for', 'want', 'learn', 'course', 'with', 'that', 'this', 'have', 'dont', "don't", 'know', 'please', 'recommend', 'something', 'about'].includes(w));
}

function wantsCourseRecommendation(message) {
    const msg = String(message || '').toLowerCase();
    return (
        /\b(recommend|suggestion|suggest|enroll|course|learn|stud(y|ying)|teach me|where (do|should) i start|help me (with|learn)|grade|math|science|physics|chem|algebra|geometry|bio)\b/.test(
            msg
        ) || extractGradeHints(msg).length > 0
    );
}

function wantsVisualization(message) {
    const msg = String(message || '').toLowerCase();
    return (
        /\b(visuali[sz]e|graph|plot|draw|diagram|simulat|interactive|3d|three.?d|fusion|particle|animat|show (me )?(this|the)|make (a |an )?(tool|sim|widget|demo)|spinning|cube|sphere)\b/.test(
            msg
        ) ||
        /\b(amc|mathcounts|geometry|quadratic|inscribed|tangent|intersect|circle|triangle|parabola|polynomial|unit circle|number line)\b/.test(
            msg
        ) ||
        /y\s*=\s*[^\n]{1,80}/i.test(message) ||
        /\$\$[\s\S]+\$\$/.test(message)
    );
}

function autoFunctionWidget(message) {
    const m =
        String(message).match(/y\s*=\s*([^\n]+)/i) ||
        String(message).match(/\bgraph\s+(?:of\s+)?([^\n]+)/i) ||
        String(message).match(/\bplot\s+(?:of\s+)?([^\n]+)/i);
    if (!m) return [];
    const expr = sanitizeExpr(m[1].replace(/[.?!]+$/, '').trim());
    if (!expr) return [];
    return validateWidgetSpecs([
        {
            id: 'auto-fn',
            title: 'Graph',
            objective: 'Auto graph from your expression',
            view: { type: 'desmos', width: 520, height: 320 },
            state: {},
            inputs: [],
            outputs: [],
            behavior: {
                preset: 'desmos_graph',
                params: { expressions: [expr.startsWith('y') ? expr : `y=${expr}`] }
            }
        }
    ]);
}

/**
 * Server-side ranking when the model forgets VEELEARN_RECOMMEND_JSON.
 */
function fallbackRecommendations(message, catalog, limit = 3) {
    if (!catalog?.length) return [];
    const msg = String(message || '').toLowerCase();
    const grades = extractGradeHints(msg);
    const tokens = tokenizeForMatch(msg);

    const scored = catalog.map((c) => {
        const title = String(c.title || '').toLowerCase();
        const desc = String(c.desc_preview || c.description || '').toLowerCase();
        const hay = `${title} ${desc}`;
        let score = Number(c.like_count) || 0;

        for (const t of tokens) {
            if (title.includes(t)) score += 12;
            else if (hay.includes(t)) score += 6;
        }

        const g = c.grade_level != null ? Number(c.grade_level) : null;
        if (grades.length && g != null && grades.includes(g)) score += 40;
        else if (grades.length && g != null) {
            const near = grades.some((x) => Math.abs(x - g) <= 1);
            score += near ? 15 : -25;
        }

        if (grades.length && grades.every((x) => x <= 5)) {
            if (/\b(algebra|calculus|competition|amc|amc\s*8|olympiad|trigonometry|linear algebra)\b/i.test(hay)) {
                score -= 50;
            }
            if (/\b(addition|subtraction|counting|number|fraction|multiply|division|grade|elementary|basic)\b/i.test(hay)) {
                score += 20;
            }
        }

        return { course: c, score };
    });

    scored.sort((a, b) => b.score - a.score || (Number(b.course.like_count) || 0) - (Number(a.course.like_count) || 0));

    const top = scored.filter((s) => s.score > 0).slice(0, limit);
    const pick = top.length ? top : scored.slice(0, Math.min(limit, scored.length));

    return pick.map(({ course: row }) => ({
        courseId: Number(row.id),
        title: row.title,
        courseType: row.course_type || 'single',
        gradeLevel: row.grade_level != null ? Number(row.grade_level) : null,
        likeCount: Number(row.like_count) || 0,
        reason: grades.length
            ? `Matches what you asked for around grades ${grades.join('–')}.`
            : 'A popular Veelearn course that fits what you asked about.'
    }));
}

function parseWidgetsJsonColumn(raw) {
    if (raw == null || raw === '') return [];
    try {
        const parsed = typeof raw === 'string' ? JSON.parse(raw) : raw;
        return Array.isArray(parsed) ? parsed : [];
    } catch (_) {
        return [];
    }
}

function createAiTutorHandlers({ query, openRouterChatCompletion, apiResponse }) {
    async function maybeRefreshLearningProfile(userId) {
        const rows = await query(
            'SELECT COUNT(*) AS cnt FROM ai_tutor_messages WHERE user_id = ? AND role = ?',
            [userId, 'user']
        );
        const cnt = rows[0]?.cnt || 0;
        if (cnt === 0 || cnt % 10 !== 0) return;

        const recent = await query(
            `SELECT role, content FROM ai_tutor_messages WHERE user_id = ? ORDER BY created_at DESC LIMIT 24`,
            [userId]
        );
        const lines = recent
            .reverse()
            .map((r) => `${r.role}: ${String(r.content).slice(0, 500)}`)
            .join('\n');

        const summaryMessages = [
            {
                role: 'system',
                content:
                    'Summarize in 3-5 short bullet points how this student tends to learn: question style, common struggles, pace, and grade/level if known. No PII, no email. Plain text bullets only.'
            },
            { role: 'user', content: lines }
        ];

        try {
            const s = await openRouterChatCompletion(summaryMessages, { max_tokens: 300, temperature: 0.25 });
            await query(
                `INSERT INTO user_learning_profile (user_id, summary_text) VALUES (?, ?)
                 ON DUPLICATE KEY UPDATE summary_text = VALUES(summary_text)`,
                [userId, s.slice(0, 4000)]
            );
        } catch (e) {
            console.warn('Learning profile refresh skipped:', e.message);
        }
    }

    return {
        async chat(req, res) {
            const userId = req.user.id;
            let message = typeof req.body?.message === 'string' ? req.body.message.trim() : '';
            if (!message) {
                return apiResponse(res, 400, 'Message is required');
            }
            if (message.length > 8000) {
                message = message.slice(0, 8000);
            }

            let courseId = null;
            if (req.body?.courseId != null && req.body.courseId !== '') {
                const cid = parseInt(req.body.courseId, 10);
                if (!Number.isNaN(cid)) courseId = cid;
            }

            let courseTitle = null;
            if (courseId != null) {
                const cr = await query('SELECT id, title FROM courses WHERE id = ? LIMIT 1', [courseId]);
                if (cr.length) courseTitle = cr[0].title;
            }

            const enrolled = await query(
                `SELECT c.id, c.title FROM enrollments e
                 JOIN courses c ON c.id = e.course_id WHERE e.user_id = ? ORDER BY c.title ASC`,
                [userId]
            );

            const catalog = await query(
                `SELECT c.id, c.title, c.course_type, c.grade_level, IFNULL(c.like_count, 0) AS like_count,
                        LEFT(IFNULL(c.description,''), 220) AS desc_preview
                 FROM courses c
                 WHERE c.status = 'approved'
                 AND c.id NOT IN (SELECT course_id FROM enrollments WHERE user_id = ?)
                 ORDER BY IFNULL(c.like_count, 0) DESC, c.title ASC LIMIT 80`,
                [userId]
            );

            const quizRow = await query(
                `SELECT COUNT(*) AS total, SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) AS correct
                 FROM user_quiz_attempts WHERE user_id = ?`,
                [userId]
            );
            const totalQ = quizRow[0]?.total || 0;
            const correctQ = quizRow[0]?.correct || 0;

            let profileSummary = '';
            const prof = await query('SELECT summary_text FROM user_learning_profile WHERE user_id = ?', [userId]);
            if (prof.length && prof[0].summary_text) {
                profileSummary = String(prof[0].summary_text).slice(0, 1500);
            }

            const historyRows = await query(
                `SELECT role, content FROM ai_tutor_messages WHERE user_id = ? ORDER BY created_at DESC LIMIT 24`,
                [userId]
            );
            historyRows.reverse();

            const availableLines = catalog
                .map((c) => {
                    const g = c.grade_level != null ? `grade=${c.grade_level}` : 'grade=any';
                    const d = String(c.desc_preview || '').replace(/\s+/g, ' ').trim();
                    return `${c.id}: ${c.title} [${c.course_type || 'single'}, ${g}, likes=${c.like_count || 0}] ${d ? `— ${d}` : ''}`;
                })
                .join('\n');
            const enrolledLines = enrolled.map((c) => `${c.id}: ${c.title}`).join('\n') || '(none)';

            const contextBlock = [
                `Enrolled courses:\n${enrolledLines}`,
                `Quiz attempts (all time): ${correctQ} correct of ${totalQ} recorded.`,
                courseTitle ? `Current course context: "${courseTitle}" (id ${courseId}).` : 'No specific course context.',
                profileSummary ? `Learning profile notes:\n${profileSummary}` : '',
                `AVAILABLE_COURSES (not enrolled; suggest ONLY from this list; include grade_level when matching):\n${availableLines || '(none available)'}`
            ]
                .filter(Boolean)
                .join('\n\n');

            const historyMessages = [];
            for (const row of historyRows) {
                if (row.role !== 'user' && row.role !== 'assistant') continue;
                historyMessages.push({
                    role: row.role,
                    content: String(row.content).slice(0, 4000)
                });
            }

            const forceViz = wantsVisualization(message);
            const messages = [
                { role: 'system', content: SOCRATIC_SYSTEM },
                {
                    role: 'system',
                    content: forceViz
                        ? `${contextBlock}\n\nIMPORTANT: The learner's latest message needs a visualization or interactive widget. You MUST include VEELEARN_WIDGET_JSON with at least one valid widgetSpec.`
                        : `Personalization context:\n${contextBlock}`
                },
                ...historyMessages,
                { role: 'user', content: message }
            ];

            let rawReply;
            try {
                rawReply = await openRouterChatCompletion(messages, {
                    max_tokens: forceViz ? 2200 : 1400,
                    temperature: 0.35
                });
            } catch (e) {
                console.error('OpenRouter tutor error:', e.message);
                if (e.code === 'OPENROUTER_NOT_CONFIGURED') {
                    return apiResponse(res, 503, 'Study coach is not configured on this server');
                }
                if (e.code === 'OPENROUTER_RATE_LIMITED' || e.status === 429) {
                    return apiResponse(
                        res,
                        429,
                        'Study coach is temporarily rate-limited. Please wait a minute and try again.'
                    );
                }
                if (e.code === 'OPENROUTER_MODEL_UNAVAILABLE' || e.status === 404) {
                    return apiResponse(
                        res,
                        503,
                        'Study coach model is temporarily unavailable. Please try again shortly.'
                    );
                }
                return apiResponse(res, 502, 'Study coach is temporarily unavailable. Please try again later.');
            }

            let { replyText, rawRecs, rawWidgets } = splitReplyAndPayloads(rawReply);
            let safeReply = guardSocraticReply(replyText);
            let recommendations = validateRecommendations(rawRecs, catalog);
            let widgets = validateWidgetSpecs(rawWidgets);

            // One JSON-only retry when visualization is required but missing
            if (forceViz && !widgets.length) {
                try {
                    const retryReply = await openRouterChatCompletion(
                        [
                            { role: 'system', content: SOCRATIC_SYSTEM },
                            {
                                role: 'system',
                                content:
                                    'Emit ONLY VEELEARN_WIDGET_JSON: then a JSON array of 1 widgetSpec for the user request. No prose. Use an allowed preset. For graphs use desmos_graph or function_plot. For geometry use geometry_board with params.elements.'
                            },
                            { role: 'user', content: message }
                        ],
                        { max_tokens: 1600, temperature: 0.2 }
                    );
                    const retryParts = splitReplyAndPayloads(
                        /VEELEARN_WIDGET_JSON:/i.test(retryReply)
                            ? retryReply
                            : `VEELEARN_WIDGET_JSON:\n${retryReply}`
                    );
                    const retryWidgets = validateWidgetSpecs(retryParts.rawWidgets);
                    if (retryWidgets.length) {
                        widgets = retryWidgets;
                        if (!safeReply) {
                            safeReply =
                                "Here's an interactive figure for this — try the controls and tell me what you notice.";
                        }
                    }
                } catch (retryErr) {
                    console.warn('Widget retry skipped:', retryErr.message);
                }
            }

            if (forceViz && !widgets.length) {
                widgets = autoFunctionWidget(message);
            }

            if (!recommendations.length && catalog.length && wantsCourseRecommendation(message) && !forceViz) {
                recommendations = fallbackRecommendations(message, catalog, 3);
                if (recommendations.length && !/veelearn course|recommended course|here are (a few )?courses/i.test(safeReply)) {
                    safeReply = `${safeReply}\n\nI picked a few Veelearn courses that fit — tap View / Enroll below to open one.`.trim();
                }
            }

            const widgetsJson = widgets.length ? JSON.stringify(widgets) : null;

            try {
                await query(
                    'INSERT INTO ai_tutor_messages (user_id, role, content, course_id, widgets_json) VALUES (?, ?, ?, ?, ?)',
                    [userId, 'user', message, courseId, null]
                );
                await query(
                    'INSERT INTO ai_tutor_messages (user_id, role, content, course_id, widgets_json) VALUES (?, ?, ?, ?, ?)',
                    [userId, 'assistant', safeReply, courseId, widgetsJson]
                );
            } catch (dbErr) {
                // Fallback if widgets_json column not yet migrated
                if (dbErr && /widgets_json|Unknown column/i.test(String(dbErr.message || dbErr))) {
                    try {
                        await query(
                            'INSERT INTO ai_tutor_messages (user_id, role, content, course_id) VALUES (?, ?, ?, ?)',
                            [userId, 'user', message, courseId]
                        );
                        await query(
                            'INSERT INTO ai_tutor_messages (user_id, role, content, course_id) VALUES (?, ?, ?, ?)',
                            [userId, 'assistant', safeReply, courseId]
                        );
                    } catch (dbErr2) {
                        console.error('ai_tutor_messages insert:', dbErr2);
                        return apiResponse(res, 500, 'Could not save conversation');
                    }
                } else {
                    console.error('ai_tutor_messages insert:', dbErr);
                    return apiResponse(res, 500, 'Could not save conversation');
                }
            }

            setImmediate(() => {
                maybeRefreshLearningProfile(userId).catch(() => {});
            });

            return apiResponse(res, 200, 'OK', { reply: safeReply, recommendations, widgets });
        },

        async history(req, res) {
            const userId = req.user.id;
            let limit = parseInt(req.query.limit, 10);
            if (Number.isNaN(limit)) limit = 30;
            limit = Math.min(50, Math.max(1, limit));

            try {
                let rows;
                try {
                    rows = await query(
                        `SELECT id, role, content, course_id, widgets_json, created_at FROM ai_tutor_messages
                         WHERE user_id = ? ORDER BY created_at DESC LIMIT ?`,
                        [userId, limit]
                    );
                } catch (colErr) {
                    if (/widgets_json|Unknown column/i.test(String(colErr.message || colErr))) {
                        rows = await query(
                            `SELECT id, role, content, course_id, created_at FROM ai_tutor_messages
                             WHERE user_id = ? ORDER BY created_at DESC LIMIT ?`,
                            [userId, limit]
                        );
                    } else {
                        throw colErr;
                    }
                }
                rows.reverse();
                const data = rows.map((r) => ({
                    id: r.id,
                    role: r.role,
                    content: r.content,
                    course_id: r.course_id,
                    created_at: r.created_at,
                    widgets: parseWidgetsJsonColumn(r.widgets_json)
                }));
                return apiResponse(res, 200, 'OK', data);
            } catch (e) {
                console.error('ai tutor history:', e);
                return apiResponse(res, 500, 'Could not load history');
            }
        }
    };
}

module.exports = createAiTutorHandlers;
module.exports.splitReplyAndRecommendations = splitReplyAndRecommendations;
module.exports.splitReplyAndPayloads = splitReplyAndPayloads;
module.exports.validateWidgetSpecs = validateWidgetSpecs;
module.exports.wantsVisualization = wantsVisualization;
