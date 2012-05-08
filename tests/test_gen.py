
from doublecheck import gen
    
class TestGen(object):
    
    def test_Empty(self):
        assert list(gen.Empty().series(100)) == []

    def test_Just(self):
        gen1 = gen.Just(1)
        assert list(gen1.series(100)) == [1]
        assert gen1.random(100) == 1

    def test_OneOfEach(self):
        gen1 = gen.Just(1)
        genHello = gen.Just('Hello')
        genEach = gen.OneOfEach([gen1, genHello])
        assert list(genEach.series(100)) == [[1, 'Hello']]
        assert genEach.random(100) == [1, 'Hello']

    def test_Ints(self):
        ints = gen.Ints()
        assert ints.random(500) < 500
        assert -20 in ints.series(100)

    def test_Dict(self):
        d = gen.Dict({ 'foo': gen.Just('foozle'),
                       'baz': gen.Ints() })

        assert d.random(100)['baz'] <= 100
        assert d.random(100)['foo'] == 'foozle'
        
    def test_ResultOf(self):
        pass

    def test_ListOfN(self):
        assert len(gen.ListOfN(45, gen.Just('bizzle')).random(100)) == 45
        for sample in gen.ListOfN(45, gen.Just('foo')).series(100):
            assert len(sample) == 45
                       
