'use strict';
const assert = require('node:assert/strict');
const M = require('./model.js');
let checks = 0;
function check(name, fn) {
  fn();
  checks++;
  console.log('PASS ' + name);
}
const demo = M.demoProjects('2026-10-13');
const valid = { title: '新しい制作', description: '説明', category: 'app', status: 'planning', priority: 'normal', dueDate: '' };

check('demo has four synthetic projects and valid persisted shape', () => {
  assert.equal(demo.length, 4);
  assert.ok(M.isPersistedState({ version: 1, projects: demo }));
});
check('fresh demo copies do not share mutable tasks', () => {
  const second = M.demoProjects('2026-10-13');
  second[0].tasks[0].done = false;
  assert.equal(demo[0].tasks[0].done, true);
});
check('project validation trims input and accepts an omitted date', () => {
  const result = M.validateProjectInput({ ...valid, title: '  新しい制作  ' });
  assert.equal(result.valid, true); assert.equal(result.value.title, '新しい制作');
});
check('blank project name produces a field error', () => {
  const result = M.validateProjectInput({ ...valid, title: '　 ' });
  assert.equal(result.valid, false); assert.ok(result.errors.title);
});
check('project name and description length limits are enforced', () => {
  const result = M.validateProjectInput({ ...valid, title: 'a'.repeat(81), description: 'b'.repeat(601) });
  assert.ok(result.errors.title && result.errors.description);
});
check('impossible calendar dates are rejected', () => {
  assert.equal(M.validateProjectInput({ ...valid, dueDate: '2026-02-30' }).valid, false);
  assert.equal(M.validateProjectInput({ ...valid, dueDate: '2028-02-29' }).valid, true);
});
check('unknown status, category, and priority are rejected', () => {
  const result = M.validateProjectInput({ ...valid, status: '__proto__', category: 'missing', priority: 'urgent' });
  assert.deepEqual(Object.keys(result.errors).sort(), ['category', 'priority', 'status']);
});
check('task names must contain text and fit the limit', () => {
  assert.equal(M.validateTaskInput({ title: ' ' }).valid, false);
  assert.equal(M.validateTaskInput({ title: 'a'.repeat(121) }).valid, false);
  assert.deepEqual(M.validateTaskInput({ title: '  名前  ' }).value, { title: '名前' });
});
check('full-width and multi-term search match together', () => {
  assert.deepEqual(M.filterProjects(demo, { query: 'ＵＸ guide', status: 'all', category: 'guide' }).map(x => x.id), ['demo-ui']);
});
check('search includes a project task', () => {
  assert.deepEqual(M.filterProjects(demo, { query: 'スマートフォン', status: 'all', category: 'all' }).map(x => x.id), ['demo-ui']);
});
check('status and category filters combine', () => {
  assert.deepEqual(M.filterProjects(demo, { query: '', status: 'active', category: 'game' }).map(x => x.id), ['demo-game']);
});
check('unmatched search returns an empty array', () => {
  assert.deepEqual(M.filterProjects(demo, { query: '存在しない言葉', status: 'all', category: 'all' }), []);
});
check('progress handles no tasks without NaN', () => {
  assert.deepEqual(M.progress({ tasks: [] }), { done: 0, total: 0, percent: 0 });
});
check('progress reflects complete and incomplete tasks', () => {
  assert.deepEqual(M.progress(demo[0]), { done: 1, total: 4, percent: 25 });
});
check('next tasks choose one unfinished task per project by priority', () => {
  const next = M.nextTasks(demo);
  assert.equal(next[0].project.id, 'demo-ui');
  assert.equal(next[0].task.id, 'ui-2');
  assert.equal(new Set(next.map(x => x.project.id)).size, next.length);
  assert.equal(next.length, 3);
});
check('completed projects are excluded from next actions', () => {
  const copy = M.demoProjects('2026-10-13');
  copy[0].status = 'done';
  assert.equal(M.nextTasks(copy).some(x => x.project.id === 'demo-ui'), false);
});
check('state round-trip preserves edited status, priority and task', () => {
  const copy = M.demoProjects('2026-10-13');
  copy[0].status = 'review'; copy[0].priority = 'low'; copy[0].tasks[1].done = true;
  const reloaded = JSON.parse(JSON.stringify({ version: 1, projects: copy }));
  assert.ok(M.isPersistedState(reloaded));
  assert.equal(reloaded.projects[0].tasks[1].done, true);
  assert.equal(reloaded.projects[0].status, 'review');
});
check('invalid saved version or primitive is rejected', () => {
  assert.equal(M.isPersistedState(null), false);
  assert.equal(M.isPersistedState({ version: 2, projects: demo }), false);
});
check('duplicate project IDs and non-boolean task values are rejected', () => {
  assert.equal(M.isPersistedState({ version: 1, projects: [demo[0], demo[0]] }), false);
  const copy = M.demoProjects('2026-10-13'); copy[0].tasks[0].done = 'true';
  assert.equal(M.isPersistedState({ version: 1, projects: copy }), false);
});
check('duplicate task IDs and oversized saved data are rejected', () => {
  const copy = M.demoProjects('2026-10-13'); copy[0].tasks.push({ ...copy[0].tasks[0] });
  assert.equal(M.isPersistedState({ version: 1, projects: copy }), false);
  assert.equal(M.isPersistedState({ version: 1, projects: Array(101).fill(demo[0]) }), false);
});
console.log(`PASS: ${checks} meaningful model checks; browser interaction checks are recorded separately.`);
