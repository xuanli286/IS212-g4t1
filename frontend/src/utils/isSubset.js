// checks if an array is a subset of another array
export const isSubset = (subset, superset) => {
  return subset.every(item => superset.includes(item));
}