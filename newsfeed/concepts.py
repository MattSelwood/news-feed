"""Daily rotating math / statistics / AI concepts.

One concept is shown per day, cycling through the full list so that each concept
reappears roughly every two months.
"""

from datetime import date

# ---------------------------------------------------------------------------
# Concept definitions
# ---------------------------------------------------------------------------
# Each concept contains:
#   title    – short display name
#   category – broad discipline
#   equation – ASCII / Unicode representation of the key formula
#   overview – multi-line explanation shown in the detail pane
# ---------------------------------------------------------------------------

CONCEPTS = [
    {
        "title": "Normal (Gaussian) Distribution",
        "category": "Statistics",
        "equation": "f(x) = (1 / sqrt(2*pi*sigma^2)) * exp(-(x-mu)^2 / (2*sigma^2))",
        "overview": (
            "The Normal distribution is the most widely used distribution in statistics, "
            "parameterised by mean mu and variance sigma^2.\n\n"
            "Key properties:\n"
            "  • 68-95-99.7 rule: 68% of data lies within ±1σ, 95% within ±2σ, 99.7% within ±3σ\n"
            "  • It is the maximum-entropy distribution for a given mean and variance\n"
            "  • The sum of n IID random variables converges to Normal (Central Limit Theorem)\n\n"
            "Why it matters: measurement errors, heights, test scores, financial returns "
            "(approximately) all follow Normal-like distributions.  Its tractability makes "
            "it the default assumption in countless statistical models."
        ),
    },
    {
        "title": "Bayes' Theorem",
        "category": "Probability",
        "equation": "P(A|B) = P(B|A) * P(A) / P(B)",
        "overview": (
            "Bayes' Theorem relates the conditional probability of A given B to the reverse "
            "conditional probability, prior probability, and marginal probability.\n\n"
            "Terms:\n"
            "  • P(A|B) – posterior: belief in A after seeing evidence B\n"
            "  • P(B|A) – likelihood: probability of evidence B if A is true\n"
            "  • P(A)   – prior: initial belief before seeing evidence\n"
            "  • P(B)   – marginal likelihood (normalisation constant)\n\n"
            "Applications: spam filtering, medical diagnosis, Bayesian neural networks, "
            "Kalman filtering.  Bayesian inference provides a principled way to update "
            "beliefs with new data."
        ),
    },
    {
        "title": "Central Limit Theorem",
        "category": "Statistics",
        "equation": "sqrt(n) * (X_bar - mu) / sigma  -->  N(0, 1)  as n --> inf",
        "overview": (
            "The Central Limit Theorem (CLT) states that the standardised sum of n "
            "independent, identically distributed (IID) random variables with finite "
            "mean mu and variance sigma^2 converges in distribution to a standard Normal.\n\n"
            "Why it matters:\n"
            "  • Justifies using the Normal distribution to approximate sample means\n"
            "  • Foundation of classical hypothesis testing and confidence intervals\n"
            "  • Explains why Normal-like patterns appear throughout nature and measurement\n\n"
            "Caveats: requires finite variance; convergence can be slow for highly skewed "
            "distributions; fails for heavy-tailed distributions without finite variance."
        ),
    },
    {
        "title": "Maximum Likelihood Estimation",
        "category": "Statistics",
        "equation": "theta_MLE = argmax_theta  sum_i log p(x_i | theta)",
        "overview": (
            "MLE finds the parameter(s) theta that maximise the probability of the "
            "observed data under the assumed statistical model.\n\n"
            "Working in log-space converts the product of likelihoods into a sum, "
            "making optimisation tractable.\n\n"
            "Properties:\n"
            "  • Consistent: converges to the true parameter as n → ∞\n"
            "  • Asymptotically efficient: achieves the Cramér–Rao lower bound\n"
            "  • Not always unbiased (e.g. MLE for variance uses n, not n-1)\n\n"
            "MLE is the foundation of logistic regression, neural network training "
            "(cross-entropy loss = negative log-likelihood), and GLMs."
        ),
    },
    {
        "title": "Gradient Descent",
        "category": "Optimisation / ML",
        "equation": "theta_new = theta_old - alpha * grad_theta L(theta)",
        "overview": (
            "Gradient descent iteratively moves parameters theta in the direction of "
            "steepest descent of a loss function L, scaled by learning rate alpha.\n\n"
            "Variants:\n"
            "  • Batch GD: uses all training examples per update — stable but slow\n"
            "  • Stochastic GD (SGD): one example per update — noisy but fast\n"
            "  • Mini-batch GD: compromise; standard in deep learning\n\n"
            "Practical improvements: momentum (builds velocity), RMSProp (adaptive LR), "
            "Adam (combines both).  Choosing learning rate is critical: too large → "
            "divergence; too small → slow convergence."
        ),
    },
    {
        "title": "Backpropagation",
        "category": "Deep Learning",
        "equation": "dL/dW_l = dL/dz_{l+1} * dz_{l+1}/dz_l * dz_l/dW_l  (chain rule)",
        "overview": (
            "Backpropagation efficiently computes gradients of the loss with respect "
            "to every weight in a neural network by applying the chain rule backwards "
            "through the computational graph.\n\n"
            "Steps:\n"
            "  1. Forward pass: compute activations and store intermediate values\n"
            "  2. Compute loss at output\n"
            "  3. Backward pass: propagate error gradients layer by layer\n"
            "  4. Update weights using gradient descent\n\n"
            "Time complexity is O(W) per sample — the same order as a forward pass — "
            "making training of large networks feasible."
        ),
    },
    {
        "title": "Bias–Variance Trade-off",
        "category": "ML Theory",
        "equation": "E[(y - f_hat)^2] = Bias^2 + Variance + Irreducible Noise",
        "overview": (
            "The expected prediction error decomposes into three terms:\n\n"
            "  • Bias^2: error from wrong model assumptions (underfitting)\n"
            "  • Variance: sensitivity to fluctuations in training data (overfitting)\n"
            "  • Noise: irreducible randomness in the data\n\n"
            "Increasing model complexity typically decreases bias but increases variance. "
            "The sweet spot minimises their sum.\n\n"
            "Practical mitigation: regularisation (Ridge, Lasso) reduces variance; "
            "ensemble methods (Random Forests, Bagging) reduce variance by averaging; "
            "Boosting reduces bias."
        ),
    },
    {
        "title": "Shannon Entropy",
        "category": "Information Theory",
        "equation": "H(X) = -sum_x  p(x) * log2( p(x) )",
        "overview": (
            "Shannon entropy measures the average uncertainty (information content) "
            "of a random variable X.  It is measured in bits (log base 2) or nats (ln).\n\n"
            "Properties:\n"
            "  • Maximum for uniform distributions: H = log2(n) for n outcomes\n"
            "  • Zero for deterministic outcomes\n"
            "  • Additive for independent random variables\n\n"
            "Applications: lossless compression (Shannon's source coding theorem shows "
            "H is the minimum average code length), cryptography, decision trees "
            "(information gain = entropy reduction), and mutual information."
        ),
    },
    {
        "title": "KL Divergence",
        "category": "Information Theory",
        "equation": "KL(P || Q) = sum_x  P(x) * log( P(x) / Q(x) )",
        "overview": (
            "Kullback–Leibler divergence measures how much distribution P differs from "
            "reference distribution Q.  It can be interpreted as the extra bits needed "
            "to encode samples from P using a code optimised for Q.\n\n"
            "Key properties:\n"
            "  • KL(P||Q) >= 0  (Gibbs' inequality)\n"
            "  • KL(P||Q) = 0  iff  P = Q\n"
            "  • NOT symmetric: KL(P||Q) ≠ KL(Q||P) in general\n\n"
            "Used in: variational inference (ELBO = E[log p] - KL), VAEs, "
            "reinforcement learning, and as a loss in language models."
        ),
    },
    {
        "title": "Principal Component Analysis (PCA)",
        "category": "Dimensionality Reduction",
        "equation": "X_reduced = X * W  where  W = top-k eigenvectors of X^T X",
        "overview": (
            "PCA finds the orthogonal directions (principal components) of maximum "
            "variance in a dataset and projects data onto the top-k components.\n\n"
            "Algorithm:\n"
            "  1. Centre the data (subtract mean)\n"
            "  2. Compute covariance matrix C = X^T X / (n-1)\n"
            "  3. Eigen-decompose C: eigenvectors are principal components\n"
            "  4. Project data onto top-k eigenvectors\n\n"
            "Applications: visualisation (2D/3D plots), noise reduction, feature "
            "extraction, speeding up downstream ML.  Equivalent to truncated SVD."
        ),
    },
    {
        "title": "Singular Value Decomposition (SVD)",
        "category": "Linear Algebra",
        "equation": "A = U * Sigma * V^T",
        "overview": (
            "SVD factorises any m×n matrix A into:\n"
            "  • U: m×m orthogonal matrix (left singular vectors)\n"
            "  • Sigma: m×n diagonal matrix of non-negative singular values\n"
            "  • V^T: n×n orthogonal matrix (right singular vectors)\n\n"
            "Applications:\n"
            "  • PCA (truncated SVD on centred data)\n"
            "  • Recommender systems (matrix factorisation)\n"
            "  • Least-squares regression and pseudo-inverse\n"
            "  • Image compression (keep top-k singular values)\n"
            "  • Numerical rank determination and condition numbers"
        ),
    },
    {
        "title": "Attention Mechanism (Transformers)",
        "category": "Deep Learning",
        "equation": "Attention(Q,K,V) = softmax( Q K^T / sqrt(d_k) ) V",
        "overview": (
            "The scaled dot-product attention, introduced in 'Attention Is All You Need' "
            "(Vaswani et al., 2017), allows each position in a sequence to attend to "
            "all other positions.\n\n"
            "  • Q (queries), K (keys), V (values) are linear projections of the input\n"
            "  • dot product Q K^T measures compatibility between positions\n"
            "  • scaling by sqrt(d_k) prevents vanishing gradients in softmax\n\n"
            "Multi-Head Attention runs h parallel attention heads and concatenates, "
            "enabling the model to attend to different representation subspaces. "
            "Transformers built on this power GPT, BERT, and LLaMA."
        ),
    },
    {
        "title": "Poisson Distribution",
        "category": "Statistics",
        "equation": "P(X=k) = (lambda^k * e^-lambda) / k!   for k=0,1,2,...",
        "overview": (
            "The Poisson distribution models the number of events occurring in a fixed "
            "interval when events are independent and occur at a constant average rate lambda.\n\n"
            "Properties:\n"
            "  • Mean = Variance = lambda\n"
            "  • Approximates Binomial(n,p) when n is large and p is small (lambda = np)\n"
            "  • Sum of independent Poisson(lambda_i) is Poisson(sum lambda_i)\n\n"
            "Applications: call centre arrivals, radioactive decay counts, server "
            "request rates, rare event modelling in insurance and epidemiology."
        ),
    },
    {
        "title": "Binomial Distribution",
        "category": "Statistics",
        "equation": "P(X=k) = C(n,k) * p^k * (1-p)^(n-k)",
        "overview": (
            "The Binomial distribution models the number of successes in n independent "
            "Bernoulli trials, each with success probability p.\n\n"
            "Properties:\n"
            "  • Mean = n*p,  Variance = n*p*(1-p)\n"
            "  • Converges to Normal(np, np(1-p)) as n → ∞ (CLT)\n"
            "  • Converges to Poisson(np) when n→∞ and p→0\n\n"
            "Applications: A/B test outcomes, quality control, genetics (allele counts), "
            "any scenario involving a fixed number of independent yes/no trials."
        ),
    },
    {
        "title": "Cross-Entropy Loss",
        "category": "ML / Information Theory",
        "equation": "H(y, y_hat) = -sum_c  y_c * log( y_hat_c )",
        "overview": (
            "Cross-entropy measures the dissimilarity between true label distribution y "
            "and predicted distribution y_hat over classes c.\n\n"
            "For binary classification with sigmoid output:\n"
            "  Loss = -[ y*log(p) + (1-y)*log(1-p) ]\n\n"
            "Why it works: minimising cross-entropy is equivalent to maximising the "
            "log-likelihood under the model, connecting it directly to MLE.\n\n"
            "It is the standard loss for classification tasks because it penalises "
            "confident wrong predictions heavily (log(0) → -∞)."
        ),
    },
    {
        "title": "Adam Optimiser",
        "category": "Optimisation / Deep Learning",
        "equation": (
            "m_t = beta1*m_{t-1} + (1-beta1)*g_t\n"
            "  v_t = beta2*v_{t-1} + (1-beta2)*g_t^2\n"
            "  theta -= alpha * m_hat_t / (sqrt(v_hat_t) + eps)"
        ),
        "overview": (
            "Adam (Adaptive Moment Estimation, Kingma & Ba 2015) combines:\n"
            "  • Momentum: exponential moving average of gradients (m_t)\n"
            "  • RMSProp: exponential moving average of squared gradients (v_t)\n\n"
            "Bias-corrected estimates m_hat = m/(1-beta1^t) and v_hat = v/(1-beta2^t) "
            "compensate for zero-initialisation at t=1.\n\n"
            "Default hyperparameters: alpha=1e-3, beta1=0.9, beta2=0.999, eps=1e-8.\n\n"
            "Adam is the de-facto default optimiser for training deep neural networks."
        ),
    },
    {
        "title": "Fourier Transform",
        "category": "Mathematics / Signal Processing",
        "equation": "F(omega) = integral  f(t) * e^(-i*omega*t) dt",
        "overview": (
            "The Fourier Transform decomposes a time-domain signal f(t) into its "
            "constituent frequencies, represented in the frequency domain F(omega).\n\n"
            "Key pairs:\n"
            "  • Gaussian → Gaussian (self-dual)\n"
            "  • Rect window → Sinc function\n"
            "  • Convolution in time ↔ multiplication in frequency\n\n"
            "The Discrete Fourier Transform (DFT) and its O(n log n) algorithm, the FFT, "
            "are fundamental to audio processing, image compression (JPEG), solving "
            "PDEs, and polynomial multiplication."
        ),
    },
    {
        "title": "Eigenvalues and Eigenvectors",
        "category": "Linear Algebra",
        "equation": "A v = lambda v   (lambda = eigenvalue, v = eigenvector)",
        "overview": (
            "An eigenvector v of matrix A is a non-zero vector that is only scaled "
            "(not rotated) by A; the scaling factor is the eigenvalue lambda.\n\n"
            "Found by solving  det(A - lambda*I) = 0  (characteristic polynomial).\n\n"
            "Applications:\n"
            "  • PCA: eigenvectors of covariance matrix are principal components\n"
            "  • PageRank: leading eigenvector of the web graph transition matrix\n"
            "  • Quantum mechanics: observable quantities are eigenvalues of operators\n"
            "  • Graph theory: graph Laplacian eigenvectors enable spectral clustering"
        ),
    },
    {
        "title": "Markov Chains",
        "category": "Probability / Statistics",
        "equation": "P(X_{t+1}=j | X_t=i, X_{t-1},...) = P(X_{t+1}=j | X_t=i) = T_{ij}",
        "overview": (
            "A Markov Chain is a stochastic process where the next state depends only "
            "on the current state (Markov property / memorylessness).\n\n"
            "Described by a transition matrix T where T_ij = P(go from i to j).\n\n"
            "Key concepts:\n"
            "  • Stationary distribution pi: pi = pi * T (long-run frequencies)\n"
            "  • Ergodic chains converge to a unique stationary distribution\n\n"
            "Applications: MCMC sampling, language models (n-grams), Google PageRank, "
            "hidden Markov models (HMMs), queueing theory, genetics."
        ),
    },
    {
        "title": "Confidence Intervals",
        "category": "Statistics",
        "equation": "CI_95 = X_bar  ±  1.96 * (sigma / sqrt(n))",
        "overview": (
            "A 95% confidence interval means that if we repeated the experiment many "
            "times, 95% of the intervals constructed would contain the true parameter.\n\n"
            "Common misconception: it does NOT mean 'there is a 95% probability that "
            "the true parameter lies in this specific interval'.\n\n"
            "Width decreases with sqrt(n) — quadrupling sample size halves the interval.\n\n"
            "For small samples (n < 30) or unknown sigma, use the t-distribution "
            "instead of the Normal to obtain t-intervals."
        ),
    },
    {
        "title": "Support Vector Machines (SVM)",
        "category": "ML",
        "equation": "max_{w,b}  2/||w||  subject to  y_i(w·x_i + b) >= 1",
        "overview": (
            "SVMs find the maximum-margin hyperplane separating two classes.  "
            "The margin is 2/||w||, and maximising it is equivalent to minimising ||w||.\n\n"
            "The support vectors are the training points closest to the decision boundary.\n\n"
            "The kernel trick replaces the dot product with K(x_i, x_j) = phi(x_i)·phi(x_j), "
            "allowing non-linear decision boundaries without explicit feature maps:\n"
            "  • RBF/Gaussian kernel: K(x,z) = exp(-||x-z||^2 / (2*sigma^2))\n"
            "  • Polynomial kernel: K(x,z) = (x·z + c)^d"
        ),
    },
    {
        "title": "Random Forests",
        "category": "ML / Ensemble Methods",
        "equation": "f_RF(x) = (1/B) * sum_{b=1}^{B} T_b(x)  [trees T_b on bootstrap samples]",
        "overview": (
            "Random Forests aggregate predictions from B decision trees, each trained on "
            "a bootstrap sample of the data with a random subset of features at each split.\n\n"
            "Two sources of randomisation:\n"
            "  1. Bagging (bootstrap aggregating): reduces variance by averaging\n"
            "  2. Random feature subset: decorrelates the trees\n\n"
            "Out-of-bag (OOB) error: each tree is evaluated on ~37% of points not in "
            "its bootstrap sample, giving a free cross-validation estimate.\n\n"
            "Highly robust, handles mixed feature types, provides feature importances."
        ),
    },
    {
        "title": "K-Means Clustering",
        "category": "Unsupervised ML",
        "equation": "min_{C} sum_{k} sum_{x in C_k}  ||x - mu_k||^2",
        "overview": (
            "K-Means partitions n points into K clusters by minimising within-cluster "
            "sum-of-squares (WCSS).  The standard Lloyd algorithm alternates:\n"
            "  1. Assignment: assign each point to nearest centroid\n"
            "  2. Update: recompute centroids as cluster means\n\n"
            "Caveats:\n"
            "  • Converges to local optima — use k-means++ initialisation\n"
            "  • Sensitive to outliers and cluster scale\n"
            "  • Assumes spherical, equal-size clusters\n\n"
            "Choosing K: Elbow method (WCSS vs K), Silhouette score, or Gap statistic."
        ),
    },
    {
        "title": "Hypothesis Testing & p-values",
        "category": "Statistics",
        "equation": "p = P(|T| >= |t_obs|  |  H_0 true)",
        "overview": (
            "A p-value is the probability of observing a test statistic at least as "
            "extreme as the one observed, assuming the null hypothesis H_0 is true.\n\n"
            "  • p < alpha (e.g. 0.05): reject H_0 — result is 'statistically significant'\n"
            "  • p >= alpha: fail to reject H_0 — NOT proof that H_0 is true\n\n"
            "Common errors:\n"
            "  • Type I (false positive): reject H_0 when it is true (rate = alpha)\n"
            "  • Type II (false negative): fail to reject H_0 when false (rate = beta)\n\n"
            "Power = 1 - beta = P(reject H_0 | H_1 true).  Increases with sample size."
        ),
    },
    {
        "title": "Logistic Regression",
        "category": "ML / Statistics",
        "equation": "P(y=1|x) = sigmoid(w·x + b)  =  1 / (1 + e^(-(w·x + b)))",
        "overview": (
            "Despite the name, logistic regression is a classification model that "
            "predicts the probability of a binary outcome.\n\n"
            "The log-odds (logit) is modelled as linear: log(p/(1-p)) = w·x + b.\n\n"
            "Trained by minimising cross-entropy loss (= negative log-likelihood).\n\n"
            "Key properties:\n"
            "  • Probabilistic output (0–1)\n"
            "  • Coefficients are interpretable as log-odds ratios\n"
            "  • Fast and highly regularisable (L1 for sparsity, L2 for stability)\n"
            "  • Generalises to multinomial logistic regression for K classes"
        ),
    },
    {
        "title": "Regularisation: Ridge and Lasso",
        "category": "ML / Statistics",
        "equation": "Ridge: L + lambda*||w||^2    Lasso: L + lambda*||w||_1",
        "overview": (
            "Regularisation adds a penalty on model complexity to the training loss, "
            "reducing variance at the cost of some bias.\n\n"
            "Ridge (L2):\n"
            "  • Penalises sum of squared weights\n"
            "  • Shrinks coefficients towards zero but rarely to exactly zero\n"
            "  • Closed-form solution: w = (X^T X + lambda*I)^{-1} X^T y\n\n"
            "Lasso (L1):\n"
            "  • Penalises sum of absolute weights\n"
            "  • Encourages exact sparsity — useful for feature selection\n\n"
            "Elastic Net combines both: lambda1*||w||_1 + lambda2*||w||^2."
        ),
    },
    {
        "title": "Variational Autoencoders (VAE)",
        "category": "Deep Learning / Generative Models",
        "equation": "ELBO = E_q[log p(x|z)] - KL( q(z|x) || p(z) )",
        "overview": (
            "A VAE is a generative model that learns a latent representation z of data x "
            "by maximising the Evidence Lower BOund (ELBO).\n\n"
            "  • Encoder q(z|x): maps data to distribution in latent space\n"
            "  • Decoder p(x|z): reconstructs data from latent code\n"
            "  • KL term: regularises the latent space towards prior p(z) = N(0,I)\n\n"
            "Reparameterisation trick: z = mu + sigma * epsilon, epsilon ~ N(0,I), "
            "allows gradients to flow through the sampling operation.\n\n"
            "Enables: continuous interpolation in latent space, novel sample generation."
        ),
    },
    {
        "title": "Convolutional Neural Networks (CNN)",
        "category": "Deep Learning",
        "equation": "(f * g)[n] = sum_k  f[k] * g[n-k]  (discrete convolution)",
        "overview": (
            "CNNs exploit spatial structure in data (images, audio) through three ideas:\n"
            "  • Local connectivity: each neuron connects only to a small receptive field\n"
            "  • Weight sharing: the same filter is applied across all spatial positions\n"
            "  • Pooling: subsampling (max/avg) provides translation invariance\n\n"
            "Building blocks: Conv → BatchNorm → ReLU → Pool → (repeat) → FC layers.\n\n"
            "Key architectures: LeNet (1998), AlexNet (2012), VGG, ResNet (skip connections), "
            "EfficientNet.  Transformed computer vision and beyond."
        ),
    },
    {
        "title": "Batch Normalisation",
        "category": "Deep Learning",
        "equation": "BN(x) = gamma * (x - mu_B) / sqrt(sigma_B^2 + eps)  +  beta",
        "overview": (
            "Batch Norm normalises activations across the mini-batch (mean 0, variance 1) "
            "then applies learnable scale gamma and shift beta.\n\n"
            "Benefits:\n"
            "  • Reduces internal covariate shift — allows higher learning rates\n"
            "  • Acts as light regularisation (adds noise from batch statistics)\n"
            "  • Smooths the loss landscape, accelerating convergence\n\n"
            "At inference, running estimates of mean and variance replace batch statistics.\n\n"
            "Variants: Layer Norm (over feature dim, used in Transformers), "
            "Instance Norm (per sample), Group Norm."
        ),
    },
    {
        "title": "Dropout Regularisation",
        "category": "Deep Learning",
        "equation": "h_dropped = h * Bernoulli(p)  /  p   (inverted dropout)",
        "overview": (
            "Dropout randomly sets a fraction p of neuron activations to zero during "
            "training, forcing the network not to rely on any single neuron.\n\n"
            "Interpretation: equivalent to training an exponential ensemble of 2^n "
            "sub-networks and averaging at test time.\n\n"
            "The inverted scaling by 1/p preserves expected activation magnitude, so "
            "no adjustment is needed at test time.\n\n"
            "Typical values: p=0.5 for FC layers, p=0.1–0.2 for convolutional layers. "
            "Superseded by BatchNorm in many architectures but still widely used."
        ),
    },
    {
        "title": "Transfer Learning & Fine-tuning",
        "category": "Deep Learning",
        "equation": "theta_new = theta_pretrained  (then fine-tune on target task)",
        "overview": (
            "Transfer learning initialises a model with weights pretrained on a large "
            "source task (e.g. ImageNet, Common Crawl) and adapts it to a target task.\n\n"
            "Strategies:\n"
            "  • Feature extraction: freeze pretrained layers, train only new head\n"
            "  • Fine-tuning: unfreeze some/all layers and train with small learning rate\n"
            "  • Full fine-tuning: unfreeze all layers\n\n"
            "Why it works: early layers learn general features (edges, textures, syntax) "
            "transferable across tasks.  Requires far less labelled target data.\n\n"
            "Foundation models (GPT, BERT, ViT) are designed to be fine-tuned."
        ),
    },
    {
        "title": "Generative Adversarial Networks (GAN)",
        "category": "Deep Learning / Generative Models",
        "equation": "min_G max_D  E[log D(x)] + E[log(1 - D(G(z)))]",
        "overview": (
            "A GAN (Goodfellow et al., 2014) trains two networks adversarially:\n"
            "  • Generator G: maps noise z to synthetic samples G(z)\n"
            "  • Discriminator D: classifies real vs. fake samples\n\n"
            "At Nash equilibrium, G(z) matches the true data distribution and D outputs 0.5 "
            "everywhere (cannot distinguish real from fake).\n\n"
            "Challenges: mode collapse, training instability, vanishing gradients.\n\n"
            "Key advances: DCGAN, Wasserstein GAN (Lipschitz constraint, stable training), "
            "StyleGAN (high-quality image synthesis), CycleGAN (unpaired translation)."
        ),
    },
    {
        "title": "Diffusion Models",
        "category": "Deep Learning / Generative Models",
        "equation": "x_{t-1} = (1/sqrt(alpha_t)) * (x_t - beta_t/sqrt(1-alpha_t_bar) * eps_theta(x_t,t)) + noise",
        "overview": (
            "Diffusion models (DDPM, Sohl-Dickstein et al.; Ho et al. 2020) learn to "
            "reverse a gradual noising process:\n\n"
            "  Forward: add Gaussian noise over T steps until x_T ~ N(0,I)\n"
            "  Reverse: train a neural network eps_theta to predict the noise at each step\n\n"
            "The denoising score matching objective trains eps_theta to predict the noise "
            "added at a random step, connecting to score-based generative models.\n\n"
            "Stable Diffusion, DALL-E 2/3, Midjourney, and Sora are based on diffusion. "
            "They outperform GANs on sample quality and diversity."
        ),
    },
    {
        "title": "Q-Learning & Bellman Equation",
        "category": "Reinforcement Learning",
        "equation": "Q(s,a) = r + gamma * max_{a'} Q(s', a')  (Bellman optimality)",
        "overview": (
            "Q-Learning learns the action-value function Q(s,a) = expected discounted "
            "return from taking action a in state s and then acting optimally.\n\n"
            "TD update rule:\n"
            "  Q(s,a) <- Q(s,a) + alpha * [r + gamma*max_{a'} Q(s',a') - Q(s,a)]\n\n"
            "Key properties:\n"
            "  • Off-policy: learns optimal policy regardless of behaviour policy\n"
            "  • Model-free: no environment model required\n"
            "  • Tabular Q-learning converges to Q* under mild conditions\n\n"
            "Deep Q-Network (DQN) approximates Q with a neural net, using experience "
            "replay and target networks for stability."
        ),
    },
    {
        "title": "Monte Carlo Methods",
        "category": "Statistics / Computation",
        "equation": "E[f(X)] ≈ (1/N) * sum_{i=1}^{N}  f(x_i),   x_i ~ p(x)",
        "overview": (
            "Monte Carlo methods use random sampling to approximate integrals, "
            "expectations, and other quantities that are analytically intractable.\n\n"
            "By the Law of Large Numbers, the sample average converges to the true "
            "expectation as N → ∞.  The error is O(1/sqrt(N)) regardless of dimension, "
            "making it invaluable in high-dimensional problems.\n\n"
            "Applications:\n"
            "  • Numerical integration (quadrature)\n"
            "  • Option pricing (Black-Scholes Monte Carlo)\n"
            "  • Bayesian inference (MCMC)\n"
            "  • Particle physics and nuclear simulations\n"
            "  • Monte Carlo Tree Search (AlphaGo)"
        ),
    },
    {
        "title": "MCMC: Metropolis–Hastings",
        "category": "Statistics / Bayesian Inference",
        "equation": "Accept x' with prob  min(1,  p(x')*q(x|x') / (p(x)*q(x'|x)) )",
        "overview": (
            "Markov Chain Monte Carlo (MCMC) draws samples from a target distribution "
            "p(x) (known up to normalisation) by constructing an ergodic Markov chain "
            "with p as its stationary distribution.\n\n"
            "Metropolis–Hastings:\n"
            "  1. Propose x' from proposal q(x'|x)\n"
            "  2. Accept with probability min(1, p(x')q(x|x') / (p(x)q(x'|x)))\n"
            "  3. If accepted: x <- x'; else x stays\n\n"
            "Enables Bayesian posterior inference without normalising constants. "
            "Extensions: Gibbs sampling, Hamiltonian MC (HMC), NUTS (used in Stan)."
        ),
    },
    {
        "title": "Taylor Series",
        "category": "Calculus / Mathematics",
        "equation": "f(x) = sum_{n=0}^{inf}  f^(n)(a) / n!  * (x-a)^n",
        "overview": (
            "The Taylor series approximates a smooth function f near point a as an "
            "infinite polynomial using successive derivatives f^(n)(a).\n\n"
            "Common expansions (about a=0, Maclaurin series):\n"
            "  • e^x = 1 + x + x²/2! + x³/3! + ...\n"
            "  • sin(x) = x - x³/3! + x⁵/5! - ...\n"
            "  • cos(x) = 1 - x²/2! + x⁴/4! - ...\n"
            "  • (1+x)^n = 1 + nx + n(n-1)x²/2! + ...  (binomial series)\n\n"
            "Used in numerical methods, deriving loss approximations (second-order "
            "optimisation), and understanding function behaviour near a point."
        ),
    },
    {
        "title": "Euler's Identity",
        "category": "Mathematics",
        "equation": "e^(i*pi) + 1 = 0",
        "overview": (
            "Euler's identity is considered the most beautiful equation in mathematics, "
            "linking five fundamental constants: e, i, pi, 1, and 0.\n\n"
            "It follows from Euler's formula:  e^(i*theta) = cos(theta) + i*sin(theta)\n"
            "Setting theta = pi:  e^(i*pi) = cos(pi) + i*sin(pi) = -1 + 0i = -1\n\n"
            "Geometric interpretation: multiplication by e^(i*theta) rotates a complex "
            "number by theta radians in the complex plane.\n\n"
            "The formula underlies the Fourier transform, quantum mechanics, and "
            "signal processing — making 'imaginary' numbers indispensable."
        ),
    },
    {
        "title": "ANOVA (Analysis of Variance)",
        "category": "Statistics",
        "equation": "F = (SS_between / df_between) / (SS_within / df_within)",
        "overview": (
            "One-way ANOVA tests whether the means of 3+ groups differ significantly "
            "by comparing variance between groups to variance within groups.\n\n"
            "Partitioning of variance:\n"
            "  SS_total = SS_between + SS_within\n"
            "  SS_between: variation explained by group membership\n"
            "  SS_within: unexplained (residual) variation\n\n"
            "F follows an F-distribution under H_0 (all group means equal).  "
            "A large F → reject H_0.\n\n"
            "Assumptions: normality, homoscedasticity (equal variances), independence. "
            "Post-hoc tests (Tukey, Bonferroni) identify which groups differ."
        ),
    },
    {
        "title": "t-test",
        "category": "Statistics",
        "equation": "t = (X_bar - mu_0) / (s / sqrt(n))  ~  t(n-1) under H_0",
        "overview": (
            "The t-test compares a sample mean to a reference value (one-sample), "
            "or compares two group means (two-sample / paired).\n\n"
            "The t-statistic measures how many standard errors the sample mean is from "
            "the null hypothesis value, following a t-distribution with n-1 degrees of "
            "freedom (heavier tails than Normal, reflecting uncertainty about sigma).\n\n"
            "Variants:\n"
            "  • One-sample: compare X_bar to mu_0\n"
            "  • Independent two-sample: compare X_bar_1 and X_bar_2\n"
            "  • Paired: compare differences within matched pairs\n\n"
            "Assumptions: approximately Normal data (or n ≥ 30 by CLT), independence."
        ),
    },
    {
        "title": "Chi-Squared Test",
        "category": "Statistics",
        "equation": "chi^2 = sum_i  (O_i - E_i)^2 / E_i   ~   chi^2(df) under H_0",
        "overview": (
            "The chi-squared test assesses whether observed frequencies O_i differ "
            "significantly from expected frequencies E_i.\n\n"
            "Two main uses:\n"
            "  • Goodness-of-fit: does a variable follow a specified distribution?\n"
            "  • Independence: are two categorical variables independent?\n\n"
            "Degrees of freedom:\n"
            "  • Goodness-of-fit: df = k - 1 - (number of estimated parameters)\n"
            "  • Independence: df = (rows-1) * (cols-1)\n\n"
            "Requires: E_i ≥ 5 in each cell.  Fisher's exact test is preferred for "
            "small samples in 2×2 tables."
        ),
    },
    {
        "title": "Expectation-Maximisation (EM) Algorithm",
        "category": "Statistics / ML",
        "equation": "E-step: Q(theta|theta_t) = E[log p(X,Z|theta) | X, theta_t]\nM-step: theta_{t+1} = argmax Q(theta|theta_t)",
        "overview": (
            "EM finds maximum likelihood estimates in models with latent variables Z "
            "by iterating between two steps until convergence:\n\n"
            "  E-step: compute the expected complete-data log-likelihood Q, given "
            "          current parameters theta_t and observed data X\n"
            "  M-step: maximise Q with respect to theta\n\n"
            "Key property: each iteration never decreases the observed log-likelihood.\n\n"
            "Applications: Gaussian Mixture Models, HMMs (Baum-Welch), missing data "
            "imputation, topic models (LDA), and matrix factorisation."
        ),
    },
    {
        "title": "Hidden Markov Models (HMM)",
        "category": "Statistics / ML",
        "equation": "P(O,Q) = P(q_1)*P(o_1|q_1) * prod_{t=2}^{T} P(q_t|q_{t-1})*P(o_t|q_t)",
        "overview": (
            "An HMM is a Markov chain over hidden states Q with observed emissions O.\n\n"
            "Three fundamental problems:\n"
            "  1. Evaluation: P(O | model) — Forward algorithm  O(N^2 T)\n"
            "  2. Decoding: most likely state sequence — Viterbi algorithm  O(N^2 T)\n"
            "  3. Learning: estimate parameters — Baum-Welch (EM)  algorithm\n\n"
            "Applications: speech recognition (phonemes = hidden states, acoustics = observations), "
            "part-of-speech tagging, gene prediction, gesture recognition."
        ),
    },
    {
        "title": "Mutual Information",
        "category": "Information Theory",
        "equation": "I(X;Y) = H(X) + H(Y) - H(X,Y)  =  H(X) - H(X|Y)",
        "overview": (
            "Mutual information measures how much knowing Y reduces uncertainty about X "
            "(and vice versa).  It is zero if and only if X and Y are independent.\n\n"
            "Properties:\n"
            "  • I(X;Y) = KL( p(x,y) || p(x)*p(y) ) — divergence from independence\n"
            "  • I(X;Y) >= 0,  equals H(X) when Y completely determines X\n"
            "  • Invariant to invertible transformations\n\n"
            "Applications: feature selection, decision trees (information gain), "
            "representation learning (maximise MI between views), causal discovery."
        ),
    },
    {
        "title": "Linear Regression (OLS)",
        "category": "Statistics",
        "equation": "beta_hat = (X^T X)^{-1} X^T y   minimises  ||y - X*beta||^2",
        "overview": (
            "Ordinary Least Squares (OLS) fits a linear model y = X*beta + epsilon by "
            "minimising the sum of squared residuals.\n\n"
            "Gauss–Markov theorem: under assumptions (linearity, exogeneity, no perfect "
            "multicollinearity, homoscedasticity), OLS is BLUE (Best Linear Unbiased Estimator).\n\n"
            "Geometric interpretation: beta_hat projects y onto the column space of X.\n\n"
            "Inference: under normality of errors, (beta_hat - beta) / se ~ t(n-p-1), "
            "enabling hypothesis tests and confidence intervals for coefficients."
        ),
    },
    {
        "title": "Convex Optimisation",
        "category": "Optimisation / Mathematics",
        "equation": "f(lambda*x + (1-lambda)*y) <= lambda*f(x) + (1-lambda)*f(y)  for lambda in [0,1]",
        "overview": (
            "A function is convex if the line segment between any two points lies "
            "above the function.  For convex f and convex feasible set:\n"
            "  • Every local minimum is a global minimum\n"
            "  • The optimality condition grad f(x*) = 0 is sufficient\n\n"
            "Convex problems include: linear programming (LP), quadratic programming (QP), "
            "SOCPs, SDPs, SVMs (dual), Ridge/Lasso regression.\n\n"
            "Algorithms: gradient descent (convergence rate O(1/k)), accelerated GD "
            "(Nesterov, O(1/k²)), Newton's method (quadratic convergence near optimum)."
        ),
    },
    {
        "title": "Reinforcement Learning: Policy Gradient",
        "category": "Reinforcement Learning",
        "equation": "grad_theta J = E_pi[ grad_theta log pi_theta(a|s) * Q^pi(s,a) ]",
        "overview": (
            "Policy gradient methods directly optimise a parameterised policy pi_theta "
            "by ascending the gradient of expected return J.\n\n"
            "REINFORCE (Williams 1992): uses Monte Carlo return G_t as an unbiased but "
            "high-variance estimate of Q^pi.\n\n"
            "Variance reduction:\n"
            "  • Baseline subtraction: Q^pi(s,a) - b(s)  reduces variance without bias\n"
            "  • Actor-Critic: baseline = V^pi(s) estimated by a separate critic network\n\n"
            "PPO (Proximal Policy Optimisation) and TRPO constrain policy updates to "
            "prevent catastrophic changes — standard in RLHF for LLMs."
        ),
    },
    {
        "title": "RLHF: Reinforcement Learning from Human Feedback",
        "category": "ML / LLMs",
        "equation": "Reward model: r_phi(x,y)  -->  PPO: max E[r_phi] - beta*KL(pi||pi_ref)",
        "overview": (
            "RLHF fine-tunes language models to align with human preferences:\n\n"
            "  1. Supervised fine-tuning (SFT) on demonstration data\n"
            "  2. Reward model training on human preference comparisons\n"
            "  3. RL fine-tuning (PPO) to maximise reward while staying close to SFT policy\n\n"
            "The KL penalty prevents reward hacking (exploiting reward model errors).\n\n"
            "Used to train InstructGPT, ChatGPT, Claude, Gemini.  Modern variants include "
            "DPO (Direct Preference Optimisation) which bypasses explicit reward training."
        ),
    },
    {
        "title": "Transformer Architecture",
        "category": "Deep Learning",
        "equation": "x_out = LayerNorm(x + MultiHeadAttn(x))  + LayerNorm(... + FFN(...))",
        "overview": (
            "The Transformer (Vaswani et al., 2017) stacks layers of:\n"
            "  • Multi-Head Self-Attention: each position attends to all others in parallel\n"
            "  • Position-wise Feed-Forward Network (FFN): two linear layers + ReLU\n"
            "  • Residual connections + LayerNorm around each sub-layer\n\n"
            "Positional encoding adds sequence-order information since attention is "
            "permutation-equivariant.\n\n"
            "Encoder-only (BERT), Decoder-only (GPT), Encoder-Decoder (T5) variants "
            "power virtually all state-of-the-art NLP and are adopted in vision, audio, "
            "and scientific AI."
        ),
    },
    {
        "title": "Kalman Filter",
        "category": "Statistics / Signal Processing",
        "equation": (
            "Predict: x_hat_t|t-1 = F*x_hat_{t-1}\n"
            "  Update: x_hat_t = x_hat_t|t-1 + K_t*(z_t - H*x_hat_t|t-1)"
        ),
        "overview": (
            "The Kalman filter is an optimal linear recursive estimator for the state "
            "of a linear dynamical system with Gaussian noise.\n\n"
            "  • F: state transition matrix\n"
            "  • H: observation matrix  \n"
            "  • K_t: Kalman gain (balances predicted state vs. measurement)\n\n"
            "The Kalman gain is chosen to minimise the posterior state covariance, "
            "equivalent to the MMSE estimator.\n\n"
            "Applications: GPS/navigation, missile tracking, autonomous vehicles, "
            "financial signal extraction.  Extended Kalman Filter handles non-linear systems."
        ),
    },
    {
        "title": "Gaussian Processes",
        "category": "Statistics / ML",
        "equation": "f(x) ~ GP(m(x), k(x,x'))  -->  f_*|X,y,X_* ~ N(mu_*, Sigma_*)",
        "overview": (
            "A Gaussian Process defines a distribution over functions; any finite "
            "collection of function values is jointly Gaussian.\n\n"
            "  • Mean function m(x): prior expectation of f\n"
            "  • Kernel k(x,x'): encodes smoothness / similarity assumptions\n\n"
            "Posterior (conditioning on observations) is also Gaussian — analytically "
            "tractable — giving predictions with calibrated uncertainty.\n\n"
            "Applications: Bayesian optimisation (hyperparameter tuning), surrogate "
            "models, spatial interpolation (kriging).  Scales as O(n³) — sparse methods "
            "(inducing points) extend to large datasets."
        ),
    },
    {
        "title": "Information Bottleneck",
        "category": "Information Theory / Deep Learning",
        "equation": "max  I(T;Y) - beta*I(T;X)  where T = compressed representation",
        "overview": (
            "The Information Bottleneck principle (Tishby et al., 2000) finds a "
            "compressed representation T of input X that retains maximal information "
            "about target Y:\n\n"
            "  • I(T;Y): task-relevant information (maximise)\n"
            "  • I(T;X): total information kept from X (minimise / penalise)\n"
            "  • beta controls the compression–relevance trade-off\n\n"
            "Argued to explain how deep networks work: the forward pass compresses "
            "X progressively while preserving Y-relevant structure.  "
            "Connects to rate-distortion theory and representational learning."
        ),
    },
    {
        "title": "Graph Neural Networks (GNN)",
        "category": "Deep Learning",
        "equation": "h_v^{(l+1)} = AGGREGATE( { h_u^{(l)} : u in N(v) } )",
        "overview": (
            "GNNs extend deep learning to graph-structured data by iteratively "
            "aggregating and transforming features from a node's neighbours.\n\n"
            "Key variants:\n"
            "  • GCN (Kipf & Welling): normalised spectral convolution\n"
            "  • GraphSAGE: sample and aggregate (inductive, scales to large graphs)\n"
            "  • GAT (Graph Attention): learn attention weights over neighbours\n"
            "  • Message Passing Neural Networks: general framework\n\n"
            "Applications: molecular property prediction, social network analysis, "
            "knowledge graphs, chip design (AlphaChip), traffic forecasting."
        ),
    },
    {
        "title": "Recurrent Neural Networks & LSTMs",
        "category": "Deep Learning",
        "equation": "h_t = tanh(W_h * h_{t-1} + W_x * x_t + b)",
        "overview": (
            "RNNs process sequential data by maintaining a hidden state h_t that "
            "summarises history up to time t.\n\n"
            "Problem: vanishing/exploding gradients over long sequences.\n\n"
            "LSTM (Long Short-Term Memory) adds a cell state c_t and three gates:\n"
            "  • Forget gate: what to erase from c_{t-1}\n"
            "  • Input gate: what new information to store\n"
            "  • Output gate: what to output as h_t\n\n"
            "GRU (Gated Recurrent Unit) is a simpler two-gate variant.  Both maintain "
            "gradients over hundreds of time steps.  Largely superseded by Transformers "
            "for long-range dependencies but still used in streaming / low-latency settings."
        ),
    },
    {
        "title": "Spectral Graph Theory",
        "category": "Mathematics / Graph Theory",
        "equation": "L = D - A   (Laplacian),   L = U * Lambda * U^T",
        "overview": (
            "The graph Laplacian L = D - A (degree matrix minus adjacency matrix) "
            "encodes graph structure through its eigenvalues and eigenvectors.\n\n"
            "Key properties:\n"
            "  • L is positive semi-definite\n"
            "  • Smallest eigenvalue = 0 (multiplicity = number of connected components)\n"
            "  • Fiedler value (2nd eigenvalue) measures connectivity / mixing time\n\n"
            "Applications:\n"
            "  • Spectral clustering: embed nodes using Fiedler vector, then k-means\n"
            "  • Graph convolutions: filter signals in frequency domain of the graph\n"
            "  • Manifold learning: Laplacian Eigenmaps, Diffusion Maps"
        ),
    },
    {
        "title": "Zipf's Law",
        "category": "Statistics / Linguistics",
        "equation": "f(r) ~ C / r^alpha   (frequency ~ 1/rank for alpha ≈ 1)",
        "overview": (
            "Zipf's Law states that in many natural distributions the frequency of an "
            "item is inversely proportional to its rank: the most common word occurs "
            "~twice as often as the 2nd most common, 3 times the 3rd, etc.\n\n"
            "Observed in: word frequencies in text, city populations, income distributions, "
            "website traffic, gene expression, earthquake magnitudes.\n\n"
            "Mathematically: arises from power laws / heavy-tailed distributions. "
            "Related to Pareto principle (80/20 rule).  "
            "Emergent in self-organised criticality and preferential attachment models."
        ),
    },
    {
        "title": "Bootstrap Resampling",
        "category": "Statistics",
        "equation": "SE_boot = std( { theta_hat_b : b=1,...,B } )  where theta_hat_b from resample",
        "overview": (
            "The bootstrap estimates the sampling distribution of a statistic by "
            "repeatedly resampling with replacement from the observed data.\n\n"
            "Algorithm:\n"
            "  1. Draw B bootstrap samples of size n with replacement from data\n"
            "  2. Compute statistic theta_hat on each bootstrap sample\n"
            "  3. Use the empirical distribution of {theta_hat_b} for inference\n\n"
            "Works without strong distributional assumptions.  "
            "Percentile bootstrap CI: (theta_hat[2.5%], theta_hat[97.5%]).\n\n"
            "Limitations: fails for extreme quantiles and when the estimator is "
            "not smooth; requires computational budget."
        ),
    },
    {
        "title": "PAC Learning",
        "category": "ML Theory",
        "equation": "n >= (1/eps) * ( ln|H| + ln(1/delta) )  samples sufficient for PAC learning",
        "overview": (
            "Probably Approximately Correct (PAC) learning (Valiant 1984) formalises "
            "when a learning algorithm can efficiently find a good hypothesis.\n\n"
            "A concept class is PAC-learnable if, for any eps > 0 and delta > 0, "
            "a polynomial number of samples n suffice to find a hypothesis h with:\n"
            "  P(error(h) > eps) < delta\n\n"
            "VC dimension: the maximum number of points that can be shattered by a "
            "hypothesis class.  Generalisation bound:\n"
            "  error(h) <= error_train(h) + O(sqrt(VC/n))\n\n"
            "Foundation of statistical learning theory, connecting to regularisation "
            "and the bias-variance trade-off."
        ),
    },
    {
        "title": "Attention: Self vs Cross",
        "category": "Deep Learning",
        "equation": (
            "Self-Attention:  Q=K=V=input\n"
            "  Cross-Attention: Q=decoder, K=V=encoder output"
        ),
        "overview": (
            "In self-attention, the queries, keys, and values all derive from the same "
            "input sequence, allowing each token to attend to every other token.\n\n"
            "In cross-attention (used in encoder-decoder Transformers), queries come "
            "from the decoder and keys/values from the encoder, conditioning generation "
            "on the encoded source.\n\n"
            "Causal (masked) self-attention restricts attention to past tokens, "
            "enforcing autoregressive generation in decoder-only models (GPT family).\n\n"
            "Efficient attention variants (Flash Attention, Sparse Attention, Sliding "
            "Window) extend Transformers to long context at reduced memory cost."
        ),
    },
    {
        "title": "Normalising Flows",
        "category": "Deep Learning / Generative Models",
        "equation": "log p(x) = log p(z) + log |det J_f^{-1}(x)|,  z = f(x)",
        "overview": (
            "Normalising flows transform a simple base distribution (e.g. N(0,I)) "
            "into a complex target distribution through a series of invertible, "
            "differentiable transformations.\n\n"
            "The change-of-variables formula tracks the log-density through each "
            "transformation via the log-determinant of the Jacobian.\n\n"
            "Key property: exact likelihood evaluation (unlike GANs/diffusion models).\n\n"
            "Examples: RealNVP, GLOW, neural spline flows, continuous normalising "
            "flows (CNF, ODE-based).  Applications: density estimation, variational "
            "inference, latent variable models."
        ),
    },
    {
        "title": "Contrastive Learning",
        "category": "Self-supervised Learning",
        "equation": "L_NT-Xent = -log( exp(sim(z,z+)/tau) / sum_j exp(sim(z,z_j)/tau) )",
        "overview": (
            "Contrastive learning trains encoders to map similar (positive) pairs close "
            "together and dissimilar (negative) pairs far apart in embedding space.\n\n"
            "SimCLR (Chen et al., 2020): positive pairs are two augmented views of the "
            "same image; negatives are other images in the mini-batch.\n\n"
            "NT-Xent loss: normalised temperature-scaled cross-entropy over positives "
            "vs. all negatives.\n\n"
            "Impact: self-supervised features approaching supervised quality; foundation "
            "for CLIP (image–text contrastive pretraining), MoCo, BYOL, SimCSE."
        ),
    },
    {
        "title": "Sparse Attention & Mixture of Experts",
        "category": "Deep Learning / LLMs",
        "equation": "MoE: y = sum_{i in top-k} G_i(x) * E_i(x),  G = softmax(Wx)[top-k]",
        "overview": (
            "Mixture of Experts (MoE) scales model capacity without proportionally "
            "increasing compute by routing each token to only k of N expert networks.\n\n"
            "  • Router G(x): gates determine which k experts receive each token\n"
            "  • Experts E_i: independent FFN layers (or any module)\n"
            "  • Load balancing loss: prevents routing collapse to few experts\n\n"
            "Models like Mixtral, GPT-4 (rumoured), and Switch Transformer use MoE to "
            "achieve ~8x parameter count at ~2x compute cost vs. a dense model.\n\n"
            "Sparse attention similarly activates only a subset of key-value pairs per "
            "query, reducing Transformer complexity from O(n²) towards O(n log n)."
        ),
    },
    {
        "title": "Causal Inference & Potential Outcomes",
        "category": "Statistics / Causal Inference",
        "equation": "ATE = E[Y(1) - Y(0)]  (Average Treatment Effect)",
        "overview": (
            "The potential outcomes framework (Rubin) defines causal effects in terms of "
            "counterfactuals: Y(1) = outcome if treated, Y(0) = outcome if untreated.\n\n"
            "Fundamental problem: we observe only one potential outcome per unit.\n\n"
            "Identification strategies:\n"
            "  • Randomised controlled trial (RCT): gold standard\n"
            "  • Propensity score matching / weighting: balance observed confounders\n"
            "  • Instrumental variables: exploit exogenous variation\n"
            "  • Difference-in-differences: exploit timing of treatment\n"
            "  • Regression discontinuity: exploit thresholds\n\n"
            "Pearl's do-calculus provides formal rules for reading causal effects from "
            "directed acyclic graphs (DAGs) / structural causal models."
        ),
    },
    {
        "title": "Dimensionality: Curse and Blessing",
        "category": "ML Theory",
        "equation": "Volume of unit ball in d dims --> 0 as d --> inf (radius fixed)",
        "overview": (
            "The curse of dimensionality: in high-dimensional spaces, data becomes "
            "exponentially sparse, distances concentrate, and nearest-neighbour search "
            "degrades.\n\n"
            "Key phenomena:\n"
            "  • Most of the volume of a d-ball is near the surface\n"
            "  • Pairwise distances concentrate: max/min ratio → 1 as d → ∞\n"
            "  • Sampling requires exponentially more points for fixed density\n\n"
            "The 'blessing of dimensionality': deep networks can form complex decision "
            "boundaries that happen to be well-separated in high-d space.  "
            "Random projections preserve distances (Johnson–Lindenstrauss lemma: "
            "n points can be embedded in O(log n / eps²) dims with (1±eps) distortion)."
        ),
    },
    {
        "title": "Attention Sink & Rotary Positional Embeddings",
        "category": "Deep Learning / LLMs",
        "equation": "RoPE: q_m^T k_n = Re( sum_i q_m,2i * k_n,2i * e^{i(m-n)*theta_i} )",
        "overview": (
            "Rotary Position Embeddings (RoPE, Su et al. 2021) encode absolute position "
            "in a way that relative positions appear naturally in the attention dot product.\n\n"
            "Each pair of dimensions is rotated by an angle proportional to position m "
            "and frequency theta_i = 10000^{-2i/d}, so q_m · k_n depends only on m-n.\n\n"
            "Advantages over learned or sinusoidal embeddings:\n"
            "  • Relative position information without explicit bias terms\n"
            "  • Extrapolates to longer contexts than seen in training\n"
            "  • Used in LLaMA, Mistral, Qwen, Falcon, and most modern LLMs\n\n"
            "Attention sink: the first token systematically receives high attention "
            "even when irrelevant, serving as a 'dump' for attention scores."
        ),
    },
    {
        "title": "Cohen's d (Effect Size)",
        "category": "Statistics",
        "equation": "d = (mu_1 - mu_2) / sigma_pooled",
        "overview": (
            "Cohen's d quantifies the standardised difference between two group means, "
            "providing a scale-invariant measure of effect size.\n\n"
            "Interpretation guidelines (Cohen 1988):\n"
            "  • d = 0.2: small effect\n"
            "  • d = 0.5: medium effect\n"
            "  • d = 0.8: large effect\n\n"
            "Why effect size matters: statistical significance (p-value) depends on "
            "sample size — a trivially small difference can be 'significant' with n=10,000. "
            "Effect size measures practical significance.\n\n"
            "Other effect sizes: eta² (ANOVA), r (correlation), odds ratio (binary outcomes)."
        ),
    },
    {
        "title": "Pareto Distribution & Power Laws",
        "category": "Statistics",
        "equation": "P(X > x) = (x_min / x)^alpha  for x >= x_min",
        "overview": (
            "The Pareto distribution is a heavy-tailed power law: the survival function "
            "decays as a power of x rather than exponentially.\n\n"
            "  • Shape alpha > 0 controls tail heaviness\n"
            "  • Mean exists only for alpha > 1; variance for alpha > 2\n"
            "  • Scale-invariant (self-similar): P(X>cx)/P(X>x) independent of x\n\n"
            "Pareto principle (80/20 rule): top 20% account for 80% of outcomes "
            "(corresponds to alpha ≈ 1.16).\n\n"
            "Appears in: wealth distribution, internet traffic, file sizes, social "
            "network degrees, natural language word frequencies (Zipf)."
        ),
    },
    {
        "title": "Variational Inference",
        "category": "Bayesian Statistics / ML",
        "equation": "ELBO = E_q[log p(x,z)] - E_q[log q(z)] = log p(x) - KL(q(z|x)||p(z|x))",
        "overview": (
            "Variational inference (VI) approximates an intractable posterior p(z|x) "
            "with a tractable family q(z|x; phi) by maximising the ELBO.\n\n"
            "Maximising the ELBO simultaneously:\n"
            "  • Maximises the log-evidence log p(x)  (tightens the bound)\n"
            "  • Minimises KL(q||p)  (makes q close to the true posterior)\n\n"
            "Mean-field VI: factorises q(z) = prod_i q_i(z_i) for tractability.\n\n"
            "Amortised VI (VAEs): use neural nets to predict variational parameters "
            "phi(x), enabling efficient per-datapoint inference with gradient descent."
        ),
    },
]


def get_daily_concept() -> dict:
    """Return the concept for today, cycling through the list by day of year."""
    day = date.today().timetuple().tm_yday
    return CONCEPTS[day % len(CONCEPTS)]


# ---------------------------------------------------------------------------
# Discipline-specific concept banks for the Daily Facts tab
# ---------------------------------------------------------------------------

CONCEPTS_AI = [
    {
        "title": "Transformer Self-Attention",
        "category": "AI",
        "equation": "Attention(Q,K,V) = softmax(Q K^T / sqrt(d_k)) V",
        "overview": (
            "The self-attention mechanism is the core building block of Transformer models "
            "(GPT, BERT, etc.).  Each token attends to every other token in the sequence.\n\n"
            "  • Q (queries), K (keys), V (values) are linear projections of the input\n"
            "  • Scaling by sqrt(d_k) prevents softmax saturation in high dimensions\n"
            "  • Multi-head attention runs h parallel attention heads, then concatenates\n\n"
            "Why it matters: unlike RNNs, attention is fully parallelisable and captures "
            "long-range dependencies without vanishing gradients.  It is the reason "
            "large language models scale so effectively."
        ),
    },
    {
        "title": "Reinforcement Learning: Bellman Equation",
        "category": "AI",
        "equation": "V*(s) = max_a [ R(s,a) + gamma * sum_{s'} P(s'|s,a) V*(s') ]",
        "overview": (
            "The Bellman optimality equation defines the value of a state under an optimal "
            "policy: the immediate reward plus discounted future value, maximised over actions.\n\n"
            "  • gamma (0-1): discount factor — how much future rewards are weighted\n"
            "  • P(s'|s,a): transition probability of reaching state s' from s via action a\n"
            "  • V*(s): optimal state-value function\n\n"
            "Q-learning, DQN, and actor-critic methods all derive from this equation.  "
            "Deep RL (AlphaGo, OpenAI Five) approximates V* or Q* with neural networks."
        ),
    },
    {
        "title": "Convolutional Neural Networks",
        "category": "AI",
        "equation": "(I * K)[i,j] = sum_m sum_n  I[i+m, j+n] * K[m,n]",
        "overview": (
            "CNNs apply learned filters (kernels K) via discrete convolution to detect "
            "local spatial patterns — edges, textures, shapes — in a translationally "
            "invariant way.\n\n"
            "Key ideas:\n"
            "  • Parameter sharing: the same kernel is applied at every spatial location\n"
            "  • Pooling layers downsample to build spatial hierarchy\n"
            "  • Deep stacking learns increasingly abstract features\n\n"
            "CNNs revolutionised computer vision (AlexNet 2012) and are now used in "
            "medical imaging, autonomous vehicles, and satellite analysis."
        ),
    },
    {
        "title": "Generative Adversarial Networks (GANs)",
        "category": "AI",
        "equation": "min_G max_D  E[log D(x)] + E[log(1 - D(G(z)))]",
        "overview": (
            "A GAN trains two networks adversarially:\n"
            "  • Generator G: maps random noise z to fake data G(z)\n"
            "  • Discriminator D: tries to distinguish real data x from G(z)\n\n"
            "At Nash equilibrium, G produces samples indistinguishable from real data "
            "and D outputs 0.5 everywhere.\n\n"
            "Applications: photorealistic image synthesis (StyleGAN), data augmentation, "
            "image-to-image translation (pix2pix), video generation.\n\n"
            "Training challenges: mode collapse, vanishing gradients → addressed by "
            "Wasserstein GAN and spectral normalisation."
        ),
    },
    {
        "title": "The Perceptron",
        "category": "AI",
        "equation": "y = sign( w^T x + b )",
        "overview": (
            "The perceptron (Rosenblatt, 1958) is the earliest trainable neural unit.  "
            "It computes a weighted sum of inputs, adds a bias, and applies a step function.\n\n"
            "Learning rule: w <- w + alpha * (y_true - y_pred) * x\n\n"
            "Limitations: can only classify linearly separable data (XOR problem, proven "
            "by Minsky & Papert 1969 — causing the first 'AI winter').\n\n"
            "Multi-layer perceptrons (MLPs) with non-linear activations overcome this, "
            "and every modern deep learning model is a descendant of this idea."
        ),
    },
]

CONCEPTS_STATS = [
    {
        "title": "Bootstrap Resampling",
        "category": "Statistics",
        "equation": "SE_boot = std( { statistic(X*_b) : b = 1..B } )",
        "overview": (
            "The bootstrap estimates the sampling distribution of a statistic by "
            "repeatedly resampling (with replacement) from the observed data.\n\n"
            "Algorithm:\n"
            "  1. Draw B bootstrap samples X*_1, ..., X*_B of size n from the data\n"
            "  2. Compute the statistic (mean, median, correlation, etc.) on each sample\n"
            "  3. The spread of those B values estimates the standard error\n\n"
            "Why it matters: works for almost any statistic without needing closed-form "
            "variance formulas.  95% confidence intervals can be read directly from the "
            "2.5th and 97.5th percentiles of the bootstrap distribution."
        ),
    },
    {
        "title": "p-values and Hypothesis Testing",
        "category": "Statistics",
        "equation": "p = P( |T| >= |t_obs|  |  H_0 true )",
        "overview": (
            "A p-value is the probability of observing a test statistic at least as "
            "extreme as the observed value, assuming the null hypothesis H_0 is true.\n\n"
            "Common misinterpretations:\n"
            "  • p is NOT the probability that H_0 is true\n"
            "  • p < 0.05 is an arbitrary threshold, not a law of nature\n"
            "  • Statistical significance ≠ practical significance\n\n"
            "Better alternatives: report effect sizes, confidence intervals, and use "
            "Bayesian methods (Bayes factors) to quantify evidence for/against H_0."
        ),
    },
    {
        "title": "Markov Chain Monte Carlo (MCMC)",
        "category": "Statistics",
        "equation": "pi(x) prop  L(data|x) * p(x)   sampled via Metropolis-Hastings",
        "overview": (
            "MCMC methods draw samples from a target distribution pi(x) (e.g. a Bayesian "
            "posterior) that is known only up to a normalising constant.\n\n"
            "Metropolis-Hastings:\n"
            "  1. Propose x' from a proposal distribution q(x'|x)\n"
            "  2. Accept with probability min(1, pi(x')/pi(x) * q(x|x')/q(x'|x))\n"
            "  3. Repeat — the chain's stationary distribution is pi\n\n"
            "Used throughout Bayesian statistics, physics (lattice QCD), and ML "
            "(contrastive divergence in RBMs).  Modern variants: HMC, NUTS (used in Stan/PyMC)."
        ),
    },
    {
        "title": "Linear Regression & OLS",
        "category": "Statistics",
        "equation": "beta_hat = (X^T X)^{-1} X^T y",
        "overview": (
            "Ordinary Least Squares (OLS) finds the linear coefficients beta that minimise "
            "the sum of squared residuals between predictions X*beta and observations y.\n\n"
            "Gauss-Markov theorem: under assumptions of linearity, exogeneity, and "
            "homoscedasticity, OLS is BLUE (Best Linear Unbiased Estimator).\n\n"
            "Key diagnostics:\n"
            "  • R^2: fraction of variance explained\n"
            "  • Residual plots: check for heteroscedasticity, non-linearity\n"
            "  • VIF: detect multicollinearity\n\n"
            "Ridge regression adds L2 penalty lambda||beta||^2 to handle collinearity."
        ),
    },
    {
        "title": "Poisson Distribution",
        "category": "Statistics",
        "equation": "P(X = k) = (lambda^k * e^{-lambda}) / k!",
        "overview": (
            "The Poisson distribution models the number of events occurring in a fixed "
            "interval of time/space, given an average rate lambda.\n\n"
            "Properties:\n"
            "  • Mean = Variance = lambda\n"
            "  • Arises as the limit of Binomial(n, p) as n→∞, p→0, np→lambda\n"
            "  • Events must be independent and occur at constant rate\n\n"
            "Applications: website traffic, radioactive decay, insurance claims, "
            "queueing theory, and as the null model for rare genomic mutations."
        ),
    },
]

CONCEPTS_PHYSICS = [
    {
        "title": "Einstein's Field Equations",
        "category": "Physics",
        "equation": "G_{mu nu} + Lambda g_{mu nu} = (8 pi G / c^4) T_{mu nu}",
        "overview": (
            "Einstein's field equations (1915) relate the curvature of spacetime "
            "(left side) to the energy-momentum content of matter (right side).\n\n"
            "  • G_{mu nu}: Einstein tensor — encodes spacetime curvature\n"
            "  • Lambda: cosmological constant (dark energy)\n"
            "  • T_{mu nu}: stress-energy tensor — matter, energy, momentum\n"
            "  • G: Newton's gravitational constant; c: speed of light\n\n"
            "Predictions confirmed: gravitational time dilation, bending of light, "
            "gravitational waves (LIGO 2015), black holes, and the expanding universe."
        ),
    },
    {
        "title": "Schrödinger's Equation",
        "category": "Physics",
        "equation": "i hbar d/dt |psi> = H |psi>",
        "overview": (
            "The time-dependent Schrödinger equation governs how the quantum state |psi> "
            "of a system evolves under Hamiltonian H (total energy operator).\n\n"
            "  • hbar = h/(2 pi): reduced Planck constant\n"
            "  • |psi|^2: probability density of finding a particle at a location\n"
            "  • H = -hbar^2/(2m) nabla^2 + V: kinetic + potential energy\n\n"
            "Solutions (wave functions) describe superpositions of states.  Measurement "
            "collapses the superposition — the central mystery of quantum mechanics.\n\n"
            "Applications: atomic structure, semiconductors, MRI, lasers, quantum computing."
        ),
    },
    {
        "title": "Maxwell's Equations",
        "category": "Physics",
        "equation": "nabla·E = rho/eps0,  nabla×B - mu0 eps0 dE/dt = mu0 J",
        "overview": (
            "Maxwell's four equations (1865) unified electricity, magnetism, and light.\n\n"
            "  1. Gauss's law: electric charges create diverging E fields\n"
            "  2. Gauss's law (magnetism): no magnetic monopoles\n"
            "  3. Faraday's law: changing B induces a curl in E\n"
            "  4. Ampère-Maxwell law: currents and changing E create B\n\n"
            "Maxwell predicted electromagnetic waves travelling at c = 1/sqrt(mu0 eps0) "
            "— the speed of light — unifying optics with electromagnetism.\n\n"
            "Every radio, WiFi, 5G, and optical device is built on these four equations."
        ),
    },
    {
        "title": "The Second Law of Thermodynamics",
        "category": "Physics",
        "equation": "dS >= dQ / T    (entropy of an isolated system never decreases)",
        "overview": (
            "The second law states that the total entropy S of an isolated system can "
            "only increase or remain constant — never decrease spontaneously.\n\n"
            "Interpretations:\n"
            "  • Thermodynamic: heat flows from hot to cold; engines have < 100% efficiency\n"
            "  • Statistical (Boltzmann): S = k_B ln(Omega) — systems evolve toward "
            "    more probable macrostates\n"
            "  • Information: entropy measures missing information\n\n"
            "Implications: the arrow of time, limits of computation (Landauer's principle), "
            "heat death of the universe, and why you can't un-scramble an egg."
        ),
    },
    {
        "title": "Special Relativity: Energy-Mass Equivalence",
        "category": "Physics",
        "equation": "E = gamma m c^2,   E^2 = (pc)^2 + (mc^2)^2",
        "overview": (
            "Einstein's special relativity (1905) showed that mass and energy are "
            "equivalent, related by the speed of light squared.\n\n"
            "  • For a stationary object: E = mc^2\n"
            "  • gamma = 1/sqrt(1 - v^2/c^2): Lorentz factor\n"
            "  • At v = 0: reduces to the famous E = mc^2\n"
            "  • For photons (m=0): E = pc\n\n"
            "Consequences: nuclear energy (fission/fusion convert mass to energy), "
            "GPS corrections for relativistic effects, particle accelerators (LHC), "
            "and the impossibility of reaching c for massive objects."
        ),
    },
]

CONCEPTS_HISTORY = [
    {
        "title": "The Printing Press (c. 1440)",
        "category": "History",
        "equation": "Information copies: scribal (~1/day)  →  press (~3,600/day)",
        "overview": (
            "Gutenberg's movable-type printing press (~1440) was arguably the most "
            "transformative communication technology before the internet.\n\n"
            "Impact:\n"
            "  • Cut the cost of books by ~95% within 50 years\n"
            "  • Enabled mass literacy across Europe\n"
            "  • Spread Reformation ideas faster than the Church could suppress them\n"
            "  • Standardised languages, accelerating national identities\n"
            "  • Catalysed the Scientific Revolution by sharing results rapidly\n\n"
            "By 1500, over 20 million books had been printed — more than all European "
            "scribes had produced in the previous thousand years."
        ),
    },
    {
        "title": "The Industrial Revolution (1760–1840)",
        "category": "History",
        "equation": "UK GDP per capita: ~$1,700 (1760) → ~$3,900 (1840)  [1990 USD]",
        "overview": (
            "The Industrial Revolution, beginning in Britain, was the transition from "
            "agrarian economies to machine-based manufacturing.\n\n"
            "Key drivers:\n"
            "  • Steam engine (Watt, 1769): unlocked mechanical power from coal\n"
            "  • Textile mechanisation: spinning jenny, power loom\n"
            "  • Railways: slashed transport costs, unified national markets\n"
            "  • Factory system: concentrated labour and capital\n\n"
            "Consequences: urbanisation, child labour, the rise of the working class, "
            "trade unionism, and a doubling of life expectancy over the following century.\n\n"
            "Considered the starting point of exponential human economic growth."
        ),
    },
    {
        "title": "The Black Death (1347–1353)",
        "category": "History",
        "equation": "Europe population: ~75M (1347) → ~50M (1353)  (~33% death rate)",
        "overview": (
            "The Black Death (bubonic plague caused by Yersinia pestis) killed an estimated "
            "30-50% of Europe's population in six years — the deadliest pandemic in history.\n\n"
            "Consequences:\n"
            "  • Acute labour shortage → collapse of feudalism; peasant wages tripled\n"
            "  • Church authority undermined (prayers failed) → seeds of the Reformation\n"
            "  • Accelerated development of quarantine practices and public health\n"
            "  • Paradoxically boosted per-capita wealth for survivors\n\n"
            "The plague recurred cyclically until the 18th century and remains endemic "
            "in wildlife populations today, though treatable with modern antibiotics."
        ),
    },
    {
        "title": "The Moon Landing (1969)",
        "category": "History",
        "equation": "Delta-v required: ~9.4 km/s (LEO) + ~3.1 km/s (lunar orbit)",
        "overview": (
            "On July 20, 1969, Apollo 11 landed Neil Armstrong and Buzz Aldrin on the "
            "Moon — the culmination of a decade-long US programme employing 400,000 people.\n\n"
            "Engineering achievements:\n"
            "  • Saturn V: still the most powerful rocket ever flown (7.6M lbf thrust)\n"
            "  • Apollo Guidance Computer: 4KB RAM, 72KB storage — navigated to the Moon\n"
            "  • Lunar Module: first crewed vehicle designed to land on another world\n\n"
            "Context: driven by Cold War competition with the USSR, which had achieved "
            "the first satellite (Sputnik, 1957) and first human in space (Gagarin, 1961).\n\n"
            "Total cost: ~$280 billion in today's dollars."
        ),
    },
    {
        "title": "The French Revolution (1789–1799)",
        "category": "History",
        "equation": "Liberté, Égalité, Fraternité",
        "overview": (
            "The French Revolution dismantled the Ancien Régime, executed a king, and "
            "reshaped the political map of Europe and the world.\n\n"
            "Key causes:\n"
            "  • Fiscal crisis: France bankrupt after American Revolutionary War\n"
            "  • Food shortages: bread prices tripled by 1789\n"
            "  • Enlightenment ideas: Rousseau's social contract, Voltaire's critique of Church\n"
            "  • Resentment of aristocratic privilege by the bourgeoisie\n\n"
            "Legacy:\n"
            "  • Declaration of the Rights of Man (1789): foundational human rights document\n"
            "  • Nationalism as a political force across Europe\n"
            "  • Napoleon Bonaparte: exported revolutionary law across a continent\n"
            "  • Inspired revolutions of 1848 across Europe"
        ),
    },
]

# Ordered list of discipline panels shown on the Daily Facts tab
DISCIPLINE_PANELS = [
    ("AI",      CONCEPTS_AI),
    ("Stats",   CONCEPTS_STATS),
    ("Physics", CONCEPTS_PHYSICS),
    ("History", CONCEPTS_HISTORY),
]


def get_daily_concepts_panel() -> list:
    """Return one concept per discipline for today, cycling independently."""
    day = date.today().timetuple().tm_yday
    return [
        concepts[day % len(concepts)]
        for _, concepts in DISCIPLINE_PANELS
    ]
