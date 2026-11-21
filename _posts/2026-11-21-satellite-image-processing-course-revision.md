---
layout: essay
title: "Understanding Satellite Image Processing: From Pixels to Intelligence"
description: "A GNR607 course revision guide, from image formation and enhancement to classification, accuracy assessment, and change detection."
excerpt: "A course-wide GNR607 reference with key equations, worked numericals, practical interpretation, and exam pitfalls."
date: 2026-11-21
permalink: /blog/satellite-image-processing-course-revision/
eyebrow: "GNR607 · Course revision reference"
topic: vision
math: true
native_article: true
course_reference: true
tags: [remote sensing, image processing, revision, classification]
toc:
  - {id: reading-map, title: "How to use this guide"}
  - {id: image-formation, title: "1. Images, sampling, and resolution"}
  - {id: storage, title: "2. Multispectral storage"}
  - {id: histograms, title: "3. Contrast and histograms"}
  - {id: filtering, title: "4. Spatial and frequency filtering"}
  - {id: edges, title: "5. Edges, Hough, and objects"}
  - {id: color, title: "6. Colour and false-colour images"}
  - {id: morphology, title: "7. Mathematical morphology"}
  - {id: texture, title: "8. Texture and GLCM"}
  - {id: features, title: "9. PCA and spectral features"}
  - {id: supervised, title: "10. Supervised classification"}
  - {id: unsupervised, title: "11. Clustering"}
  - {id: assessment, title: "12. Accuracy assessment"}
  - {id: indices, title: "13. Mixed pixels and indices"}
  - {id: change, title: "14. Fusion and change detection"}
  - {id: supporting-ml, title: "15. Supporting ML concepts"}
  - {id: practice, title: "16. Worked revision problems"}
  - {id: formula-sheet, title: "17. Formula sheet and pitfalls"}
---

A satellite image is a record of measured radiation. It does not arrive with labels saying *forest*, *road*, or *water*. We turn measurements into those interpretations through a sequence of choices: calibrate and align the image, improve its visibility, describe its spectral and spatial patterns, classify what we see, and assess how reliable the result is.

**Course:** GNR607, Principles of Satellite Image Processing · **Instructor:** Prof. B. Krishna Mohan, IIT Bombay.

This guide follows that sequence. It grew from my GNR607 revision notes, discussions, numerical exercises, and an image-processing project. It is a reconstruction for revision, not a verified transcript of every lecture or an official syllabus. The general machine-learning material appears near the end as supporting context.

**The course in one line:** radiation → sensor samples → pixels and bands → enhancement → features and objects → classification → validation → change.

## How to use this guide
{: #reading-map}

Read sections 1–4 to establish what the numbers in an image mean. Sections 5–9 explain how local structures and useful features emerge. Sections 10–14 connect those features to maps and decisions. The worked problems and formula sheet are for a final pass. Expand a solution only after trying it yourself; use “Print notes” to keep a copy with all solutions visible.

## 1. Images, sampling, and sensor resolution
{: #image-formation}

A grayscale digital image is a grid <span class="math-inline" markdown="0">\(I(r,c)\)</span> of sampled and quantized measurements. A multispectral pixel is a vector <span class="math-inline" markdown="0">\(x(r,c)=[B_1(r,c),\ldots,B_K(r,c)]^\top\)</span>, and the image is an array in <span class="math-inline" markdown="0">\(\mathbb R^{H\times W\times K}\)</span>. The band values may be raw digital numbers, calibrated radiance, or surface reflectance. Those are different physical quantities; check the processing level before comparing images.

**Sampling** chooses spatial locations. For fixed ground coverage, halving both pixel dimensions roughly quadruples the pixel count. **Quantization** chooses discrete output levels: <span class="math-inline" markdown="0">\(b\)</span> bits allow <span class="math-inline" markdown="0">\(2^b\)</span> possible codes. It does not imply that the sensor can resolve all <span class="math-inline" markdown="0">\(2^b\)</span> levels above its noise floor.

| Resolution | Main question |
| --- | --- |
| Spatial | How small a ground feature can be distinguished? |
| Spectral | How narrow and how numerous are the wavelength bands? |
| Radiometric | How finely can measured radiation be distinguished? |
| Temporal | How often is the same place observed? |

Pixel spacing is not the entire spatial-resolution story: optics, detector response, motion, and resampling also blur detail. Narrower bands or smaller pixels may collect fewer photons, so improving one resolution can create a signal-to-noise trade-off. Revisit time also depends on orbit, viewing geometry, and cloud cover.

<details markdown="1" data-proof><summary>Worked numerical: image storage</summary>

For 1,000 rows, 1,000 columns, four bands, and eight bits per sample, uncompressed sample storage is

<div class="math-display" markdown="0">\[S=1000\times1000\times4\times8/8=4{,}000{,}000\text{ bytes}.\]</div>

That is 4 MB in decimal units, or about 3.81 MiB. Metadata, padding, compression, and file headers change actual file size. Halving pixel width and height over the same footprint gives about four times as many samples.

</details>

## 2. How multispectral pixels are stored
{: #storage}

The same two-band, two-by-two image can be laid out in several ways. Let band 1 be <span class="math-inline" markdown="0">\([1,2;3,4]\)</span> and band 2 be <span class="math-inline" markdown="0">\([5,6;7,8]\)</span> in row-major order.

| Layout | Sample sequence | Convenient access |
| --- | --- | --- |
| BSQ, band sequential | 1,2,3,4, 5,6,7,8 | A whole band |
| BIL, band interleaved by line | 1,2, 5,6, 3,4, 7,8 | All bands for a line |
| BIP, band interleaved by pixel | 1,5, 2,6, 3,7, 4,8 | A pixel's spectral vector |

The layouts contain identical samples and require identical uncompressed sample storage when dimensions and data types match. Their distinction is access pattern, not scientific content. A file reader also needs dimensions, data type, byte order, and often georeferencing metadata.

## 3. Enhancement: contrast and histograms
{: #histograms}

Enhancement makes patterns easier to see. It may change display values without adding information to the original measurement. Keep a display stretch distinct from a physical reflectance correction.

A linear min–max stretch maps <span class="math-inline" markdown="0">\(f_{\min}\)</span> to zero and <span class="math-inline" markdown="0">\(f_{\max}\)</span> to 255:

<div class="math-display" markdown="0">\[g=255\frac{f-f_{\min}}{f_{\max}-f_{\min}}.\]</div>

With endpoints 50 and 150, the value 100 maps to 127.5 before rounding. The formula requires different endpoints; clipping is needed for values outside the chosen range. Percentile endpoints help when isolated outliers would otherwise compress most of the display contrast.

For histogram equalization, count <span class="math-inline" markdown="0">\(n_k\)</span> pixels at level <span class="math-inline" markdown="0">\(r_k\)</span> among <span class="math-inline" markdown="0">\(N\)</span> pixels, set <span class="math-inline" markdown="0">\(p_k=n_k/N\)</span>, and compute <span class="math-inline" markdown="0">\(C_k=\sum_{j\le k}p_j\)</span>. One discrete rule is <span class="math-inline" markdown="0">\(s_k=\lfloor(L-1)C_k\rfloor\)</span>. Rounding conventions differ, and a discrete output histogram need not become uniform.

<details markdown="1" data-proof><summary>Worked numerical: equalize four pixels</summary>

For <span class="math-inline" markdown="0">\([0,0,1,3]\)</span> with <span class="math-inline" markdown="0">\(L=4\)</span>, the probabilities at levels 0–3 are <span class="math-inline" markdown="0">\((0.5,0.25,0,0.25)\)</span>. The CDF is <span class="math-inline" markdown="0">\((0.5,0.75,0.75,1)\)</span>. Flooring <span class="math-inline" markdown="0">\(3C_k\)</span> maps the observed levels <span class="math-inline" markdown="0">\(0\mapsto1\)</span>, <span class="math-inline" markdown="0">\(1\mapsto2\)</span>, and <span class="math-inline" markdown="0">\(3\mapsto3\)</span>. The output is <span class="math-inline" markdown="0">\([1,1,2,3]\)</span>. A different stated rounding rule can give different output codes.

</details>

Histogram specification tries to match a target distribution, often via CDF mapping. It is useful for visual or statistical normalization across scenes, but a matching histogram does not establish equal physical reflectance. Equalization may amplify noise or change brightness, especially if applied globally to a heterogeneous image.

## 4. Spatial and frequency-domain filtering
{: #filtering}

A spatial filter combines pixels in a neighborhood. A 3×3 mean kernel has nine weights of <span class="math-inline" markdown="0">\(1/9\)</span>; it reduces fluctuations but blurs boundaries. A median filter is nonlinear and resists isolated impulse noise: the median of <span class="math-inline" markdown="0">\([10,11,12,13,255]\)</span> is 12, while the mean is 60.2. Gaussian smoothing places more weight near the center. Adaptive filters vary smoothing according to local statistics and noise estimates.

**Correlation** applies a kernel as written. **Convolution** reverses it in both dimensions. For the patch <span class="math-inline" markdown="0">\([1,2;3,4]\)</span> and kernel <span class="math-inline" markdown="0">\([1,0;0,-1]\)</span>, aligned correlation is <span class="math-inline" markdown="0">\(-3\)</span> and convolution using the flipped kernel is <span class="math-inline" markdown="0">\(3\)</span>. Symmetric kernels give the same result under matching boundary and alignment conventions. Many software libraries call an operation “convolution” while implementing correlation, so inspect the convention.

The 2D discrete Fourier transform decomposes an image into spatial frequencies:

<div class="math-display" markdown="0">\[F(u,v)=\sum_{x=0}^{M-1}\sum_{y=0}^{N-1}f(x,y)e^{-2\pi i(ux/M+vy/N)}.\]</div>

Slow variation tends to occupy low frequencies; rapid transitions contribute high frequencies. This is a useful intuition, not a perfect separation: sharp boundaries affect a range of frequencies, and noise can occur at several scales. A frequency filter computes <span class="math-inline" markdown="0">\(G(u,v)=H(u,v)F(u,v)\)</span> and then applies the inverse transform.

For <span class="math-inline" markdown="0">\(H(u,v)=e^{-k(u^2+v^2)}\)</span> with <span class="math-inline" markdown="0">\(k&gt;0\)</span>, <span class="math-inline" markdown="0">\(H(0,0)=1\)</span> and higher frequencies decay toward zero. It is a Gaussian low-pass response in the stated frequency coordinates. Larger <span class="math-inline" markdown="0">\(k\)</span> attenuates nonzero frequencies more strongly. The complementary high-pass response is <span class="math-inline" markdown="0">\(1-H\)</span>. A sharp ideal cutoff often creates ringing; the Gaussian transition is smoother.

## 5. Edges, lines, and object candidates
{: #edges}

An edge is a strong image change; it might trace a building, road, shadow, cloud boundary, or calibration artifact. The image gradient <span class="math-inline" markdown="0">\(\nabla I=(I_x,I_y)^\top\)</span> has magnitude <span class="math-inline" markdown="0">\(\sqrt{I_x^2+I_y^2}\)</span> and direction <span class="math-inline" markdown="0">\(\operatorname{atan2}(I_y,I_x)\)</span>. Sobel masks approximate the two components using local weighted differences.

The Laplacian <span class="math-inline" markdown="0">\(\nabla^2I=I_{xx}+I_{yy}\)</span> responds to rapid changes but also to noise. Laplacian of Gaussian first smooths, then takes a Laplacian; candidate edges are found from sufficiently strong zero crossings.

Canny combines Gaussian smoothing, gradient estimation, non-maximum suppression, a high and low threshold, and hysteresis. The high threshold marks confident edges; the lower threshold lets connected weak segments survive. Its output depends on scale and thresholds.

Hough line detection maps an edge point <span class="math-inline" markdown="0">\((x,y)\)</span> to line parameters via

<div class="math-display" markdown="0">\[\rho=x\cos\theta+y\sin\theta.\]</div>

Votes accumulate where many points support one line. Standard Hough identifies line parameters; probabilistic variants often sample edge points and return finite segments. A peak is geometric evidence, not proof that a whole semantic object exists.

**Project example: rectangle detection.** A practical pipeline is grayscale → smoothing → Canny → selective morphology → Hough segments → geometric checks. A rectangle candidate needs two approximately parallel pairs, near-perpendicular pair orientations, plausible intersections, and size constraints. Check the source image too: shadows and roof texture can create convincing false rectangles. Canny thresholds, structuring-element shape, minimum segment length, Hough vote threshold, and gap tolerance all influence the outcome.

## 6. Colour and false-colour interpretation
{: #color}

RGB is additive light; ideal full red plus green appears yellow. CMYK is subtractive ink; ideal magenta plus yellow yields red. These are display and printing models, not the same as a sensor's calibrated spectral bands.

HSI separates hue, saturation, and intensity. In one standard HSI convention,

<div class="math-display" markdown="0">\[I=(R+G+B)/3,\qquad S=1-\frac{3\min(R,G,B)}{R+G+B},\]</div>

for nonblack input. For <span class="math-inline" markdown="0">\((R,G,B)=(0.7,0.3,0)\)</span>, saturation is 1, or 100%, despite red being 70% of the channel sum. At black the denominator vanishes, so saturation must be defined by convention. Other colour models define saturation differently.

A false-colour composite maps selected sensor bands to visible display channels. Putting near-infrared in the red channel commonly makes healthy vegetation appear bright red because vegetation reflects NIR strongly. The displayed red is a visualization choice, not a claim that the surface emits visible red light.

## 7. Mathematical morphology
{: #morphology}

Morphology probes shape with a structuring element <span class="math-inline" markdown="0">\(B\)</span>. In binary morphology, erosion <span class="math-inline" markdown="0">\(A\ominus B\)</span> keeps locations where the translated element fits inside foreground <span class="math-inline" markdown="0">\(A\)</span>; dilation <span class="math-inline" markdown="0">\(A\oplus B\)</span> expands foreground according to <span class="math-inline" markdown="0">\(B\)</span>. Orientation matters for nonsymmetric elements.

Opening and closing compose these operations:

<div class="math-display" markdown="0">\[A\circ B=(A\ominus B)\oplus B,\qquad A\bullet B=(A\oplus B)\ominus B.\]</div>

Opening removes small foreground features; closing fills small background gaps. Under standard definitions, opening is anti-extensive, closing is extensive, and both are idempotent. With an SE containing the origin, erosion is contained in opening, which is contained in the original set; the original is contained in closing, which is contained in dilation.

For a flat grayscale element, erosion selects a local minimum and dilation a local maximum over their respective reflected neighborhoods. The same ordering holds pointwise when the SE contains the origin. A repeated dilation can propagate the image's actual maximum across a finite connected domain. It does not invent a value of 255.

<details markdown="1" data-proof><summary>Worked numerical: cross-shaped closing</summary>

Take the 5×5 image

<div class="math-display" markdown="0">\[\begin{bmatrix}25&amp;60&amp;28&amp;29&amp;27\\59&amp;56&amp;57&amp;20&amp;19\\25&amp;59&amp;29&amp;32&amp;20\\20&amp;33&amp;28&amp;29&amp;27\\24&amp;31&amp;29&amp;27&amp;25\end{bmatrix}\]</div>

and a 3×3 cross containing the center and four axial neighbors. To close the center pixel, first dilate at the center and all four axial neighbors. Those five dilated values are 59 at center, 57 above, 33 below, 59 left, and 32 right. Their minimum is **32**. The computation assumes the displayed neighborhood is interior, so no boundary rule is needed. A one-step min or max on the original center neighborhood would be the wrong operation.

</details>

Hit-or-miss looks for foreground and background simultaneously:

<div class="math-display" markdown="0">\[A\otimes(B_1,B_2)=(A\ominus B_1)\cap(A^c\ominus B_2).\]</div>

It can detect endpoints or corners, but one wrong required pixel can break a match. White top-hat <span class="math-inline" markdown="0">\(I-(I\circ B)\)</span> extracts bright structures removed by opening; black top-hat <span class="math-inline" markdown="0">\((I\bullet B)-I\)</span> extracts small dark structures filled by closing. Morphological gradient is dilation minus erosion. Thinning and skeletonization reduce shapes to compact line structures while attempting to preserve topology.

## 8. Texture and the GLCM
{: #texture}

A histogram counts intensity values. Texture records how those values occur together in space. A gray-level co-occurrence matrix <span class="math-inline" markdown="0">\(G(i,j)\)</span> counts pixel pairs of levels <span class="math-inline" markdown="0">\(i\)</span> and <span class="math-inline" markdown="0">\(j\)</span> at a chosen offset. Normalize by the number of eligible pairs to obtain <span class="math-inline" markdown="0">\(P(i,j)\)</span>; specify distance, direction, and whether pairs are symmetrized.

For <span class="math-inline" markdown="0">\(I=[1,1;0,0]\)</span>, the immediate right-neighbor pairs are <span class="math-inline" markdown="0">\((1,1)\)</span> and <span class="math-inline" markdown="0">\((0,0)\)</span>, giving <span class="math-inline" markdown="0">\(P=\operatorname{diag}(0.5,0.5)\)</span>. Common descriptors are:

| Descriptor | Formula | Reading |
| --- | --- | --- |
| ASM | <span class="math-inline" markdown="0">\(\sum_{i,j}P(i,j)^2\)</span> | Concentration of pair probabilities |
| Contrast | <span class="math-inline" markdown="0">\(\sum_{i,j}(i-j)^2P(i,j)\)</span> | Local gray-level difference |
| Entropy | <span class="math-inline" markdown="0">\(-\sum_{i,j}P(i,j)\log_2P(i,j)\)</span> | Pair-distribution uncertainty |
| Homogeneity | <span class="math-inline" markdown="0">\(\sum_{i,j}P(i,j)/(1+(i-j)^2)\)</span> | Weight near the diagonal |
| Dissimilarity | <span class="math-inline" markdown="0">\(\sum_{i,j}&#124;i-j&#124;P(i,j)\)</span> | Mean absolute difference |

Treat <span class="math-inline" markdown="0">\(0\log0\)</span> as zero. Correlation standardizes <span class="math-inline" markdown="0">\(\sum(i-\mu_i)(j-\mu_j)P(i,j)\)</span> by the two marginal standard deviations; it is undefined when one is zero. In the example, ASM is 0.5, contrast is zero, and entropy is one bit. Direction matters: horizontal stripes can be smooth horizontally yet variable vertically.

**Sum-and-difference histograms** count <span class="math-inline" markdown="0">\(s=x+y\)</span> and <span class="math-inline" markdown="0">\(d=x-y\)</span> for neighboring pixels. With <span class="math-inline" markdown="0">\(L\)</span> integer gray levels their storage is <span class="math-inline" markdown="0">\(O(L)\)</span>, compared with <span class="math-inline" markdown="0">\(O(L^2)\)</span> for a dense GLCM. For equal marginal variances and positive covariance, centered and normalized sum and difference align with the two PCA directions. Product <span class="math-inline" markdown="0">\(xy\)</span> can have a large range; ratio <span class="math-inline" markdown="0">\(x/y\)</span> is unstable near zero.

## 9. PCA, bands, and class separability
{: #features}

PCA centers spectral vectors, computes their covariance <span class="math-inline" markdown="0">\(\Sigma\)</span>, and diagonalizes it: <span class="math-inline" markdown="0">\(\Sigma v_i=\lambda_i v_i\)</span>. Components are uncorrelated in the sample covariance and sorted by variance. Explained variance for component <span class="math-inline" markdown="0">\(i\)</span> is <span class="math-inline" markdown="0">\(\lambda_i/\sum_j\lambda_j\)</span>. Eigenvalues <span class="math-inline" markdown="0">\((60,25,10,3,2)\)</span> sum to 100, so the first three retain **95%** of variance.

PC1 often captures common brightness when bands are strongly positively correlated; later components may encode band contrasts. Inspect eigenvector loadings before assigning meaning. PCA preserves variance, not labels or class separation. Selecting bands retains original measurements; extracting features constructs new ones, such as PCs, ratios, indices, or texture measures.

The **Hughes phenomenon** describes performance that initially improves and then worsens as feature dimension grows with limited training data. A full <span class="math-inline" markdown="0">\(n\)</span>-band covariance matrix needs <span class="math-inline" markdown="0">\(n(n+1)/2\)</span> distinct parameters per class; regularization, feature reduction, and better samples can help.

For Gaussian classes, Bhattacharyya distance combines a mean-separation term and a covariance-volume term:

<div class="math-display" markdown="0">\[B=\tfrac18(\mu_i-\mu_j)^\top\bar\Sigma^{-1}(\mu_i-\mu_j)+\tfrac12\log\frac{&#124;\bar\Sigma&#124;}{\sqrt{&#124;\Sigma_i&#124;&#124;\Sigma_j&#124;}},\quad\bar\Sigma=(\Sigma_i+\Sigma_j)/2.\]</div>

One convention for Jeffries–Matusita separation is <span class="math-inline" markdown="0">\(JM=2(1-e^{-B})\)</span>, approaching 2 as separation grows. Specify the convention because some texts use a square-root scaling. A symmetrized KL divergence is nonnegative and symmetric but need not satisfy the triangle inequality. An invertible full-dimensional PCA rotation preserves information-theoretic divergence; selecting a subset may help a finite-sample classifier while discarding information.

## 10. Supervised spectral classification
{: #supervised}

Supervised methods use reference-labeled examples to learn a decision rule. The feature vector may include bands, indices, texture, and spatial context. Training quality and sampling design matter as much as classifier complexity.

| Method | Decision rule | Main limitation |
| --- | --- | --- |
| Minimum distance to mean | Smallest <span class="math-inline" markdown="0">\(\&#124;x-\mu_i\&#124;_2\)</span> | Ignores class spread and covariance |
| Parallelepiped | Inside each band's class interval | Overlaps and uncovered pixels |
| Gaussian maximum likelihood | Largest <span class="math-inline" markdown="0">\(p(x\mid C_i)P(C_i)\)</span> | Needs reliable means and covariances |
| K-nearest neighbors | Vote among nearest training vectors | Storage and distance cost; scaling matters |
| Spectral angle mapper | Smallest angle to reference spectrum | Shape based, ignores positive scale |
| SVM | Margin-based decision surface | Kernel and regularization choices |

A parallelepiped class with band ranges <span class="math-inline" markdown="0">\(20\le B_1\le40\)</span> and <span class="math-inline" markdown="0">\(30\le B_2\le60\)</span> rejects <span class="math-inline" markdown="0">\((35,65)\)</span> because the second band is out of range. Other pixels may fit several boxes; the implementation needs a tie rule.

For Gaussian maximum likelihood with positive-definite <span class="math-inline" markdown="0">\(\Sigma_i\)</span>, compare

<div class="math-display" markdown="0">\[g_i(x)=-\tfrac12(x-\mu_i)^\top\Sigma_i^{-1}(x-\mu_i)-\tfrac12\log&#124;\Sigma_i&#124;+\log P(C_i).\]</div>

The first quadratic is Mahalanobis distance squared. The determinant and prior also matter. Equal covariance matrices produce linear boundaries; different covariances generally produce quadratic ones. Singular estimated covariance needs regularization or a different model. A rejection threshold can prevent forced labels.

KNN neighbors are near in **feature space**, not necessarily adjacent on the map. For neighbor labels <span class="math-inline" markdown="0">\([C_1,C_1,C_2]\)</span> at <span class="math-inline" markdown="0">\(K=3\)</span>, predict <span class="math-inline" markdown="0">\(C_1\)</span>. Standardizing features matters when different bands or derived measures have different scales.

Spectral angle mapper computes <span class="math-inline" markdown="0">\(\theta=\cos^{-1}[(x^\top v)/(\&#124;x\&#124;\&#124;v\&#124;)]\)</span> for nonzero vectors. If <span class="math-inline" markdown="0">\(v=2x\)</span>, the angle is zero although Euclidean distance is nonzero. Atmospheric and sensor effects are not always pure scaling, so angle invariance alone does not solve cross-scene comparison.

A linear SVM uses <span class="math-inline" markdown="0">\(w^\top x+b=0\)</span>; an RBF kernel uses <span class="math-inline" markdown="0">\(e^{-\gamma\&#124;x-z\&#124;^2}\)</span>. A perceptron updates a misclassified labeled point via <span class="math-inline" markdown="0">\(w\leftarrow w+\eta yx\)</span>, <span class="math-inline" markdown="0">\(b\leftarrow b+\eta y\)</span>. A single linear decision surface cannot separate XOR in its original two-dimensional input space.

## 11. Unsupervised classification
{: #unsupervised}

Clustering groups pixels without land-cover labels. A spectral cluster requires interpretation before it becomes a thematic class.

K-means minimizes <span class="math-inline" markdown="0">\(J=\sum_{k=1}^{K}\sum_{x\in C_k}\&#124;x-\mu_k\&#124;^2\)</span> by alternating nearest-center assignment and center recomputation. The objective does not increase under exact alternating steps, but the final solution depends on initialization and can be local. Standard k-means fixes <span class="math-inline" markdown="0">\(K\)</span>; ISODATA can split dispersed clusters, merge nearby clusters, and remove small clusters according to thresholds.

<details markdown="1" data-proof><summary>Worked numerical: one k-means iteration</summary>

For points <span class="math-inline" markdown="0">\([1,2,8,9]\)</span>, start two centers at 1 and 9. Assignment gives clusters <span class="math-inline" markdown="0">\(\{1,2\}\)</span> and <span class="math-inline" markdown="0">\(\{8,9\}\)</span>; new centers are 1.5 and 8.5. The sum of squared deviations is <span class="math-inline" markdown="0">\(4(0.5)^2=1\)</span>. Assignments remain stable at those centers.

</details>

## 12. Confusion matrices and validation
{: #assessment}

A map's appearance cannot establish accuracy. Compare predictions with independent reference labels and state how test locations were sampled. For a table with **rows as predictions** and **columns as actual classes**:

| Predicted / actual | Forest | Water | Row total |
| --- | ---: | ---: | ---: |
| Forest | 40 | 10 | 50 |
| Water | 20 | 30 | 50 |
| Column total | 60 | 40 | 100 |

Overall accuracy is <span class="math-inline" markdown="0">\((40+30)/100=70\%\)</span>. Forest **user's accuracy** is <span class="math-inline" markdown="0">\(40/50=80\%\)</span>: of pixels labeled Forest, how many truly are Forest? It is precision. Forest **producer's accuracy** is <span class="math-inline" markdown="0">\(40/60\approx66.67\%\)</span>: of actual Forest pixels, how many did we capture? It is recall. Commission error is <span class="math-inline" markdown="0">\(1-UA=20\%\)</span>; omission error is <span class="math-inline" markdown="0">\(1-PA\approx33.33\%\)</span>.

Kappa compares observed agreement <span class="math-inline" markdown="0">\(P_o\)</span> with agreement expected from row and column marginals <span class="math-inline" markdown="0">\(P_e\)</span>: <span class="math-inline" markdown="0">\(\kappa=(P_o-P_e)/(1-P_e)\)</span>. Here <span class="math-inline" markdown="0">\(P_e=[50(60)+50(40)]/100^2=0.5\)</span>, so <span class="math-inline" markdown="0">\(\kappa=(0.7-0.5)/(1-0.5)=0.4\)</span>. Kappa is sensitive to prevalence; report the matrix and class-specific measures too.

**Validation design changes the answer.** Leave-one-out uses <span class="math-inline" markdown="0">\(N-1\)</span> training samples for each of <span class="math-inline" markdown="0">\(N\)</span> tests. K-fold uses each fold for validation once. Stratification preserves class proportions, but random splits of neighboring satellite pixels can leak spatial similarity into both train and test. Geographic holdouts better test transfer to new areas. The reference label, acquisition date, mapping unit, registration, and sampling frame all affect estimates. Small tests mainly increase uncertainty; they are not automatically biased. Reusing training samples or selecting only easy sites usually creates optimistic estimates.

## 13. Mixed pixels and spectral indices
{: #indices}

A coarse pixel can contain multiple materials. A linear mixture model writes <span class="math-inline" markdown="0">\(x=\sum_{k=1}^K w_ks_k+\epsilon\)</span>, with nonnegative abundances <span class="math-inline" markdown="0">\(w_k\)</span> summing to one. For example, <span class="math-inline" markdown="0">\(0.6s_{veg}+0.3s_{soil}+0.1s_{water}\)</span> represents estimated fractions, subject to the model and endmember assumptions. Multiple scattering and nonlinear interactions can violate this approximation.

NDVI is <span class="math-inline" markdown="0">\((NIR-Red)/(NIR+Red)\)</span> when the denominator is nonzero. Red 20 and NIR 80 give 0.6. It often tracks green vegetation, but it can saturate in dense canopies and respond to soil, atmosphere, illumination, and crop type. A seasonal NDVI curve may rise after emergence and fall during senescence, but it is not a universal yield meter.

The **Green–NIR NDWI** for open water is <span class="math-inline" markdown="0">\((Green-NIR)/(Green+NIR)\)</span>: Green 60 and NIR 10 give <span class="math-inline" markdown="0">\(50/70\approx0.714\)</span>. Another index also called NDWI uses NIR and SWIR for vegetation water content. Name the bands, not just the acronym. All normalized ratios require care when their denominators are near zero.

## 14. Fusion, registration, and change detection
{: #change}

Pansharpening combines a high-detail panchromatic image with multispectral bands. Good fusion preserves useful spectral behavior while adding spatial detail. Registration establishes corresponding ground locations; an offset can manufacture edges and changes. Subpixel alignment is often sought, but the acceptable error depends on resolution and target size.

Direct spectral change starts with <span class="math-inline" markdown="0">\(\Delta x=x_{t_2}-x_{t_1}\)</span> and may use <span class="math-inline" markdown="0">\(\&#124;\Delta x\&#124;\)</span> or its direction. It requires comparable calibration, band responses, spatial resolution, geometry, and season. Post-classification comparison instead compares thematic labels at the two dates and yields from–to transitions. It still depends on consistent class definitions and accurate classifications; errors can compound.

| Approach | Strength | Main risk |
| --- | --- | --- |
| Image differencing or ratioing | Simple direct measurement change | Radiometric and denominator artifacts |
| NDVI differencing | Vegetation-focused trend | Seasonal or atmospheric variation |
| Change-vector analysis | Multiband magnitude and direction | Feature comparability |
| Temporal PCA | Captures joint variability | PCs need interpretation |
| Post-classification comparison | Explicit class transitions | Two maps' errors propagate |

Cloud and shadow, sun/view angle, soil moisture, phenology, sensor response, and registration can all look like land-cover change. Same-sensor images still need alignment and radiometric care; cross-sensor work needs extra harmonization.

## 15. Supporting machine-learning concepts
{: #supporting-ml}

These ideas support the classification sections rather than being a replacement for the remote-sensing workflow. AI is a broad field; machine learning learns patterns from data; deep learning uses multilayer neural networks. Classification predicts categories, while regression predicts numerical values. Supervised learning uses labels; clustering usually does not.

Naive Bayes assumes features are conditionally independent given the class: <span class="math-inline" markdown="0">\(P(C\mid x)\propto P(C)\prod_jP(x_j\mid C)\)</span>. With vegetation prior 0.6 and feature likelihoods 0.8 and 0.7, its unnormalized score is 0.336. With water prior 0.4 and likelihoods 0.2 and 0.5, the score is 0.04. The normalized vegetation posterior is <span class="math-inline" markdown="0">\(0.336/(0.336+0.04)\approx0.894\)</span>, under the model assumptions.

Decision trees split features to reduce impurity. Entropy is <span class="math-inline" markdown="0">\(H=-\sum_i p_i\log_2p_i\)</span>; information gain subtracts weighted child entropy from parent entropy. Gini impurity is <span class="math-inline" markdown="0">\(1-\sum_i p_i^2\)</span>. These quantities describe label mixtures, not sensor physics.

A neuron's forward computation is <span class="math-inline" markdown="0">\(\hat y=wx+b\)</span> followed by an activation. Backpropagation applies the chain rule to a loss. If <span class="math-inline" markdown="0">\(x=2,w=3,b=1,y=5\)</span> and activation is identity, <span class="math-inline" markdown="0">\(\hat y=7\)</span>, <span class="math-inline" markdown="0">\(L=(\hat y-y)^2/2=2\)</span>, and <span class="math-inline" markdown="0">\(\partial L/\partial w=(7-5)\cdot2=4\)</span>. A gradient step of size 0.1 changes <span class="math-inline" markdown="0">\(w\)</span> to 2.6.

## 16. Worked revision problems
{: #practice}

### Problem A · Which neighborhood is being used?

A classifier uses KNN on spectral vectors, and a median filter uses a 3×3 window. Do both use “nearest pixels” in the same sense?

<details markdown="1" data-proof><summary>Show solution</summary>

No. KNN compares feature vectors and can retrieve training pixels from distant map locations. The median filter uses nearby image coordinates. Combining spectral and spatial features is possible, but it must be explicit.

</details>

### Problem B · Convolution and correlation

Use patch <span class="math-inline" markdown="0">\([1,2;3,4]\)</span> and kernel <span class="math-inline" markdown="0">\([1,0;0,-1]\)</span>. Find aligned correlation and convolution responses.

<details markdown="1" data-proof><summary>Show solution</summary>

Correlation is <span class="math-inline" markdown="0">\(1-4=-3\)</span>. The 180° flipped kernel is <span class="math-inline" markdown="0">\([-1,0;0,1]\)</span>, giving convolution <span class="math-inline" markdown="0">\(-1+4=3\)</span>. Specify the alignment and boundary rule for a whole image.

</details>

### Problem C · Read an error matrix

Using section 12's matrix, compute forest user's accuracy, producer's accuracy, and kappa. Then swap the row and column meaning: which interpretation changes?

<details markdown="1" data-proof><summary>Show solution</summary>

With rows predicted, <span class="math-inline" markdown="0">\(UA=40/50=0.8\)</span>, <span class="math-inline" markdown="0">\(PA=40/60\approx0.667\)</span>, and <span class="math-inline" markdown="0">\(\kappa=0.4\)</span>. If rows instead mean actual, the same numerical matrix gives <span class="math-inline" markdown="0">\(UA=40/60\)</span> and <span class="math-inline" markdown="0">\(PA=40/50\)</span>. Overall accuracy and kappa stay the same because the diagonal and products of marginals are unchanged by transposition.

</details>

### Problem D · A spectral look-alike

A pixel spectrum is <span class="math-inline" markdown="0">\((10,20,30)\)</span> and a reference is <span class="math-inline" markdown="0">\((20,40,60)\)</span>. What do SAM and Euclidean distance say?

<details markdown="1" data-proof><summary>Show solution</summary>

SAM gives zero angle because the vectors have the same direction. Euclidean distance is <span class="math-inline" markdown="0">\(\sqrt{10^2+20^2+30^2}=\sqrt{1400}\approx37.42\)</span>. SAM compares shape under positive scaling; Euclidean distance responds to magnitude.

</details>

### Problem E · Feature count versus sample count

How many distinct covariance parameters does a 12-band Gaussian class model need, before counting its mean?

<details markdown="1" data-proof><summary>Show solution</summary>

A symmetric 12×12 covariance has <span class="math-inline" markdown="0">\(12(13)/2=78\)</span> distinct entries. The mean adds 12 more parameters. This helps explain why full covariance estimates become fragile with small training sets.

</details>

## 17. Formula sheet and common mistakes
{: #formula-sheet}

| Task | Formula or test |
| --- | --- |
| Raw sample bytes | <span class="math-inline" markdown="0">\(H\,W\,K\,b/8\)</span> when every sample uses <span class="math-inline" markdown="0">\(b\)</span> bits |
| Stretch | <span class="math-inline" markdown="0">\(255(f-f_{min})/(f_{max}-f_{min})\)</span> |
| Equalization | <span class="math-inline" markdown="0">\(s_k\approx(L-1)\sum_{j\le k}p_j\)</span>, then state rounding |
| Gaussian low-pass | <span class="math-inline" markdown="0">\(e^{-k(u^2+v^2)}\)</span> for <span class="math-inline" markdown="0">\(k&gt;0\)</span> |
| Hough line | <span class="math-inline" markdown="0">\(\rho=x\cos\theta+y\sin\theta\)</span> |
| Opening / closing | <span class="math-inline" markdown="0">\((A\ominus B)\oplus B\)</span> / <span class="math-inline" markdown="0">\((A\oplus B)\ominus B\)</span> |
| Hit-or-miss | <span class="math-inline" markdown="0">\((A\ominus B_1)\cap(A^c\ominus B_2)\)</span> |
| GLCM contrast / ASM | <span class="math-inline" markdown="0">\(\sum(i-j)^2P(i,j)\)</span> / <span class="math-inline" markdown="0">\(\sum P(i,j)^2\)</span> |
| PCA retained variance | <span class="math-inline" markdown="0">\(\sum_{i\le k}\lambda_i/\sum_j\lambda_j\)</span> |
| Mahalanobis squared | <span class="math-inline" markdown="0">\((x-\mu)^\top\Sigma^{-1}(x-\mu)\)</span> |
| Spectral angle | <span class="math-inline" markdown="0">\(\arccos[(x^\top v)/(\&#124;x\&#124;\&#124;v\&#124;)]\)</span> |
| User / producer accuracy | Correct / predicted total; correct / actual total |
| Kappa | <span class="math-inline" markdown="0">\((P_o-P_e)/(1-P_e)\)</span> |
| NDVI / Green–NIR NDWI | <span class="math-inline" markdown="0">\((NIR-Red)/(NIR+Red)\)</span> / <span class="math-inline" markdown="0">\((Green-NIR)/(Green+NIR)\)</span> |

When revising, check these traps: a feature-space neighbor is not necessarily a spatial neighbor; closing requires dilation **then** erosion; GLCM statistics use normalized pair counts; PCA variance does not equal classification value; SAM ignores positive scale; and a direct spectral difference may reflect the atmosphere or a shifted pixel. Always identify which confusion-matrix axis is predicted, whether a classifier can reject a pixel, and whether a spectral index's denominator is safe. Changing the class definitions can raise overall accuracy without improving the underlying map.

The whole workflow comes back to one question: **what information about the ground can this measurement support?** Better processing matters, but so do calibration, sampling, alignment, ground truth, and honest uncertainty.
