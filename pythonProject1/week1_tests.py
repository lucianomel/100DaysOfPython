import pytest

from week1_functions import *

@pytest.mark.isomorphicStrings205
def isomorphic_test():
    assert Solution.isIsomorphic("add","egg")

@pytest.mark.isomorphicStrings205
def no_isomorphic_letters_test():
    assert Solution.isIsomorphic("addsa","eggtt")

@pytest.mark.isomorphicStrings205
def no_isomorphic_length_test():
    assert not Solution.isIsomorphic("addsa","eggtfg")
