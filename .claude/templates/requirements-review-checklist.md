---
tier: 3
purpose: Specification review process
reload_trigger: When reviewing specs
estimated_read_time: 10 minutes
---

# Requirements Review Checklist

**Version**: 2.0
**Last Updated**: 2025-09-30
**Purpose**: Critical review framework for user-submitted requirements documents

---

## Overview

When users provide requirements documents (PDFs, Word docs, Markdown, acceptance criteria), Claude must:
1. **Review critically** - Identify gaps, ambiguities, contradictions
2. **Convert to use cases** - Transform into framework-compliant specifications
3. **Validate completeness** - Ensure all necessary information is present
4. **Challenge assumptions** - Question unclear or potentially problematic requirements

---

## Phase 1: Initial Review 📄

### Document Intake
- [ ] Identify document type (requirements doc, acceptance criteria, user stories, PRD)
- [ ] Note document format (PDF, Word, Markdown, text)
- [ ] Extract key sections (objectives, features, constraints, acceptance criteria)
- [ ] Identify primary stakeholder perspective (business, technical, user)

### Completeness Check
- [ ] **Problem Statement**: Is the business problem clearly defined?
- [ ] **Target Users**: Are user personas or target audience specified?
- [ ] **Success Criteria**: How will success be measured?
- [ ] **Scope Boundaries**: What's explicitly in/out of scope?
- [ ] **Constraints**: Technical, business, timeline, resource constraints?
- [ ] **Dependencies**: External systems, services, or prerequisites?

### Red Flags to Identify
- ❌ Vague language ("fast", "user-friendly", "scalable" without definitions)
- ❌ Missing acceptance criteria
- ❌ Implementation prescribed without why (e.g., "use Redis" without justification)
- ❌ Conflicting requirements
- ❌ Unrealistic constraints (e.g., "100% uptime" without budget for redundancy)
- ❌ Missing error scenarios
- ❌ No performance criteria

**Output**: Initial assessment report with red flags highlighted

---

## Phase 2: Critical Analysis 🔍

### Clarity Assessment
For each requirement, verify:
- [ ] **Unambiguous**: Only one interpretation possible?
- [ ] **Testable**: Can you write a test to verify it?
- [ ] **Measurable**: Quantified or clearly verifiable?
- [ ] **Complete**: All scenarios covered (happy path + edge cases)?

### Example Critical Questions to Ask User:

**Vague Requirements**:
> "Requirement says 'fast response time' - what specific response time threshold defines success? (e.g., 95th percentile < 200ms)"

**Missing Error Scenarios**:
> "I see the happy path for user login, but what should happen when: password is wrong, account is locked, email doesn't exist?"

**Implementation Details Without Rationale**:
> "Document specifies using PostgreSQL - is this a hard constraint or a suggestion? What drives this choice?"

**Scope Ambiguity**:
> "Should the API support bulk operations, or only single-item operations? This affects architecture."

**Missing Non-Functional Requirements**:
> "What's the expected scale? (concurrent users, requests/second, data volume) This affects design decisions."

### Contradiction Detection
- [ ] Cross-check requirements for conflicts
- [ ] Verify acceptance criteria align with objectives
- [ ] Ensure constraints don't make objectives impossible
- [ ] Flag mutually exclusive requirements

**Output**: List of clarification questions for user

---

## Phase 3: Gap Analysis 🕳️

### Information Gaps
Check for missing:
- [ ] **Authentication/Authorization**: Who can do what?
- [ ] **Error Handling**: What happens when things go wrong?
- [ ] **Data Validation**: Input validation rules?
- [ ] **Audit/Logging**: What needs tracking?
- [ ] **Performance**: Response time, throughput expectations?
- [ ] **Security**: Sensitive data handling, encryption, compliance?
- [ ] **Internationalization**: Multi-language, timezone, currency support?
- [ ] **Accessibility**: WCAG compliance, screen reader support?
- [ ] **Browser/Platform Support**: Which versions/platforms?
- [ ] **Data Retention**: How long to keep data? Deletion rules?

### Scenario Gaps
- [ ] Happy path covered?
- [ ] Error scenarios covered?
- [ ] Edge cases identified?
- [ ] Concurrency scenarios addressed?
- [ ] Rollback/recovery procedures?

**Output**: Comprehensive gap list

---

## Phase 4: Requirements Transformation 📝

### Convert to Use Case Format

For each feature/requirement, create use case with: Objective, Actors, Preconditions, Main Flow, Alternative Flows, Error Scenarios, Acceptance Criteria (Given/When/Then), Data Requirements (Input/Output/Validation), Non-Functional Requirements (Performance/Security/Reliability), Open Questions.

**See**: `.claude/templates/use-case-template.md` for complete template

### Conversion Process
- [ ] Group related requirements into use cases
- [ ] Extract acceptance criteria
- [ ] Identify missing scenarios
- [ ] Add spec structure (flows, error cases, data)
- [ ] Link to ADRs for technical decisions
- [ ] Flag open questions

**Output**: Draft use case specifications

---

## Phase 5: Validation & Review 🎯

### Specification Quality Check
- [ ] Every requirement mapped to use case?
- [ ] All use cases have acceptance criteria?
- [ ] All use cases testable?
- [ ] Dependencies between use cases identified?
- [ ] Priority/sequencing determined?

### User Review Session
Present to user:
1. **Transformed specifications**: Show use case documents
2. **Clarification questions**: List of gaps/ambiguities
3. **Red flags identified**: Contradictions, unrealistic items
4. **Suggested changes**: Improvements to original requirements
5. **Implementation plan**: Proposed iteration sequence

**Format**:
```
📋 Requirements Review Summary

✅ CLEAR & COMPLETE:
- [List requirements that are good as-is]

⚠️ NEEDS CLARIFICATION:
- [Requirement X]: [Specific question]
- [Requirement Y]: [Why it's ambiguous]

❌ ISSUES IDENTIFIED:
- [Contradiction between A and B]
- [Unrealistic constraint C]

📝 TRANSFORMED TO:
- UC-001: [Use case name]
- UC-002: [Use case name]
...

🔄 RECOMMENDED SEQUENCE:
Iteration 1: [UC-001, UC-002] (foundation)
Iteration 2: [UC-003] (builds on iteration 1)
...

❓ OPEN QUESTIONS:
1. [Question requiring user input]
2. ...
```

**Output**: Requirements review report + draft use case specifications

---

## Phase 6: Specification Finalization ✓

### After User Feedback
- [ ] Incorporate user answers to clarification questions
- [ ] Resolve contradictions with user guidance
- [ ] Update use case specifications
- [ ] Remove "Draft" status from approved specs
- [ ] Create ADRs for technical decisions
- [ ] Update project overview with scope

### Verification
- [ ] All original requirements accounted for
- [ ] All open questions resolved or explicitly deferred
- [ ] Specs follow framework format (BDD scenarios, acceptance criteria)
- [ ] Ready for iteration planning

**Output**: Finalized use case specifications ready for implementation

---

## Critical Review Principles

### Always Challenge
- **"How would this fail?"** - Force error scenario thinking
- **"What if 10,000 users do this simultaneously?"** - Force scale thinking
- **"What if the third-party API is down?"** - Force resilience thinking
- **"How do we test this?"** - Force testability thinking

### Never Accept
- ❌ "It should be intuitive" (not testable)
- ❌ "Fast enough" (not measurable)
- ❌ "Secure" (not specific)
- ❌ "User-friendly" (not defined)
- ❌ Implementation without rationale

### Always Ask
- ✅ "What specific metric defines success here?"
- ✅ "What happens when [error scenario]?"
- ✅ "Why this technical choice over alternatives?"
- ✅ "How do we verify this works correctly?"
- ✅ "What's the user impact if this fails?"

---

## Common Requirement Pitfalls

| Pitfall | Bad | Good |
|---------|-----|------|
| **Solution vs Need** | "Use JWT tokens" | "Users authenticate; sessions persist across requests" |
| **Ambiguous Metrics** | "System should be fast" | "95th percentile < 200ms; 99th < 500ms" |
| **Missing Failures** | "User uploads picture" | "User uploads picture (max 5MB, JPG/PNG). Errors: size, format, failure" |
| **Implied vs Explicit** | "Admin deletes users" | "Admin deletes users → archive data, disable login, anonymize content, log" |

---

## Success Criteria

You've done this right if:
- ✅ Every vague requirement has clarifying questions
- ✅ Every requirement maps to testable acceptance criteria
- ✅ Error scenarios are explicitly documented
- ✅ Non-functional requirements are quantified
- ✅ User understands gaps you've identified
- ✅ Final specifications are unambiguous and complete

---

## Emergency Procedures

### If Requirements are Severely Incomplete
1. **STOP transformation process**
2. Say: "These requirements have significant gaps. Before converting to specifications, I need answers to [X] critical questions."
3. Present gap list with prioritization
4. Get user input
5. THEN proceed with transformation

### If Requirements Conflict
1. **STOP and highlight conflict**
2. Say: "Requirement A says [X], but Requirement B says [Y]. These conflict because [reason]. Which should take precedence?"
3. Document user decision as ADR
4. Update specifications accordingly

### If Requirements Prescribe Bad Architecture
1. **Flag the issue**
2. Say: "Requirement specifies [technical solution], but this may cause [problem]. Can we reframe as: [user need] and evaluate options?"
3. If user insists: Create ADR documenting decision and risks
4. If user open: Create ADR evaluating alternatives

---

**Remember**: Your job is to **protect the user from their own ambiguity**. Better to ask clarifying questions now than build the wrong thing.
---

**Template Version**: 1.0
**Framework**: Claude Development Framework v2.2
**Last Updated**: 2025-10-01
**Compatibility**: Framework v2.2+
