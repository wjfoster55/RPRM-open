import Init

/-!
RPRM: a typed relation core, with Lean 4.22.0 and Init only.

`Relation X Y` is a supplied binary relation. `compose S R` means first R,
then S, retaining existence of a compatible intermediate state. It hides
which intermediate witness was used; it is not a witness-preserving ATTACH.
Converse reverses a relation and does not assert a single-valued inverse.

All types, including empty types, are admitted by the algebra. These theorems
do not construct a finite enumeration, choose a MANY-fiber member, or establish
an interpretation of external source objects. Application bounds and source
bindings are separate hypotheses.

The final two results give explicit inverse maps for an aperture fiber under
a supplied coordinate change. The known coordinate is embedded with a supplied
retraction; the missing coordinate has a supplied two-sided inverse. The target
fiber is evaluated at the image of the known source coordinate. There is no
claim about arbitrary target coordinates outside that image.
-/

namespace RPRM.Relations

universe u v w t u' v'

abbrev Relation (X : Type u) (Y : Type v) := X → Y → Prop

variable {X : Type u} {Y : Type v} {Z : Type w} {W : Type t}
variable {X' : Type u'} {Y' : Type v'}

def identity (X : Type u) : Relation X X := fun x y => x = y

def converse (R : Relation X Y) : Relation Y X := fun y x => R x y

def compose (S : Relation Y Z) (R : Relation X Y) : Relation X Z :=
  fun x z => ∃ y, R x y ∧ S y z

def graph (f : X → Y) : Relation X Y := fun x y => f x = y

/-- L01: the identity of the target is a left unit for composition. -/
theorem identity_left (R : Relation X Y) : compose (identity Y) R = R := by
  funext x y
  apply propext
  constructor
  · rintro ⟨z, hr, hz⟩
    exact (show z = y from hz) ▸ hr
  · intro hr
    exact ⟨y, hr, rfl⟩

/-- L02: the identity of the source is a right unit for composition. -/
theorem identity_right (R : Relation X Y) : compose R (identity X) = R := by
  funext x y
  apply propext
  constructor
  · rintro ⟨z, hz, hr⟩
    change x = z at hz
    cases hz
    exact hr
  · intro hr
    exact ⟨x, rfl, hr⟩

/-- L03: typed relation composition is associative. -/
theorem compose_assoc (R : Relation X Y) (S : Relation Y Z) (T : Relation Z W) :
    compose T (compose S R) = compose (compose T S) R := by
  funext x w
  apply propext
  constructor
  · rintro ⟨z, ⟨y, hr, hs⟩, ht⟩
    exact ⟨y, hr, z, hs, ht⟩
  · rintro ⟨y, hr, z, hs, ht⟩
    exact ⟨z, ⟨y, hr, hs⟩, ht⟩

/-- L04: taking converse twice restores the original relation. -/
theorem converse_involutive (R : Relation X Y) : converse (converse R) = R := by
  rfl

/-- L05: converse reverses the order of composition. -/
theorem converse_compose (R : Relation X Y) (S : Relation Y Z) :
    converse (compose S R) = compose (converse R) (converse S) := by
  funext z x
  apply propext
  constructor
  · rintro ⟨y, hr, hs⟩
    exact ⟨y, hs, hr⟩
  · rintro ⟨y, hs, hr⟩
    exact ⟨y, hr, hs⟩

/-- L06: the graph of the identity map is the identity relation. -/
theorem graph_identity : graph (fun x : X => x) = identity X := by
  rfl

/-- L07: composing function graphs gives the graph of function composition. -/
theorem graph_compose (f : X → Y) (g : Y → Z) :
    compose (graph g) (graph f) = graph (fun x => g (f x)) := by
  funext x z
  apply propext
  constructor
  · rintro ⟨y, hf, hg⟩
    exact (congrArg g hf).trans hg
  · intro h
    exact ⟨f x, rfl, h⟩

/-- L08: under both inverse equations, the converse graph is the inverse graph. -/
theorem graph_converse_inverse (e : X → Y) (r : Y → X)
    (left : ∀ x, r (e x) = x) (right : ∀ y, e (r y) = y) :
    converse (graph e) = graph r := by
  funext y x
  apply propext
  constructor
  · intro h
    exact (congrArg r h).symm.trans (left x)
  · intro h
    exact (congrArg e h).symm.trans (right y)

/-- L09: a supplied retraction forces its section to be injective. -/
theorem retraction_section_injective (e : X → Y) (r : Y → X)
    (left : ∀ x, r (e x) = x) :
    ∀ x y, e x = e y → x = y := by
  intro x y h
  exact (left x).symm.trans ((congrArg r h).trans (left y))

/-- A missing-coordinate aperture, with the known coordinate fixed at x. -/
def Fiber (R : Relation X Y) (x : X) := {y : Y // R x y}

/-- Pull a relation back along two explicitly supplied decoding maps. -/
def pullback (R : Relation X Y) (d : X' → X) (r : Y' → Y) : Relation X' Y' :=
  fun x' y' => R (d x') (r y')

def apertureForward (R : Relation X Y) (s : X → X') (d : X' → X)
    (known_left : ∀ x, d (s x) = x) (e : Y → Y') (r : Y' → Y)
    (missing_left : ∀ y, r (e y) = y) (x : X) :
    Fiber R x → Fiber (pullback R d r) (s x) :=
  fun y => ⟨e y.val, by
    change R (d (s x)) (r (e y.val))
    rw [known_left x, missing_left y.val]
    exact y.property⟩

def apertureBackward (R : Relation X Y) (s : X → X') (d : X' → X)
    (known_left : ∀ x, d (s x) = x) (r : Y' → Y) (x : X) :
    Fiber (pullback R d r) (s x) → Fiber R x :=
  fun y => ⟨r y.val, by
    have hy := y.property
    change R (d (s x)) (r y.val) at hy
    rw [known_left x] at hy
    exact hy⟩

/-- L10: decoding an encoded source-fiber element restores that element. -/
theorem aperture_backward_forward (R : Relation X Y) (s : X → X') (d : X' → X)
    (known_left : ∀ x, d (s x) = x) (e : Y → Y') (r : Y' → Y)
    (missing_left : ∀ y, r (e y) = y) (x : X) (y : Fiber R x) :
    apertureBackward R s d known_left r x
      (apertureForward R s d known_left e r missing_left x y) = y := by
  exact Subtype.eq (missing_left y.val)

/-- L11: with the other inverse equation, encoding also restores every target-fiber element. -/
theorem aperture_forward_backward (R : Relation X Y) (s : X → X') (d : X' → X)
    (known_left : ∀ x, d (s x) = x) (e : Y → Y') (r : Y' → Y)
    (missing_left : ∀ y, r (e y) = y) (missing_right : ∀ y', e (r y') = y')
    (x : X) (y : Fiber (pullback R d r) (s x)) :
    apertureForward R s d known_left e r missing_left x
      (apertureBackward R s d known_left r x y) = y := by
  exact Subtype.eq (missing_right y.val)

#print axioms identity_left
#print axioms identity_right
#print axioms compose_assoc
#print axioms converse_involutive
#print axioms converse_compose
#print axioms graph_identity
#print axioms graph_compose
#print axioms graph_converse_inverse
#print axioms retraction_section_injective
#print axioms aperture_backward_forward
#print axioms aperture_forward_backward

end RPRM.Relations
