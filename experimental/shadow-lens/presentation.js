/*
 * Three source scenes share one target and lamp position; their three depths
 * are independently chosen integers 2..8, with repeats allowed. See MODEL.md
 * for the unchanged source carrier and point-light relation.
 *
 * build supplies the shared source and depths, then retains every full scene.
 * observe reads A or B without changing those sources. Equality compares the
 * complete ordered polygons in the model's reduced rational coordinates.
 * The observation omits source geometry; the retained family is its reopen
 * route. These three witnesses are not the complete source fiber. B recovers
 * their depths, but neither exposure recovers absolute lamp position.
 *
 * The adjacent finite tests cover all 343 depth triples, including the hostile
 * repeated-depth case where B must not claim three distinct observations.
 * This composition adds no physical model or unbounded mathematical claim.
 */
(function (root, factory) {
  'use strict';
  if (typeof module === 'object' && module.exports) module.exports = factory(require('./model.js'));
  else root.ShadowFamily = factory(root.ShadowLens);
})(typeof globalThis === 'object' ? globalThis : this, function (M) {
  'use strict';

  const families = new WeakSet();
  const zeroShift = Object.freeze({ x: 0, y: 0 });

  function freeze(value) {
    if (value && typeof value === 'object' && !Object.isFrozen(value)) {
      for (const child of Object.values(value)) freeze(child);
      Object.freeze(value);
    }
    return value;
  }

  function admitDepths(depths) {
    if (!Array.isArray(depths) || depths.length !== 3) {
      throw new TypeError('Depths must be an array of exactly three integers');
    }
    const descriptors = Object.getOwnPropertyDescriptors(depths);
    if (Reflect.ownKeys(descriptors).some(key => !['0', '1', '2', 'length'].includes(key))) {
      throw new TypeError('Depths must contain only three own data entries');
    }
    return [0, 1, 2].map(index => {
      const descriptor = descriptors[index];
      if (!descriptor || !descriptor.enumerable || !('value' in descriptor)
        || !Number.isSafeInteger(descriptor.value)) {
        throw new TypeError('Every depth must be an own integer data entry');
      }
      if (descriptor.value < 2 || descriptor.value > 8) {
        throw new RangeError('Depth is outside the admitted range 2..8');
      }
      return descriptor.value;
    });
  }

  function build(shared, depths) {
    // Validate the complete prior source even though each depth is replaced.
    const source = M.scene(shared).state;
    const scenes = admitDepths(depths).map(depth => M.scene(M.update(source, { depth })));
    const family = freeze({ scenes, target: scenes[0].shadow });
    families.add(family);
    return family;
  }

  function observe(family, observer) {
    if (!families.has(family)) throw new TypeError('Family must be returned by ShadowFamily.build');
    if (observer !== 'A' && observer !== 'B') throw new TypeError('Observer must be A or B');
    const secondary = observer === 'B';
    const key = secondary ? 'secondary' : 'shadow';
    const polygons = family.scenes.map(scene => scene[key]);
    const exact = family.scenes.map(scene => scene.exact[key]);
    // All coordinates come from frozen model scenes in canonical reduced form.
    const groups = new Set(exact.map(polygon => JSON.stringify(polygon))).size;
    return freeze({
      polygons, exact, groups, allMatch: groups === 1,
      shifts: family.scenes.map(scene => secondary ? scene.displacement : zeroShift),
      recoveredDepths: secondary
        ? family.scenes.map(scene => M.depthFromDisplacement(scene.exact.displacement).values[0])
        : null
    });
  }

  return Object.freeze({ build, observe });
});
