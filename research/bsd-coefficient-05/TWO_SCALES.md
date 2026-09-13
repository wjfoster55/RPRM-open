# The two scales, side by side

Start with the real BSD comparison for the same curve E34. The following
are the earlier rigorous enclosures, shown here to explain the target.
They were not recomputed as part of this coefficient experiment.

| | Analytic side | Arithmetic side |
|---|---|---|
| What is measured | Strength of the first nonzero term in L(E,s) near s=1 | Period times the regulator of the two independent rational-point directions |
| Formula | c=L''(E,1)/2 | Omega_all·det(G_infinity) |
| Certified interval | [6.38511803,6.38518585] | [6.384593255,6.385625424] |
| Source construction | Prime point counts build the L-function, then a rigorously bounded central expansion | A full rational-point basis builds a 2×2 height matrix; the period is integrated over both real components |

The ratio we ultimately want to understand is

\[
\boxed{q_\infty=
\frac{L''(E,1)/2}{\Omega_{\rm all}\det(G_\infty)}}
\quad\in [0.999920542,1.000092816].
\]

Full BSD would identify this ratio with the order of Sha. The interval
contains 1 but does not establish that identification or exact equality.
The Tamagawa-product/torsion-square factor is 16/16=1 for this curve.

The components of the arithmetic side are
Omega_all∈[0.899358321446,0.899358321447] and
Reg_full∈[7.099053962,7.100201634]. The regulator includes the mixed
pairing between P and Q; multiplying two diagonal heights alone would
discard that correlation.

## What “same dimensionality” means here

Both sides already reflect rank 2. The analytic function starts at quadratic
order; the arithmetic regulator is a determinant of a 2×2 matrix. In the
5-adic version, each height occupies degree 1 and its determinant occupies
degree 2, the same degree as the analytic quadratic coefficient. That
degree-two space is a one-dimensional scalar line.

Changing the coordinate does change the displayed coefficient. If
T'=gamma^u−1 with u a 5-adic unit, then both the analytic quadratic
coefficient and the scalar regulator become u^(-2) times their previous
values. Their quotient is unchanged. Scaling every height by a multiplies
the rank-two regulator by a². Replacing a full basis by an index-d
sublattice multiplies it by d². These operations have to be retained;
they cannot be folded into an unnamed dimension change.

## The new 5-adic calculation

The independently normalized power series is

\[
F_{34}(T)=b_2T^2+\cdots,\qquad
\boxed{b_2=1+2\cdot5^2+3\cdot5^3+O(5^4).}
\]

This reads as residue426 modulo 625 in the 5-adic number system. It is
not a real-valued height426 to compare with 6.385. Its normalization is
the connected real period, minimal differential and gamma=6.

The new coefficient and the arithmetic regulator can be put in the same
5-adic coordinates. With C5 the known local factor, define

\[
\Lambda_c=
\frac{C_5b_2\,[\log_5(6)/5]^2}{R_{\rm MST}}
=\frac{C_5D_{\rm raw}}{100R_{\rm MST}}.
\]

Fresh calculation gives R_MST=3 mod 5 and 5Lambda_c=1 mod 5. Thus we
now have the first digit of this explicitly defined local multiplier.
The BKS period convention multiplies Lambda_c by
c_xi=Omega_(34,c)/Omega_xi; this factor is retained explicitly.

The exact target remains

\[
C_5A_\xi=
\frac{L_S^*(E,1)}{\Omega_\xi R_\infty}R_5,
\qquad A_\xi=c_\xi b_2.
\]

Do not divide a real interval directly by a 5-adic value. The source
comparison fixes an embedding and period/height conventions. A safe
connector from the displayed real ratio is

\[
\frac{L_S^*}{\Omega_\xi R_\infty}
=\frac85\frac{\Omega_{\rm all}}{\Omega_\xi}
  \frac{\operatorname{Reg}_{\rm full}}{R_\infty}q_\infty.
\]

Here8/5 is the removed Euler factor at 5. This formula keeps the exact
period and real-height conversions visible instead of assuming they are 1.
Matching these conventions makes the comparison well-typed; proving the
comparison is still additional mathematical work.
