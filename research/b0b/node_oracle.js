// Optional, installed-Node secondary oracle: primitives/arrays, NOT full JCS.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const corpus = JSON.parse(fs.readFileSync(path.join(__dirname, '../../fixtures/b0b/vectors.json'), 'utf8'));
const results = [];
for (const [id, bits, expected] of corpus.binary64) {
  const value = Buffer.from(bits, 'hex').readDoubleBE();
  const actual = JSON.stringify(value);
  // Native stringify emits null for nonfinite values: counterexample, not a JCS pass.
  assert.equal(actual, expected === null ? 'null' : expected);
  results.push({id, observed: actual, kind: expected === null ? 'non-JCS counterexample' : 'number agreement'});
}
const shared = ['P01', 'P04', 'P05', 'P06', 'P07', 'P17', 'P18', 'P19', 'P34', 'P35', 'P36', 'P39', 'P40', 'P46'];
for (const id of shared) {
  const c = corpus.bytes.find(c => c.id === id);
  assert.equal(JSON.stringify(JSON.parse(c.text)), c.canon);
  results.push({id, kind: 'shared primitive/array agreement'});
}
assert.deepEqual(['דּ', '😀'].sort(), ['😀', 'דּ']);
assert.equal(JSON.stringify(JSON.parse('{"2":0,"10":1}')), '{"2":0,"10":1}');
assert.equal(JSON.parse('{"a":1,"\\u0061":2}').a, 2);
console.log(JSON.stringify({node: process.version, executable: process.execPath, results,
  controls: ['UTF-16 sorting', 'numeric-looking keys are not JCS ordered', 'duplicates lost on parse']}, null, 2));
