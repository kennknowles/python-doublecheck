DoubleCheck
===========

A library for property-based testing in two different ways:

1. "QuickCheck" - randomly generated inputs
2. "SmallCheck" - exhaustively enumerated inputs

These testing approaches are named for the pioneering Haskell libraries.  The two
approaches truly shine when used together - once a property is found to be
refutable by some probably-huge-and-crazy random input, it is often worth investing 
the CPU time to find the _smallest_ counterexample.

This library is a brand new work-in-progress (see commit log for dates) with known
issues:

 - Does not have randomly generated strings just yet
 - No existential quantification yet, but smallcheck does allow it!
 - I've reversed the argument order from traditional ordering to use pythons *args and **kwargs... unsure if this is cool
 - Needs more thorough testing
 - Needs to be able to test that a property always throws an exception
 - Needs lots more combinators


Installation & Usage
--------------------

(TODO: Describe in more detail. For now, read doublecheck/gen.py and doublecheck/prop.py)

    $ pip install doublecheck
    $ python
    >>> from doublecheck import * 
    >>> ForAll(lambda i: i > 0, PosInts()).quickcheck(100000)

    >>> ForAll(Strings, lambda s: s != "bb").smallcheck(20)


Further Reading & Related Projects
----------------------------------

The original libraries.

 - [QuickCheck]() ([mirrored on github](https://github.com/darcs-mirrors/QuickCheck) if you'd like to fork it)
 - [SmallCheck and Lazy SmallCheck](http://www.cs.york.ac.uk/fp/smallcheck/) ([also on github](https://github.com/feuerbach/smallcheck))

There are also already a few python libraries inspired by QuickCheck. None seem to take
the approach of a full port, and certainly none include SmallCheck-style exhaustive testing.

 - [PayCheck](https://github.com/markchadwick/paycheck) 
 - [qc.py](https://github.com/dbravender/qc)

Essentially every language has multiple implementations.
Here are some that I think are worth checking out.

 - [ScalaCheck](https://github.com/rickynils/scalacheck) (Scala)
 - [jsqc](https://github.com/sakari/jsqc) (JavaScript) 
 - [QueenCheck](https://github.com/rosylilly/QueenCheck) (Ruby)
 - [Rantly](https://github.com/hayeah/rantly) (Ruby)
 - [Triq](https://github.com/krestenkrab/triq) (Erlang)


Copyright & License
-------------------
Copyright 2012- Kenneth Knowles

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
