---
layout: essay
title: "Optimization, Connected: A Revision Guide"
description: "Revisit the core ideas of optimization—from derivatives and gradients to convexity, subgradients, and proximal methods."
excerpt: "A connected guide to gradients, convexity, subgradients, and proximal methods—and what they tell us about optimization and expert routing."
date: 2026-11-15
permalink: /blog/optimization-revision-guide/
eyebrow: "Mathematics · Revision guide"
topic: mathematics
math: true
native_article: true
tags: [optimization, convexity, machine learning]
---

Optimization is easier to revise when the concepts connect. Derivatives describe change, convexity helps certify minima, and smoothness helps us choose useful steps. Subgradients and proximal methods extend the picture to objectives with corners.

This guide revisits those foundations in the order they depend on one another, using small examples and derivations. It covers the core ideas behind unconstrained smooth and convex nonsmooth optimization, then connects them to Mixture of Experts routing.

Much of optimization begins with a simple instruction: take a derivative, set it to zero, and solve.

For a function like <span class="math-inline" markdown="0">\(f(x)=x^2\)</span>, this works beautifully. The derivative is <span class="math-inline" markdown="0">\(2x\)</span>, it vanishes at zero, and zero is the minimum.

But a few small changes expose the limits of that recipe. The function <span class="math-inline" markdown="0">\(x^3\)</span> also has a zero derivative at the origin, yet no minimum there. The function <span class="math-inline" markdown="0">\(&#124;x&#124;\)</span> has a minimum at the origin, but no derivative there at all.

These examples raise two different questions. What does a derivative actually tell us? And what additional structure lets us turn that information into an optimization method?

Following those questions leads from ordinary calculus to gradients, convexity, subgradients, and proximal methods. It also helps explain some of the difficulties that arise when neural networks make discrete routing decisions.

## A derivative describes local change

For a function of one variable, the derivative measures how its output changes under a small change in its input:

<div class="math-display" markdown="0">\[
f'(x)=\lim_{h\to 0}\frac{f(x+h)-f(x)}{h}.
\]</div>

For <span class="math-inline" markdown="0">\(f(x)=x^2\)</span>,

<div class="math-display" markdown="0">\[
\begin{aligned}
f'(x)&amp;=\lim_{h\to 0}\frac{(x+h)^2-x^2}{h}\\
&amp;=\lim_{h\to 0}(2x+h)\\
&amp;=2x.
\end{aligned}
\]</div>

At <span class="math-inline" markdown="0">\(x=-2\)</span>, the slope is <span class="math-inline" markdown="0">\(-4\)</span>: moving a little to the right decreases the function. At <span class="math-inline" markdown="0">\(x=2\)</span>, the slope is <span class="math-inline" markdown="0">\(4\)</span>: the same movement increases it.

At zero, the tangent is flat.

A flat tangent is useful evidence, but it does not identify a minimum on its own. For <span class="math-inline" markdown="0">\(f(x)=x^3\)</span>, the derivative <span class="math-inline" markdown="0">\(3x^2\)</span> also vanishes at zero, even though the function continues increasing through that point.

The derivative describes first-order behavior near a point. To understand whether that point minimizes the function, we need more information.

## From one slope to a gradient

A machine-learning objective usually depends on many parameters. Consider a small example:

<div class="math-display" markdown="0">\[f(x,y)=x^2+3y^2.\]</div>

We can measure change along each coordinate while holding the other fixed:

<div class="math-display" markdown="0">\[\frac{\partial f}{\partial x}=2x,\qquad \frac{\partial f}{\partial y}=6y.\]</div>

Collecting these partial derivatives gives the gradient:

<div class="math-display" markdown="0">\[\nabla f(x,y)=\begin{bmatrix}2x\\6y\end{bmatrix}.\]</div>

At <span class="math-inline" markdown="0">\((1,2)\)</span>,

<div class="math-display" markdown="0">\[\nabla f(1,2)=\begin{bmatrix}2\\12\end{bmatrix}.\]</div>

Here, a small positive change in <span class="math-inline" markdown="0">\(y\)</span> affects the function more strongly than an equally sized positive change in <span class="math-inline" markdown="0">\(x\)</span>.

More generally, the gradient describes change along any direction <span class="math-inline" markdown="0">\(d\)</span>:

<div class="math-display" markdown="0">\[D_d f(x)=\nabla f(x)^\top d.\]</div>

This is the **directional derivative**. Among directions of unit Euclidean length, it is largest in the direction of the gradient and smallest in the opposite direction, provided the gradient is nonzero.

That observation gives us gradient descent:

<div class="math-display" markdown="0">\[x_{t+1}=x_t-\eta_t\nabla f(x_t),\]</div>

where <span class="math-inline" markdown="0">\(\eta_t&gt;0\)</span> is the step size.

Indeed, choosing <span class="math-inline" markdown="0">\(d=-\nabla f(x)\)</span> gives

<div class="math-display" markdown="0">\[\nabla f(x)^\top d=-\&#124;\nabla f(x)\&#124;^2.\]</div>

This is negative whenever the gradient is nonzero. A sufficiently small step in that direction therefore decreases the objective. How small the step needs to be will become important later.

### Where the differential fits

The gradient also gives a linear approximation to a change in the function:

<div class="math-display" markdown="0">\[f(x+\Delta x)-f(x)\approx\nabla f(x)^\top\Delta x.\]</div>

The corresponding linear map is the differential, often written as

<div class="math-display" markdown="0">\[df=\nabla f(x)^\top dx.\]</div>

For our quadratic,

<div class="math-display" markdown="0">\[df=2x\,dx+6y\,dy.\]</div>

Starting at <span class="math-inline" markdown="0">\((1,2)\)</span>, let both coordinates increase by <span class="math-inline" markdown="0">\(0.01\)</span>. The predicted change is

<div class="math-display" markdown="0">\[df=2(1)(0.01)+6(2)(0.01)=0.14.\]</div>

The actual change is <span class="math-inline" markdown="0">\(0.1404\)</span>. The small discrepancy comes from the quadratic terms omitted by the linear approximation.

For vector-valued functions, these derivatives are organized into a **Jacobian**. Under the usual convention, the Jacobian of a scalar-valued function is the transpose of its gradient. This distinction matters in backpropagation, where intermediate computations often produce vectors.

## Curvature explains how the gradient changes

The gradient tells us the local slope. The second derivative tells us how that slope changes.

For <span class="math-inline" markdown="0">\(f(x)=x^2\)</span>,

<div class="math-display" markdown="0">\[f'(x)=2x,\qquad f''(x)=2.\]</div>

In several variables, second derivatives form the Hessian matrix:

<div class="math-display" markdown="0">\[
\nabla^2 f(x,y)=\begin{bmatrix}
\frac{\partial^2 f}{\partial x^2}&amp;\frac{\partial^2 f}{\partial x\partial y}\\
\frac{\partial^2 f}{\partial y\partial x}&amp;\frac{\partial^2 f}{\partial y^2}
\end{bmatrix}.
\]</div>

For <span class="math-inline" markdown="0">\(f(x,y)=x^2+3y^2\)</span>,

<div class="math-display" markdown="0">\[\nabla^2 f(x,y)=\begin{bmatrix}2&amp;0\\0&amp;6\end{bmatrix}.\]</div>

The curvature along a direction <span class="math-inline" markdown="0">\(d\)</span> is described by

<div class="math-display" markdown="0">\[d^\top\nabla^2 f(x)d.\]</div>

In this example, the Hessian’s eigenvalues are <span class="math-inline" markdown="0">\(2\)</span> and <span class="math-inline" markdown="0">\(6\)</span>. Both are positive, so the function bends upward in every nonzero direction. It bends more sharply along the <span class="math-inline" markdown="0">\(y\)</span>-axis.

This is also the geometry that makes optimization easier: the surface has a single bowl-shaped structure.

## Convexity turns local information into a global guarantee

A function on a convex domain is convex if

<div class="math-display" markdown="0">\[
f(\lambda x+(1-\lambda)y)\leq\lambda f(x)+(1-\lambda)f(y),\qquad 0\leq\lambda\leq1.
\]</div>

Geometrically, the line segment joining two points on its graph lies on or above the graph.

For a differentiable convex function, an equivalent characterization is

<div class="math-display" markdown="0">\[f(y)\geq f(x)+\nabla f(x)^\top(y-x).\]</div>

The tangent approximation is a lower bound on the entire function.

Now suppose <span class="math-inline" markdown="0">\(\nabla f(x^\star)=0\)</span>. Substituting gives

<div class="math-display" markdown="0">\[f(y)\geq f(x^\star)\qquad\text{for every }y.\]</div>

So <span class="math-inline" markdown="0">\(x^\star\)</span> is a global minimizer.

This is the missing ingredient in the “set the derivative to zero” recipe. For a differentiable convex objective in unconstrained optimization, a zero gradient certifies global optimality.

There are useful distinctions within convexity:

- **Convexity** guarantees that every local minimum is global.
- **Strict convexity** guarantees that there is at most one minimizer.
- **Strong convexity** imposes a positive lower bound on curvature.

For a differentiable <span class="math-inline" markdown="0">\(\mu\)</span>-strongly convex function,

<div class="math-display" markdown="0">\[
f(y)\geq f(x)+\nabla f(x)^\top(y-x)+\frac{\mu}{2}\&#124;y-x\&#124;^2,\qquad\mu&gt;0.
\]</div>

For twice continuously differentiable functions on an open convex domain, the corresponding Hessian conditions are

<div class="math-display" markdown="0">\[
\begin{aligned}
\text{Convexity:}\quad&amp;\nabla^2f(x)\succeq0,\\
\text{Strong convexity:}\quad&amp;\nabla^2f(x)\succeq\mu I.
\end{aligned}
\]</div>

Our quadratic has smallest Hessian eigenvalue <span class="math-inline" markdown="0">\(2\)</span>, so it is <span class="math-inline" markdown="0">\(2\)</span>-strongly convex under the Euclidean norm.

But convex functions need not be smooth bowls. They can have corners.

## A minimum without a derivative

Consider

<div class="math-display" markdown="0">\[f(x)=&#124;x&#124;.\]</div>

To the left of zero, its slope is <span class="math-inline" markdown="0">\(-1\)</span>. To the right, its slope is <span class="math-inline" markdown="0">\(1\)</span>. Since these one-sided derivatives disagree, <span class="math-inline" markdown="0">\(f'(0)\)</span> does not exist.

Yet zero is plainly the global minimizer.

We need an optimality condition that survives this corner. The supporting-line interpretation of convexity provides one.

A vector <span class="math-inline" markdown="0">\(g\)</span> is a **subgradient** of a convex function at <span class="math-inline" markdown="0">\(x_0\)</span> if

<div class="math-display" markdown="0">\[f(x)\geq f(x_0)+g^\top(x-x_0)\qquad\text{for every }x.\]</div>

The affine function on the right touches <span class="math-inline" markdown="0">\(f\)</span> at <span class="math-inline" markdown="0">\(x_0\)</span> and stays below it everywhere.

At a smooth interior point, the gradient is the only such vector. At a corner, several supporting slopes may work.

### Finding every supporting slope of absolute value at zero

Substituting <span class="math-inline" markdown="0">\(f(x)=&#124;x&#124;\)</span> and <span class="math-inline" markdown="0">\(x_0=0\)</span> gives

<div class="math-display" markdown="0">\[&#124;x&#124;\geq gx\qquad\text{for every }x.\]</div>

For <span class="math-inline" markdown="0">\(x&gt;0\)</span>,

<div class="math-display" markdown="0">\[x\geq gx\quad\Longrightarrow\quad g\leq1.\]</div>

For <span class="math-inline" markdown="0">\(x&lt;0\)</span>,

<div class="math-display" markdown="0">\[-x\geq gx\quad\Longrightarrow\quad g\geq-1,\]</div>

where the inequality reverses when we divide by a negative number.

Together,

<div class="math-display" markdown="0">\[-1\leq g\leq1.\]</div>

Every slope in this interval supports the graph from below.

The set of all subgradients is called the **subdifferential**, denoted by <span class="math-inline" markdown="0">\(\partial f(x)\)</span>. For absolute value,

<div class="math-display" markdown="0">\[
\partial f(x)=\begin{cases}
\{-1\},&amp;x&lt;0,\\
[-1,1],&amp;x=0,\\
\{1\},&amp;x&gt;0.
\end{cases}
\]</div>

A subgradient is one vector; the subdifferential is a set of vectors.

For a convex function differentiable at an interior point,

<div class="math-display" markdown="0">\[\partial f(x)=\{\nabla f(x)\}.\]</div>

Boundary points require more care: a convex function can have an empty subdifferential at the boundary of its domain.

## Zero still certifies a minimum

The familiar stationary-point condition now becomes

<div class="math-display" markdown="0">\[\boxed{x^\star\text{ is a global minimizer}\iff0\in\partial f(x^\star).}\]</div>

For a convex objective, this follows directly from the definition. If zero is a subgradient, then

<div class="math-display" markdown="0">\[f(x)\geq f(x^\star)+0^\top(x-x^\star)=f(x^\star).\]</div>

Conversely, if <span class="math-inline" markdown="0">\(x^\star\)</span> is a global minimizer, this inequality holds, so zero is a subgradient.

For absolute value,

<div class="math-display" markdown="0">\[0\in[-1,1]=\partial f(0).\]</div>

We have certified the minimum without needing a derivative there.

The supporting-hyperplane definition is central to convex analysis. General nonconvex, nonsmooth functions require other notions of generalized derivatives; the same conclusions should not be carried over automatically.

## What happens when the objective takes a maximum?

Another common source of corners is a maximum of smooth functions.

Consider

<div class="math-display" markdown="0">\[f(x)=\max(2x,-x).\]</div>

For positive <span class="math-inline" markdown="0">\(x\)</span>, the active branch is <span class="math-inline" markdown="0">\(2x\)</span>. For negative <span class="math-inline" markdown="0">\(x\)</span>, it is <span class="math-inline" markdown="0">\(-x\)</span>. At zero, the branches tie.

Their slopes are <span class="math-inline" markdown="0">\(2\)</span> and <span class="math-inline" markdown="0">\(-1\)</span>. At the tie, every convex combination of those slopes is a subgradient:

<div class="math-display" markdown="0">\[
\begin{aligned}
\partial f(0)&amp;=\{2\alpha-(1-\alpha):0\leq\alpha\leq1\}\\
&amp;=[-1,2].
\end{aligned}
\]</div>

For a finite maximum of differentiable convex functions,

<div class="math-display" markdown="0">\[f(x)=\max_i f_i(x),\]</div>

the general rule is

<div class="math-display" markdown="0">\[\partial f(x)=\operatorname{conv}\{\nabla f_i(x):i\in A(x)\},\]</div>

where

<div class="math-display" markdown="0">\[A(x)=\{i:f_i(x)=f(x)\}\]</div>

is the active set.

Only branches attaining the maximum contribute. When one branch is active, its gradient determines the subdifferential. When several tie, we take the convex hull of their gradients.

## Subgradient steps behave differently

Subgradient descent replaces the gradient with a selected subgradient:

<div class="math-display" markdown="0">\[x_{t+1}=x_t-\eta_tg_t,\qquad g_t\in\partial f(x_t).\]</div>

For <span class="math-inline" markdown="0">\(f(x)=&#124;x&#124;\)</span>, starting at <span class="math-inline" markdown="0">\(x_0=2\)</span> with step size <span class="math-inline" markdown="0">\(0.5\)</span> gives

<div class="math-display" markdown="0">\[2\rightarrow1.5\rightarrow1\rightarrow0.5\rightarrow0.\]</div>

At zero, choosing <span class="math-inline" markdown="0">\(g=0\)</span> keeps the iterate at the minimum.

This example lands exactly at the optimum. A slightly different starting point shows why step sizes matter. Starting at <span class="math-inline" markdown="0">\(0.2\)</span> with the same fixed step size gives

<div class="math-display" markdown="0">\[0.2\rightarrow-0.3\rightarrow0.2\rightarrow-0.3\rightarrow\cdots.\]</div>

The iterates oscillate, and the objective increases on every move from <span class="math-inline" markdown="0">\(0.2\)</span> to <span class="math-inline" markdown="0">\(-0.3\)</span>.

A subgradient step need not decrease the function at each iteration. Convergence guarantees therefore depend on assumptions about the objective, the step-size schedule, and which iterate or average is reported.

To understand the stronger descent guarantees available for smooth functions, we need to distinguish two kinds of Lipschitz continuity.

## Bounding the function versus bounding its gradient

A function is <span class="math-inline" markdown="0">\(B\)</span>-Lipschitz if

<div class="math-display" markdown="0">\[&#124;f(x)-f(y)&#124;\leq B\&#124;x-y\&#124;.\]</div>

This bounds changes in function values.

Absolute value is <span class="math-inline" markdown="0">\(1\)</span>-Lipschitz because

<div class="math-display" markdown="0">\[\bigl&#124;&#124;x&#124;-&#124;y&#124;\bigr&#124;\leq&#124;x-y&#124;.\]</div>

It is still nondifferentiable at zero.

A differentiable function is <span class="math-inline" markdown="0">\(L\)</span>-smooth if its gradient is <span class="math-inline" markdown="0">\(L\)</span>-Lipschitz:

<div class="math-display" markdown="0">\[\&#124;\nabla f(x)-\nabla f(y)\&#124;\leq L\&#124;x-y\&#124;.\]</div>

This bounds changes in slope.

For <span class="math-inline" markdown="0">\(f(x)=x^2\)</span>,

<div class="math-display" markdown="0">\[&#124;f'(x)-f'(y)&#124;=2&#124;x-y&#124;,\]</div>

so the function is <span class="math-inline" markdown="0">\(2\)</span>-smooth. However, it is not globally Lipschitz on <span class="math-inline" markdown="0">\(\mathbb R\)</span>: its slope grows without bound.

These conditions control different quantities.

### Why smoothness helps choose a step size

For an <span class="math-inline" markdown="0">\(L\)</span>-smooth function, the descent lemma gives

<div class="math-display" markdown="0">\[f(y)\leq f(x)+\nabla f(x)^\top(y-x)+\frac{L}{2}\&#124;y-x\&#124;^2.\]</div>

The quadratic term bounds the error in the first-order approximation.

Taking a gradient step with <span class="math-inline" markdown="0">\(L&gt;0\)</span>,

<div class="math-display" markdown="0">\[y=x-\frac1L\nabla f(x),\]</div>

yields

<div class="math-display" markdown="0">\[f\left(x-\frac1L\nabla f(x)\right)\leq f(x)-\frac{1}{2L}\&#124;\nabla f(x)\&#124;^2.\]</div>

Unless the gradient is zero, the objective decreases.

This descent statement does not require convexity. Convexity becomes important when we want to connect progress to a global minimum.

For twice continuously differentiable, convex functions on an open convex domain, smoothness corresponds to an upper curvature bound. Combining it with strong convexity gives

<div class="math-display" markdown="0">\[\mu I\preceq\nabla^2f(x)\preceq LI.\]</div>

The lower bound prevents excessively flat directions; the upper bound limits how sharply the function can bend.

## Proximal methods make use of nonsmooth structure

Many learning problems combine a smooth loss with a nonsmooth regularizer:

<div class="math-display" markdown="0">\[\min_w F(w)=f(w)+h(w).\]</div>

A simple example is

<div class="math-display" markdown="0">\[F(w)=\frac12(w-3)^2+\lambda&#124;w&#124;,\qquad\lambda\geq0.\]</div>

The squared-error term is smooth. The absolute-value penalty has a corner.

Proximal gradient descent treats these terms separately. First, take a gradient step on the smooth part:

<div class="math-display" markdown="0">\[v_t=w_t-\eta\nabla f(w_t).\]</div>

Then apply the proximal operator of the regularizer:

<div class="math-display" markdown="0">\[w_{t+1}=\operatorname{prox}_{\eta h}(v_t),\]</div>

where

<div class="math-display" markdown="0">\[\operatorname{prox}_{\eta h}(v)=\arg\min_w\left\{h(w)+\frac{1}{2\eta}\&#124;w-v\&#124;^2\right\}.\]</div>

This small optimization problem balances reducing the regularizer against staying close to the gradient-step result.

For <span class="math-inline" markdown="0">\(h(w)=\lambda&#124;w&#124;\)</span>, its optimality condition is

<div class="math-display" markdown="0">\[0\in\lambda\,\partial&#124;w&#124;+\frac{w-v}{\eta}.\]</div>

Solving separately for positive, negative, and zero <span class="math-inline" markdown="0">\(w\)</span> gives **soft thresholding**:

<div class="math-display" markdown="0">\[
\operatorname{prox}_{\eta\lambda&#124;\cdot&#124;}(v)=\begin{cases}
v-\eta\lambda,&amp;v&gt;\eta\lambda,\\
0,&amp;&#124;v&#124;\leq\eta\lambda,\\
v+\eta\lambda,&amp;v&lt;-\eta\lambda.
\end{cases}
\]</div>

Equivalently,

<div class="math-display" markdown="0">\[\operatorname{prox}_{\eta\lambda&#124;\cdot&#124;}(v)=\operatorname{sign}(v)\max(&#124;v&#124;-\eta\lambda,0).\]</div>

Small values become exactly zero. This is the mechanism behind the sparsity encouraged by <span class="math-inline" markdown="0">\(L_1\)</span> regularization.

For the scalar example above, taking <span class="math-inline" markdown="0">\(\eta=1\)</span> gives

<div class="math-display" markdown="0">\[v=w-(w-3)=3.\]</div>

Applying soft thresholding immediately produces the minimizer:

<div class="math-display" markdown="0">\[w^\star=\max(3-\lambda,0).\]</div>

The subdifferential provides the condition that makes this derivation possible.

## The connection to Mixture of Experts—and its limit

A dense Mixture of Experts combines expert outputs using gating weights:

<div class="math-display" markdown="0">\[\hat y=\sum_iG_i(x)E_i(x).\]</div>

For scalar expert outputs, the chain rule gives

<div class="math-display" markdown="0">\[
\frac{\partial\mathcal L}{\partial E_i}=G_i\frac{\partial\mathcal L}{\partial\hat y},\qquad
\frac{\partial\mathcal L}{\partial G_i}=E_i\frac{\partial\mathcal L}{\partial\hat y}.
\]</div>

These derivatives describe how the loss changes with each expert output and gating weight. Backpropagation carries them through the networks producing those quantities.

Hard routing introduces a different operation:

<div class="math-display" markdown="0">\[i^\star=\arg\max_iG_i(x).\]</div>

It is tempting to treat this as another application of the maximum rule. But the maximum value and the index attaining that maximum are different objects.

The function

<div class="math-display" markdown="0">\[m(x)=\max_iG_i(x)\]</div>

returns a score. The convex subgradient rule applies when its component score functions satisfy the relevant convexity and differentiability assumptions.

The expression

<div class="math-display" markdown="0">\[\arg\max_iG_i(x)\]</div>

selects an index. If that index determines which expert output is used, crossing a routing boundary can switch between different outputs. The resulting model can even be discontinuous.

Understanding subgradients helps us analyze maximum-score functions, but it does not automatically solve differentiation through discrete routing.

## Putting the ideas together

The derivative of <span class="math-inline" markdown="0">\(x^2\)</span>, the corner of <span class="math-inline" markdown="0">\(&#124;x&#124;\)</span>, and the soft-thresholding operator are parts of the same story.

Derivatives and gradients describe local change. The Hessian describes how that local change varies. Convexity lets a local supporting condition certify a global minimum. At a corner, subgradients preserve that supporting geometry even when ordinary derivatives fail.

Algorithm design then depends on the structure available. Smoothness gives control over gradient steps. Nonsmooth convex objectives admit subgradient methods. A smooth loss paired with a structured regularizer often leads naturally to a proximal method.

Before choosing an optimizer, it is worth asking what the objective allows us to know: whether it is differentiable, whether it is convex, how its curvature behaves, and whether its nonsmooth terms can be handled directly.

Those questions explain both why familiar methods work and where their guarantees stop.

## A small problem to check your understanding

Consider

<div class="math-display" markdown="0">\[f(x)=\max(2x,-x).\]</div>

1. Why is <span class="math-inline" markdown="0">\(f\)</span> convex?
2. Is it differentiable at zero?
3. What is <span class="math-inline" markdown="0">\(\partial f(0)\)</span>?
4. Does the subdifferential certify that zero is a global minimizer?
5. Starting from <span class="math-inline" markdown="0">\(x_0=2\)</span>, what is one subgradient step with <span class="math-inline" markdown="0">\(\eta=0.5\)</span>?

<details markdown="1">
<summary>Show the solution</summary>

The maximum of two affine functions is convex. At zero, its left and right slopes are <span class="math-inline" markdown="0">\(-1\)</span> and <span class="math-inline" markdown="0">\(2\)</span>, so it is not differentiable there. Its subdifferential is <span class="math-inline" markdown="0">\([-1,2]\)</span>, which contains zero and therefore certifies a global minimum. At <span class="math-inline" markdown="0">\(x_0=2\)</span>, the active branch is <span class="math-inline" markdown="0">\(2x\)</span>, so the subgradient is <span class="math-inline" markdown="0">\(2\)</span> and

<div class="math-display" markdown="0">\[x_1=2-0.5(2)=1.\]</div>

</details>
