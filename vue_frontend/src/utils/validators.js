const positiveNumber = function (value) {
    const v = Number(value);
    return value === '' || (!isNaN(v) && v >= 0)
}

export { positiveNumber };