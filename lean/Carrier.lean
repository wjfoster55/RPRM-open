import Init

/-!
Operational carrier core; statement correspondence is in docs/formal-proofs.md.
Lean 4.22.0; no external library dependencies.

`X` is the fixed admitted full state carrier, `Z` its retained representation,
`A` the frozen operation alphabet, and `Y` the observation receiver.
`Option X` represents a deterministic partial operation: `none` is failure,
distinct from every successful state. Every successful successor is in `X`.
Surjectivity of `C` states that `Z` is exactly the reachable image.

The statements quantify over arbitrary types and every finite operation list.
Applying them to a bounded carrier requires choosing that carrier as `X`.
They make no claim that any chosen quotient or decoder is computable or cheap.
-/

namespace RPRM

universe u v w r

variable {X : Type u} {Z : Type v} {Y : Type w} {A : Type r}

def Onto (C : X → Z) : Prop := ∀ z, ∃ x, C x = z

def FiberConstant (C : X → Z) (Q : X → Y) : Prop :=
  ∀ x y, C x = C y → Q x = Q y

/-- Theorem 1: a question has a decoder exactly when it is fiber-constant. -/
theorem factorization_iff (C : X → Z) (Q : X → Y) (onto : Onto C) :
    (∃ g : Z → Y, ∀ x, g (C x) = Q x) ↔ FiberConstant C Q := by
  constructor
  · rintro ⟨g, hg⟩ x y hxy
    rw [← hg x, ← hg y, hxy]
  · intro hQ
    let pick : Z → X := fun z => Classical.choose (onto z)
    have hpick : ∀ z, C (pick z) = z := fun z => Classical.choose_spec (onto z)
    refine ⟨fun z => Q (pick z), ?_⟩
    intro x
    exact hQ (pick (C x)) x (hpick (C x))

/-- On the reachable image the decoder is unique. -/
theorem decoder_unique (C : X → Z) (Q : X → Y) (onto : Onto C)
    (g h : Z → Y) (hg : ∀ x, g (C x) = Q x)
    (hh : ∀ x, h (C x) = Q x) : g = h := by
  funext z
  obtain ⟨x, rfl⟩ := onto z
  exact (hg x).trans (hh x).symm

/-- Passing to this subtype supplies the reachable-image hypothesis. -/
def Reachable (C : X → Z) := {z : Z // ∃ x, C x = z}

def toReachable (C : X → Z) (x : X) : Reachable C := ⟨C x, x, rfl⟩

theorem toReachable_onto (C : X → Z) : Onto (toReachable C) := by
  intro z
  obtain ⟨x, hx⟩ := z.property
  refine ⟨x, ?_⟩
  exact Subtype.eq hx

def Defined (s : Option X) : Prop := ∃ x, s = some x

/-- Equality of retained partial results means equal domains and successors. -/
theorem option_map_eq_iff (C : X → Z) (s t : Option X) :
    s.map C = t.map C ↔
      (Defined s ↔ Defined t) ∧
      (∀ x y, s = some x → t = some y → C x = C y) := by
  cases s <;> cases t <;> simp [Defined]

/-- The three explicit fiber conditions in CARRIER_PROOF.md Theorem 2. -/
def FiberConditions (C : X → Z) (O : X → Y) (T : A → X → Option X) : Prop :=
  FiberConstant C O ∧
  (∀ a x y, C x = C y → (Defined (T a x) ↔ Defined (T a y))) ∧
  (∀ a x y x' y', C x = C y → T a x = some x' → T a y = some y' →
    C x' = C y')

/-- The equation includes both exact enabledness and exact retained updates. -/
def OperationalFold (C : X → Z) (O : X → Y) (T : A → X → Option X) : Prop :=
  ∃ Obar : Z → Y, ∃ Tbar : A → Z → Option Z,
    (∀ x, Obar (C x) = O x) ∧
    (∀ a x, Tbar a (C x) = (T a x).map C)

/-- Theorem 2: the conditions are necessary and sufficient, for every letter. -/
theorem operational_fold_iff (C : X → Z) (O : X → Y)
    (T : A → X → Option X) (onto : Onto C) :
    OperationalFold C O T ↔ FiberConditions C O T := by
  constructor
  · rintro ⟨Obar, Tbar, hO, hT⟩
    have hObs : FiberConstant C O := (factorization_iff C O onto).mp ⟨Obar, hO⟩
    have hStep : ∀ a, FiberConstant C (fun x => (T a x).map C) := by
      intro a
      exact (factorization_iff C (fun x => (T a x).map C) onto).mp ⟨Tbar a, hT a⟩
    refine ⟨hObs, ?_, ?_⟩
    · intro a x y hxy
      exact ((option_map_eq_iff C (T a x) (T a y)).mp (hStep a x y hxy)).1
    · intro a x y x' y' hxy hx hy
      exact ((option_map_eq_iff C (T a x) (T a y)).mp
        (hStep a x y hxy)).2 x' y' hx hy
  · rintro ⟨hObs, hDomain, hNext⟩
    obtain ⟨Obar, hO⟩ := (factorization_iff C O onto).mpr hObs
    have hSteps : ∀ a, ∃ tbar : Z → Option Z,
        ∀ x, tbar (C x) = (T a x).map C := by
      intro a
      apply (factorization_iff C (fun x => (T a x).map C) onto).mpr
      intro x y hxy
      exact (option_map_eq_iff C (T a x) (T a y)).mpr
        ⟨hDomain a x y hxy, fun x' y' hx hy => hNext a x y x' y' hxy hx hy⟩
    refine ⟨Obar, fun a => Classical.choose (hSteps a), hO, ?_⟩
    intro a
    exact Classical.choose_spec (hSteps a)

/-- Letters execute from left to right, and failure stops the whole word. -/
def run (T : A → X → Option X) : List A → X → Option X
  | [], x => some x
  | a :: rest, x => (T a x).bind (run T rest)

/-- Induction proves exact retained state equality for every finite word. -/
theorem run_commutes (C : X → Z) (T : A → X → Option X)
    (Tbar : A → Z → Option Z)
    (hT : ∀ a x, Tbar a (C x) = (T a x).map C)
    (word : List A) (x : X) :
    run Tbar word (C x) = (run T word x).map C := by
  induction word generalizing x with
  | nil => rfl
  | cons a rest ih =>
    simp only [run, hT]
    cases h : T a x with
    | none => rfl
    | some next => exact ih next

/-- Every finite word has exactly the same enabledness after compression. -/
theorem run_defined_iff (C : X → Z) (T : A → X → Option X)
    (Tbar : A → Z → Option Z)
    (hT : ∀ a x, Tbar a (C x) = (T a x).map C)
    (word : List A) (x : X) :
    Defined (run Tbar word (C x)) ↔ Defined (run T word x) := by
  rw [run_commutes C T Tbar hT word x]
  cases run T word x <;> simp [Defined]

/-- `none` is FAIL; `some y` is a successful, tagged observation. -/
def future (O : X → Y) (T : A → X → Option X)
    (word : List A) (x : X) : Option Y := (run T word x).map O

/-- The observation decoder preserves the exact future answer of every word. -/
theorem future_preserved (C : X → Z) (O : X → Y)
    (T : A → X → Option X) (Obar : Z → Y) (Tbar : A → Z → Option Z)
    (hO : ∀ x, Obar (C x) = O x)
    (hT : ∀ a x, Tbar a (C x) = (T a x).map C)
    (word : List A) (x : X) :
    future Obar Tbar word (C x) = future O T word x := by
  unfold future
  rw [run_commutes C T Tbar hT word x]
  cases run T word x with
  | none => rfl
  | some next => exact congrArg some (hO next)

/-- Fiber conditions imply preservation simultaneously for all finite words. -/
theorem fiber_conditions_preserve_all_futures (C : X → Z) (O : X → Y)
    (T : A → X → Option X) (onto : Onto C) (h : FiberConditions C O T) :
    ∃ Obar : Z → Y, ∃ Tbar : A → Z → Option Z,
      ∀ (word : List A) (x : X),
        run Tbar word (C x) = (run T word x).map C ∧
        (Defined (run Tbar word (C x)) ↔ Defined (run T word x)) ∧
        future Obar Tbar word (C x) = future O T word x := by
  obtain ⟨Obar, Tbar, hO, hT⟩ := (operational_fold_iff C O T onto).mpr h
  refine ⟨Obar, Tbar, ?_⟩
  intro word x
  exact ⟨run_commutes C T Tbar hT word x,
    run_defined_iff C T Tbar hT word x,
    future_preserved C O T Obar Tbar hO hT word x⟩

#print axioms factorization_iff
#print axioms decoder_unique
#print axioms toReachable_onto
#print axioms option_map_eq_iff
#print axioms operational_fold_iff
#print axioms run_commutes
#print axioms run_defined_iff
#print axioms future_preserved
#print axioms fiber_conditions_preserve_all_futures

end RPRM
