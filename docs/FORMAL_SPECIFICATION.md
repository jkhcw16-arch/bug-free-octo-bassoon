---
title: "Rotational Prime Ontology: Formal Specification"
version: "1.0"
author: "Jamie Kinney"
date: "2026-09-28"
domain: "Deterministic decision systems for governance, risk, safety, and statutory alignment"
---

# Rotational Prime Ontology — Formal Specification

## 1. Ontology Identity

**Name:** Rotational Prime Ontology (RPO)  
**Version:** 1.0  
**Author:** Jamie Kinney  
**Domain:** Deterministic decision systems for governance, risk, safety, and statutory alignment  
**License:** MIT  

### Core Components

1. Prime‑indexed semantic categories
2. Rotational state operators
3. Paired temporal memory
4. Deterministic event chain
5. Risk‑to‑protection projection

---

## 2. Semantic Category System (Prime Indexing)

### 2.1 Category Set

Let **C** be the set of semantic categories relevant to decision evaluation.

**Example categories (extensible):**

| Category | Domain | Example |
|----------|--------|---------|
| Safety | Physical or wellbeing integrity | child injury risk, threat level |
| Risk | Magnitude of negative outcome | likelihood × severity |
| Support | Availability of protective resources | family network, agency capacity |
| Agency Action | Actions taken by decision-making entity | investigation, placement, intervention |
| Subject Action | Actions taken by the subject under evaluation | compliance, cooperation, escalation |
| Environment | Contextual factors | isolation, crowding, resource availability |
| History | Prior events and patterns | previous incidents, trends |
| Intent | Motivation or purposefulness | accidental vs. deliberate, good-faith vs. malicious |

### 2.2 Prime Mapping Function

Define a bijective mapping:

$$\pi: C \to P$$

Where **P** is the ordered set of prime numbers {2, 3, 5, 7, 11, 13, 17, 19, 23, ...}.

**Example mapping:**

| Category | Prime |
|----------|-------|
| Safety | 2 |
| Risk | 3 |
| Support | 5 |
| Agency Action | 7 |
| Subject Action | 11 |
| Environment | 13 |
| History | 17 |
| Intent | 19 |

**Invariant:** π is collision-free. Each category has exactly one prime; no two categories share a prime.

### 2.3 Prime Vector Encoding

A state's semantic content is encoded as:

$$V = \{(c, \pi(c), w_c) \mid c \in C\}$$

Where:
- **c** ∈ **C** is a semantic category
- **π(c)** is the assigned prime
- **w_c** ∈ [0, 1] is the normalized category weight

**Example state encoding:**

```json
{
  "Safety": {"prime": 2, "weight": 0.9},
  "Risk": {"prime": 3, "weight": 0.8},
  "Support": {"prime": 5, "weight": 0.4},
  "Intent": {"prime": 19, "weight": 0.2}
}
```

**Property:** The encoding is deterministic. Identical inputs always produce identical encodings.

---

## 3. Rotational Operator System

### 3.1 State Vector

Let a decision state be:

$$S = (V, M, T)$$

Where:
- **V** = prime-indexed semantic vector (from §2.3)
- **M** = paired temporal memory (from §4)
- **T** = timestamp or temporal index

### 3.2 Rotational Operators

Define a family of rotational operators:

$$R_k: S \to S$$

Each operator applies a deterministic rotation in semantic decision space.

**Operator Implementation (Modular Arithmetic):**

For a state value $s_i$:

$$R_k(s_i) = (s_i + \theta_k) \bmod m$$

Where:
- **θ_k** is the operator's rotation magnitude (in degrees or radians)
- **m** is the modulus (state space size, typically 360 for angular space)
- The operation is deterministic and invertible (if gcd(θ_k, m) = 1)

**Operator Composition:**

Multiple rotations compose:

$$R_{k_1}(R_{k_2}(S)) = R_{k_1 + k_2}(S)$$

### 3.3 Operator Semantics

Define three primary rotations:

| Operator | Semantic Meaning | Application |
|----------|-----------------|-------------|
| **R₁** (Analysis) | Transform raw state into interpretable risk assessment | Apply domain-specific weights; aggregate factors |
| **R₂** (Alignment) | Rotate state to align with policy and legal constraints | Check statutory requirements; apply bias correction |
| **R₃** (Response) | Transform risk into protective action recommendation | Project from risk vector to action vector |

Each operator is:
- **Deterministic:** identical inputs → identical outputs
- **Auditable:** transformation is transparent and logged
- **Reversible:** most operators can be inverted to trace back to prior state
- **Ordered:** R₁ → R₂ → R₃ (strict sequence)

**Invariant:** Operator application order is fixed. Reordering violates determinism guarantees.

---

## 4. Paired Temporal Memory

### 4.1 Memory Structure

Define memory as a dual-role structure:

$$M = (M_a, M_s)$$

Where:
- **M_a** = agency memory (state as perceived/acted by the decision-making entity)
- **M_s** = subject memory (state as perceived/acted by the subject under evaluation)

**Rationale:** Role symmetry ensures both perspectives are recorded, enabling fairness audits and accountability.

### 4.2 Memory Records

Each memory is a sequence of immutable records:

$$M_a(t) = [S_a(0), S_a(1), \ldots, S_a(t)]$$

Where each $S_a(i)$ is a timestamped state snapshot.

### 4.3 Update Rule

At time $t + 1$, memory updates append-only:

$$M_a(t+1) = M_a(t) \cup \{S_a(t)\}$$

$$M_s(t+1) = M_s(t) \cup \{S_s(t)\}$$

**Properties:**
- Append-only: historical records are never modified or deleted
- Immutable: once written, records are locked
- Ordered: records are timestamped and ordered by insertion
- Symmetric: both perspectives are maintained in parallel

### 4.4 Correlation Tracking

Memory pairs are linked by directed correlation edges:

$$E = \{(r_i, r_j, \sigma) \mid r_i, r_j \in M, \sigma \in [0, 1]\}$$

Where **σ** is the correlation strength (0 = independent, 1 = causal).

**Example:** A child welfare case links agency assessment (M_a record) to subject outcome (M_s record) with correlation 0.9 indicating strong causal relationship.

---

## 5. Deterministic Event Chain

The ontology enforces a strict, ordered sequence of operations:

$$S_{t+1} = P(R_3(R_2(R_1(E(S_t)))))$$

**Expanded pipeline:**

1. **Encoding (E):** Semantic categories → prime vector (§2)
2. **Rotation R₁:** Analyze and aggregate factors
3. **Rotation R₂:** Align with constraints and policy
4. **Rotation R₃:** Transform to protective actions
5. **Projection (P):** Output decision and recommended actions
6. **Memory Update (M):** Record in paired temporal memory

**Invariant:** This sequence is deterministic. Reordering, skipping, or modifying any step violates the formal semantics.

**Chain Diagram:**

```
State Input
    ↓
[E] Encoding (→ prime vector)
    ↓
[R₁] Analysis Rotation
    ↓
[R₂] Alignment Rotation (policy/legal)
    ↓
[R₃] Response Rotation
    ↓
[M] Memory Update (append-only)
    ↓
[P] Projection (→ decision output)
    ↓
Decision Output
```

---

## 6. Risk‑to‑Protection Projection

### 6.1 Risk Vector

Define the risk vector as:

$$\vec{r} = \{r_c \mid c \in C\}$$

Where $r_c \in [0, 1]$ is the normalized risk magnitude for category **c**.

**Computation:**

$$r_c = \sum_i (f_i \cdot w_i)$$

Where:
- **f_i** are risk factors (individual assessments)
- **w_i** are factor weights
- Normalized to [0, 1] by dividing by sum of weights

### 6.2 Risk Levels

Map risk to discrete levels:

| Level | Range | Meaning |
|-------|-------|---------|
| **Low** | [0.00, 0.34) | Routine monitoring; minimal intervention |
| **Medium** | [0.34, 0.67) | Targeted intervention; active engagement |
| **High** | [0.67, 1.00] | Immediate protection; escalated response |

### 6.3 Protection Projection Function

Define:

$$\Phi: \vec{r} \to \vec{a}$$

Where $\vec{a}$ is the protective action vector.

**Projection Rule (Monotonic):**

$$a_i = f(\pi(r_i))$$

Where **f** is a monotonic function:

$$r_i > r_j \Rightarrow a_i \geq a_j$$

**Example action mapping:**

| Risk Level | Recommended Action | Rationale |
|------------|-------------------|-----------|
| Low | Monitor | Continue routine oversight; maintain contact |
| Medium | Targeted Intervention | Provide targeted support; increase frequency of contact |
| High | Immediate Protection | Immediate safeguarding; remove threat; activate escalation |

**Invariant:** Monotonicity ensures consistency: higher assessed risk produces equal or stronger protective response.

---

## 7. Decision Output Specification

### 7.1 Output Structure

A decision output is:

$$D = (A, S', M', C, E)$$

Where:
- **A** = set of recommended actions
- **S'** = transformed state after all rotations
- **M'** = updated memory (M_a and M_s)
- **C** = constraints applied (policy, legal, statutory)
- **E** = explanation trace (audit log of transformations)

### 7.2 Output Requirements

All decision outputs must satisfy:

**Determinism**

$$\forall S_i, S_j: S_i = S_j \Rightarrow D_i = D_j$$

Identical inputs produce identical outputs.

**Auditability**

Every decision includes a complete audit trail:
- Input state
- Applied rotations
- Constraint checks
- Projection decisions
- Timestamps and actor IDs

**Interpretability**

Outputs are human-readable and explainable:
- Why was this risk level assigned?
- Which factors contributed most?
- Which constraints were binding?
- What are the legal/statutory justifications?

**Statutory Alignment**

Outputs comply with all applicable legal and regulatory requirements:
- Domain-specific mandates (e.g., child safety law)
- Non-discrimination principles
- Due-process requirements
- Documentation standards

**Role Symmetry**

Both agency and subject perspectives are recorded and accessible:
- M_a and M_s are preserved
- Correlations between them are documented
- Fairness audits can compare perspectives

---

## 8. Formal Properties

### 8.1 Determinism Property

**Statement:** Identical inputs produce identical outputs.

$$S = S' \Rightarrow D = D'$$

**Proof sketch:**
- All components are deterministic (prime encoding, modular rotation, aggregation)
- No randomness or external state
- Event chain is fixed and ordered
- Memory is immutable once written

**Consequence:** The system is fully reproducible and auditable.

### 8.2 Monotonicity Property

**Statement:** Increased risk leads to equal-or-greater protective action.

$$r > r' \Rightarrow a \geq a'$$

**Proof sketch:**
- Projection function Φ is monotonically increasing
- Risk aggregation is a weighted sum (monotonic)
- Protection levels are ordered: Low < Medium < High

**Consequence:** The system cannot decrease protection in response to increased risk.

### 8.3 Role Symmetry Property

**Statement:** Agency and subject memories are maintained in parallel.

$$M_a(t) \neq \emptyset \text{ and } M_s(t) \neq \emptyset \text{ for all } t$$

**Consequence:** Both perspectives are preserved for fairness audits and accountability.

### 8.4 Collision‑Free Encoding Property

**Statement:** No two categories share a prime index.

$$c_i \neq c_j \Rightarrow \pi(c_i) \neq \pi(c_j)$$

**Proof:** π is a bijection from C to a subset of P (primes). Primes are unique by definition.

**Consequence:** Semantic categories cannot be confused; encoding is unambiguous.

### 8.5 Temporal Consistency Property

**Statement:** Timestamps are monotonically increasing.

$$T_{t+1} > T_t \text{ for all } t$$

**Consequence:** Event ordering is preservable; causality can be reconstructed.

### 8.6 Invertibility Property (Conditional)

**Statement:** If gcd(θ_k, m) = 1, rotation R_k is invertible.

$$R_k^{-1}(R_k(S)) = S$$

**Consequence:** Decision chains can be traced backward to understand prior state.

---

## 9. Extensibility Model

The ontology is designed to support extension while preserving core properties.

### 9.1 Extension Points

**New Categories:**

Add to C:
- Define new semantic category
- Assign unique prime via π
- Set initial weight
- Update all dependent functions

**Requirement:** π remains bijective (one prime per category).

**New Rotational Operators:**

Add to {R_k}:
- Define rotation angle θ and semantics
- Specify position in event chain
- Prove determinism and monotonicity
- Document audit trail generation

**Requirement:** Operator composition remains associative; chain ordering is preserved.

**New Projection Functions:**

Extend Φ:
- Define new risk-to-action mapping
- Verify monotonicity: r ↑ ⇒ a ↑
- Test against baseline cases
- Document statutory alignment

**Requirement:** All existing constraints must still hold.

**Domain‑Specific Modules:**

Layer domain knowledge on top without modifying core:
- Child welfare module: specialized categories, constraints, thresholds
- Public safety module: threat assessment, escalation rules
- AI governance module: trust scores, transparency requirements

**Requirement:** All modules use the same core event chain and memory structure.

### 9.2 Preservation Invariants

Any extension must preserve:

1. **Determinism:** S = S' ⇒ D = D'
2. **Prime Uniqueness:** π is bijective
3. **Operator Consistency:** New operators are deterministic
4. **Event‑Chain Ordering:** Sequence is fixed
5. **Role Symmetry:** M_a and M_s remain parallel
6. **Monotonicity:** Risk → Action is monotonic

---

## 10. Comparison to Standard Ontologies

### 10.1 vs. OWL/RDF

| Aspect | OWL/RDF | RPO |
|--------|---------|-----|
| **Purpose** | Semantic interoperability | Operational decision execution |
| **Reasoning** | Logical inference | Deterministic transformation |
| **Expressiveness** | High (first-order logic) | Lower (domain-specific) |
| **Auditability** | Medium (depends on reasoner) | High (fully traceable) |
| **Determinism** | No guarantee | Guaranteed by design |
| **Scalability** | Excellent for knowledge graphs | Good for decision pipelines |
| **Compliance** | Not designed for it | Built-in statutory alignment |

**Recommendation:** Use OWL for shared ontology infrastructure; use RPO as the decision execution layer.

### 10.2 vs. BFO (Basic Formal Ontology)

| Aspect | BFO | RPO |
|--------|-----|-----|
| **Scope** | General foundational ontology | Specialized decision ontology |
| **Rigor** | Very high (philosophical grounding) | High (operational guarantees) |
| **Real-world entities** | Excellent modeling | Less focused |
| **Decision support** | Not primary design goal | Core design goal |
| **Auditability** | Medium | High |
| **Determinism** | Not enforced | Enforced |

**Recommendation:** RPO can be grounded on BFO categories for conceptual rigor.

### 10.3 vs. Event Ontologies

| Aspect | Event Ontologies | RPO |
|--------|------------------|-----|
| **Time modeling** | Flexible, rich | Ordered, deterministic |
| **Causality** | Declarative | Encoded in operator order |
| **State transitions** | Described | Executed deterministically |
| **Memory** | Often not built-in | Core design: paired memory |
| **Role symmetry** | Not standard | Built-in |

**Recommendation:** RPO's paired temporal memory is stronger than typical event ontologies for governance.

---

## 11. Implementation Mapping

### 11.1 Python Classes to Formal Notation

| Formal Concept | Python Class | File |
|----------------|--------------|------|
| π : C → P | `PrimeEncoder` | `ontology/core.py` |
| R_k : S → S | `RotationalOperator` | `ontology/core.py` |
| M_a, M_s | `PairedTemporalMemory` | `ontology/memory.py` |
| S = (V, M, T) | `DecisionState` | `ontology/state.py` |
| Φ : r → a | `ProtectionProjector` | `ontology/projection.py` |
| Event chain | `api/server.py` | `/evaluate` endpoint |

### 11.2 Test Coverage

| Property | Test |
|----------|------|
| Determinism | `test_prime_encoding_is_stable_and_unique` |
| Monotonicity | `test_risk_levels_are_correct` |
| Role Symmetry | `test_memory_tracks_correlations` |
| Collision-Free | `test_concepts_are_assigned_in_order` |
| Immutability | `test_state_values_dict_mutation_is_immutable` |
| Invertibility | `test_rotation_wraps_and_inverts` |

---

## 12. Limitations and Risks

### 12.1 Known Limitations

1. **Scalability:** Prime indexing becomes expensive for very large category sets (>100 categories).
2. **Expressiveness:** Rotational operators are simpler than full logical inference.
3. **Interoperability:** Not compatible with existing OWL/RDF tools without bridging layer.
4. **Domain Specificity:** Categories and thresholds must be carefully tuned per domain.

### 12.2 Risk Mitigation

1. **Validation:** All outputs require human review in high-consequence domains.
2. **Monitoring:** Track decision accuracy and fairness metrics continuously.
3. **Auditability:** Complete audit trails enable post-hoc investigation.
4. **Testing:** Extensive unit and integration tests ensure consistency.

---

## 13. Future Work

1. **Formal Verification:** Use theorem provers (Coq, Isabelle) to verify invariants.
2. **Fairness Theorems:** Prove role-symmetry guarantees reduce bias.
3. **Scalability:** Optimize prime generation for very large category sets.
4. **Integration:** Develop OWL bridge for semantic interoperability.
5. **Domain Applications:** Implement and validate in public safety, child welfare, and AI governance.

---

## References

- Kinney, J. (2026). The Rotational Prime Ontology: A Deterministic Architecture for Governance-Grade Decision Systems.
- W3C. OWL 2 Web Ontology Language. https://www.w3.org/TR/owl2-overview/
- Arp, R., Smith, B., & Spear, A. D. (2015). Building Ontologies with Basic Formal Ontology. MIT Press.
- Allen, J. F. (1983). Maintaining Knowledge about Temporal Intervals. Communications of the ACM, 26(11), 832–843.

---

**Document Version:** 1.0  
**Date:** 2026-09-28  
**Status:** Formal Specification (Complete)
