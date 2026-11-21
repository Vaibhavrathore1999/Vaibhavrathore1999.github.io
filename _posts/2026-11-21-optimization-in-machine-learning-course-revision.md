---
layout: essay
title: "Optimization in Machine Learning: The Course Revision Guide"
description: "A reference to return to: convexity, convergence proofs, stochastic and adaptive methods, proximal optimization, and the mathematics behind policy gradients and expert routing."
excerpt: "A course-wide CS769 revision reference, with definitions, convergence rates, expandable proofs, worked examples, and self-check questions."
date: 2026-11-21
permalink: /blog/optimization-in-machine-learning-course-revision/
eyebrow: "CS769 · Course revision reference"
topic: mathematics
math: true
native_article: true
course_reference: true
tags: [optimization, revision, convexity, stochastic gradient descent, machine learning]
toc:
  - {id: reading-map, title: "How to use these notes"}
  - {id: toolkit, title: "1. Notation and proof toolkit"}
  - {id: geometry, title: "2. Convex sets and geometry"}
  - {id: convexity, title: "3. Convex functions and calculus"}
  - {id: norms, title: "4. Vector and matrix norms"}
  - {id: subgradients, title: "5. Subgradients and optimality"}
  - {id: regularity, title: "6. Lipschitz, smooth, strongly convex"}
  - {id: losses, title: "7. Classifying ML objectives"}
  - {id: rates, title: "8. Convergence rates at a glance"}
  - {id: gd-proofs, title: "9. Four convergence proofs"}
  - {id: acceleration, title: "10. Momentum and acceleration"}
  - {id: stochastic, title: "11. SGD and variance reduction"}
  - {id: adaptive, title: "12. Adaptive optimizers"}
  - {id: proximal, title: "13. Proximal gradient methods"}
  - {id: second-order, title: "14. Newton, quasi-Newton, CG"}
  - {id: rl, title: "15. Bellman equations and policy gradients"}
  - {id: moe, title: "16. Backpropagation and MoE"}
  - {id: extensions, title: "17. Constraints, duality, structure"}
  - {id: practice, title: "18. Worked revision problems"}
  - {id: checklist, title: "19. Final self-check"}
  - {id: references, title: "References and further reading"}
---

These notes are meant for the moment when the ideas are familiar but the details have started to blur. You remember that smoothness gives a quadratic bound, that strong convexity improves convergence, and that Adam keeps two moving averages—but you want to recover the argument without rereading an entire course.

The aim is to keep the definitions, assumptions, proofs, and examples together. A rate is much easier to remember when you can see which inequality produces it. A counterexample is often more useful than another definition.

This reference grew out of my CS769 Optimization in Machine Learning revision notes for lectures 3–24. It brings together the course themes and supplementary practice material; it is a personal study guide, not an official syllabus or answer key. Repeated questions have been merged by concept, and conditions that compact cheat sheets tend to omit are stated explicitly.

For a gentler first pass through derivatives, gradients, and subgradients, start with [Optimization, Connected: A Revision Guide](/blog/optimization-revision-guide/). This post is the broader reference to come back to afterward.

## How to use these notes
{: #reading-map}

**For a quick pass:** read the definitions in sections 2–7, the rate table in section 8, the optimizer comparison in section 12, and the self-check at the end.

**For proof revision:** work through the toolkit, the four GD proofs, the stochastic extension, and the proximal-gradient proof. Try to reproduce each argument before opening its derivation.

**For applications:** revisit loss classification, policy gradients, MoE routing, and the structured-optimization examples. Ask what each term measures and what assumptions actually hold.

Proofs and solutions are expandable. The controls above let you open them all for a full reading or print the reference with every derivation visible.

## 1. Notation and the proof toolkit
{: #toolkit}

Unless stated otherwise, vectors are in finite-dimensional Euclidean space and <span class="math-inline" markdown="0">\(\&#124;\cdot\&#124;\)</span> is the Euclidean norm. Matrix <span class="math-inline" markdown="0">\(\&#124;A\&#124;_2\)</span> means the spectral norm. Domains are convex when we apply convexity or integrate along a line segment.

| Symbol | Meaning |
| --- | --- |
| <span class="math-inline" markdown="0">\(x^\star\)</span>, <span class="math-inline" markdown="0">\(f^\star\)</span> | A minimizer and its objective value; existence is assumed in rate statements |
| <span class="math-inline" markdown="0">\(R=\&#124;x_0-x^\star\&#124;\)</span> | Initial distance to a chosen minimizer |
| <span class="math-inline" markdown="0">\(g_t\)</span> | A gradient, subgradient, or stochastic estimate, specified in context |
| <span class="math-inline" markdown="0">\(B\)</span> | Bound on subgradient norms, or a stochastic second-moment bound |
| <span class="math-inline" markdown="0">\(L\)</span> | Gradient-Lipschitz constant; the smoothness parameter |
| <span class="math-inline" markdown="0">\(\mu&gt;0\)</span> | Strong-convexity parameter |
| <span class="math-inline" markdown="0">\(\kappa=L/\mu\)</span> | Condition-number bound for a smooth, strongly convex objective |
| <span class="math-inline" markdown="0">\(\eta_t\)</span> | Optimization step size; <span class="math-inline" markdown="0">\(\gamma\)</span> is reserved for RL discounting |
| <span class="math-inline" markdown="0">\(D_t=\&#124;x_t-x^\star\&#124;^2\)</span> | Squared distance used in telescoping proofs |

### The calculus underneath the notation

The gradient collects partial derivatives of a scalar objective. Its differential is <span class="math-inline" markdown="0">\(df=\nabla f(x)^\top dx\)</span>, the linear approximation to the change caused by a displacement. The directional derivative is <span class="math-inline" markdown="0">\(D_vf(x)=\nabla f(x)^\top v\)</span>; a negative value identifies a local descent direction. Among Euclidean unit directions, the negative normalized gradient gives the steepest local decrease when the gradient is nonzero.

A vector-valued function has a Jacobian, with one row per output. A scalar objective has a Hessian of second derivatives; its quadratic form <span class="math-inline" markdown="0">\(v^\top\nabla^2f(x)v\)</span> describes directional curvature. Under the usual convention the scalar Jacobian is the gradient's transpose.

### The identity behind most first-order proofs

For the update <span class="math-inline" markdown="0">\(x_{t+1}=x_t-\eta_tg_t\)</span>,

<div class="math-display" markdown="0">\[
D_{t+1}=D_t-2\eta_tg_t^\top(x_t-x^\star)+\eta_t^2\&#124;g_t\&#124;^2.
\]</div>

Equivalently, for <span class="math-inline" markdown="0">\(\eta_t&gt;0\)</span>,

<div class="math-display" markdown="0">\[
g_t^\top(x_t-x^\star)=\frac{D_t-D_{t+1}}{2\eta_t}+\frac{\eta_t}{2}\&#124;g_t\&#124;^2.
\]</div>

This is algebra. It does not require convexity, smoothness, or even that <span class="math-inline" markdown="0">\(g_t\)</span> be a gradient. The assumptions enter when we bound its two sides.

### Moves worth recognizing immediately

1. **Turn an inner product into distances:** <span class="math-inline" markdown="0">\(2u^\top v=\&#124;u\&#124;^2+\&#124;v\&#124;^2-\&#124;u-v\&#124;^2\)</span>.
2. **Telescope:** <span class="math-inline" markdown="0">\(\sum_{t=0}^{T-1}(a_t-a_{t+1})=a_0-a_T\)</span>. Drop the final term only when its sign allows it.
3. **Optimize a free parameter:** minimize <span class="math-inline" markdown="0">\(R^2/(2\eta T)+\eta B^2/2\)</span> over <span class="math-inline" markdown="0">\(\eta&gt;0\)</span>.
4. **Choose the output:** best objective value is at most the average; convexity transfers an average of values to the value at an averaged iterate. A last-iterate guarantee needs its own justification.
5. **Contract:** <span class="math-inline" markdown="0">\(a_{t+1}\le\rho a_t\)</span> gives <span class="math-inline" markdown="0">\(a_T\le\rho^Ta_0\)</span> for <span class="math-inline" markdown="0">\(0\le\rho&lt;1\)</span>.
6. **Weight before summing:** weights proportional to <span class="math-inline" markdown="0">\(t\)</span> can turn a non-telescoping strongly convex bound into a telescoping one.
7. **Write an inequality both ways and add:** this turns first-order convexity into monotonicity of the gradient.
8. **Restrict to a line:** set <span class="math-inline" markdown="0">\(\phi(t)=f(x+t(y-x))\)</span> and integrate <span class="math-inline" markdown="0">\(\phi'\)</span>.
9. **Add and subtract a cross term:** useful for differences of products and composite expressions.
10. **Condition before taking expectation:** use <span class="math-inline" markdown="0">\(\mathbb E[g_t\mid x_t]=\nabla f(x_t)\)</span>, then the tower rule.
11. **Complete the square:** this reveals a proximal step inside a quadratic model.
12. **Use normalization:** <span class="math-inline" markdown="0">\(\sum_a\nabla\pi(a\mid s)=\nabla1=0\)</span> removes policy-gradient baselines.

**From a rate to an iteration count:** <span class="math-inline" markdown="0">\(RB/\sqrt T\le\epsilon\)</span> requires <span class="math-inline" markdown="0">\(T\ge R^2B^2/\epsilon^2\)</span>. Round up to an integer. Logarithmic formulas should be clipped at zero when the initial bound is already below the requested tolerance.

## 2. Convex sets and the geometry underneath
{: #geometry}

A set <span class="math-inline" markdown="0">\(C\)</span> is convex if every segment between two of its points remains in the set:

<div class="math-display" markdown="0">\[x,y\in C,\quad\theta\in[0,1]\quad\Longrightarrow\quad\theta x+(1-\theta)y\in C.\]</div>

Halfspaces, affine sets, norm balls, and ellipsoids are convex. Intersections preserve convexity; arbitrary unions do not. Two disjoint intervals are the simplest counterexample.

A norm ball is convex because

<div class="math-display" markdown="0">\[
\&#124;\theta(x-c)+(1-\theta)(y-c)\&#124;
\le\theta\&#124;x-c\&#124;+(1-\theta)\&#124;y-c\&#124;.
\]</div>

An ellipsoid can be written either as

<div class="math-display" markdown="0">\[\{x:(x-c)^\top P^{-1}(x-c)\le1\},\qquad P\succ0,\]</div>

or as <span class="math-inline" markdown="0">\(\{c+P^{1/2}u:\&#124;u\&#124;_2\le1\}\)</span>. The second form makes its scaling and rotation explicit.

The **convex hull** of <span class="math-inline" markdown="0">\(S\)</span> is the set of all finite convex combinations <span class="math-inline" markdown="0">\(\sum_i\theta_ix_i\)</span>, where <span class="math-inline" markdown="0">\(x_i\in S\)</span>, <span class="math-inline" markdown="0">\(\theta_i\ge0\)</span>, and <span class="math-inline" markdown="0">\(\sum_i\theta_i=1\)</span>. Combining two such combinations produces another one, so the hull is convex even when <span class="math-inline" markdown="0">\(S\)</span> is not.

### Separation, support, and projection

For two nonempty, disjoint convex sets in finite dimensions, a separating hyperplane gives <span class="math-inline" markdown="0">\(a\ne0\)</span> and <span class="math-inline" markdown="0">\(b\)</span> such that

<div class="math-display" markdown="0">\[a^\top x\le b\le a^\top y\qquad(x\in C,\ y\in D).\]</div>

Strict separation needs additional conditions. A point outside a nonempty closed convex set can be strictly separated from that set.

A supporting hyperplane touches the boundary of a convex set and leaves the set on one side. Applying this geometry to an epigraph explains subgradients—but a supporting plane at a domain boundary may be vertical, so it need not define a finite subgradient.

For a **nonempty closed convex set**, Euclidean projection exists and is unique:

<div class="math-display" markdown="0">\[P_C(z)=\arg\min_{x\in C}\frac12\&#124;x-z\&#124;_2^2.\]</div>

Uniqueness here comes from the strictly convex squared Euclidean distance. It need not hold if Euclidean distance is replaced by an arbitrary norm.

### Sublevel sets, epigraphs, and quasiconvexity

The sublevel set <span class="math-inline" markdown="0">\(L_\alpha(f)=\{x:f(x)\le\alpha\}\)</span> is convex whenever <span class="math-inline" markdown="0">\(f\)</span> is convex. The converse fails: <span class="math-inline" markdown="0">\(f(x)=x^3\)</span> has interval-shaped sublevel sets but is not convex on <span class="math-inline" markdown="0">\(\mathbb R\)</span>.

A function is **quasiconvex** when all its sublevel sets are convex, equivalently

<div class="math-display" markdown="0">\[f(\theta x+(1-\theta)y)\le\max\{f(x),f(y)\}.\]</div>

Another example is <span class="math-inline" markdown="0">\(-e^{-(x-m)^2}\)</span>: its nontrivial sublevel sets are intervals around <span class="math-inline" markdown="0">\(m\)</span>, although its second derivative changes sign. Avoid using <span class="math-inline" markdown="0">\(\log&#124;x&#124;\)</span> on <span class="math-inline" markdown="0">\(\mathbb R\setminus\{0\}\)</span> as an interval example: excluding zero leaves a gap in both the domain and the sublevel sets.

The **epigraph** retains more information:

<div class="math-display" markdown="0">\[\operatorname{epi}f=\{(x,t):t\ge f(x)\}.\]</div>

A function is convex if and only if its epigraph is convex. To prove the reverse direction, take the two epigraph points <span class="math-inline" markdown="0">\((x,f(x))\)</span> and <span class="math-inline" markdown="0">\((y,f(y))\)</span> and apply convexity to their combination.

## 3. Convex functions and the calculus of convexity
{: #convexity}

The defining inequality is

<div class="math-display" markdown="0">\[f(\theta x+(1-\theta)y)\le\theta f(x)+(1-\theta)f(y).\]</div>

Strict convexity replaces <span class="math-inline" markdown="0">\(\le\)</span> by <span class="math-inline" markdown="0">\(&lt;\)</span> for distinct points and <span class="math-inline" markdown="0">\(0&lt;\theta&lt;1\)</span>. Strong convexity asks for a uniform quadratic margin:

<div class="math-display" markdown="0">\[
f(\theta x+(1-\theta)y)\le\theta f(x)+(1-\theta)f(y)
-\frac\mu2\theta(1-\theta)\&#124;x-y\&#124;^2.
\]</div>

Equivalently, <span class="math-inline" markdown="0">\(f(x)-\mu\&#124;x\&#124;^2/2\)</span> is convex. Strong convexity does not require differentiability: hinge loss plus a positive squared Euclidean regularizer is an example.

The identity that connects these definitions is

<div class="math-display" markdown="0">\[\theta\&#124;x\&#124;^2+(1-\theta)\&#124;y\&#124;^2-\&#124;\theta x+(1-\theta)y\&#124;^2=\theta(1-\theta)\&#124;x-y\&#124;^2.\]</div>

### Closure rules

| Construction | Conditions for convexity |
| --- | --- |
| <span class="math-inline" markdown="0">\(\sum_i a_if_i\)</span> | Convex <span class="math-inline" markdown="0">\(f_i\)</span> and <span class="math-inline" markdown="0">\(a_i\ge0\)</span> |
| <span class="math-inline" markdown="0">\(f(Ax+b)\)</span> | Convex <span class="math-inline" markdown="0">\(f\)</span> |
| <span class="math-inline" markdown="0">\(\max_i f_i(x)\)</span> or <span class="math-inline" markdown="0">\(\sup_s f_s(x)\)</span> | Each function convex; respect the effective domain |
| <span class="math-inline" markdown="0">\(h(g(x))\)</span> | Convex nondecreasing <span class="math-inline" markdown="0">\(h\)</span> and convex <span class="math-inline" markdown="0">\(g\)</span>; or convex nonincreasing <span class="math-inline" markdown="0">\(h\)</span> and concave <span class="math-inline" markdown="0">\(g\)</span> |
| <span class="math-inline" markdown="0">\(\inf_{y\in C}F(x,y)\)</span> | Jointly convex <span class="math-inline" markdown="0">\(F\)</span> and convex <span class="math-inline" markdown="0">\(C\)</span>; infimum need not be attained |
| <span class="math-inline" markdown="0">\(t f(x/t)\)</span> | Convex <span class="math-inline" markdown="0">\(f\)</span>, with <span class="math-inline" markdown="0">\(t&gt;0\)</span> and <span class="math-inline" markdown="0">\(x/t\)</span> in its domain |

For a vector-valued inner map, check the outer function's monotonicity separately in every coordinate. For example, log-sum-exp is convex and increasing in each argument, so applying it to convex components preserves convexity.

Monotonicity cannot be dropped from the composition rule: the affine, hence convex, outer function <span class="math-inline" markdown="0">\(h(t)=-t\)</span> composed with <span class="math-inline" markdown="0">\(g(x)=x^2\)</span> gives <span class="math-inline" markdown="0">\(-x^2\)</span>.

### First-order, second-order, and monotonicity tests

For differentiable functions on an open convex domain:

<div class="math-display" markdown="0">\[f\text{ convex}\iff f(y)\ge f(x)+\nabla f(x)^\top(y-x).\]</div>

For twice continuously differentiable functions:

<div class="math-display" markdown="0">\[f\text{ convex}\iff\nabla^2f(x)\succeq0\quad\text{everywhere}.\]</div>

Positive definiteness everywhere is sufficient for strict convexity, but not necessary: <span class="math-inline" markdown="0">\(x^4\)</span> is strictly convex and has zero curvature at zero. Strong convexity is equivalent to <span class="math-inline" markdown="0">\(\nabla^2f(x)\succeq\mu I\)</span> under the same differentiability and domain assumptions.

Convexity also has a gradient characterization:

<div class="math-display" markdown="0">\[ (\nabla f(x)-\nabla f(y))^\top(x-y)\ge0.\]</div>

Strict convexity gives strict inequality for <span class="math-inline" markdown="0">\(x\ne y\)</span>; strong convexity gives the lower bound <span class="math-inline" markdown="0">\(\mu\&#124;x-y\&#124;^2\)</span>.

<details markdown="1" data-proof>
<summary>Derivation: first-order convexity and monotone gradients</summary>

Convexity gives

<div class="math-display" markdown="0">\[\frac{f(x+t(y-x))-f(x)}t\le f(y)-f(x),\qquad0&lt;t\le1.\]</div>

Let <span class="math-inline" markdown="0">\(t\downarrow0\)</span> to get the first-order inequality. Conversely, apply that inequality at <span class="math-inline" markdown="0">\(z=\theta x+(1-\theta)y\)</span> toward both <span class="math-inline" markdown="0">\(x\)</span> and <span class="math-inline" markdown="0">\(y\)</span>, multiply by <span class="math-inline" markdown="0">\(\theta\)</span> and <span class="math-inline" markdown="0">\(1-\theta\)</span>, and add. The gradient terms cancel.

Writing the first-order inequality in both directions and adding gives gradient monotonicity. For the converse, use

<div class="math-display" markdown="0">\[f(y)-f(x)=\int_0^1\nabla f(x+t(y-x))^\top(y-x)\,dt.\]</div>

Monotonicity bounds the integrand below by <span class="math-inline" markdown="0">\(\nabla f(x)^\top(y-x)\)</span>. Strong monotonicity adds <span class="math-inline" markdown="0">\(\mu t\&#124;y-x\&#124;^2\)</span>; its integral gives the required <span class="math-inline" markdown="0">\(\mu/2\)</span> term.

</details>

### Log-sum-exp: a useful test case

Let <span class="math-inline" markdown="0">\(h(z)=\log\sum_i e^{z_i}\)</span> and <span class="math-inline" markdown="0">\(p_i=e^{z_i}/\sum_j e^{z_j}\)</span>. Then

<div class="math-display" markdown="0">\[\nabla h=p,\qquad\nabla^2h=\operatorname{diag}(p)-pp^\top.\]</div>

For any <span class="math-inline" markdown="0">\(v\)</span>,

<div class="math-display" markdown="0">\[v^\top\nabla^2h\,v=\sum_i p_iv_i^2-\left(\sum_i p_iv_i\right)^2=\operatorname{Var}_p(v)\ge0.\]</div>

So log-sum-exp is convex. It is **not strictly convex on the full space**, since <span class="math-inline" markdown="0">\(h(z+c\mathbf1)=h(z)+c\)</span> is affine along the all-ones direction.

<details markdown="1" data-proof>
<summary>Alternative proof: midpoint convexity and Cauchy–Schwarz</summary>

Set <span class="math-inline" markdown="0">\(a_i=e^{x_i/2}\)</span> and <span class="math-inline" markdown="0">\(b_i=e^{y_i/2}\)</span>. Cauchy–Schwarz gives

<div class="math-display" markdown="0">\[\log\sum_i a_ib_i\le\frac12\log\sum_i a_i^2+\frac12\log\sum_i b_i^2.\]</div>

This is the midpoint convexity inequality. Continuity extends it to every mixing weight. Equality holds when <span class="math-inline" markdown="0">\(a\)</span> and <span class="math-inline" markdown="0">\(b\)</span> are proportional, meaning <span class="math-inline" markdown="0">\(x-y=c\mathbf1\)</span>, not just when <span class="math-inline" markdown="0">\(x=y\)</span>.

</details>

## 4. Vector norms, matrix norms, and duality
{: #norms}

A norm satisfies positive definiteness, absolute homogeneity, and the triangle inequality:

<div class="math-display" markdown="0">\[N(x)\ge0,\quad N(x)=0\iff x=0;\qquad N(ax)=&#124;a&#124;N(x);\qquad N(x+y)\le N(x)+N(y).\]</div>

Drop positive definiteness and you get a seminorm. For symmetric <span class="math-inline" markdown="0">\(A\)</span>, <span class="math-inline" markdown="0">\(\sqrt{x^\top Ax}\)</span> is a norm exactly when <span class="math-inline" markdown="0">\(A\succ0\)</span>; a singular PSD matrix gives a seminorm.

Every norm is a convex function and obeys the reverse triangle inequality

<div class="math-display" markdown="0">\[&#124;N(x)-N(y)&#124;\le N(x-y).\]</div>

A norm on a nontrivial vector space is not strictly convex **as a function on the whole space**, because it is linear along positive rays. The separate phrase “strictly convex norm” describes the geometry of its unit sphere; Euclidean norm has that property. Norms are not differentiable at the origin.

The dual norm is

<div class="math-display" markdown="0">\[N_*(z)=\sup_{N(x)\le1}z^\top x,\]</div>

and Hölder's inequality is <span class="math-inline" markdown="0">\(&#124;z^\top x&#124;\le N_*(z)N(x)\)</span>. The pairs are <span class="math-inline" markdown="0">\(\ell_p\leftrightarrow\ell_q\)</span> with <span class="math-inline" markdown="0">\(1/p+1/q=1\)</span>, including <span class="math-inline" markdown="0">\(\ell_1\leftrightarrow\ell_\infty\)</span> and self-dual <span class="math-inline" markdown="0">\(\ell_2\)</span>.

| Matrix quantity | Formula |
| --- | --- |
| Induced norm | <span class="math-inline" markdown="0">\(M_N(A)=\sup_{x\ne0}N(Ax)/N(x)\)</span> |
| Spectral norm | <span class="math-inline" markdown="0">\(\&#124;A\&#124;_2=\sigma_1(A)=\sqrt{\lambda_{\max}(A^\top A)}\)</span> |
| Induced <span class="math-inline" markdown="0">\(\ell_1\)</span> norm | Maximum absolute column sum |
| Induced <span class="math-inline" markdown="0">\(\ell_\infty\)</span> norm | Maximum absolute row sum |
| Frobenius norm | <span class="math-inline" markdown="0">\(\&#124;A\&#124;_F=(\sum_i\sigma_i^2)^{1/2}\)</span> |
| Nuclear norm | <span class="math-inline" markdown="0">\(\&#124;A\&#124;_*=\sum_i\sigma_i\)</span> |
| Schatten <span class="math-inline" markdown="0">\(p\)</span> norm, <span class="math-inline" markdown="0">\(p\ge1\)</span> | <span class="math-inline" markdown="0">\(\&#124;\sigma(A)\&#124;_p\)</span> |
| Ky Fan <span class="math-inline" markdown="0">\(k\)</span> norm | <span class="math-inline" markdown="0">\(\sum_{i=1}^k\sigma_i(A)\)</span> |

Spectral and nuclear norms are dual under the trace inner product <span class="math-inline" markdown="0">\(\langle A,B\rangle=\operatorname{tr}(A^\top B)\)</span>. For rank <span class="math-inline" markdown="0">\(r\)</span>,

<div class="math-display" markdown="0">\[\&#124;A\&#124;_2\le\&#124;A\&#124;_F\le\&#124;A\&#124;_*\le\sqrt r\&#124;A\&#124;_F\le r\&#124;A\&#124;_2.\]</div>

The nuclear norm is the convex envelope of rank **on the spectral-norm unit ball**. The domain restriction matters; it is not an unrestricted identity. See [Fazel's account of rank and cardinality envelopes](https://faculty.washington.edu/mfazel/low-rank-v2.pdf).

<details markdown="1" data-proof>
<summary>Proof template: an induced norm is convex and submultiplicative</summary>

For fixed <span class="math-inline" markdown="0">\(x\ne0\)</span>, use the triangle inequality and homogeneity of <span class="math-inline" markdown="0">\(N\)</span>:

<div class="math-display" markdown="0">\[\frac{N((\theta A+(1-\theta)B)x)}{N(x)}\le\theta\frac{N(Ax)}{N(x)}+(1-\theta)\frac{N(Bx)}{N(x)}.\]</div>

Take the supremum and use <span class="math-inline" markdown="0">\(\sup(a+b)\le\sup a+\sup b\)</span>. This proves convexity without assuming that <span class="math-inline" markdown="0">\(M_N\)</span> is a norm.

Its norm axioms follow similarly: <span class="math-inline" markdown="0">\(M_N(A)=0\)</span> forces <span class="math-inline" markdown="0">\(Ax=0\)</span> for every <span class="math-inline" markdown="0">\(x\)</span>; scalar factors pull out in absolute value; triangle inequality follows from the same supremum argument.

Finally, <span class="math-inline" markdown="0">\(N(ABx)\le M_N(A)N(Bx)\le M_N(A)M_N(B)N(x)\)</span>, so <span class="math-inline" markdown="0">\(M_N(AB)\le M_N(A)M_N(B)\)</span>.

</details>

**Useful counterexamples:** the count of nonzeros and matrix rank fail absolute homogeneity. Squared norm also fails homogeneity of degree one. For <span class="math-inline" markdown="0">\(0&lt;p&lt;1\)</span>, the usual <span class="math-inline" markdown="0">\(\ell_p\)</span> expression fails triangle inequality. Individual singular values <span class="math-inline" markdown="0">\(\sigma_k\)</span> for <span class="math-inline" markdown="0">\(k\ge2\)</span> are not convex, even though their leading partial sums are: <span class="math-inline" markdown="0">\(\sigma_2(\operatorname{diag}(1,0))=\sigma_2(\operatorname{diag}(0,1))=0\)</span>, but <span class="math-inline" markdown="0">\(\sigma_2(I/2)=1/2\)</span>.

## 5. Subgradients, their calculus, and optimality
{: #subgradients}

A convex subgradient supports the function globally from below:

<div class="math-display" markdown="0">\[g\in\partial f(x)\iff f(y)\ge f(x)+g^\top(y-x)\quad\text{for every }y.\]</div>

The subdifferential is a closed convex set, possibly empty. For a proper convex function, it is nonempty at points in the relative interior of its effective domain. At a differentiable interior point, it equals <span class="math-inline" markdown="0">\(\{\nabla f(x)\}\)</span>.

| Function | Subdifferential |
| --- | --- |
| <span class="math-inline" markdown="0">\(&#124;x&#124;\)</span> | <span class="math-inline" markdown="0">\(\{-1\}\)</span> for <span class="math-inline" markdown="0">\(x&lt;0\)</span>; <span class="math-inline" markdown="0">\([-1,1]\)</span> at zero; <span class="math-inline" markdown="0">\(\{1\}\)</span> for <span class="math-inline" markdown="0">\(x&gt;0\)</span> |
| <span class="math-inline" markdown="0">\(\max(0,x)\)</span> | <span class="math-inline" markdown="0">\(\{0\}\)</span> for <span class="math-inline" markdown="0">\(x&lt;0\)</span>; <span class="math-inline" markdown="0">\([0,1]\)</span> at zero; <span class="math-inline" markdown="0">\(\{1\}\)</span> for <span class="math-inline" markdown="0">\(x&gt;0\)</span> |
| <span class="math-inline" markdown="0">\(\&#124;x\&#124;_1\)</span> | Coordinatewise sign away from zero, any value in <span class="math-inline" markdown="0">\([-1,1]\)</span> at zero |
| A norm <span class="math-inline" markdown="0">\(N(x)\)</span> | <span class="math-inline" markdown="0">\(\{z:N_*(z)\le1,\ z^\top x=N(x)\}\)</span> |
| Indicator <span class="math-inline" markdown="0">\(I_C(x)\)</span>, <span class="math-inline" markdown="0">\(x\in C\)</span> | Normal cone <span class="math-inline" markdown="0">\(\{g:g^\top(y-x)\le0\ \forall y\in C\}\)</span> |

For finite convex functions on the full space, the familiar rules are

<div class="math-display" markdown="0">\[\partial(af)=a\partial f\ (a&gt;0),\qquad\partial(f+g)=\partial f+\partial g,\]</div>

<div class="math-display" markdown="0">\[\partial[f(Ax+b)]=A^\top\partial f(Ax+b).\]</div>

For extended-valued functions, the sum and affine-chain equalities need domain qualification conditions, such as appropriate relative-interior intersections. A finite maximum of finite convex functions has

<div class="math-display" markdown="0">\[\partial\max_i f_i(x)=\operatorname{conv}\left(\bigcup_{i\in A(x)}\partial f_i(x)\right),\quad A(x)=\{i:f_i(x)=\max_j f_j(x)\}.\]</div>

Do not transfer this finite-max formula to an arbitrary infinite supremum without checking attainment and regularity.

For a convex outer function <span class="math-inline" markdown="0">\(p\)</span> with a chosen nonnegative subgradient <span class="math-inline" markdown="0">\(a\in\partial p(q(x))\)</span>, and convex inner functions with <span class="math-inline" markdown="0">\(g_i\in\partial q_i(x)\)</span>, the vector <span class="math-inline" markdown="0">\(\sum_i a_ig_i\)</span> is a subgradient of the composition. The nonnegative coefficients let us combine the inner supporting inequalities in the correct direction.

### What certifies a minimum?

For an unconstrained convex objective,

<div class="math-display" markdown="0">\[0\in\partial f(x^\star)\iff x^\star\in\arg\min f.\]</div>

A zero subgradient makes the supporting plane constant. Conversely, the defining inequality for a global minimizer is precisely the subgradient inequality with zero.

Every local minimum of a convex function is global. Strict convexity makes the minimizer unique **if it exists**. It does not prove existence: <span class="math-inline" markdown="0">\(e^x\)</span> is strictly convex and bounded below on <span class="math-inline" markdown="0">\(\mathbb R\)</span>, but never attains its infimum.

A sufficient existence condition is a nonempty **compact** sublevel set together with lower semicontinuity. Boundedness alone is not enough if the domain or sublevel set is not closed.

For differentiable convex <span class="math-inline" markdown="0">\(f\)</span> over a convex feasible set <span class="math-inline" markdown="0">\(C\)</span>,

<div class="math-display" markdown="0">\[x^\star\text{ minimizes }f\text{ over }C\iff\nabla f(x^\star)^\top(x-x^\star)\ge0\quad\forall x\in C.\]</div>

The gradient need not vanish at a constrained optimum. In normal-cone language, <span class="math-inline" markdown="0">\(-\nabla f(x^\star)\in N_C(x^\star)\)</span>.

<details markdown="1" data-proof>
<summary>Two short proofs: local means global; strict means unique</summary>

If a local minimizer <span class="math-inline" markdown="0">\(x\)</span> had a better point <span class="math-inline" markdown="0">\(y\)</span>, a sufficiently small positive <span class="math-inline" markdown="0">\(\theta\)</span> would place <span class="math-inline" markdown="0">\(z=(1-\theta)x+\theta y\)</span> inside its local neighborhood. Convexity would give <span class="math-inline" markdown="0">\(f(z)\le(1-\theta)f(x)+\theta f(y)&lt;f(x)\)</span>, a contradiction.

If a strictly convex function had two distinct minimizers, their midpoint would have a value strictly below the minimum, also a contradiction.

</details>

## 6. Lipschitz continuity, smoothness, and strong convexity
{: #regularity}

These properties bound different things. Keep the function, its gradient, and its curvature separate.

| Property | Definition or characterization |
| --- | --- |
| <span class="math-inline" markdown="0">\(B\)</span>-Lipschitz | <span class="math-inline" markdown="0">\(&#124;f(x)-f(y)&#124;\le B\&#124;x-y\&#124;\)</span> |
| <span class="math-inline" markdown="0">\(L\)</span>-smooth | <span class="math-inline" markdown="0">\(\&#124;\nabla f(x)-\nabla f(y)\&#124;\le L\&#124;x-y\&#124;\)</span> |
| <span class="math-inline" markdown="0">\(\mu\)</span>-strongly convex | <span class="math-inline" markdown="0">\(f(y)\ge f(x)+g^\top(y-x)+\mu\&#124;y-x\&#124;^2/2\)</span> for convex subgradients <span class="math-inline" markdown="0">\(g\)</span> |

On an open convex domain, differentiable <span class="math-inline" markdown="0">\(f\)</span> is <span class="math-inline" markdown="0">\(B\)</span>-Lipschitz exactly when <span class="math-inline" markdown="0">\(\&#124;\nabla f\&#124;\le B\)</span>. The analogous convex-subgradient statement holds at interior points. Boundary normal components can be unbounded, so “every subgradient is bounded” needs this qualification.

For a <span class="math-inline" markdown="0">\(C^2\)</span> function on an open convex domain, smoothness is equivalent to

<div class="math-display" markdown="0">\[-LI\preceq\nabla^2f(x)\preceq LI.\]</div>

For a **convex** function, the lower bound is already zero, and the test simplifies to <span class="math-inline" markdown="0">\(0\preceq\nabla^2f\preceq LI\)</span>. An upper Hessian bound alone is insufficient outside convexity: <span class="math-inline" markdown="0">\(-x^4\)</span> has Hessian <span class="math-inline" markdown="0">\(-12x^2\le L\)</span> for any positive <span class="math-inline" markdown="0">\(L\)</span>, but its gradient is not globally Lipschitz.

Likewise, convexity of <span class="math-inline" markdown="0">\(L\&#124;x\&#124;^2/2-f(x)\)</span> gives a one-sided upper-curvature bound. It characterizes smoothness when <span class="math-inline" markdown="0">\(f\)</span> is also convex; it is not a general replacement for gradient Lipschitzness.

### Examples to keep straight

- <span class="math-inline" markdown="0">\(x^2\)</span> is globally <span class="math-inline" markdown="0">\(2\)</span>-smooth and <span class="math-inline" markdown="0">\(2\)</span>-strongly convex, but not globally Lipschitz.
- <span class="math-inline" markdown="0">\(&#124;x&#124;\)</span> is globally <span class="math-inline" markdown="0">\(1\)</span>-Lipschitz and convex, but nonsmooth.
- <span class="math-inline" markdown="0">\(x^4\)</span> is strictly convex, but neither globally smooth nor strongly convex on <span class="math-inline" markdown="0">\(\mathbb R\)</span>.
- <span class="math-inline" markdown="0">\(&#124;x&#124;^{3/2}\)</span> is differentiable, but its gradient is not Lipschitz near zero.
- <span class="math-inline" markdown="0">\(f(x)=x&#124;x&#124;/2\)</span> has derivative <span class="math-inline" markdown="0">\(&#124;x&#124;\)</span>, so it is <span class="math-inline" markdown="0">\(1\)</span>-smooth even though its second derivative fails to exist at zero.
- For <span class="math-inline" markdown="0">\(f(x)=x^3/3\)</span> on <span class="math-inline" markdown="0">\([-M,M]\)</span>, a tight smoothness constant is <span class="math-inline" markdown="0">\(2M\)</span>.

Global smoothness bounds growth in magnitude by a quadratic relative to a fixed base point. The converse is false: at-most-quadratic growth does not by itself control derivative oscillations. Strong convexity on the full space forces at least quadratic growth, so it is incompatible with global function Lipschitzness there.

**A bounded domain is not enough by itself to give Lipschitzness.** A bounded gradient is enough; continuous differentiability on a neighborhood of a compact convex set is a useful sufficient condition. Differentiability almost everywhere is not enough.

<details markdown="1" data-proof>
<summary>Derivation: the descent lemma and three useful inequalities</summary>

Integrate along the segment from <span class="math-inline" markdown="0">\(x\)</span> to <span class="math-inline" markdown="0">\(y\)</span>:

<div class="math-display" markdown="0">\[
f(y)-f(x)-\nabla f(x)^\top(y-x)
=\int_0^1[\nabla f(x+t(y-x))-\nabla f(x)]^\top(y-x)\,dt.
\]</div>

Cauchy–Schwarz and smoothness bound the integrand above by <span class="math-inline" markdown="0">\(Lt\&#124;y-x\&#124;^2\)</span>. Hence

<div class="math-display" markdown="0">\[f(y)\le f(x)+\nabla f(x)^\top(y-x)+\frac L2\&#124;y-x\&#124;^2.\]</div>

For <span class="math-inline" markdown="0">\(y=x-\nabla f(x)/L\)</span>, this becomes

<div class="math-display" markdown="0">\[f(y)\le f(x)-\frac1{2L}\&#124;\nabla f(x)\&#124;^2.\]</div>

For an unconstrained strongly convex objective, minimize its quadratic lower model to obtain the Polyak–Łojasiewicz inequality:

<div class="math-display" markdown="0">\[\&#124;\nabla f(x)\&#124;^2\ge2\mu(f(x)-f^\star).\]</div>

The smooth descent step gives the complementary inequality <span class="math-inline" markdown="0">\(\&#124;\nabla f(x)\&#124;^2\le2L(f(x)-f^\star)\)</span>. At an unconstrained minimizer, strong convexity also gives quadratic growth:

<div class="math-display" markdown="0">\[f(x)-f^\star\ge\frac\mu2\&#124;x-x^\star\&#124;^2.\]</div>

</details>

For convex <span class="math-inline" markdown="0">\(L\)</span>-smooth functions on <span class="math-inline" markdown="0">\(\mathbb R^d\)</span>, co-coercivity strengthens monotonicity:

<div class="math-display" markdown="0">\[(\nabla f(x)-\nabla f(y))^\top(x-y)\ge\frac1L\&#124;\nabla f(x)-\nabla f(y)\&#124;^2.\]</div>

Sum constants add. If <span class="math-inline" markdown="0">\(h(x)=f(Ax+b)\)</span> and <span class="math-inline" markdown="0">\(f\)</span> is <span class="math-inline" markdown="0">\(L\)</span>-smooth, then <span class="math-inline" markdown="0">\(h\)</span> is <span class="math-inline" markdown="0">\(L\&#124;A\&#124;_2^2\)</span>-smooth: apply the chain rule and the operator-norm bound twice. A product of bounded Lipschitz functions is Lipschitz; the boundedness is essential, as <span class="math-inline" markdown="0">\(x\cdot x\)</span> shows.

## 7. Classifying the objectives used in ML
{: #losses}

The common template is a fit term plus a regularizer:

<div class="math-display" markdown="0">\[\min_w\sum_i\ell(F_w(x_i),y_i)+\lambda\Omega(w).\]</div>

Convexity below refers to linear predictors with fixed features, not arbitrary neural-network parameterizations. Assume finite data, binary labels in <span class="math-inline" markdown="0">\(\{-1,1\}\)</span> where relevant, and positive regularization coefficients. Constants here are for **sums**; divide the data-loss constants by <span class="math-inline" markdown="0">\(n\)</span> for averages.

| Objective | Lipschitz on the full space? | Smooth? | Convexity |
| --- | --- | --- | --- |
| Logistic loss | Yes | Yes | Convex |
| Multiclass linear softmax loss | Yes | Yes | Convex |
| Hinge loss | Yes | Generally no | Convex |
| Nonconstant least squares | Generally no | Yes | Strongly convex iff the design has full column rank |
| Positive squared <span class="math-inline" markdown="0">\(\ell_2\)</span> regularizer | No | Yes | Strongly convex |
| Positive <span class="math-inline" markdown="0">\(\ell_1\)</span> regularizer | Yes | No | Convex |
| Logistic plus squared <span class="math-inline" markdown="0">\(\ell_2\)</span> | No | Yes | Strongly convex |
| Hinge plus squared <span class="math-inline" markdown="0">\(\ell_2\)</span> | No | Generally no | Strongly convex |
| Least squares plus <span class="math-inline" markdown="0">\(\ell_1\)</span> | Generally no | No | Strongly convex iff the design has full column rank |

### Derivatives worth being able to produce

For symmetric <span class="math-inline" markdown="0">\(A\)</span>,

<div class="math-display" markdown="0">\[\nabla(a^\top x)=a,\qquad\nabla(x^\top Ax)=2Ax,\qquad\nabla\frac12\&#124;Ax-b\&#124;^2=A^\top(Ax-b).\]</div>

For nonsymmetric <span class="math-inline" markdown="0">\(A\)</span>, the quadratic gradient is <span class="math-inline" markdown="0">\((A+A^\top)x\)</span>.

**Logistic loss.** Write <span class="math-inline" markdown="0">\(\ell(t)=\log(1+e^t)\)</span>, <span class="math-inline" markdown="0">\(t_i=-y_ix_i^\top w\)</span>. Then <span class="math-inline" markdown="0">\(\ell'=\sigma\)</span> and <span class="math-inline" markdown="0">\(\ell''=\sigma(1-\sigma)\le1/4\)</span>, giving

<div class="math-display" markdown="0">\[\nabla f(w)=-\sum_i\frac{y_ix_i}{1+e^{y_ix_i^\top w}},\qquad0\preceq\nabla^2f(w)\preceq\frac14X^\top X.\]</div>

Valid constants are <span class="math-inline" markdown="0">\(B=\sum_i\&#124;x_i\&#124;\)</span> and <span class="math-inline" markdown="0">\(L=\lambda_{\max}(X^\top X)/4\)</span>. Adding <span class="math-inline" markdown="0">\(\lambda\&#124;w\&#124;^2/2\)</span> adds <span class="math-inline" markdown="0">\(\lambda w\)</span> to the gradient and <span class="math-inline" markdown="0">\(\lambda I\)</span> to the Hessian, giving strong convexity parameter <span class="math-inline" markdown="0">\(\lambda\)</span>.

**Hinge loss.** For one example, <span class="math-inline" markdown="0">\(\max(0,1-yx^\top w)\)</span> has subgradient <span class="math-inline" markdown="0">\(-yx\)</span> below margin one, zero above it, and <span class="math-inline" markdown="0">\(-a yx\)</span> with <span class="math-inline" markdown="0">\(a\in[0,1]\)</span> at the margin. This gives the same simple sum bound <span class="math-inline" markdown="0">\(B=\sum_i\&#124;x_i\&#124;\)</span>.

**Least squares.** For <span class="math-inline" markdown="0">\(f(w)=\&#124;Xw-y\&#124;^2\)</span>,

<div class="math-display" markdown="0">\[\nabla f=2X^\top(Xw-y),\qquad\nabla^2f=2X^\top X.\]</div>

Thus <span class="math-inline" markdown="0">\(L=2\lambda_{\max}(X^\top X)\)</span> and, when positive, <span class="math-inline" markdown="0">\(\mu=2\lambda_{\min}(X^\top X)\)</span>. If <span class="math-inline" markdown="0">\(n&lt;d\)</span>, the Hessian is singular, so there is no global strong convexity. Ridge with objective <span class="math-inline" markdown="0">\(\&#124;Xw-y\&#124;^2+\lambda\&#124;w\&#124;^2\)</span> has

<div class="math-display" markdown="0">\[w^\star=(X^\top X+\lambda I)^{-1}X^\top y.\]</div>

Lasso has no analogous general closed form for an arbitrary design matrix. Soft thresholding is exact for an identity or suitably orthogonal design, and appears as a proximal step more generally.

**Multiclass softmax.** For one sample, <span class="math-inline" markdown="0">\(\ell(z,y)=-z_y+\log\sum_c e^{z_c}\)</span>. Then <span class="math-inline" markdown="0">\(\nabla_z\ell=p-e_y\)</span> and <span class="math-inline" markdown="0">\(\nabla_z^2\ell=\operatorname{diag}(p)-pp^\top\)</span>. The gradient norm is at most <span class="math-inline" markdown="0">\(\sqrt2\)</span> and the Hessian is PSD and bounded. A valid, conservative parameter-space smoothness bound for summed linear-model losses is <span class="math-inline" markdown="0">\(\sum_i\&#124;x_i\&#124;^2\)</span>.

**Other patterns.** Quadratic-over-linear <span class="math-inline" markdown="0">\(x^2/t\)</span> is convex for <span class="math-inline" markdown="0">\(t&gt;0\)</span>: its Hessian is <span class="math-inline" markdown="0">\(2vv^\top/t^3\)</span> with <span class="math-inline" markdown="0">\(v=(t,-x)\)</span>. Log barriers are convex on their positive-slack domain. PCA with an orthogonality constraint is a nonconvex optimization problem even though eigendecomposition solves its standard form exactly. Check both objective and feasible set.

## 8. Convergence rates at a glance
{: #rates}

These are worst-case guarantees with their prescribed outputs, not promises that one optimizer wins on every dataset. Assume a minimizer exists, the stated bounds hold along the iterates, and proximal subproblems are solved exactly. Constrained nonsmooth problems can use projected updates to keep iterates in the region where the bounds apply.

| Problem class and method | Step size | Guaranteed error | Output |
| --- | --- | --- | --- |
| Convex, bounded subgradients | <span class="math-inline" markdown="0">\(R/(B\sqrt T)\)</span> | <span class="math-inline" markdown="0">\(RB/\sqrt T\)</span> | Best or averaged iterate |
| Strongly convex, bounded subgradients | <span class="math-inline" markdown="0">\(2/[\mu(t+1)]\)</span>, <span class="math-inline" markdown="0">\(t\ge1\)</span> | <span class="math-inline" markdown="0">\(2B^2/[\mu(T+1)]\)</span> | Average weighted by <span class="math-inline" markdown="0">\(t\)</span> |
| Convex, <span class="math-inline" markdown="0">\(L\)</span>-smooth GD | <span class="math-inline" markdown="0">\(1/L\)</span> | <span class="math-inline" markdown="0">\(LR^2/(2T)\)</span> | Last iterate |
| Smooth, strongly convex GD | <span class="math-inline" markdown="0">\(1/L\)</span> | <span class="math-inline" markdown="0">\((L/2)(1-\mu/L)^TR^2\)</span> | Last iterate |
| Accelerated smooth convex method | <span class="math-inline" markdown="0">\(1/L\)</span>, prescribed momentum | <span class="math-inline" markdown="0">\(2LR^2/(T+1)^2\)</span> for a standard variant | Algorithm's output iterate |
| Convex composite proximal gradient | <span class="math-inline" markdown="0">\(0&lt;\eta\le1/L\)</span> | <span class="math-inline" markdown="0">\(R^2/(2\eta T)\)</span> | Last iterate |
| Accelerated convex composite method | <span class="math-inline" markdown="0">\(1/L\)</span>, prescribed acceleration | <span class="math-inline" markdown="0">\(2LR^2/(T+1)^2\)</span> | Algorithm's output iterate |

The corresponding tolerance dependence is <span class="math-inline" markdown="0">\(\epsilon^{-2}\)</span>, <span class="math-inline" markdown="0">\(\epsilon^{-1}\)</span>, <span class="math-inline" markdown="0">\(\epsilon^{-1}\)</span>, <span class="math-inline" markdown="0">\(\log(1/\epsilon)\)</span>, <span class="math-inline" markdown="0">\(\epsilon^{-1/2}\)</span>, <span class="math-inline" markdown="0">\(\epsilon^{-1}\)</span>, and <span class="math-inline" markdown="0">\(\epsilon^{-1/2}\)</span>, respectively. Constants and assumptions still matter.

For <span class="math-inline" markdown="0">\(R=2\)</span>, <span class="math-inline" markdown="0">\(B=3\)</span>, <span class="math-inline" markdown="0">\(L=5\)</span>, and <span class="math-inline" markdown="0">\(\epsilon=0.01\)</span>, the first bound asks for <span class="math-inline" markdown="0">\(360{,}000\)</span> steps; smooth GD asks for <span class="math-inline" markdown="0">\(1{,}000\)</span>. These are sufficient theoretical counts, not measured runtimes.

In the black-box first-order oracle model, with suitable dimension and problem-class assumptions, the characteristic worst-case lower rates are <span class="math-inline" markdown="0">\(T^{-1/2}\)</span> for Lipschitz convex objectives and <span class="math-inline" markdown="0">\(T^{-2}\)</span> for smooth convex objectives. Acceleration closes the smooth-class gap left by ordinary GD. A lower bound for a problem class is not a lower bound on every individual instance.

## 9. Four convergence proofs to reconstruct from memory
{: #gd-proofs}

All four proofs reuse the distance identity. What changes is the inequality used to control the inner product and gradient norm.

### A. Convexity and bounded subgradients

Convexity gives <span class="math-inline" markdown="0">\(f(x_t)-f^\star\le g_t^\top(x_t-x^\star)\)</span>. If <span class="math-inline" markdown="0">\(\&#124;g_t\&#124;\le B\)</span>, then for fixed <span class="math-inline" markdown="0">\(\eta&gt;0\)</span>,

<div class="math-display" markdown="0">\[\frac1T\sum_{t=0}^{T-1}(f(x_t)-f^\star)\le\frac{R^2}{2\eta T}+\frac{\eta B^2}{2}.\]</div>

Choose <span class="math-inline" markdown="0">\(\eta=R/(B\sqrt T)\)</span> to get <span class="math-inline" markdown="0">\(RB/\sqrt T\)</span>, assuming <span class="math-inline" markdown="0">\(R,B&gt;0\)</span>. If either is zero, handle that trivial case separately.

<details markdown="1" data-proof>
<summary>Proof A: telescope, tune the step, and choose an output</summary>

Substitute convexity into the identity and sum:

<div class="math-display" markdown="0">\[\sum_{t=0}^{T-1}(f(x_t)-f^\star)\le\frac{D_0-D_T}{2\eta}+\frac\eta2\sum_{t=0}^{T-1}\&#124;g_t\&#124;^2\le\frac{R^2}{2\eta}+\frac{\eta TB^2}{2}.\]</div>

Divide by <span class="math-inline" markdown="0">\(T\)</span>. Differentiating the bound with respect to <span class="math-inline" markdown="0">\(\eta\)</span> gives <span class="math-inline" markdown="0">\(-R^2/(2T\eta^2)+B^2/2=0\)</span>, hence the stated step size.

The best iterate is no worse than the average value. For <span class="math-inline" markdown="0">\(\bar x=T^{-1}\sum_{t=0}^{T-1}x_t\)</span>, Jensen gives <span class="math-inline" markdown="0">\(f(\bar x)\le T^{-1}\sum_t f(x_t)\)</span>. Neither argument certifies the last iterate.

A fixed, untuned step leaves the bound <span class="math-inline" markdown="0">\(\eta B^2/2\)</span> as <span class="math-inline" markdown="0">\(T\)</span> grows. That is a floor in the guarantee, not a claim that every problem actually stalls there.

</details>

With varying steps, multiply by <span class="math-inline" markdown="0">\(2\eta_t\)</span> before summing:

<div class="math-display" markdown="0">\[\min_{0\le t&lt;T}(f(x_t)-f^\star)\le\frac{R^2+B^2\sum_t\eta_t^2}{2\sum_t\eta_t}.\]</div>

The same bound holds for the step-weighted average by Jensen. Conditions <span class="math-inline" markdown="0">\(\sum_t\eta_t=\infty\)</span> and <span class="math-inline" markdown="0">\(\sum_t\eta_t^2&lt;\infty\)</span> make this bound vanish. The schedule <span class="math-inline" markdown="0">\(\eta_t\propto1/\sqrt{t+1}\)</span> does not have a finite square sum, but the displayed bound still gives <span class="math-inline" markdown="0">\(O(\log T/\sqrt T)\)</span>.

### B. Convexity and smoothness

The descent lemma gives, for <span class="math-inline" markdown="0">\(g_t=\nabla f(x_t)\)</span>,

<div class="math-display" markdown="0">\[f(x_{t+1})\le f(x_t)-\eta\left(1-\frac{L\eta}{2}\right)\&#124;g_t\&#124;^2.\]</div>

At <span class="math-inline" markdown="0">\(\eta=1/L\)</span>, the decrease is at least <span class="math-inline" markdown="0">\(\&#124;g_t\&#124;^2/(2L)\)</span>. This replaces the bounded-gradient assumption in Proof A.

<details markdown="1" data-proof>
<summary>Proof B: use descent to remove the gradient-norm sum</summary>

Smoothness telescopes to

<div class="math-display" markdown="0">\[\frac1{2L}\sum_{t=0}^{T-1}\&#124;g_t\&#124;^2\le f(x_0)-f(x_T).\]</div>

The distance identity and convexity give

<div class="math-display" markdown="0">\[\sum_{t=0}^{T-1}(f(x_t)-f^\star)\le\frac L2R^2+\frac1{2L}\sum_t\&#124;g_t\&#124;^2.\]</div>

Substitute the first inequality and move <span class="math-inline" markdown="0">\(f(x_0)-f(x_T)\)</span> to the left. The index shift is the key step:

<div class="math-display" markdown="0">\[\sum_{t=1}^{T}(f(x_t)-f^\star)\le\frac L2R^2.\]</div>

Objective values decrease, so the last value is at most this average:

<div class="math-display" markdown="0">\[f(x_T)-f^\star\le\frac{LR^2}{2T}.\]</div>

For <span class="math-inline" markdown="0">\(0&lt;\eta\le1/L\)</span>, the same argument gives <span class="math-inline" markdown="0">\(R^2/(2\eta T)\)</span>. Strict decrease away from stationarity is guaranteed for <span class="math-inline" markdown="0">\(0&lt;\eta&lt;2/L\)</span>, but the displayed rate proof uses the smaller range.

</details>

**Without convexity**, descent still gives a stationarity guarantee for a lower-bounded smooth function:

<div class="math-display" markdown="0">\[\min_{0\le t&lt;T}\&#124;\nabla f(x_t)\&#124;^2\le\frac{2L(f(x_0)-f_{\inf})}{T}.\]</div>

Small gradient is not a certificate of global optimality and can occur near a saddle.

### C. Smoothness and strong convexity

Strong convexity strengthens the inner-product bound:

<div class="math-display" markdown="0">\[g_t^\top(x_t-x^\star)\ge f(x_t)-f^\star+\frac\mu2D_t.\]</div>

At <span class="math-inline" markdown="0">\(\eta=1/L\)</span>, it leads to

<div class="math-display" markdown="0">\[D_{t+1}\le(1-\mu/L)D_t.\]</div>

<details markdown="1" data-proof>
<summary>Proof C: the contraction argument and a shorter function-value proof</summary>

Insert the strengthened inequality into the distance update:

<div class="math-display" markdown="0">\[D_{t+1}\le(1-\mu\eta)D_t+2\eta(f^\star-f(x_t))+\eta^2\&#124;g_t\&#124;^2.\]</div>

At <span class="math-inline" markdown="0">\(\eta=1/L\)</span>, sufficient decrease and <span class="math-inline" markdown="0">\(f^\star\le f(x_{t+1})\)</span> make the last two terms nonpositive. Iteration gives <span class="math-inline" markdown="0">\(D_T\le(1-\mu/L)^TR^2\)</span>.

Smoothness at <span class="math-inline" markdown="0">\(x^\star\)</span>, where the unconstrained gradient is zero, gives

<div class="math-display" markdown="0">\[f(x_T)-f^\star\le\frac L2D_T\le\frac L2(1-\mu/L)^TR^2.\]</div>

Since <span class="math-inline" markdown="0">\(1-u\le e^{-u}\)</span>, a sufficient count is

<div class="math-display" markdown="0">\[T\ge\frac L\mu\log\frac{LR^2}{2\epsilon}.\]</div>

A shorter proof uses PL directly:

<div class="math-display" markdown="0">\[f(x_{t+1})-f^\star\le f(x_t)-f^\star-\frac1{2L}\&#124;g_t\&#124;^2\le(1-\mu/L)(f(x_t)-f^\star).\]</div>

This version only needs smoothness and the PL inequality, which some nonconvex functions also satisfy.

</details>

The squared-distance bound gives a distance contraction factor <span class="math-inline" markdown="0">\(\sqrt{1-\mu/L}\)</span>. “Linear convergence” refers to geometric error decay, not to a linearly shrinking error. Reducing the tolerance tenfold adds about <span class="math-inline" markdown="0">\(\kappa\log10\)</span> iterations in the exponential bound.

### D. Strong convexity and bounded subgradients

For nonsmooth strongly convex objectives, assume <span class="math-inline" markdown="0">\(\&#124;g_t\&#124;\le B\)</span> along the iterates. This can hold on a bounded feasible region with projected updates; it cannot hold globally for a strongly convex function on the entire space.

Use <span class="math-inline" markdown="0">\(\eta_t=2/[\mu(t+1)]\)</span> for <span class="math-inline" markdown="0">\(t=1,\ldots,T\)</span> and output

<div class="math-display" markdown="0">\[\bar x_T=\frac{2}{T(T+1)}\sum_{t=1}^Tt x_t.\]</div>

Then

<div class="math-display" markdown="0">\[f(\bar x_T)-f^\star\le\frac{2B^2}{\mu(T+1)}.\]</div>

<details markdown="1" data-proof>
<summary>Proof D: why weighting by time removes the logarithm</summary>

The one-step relation is

<div class="math-display" markdown="0">\[f(x_t)-f^\star\le\frac{\eta_tB^2}{2}+\left(\frac1{2\eta_t}-\frac\mu2\right)D_t-\frac1{2\eta_t}D_{t+1}.\]</div>

Substitute the schedule and multiply by <span class="math-inline" markdown="0">\(t\)</span>:

<div class="math-display" markdown="0">\[t(f(x_t)-f^\star)\le\frac{B^2}{\mu}+\frac\mu4\left[t(t-1)D_t-t(t+1)D_{t+1}\right].\]</div>

The distance terms telescope from <span class="math-inline" markdown="0">\(t=1\)</span> to <span class="math-inline" markdown="0">\(T\)</span>. The initial coefficient is zero, and the final term is nonpositive. Thus <span class="math-inline" markdown="0">\(\sum_t t(f(x_t)-f^\star)\le TB^2/\mu\)</span>.

Normalize by <span class="math-inline" markdown="0">\(T(T+1)/2\)</span> and apply Jensen. This explains both the <span class="math-inline" markdown="0">\(1/T\)</span> rate and the absence of an initial-distance term in this particular bound. A common unweighted analysis with <span class="math-inline" markdown="0">\(\eta_t=1/(\mu t)\)</span> instead produces a <span class="math-inline" markdown="0">\(\log T/T\)</span> term.

The same distance inequality survives Euclidean projection because projection cannot increase distance to a feasible minimizer.

</details>

## 10. Momentum, acceleration, and step-size selection
{: #acceleration}

Heavy-ball momentum keeps a velocity:

<div class="math-display" markdown="0">\[v_{t+1}=\beta v_t-\eta\nabla f(x_t),\qquad x_{t+1}=x_t+v_{t+1}.\]</div>

Equivalently, <span class="math-inline" markdown="0">\(x_{t+1}=x_t-\eta\nabla f(x_t)+\beta(x_t-x_{t-1})\)</span>. Gradients that repeatedly point in similar directions accumulate movement. Stability depends on the objective, step size, and momentum together; <span class="math-inline" markdown="0">\(0\le\beta&lt;1\)</span> alone is not a convergence theorem.

For positive-definite quadratics, the classical tuned parameters are

<div class="math-display" markdown="0">\[\eta=\frac4{(\sqrt L+\sqrt\mu)^2},\qquad\beta=\left(\frac{\sqrt L-\sqrt\mu}{\sqrt L+\sqrt\mu}\right)^2.\]</div>

Do not promote the quadratic result to a universal accelerated guarantee for all smooth strongly convex objectives. Results beyond quadratics require additional analysis; see [Wang et al. on heavy-ball acceleration beyond quadratics](https://proceedings.mlr.press/v162/wang22p.html).

### A standard accelerated convex scheme

Initialize <span class="math-inline" markdown="0">\(x_0\)</span>, <span class="math-inline" markdown="0">\(y_0=x_0\)</span>, and <span class="math-inline" markdown="0">\(a_0=1\)</span>. For <span class="math-inline" markdown="0">\(t\ge0\)</span>,

<div class="math-display" markdown="0">\[
\begin{aligned}
x_{t+1}&amp;=y_t-\frac1L\nabla f(y_t),\\
a_{t+1}&amp;=\frac{1+\sqrt{1+4a_t^2}}2,\\
y_{t+1}&amp;=x_{t+1}+\frac{a_t-1}{a_{t+1}}(x_{t+1}-x_t).
\end{aligned}
\]</div>

For convex <span class="math-inline" markdown="0">\(L\)</span>-smooth objectives this gives the characteristic <span class="math-inline" markdown="0">\(O(LR^2/T^2)\)</span> guarantee. Evaluating the gradient at the extrapolated point is central. An arbitrary fixed momentum coefficient is not interchangeable with the schedule in the theorem. Accelerated objective values need not decrease every step.

### Line search

For a descent direction <span class="math-inline" markdown="0">\(d\)</span>, Armijo backtracking seeks

<div class="math-display" markdown="0">\[f(x+\eta d)\le f(x)+c_1\eta\nabla f(x)^\top d,\qquad0&lt;c_1&lt;1.\]</div>

Strong Wolfe additionally requires

<div class="math-display" markdown="0">\[&#124;\nabla f(x+\eta d)^\top d&#124;\le c_2&#124;\nabla f(x)^\top d&#124;,\qquad c_1&lt;c_2&lt;1.\]</div>

These conditions are useful for smooth objectives. They are not a direct replacement for a horizon-tuned nonsmooth subgradient schedule.

## 11. Stochastic gradients and variance reduction
{: #stochastic}

For <span class="math-inline" markdown="0">\(f(w)=n^{-1}\sum_i f_i(w)\)</span>, uniformly sampling <span class="math-inline" markdown="0">\(i_t\)</span> gives the unbiased estimate <span class="math-inline" markdown="0">\(g_t=\nabla f_{i_t}(w_t)\)</span>. One sample gradient usually costs much less than all <span class="math-inline" markdown="0">\(n\)</span> gradients, although actual speedup depends on batching and hardware.

The key statement is conditional:

<div class="math-display" markdown="0">\[\mathbb E[g_t\mid w_t]=\nabla f(w_t).\]</div>

A single sampled gradient need not satisfy the full objective's supporting inequality. Its conditional expectation does.

<details markdown="1" data-proof>
<summary>SGD proof: exactly where the expectation enters</summary>

The distance identity holds for the random vector <span class="math-inline" markdown="0">\(g_t\)</span>. By the tower rule,

<div class="math-display" markdown="0">\[\mathbb E[g_t^\top(w_t-w^\star)]=\mathbb E[\nabla f(w_t)^\top(w_t-w^\star)]\ge\mathbb E[f(w_t)]-f^\star.\]</div>

If <span class="math-inline" markdown="0">\(\mathbb E\&#124;g_t\&#124;^2\le B^2\)</span>, taking expectations and telescoping gives

<div class="math-display" markdown="0">\[\frac1T\sum_{t=0}^{T-1}(\mathbb E f(w_t)-f^\star)\le\frac{R^2}{2\eta T}+\frac{\eta B^2}{2}.\]</div>

The same tuning yields <span class="math-inline" markdown="0">\(RB/\sqrt T\)</span> for an averaged iterate in expectation. Strong convexity and the time-weighted proof give <span class="math-inline" markdown="0">\(2B^2/[\mu(T+1)]\)</span> under the corresponding moment and feasibility assumptions.

Do not substitute a variance bound <span class="math-inline" markdown="0">\(\mathbb E\&#124;g_t-\nabla f(w_t)\&#124;^2\le\sigma^2\)</span> for a second-moment bound without also controlling the gradient norm.

</details>

### Mini-batches

For <span class="math-inline" markdown="0">\(m\)</span> conditionally independent samples with variance <span class="math-inline" markdown="0">\(\sigma^2\)</span>, the mean has variance <span class="math-inline" markdown="0">\(\sigma^2/m\)</span>. Write the centered errors as <span class="math-inline" markdown="0">\(e_j\)</span>; independence and zero mean kill cross terms in <span class="math-inline" markdown="0">\(\mathbb E\&#124;m^{-1}\sum_j e_j\&#124;^2\)</span>.

Sampling without replacement has a finite-population correction. Taking <span class="math-inline" markdown="0">\(m=n\)</span> recovers the full gradient when every sample is used exactly once; drawing <span class="math-inline" markdown="0">\(n\)</span> samples with replacement does not make the variance vanish.

### SAG, SAGA, and SVRG

SAG stores a previous gradient for each sample, refreshes one, and steps using the average of the stored values. Its estimator is generally biased, but its memory permits linear convergence under appropriate smooth finite-sum strong-convexity assumptions. Generic storage is <span class="math-inline" markdown="0">\(O(nd)\)</span>; some linear models only need one scalar per sample.

SAGA also keeps a gradient table but uses an unbiased correction. SVRG uses a snapshot <span class="math-inline" markdown="0">\(\tilde w\)</span> and full snapshot gradient <span class="math-inline" markdown="0">\(\tilde\mu=\nabla f(\tilde w)\)</span>:

<div class="math-display" markdown="0">\[v_t=\nabla f_{i_t}(w_t)-\nabla f_{i_t}(\tilde w)+\tilde\mu.\]</div>

Its expectation is <span class="math-inline" markdown="0">\(\nabla f(w_t)\)</span>. It avoids storing all <span class="math-inline" markdown="0">\(n\)</span> gradients, at the cost of snapshot passes and recomputation. As both points approach a common optimum, the correction's noise can vanish. These linear-rate results are stronger than generic noisy SGD's <span class="math-inline" markdown="0">\(O(1/T)\)</span> strongly convex guarantee, but they use extra finite-sum structure.

SGD's noise can help leave some unstable regions; it does not guarantee escape from every local minimum or saddle. Nor does SGD universally generalize better than every adaptive optimizer.

## 12. Adaptive optimizers: what is remembered?
{: #adaptive}

Adaptive methods rescale coordinates using gradient history. They still have hyperparameters, and their guarantees depend on the objective and update details. All operations below are coordinatewise; a small <span class="math-inline" markdown="0">\(\varepsilon&gt;0\)</span> prevents division by zero.

| Method | Memory | Update idea |
| --- | --- | --- |
| SGD | None | <span class="math-inline" markdown="0">\(w_{t+1}=w_t-\alpha_tg_t\)</span> |
| Heavy ball | Past velocity | Add momentum to the gradient step |
| AdaGrad | Sum of all squared gradients | Divide by the square root of accumulated squares |
| RMSProp | Exponential average of squares | Downweight older squared gradients |
| Adam | Exponential averages of gradients and squares | Bias-correct both, then divide |
| AMSGrad | Adam-like moments plus a running maximum | Prevent the second-moment denominator from shrinking |

**AdaGrad:** <span class="math-inline" markdown="0">\(s_t=s_{t-1}+g_t\odot g_t\)</span> and <span class="math-inline" markdown="0">\(w_{t+1}=w_t-\alpha g_t/(\sqrt{s_t}+\varepsilon)\)</span>. Rarely updated coordinates retain larger effective steps. For a constant nonzero gradient magnitude and negligible <span class="math-inline" markdown="0">\(\varepsilon\)</span>, the update magnitude decays as <span class="math-inline" markdown="0">\(\alpha/\sqrt t\)</span>.

**RMSProp:** <span class="math-inline" markdown="0">\(v_t=\beta_2v_{t-1}+(1-\beta_2)g_t\odot g_t\)</span>. Use <span class="math-inline" markdown="0">\(w_{t+1}=w_t-\alpha g_t/(\sqrt{v_t}+\varepsilon)\)</span>. Under a constant squared gradient <span class="math-inline" markdown="0">\(c^2\)</span>, <span class="math-inline" markdown="0">\(v_t=c^2(1-\beta_2^t)\to c^2\)</span>; unlike AdaGrad's accumulator it does not grow indefinitely in this example.

**Adam**, with <span class="math-inline" markdown="0">\(m_0=v_0=0\)</span>:

<div class="math-display" markdown="0">\[
\begin{aligned}
m_t&amp;=\beta_1m_{t-1}+(1-\beta_1)g_t,\\
v_t&amp;=\beta_2v_{t-1}+(1-\beta_2)g_t\odot g_t,\\
\hat m_t&amp;=m_t/(1-\beta_1^t),\qquad\hat v_t=v_t/(1-\beta_2^t),\\
w_{t+1}&amp;=w_t-\alpha_t\hat m_t/(\sqrt{\hat v_t}+\varepsilon).
\end{aligned}
\]</div>

The second moment is a mean of squared gradients, not the centered variance. Bias correction removes the effect of zero initialization on an exponentially weighted history. It does not make a history of changing gradients an unbiased estimate of the current gradient.

<details markdown="1" data-proof>
<summary>Derivation: moving averages and bias correction</summary>

Unroll the first moment:

<div class="math-display" markdown="0">\[m_t=(1-\beta_1)\sum_{s=1}^t\beta_1^{t-s}g_s.\]</div>

The weights sum to <span class="math-inline" markdown="0">\(1-\beta_1^t\)</span>. If all gradients have the same mean <span class="math-inline" markdown="0">\(g\)</span>, then <span class="math-inline" markdown="0">\(\mathbb E[m_t]=(1-\beta_1^t)g\)</span>, so division removes that initialization bias. The squared-gradient argument is identical under a constant second-moment assumption.

If you write a recurrence directly for the corrected second moment, it is

<div class="math-display" markdown="0">\[\hat v_t=\frac{\beta_2(1-\beta_2^{t-1})}{1-\beta_2^t}\hat v_{t-1}+\frac{1-\beta_2}{1-\beta_2^t}g_t^2.\]</div>

Applying the raw-moment recurrence to <span class="math-inline" markdown="0">\(\hat v_{t-1}\)</span> and then dividing again would double-correct it.

</details>

### A two-step numerical check

Let <span class="math-inline" markdown="0">\(g_1=(2,4)\)</span>, <span class="math-inline" markdown="0">\(g_2=(4,2)\)</span>, and <span class="math-inline" markdown="0">\(\alpha=0.1\)</span>. Ignore <span class="math-inline" markdown="0">\(\varepsilon\)</span>. Use <span class="math-inline" markdown="0">\(\beta_2=0.9\)</span> for RMSProp and <span class="math-inline" markdown="0">\((\beta_1,\beta_2)=(0.9,0.999)\)</span> for Adam.

| Method | State after step 2 | Magnitude of update 2 |
| --- | --- | --- |
| AdaGrad | <span class="math-inline" markdown="0">\(s_2=(20,20)\)</span> | <span class="math-inline" markdown="0">\((0.0894,0.0447)\)</span> |
| RMSProp | <span class="math-inline" markdown="0">\(v_2=(1.96,1.84)\)</span> | <span class="math-inline" markdown="0">\((0.2857,0.1474)\)</span> |
| Adam | <span class="math-inline" markdown="0">\(m_2=(0.58,0.56)\)</span>; <span class="math-inline" markdown="0">\(v_2=(0.019996,0.019984)\)</span> | Approximately <span class="math-inline" markdown="0">\((0.0965,0.0932)\)</span> |

For Adam, divide by <span class="math-inline" markdown="0">\(1-0.9^2=0.19\)</span> and <span class="math-inline" markdown="0">\(1-0.999^2=0.001999\)</span> before taking the update. At the first step, AdaGrad and Adam each move by <span class="math-inline" markdown="0">\(0.1\)</span> in these positive coordinates; uncorrected RMSProp moves by approximately <span class="math-inline" markdown="0">\(0.316\)</span>.

### Variants and what the theory actually says

AdaMax replaces the squared-gradient accumulator with an exponentially weighted infinity-norm-style maximum. AdaDelta also tracks past squared updates. NAdam introduces a Nesterov-style correction; exact formulas depend on the variant.

AMSGrad uses a running maximum of second-moment estimates. With a constant or nonincreasing base step, its corresponding denominator-based step multiplier cannot grow. This addresses a failure in Adam's original general convergence argument; it is not a guarantee that every quantity in the update decreases. [Reddi et al., *On the Convergence of Adam and Beyond*](https://arxiv.org/abs/1904.09237).

It would be incorrect to say adaptive methods have no nonconvex theory: for example, AdaGrad-Norm has nonconvex convergence results under stated assumptions. [Ward, Wu, and Bottou](https://proceedings.mlr.press/v97/ward19a.html).

Likewise, experiments in which adaptive methods generalize worse than SGD are evidence about those settings, not a universal ranking. Optimizer choice, tuning, model, and data all matter. [Wilson et al., *The Marginal Value of Adaptive Gradient Methods in Machine Learning*](https://arxiv.org/abs/1705.08292).

## 13. Proximal gradient: preserve the difficult term
{: #proximal}

Consider <span class="math-inline" markdown="0">\(F(x)=f(x)+c(x)\)</span>, where <span class="math-inline" markdown="0">\(f\)</span> is convex and <span class="math-inline" markdown="0">\(L\)</span>-smooth and <span class="math-inline" markdown="0">\(c\)</span> is proper, closed, and convex. The second term may be nonsmooth or extended-valued, such as an indicator encoding constraints.

Linearize only <span class="math-inline" markdown="0">\(f\)</span>, add a quadratic model, and leave <span class="math-inline" markdown="0">\(c\)</span> intact:

<div class="math-display" markdown="0">\[x_{t+1}=\arg\min_x\left\{f(x_t)+\nabla f(x_t)^\top(x-x_t)+\frac1{2\eta}\&#124;x-x_t\&#124;^2+c(x)\right\}.\]</div>

Completing the square gives

<div class="math-display" markdown="0">\[z_t=x_t-\eta\nabla f(x_t),\qquad x_{t+1}=\operatorname{prox}_{\eta c}(z_t),\]</div>

<div class="math-display" markdown="0">\[\operatorname{prox}_{\eta c}(z)=\arg\min_x\left\{c(x)+\frac1{2\eta}\&#124;x-z\&#124;^2\right\}.\]</div>

| Penalty or constraint | Proximal result |
| --- | --- |
| <span class="math-inline" markdown="0">\(c=0\)</span> | <span class="math-inline" markdown="0">\(z\)</span> |
| <span class="math-inline" markdown="0">\(c(x)=\lambda\&#124;x\&#124;_1\)</span> | <span class="math-inline" markdown="0">\(\operatorname{sign}(z)\odot\max(&#124;z&#124;-\eta\lambda,0)\)</span> |
| <span class="math-inline" markdown="0">\(c=I_C\)</span>, closed convex <span class="math-inline" markdown="0">\(C\)</span> | Euclidean projection <span class="math-inline" markdown="0">\(P_C(z)\)</span> |
| <span class="math-inline" markdown="0">\(c=I_{[l,r]}\)</span> | <span class="math-inline" markdown="0">\(\min(\max(z,l),r)\)</span> |
| <span class="math-inline" markdown="0">\(c(x)=\lambda\&#124;x\&#124;^2/2\)</span> | <span class="math-inline" markdown="0">\(z/(1+\eta\lambda)\)</span> |
| <span class="math-inline" markdown="0">\(c(x)=\lambda\&#124;x\&#124;_1+\mu\&#124;x\&#124;^2/2\)</span> | Soft threshold at <span class="math-inline" markdown="0">\(\eta\lambda\)</span>, then divide by <span class="math-inline" markdown="0">\(1+\eta\mu\)</span> |
| <span class="math-inline" markdown="0">\(c(x)=-\lambda\log x\)</span>, <span class="math-inline" markdown="0">\(x&gt;0\)</span>, <span class="math-inline" markdown="0">\(\lambda&gt;0\)</span> | <span class="math-inline" markdown="0">\((z+\sqrt{z^2+4\eta\lambda})/2\)</span> |

For soft thresholding, solve <span class="math-inline" markdown="0">\(0\in(x-z)/\eta+\lambda\partial&#124;x&#124;\)</span> by splitting into positive, negative, and zero cases. The zero case is possible exactly when <span class="math-inline" markdown="0">\(&#124;z&#124;\le\eta\lambda\)</span>.

<details markdown="1" data-proof>
<summary>Proximal-gradient rate: the three-point inequality</summary>

Let <span class="math-inline" markdown="0">\(x^+\)</span> be the step from <span class="math-inline" markdown="0">\(y\)</span>. Its optimality condition is

<div class="math-display" markdown="0">\[\frac{y-x^+}{\eta}-\nabla f(y)\in\partial c(x^+).\]</div>

For any <span class="math-inline" markdown="0">\(z\)</span>, combine this supporting inequality with smoothness of <span class="math-inline" markdown="0">\(f\)</span> and <span class="math-inline" markdown="0">\(\eta\le1/L\)</span>. Convexity replaces <span class="math-inline" markdown="0">\(f(y)+\nabla f(y)^\top(z-y)\)</span> by a lower bound on <span class="math-inline" markdown="0">\(f(z)\)</span>, producing

<div class="math-display" markdown="0">\[F(x^+)\le F(z)+\frac1\eta(x^+-y)^\top(z-x^+)+\frac1{2\eta}\&#124;x^+-y\&#124;^2.\]</div>

The right-hand distance terms simplify to

<div class="math-display" markdown="0">\[F(x^+)\le F(z)+\frac1{2\eta}\bigl(\&#124;y-z\&#124;^2-\&#124;x^+-z\&#124;^2\bigr).\]</div>

Take <span class="math-inline" markdown="0">\(z=y\)</span> for descent. Take <span class="math-inline" markdown="0">\(z=x^\star\)</span> for a telescoping gap bound. Sum and use monotonicity:

<div class="math-display" markdown="0">\[F(x_T)-F^\star\le\frac1T\sum_{t=1}^T(F(x_t)-F^\star)\le\frac{R^2}{2\eta T}.\]</div>

This exploits the smooth-plus-proximable structure, rather than treating the entire objective as an arbitrary nonsmooth function.

</details>

<details markdown="1" data-proof>
<summary>Accelerated proximal proof: the weighted potential</summary>

One useful variant uses <span class="math-inline" markdown="0">\(\theta_t=2/(t+1)\)</span> for <span class="math-inline" markdown="0">\(t\ge1\)</span>, <span class="math-inline" markdown="0">\(u_0=x_0\)</span>, and

<div class="math-display" markdown="0">\[y_t=(1-\theta_t)x_{t-1}+\theta_tu_{t-1},\qquad x_t=\operatorname{prox}_{\eta c}(y_t-\eta\nabla f(y_t)),\]</div>

<div class="math-display" markdown="0">\[u_t=x_{t-1}+\frac{x_t-x_{t-1}}{\theta_t}.\]</div>

Apply the preceding three-point inequality with <span class="math-inline" markdown="0">\(z=x_{t-1}\)</span> and with <span class="math-inline" markdown="0">\(z=x^\star\)</span>, weight by <span class="math-inline" markdown="0">\(1-\theta_t\)</span> and <span class="math-inline" markdown="0">\(\theta_t\)</span>, then add. Since <span class="math-inline" markdown="0">\(x_t-y_t=\theta_t(u_t-u_{t-1})\)</span>, the inner product reduces to a difference of squared distances. With <span class="math-inline" markdown="0">\(\Delta_t=F(x_t)-F^\star\)</span>,

<div class="math-display" markdown="0">\[\frac{\Delta_t}{\theta_t^2}+\frac{\&#124;u_t-x^\star\&#124;^2}{2\eta}\le\frac{1-\theta_t}{\theta_t^2}\Delta_{t-1}+\frac{\&#124;u_{t-1}-x^\star\&#124;^2}{2\eta}.\]</div>

For <span class="math-inline" markdown="0">\(t\ge2\)</span>, <span class="math-inline" markdown="0">\((1-\theta_t)/\theta_t^2=(t^2-1)/4\le1/\theta_{t-1}^2\)</span>. At <span class="math-inline" markdown="0">\(t=1\)</span>, <span class="math-inline" markdown="0">\(\theta_1=1\)</span> eliminates the initial gap. The potential therefore telescopes to

<div class="math-display" markdown="0">\[F(x_T)-F^\star\le\frac{2R^2}{\eta(T+1)^2}.\]</div>

With <span class="math-inline" markdown="0">\(\eta=1/L\)</span>, this is the accelerated composite rate. The initial point must have finite objective value, and every proximal step must be well-defined and solved exactly for this proof.

</details>

### A discontinuous penalty is a separate case

Suppose <span class="math-inline" markdown="0">\(c(x)=0\)</span> on <span class="math-inline" markdown="0">\([0,\theta]\)</span> and <span class="math-inline" markdown="0">\(M&gt;0\)</span> outside, with <span class="math-inline" markdown="0">\(\theta\ge0\)</span>. This penalty is **not convex**, so the preceding convex rates do not apply. Its scalar proximal problem can still be solved by comparing candidates.

If <span class="math-inline" markdown="0">\(z\)</span> is inside, choose <span class="math-inline" markdown="0">\(z\)</span>. Otherwise compare the clipped point, whose cost is <span class="math-inline" markdown="0">\(\operatorname{dist}(z,[0,\theta])^2/(2\eta)\)</span>, with <span class="math-inline" markdown="0">\(z\)</span> itself, whose cost is <span class="math-inline" markdown="0">\(M\)</span>. Choose the lower cost; at equality both are minimizers. Solvability of a proximal subproblem does not imply convexity of the penalty.

## 14. Newton, quasi-Newton, and conjugate gradient
{: #second-order}

Newton's method minimizes a local second-order model:

<div class="math-display" markdown="0">\[x_{t+1}=x_t-[\nabla^2f(x_t)]^{-1}\nabla f(x_t).\]</div>

In implementation, solve a linear system rather than explicitly forming the inverse. A positive-definite Hessian makes the direction a descent direction. Indefinite or singular Hessians require safeguards, and full Newton steps are not globally reliable without additional assumptions or damping. A dense factorization costs roughly <span class="math-inline" markdown="0">\(O(d^3)\)</span>, though structure can change that cost substantially.

The Newton decrement is <span class="math-inline" markdown="0">\(\lambda_N^2=\nabla f^\top H^{-1}\nabla f\)</span> for <span class="math-inline" markdown="0">\(H\succ0\)</span>. Half this quantity is the predicted quadratic-model decrease. Treating it as a certified objective-gap stopping rule requires further conditions, such as an appropriate self-concordant analysis.

### Quasi-Newton updates

Let <span class="math-inline" markdown="0">\(s=x^+-x\)</span> and <span class="math-inline" markdown="0">\(y=\nabla f(x^+)-\nabla f(x)\)</span>. DFP updates an inverse-Hessian approximation <span class="math-inline" markdown="0">\(H\)</span>:

<div class="math-display" markdown="0">\[H^+=H+\frac{ss^\top}{s^\top y}-\frac{Hyy^\top H}{y^\top Hy}.\]</div>

BFGS in Hessian form updates <span class="math-inline" markdown="0">\(B\)</span>:

<div class="math-display" markdown="0">\[B^+=B-\frac{Bss^\top B}{s^\top Bs}+\frac{yy^\top}{y^\top s}.\]</div>

Both preserve positive definiteness when the starting matrix is positive definite and <span class="math-inline" markdown="0">\(s^\top y&gt;0\)</span>. Strong convexity ensures this for a nonzero displacement; Wolfe line search is another way to obtain the curvature condition. L-BFGS stores a limited history of these displacement pairs.

<details markdown="1" data-proof>
<summary>DFP proof: Cauchy–Schwarz plus its equality case</summary>

For <span class="math-inline" markdown="0">\(v\ne0\)</span>, put <span class="math-inline" markdown="0">\(a=H^{1/2}v\)</span> and <span class="math-inline" markdown="0">\(b=H^{1/2}y\)</span>. Then

<div class="math-display" markdown="0">\[v^\top H^+v=\&#124;a\&#124;^2-\frac{(a^\top b)^2}{\&#124;b\&#124;^2}+\frac{(s^\top v)^2}{s^\top y}.\]</div>

Both terms are nonnegative. The first is zero only when <span class="math-inline" markdown="0">\(v=cy\)</span> for some nonzero <span class="math-inline" markdown="0">\(c\)</span>. Then the second equals <span class="math-inline" markdown="0">\(c^2s^\top y&gt;0\)</span>. Thus the sum is strictly positive for every nonzero <span class="math-inline" markdown="0">\(v\)</span>.

The proof for Hessian-form BFGS is the same argument with the roles of <span class="math-inline" markdown="0">\(s\)</span> and <span class="math-inline" markdown="0">\(y\)</span> exchanged. The secant equations are <span class="math-inline" markdown="0">\(H^+y=s\)</span> and <span class="math-inline" markdown="0">\(B^+s=y\)</span>; keep straight which matrix approximates which object.

</details>

### Conjugate gradient

For <span class="math-inline" markdown="0">\(f(x)=x^\top Ax/2-b^\top x\)</span> with <span class="math-inline" markdown="0">\(A\succ0\)</span>, directions satisfy <span class="math-inline" markdown="0">\(d_i^\top Ad_j=0\)</span> for <span class="math-inline" markdown="0">\(i\ne j\)</span>. Exact line search along <span class="math-inline" markdown="0">\(d_k\)</span> gives

<div class="math-display" markdown="0">\[\alpha_k=-\frac{\nabla f(x_k)^\top d_k}{d_k^\top Ad_k},\qquad x_{k+1}=x_k+\alpha_kd_k.\]</div>

In exact arithmetic, conjugate gradient solves the system in at most <span class="math-inline" markdown="0">\(d\)</span> steps. Finite precision loses exact conjugacy, so that finite-termination statement is not a literal runtime guarantee.

## 15. Bellman equations and policy gradients
{: #rl}

In reinforcement learning, the policy is the object being optimized. For autoregressive language models, a useful abstraction takes the prompt and generated prefix as the state, the next token as the action, and a completed response as a trajectory.

For discounted returns, <span class="math-inline" markdown="0">\(G_t=\sum_{k\ge0}\gamma^kr_{t+k+1}\)</span> with <span class="math-inline" markdown="0">\(0\le\gamma&lt;1\)</span>. Bounded rewards make the infinite sum converge. Finite episodic problems can use <span class="math-inline" markdown="0">\(\gamma=1\)</span>.

### Bellman equations

With expectations over transitions and the policy,

<div class="math-display" markdown="0">\[V^\pi(s)=\mathbb E_{a,s'}[r(s,a,s')+\gamma V^\pi(s')],\]</div>

<div class="math-display" markdown="0">\[Q^\pi(s,a)=\mathbb E_{s'}[r(s,a,s')+\gamma\mathbb E_{a'\sim\pi}Q^\pi(s',a')].\]</div>

For optimal values, replace the policy expectation over the next action by a maximum:

<div class="math-display" markdown="0">\[V^*(s)=\max_a\mathbb E_{s'}[r(s,a,s')+\gamma V^*(s')],\]</div>

<div class="math-display" markdown="0">\[Q^*(s,a)=\mathbb E_{s'}[r(s,a,s')+\gamma\max_{a'}Q^*(s',a')].\]</div>

The advantage is <span class="math-inline" markdown="0">\(A^\pi(s,a)=Q^\pi(s,a)-V^\pi(s)\)</span>; it can be negative.

### The log-derivative trick

For an undiscounted finite episode, let <span class="math-inline" markdown="0">\(J(\theta)=\mathbb E_{\tau\sim p_\theta}[R(\tau)]\)</span>. Assuming differentiation and expectation can be interchanged, policy-independent reward and environment dynamics give

<div class="math-display" markdown="0">\[\nabla J=\mathbb E[R(\tau)\nabla\log p_\theta(\tau)].\]</div>

The trajectory density factors as

<div class="math-display" markdown="0">\[p_\theta(\tau)=p(s_0)\prod_t\pi_\theta(a_t\mid s_t)p(s_{t+1}\mid s_t,a_t).\]</div>

Only the policy factors depend on <span class="math-inline" markdown="0">\(\theta\)</span>, so

<div class="math-display" markdown="0">\[\nabla\log p_\theta(\tau)=\sum_t\nabla\log\pi_\theta(a_t\mid s_t).\]</div>

Past rewards contribute zero to the expected score at time <span class="math-inline" markdown="0">\(t\)</span>. Replacing the total return by reward-to-go yields

<div class="math-display" markdown="0">\[\nabla J=\mathbb E\left[\sum_t\nabla\log\pi_\theta(a_t\mid s_t)G_t\right].\]</div>

Discounted objectives require consistent time weights or a discounted occupancy convention; do not mix the finite undiscounted formula with a different objective silently. The policy-gradient framework is developed in [Sutton et al., *Policy Gradient Methods for Reinforcement Learning with Function Approximation*](https://proceedings.neurips.cc/paper_files/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html).

<details markdown="1" data-proof>
<summary>Why an action-independent baseline preserves the gradient</summary>

Condition on <span class="math-inline" markdown="0">\(s\)</span> and treat <span class="math-inline" markdown="0">\(b(s)\)</span> as fixed in the score estimator:

<div class="math-display" markdown="0">\[
\begin{aligned}
\mathbb E_{a\sim\pi}[b(s)\nabla\log\pi(a\mid s)]
&amp;=b(s)\sum_a\pi(a\mid s)\frac{\nabla\pi(a\mid s)}{\pi(a\mid s)}\\
&amp;=b(s)\nabla\sum_a\pi(a\mid s)=0.
\end{aligned}
\]</div>

A learned baseline is normally detached when forming this policy-gradient term. An arbitrary action-dependent baseline cannot be pulled outside the sum. A suitable baseline can reduce variance; action independence alone does not guarantee that every choice reduces it.

</details>

Exact <span class="math-inline" markdown="0">\(Q^\pi\)</span> can replace sampled reward-to-go by conditional expectation. Exact advantage subtracts <span class="math-inline" markdown="0">\(V^\pi\)</span>. A TD residual <span class="math-inline" markdown="0">\(r_t+\gamma V(s_{t+1})-V(s_t)\)</span> has the correct conditional advantage mean when <span class="math-inline" markdown="0">\(V=V^\pi\)</span>; an approximate critic can introduce bias. A fixed ranking of all these estimators by variance is not universal.

### LLM training context

A common pipeline is next-token pretraining, supervised instruction tuning, preference/reward modeling, and policy optimization; direct preference optimization is an alternative preference-learning route. This is a useful conceptual map, not a requirement that every system follow every stage.

A KL penalty to a reference policy discourages distributional drift. The sampled log ratio <span class="math-inline" markdown="0">\(\log\pi_\theta(a\mid s)-\log\pi_{\rm ref}(a\mid s)\)</span> estimates a statewise KL in expectation under <span class="math-inline" markdown="0">\(\pi_\theta\)</span>; a single sampled ratio can be negative. KL regularization does not guarantee prevention of reward hacking. Verifiable rewards also depend on the verifier and can be exploited when checks are incomplete.

If the reward includes a parameter-dependent regularizer, account for that dependence when differentiating the full objective. The simple score-function derivation above assumed a fixed reward.

## 16. Backpropagation and Mixture of Experts
{: #moe}

Backpropagation is repeated chain rule with intermediate derivatives reused rather than recomputed. For a sigmoid unit <span class="math-inline" markdown="0">\(a_j^\ell=\sigma(z_j^\ell)\)</span>,

<div class="math-display" markdown="0">\[z_j^\ell=\sum_iw_{ij}^\ell a_i^{\ell-1},\qquad\sigma'(z)=\sigma(z)(1-\sigma(z)).\]</div>

Writing <span class="math-inline" markdown="0">\(\delta_j^\ell=\partial\mathcal L/\partial z_j^\ell\)</span>,

<div class="math-display" markdown="0">\[\frac{\partial\mathcal L}{\partial w_{ij}^\ell}=\delta_j^\ell a_i^{\ell-1},\qquad\delta_j^\ell=\sigma'(z_j^\ell)\sum_pw_{jp}^{\ell+1}\delta_p^{\ell+1}.\]</div>

An <span class="math-inline" markdown="0">\(\ell_2\)</span> penalty adds its gradient separately, with the coefficient determined by the exact loss normalization.

For softmax logits <span class="math-inline" markdown="0">\(z\)</span>,

<div class="math-display" markdown="0">\[\frac{\partial\log p_a}{\partial z_b}=\mathbf1[a=b]-p_b,\qquad\frac{\partial p_a}{\partial z_b}=p_a(\mathbf1[a=b]-p_b).\]</div>

These are logit derivatives. Gradients with respect to model parameters require another chain-rule multiplication.

### Dense experts

For <span class="math-inline" markdown="0">\(y=\sum_iG_i(x)E_i(x)\)</span>, with scalar gates and vector expert outputs,

<div class="math-display" markdown="0">\[\frac{\partial\mathcal L}{\partial E_i}=G_i\frac{\partial\mathcal L}{\partial y},\qquad\frac{\partial\mathcal L}{\partial G_i}=E_i^\top\frac{\partial\mathcal L}{\partial y}.\]</div>

The gate derivative is a scalar inner product. If <span class="math-inline" markdown="0">\(E_2=(2,4)\)</span> and <span class="math-inline" markdown="0">\(\partial\mathcal L/\partial y=(2,-1)\)</span>, that gate derivative is zero. If <span class="math-inline" markdown="0">\(G_1=0.6\)</span>, the first expert's output gradient is <span class="math-inline" markdown="0">\((1.2,-0.6)\)</span>.

### Hard routing is not the maximum-score function

Hard top-1 chooses <span class="math-inline" markdown="0">\(i^\star=\arg\max_i s_i(x)\)</span> and returns <span class="math-inline" markdown="0">\(E_{i^\star}(x)\)</span>. Away from ties, the chosen index is locally constant: the task loss provides no ordinary derivative through the discrete selection itself. Unselected expert parameters receive no task gradient through this token's routed output, though shared parameters and auxiliary losses can still receive gradients.

This is different from <span class="math-inline" markdown="0">\(m(x)=\max_i s_i(x)\)</span>. For differentiable convex scores, the subdifferential of <span class="math-inline" markdown="0">\(m\)</span> is the convex hull of the active score gradients. That formula does not differentiate the hard-routed output and should not be used as if it did.

Also, the formal partial derivative with respect to an independently variable dense gate is <span class="math-inline" markdown="0">\(E_i^\top\nabla_y\mathcal L\)</span> even at <span class="math-inline" markdown="0">\(G_i=0\)</span>. A zero hard gate and differentiation through its selection mechanism are different operations.

Noisy top-<span class="math-inline" markdown="0">\(k\)</span> can form scores

<div class="math-display" markdown="0">\[H_i(x)=(xW_g)_i+\xi_i\operatorname{softplus}((xW_{\rm noise})_i),\qquad\xi_i\sim\mathcal N(0,1),\]</div>

retain the top <span class="math-inline" markdown="0">\(k\)</span>, set the other logits to <span class="math-inline" markdown="0">\(-\infty\)</span>, and apply softmax. Softplus supplies a positive noise scale. Load-balancing objectives encourage broader expert use; they do not guarantee that every expert trains on every batch.

## 17. Supplementary tools: constraints, duality, and structure
{: #extensions}

These topics extend the core first-order material and are useful for interpreting optimization problems and practice questions. Their inclusion here does not imply a particular exam's syllabus.

### Lagrangians and KKT

For <span class="math-inline" markdown="0">\(\min f(x)\)</span> subject to <span class="math-inline" markdown="0">\(g_i(x)\le0\)</span> and <span class="math-inline" markdown="0">\(h_j(x)=0\)</span>,

<div class="math-display" markdown="0">\[\mathcal L(x,\lambda,\nu)=f(x)+\sum_i\lambda_i g_i(x)+\sum_j\nu_jh_j(x),\qquad\lambda_i\ge0.\]</div>

The dual function <span class="math-inline" markdown="0">\(q(\lambda,\nu)=\inf_x\mathcal L(x,\lambda,\nu)\)</span> is concave, even when the primal is nonconvex. For fixed <span class="math-inline" markdown="0">\(x\)</span>, the Lagrangian is affine in the multipliers. Weak duality follows because <span class="math-inline" markdown="0">\(\mathcal L(x,\lambda,\nu)\le f(x)\)</span> for feasible <span class="math-inline" markdown="0">\(x\)</span> and nonnegative inequality multipliers.

For a differentiable convex problem, KKT consists of primal feasibility, dual feasibility, stationarity, and complementary slackness:

<div class="math-display" markdown="0">\[\nabla f(x^\star)+\sum_i\lambda_i^\star\nabla g_i(x^\star)+\sum_j\nu_j^\star\nabla h_j(x^\star)=0,\]</div>

<div class="math-display" markdown="0">\[\lambda_i^\star g_i(x^\star)=0.\]</div>

KKT is sufficient in the convex setting; a constraint qualification such as Slater's condition gives the usual necessity and strong-duality result. Standard convex formulations use convex inequality functions and affine equality functions. A nonlinear equality can happen to describe a convex set, so “every representation of a convex feasible set must use affine equalities” would be too strong.

At a primal-dual saddle point,

<div class="math-display" markdown="0">\[\mathcal L(x^\star,\lambda,\nu)\le\mathcal L(x^\star,\lambda^\star,\nu^\star)\le\mathcal L(x,\lambda^\star,\nu^\star).\]</div>

This is an inequality, not equality for all arguments. These definitions and qualification conditions are treated systematically in [Boyd and Vandenberghe, *Convex Optimization*](https://web.stanford.edu/~boyd/cvxbook/).

### Projection formulas

For a halfspace <span class="math-inline" markdown="0">\(a^\top x\le b\)</span>, with <span class="math-inline" markdown="0">\(a\ne0\)</span>,

<div class="math-display" markdown="0">\[P_C(z)=z-\frac{\max(a^\top z-b,0)}{\&#124;a\&#124;^2}a.\]</div>

For a box, clip each coordinate. For a feasible box intersected with a halfspace, the candidate is <span class="math-inline" markdown="0">\(x(\lambda)=\operatorname{clip}(z-\lambda a,l,u)\)</span>. Use <span class="math-inline" markdown="0">\(\lambda=0\)</span> if it is feasible; otherwise solve <span class="math-inline" markdown="0">\(a^\top x(\lambda)=b\)</span> for a nonnegative multiplier. The left side is nonincreasing, so bisection is useful after bracketing a solution.

### Lasso reformulations and duality

For <span class="math-inline" markdown="0">\(\lambda&gt;0\)</span>, introducing <span class="math-inline" markdown="0">\(p\)</span> with <span class="math-inline" markdown="0">\(-p_i\le w_i\le p_i\)</span> rewrites Lasso as

<div class="math-display" markdown="0">\[\min_{w,p}\frac12\&#124;Aw-y\&#124;^2+\lambda\sum_i p_i.\]</div>

For fixed <span class="math-inline" markdown="0">\(w\)</span>, the smallest feasible <span class="math-inline" markdown="0">\(p_i\)</span> is <span class="math-inline" markdown="0">\(&#124;w_i&#124;\)</span>, so the minimizers in <span class="math-inline" markdown="0">\(w\)</span> are unchanged. The objective is now smooth, with linear constraints. Projection onto each cone <span class="math-inline" markdown="0">\(&#124;w_i&#124;\le p_i\)</span> is unchanged inside; zero if <span class="math-inline" markdown="0">\(p_i\le-&#124;w_i&#124;\)</span>; otherwise <span class="math-inline" markdown="0">\(((&#124;w_i&#124;+p_i)\operatorname{sign}(w_i)/2,(&#124;w_i&#124;+p_i)/2)\)</span>.

<details markdown="1" data-proof>
<summary>Derivation: the Lasso dual</summary>

Introduce <span class="math-inline" markdown="0">\(z=Aw-y\)</span> and multiplier <span class="math-inline" markdown="0">\(v\)</span>:

<div class="math-display" markdown="0">\[\mathcal L=\frac12\&#124;z\&#124;^2+\lambda\&#124;w\&#124;_1+v^\top(Aw-y-z).\]</div>

Minimizing over <span class="math-inline" markdown="0">\(z\)</span> gives <span class="math-inline" markdown="0">\(z=v\)</span> and contribution <span class="math-inline" markdown="0">\(-\&#124;v\&#124;^2/2\)</span>. Minimizing over <span class="math-inline" markdown="0">\(w\)</span> gives zero when <span class="math-inline" markdown="0">\(\&#124;A^\top v\&#124;_\infty\le\lambda\)</span>, and <span class="math-inline" markdown="0">\(-\infty\)</span> otherwise. Therefore the dual is

<div class="math-display" markdown="0">\[\max_v-\frac12\&#124;v\&#124;^2-v^\top y\quad\text{subject to}\quad\&#124;A^\top v\&#124;_\infty\le\lambda.\]</div>

Changing the loss normalization changes the quadratic coefficient in the dual. Strong duality holds under the standard finite-valued convex affine-constraint qualification here.

</details>

### Low rank, sparsity, and decomposability

Robust PCA separates <span class="math-inline" markdown="0">\(X=L+S\)</span> into low-rank structure and sparse corruption. The convex relaxation

<div class="math-display" markdown="0">\[\min_{L,S}\&#124;L\&#124;_*+\lambda\&#124;S\&#124;_1\quad\text{subject to }X=L+S\]</div>

uses the nuclear norm for rank and the entrywise <span class="math-inline" markdown="0">\(\ell_1\)</span> norm for sparsity. Exact recovery needs additional assumptions; merely writing this objective does not prove recovery.

A regularizer is decomposable across appropriate subspaces when it adds exactly. For <span class="math-inline" markdown="0">\(\ell_1\)</span>, vectors on disjoint coordinate supports satisfy <span class="math-inline" markdown="0">\(\&#124;u+v\&#124;_1=\&#124;u\&#124;_1+\&#124;v\&#124;_1\)</span>. Group norms have the analogous property on disjoint groups. Nuclear norm is additive for matrices with orthogonal row and column spaces. Euclidean norm is generally not additive on orthogonal vectors: <span class="math-inline" markdown="0">\(\&#124;e_1+e_2\&#124;_2=\sqrt2&lt;2\)</span>.

**Restricted strong convexity** asks for quadratic curvature only on a specified family of differences. For a <span class="math-inline" markdown="0">\(k\)</span>-sparse difference in least squares, it is enough to control <span class="math-inline" markdown="0">\(X_S^\top X_S/n\succeq\alpha_k I\)</span> on each relevant support. This can hold when the full Hessian is singular.

**Graph-signal objectives** often combine reconstruction <span class="math-inline" markdown="0">\(\&#124;X-V\alpha\&#124;_F^2\)</span>, graph smoothness <span class="math-inline" markdown="0">\(\operatorname{tr}(\alpha^\top\Delta\alpha)\)</span>, and row sparsity <span class="math-inline" markdown="0">\(\sum_i\&#124;\alpha_{i,:}\&#124;_2\)</span>. Orthonormality of <span class="math-inline" markdown="0">\(V\)</span>, Laplacian sign constraints, and a trace normalization enforce structure and scale. With fixed graph quantities the coefficient problem can be convex; joint graph/basis learning is generally nonconvex. An orthogonality constraint also prevents an automatic “convex in every block” conclusion.

### Min–max and submodularity

Weak min–max duality says

<div class="math-display" markdown="0">\[\sup_y\inf_x f(x,y)\le\inf_x\sup_y f(x,y).\]</div>

Equality requires extra structure or a saddle point. An infimum or supremum need not be attained.

For a finite ground set and nonnegative similarities, facility location <span class="math-inline" markdown="0">\(F(S)=\sum_i\max_{j\in S}s_{ij}\)</span>, with empty-set baseline zero, is monotone submodular. The gain of adding <span class="math-inline" markdown="0">\(j\)</span> is <span class="math-inline" markdown="0">\(\sum_i\max(0,s_{ij}-\max_{k\in S}s_{ik})\)</span>, which decreases as <span class="math-inline" markdown="0">\(S\)</span> grows. Column-set rank is also submodular: a column that adds a new direction to a larger span also adds a new direction to a smaller span. These are set-function statements, distinct from convexity in a continuous matrix variable.

## 18. Worked revision problems
{: #practice}

These problems consolidate the mathematical patterns from the notes. The solutions are self-contained rather than tied to unverified past-paper numbering or marking schemes.

### Problem 1 · A corner can be the optimum

For <span class="math-inline" markdown="0">\(f(x)=\max(2x,-x)\)</span>, establish convexity, compute <span class="math-inline" markdown="0">\(\partial f(0)\)</span>, certify a minimum, and take one subgradient step from <span class="math-inline" markdown="0">\(x_0=2\)</span> with <span class="math-inline" markdown="0">\(\eta=0.5\)</span>.

<details markdown="1" data-proof>
<summary>Show solution</summary>

It is a maximum of affine functions, hence convex. The left and right slopes are <span class="math-inline" markdown="0">\(-1\)</span> and <span class="math-inline" markdown="0">\(2\)</span>, so it is nondifferentiable at zero and <span class="math-inline" markdown="0">\(\partial f(0)=[-1,2]\)</span>. Since zero belongs to this interval, zero is a global minimizer. At <span class="math-inline" markdown="0">\(x_0=2\)</span>, the active slope is <span class="math-inline" markdown="0">\(2\)</span>, giving <span class="math-inline" markdown="0">\(x_1=2-0.5(2)=1\)</span>.

</details>

### Problem 2 · Find the curvature constants

Let <span class="math-inline" markdown="0">\(f(w)=\&#124;Xw-y\&#124;^2+\lambda\&#124;w\&#124;^2/2\)</span> with <span class="math-inline" markdown="0">\(\lambda&gt;0\)</span>. Find <span class="math-inline" markdown="0">\(L\)</span> and <span class="math-inline" markdown="0">\(\mu\)</span>. What changes when <span class="math-inline" markdown="0">\(n&lt;d\)</span>?

<details markdown="1" data-proof>
<summary>Show solution</summary>

The Hessian is <span class="math-inline" markdown="0">\(2X^\top X+\lambda I\)</span>, so <span class="math-inline" markdown="0">\(L=2\lambda_{\max}(X^\top X)+\lambda\)</span> and <span class="math-inline" markdown="0">\(\mu=2\lambda_{\min}(X^\top X)+\lambda\)</span>. When <span class="math-inline" markdown="0">\(n&lt;d\)</span>, the unregularized matrix is singular; regularization still guarantees <span class="math-inline" markdown="0">\(\mu=\lambda\)</span> as a tight lower eigenvalue in that case. The factor <span class="math-inline" markdown="0">\(1/2\)</span> on the regularizer matters.

</details>

### Problem 3 · Soft thresholding and elastic net

For <span class="math-inline" markdown="0">\(y=(3.5,-4,1.2,-0.8)\)</span> and <span class="math-inline" markdown="0">\(\lambda=1.5\)</span>, minimize <span class="math-inline" markdown="0">\(\&#124;x-y\&#124;^2/2+\lambda\&#124;x\&#124;_1\)</span>. Then evaluate the elastic-net prox at <span class="math-inline" markdown="0">\(z=(3,-1,0)\)</span> with <span class="math-inline" markdown="0">\(\eta=1\)</span>, <span class="math-inline" markdown="0">\(\lambda=2\)</span>, <span class="math-inline" markdown="0">\(\mu=1\)</span>.

<details markdown="1" data-proof>
<summary>Show solution</summary>

Soft thresholding gives <span class="math-inline" markdown="0">\(x^\star=(2,-2.5,0,0)\)</span> and <span class="math-inline" markdown="0">\(\&#124;x^\star\&#124;^2=10.25\)</span>. For elastic net, threshold at two to obtain <span class="math-inline" markdown="0">\((1,0,0)\)</span>, then divide by <span class="math-inline" markdown="0">\(1+\eta\mu=2\)</span>: the result is <span class="math-inline" markdown="0">\((0.5,0,0)\)</span>.

</details>

### Problem 4 · A linear-fractional quasigradient

Let <span class="math-inline" markdown="0">\(f(x)=(a^\top x+b)/(c^\top x+d)\)</span> on the positive-denominator domain. Show that <span class="math-inline" markdown="0">\(g=a-f(x_0)c\)</span> satisfies <span class="math-inline" markdown="0">\(g^\top(x-x_0)\ge0\Rightarrow f(x)\ge f(x_0)\)</span>.

<details markdown="1" data-proof>
<summary>Show solution</summary>

Use the identity <span class="math-inline" markdown="0">\(a^\top x_0+b=f(x_0)(c^\top x_0+d)\)</span>. Then

<div class="math-display" markdown="0">\[g^\top(x-x_0)=a^\top x+b-f(x_0)(c^\top x+d).\]</div>

Nonnegativity and division by the positive denominator give the result. Sublevel and superlevel sets are halfspaces intersected with the domain, so this function is both quasiconvex and quasiconcave. For a general differentiable quasiconvex function, only the appropriate strict-direction implication follows from its gradient; a zero gradient need not certify a minimum.

</details>

### Problem 5 · Convexity of a spectral quantity

Show that <span class="math-inline" markdown="0">\(\phi_k(X)=\sum_{i=1}^k\sigma_i(X)\)</span> is convex. Explain why proving each singular value convex would be invalid.

<details markdown="1" data-proof>
<summary>Show solution and subdifferential</summary>

Use the variational representation, for <span class="math-inline" markdown="0">\(1\le k\le\min(m,n)\)</span>,

<div class="math-display" markdown="0">\[\phi_k(X)=\max_{U^\top U=V^\top V=I_k}\operatorname{tr}(U^\top XV).\]</div>

The trace inequality bounds the right side by the sum of leading singular values, with equality at their singular vectors. Each expression is linear in <span class="math-inline" markdown="0">\(X\)</span>, so the maximum is convex. The counterexample in section 4 rules out convexity of individual <span class="math-inline" markdown="0">\(\sigma_k\)</span> for <span class="math-inline" markdown="0">\(k\ge2\)</span>.

The general subdifferential is the convex hull of coefficient matrices <span class="math-inline" markdown="0">\(UV^\top\)</span> attaining the maximum. For <span class="math-inline" markdown="0">\(k&lt;\min(m,n)\)</span>, a strict positive gap <span class="math-inline" markdown="0">\(\sigma_k&gt;\sigma_{k+1}\)</span> gives gradient <span class="math-inline" markdown="0">\(U_kV_k^\top\)</span>. Ties need the convex-hull formula. For the full nuclear norm at rank <span class="math-inline" markdown="0">\(r\)</span>,

<div class="math-display" markdown="0">\[\partial\&#124;X\&#124;_*=\{U_rV_r^\top+W:U_r^\top W=0,\ WV_r=0,\ \&#124;W\&#124;_2\le1\}.\]</div>

The full-norm, rank-deficient case needs this separate treatment; a blanket claim of differentiability without considering zero singular values is unsafe.

</details>

### Problem 6 · Positive definiteness and a quadratic optimum

Minimize <span class="math-inline" markdown="0">\(x_1^2+x_2^2-14x_1-6x_2\)</span> subject to <span class="math-inline" markdown="0">\(x_1+x_2\le2\)</span> and <span class="math-inline" markdown="0">\(x_1+2x_2\le3\)</span>.

<details markdown="1" data-proof>
<summary>Show KKT solution</summary>

The Hessian is <span class="math-inline" markdown="0">\(2I\)</span>, so the objective is strongly convex. The unconstrained solution <span class="math-inline" markdown="0">\((7,3)\)</span> is infeasible. Try the first constraint active and the second inactive. Stationarity gives

<div class="math-display" markdown="0">\[2x_1-14+\lambda_1=0,\qquad2x_2-6+\lambda_1=0.\]</div>

Together with <span class="math-inline" markdown="0">\(x_1+x_2=2\)</span>, this gives <span class="math-inline" markdown="0">\((x_1,x_2)=(3,-1)\)</span> and <span class="math-inline" markdown="0">\(\lambda_1=8\)</span>. The second constraint has value <span class="math-inline" markdown="0">\(1\le3\)</span>, and its multiplier is zero. Primal feasibility, nonnegative multipliers, stationarity, and complementary slackness all hold. Hence the unique optimum is <span class="math-inline" markdown="0">\((3,-1)\)</span>, with value <span class="math-inline" markdown="0">\(-26\)</span>.

For comparison, imposing only the second constraint gives <span class="math-inline" markdown="0">\((5,-1)\)</span>, which violates the first. Imposing both gives <span class="math-inline" markdown="0">\((1,1)\)</span> with a negative second multiplier. One valid KKT point already suffices to certify the convex optimum.

</details>

### Problem 7 · Momentum arithmetic

Take <span class="math-inline" markdown="0">\(x_t=(2,3)\)</span>, <span class="math-inline" markdown="0">\(v_t=(1,-2)\)</span>, <span class="math-inline" markdown="0">\(\beta=0.9\)</span>, <span class="math-inline" markdown="0">\(\eta=0.1\)</span>, and <span class="math-inline" markdown="0">\(\nabla f(x_t)=(4,-5)\)</span>. Compute the next velocity and point.

<details markdown="1" data-proof>
<summary>Show solution</summary>

<div class="math-display" markdown="0">\[v_{t+1}=0.9(1,-2)-0.1(4,-5)=(0.5,-1.3),\qquad x_{t+1}=(2.5,1.7).\]</div>

Keep the velocity update and position update separate. Mixing the two is a common sign error.

</details>

### Problem 8 · Projection, proximity, and a jump

Find the proximal point for <span class="math-inline" markdown="0">\(c(x)=0\)</span> on <span class="math-inline" markdown="0">\([0,1]\)</span> and <span class="math-inline" markdown="0">\(c(x)=2\)</span> elsewhere, with <span class="math-inline" markdown="0">\(z=3\)</span> and <span class="math-inline" markdown="0">\(\eta=1\)</span>. Is it unique? Can the convex proximal-gradient rate be used for this penalty?

<details markdown="1" data-proof>
<summary>Show solution</summary>

The best inside point is <span class="math-inline" markdown="0">\(1\)</span>, with cost <span class="math-inline" markdown="0">\((1-3)^2/2=2\)</span>. The best outside point is <span class="math-inline" markdown="0">\(3\)</span>, with cost <span class="math-inline" markdown="0">\(2\)</span>. Both are minimizers. The penalty has a jump and is nonconvex, so the convex composite theorem does not apply. This illustrates why uniqueness and rate claims cannot be inferred just from the word “proximal.”

</details>

### Problem 9 · Sampling and policy normalization

A density on <span class="math-inline" markdown="0">\([0,1]\)</span> is <span class="math-inline" markdown="0">\(p(x)=2x\)</span>. Transform a uniform sample <span class="math-inline" markdown="0">\(u=0.64\)</span> into a sample from this density. Separately, show that the mean softmax logit score is zero.

<details markdown="1" data-proof>
<summary>Show solution</summary>

The CDF is <span class="math-inline" markdown="0">\(F(x)=x^2\)</span>, so inverse-CDF sampling gives <span class="math-inline" markdown="0">\(x=\sqrt u=0.8\)</span>. For the softmax score,

<div class="math-display" markdown="0">\[\sum_a p_a\frac{\partial\log p_a}{\partial z_b}=\sum_a p_a(\mathbf1[a=b]-p_b)=p_b-p_b\sum_a p_a=0.\]</div>

The second identity is the algebra behind action-independent baselines.

</details>

### Problem 10 · Decomposability and reversed inclusions

If <span class="math-inline" markdown="0">\(M\subseteq\bar M\)</span>, which way does the orthogonal-complement inclusion go? Why is <span class="math-inline" markdown="0">\(\ell_1\)</span> decomposable across a support and its complement?

<details markdown="1" data-proof>
<summary>Show solution</summary>

<span class="math-inline" markdown="0">\(\bar M^\perp\subseteq M^\perp\)</span>: a vector orthogonal to every member of the larger space is also orthogonal to every member of the smaller space.

If <span class="math-inline" markdown="0">\(u\)</span> is supported on <span class="math-inline" markdown="0">\(S\)</span> and <span class="math-inline" markdown="0">\(v\)</span> on <span class="math-inline" markdown="0">\(S^c\)</span>, every coordinate contains at most one nonzero term. Therefore

<div class="math-display" markdown="0">\[\&#124;u+v\&#124;_1=\sum_{i\in S}&#124;u_i&#124;+\sum_{i\notin S}&#124;v_i&#124;=\&#124;u\&#124;_1+\&#124;v\&#124;_1.\]</div>

No cancellation or reinforcement can occur within a coordinate because the supports are disjoint.

</details>

## 19. The final self-check
{: #checklist}

Before calling a proof complete, check the following.

| Claim or shortcut | What to check |
| --- | --- |
| “The Hessian is PSD” | Everywhere on a convex domain, or only at one point? |
| “The function is smooth” | A gradient-Lipschitz bound; outside convexity, both curvature signs matter |
| “The minimum exists” | Attainment, not just a finite infimum |
| “Strictly convex” | Uniqueness if a minimum exists, not necessarily strong convexity |
| “The subgradient is bounded” | Domain interior and chosen norm; boundary normals can change the statement |
| “The last iterate converges at this rate” | Does the proof actually bound a best or averaged iterate? |
| “SGD is unbiased” | Conditional expectation at the current iterate, and the sampling distribution |
| “Variance is divided by batch size” | Independent samples, or a without-replacement correction |
| “Momentum accelerates” | Which algorithm, schedule, objective class, and measured error? |
| “Adaptive methods generalize worse” | A finding in some experiments, not a theorem for all tasks |
| “The router has a subgradient” | Maximum score versus discrete selection and the routed output |
| “A baseline reduces variance” | A suitable choice is needed; unbiasedness alone is not variance reduction |
| “A constraint is convex” | The feasible set and the standard formulation both deserve attention |

For rate proofs, reconstruct this sequence: **one-step relation → class assumption → telescope or contract → choose the step → identify the output → solve for the tolerance**.

For property questions, start with the simplest route: closure rules, then derivatives or Hessians, then the definition. To disprove a claim, produce one concrete violating example. A matrix being positive semidefinite is a statement about quadratic forms, not about every entry being nonnegative.

For objective-reading questions, label every term by what it measures and encourages. Then examine each constraint, the variable with respect to which convexity is claimed, and whether the problem is jointly convex. These habits transfer beyond any particular course or exam.

## References and further reading
{: #references}

The organization and worked examples above are based on my course revision notes. These primary sources provide context and fuller treatments for the definitions and qualifications used here:

- [Boyd and Vandenberghe — *Convex Optimization*](https://web.stanford.edu/~boyd/cvxbook/): convex geometry, optimality, duality, and numerical methods.
- [Fazel — *Convex Envelopes of Rank and Cardinality Functions*](https://faculty.washington.edu/mfazel/low-rank-v2.pdf): the domains on which nuclear and sparsity envelopes apply.
- [Sutton et al. — *Policy Gradient Methods for Reinforcement Learning with Function Approximation*](https://proceedings.neurips.cc/paper_files/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html): policy gradients and function approximation.
- [Wilson et al. — *The Marginal Value of Adaptive Gradient Methods in Machine Learning*](https://arxiv.org/abs/1705.08292): empirical and theoretical comparisons of adaptive and non-adaptive methods.
- [Reddi et al. — *On the Convergence of Adam and Beyond*](https://arxiv.org/abs/1904.09237): convergence failures and the motivation for AMSGrad.
- [Ward, Wu, and Bottou — *AdaGrad Stepsizes: Sharp Convergence Over Nonconvex Landscapes*](https://proceedings.mlr.press/v97/ward19a.html): nonconvex results for AdaGrad-Norm.
- [Wang et al. — *Provable Acceleration of Heavy Ball beyond Quadratics*](https://proceedings.mlr.press/v162/wang22p.html): why extending quadratic momentum results requires care.
