Title: Equality in Type Theory
Date: 2016-08-08 23:33
Tags:
Slug: equality-in-type-theory
Author: zhangsheng


Recently I have engulfed myself in reading the [HoTT book](https://github.com/HoTT/book/wiki/Nightly-Builds). For readers who do not know what is HoTT, you are not alone for I would not have known if I had not further my studies. HoTT stands for *Homotopy Type Theory*, an interpretation of Martin-Löf’s intensional type theory into abstract homotopy theory. Reading this book has not been a walk in the park; many a times I had to re-read the same paragraph over and over again only to get a rough flavour of it. But it had definitely lead me to see things that I used to be oblivious of.

We shall talk about equality today, not the equality that you and I both know. But the different equalities in Type Theory and yes, there are more than one equality; **judgmental equality** and **propositional equality**. Judgmental equality is also known as **definitional equality** which I think is a better name, but I will stick to the former.

But before I dive into the equality issue, we need a brief introduction of what is a type.



#### Judgmental equality
From the HoTT book, it says that it is helpful to think of this meaning "equality by definition" which is really exactly what it says.

#### Propositional equality
The naming of this equality comes from the treatment of this equality as a proposition, i.e. it can be true or false. The essence of Type Theory's *propositions as types* is also exhibited here as we treat equality as a type.
