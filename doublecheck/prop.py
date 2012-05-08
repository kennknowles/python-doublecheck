import itertools

from doublecheck import gen

class TestCase(object):
    '''
    A result is the Certain/Falsified/Undecided status of a property
    along with any debugging info.
    '''
    Falsified = "Falsified"
    Certain = "Certain"
    Undecided = "Undecided"

    def __init__(self, status, arguments = []):
        self.status = status
        self.arguments = arguments

class Prop(object):
    '''
    A Prop is more-or-less a Gen for TestCase objects... but for e.g. LazySmallCheck it gets special treatment
    '''

    def check(self, test_gen_strategy):
        '''
        Checks this property using test_gen_strategy, which
        should be a function from prop -> finite stream of test cases;
        quickcheck and smallcheck and just different strategies
        '''
        successes = 0
        total = 0
        min_successes = 1
        for test_case in test_gen_strategy(self):
            total = total + 1
            if test_case.status == TestCase.Falsified:
                return test_case
            elif test_case.status == TestCase.Certain:
                successes = successes + 1

        if successes >= min_successes:
            return TestCase(status = TestCase.Certain) # TODO: configure min_successes; more than 1!
        else:
            return TestCase(status = TestCase.Undecided)

    def quickcheck(self, size, numtests = None):
        '''
        Randomly searches for a counterexample, returning it
        in the form of a TestCase with status = Falsified
        '''
        numtests = numtests or 100
        def strat(prop):
            for __ in xrange(0, numtests):
                yield self.random(size)

        return self.check(strat)

    def smallcheck(self, size):
        '''
        Exhaustively searches for a counterexample up to depth provided
        retuning it in the form of a TestCase with status = Falsified
        '''
        def strat(prop):
            return prop.series(size)

        return self.check(strat)

    def doublecheck(self, size, numtests = None):
        '''
        Runs quickcheck until a counterexample is found, then
        runs smallcheck. Optimistically does not run smallcheck
        otherwise
        '''
        numtests = numtests or 100
        qc_result = self.quickcheck(size, numtests = 100)
        if qc_result.status == TestCase.Certain:
            return qc_result
        
        else:
            sc_result = self.smallcheck(size)
            if sc_result.status == TestCase.Falsified:
                return sc_result
            else:
                return qc_result

            
    def implies(self, other_prop):
        return Implies(self, other_prop)

class Certain(Prop):
    def random(self, size):
        return TestCase(status = TestCase.Certain)
    
    def series(self, size):
        return [TestCase(status = TestCase.Certain)]

class Falsified(Prop):
    def random(self, size):
        return TestCase(status = TestCase.Falsified)

    def series(self, size):
        return [TestCase(status = TestCase.Falsified)]

class Undecided(Prop):
    def random(self, size):
        return TestCase(status = TestCase.Undecided)

    def smallcheck(self, size):
        return TestCase(status = TestCase.Undecided)

def ToProp(bool_or_prop):
    if isinstance(bool_or_prop, bool):
        if bool_or_prop:
            return Certain()
        else:
            return Falsified()
    else:
        return bool_or_prop
    
class Implies(Prop):
    def __init__(self, condition, prop):
        self.condition = ToProp(condition)
        self.prop = ToProp(prop)

    def random(self, size):
        condition_result = self.condition.random(size)

        if condition_result.status != TestCase.Certain:
            return TestCase(status = TestCase.Undecided)
        else:
            return self.prop.random(size)

    def series(self, size):
        for condition_result in self.condition.series(size):
            if condition_result.status != TestCase.Certain:
                yield TestCase(status = TestCase.Undecided)
            else:
                for prop_result in self.prop.series(size):
                    yield prop_result
            

class ForAll(Prop):

    def __init__(self, predicate, *arg_gens, **kwarg_gens):
        self.args_gen = gen.OneOfEach(arg_gens)
        self.kwargs_gen = gen.Dict(kwarg_gens)
        self.predicate = predicate
        
    def series(self, size):
        for args in self.args_gen.series(size-1):
            for kwargs in self.kwargs_gen.series(size-1):
                for testcase in ToProp(self.predicate(*args, **kwargs)).series(size-1):
                    yield testcase

    def random(self, size):
        args = self.args_gen.random(size-1)
        kwargs = self.kwargs_gen.random(size-1)
        return ToProp(self.predicate(*args, **kwargs)).random(size-1)

