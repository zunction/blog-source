Title: Understanding Variational Bayes
Date: 2017-06-07 19:26
Tags:
Slug: understanding-variational-bayes
Author: zhangsheng

For the past few days, I have been reading a paper written by my advisor, where the term *variational* was used frequently. As the term variational was foreign to me, there were gaps in my understanding of the paper. I went looking for tutorials or introduction to Variational Bayes and got a good read from [this](http://www.orchid.ac.uk/eprints/40/1/fox_vbtut.pdf).

## Introduction

Variational Bayes is a [variational method](https://en.wikipedia.org/wiki/Variational_method_(quantum_mechanics)) which in quantum mechanics, is a way of finding approximations to the lowest energy eigenstate or ground state and some excited states (which I do not understand fully for now). A probabilistic model defines a joint distribution over a set $S$ of random variables. We can then partition this set into disjoint sets $V$ and $H$ which corresponds to visible (observed) and hidden (latent) variables. Usually the model is governed by a set of adaptive parameters $W$ and we can condition on $W$, describe the the joint distribution $P(H,V|W)$. The distribution of the observed variables is obtained by marginalization over the hidden variables

$$\mathcal{L}(W) = P(V|W) = \sum_{H} P(H,V|W)$$

The $\mathcal{L}(W)$ is the likelihood function which we usually maximize it to get a maximum likelihood estimator for $W$. We are also interested in the posterior distribution $\mathbb{P}(H|V)$ of the hidden variables given the visible variables. Using Bayes' theorem,

$$P(H|V,W) = \frac{P(H,V|W)}{P(V|W)} $$

where the denominator of the expression is the likelihood function. As we have seen in an [earlier post](https://zunction.github.io/2016/12/a-prelude-to-mpf/), we run into tractability issues when we have exponentially large number of terms. Here is where variational methods come into play by introducing an approximating distribution $Q(H|V)$ to approximate the true posterior distribution. Doing the following transformation to the log likelihood function,

$$ \ln P(V|W) = \ln \sum_{H}P(H,V|W)$$
$$= \ln \sum_{H}Q(H|V)\frac{P(H,V|W)}{Q(H|V)}$$
$$ \geq L(Q,W) = \sum_{H}Q(H|V)\ln \frac{P(H,V|W)}{Q(H|V)}$$
where the last inequality is obtained by using Jensen's inequality. The function $L(Q,W)$ forms a lower bound on the true log likelihood since

$$ \ln P(V|W) = L(Q,W) - \sum_{H}Q(H|V) \ln \frac{P(H|V,W)}{Q(H|V)} = L(Q,W) + KL(Q||P)$$

and the nonnegative property of the Kullback Leibler divergence. In the variational approach, we want to find a suitable $Q(H|V)$ which is simply enough for the lower bound $L(Q,W)$ to be evaluated but with a reasonably tight bound. Since the true log likelihood is independent of $Q$ finding such a $Q$ is equivalent to minimizing the Kullback Leibler divergence. We also assume that the form of $Q(H|V)$ factorizes over the component variables $\{h_i\}$ in $H$, so we have

$$Q(H|V) = \prod_{i}Q_i(h_i|V)$$

this assumption is also known as the mean field assumption.

## Solution of Free Energy Optimization

Our goal now is to find $Q$ to maximize the lower bound (which was stated earlier as minimizing the Kullback Leibler divergence), with $Q$ subjected to normalization constrains.

$$L(Q,W) =  \ln P(V|W) + \sum_{H}Q(H|V) \ln \frac{P(H|V,W)}{Q(H|V)}$$

$$ =  \ln P(V|W) + \sum_{H}Q(H|V) \bigg\{\ln \frac{P(H,V|W)}{Q(H|V)} - \ln P(V|W)\bigg\}$$

$$ =  \ln P(V|W) + \sum_{H}Q(H|V) \ln \frac{P(H,V|W)}{Q(H|V)} - \sum_{H}Q(H|V) \ln P(V|W)$$

$$ = \sum_{H}Q(H|V) \ln \frac{P(H,V|W)}{Q(H|V)}$$

$$ = \sum_{H}Q(H|V) \ln P(H,V|W) -\sum_{H}Q(H|V) \ln Q(H|V)$$


where we define energy as $E(\cdot) = \ln P(\cdot)$ and entropy as $H\left[Q(H|V)\right] = -\sum_{H}Q(H|V) \ln Q(H|V)$. By the mean field assumption,

$$L(Q,W) = \sum_{H}\prod_{i}Q_i(h_i|V) \ln P(H,V|W) -\sum_{H}\prod_{i}Q_i(h_i|V) \sum_{i}\ln Q_i(h_i|V)$$
