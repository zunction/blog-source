Title: Goodbye Partition Function
Date: 2017-01-02 10:40
Tags:
Slug: goodbye-partition-function
Author: zhangsheng

In my earlier blog post, I talked about energy based models and looked at maximum likelihood learning (ML) on Boltzmann machines as an example. We learnt that the ML method of learning probabilistic models become intractable when the number of units in the Boltzmann machine is on the order of hundreds. Here, I shall start by looking at an [contrastive divergence (CD)](http://www.cs.toronto.edu/~fritz/absps/cdmiguel.pdf), an alternative to ML.

## Contrastive Divergence

Recall in my earlier blog post [we looked at maximum likelihood (ML) learning for Boltzmann machines and identified the problem plaguing ML learning](https://zunction.github.io/2016/12/a-prelude-to-mpf/); the intractability of the partition function when the number of units is big. Therefore to overcome this problem, sampling of the model distribution $p_{model}(\mathbf{x}\mid W)$ is done to approximate the expected $\theta$ gradient over the model distribution.

Sampling provides a solution, but the time sampling takes for the distribution to converge to the model distribution is another obstacle to overcome. Hinton's contrastive divergence then does the following:

$$
\left\langle\frac{\partial E(x;\theta)}{\partial \theta}\right\rangle_{model} \to \left\langle\frac{\partial E(x;\theta)}{\partial \theta}\right\rangle_{n}
$$

which is to estimate the model distribution by doing a few step of sampling. In fact we have $n = 1$ when implementing contrastive divergence. It turns out that using this approximated gradient allows us to approximately minimize the objective function

$$
J_{CD} = D_{KL}(p^{(0)}(\mathbf{x})||p^{(\infty)}(\mathbf{x}\mid \theta)) - D_{KL}(p^{(1)}(\mathbf{x})||p^{(\infty)}(\mathbf{x}\mid \theta))
$$

At this point you would see some link after recalling that maximizing the log likelihood function of the parameters is same as minimizing the KL divergence from the model distribution to the data distribution, i.e. $D_{KL}(p_{data}(x)||p_X(x\mid \theta))$. Let's work out the gradient of $J_{CD}$ with respect to $\theta$:

$$
\frac{\partial J_{CD}}{\partial \theta} = -N\left[\left\langle\frac{\partial E(x;\theta)}{\partial \theta}\right\rangle_{0}-\left\langle\frac{\partial E(x;\theta)}{\partial \theta}\right\rangle_{model}\right] - \left(-N\left[\left\langle\frac{\partial E(x;\theta)}{\partial \theta}\right\rangle_{1}-\left\langle\frac{\partial E(x;\theta)}{\partial \theta}\right\rangle_{model}\right]\right)\\
=-N\left[\left\langle\frac{\partial E(x;\theta)}{\partial \theta}\right\rangle_{0}-\left\langle\frac{\partial E(x;\theta)}{\partial \theta}\right\rangle_{1}\right]
$$

where the $\langle \cdot \rangle_n$ denotes the expectation after $n$ sampling steps with $n = 0$ refers to the data distribution and $n = \infty$ the model distribution. Thus if we look at the gradient of the log likelihood function,

$$
\frac{\partial \ell(\theta;\mathcal{D})}{\partial \theta} -N\left[\left\langle\frac{\partial E(x_i;\theta)}{\partial \theta}\right\rangle_{0}-\left\langle\frac{\partial E(x_i;\theta)}{\partial \theta}\right\rangle_{\infty}\right]
$$

we can see the difference between using ML estimator and contrastive divergence. The latter is evolved over one step before being used to approximate the gradient as compared to the former where many steps of sampling has to be carried out before we can arrive at the model distribution. CD might seem to be an excellent remedy to the large number of sampling to be done to get the model distribution but there is no guarantee of convergence.

## Minimum Probability Flow

We finally arrive at MPF after going through maximum likelihood estimation (MLE) and CD. The goal of MPF is to find parameters that cause a probabilistic model to best agree with a list $\mathcal{D}$ of assumed iid observations of the state of the system. The approach uses deterministic dynamics that guarantees the transformation of the data distribution to the model distribution and then minimizing the KL divergence between them that results from running the dynamics for a short time $\epsilon$. For the discussion here, we will be considering Boltzmann machines with binary states.

### Distribution

We use $\mathbf{p}^{(0)}$ to denote the data distribution, with $p^{(0)}_i$ the fraction of the observations $\mathcal{D}$ in state $i$. The superscript refers to the time under the system dynamics and for the superscript $(\infty)$ it refers to the model distribution obtained after running the dynamics for infinite time. The model distribution is assumed to be of the form

$$
p_i^{(\infty)}(\theta) = \frac{\exp(-E_i(\theta))}{Z(\theta)}
$$

where $\mathbf{E}(\theta)$ is the energy function and the normalizing factor $Z(\theta)$ is the partition function

$$
Z(\theta) = \sum_i \exp(-E_i(\theta))
$$

this can also be though of as a [Boltzmann distribution](https://en.wikipedia.org/wiki/Boltzmann_distribution) of a physical system with $k_BT = 1$.

### Dynamics

The conversation of probability enforced by the [master equation](https://en.wikipedia.org/wiki/Master_equation) for the time evolution of a distribution $\mathbf{p}^{(t)}$:

$$
\dot{p}_{i}^{(t)} = \sum_{j\neq i}\Gamma_{ij}(\theta)p_j^{(t)} -  \sum_{j\neq i}\Gamma_{ji}(\theta)p_i^{(t)}
$$

where $\dot{p}_{i}^{(t)}$ is the time derivative of $p_i^{(t)}$. The transition rates $\Gamma_{ij}(\theta)$ for $i\neq j$ give the rate at which probability flows from state $j$ into state $i$. Thus the first term of the equation above captures the flow of probability out of other states $j$ into state $i$ and the reverse is true for the second term. The dependence on $\theta$ results from the requirement that the chosen dynamics cause $\mathbf{p}^{(t)}$ to flow to the equilibrium distribution $\mathbf{p}^{(\infty)}$. Setting the diagonal entries of $\mathbf{\Gamma}$ to be $\Gamma_{ii} = -\sum_{j\neq i}\Gamma_{ji}$, we can then write the dynamics as

$$
\mathbf{\dot{p}}^{(t)} = \mathbf{\Gamma}\mathbf{p}^{(t)}
$$

where the explicit dependence on $\theta$ is dropped unless necessary. The unique solution for $\mathbf{p}^{(t)}$ is

$$
\mathbf{p}^{(t)} = \exp (\mathbf{\Gamma t})\mathbf{p}^{(0)}
$$

where $\exp (\mathbf{\Gamma t})$ is the matrix exponential. This solution allows us to find the distribution of the states at any continuous time $t$ compared to the discrete sampling steps used in contrastive divergence.

### Detailed Balance

Another core concept is [detailed balance](https://en.wikipedia.org/wiki/Detailed_balance),

$$
\Gamma_{ji}p_i^{(\infty)}(\theta) = \Gamma_{ij}p_j^{(\infty)}(\theta)
$$

which states that at equilibirum the probability flow from $j$ into $i$ equals the probability flow from $i$ into $j$. Having detailed balance guarantees that the distribution $\mathbf{p}^{(\infty)}$ is a fixed point of the dynamics. We can further simplify the detailed balance requirement to

$$
\Gamma_{ji}\exp(-E_i(\theta)) = \Gamma_{ij}\exp(-E_i(\theta))
$$

which conveniently removes the usually intractable partition function. The choice of $\mathbf{\Gamma}$ is chosen to be

$$
\Gamma_{ij} = g_{ij}\exp\left[\frac{1}{2}(E_j(\theta)-E_i(\theta))\right]\qquad i\neq j
$$

with

$$
g_{ij} = \begin{cases}0 & \text{unconnected states}\\ 1 & \text{connected states}\end{cases} \qquad i \neq j
$$

decides which states are allowed to exchange probabilities with each other. The coefficients $g_{ij}$ can be set such that $\mathbf{\Gamma}$ is *extremely sparse* which we shall see later why this is crucial.


### Objective Function

Before we jump right into the objective function for MPF, let's take a quick look at the objective function of ML and CD.

Maximum likelihood:
$$
\hat{\theta}_{ML} = \text{argmin}_{\theta}~ D_{KL}(p^{(0)}||p^{(\infty)})
$$

Contrastive divergence:
$$
\hat{\theta}_{CD} = \text{argmin}_{\theta}~ D_{KL}(p^{(0)}||p^{(\infty)}) - D_{KL}(p^{(1)}||p^{(\infty)})
$$

and now for Minimum probability flow, we have:

$$
\hat{\theta}_{MPF} = \text{argmin}_{\theta}~ D_{KL}(p^{(0)}||p^{(\epsilon)})
$$

which is to minimize the KL divergence after running the dynamics for an infinitesimal time $\epsilon$. To calculate the cost function, $K(\theta)$ we approximate it using first order Taylor expansion:

$$
K(\theta) \approx D_{KL}(p^{(0)}||p^{(t)})\mid_{t=0} + \epsilon \frac{\partial D_{KL}(p^{(0)}||p^{(t)})}{\partial t}\mid_{t=0}
$$

skipping the specifics here, we arrive at

$$
K(\theta) \approx \epsilon\sum_{i \notin \mathcal{D}}\sum_{j \in \mathcal{D}}\Gamma_{ij}p_j^{(0)}\\
= \frac{\epsilon}{|\mathcal{D}|}\sum_{i \notin \mathcal{D}}\sum_{j \in \mathcal{D}}\Gamma_{ij}
$$

which is a measure of flow of probabilities at time $t=0$ under the dynamics, out of the states $j \in \mathcal{D}$ into non-data states $i \notin \mathcal{D}$. Rewriting the explicit expression of $\Gamma_{ij}$,

$$
K(\theta) = \frac{\epsilon}{|\mathcal{D}|}\sum_{i \notin \mathcal{D}}\sum_{j \in \mathcal{D}} g_{ij}\exp\left[\frac{1}{2}(E_j(\theta) - E_i(\theta))\right]
$$

with its gradient with respect to $\theta$

$$
\frac{\partial K(\theta)}{\partial \theta} = \frac{\epsilon}{|\mathcal{D}|}\sum_{i \notin \mathcal{D}}\sum_{j \in \mathcal{D}} \left (\frac{\partial E_j(\theta)}{\partial \theta} - \frac{\partial E_i(\theta)}{\partial \theta}\right) g_{ij}\exp\left[\frac{1}{2}(E_j(\theta) - E_i(\theta))\right]
$$

where $|\mathcal{D}|$ is the number of observed data points. There is also no need to evaluate the partition function for both the cost function and gradient of the cost function for MPF.

### Tractability

With everything in place, we can go on to discuss about the feasibility of computing the cost function and gradient. Although we have successful avoided having to compute the intractable partition function, we are still not assured that the cost of computation is within our means.

Looking at the construction of MPF and considering a Boltzmann machine with $d$ binary states, each sample is a $d$ dimension binary vector; thus there are $2^d$ possible states and $\mathbf{\Gamma}$ will be a $2^d \times 2^d$ matrix. If we were to have 100 units in our network, it would seem to be impossible to evaluate the objective function. However, if we were to limit the connectivity of the states using the $g_{ij}$ we can reduce the amount of computation in the cost function. One example would be define two states are connected if they are of one [Hamming distance](https://en.wikipedia.org/wiki/Hamming_distance) away from each other which is what I used in the implementation of MPF. Thus by making $\mathbf{\Gamma}$ sparse, we ensure the tractability of the cost function and gradient.

### Conclusion

Building upon our learnings of ML and CD, we see how MPF differs from them. One major win for  MPF is that it elegantly avoids the partition function by running the dynamics over an infinitesimal time $\epsilon$, small enough for us to approximate the cost using Taylor expansion. The flexibility of choosing $g_{ij}$ to make $\mathbf{\Gamma}$ sparse makes MPF tractable.

A few thoughts that I have from learning MPF is that although we have greater access to computing power, for example the [NVIDIA DGX-1](http://www.nvidia.com/object/deep-learning-system.html) which is a dedicated deep learning system, we cannot take all this computing power for granted. There might be a day where we exhaust the limits of computing power and before this happens, we should try to find new learning models that allow us to learn at a cheaper computing cost. The MPF learning technique we looked at today is just that start.
