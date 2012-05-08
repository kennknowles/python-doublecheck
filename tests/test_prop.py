
from doublecheck import gen, prop
    
class TestProp(object):
    
    def test_Falsified(self):
        assert prop.Falsified().quickcheck(100).status == prop.TestCase.Falsified
        assert prop.Falsified().smallcheck(100).status == prop.TestCase.Falsified

    def test_Certain(self):
        assert prop.Certain().quickcheck(100).status == prop.TestCase.Certain
        assert prop.Certain().smallcheck(100).status == prop.TestCase.Certain

    def test_Undecided(self):
        assert prop.Undecided().quickcheck(100).status == prop.TestCase.Undecided
        assert prop.Undecided().smallcheck(100).status == prop.TestCase.Undecided

    def test_Implies(self):
        assert prop.Implies(True, True).quickcheck(100).status == prop.TestCase.Certain
        assert prop.Implies(True, False).quickcheck(100).status == prop.TestCase.Falsified
        assert prop.Implies(False, True).quickcheck(100).status == prop.TestCase.Undecided
        assert prop.Implies(False, False).quickcheck(100).status == prop.TestCase.Undecided

        assert prop.Implies(prop.Certain(), prop.Certain()).quickcheck(100).status == prop.TestCase.Certain
        assert prop.Implies(prop.Certain(), prop.Falsified()).quickcheck(100).status == prop.TestCase.Falsified
        assert prop.Implies(prop.Certain(), prop.Undecided()).quickcheck(100).status == prop.TestCase.Undecided

        assert prop.Implies(prop.Falsified(), prop.Certain()).quickcheck(100).status == prop.TestCase.Undecided
        assert prop.Implies(prop.Falsified(), prop.Falsified()).quickcheck(100).status == prop.TestCase.Undecided
        assert prop.Implies(prop.Falsified(), prop.Undecided()).quickcheck(100).status == prop.TestCase.Undecided

        assert prop.Implies(prop.Undecided(), prop.Certain()).quickcheck(100).status == prop.TestCase.Undecided
        assert prop.Implies(prop.Undecided(), prop.Falsified()).quickcheck(100).status == prop.TestCase.Undecided
        assert prop.Implies(prop.Undecided(), prop.Undecided()).quickcheck(100).status == prop.TestCase.Undecided

    def test_ForAll(self):
        assert prop.ForAll(lambda i: prop.Certain(), gen.Ints()).quickcheck(100).status == prop.TestCase.Certain
        assert prop.ForAll(lambda i: i > 0, gen.Ints()).quickcheck(100).status == prop.TestCase.Falsified

        # Probably going to miss this random int
        assert prop.ForAll(lambda i: i != 42, gen.Ints()).quickcheck(100000).status == prop.TestCase.Certain
        assert prop.ForAll(lambda i: i != 42, gen.Ints()).smallcheck(100000).status == prop.TestCase.Falsified

    def test_Exists(self):
        pass

    def test_Iff(self):
        pass

    def test_Throws(self):
        pass
        
