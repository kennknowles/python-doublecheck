import random
    
class Gen(object):
    '''
    A set of values, which may either be randomly drawn from or
    traversed serially. For uncountable sets (or those which are pain
    to exhaustively enumerate) the function series should return None
    '''

    def series(self, size):
        '''
        An iterator over all elements of the set smaller than `size`
        '''
        raise NotImplementedError()

    def coseries(self, range_series):
        '''
        When range_series is a function (int -> [B]) a la series, this
        returns a function int -> (A -> B) where A is the set represented by self
        '''
        raise NotImplementedError()

    def random(self, size):
        '''
        Draw one random sample. TODO: take other configuration values
        '''
        raise NotImplementedError()

    def map(self, fn):
        '''
        Maps a function over a set
        '''
        return Map(fn, self)

    def flat_map(self, fn):
        '''
        FlatMaps a function over a set (i.e. monadic bind)
        '''
        return FlatMap(fn, self)


class Map(Gen):
    '''
    The set of inputs fn(x) where x is drawn from gen
    '''
    def __init__(self, fn, gen):
        self.gen = gen
        self.fn = fn
    
    def series(self, size):
        for elem in self.gen.series(size):
            yield self.fn(elem)

    def random(self, size):
        return self.fn(self.gen.random(size))

class FlatMap(Gen):
    '''
    The set of inputs drawn from any Gen return by fn(x) for any x drawn from gen
    '''
    def __init__(self, fn, gen):
        self.gen = gen
        self.fn = fn

    def series(self, size):
        for elem in self.gen.series(size):
            subgen = self.fn(elem)
            for subelem in subgen.series(size):
                yield subelem

                
class Empty(Gen):
    '''
    The empty set
    '''
    def __init__(self):
        pass

    def series(self, size):
        return []


class Just(Gen):
    '''
    The set of input that is just its argument
    '''

    def __init__(self, val):
        self.val = val

    def series(self, size):
        return [self.val]

    def random(self, size):
        return self.val

class Ints(Gen):
    '''
    All integers from -sys.maxint to sys.maxint
    '''
    
    def random(self, size):
        return random.randint(-size, size)
    
    def series(self, size):
        yield 0
        for i in xrange(1, size):
            yield i
            yield -i

class PosInts(Gen):
    '''
    All positive integers 
    '''
    
    def random(self, size):
        return random.randint(1, size)
    
    def series(self, size):
        for i in xrange(1, size):
            yield i

class OneOf(Gen):
    '''
    The set of inputs drawn from a provided list
    '''
    def __init__(self, values):
        self.values = values

    def random(self, size):
        return random.choice(self.values)

    def series(self, size):
        return self.values

class OneOfEach(Gen):
    '''
    OneOfEach(gens) is the set of lists l where l[i] is drawn from gens[i]
    '''

    def __init__(self, subgens):
        self.subgens = subgens

    def random(self, size):
        return [gen.random(size) for gen in self.subgens]
        
    def series(self, size):
        if len(self.subgens) < 1:
            yield []
        else:
            for head in self.subgens[0].series(size):
                for tail in OneOfEach(self.subgens[1:]).series(size):
                    yield [head] + tail
        
class Dict(Gen):
    '''
    Dict(gendict) is the set of dictionaries where d[key] is drawn from gendict[key]
    '''

    def __init__(self, gendict):
        self.one_of_each = OneOfEach([OneOfEach([Just(key), gen]) for key, gen in gendict.items()]) 

    def random(self, size):
        return dict(self.one_of_each.random(size))

    def series(self, size):
        for list_repr in self.one_of_each.series(size):
            yield dict(list_repr)


class ResultOf(Gen):
    '''
    The set of inputs f(*args, **kwargs) where args is drawn from OneOfEach(*arg_gens) and kwargs is drawn from Dict(**kwarg_gens)
    '''
    def __init__(self, fn, *arg_gens, **kwarg_gens):
        self.fn = fn
        self.args_gen = OneOfEach(arg_gens)
        self.kwargs_gen = Dict(kwarg_gens)

    def series(self, size):
        for args in self.args_gen.series(size-1):
            for kwargs in self.kwargs_gen.series(size-1):
                yield fn(*args, **kwargs)

    def random(self, size):
        args = self.args_gen.random(size-1)
        kwargs = self.kwargs_gen.random(size-1)
        return self.fn(*args, **kwargs)

    
class ListOfN(Gen):
    '''
    ListOfN(n, gen) is the set of lists of length n where each element is drawn from gen
    '''

    def __init__(self, n, gen):
        self.n = n
        self.gen = gen

    def random(self, size):
        return [self.gen.random(size-1) for __ in xrange(0, self.n)]

    def series(self, size):
        if self.n < 1:
           yield []
        else:
            for head in self.gen.series(size-1):
                for tail in ListOfN(self.n-1, self.gen).series(size-1):
                    yield [head] + tail

