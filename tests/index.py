# ------- #
# Imports #
# ------- #

from simple_chalk import green, red
from all_purpose_set.fns import isLaden, joinWith, map_, passThrough
from all_purpose_set import ApSet
import os


# ---- #
# Init #
# ---- #

x = red("✘")
o = green("✔")


# ---- #
# Main #
# ---- #


def runTests():
    errors = []

    # validate input
    try:
        code = "ApSet(1)"
        ApSet(1)
    except Exception as e:
        expected = "aList is not an instance of list"
        if expected not in str(e):
            errors.append(code)

    # ensure an empty set works and test `len`
    code = "ApSet()"
    result = ApSet()
    if len(result) != 0:
        errors.append(code)

    # remove -> key error
    code = "result.remove('doesnt exist')"
    try:
        result.remove("doesnt exist")
        errors.append(code)
    except KeyError:
        pass
    except:
        errors.append(code)

    # _hashableElements is populated
    code = "ApSet(['a'])"
    result = ApSet(["a"])
    passed = (
        len(result._hashableElements) == 1 and "a" in result._hashableElements
    )
    if not passed:
        errors.append(code)

    # _nonHashableElements is populated
    el = {}
    code = "ApSet([<ref to {}>])"
    result = ApSet([el])
    passed = (
        len(result._nonHashableElements) == 1
        and result._nonHashableElements[id(el)] is el
    )
    if not passed:
        errors.append(code)

    # add hashable element
    code = "result.add('a')"
    result = ApSet()
    result.add("a")
    passed = (
        len(result._hashableElements) == 1 and "a" in result._hashableElements
    )
    if not passed:
        errors.append(code)

    # add non-hashable element
    el = {}
    code = "result.add(<ref to {}>)"
    result = ApSet()
    result.add(el)
    passed = (
        len(result._nonHashableElements) == 1
        and result._nonHashableElements[id(el)] is el
    )
    if not passed:
        errors.append(code)

    # remove a hashable element
    code = "result.remove('a')"
    result = ApSet(["a"])
    result.remove("a")
    passed = len(result._hashableElements) == 0
    if not passed:
        print(result._hashableElements)
        errors.append(code)

    # remove a non-hashable element
    el = {}
    code = "result.remove(<ref to {}>)"
    result = ApSet([el])
    result.remove(el)
    passed = len(result._nonHashableElements) == 0
    if not passed:
        errors.append(code)

    # has a hashable element (and 'in')
    code = "result.has('a')"
    result = ApSet(["a"])
    passed = result.has("a") and "a" in result
    if not passed:
        errors.append(code)

    # has a non-hashable element (and 'in')
    el = {}
    code = "result.has(<ref to {}>)"
    result = ApSet([el])
    passed = result.has(el) and el in result
    if not passed:
        errors.append(code)

    # clear all elements
    el = {}
    code = "result.clear()"
    result = ApSet(["a", el])
    result.clear()
    passed = len(result) == 0
    if not passed:
        errors.append(code)

    # iterable
    el = {}
    code = "for el in result"
    result = ApSet(["a", el, 1])
    passed = list(result) == ["a", el, 1]
    if not passed:
        errors.append(code)

    if isLaden(errors):
        errorOutput = passThrough(
            errors, [map_(prepend(f"{x} ")), joinWith(os.linesep)]
        )
        print(errorOutput)
    else:
        print(f"{o} all tests")


# ------- #
# Helpers #
# ------- #


def prepend(leftStr):
    def prepend_inner(rightStr):
        return leftStr + rightStr

    return prepend_inner
