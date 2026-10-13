'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { matches, normalize } = require('../app.js');
const entries = JSON.parse(fs.readFileSync(path.join(__dirname, '../data/catalog.json'), 'utf8')).entries;
function find(query = '', category = 'all', origin = 'all') {
  return entries.filter(entry => matches(entry, query, category, origin)).map(entry => entry.id);
}
assert.equal(find().length, 7);
assert.equal(normalize(' ＲＥＡＣＴ　'), 'react');
assert.deepEqual(find('ｒｅａｃｔ'), ['motion-dev-animations', 'motion']);
assert.deepEqual(find('Motion  React'), ['motion-dev-animations', 'motion']);
assert.deepEqual(find('フォーム'), ['web-design-guidelines']);
assert.deepEqual(find('', 'review'), ['impeccable', 'web-design-guidelines']);
assert.deepEqual(find('', 'all', 'source-post'), ['motion-dev-animations', 'motion']);
assert.equal(find('', 'all', 'supplement').length, 5);
assert.deepEqual(find('', 'interaction', 'source-post'), ['motion-dev-animations']);
assert.deepEqual(find('', 'review', 'source-post'), []);
assert.deepEqual(find('存在しないキーワード'), []);
assert.deepEqual(find('   '), find());
assert.deepEqual(find('<script>'), []);
console.log('PASS: 13 search checks (Japanese, NFKC, multi-term, category, origin, combined filters, empty results)');
