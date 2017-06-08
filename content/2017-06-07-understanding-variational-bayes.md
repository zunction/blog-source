Title: Understanding Variational Bayes
Date: 2017-06-07 19:26
Tags:
Slug: understanding-variational-bayes
Author: zhangsheng

For the past few days, I have been reading a paper written by my advisor, where the term *variational* was used frequently. As the term variational was foreign to me, there were gaps in my understanding of the paper. I went looking for tutorials or introduction to Variational Bayes and got a good read from [this](http://www.orchid.ac.uk/eprints/40/1/fox_vbtut.pdf). In my discussion of variational bayes below, it will be in done in the discrete form compared to the continuous version given in the tutorial as it is closer to what I'm working on.

## Introduction

Variational Bayes is a [variational method](https://en.wikipedia.org/wiki/Variational_method_(quantum_mechanics)) which in quantum mechanics, is a way of finding approximations to the lowest energy eigenstate or ground state and some excited states (which I do not understand fully for now). A probabilistic model defines a joint distribution over a set $S$ of random variables. We can then partition this set into disjoint sets $V$ and $H$ which corresponds to visible (observed) and hidden (latent) variables. Usually the model is governed by a set of adaptive parameters $W$ and we can condition on $W$, describe the joint distribution $P(H,V|W)$. The distribution of the observed variables is obtained by marginalization over the hidden variables

$$\mathcal{L}(W) = P(V|W) = \sum_{H} P(H,V|W)$$

The $\mathcal{L}(W)$ is the likelihood function which we usually maximize it to get a maximum likelihood estimator for $W$. We are also interested in the posterior distribution $\mathbb{P}(H|V)$ of the hidden variables given the visible variables. Using Bayes' theorem,

$$P(H|V,W) = \frac{P(H,V|W)}{P(V|W)} $$

where the denominator of the expression is the likelihood function. As we have seen in an [earlier post](https://zunction.github.io/2016/12/a-prelude-to-mpf/), we run into tractability issues when we have exponentially large number of terms. Here is where variational methods come into play by introducing an approximating distribution $Q(H|V)$ to approximate the true posterior distribution. We also assume that the form of $Q(H|V)$ factorizes over the component variables $\{h_i\}$ in $H$, so we have

$$Q(H|V) = \prod_{i}Q_i(h_i|V)$$

this assumption is also known as the mean field assumption. It is also important to stress that $Q$ approximates the joint distribution $P$ and $Q_i(h_i)$ are poor approximations to the marginals $P_i(h_i)$. This is also why variational bayes are harder to debug than algorithms whose node states have some local interpretation.

Doing the following transformation to the log likelihood function,

$$ \ln P(V|W) = \ln \sum_{H}P(H,V|W)$$
$$= \ln \sum_{H}Q(H|V)\frac{P(H,V|W)}{Q(H|V)}$$
$$ \geq L(Q,W) = \sum_{H}Q(H|V)\ln \frac{P(H,V|W)}{Q(H|V)}$$
where the last inequality is obtained by using Jensen's inequality. The function $L(Q,W)$ forms a lower bound on the true log likelihood since

$$ \ln P(V|W) = L(Q,W) - \sum_{H}Q(H|V) \ln \frac{P(H|V,W)}{Q(H|V)} = L(Q,W) + KL(Q||P)$$

and the nonnegative property of the Kullback Leibler divergence. In the variational approach, we want to find a suitable $Q(H|V)$ which is simply enough for the lower bound $L(Q,W)$ to be evaluated but with a reasonably tight bound. Since the true log likelihood is independent of $Q$ finding such a $Q$ is equivalent to minimizing the Kullback Leibler divergence.

## Solution of Free Energy Optimization

Our goal now is to find $Q$ to maximize the lower bound (which was stated earlier as minimizing the Kullback Leibler divergence), with $Q$ subjected to normalization constrains.

$$L(Q,W) =  \ln P(V|W) + \sum_{H}Q(H|V) \ln \frac{P(H|V,W)}{Q(H|V)}$$

$$ =  \ln P(V|W) + \sum_{H}Q(H|V) \bigg\{\ln \frac{P(H,V|W)}{Q(H|V)} - \ln P(V|W)\bigg\}$$

$$ =  \ln P(V|W) + \sum_{H}Q(H|V) \ln \frac{P(H,V|W)}{Q(H|V)} - \sum_{H}Q(H|V) \ln P(V|W)$$

$$ = \sum_{H}Q(H|V) \ln \frac{P(H,V|W)}{Q(H|V)}$$

$$ = \sum_{H}Q(H|V) \ln P(H,V|W) -\sum_{H}Q(H|V) \ln Q(H|V)$$

$$ = \left\langle E(H,V)\right\rangle_{Q(H|V)} + H\left[Q(H|V)\right]$$

where we define entropy as $H\left[Q(H|V)\right] = -\sum_{H}Q(H|V) \ln Q(H|V)$ and energy as $E(\cdot) = \ln P(\cdot)$, the notation, $\left\langle\cdot\right\rangle_{Q(H|V)}$ is defined as the expectation over $Q(H|V)$. By the mean field assumption,

$$L(Q,W) = \sum_{H}\left(\prod_{k}Q_k(h_k|V)\right) \ln P(H,V|W) -\sum_{H}\left(\prod_{k}Q_k(h_k|V)\right) \sum_{i}\ln Q_i(h_i|V)$$

Working on the term on the right,

$$\sum_{i}\sum_{H}\left(\prod_{k}Q_k(h_k|V)\right) \ln Q_i(h_i|V)$$

and consider the partitions $H = \{h_i, \bar{h}_i\}$ where $\bar{h}_i = H\backslash h_i$. Pulling out the $h_i$ term,

$$\sum_{i}\sum_{h_i}\sum_{\bar{h}_i}Q_i(\bar{h}_i|V)Q_i(h_i|V) \ln Q_i(h_i|V)$$

$$ = \sum_{i}\left\langle\sum_{h_i}Q_i(h_i|V) \ln Q_i(h_i|V)\right\rangle_{Q_i(\bar{h}_i|V)}$$

$$ = \sum_{i}\sum_{h_i}Q_i(h_i|V) \ln Q_i(h_i|V)$$

Now we look at the energy,

$$\sum_{H}Q(H|V) E(H,V|W)$$

$$= \sum_{h_i}Q_i(h_i|V)\left\langle  E(H,V|W)\right\rangle_{Q(\bar{h}_i|V}$$

$$= \sum_{h_i}Q_i(h_i|V)\ln \exp\left\langle  E(H,V|W)\right\rangle_{Q(\bar{h}_i|V)}$$

defining $Q^\ast(h_i|V) = \frac{1}{Z}\exp\left\langle  E(H,V|W)\right\rangle_{Q(\bar{h}_i|V)}$  with $Z$ normalizing $Q_i^\ast(h_i|V)$

$$\sum_{H}Q(H|V) E(H,V|W) = \sum_{h_i}Q_i(h_i|V)\ln Q^\ast(h_i|V) + \ln Z$$

With the new forms of the energy and entropy, we have

$$L(Q,W) = \sum_{h_i}Q_i(h_i|V)\ln Q^\ast(h_i|V) - \sum_{i}\sum_{h_i}Q_i(h_i|V) \ln Q_i(h_i|V) + \ln Z$$

$$= \sum_{h_i}Q_i(h_i|V)\ln Q^\ast(h_i|V) - \sum_{h_i}Q_i(h_i|V) \ln Q_i(h_i|V) - \sum_{\bar{h}_i}Q_i(\bar{h}_i|V) \ln Q_i(\bar{h}_i|V) + \ln Z$$

$$= \bigg\{\sum_{h_i}Q_i(h_i|V)\ln Q^\ast(h_i|V) - \sum_{h_i}Q_i(h_i|V) \ln Q_i(h_i|V)\bigg\} + H\left[Q(\bar{h}_i|V)\right] + \ln Z$$

$$= \sum_{h_i}Q_i(h_i|V)\ln \frac{Q^\ast(h_i|V)}{Q_i(h_i|V)} + H\left[Q(\bar{h}_i|V)\right] + \ln Z$$

$$= -KL(Q_i(h_i|V)||Q_i^\ast(h_i)) + H\left[Q(\bar{h}_i|V)\right] + \ln Z$$

We obtain this neat result that says that trying to maximize $L(Q,W)$ or equivalently minimize $KL(Q||P) = -\sum_{H}Q(H|V) \frac{P(H|V,W)}{Q(H|V)}$, which is a large joint distribution, can be simplified to minimizing the KL divergence between individual 1-dimensional distributions. The Kullback Leibler divergence arrangment allows us to see that the KL divergence is minimized when

$$Q(h_i|V) = Q^\ast(h_i)$$

Expanding the definition of $Q^\ast(h_i)$,

$$Q(h_i|V) = \frac{1}{Z} \exp \left\langle E(h_i,\bar{h}_i, V|W)\right\rangle_{Q(\bar{h}_i|V)}$$

$$= \frac{1}{Z} \exp \left\langle \ln P(h_i,\bar{h}_i, V|W)\right\rangle_{Q(\bar{h}_i|V)}$$

## Solution as an iterative update equation

This is the portion that stumbles me. In this section, it converts the equation that we solved for above as an iterative update equation, which means that for the many components to update, it does not update synchronously, but instead updates them one by one, i.e. iteratively.

$$Q_i(h_i|V) \gets \frac{1}{Z} \exp \left\langle \ln P(h_i,\bar{h}_i, V|W)\right\rangle_{Q(\bar{h}_i|V)}$$

>where $h_i$ is a hidden node to be updated; V are the observed data, and $\bar{h}_i = H\backslash h_i$
are the other hidden nodes
These updates give us an EM-like algorithm, optimising
one node at a time in the hope of converging to a local minimum.

This sentence gave rise to a few questions in my head, what is the objective we are trying to minimize here? The best answer that I could come up with is the KL divergence that measures the 'closeness' between the true posterior $P(H|V,W)$ and the approximated posterior $Q(H|V)$. But then when we talk about updating the hidden nodes, which for my case my visible and hidden variables are binaries, what is the reason for doing such updates? It feels like these updates just flip the bits trying to find the best configuration of the hidden variables such that the KL divergence is minimized. In that case we have $2^{|H|}$ configurations to try out in so as to find the minimum, but then again, the sentence says we hope for it to converge to a local minimum.

I feel that I am still missing something important in this tutorial which has lead to my questions above which is most likely caused by my misunderstanding of the ideas or me missing out some important point from the tutorial. Please feel free to point out what I'm missing out if you know by starting some discussions below. It will be nice to have someone to discuss this with. 
