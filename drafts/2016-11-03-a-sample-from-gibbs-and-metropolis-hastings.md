Title: A sample from Gibbs and Metropolis-Hastings
Date: 2016-11-03 11:20
Tags:
Slug: a-sample-from-gibbs-and-metropolis-hastings
Author: zhangsheng

In order to synthesis samples for the implementation of the
minimum probability flow learning technique, we need to use
Monte Carlo methods like *Gibbs sampling* or *Metropolis-Hastings
sampling*. Being new to both sampling methods, I went to
find materials and explanations on these two methods. The discussions
below is the result obtained from my learnings.

## Bayesian Inference
We start off with a basic of understanding of Bayesian inference. Given
a prior $f(\theta)$ and data $\mathbf{x}=(x_1,\ldots,x_n)$, the posterior density
is
$$f(\theta \mid \mathbf{x})$$
