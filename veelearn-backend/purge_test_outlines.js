'use strict';

/**
 * Remove placeholder outlines/courses ("a", "Outline Test 1794761977545", …).
 *
 *   node purge_test_outlines.js           # dry run: list what would go
 *   node purge_test_outlines.js --apply   # delete the listed rows
 *
 * Safety: only rows whose TITLE is a placeholder are candidates, and a row that
 * real learners are attached to (an enrollment or a classroom assignment) is
 * skipped and reported. Nothing else is touched.
 */

require('dotenv').config();
const { query, close } = require('./db');
const quality = require('./course-quality');

async function main() {
    const apply = process.argv.includes('--apply');

    const rows = await query(
        `SELECT c.id, c.title, c.status, c.creator_id, u.email AS creator_email,
                (SELECT outline_json FROM course_outlines co WHERE co.course_id = c.id LIMIT 1) AS outline_json
         FROM courses c
         LEFT JOIN users u ON u.id = c.creator_id
         ORDER BY c.id ASC`
    );

    const candidates = rows.filter((row) => quality.isTestTitle(row.title));
    if (!candidates.length) {
        console.log('No placeholder courses found.');
        await close();
        return;
    }

    const summary = [];
    for (const row of candidates) {
        const enrollments = await query('SELECT COUNT(*) AS c FROM enrollments WHERE course_id = ?', [row.id]);
        const assignments = await query('SELECT COUNT(*) AS c FROM classroom_assignments WHERE course_id = ?', [row.id]);
        const learners = Number((enrollments[0] && enrollments[0].c) || 0);
        const assigned = Number((assignments[0] && assignments[0].c) || 0);
        const stats = quality.outlineStats(row.outline_json);
        summary.push({ row, learners, assigned, stats, keep: learners > 0 || assigned > 0 });
    }

    console.log(`${candidates.length} placeholder course(s):\n`);
    for (const item of summary) {
        const { row, stats } = item;
        const mark = item.keep ? 'KEEP' : apply ? 'DELETE' : 'would delete';
        console.log(
            `  [${mark}] #${row.id} "${row.title}" · ${row.status || 'draft'} · ${row.creator_email || 'unknown creator'} · ` +
                `${stats.units} unit(s), ${stats.skills} skill(s), ${stats.questions} question(s)` +
                (item.keep ? ` · ${item.learners} enrollment(s), ${item.assigned} assignment(s)` : '')
        );
    }

    const removable = summary.filter((item) => !item.keep);
    if (!apply) {
        console.log(`\nDry run. ${removable.length} row(s) would be deleted. Re-run with --apply.`);
        await close();
        return;
    }

    for (const { row } of removable) {
        const id = Number(row.id);
        await query('DELETE FROM course_outlines WHERE course_id = ?', [id]);
        await query('UPDATE sessions SET course_id = NULL WHERE course_id = ?', [id]);
        await query('DELETE FROM enrollments WHERE course_id = ?', [id]);
        await query('DELETE FROM course_questions WHERE course_id = ?', [id]);
        await query('UPDATE qbank_items SET live = 0 WHERE course_id = ?', [id]);
        await query('DELETE FROM course_units WHERE parent_course_id = ? OR child_course_id = ?', [id, id]);
        await query('DELETE FROM courses WHERE id = ?', [id]);
        console.log(`  deleted #${id} "${row.title}"`);
    }
    console.log(`\nDeleted ${removable.length} placeholder course(s).`);
    await close();
}

main().catch(async (err) => {
    console.error('purge failed:', err.message);
    try {
        await close();
    } catch (_) {
        /* pool already closed */
    }
    process.exit(1);
});
