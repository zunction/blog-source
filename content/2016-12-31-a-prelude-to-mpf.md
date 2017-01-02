Title: A Prelude to MPF
Date: 2016-12-31 21:01
Tags:
Slug: a-prelude-to-mpf
Author: zhangsheng

On the last day of 2016, let's do some sharing. Recently I implemented a learning technique called [Minimum Probability Flow (MPF)](https://arxiv.org/pdf/0906.4779.pdf) where I generated samples using Gibbs sampling using a given parameter matrix $W$ and then re-learnt this matrix using MPF. Initially I was very lost in this learning technique as it is different from what we normally use in deep learning where we learn the weight matrix (which is also denoted by $W$) such that our cost function is minimized. After much exploration and learning through discussions with my lab mates and advisor, I managed to get a better understanding of this beautiful learning technique that I would like to dissect and discuss about here.

With larger and more complex data, it becomes harder to fit probabilistic models to data due to the intractability of the partition function. Here, what we like to do with the data is to perform parameter estimation, which is the finding of model parameters from observations. An observation is of the form $\mathbf{x} = (x_1, x_2, \ldots, x_d)$ where each $x_i$ can be continuous or discrete. A dataset, represented by $\mathcal{D}$ consists of $N$ such feature vectors. To perform parameter estimation is to fit a particular probabilistic model $p(\mathbf{x}\mid \theta)$, chosen from a family of models parametrized by $\theta$, such that the model best summarizes the statistics of the observed dataset $\mathcal{D}$. The resulting learnt estimator is denoted by $\hat{\theta}$. For a probabilistic model $p(\mathbf{x}\mid \theta)$ we will use the notation:

$$p(\mathbf{x}\mid \theta) = \frac{1}{Z(\theta)}\exp\left[-E(\mathbf{x};\theta)\right]$$

where

$$Z(\theta) = \sum_{\mathbf{x}}\exp\left[-E(\mathbf{x};\theta)\right]$$

is a normalization factor which is also known as the partition function. These types of models are often called 'energy based models' and the function $E(\mathbf{x};\theta)$ is the 'energy'. One might think that energy based models are a specific class of models, however, any model that can be expressed as $p(\mathbf{x}\mid \theta)$ can we written in the form above:

$$p(\mathbf{x}\mid\theta) = \exp\left[\log p(\mathbf{x}\mid \theta)\right] = \frac{ \exp\left[\log p(\mathbf{x}\mid \theta)+\log\right] }{Z(\theta)}$$

and so we can identify the energy as

$$E(\mathbf{x}\mid \theta) = -\log p(\mathbf{x}\mid \theta - \log Z(\theta))$$

## Maximum Likelihood Learning

In practice, the method for fitting a probabilistic model to data is called [maximum likelihood learning (ML)](https://en.wikipedia.org/wiki/Maximum_likelihood_estimation). The approach maximizes the log likelihood of the model parameters given the observed data with respect to the model parameters. For a given list of $N$ observed data samples $\mathcal{D} = \{x_i\}_i$, the log likelihood is defined as

$$\ell(\theta, \mathcal{D}) = \log p(\mathcal{D}\mid \theta)$$

and with the assumption that the observed data $\mathcal{D}$ is independent and identically distributed (iid) and we get

$$p(\mathcal{D}\mid \theta) = \prod_{i=1}^{N}p_X(x_i\mid \theta)$$

and the log likelihood is

$$\ell(\theta,\mathcal{D}) = \sum_{i=1}^{N}\ell(\theta,x_i)$$

with $\ell(\theta,x_i) = p_X(x_i\mid\theta)$. The probability mass function is then writtqen in the form

$$p_X(x\mid \theta) = \frac{1}{Z(\theta)}e^{-E(x;\theta)}$$

Using the above notation, the log likelihood function is represented as

$$\ell(\theta, \mathcal{D}) = -\sum_{i=1}^{N}E(x;\theta)-N\log Z(\theta)$$

and the ML estimator is evaluated by finding the parameters $\theta$ that maximise $\ell(\theta,\mathcal{D})$.

In cases when it is impossible to derive a solution for the estimate $\hat{\theta}_{ML}$ that maximises the likelihod function, gradient ascent is used to find the maximum which comes with a set of problems in this approach. To do gradient ascent, we compute the gradient of the objective function and travel in a small step in the direction given by the gradient. Repeating this enough times with an appropriate step size which is also known as the learning rate, we will eventually arrive at a local maximum of the objective function. Unless the objective function is convex, there is no guarantee of arriving at the global maximum. Working out the gradient of $\ell$:

$$\frac{\partial \ell (\theta, \mathcal{D})}{\partial \theta} = -\sum_{i=1}^{N}\frac{\partial E(x_i;\theta)}{\partial \theta} - N \frac{\partial \log Z(\theta)}{\partial \theta} \\
 = -N\left[\frac{1}{N}\sum_{i=1}^{N}\frac{\partial E(x_i;\theta)}{\partial \theta} + \frac{1}{Z(\theta)}\frac{\partial}{\partial \theta}\sum_{all~x}e^{-E(x;\theta)}\right]\\
 = -N\left[\frac{1}{N}\sum_{i=1}^{N}\frac{\partial E(x_i;\theta)}{\partial \theta} - \sum_{all~x}\frac{\partial E(x_i;\theta)}{\partial \theta}\frac{e^{-E(x_i;\theta)}}{Z(\theta)}\right] \\
 = -N\left[\left\langle\frac{\partial E(x_i;\theta)}{\partial \theta}\right\rangle_{data}-\left\langle\frac{\partial E(x_i;\theta)}{\partial \theta}\right\rangle_{model}\right]
$$

which says that $\ell$ is maximized when the expected $\theta$ gradient of the energy over the data distribution is equal to the expected $\theta$ gradient of the energy over the model distribution.

Allow me to deviate from the current discussion and define [Kullback-Leibler (KL) divergence](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence), that with respect to two probability distributions $p(x)$ and $q(x)$ is defined as

$$D_{KL}(p||q) = \sum_{all~x}p(x)\log \frac{p(x)}{q(x)}$$

Coming back, by thinking of the data distribution of $\mathcal{D}$ as the theoretical distribution underlying $\mathcal{D}$ and denoting it by $p_{data}(x)$, consider the KL divergence between the data distribution $\mathcal{D}$ and the model distribution $p_X(x \mid \theta)$. Its negative gradient with respect to $\theta$ is

$$-\frac{\partial}{\partial \theta}D_{KL}(p_{data}(x)||p_X(x\mid \theta)) = -\frac{\partial}{\partial \theta}\sum_{all~x}p_{data}(x) \log \frac{p_{data}(x)}{p_X(x\mid \theta)} \\
 = \sum_{all~x} p_{data}(x) \frac{\partial}{\partial \theta} \log p_X(x\mid \theta)\\
 = -\sum_{i=1}^{N}\frac{\partial E(x;\theta)}{\partial \theta} -N \frac{\partial}{\partial \theta}\log Z(\theta)\\
  = -N\left[\frac{1}{N}\sum_{i=1}^{N}\frac{\partial E(x_i;\theta)}{\partial \theta} + \frac{1}{Z(\theta)}\frac{\partial}{\partial \theta}\sum_{all~x}e^{-E(x;\theta)}\right]
$$

which is same as the gradient of the likelihood function $\ell$. The equivalence of the second and third line is nontrivial; the reader might like to work it out for more rigor. Therefore, we see that minimizing the KL divergence between the distributions of the data and the model with respect to parameters $\theta$ is equivalent to maximizing the log likelihood function of the parameters given the dataset $\mathcal{D}$:

$$\hat{\theta}_{ML} = \text{argmin}_{\theta}~ D_{KL}(p_{data}||p_X(x\mid \theta))$$

Thinking of ML estimation in this manner will be useful for understanding how MPF estimation works later.

## Boltzmann Machine

We now look at an example, the visible [Boltzmann machine](https://en.wikipedia.org/wiki/Boltzmann_machine), which is a type of probabilistic model over a binary state space that has $v$ visible units $\mathbf{x} = (x_1, x_2, \ldots, x_v)$ encoding a data vector, where each $x_i \in \{0, 1\}$.

{% img left half /images/boltzmann.png 335 241 Boltzmann machine %}


The above figure gives a Boltzmann machines with three visible units and the edges represent the interactions between the nodes. The contribution of an edge is the energy $W_{ij}x_ix_j$. We also note that an edge only contribute non-zero energy iff both of its corresponding nodes are 'on'. If we were to find the energy function of this network of three nodes, we get

$$
E(x;W) = \sum_{i,j=1}^{3}W_{ij}x_ix_j
$$

and the partition function $Z(W)$ is

$$
Z(W) = \sum_{all~x} e^{-\sum_{i,j=1}^{3}W_{ij}x_ix_j}
$$

with

$$
\ell(W, \mathcal{D}) = -\sum_{x \in \mathcal{D}}\sum_{i,j=1}^{3} W_{ij}x_ix_j - N \log Z(W)
$$

The evaluation of $Z(W)$ is plausible, but solving $\partial \ell /\partial W = 0$ for the parameter $W$ is not possible analytically. Therefore, the next best option is to numerically solve for the weights $W$ using gradient ascent which we will use the gradient of the likelihood function that was derived earlier and take iterative steps $W_{ij}^{n+1} = W_{ij}^{n} + \delta W_{ij}^{n}$ where $\delta$ is the learning rate

$$
\delta W_{ij}^n \propto \left[\left\langle\frac{\partial E(x;W^n)}{\partial W_{ij}^n}\right\rangle_{data}-\left\langle\frac{\partial E(x;W^n)}{\partial W_{ij}^n}\right\rangle_{model}\right]=\Bigg[\left\langle x_ix_j\right\rangle_{data}-\left\langle x_ix_j\right\rangle_{model}\Bigg]\\
=-\left[\frac{1}{N}\sum_{x\in \mathcal{D}}x_ix_j-\sum_{all~x}x_ix_j\frac{e^{-\sum_{kl}W_{kl}x_kx_l}}{Z(W)}\right]
$$

thus to find the maximum value of $\ell(W;\mathcal{D})$ using gradient ascent for a Boltzmann machine with three units is tractable.

Now what if we try to increase the network to a Boltzmann machine with 1M units or maybe a less ambitious 100 units? You will realize that to compute $Z(W)$ we need to sum over $2^{100} \sim 10^{30}$ terms; hence it is either very costly or impossible to evaluate $p_{model}(\mathbf{x}\mid W)$, thus approximation by sampling from the distribution $p_{model}(\mathbf{x}\mid W)$ is the next best alternative.

## Conclusion

Maximum likelihood might be the *de facto* method for fitting a probabilistic model to data, however it has its limitations. In the example of the Boltzmann machine, we see that for small number of units we already have a problem of solving for the maximum analytically and have to utilize gradient ascent instead. But when we raise the number of units to the hundreds, computing the partition function becomes intractable, thus rendering the gradient ascent method not viable. Here is where MPF is different, which allows us to say goodbye to the partition function.

In my next blog post, I will gradually move closer towards unravelling MPF and also discuss some alternatives to ML that have been tried.

Happy New Year, 2017 is going to be a **prime** year.
