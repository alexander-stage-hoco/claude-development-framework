---
tier: 2
purpose: Service catalog template
reload_trigger: When working with services
estimated_read_time: 5 minutes
---

# Service Registry

**Project**: [PROJECT_NAME]
**Last Updated**: [DATE]
**Total Services**: 0

---

## Purpose

This file maintains a central catalog of all services in the system:
- Service inventory and status
- Dependency relationships
- UC-to-Service traceability
- Infrastructure requirements
- Performance metrics

**Update Frequency**: After every service addition, modification, or removal

---

## Service Catalog

| Service ID | Name | Status | Dependencies | Used By (UCs) | Location |
|------------|------|--------|--------------|---------------|----------|
| SVC-001 | [ServiceName] | [Draft/Implemented/Optimized/Deprecated] | [SVC-XXX, SVC-YYY] or None | UC-001, UC-002 | `services/[name]/` |

**Example**:
```
| Service ID | Name | Status | Dependencies | Used By (UCs) | Location |
|------------|------|--------|--------------|---------------|----------|
| SVC-001 | AuthService | Implemented | SVC-003 (ValidationService) | UC-001, UC-002, UC-003 | services/auth-service/ |
| SVC-002 | UserService | Implemented | SVC-004 (DatabaseService) | UC-001, UC-004, UC-005 | services/user-service/ |
| SVC-003 | ValidationService | Implemented | None | SVC-001, SVC-002 | services/validation-service/ |
| SVC-004 | DatabaseService | Implemented | None | SVC-002, SVC-005 | services/database-service/ |
| SVC-005 | EmailService | Implemented | None | UC-001, UC-003, UC-007 | services/email-service/ |
```

**Status Definitions**:
- **Draft**: Service identified but not yet designed
- **Design**: Specification complete, not yet implemented
- **Implemented**: Code written, tests passing
- **Optimized**: Benchmarked and tuned for performance
- **Deprecated**: Marked for removal, do not use in new UCs

---

## Dependency Graph

**Purpose**: Visualize service dependencies to detect coupling issues

### Layered Architecture

```
Layer 1 (Infrastructure - No dependencies on other services):
├── DatabaseService (SVC-004)
├── CacheService (SVC-006)
├── LogService (SVC-007)
└── ValidationService (SVC-003)

Layer 2 (Domain Services - Depend only on Layer 1):
├── UserService (SVC-002) → DatabaseService
├── EmailService (SVC-005) → None
└── SessionService (SVC-008) → CacheService

Layer 3 (Application Services - Depend on Layer 1 & 2):
├── AuthService (SVC-001) → ValidationService, UserService, SessionService
└── NotificationService (SVC-009) → EmailService, UserService
```

**Dependency Rules**:
- ✅ Layer N may depend on Layer N-1, N-2, etc.
- ❌ Layer N must NOT depend on Layer N+1 (upward dependency)
- ❌ No circular dependencies (A→B→C→A)
- ⚠️ If a service has >3 dependencies, consider splitting

**Dependency Complexity**: [Simple: 0-2 deps | Moderate: 3-4 deps | High: 5+ deps]

---

## Service-to-UC Traceability

**Purpose**: Map which use cases depend on which services

### By Service

#### SVC-001: AuthService
- **UC-001**: User Registration (methods: `register()`, `hash_password()`)
- **UC-002**: User Login (methods: `authenticate()`, `create_session()`)
- **UC-003**: Password Reset (methods: `verify_reset_token()`, `update_password()`)

#### SVC-002: UserService
- **UC-001**: User Registration (methods: `create_user()`)
- **UC-004**: View Profile (methods: `get_user()`)
- **UC-005**: Update Profile (methods: `update_user()`)

#### SVC-005: EmailService
- **UC-001**: User Registration (methods: `send_welcome_email()`)
- **UC-003**: Password Reset (methods: `send_reset_email()`)
- **UC-007**: Notification (methods: `send_notification()`)

---

### By Use Case

#### UC-001: User Registration
- **SVC-001** (AuthService): Register user, hash password
- **SVC-002** (UserService): Create user record
- **SVC-005** (EmailService): Send welcome email

#### UC-002: User Login
- **SVC-001** (AuthService): Authenticate credentials, create session
- **SVC-002** (UserService): Retrieve user data

#### UC-003: Password Reset
- **SVC-001** (AuthService): Verify token, update password
- **SVC-005** (EmailService): Send reset email

---

## UC Without Services (Red Flags)

**UCs with no service references should be challenged**:

| UC ID | UC Name | Why No Services? | Resolution |
|-------|---------|------------------|------------|
| UC-010 | View Dashboard | Read-only UI | Justified: Pure view, no business logic |
| UC-015 | Update Theme | Pure UI change | Justified: User preference, no backend |

**Guidelines**:
- If UC has business logic → MUST have service
- If UC modifies data → MUST have service
- If UC only displays data → MAY be serviceless (but consider read service)

---

## Unused Services (Waste Alert)

**Services defined but not used by any UC**:

| Service ID | Service Name | Reason Not Used | Action |
|------------|-------------|-----------------|--------|
| SVC-012 | PaymentService | Future feature (planned for Q2) | Keep (documented plan) |
| SVC-014 | LegacyImporter | One-time migration complete | Remove (no longer needed) |

**Action Triggers**:
- Service unused for >3 months → Review for removal
- Service designed but never implemented → Reconsider need

---

## Infrastructure Requirements

**Purpose**: Track external dependencies (databases, caches, APIs)

| Infrastructure | Type | Used By Services | Purpose | Configuration |
|----------------|------|------------------|---------|---------------|
| PostgreSQL | Database | SVC-002, SVC-008, SVC-010 | Primary data store | Tables: users, sessions, orders |
| Redis | Cache | SVC-006, SVC-008 | Caching & sessions | Keys: `user:*`, `session:*` |
| SMTP Server | External API | SVC-005 | Email delivery | Host: smtp.example.com |
| AWS S3 | Object Storage | SVC-011 | File storage | Bucket: app-uploads |
| Stripe API | External API | SVC-012 | Payment processing | API Key (env: STRIPE_KEY) |

**Infrastructure Health**:
- Monitor availability
- Track API rate limits
- Document failover strategies

---

## Performance Metrics Dashboard

**Purpose**: Track service performance over time

| Service | Latency (p95) | Throughput | Error Rate | Last Benchmark | Status |
|---------|---------------|------------|------------|----------------|--------|
| AuthService | 15ms | 500 req/s | 0.01% | 2025-10-01 | ✅ Healthy |
| UserService | 20ms | 400 req/s | 0.05% | 2025-10-01 | ✅ Healthy |
| EmailService | 120ms | 50 req/s | 0.5% | 2025-09-28 | ⚠️ High latency |
| DatabaseService | 8ms | 1000 req/s | 0.001% | 2025-10-01 | ✅ Healthy |

**Thresholds**:
- 🟢 Healthy: Within target metrics
- 🟡 Warning: Approaching threshold
- 🔴 Critical: Exceeds threshold, requires action

**Benchmark Frequency**:
- Critical services: Monthly
- Standard services: Quarterly
- Low-traffic services: Annually or when issues arise

---

## Service Lifecycle Tracking

| Service | Phase | Created | Implemented | Optimized | Deprecated | Removed |
|---------|-------|---------|-------------|-----------|------------|---------|
| AuthService | Production | 2025-01-15 | 2025-01-20 | 2025-02-10 | - | - |
| UserService | Production | 2025-01-15 | 2025-01-22 | - | - | - |
| LegacyImporter | Removed | 2025-03-01 | 2025-03-05 | - | 2025-04-01 | 2025-04-15 |
| PaymentService | Design | 2025-09-20 | - | - | - | - |

**Lifecycle Stages**:
1. **Draft**: Identified in UC but not designed
2. **Design**: service-spec.md complete
3. **Implemented**: Code + tests complete
4. **Optimized**: Benchmarked and tuned
5. **Deprecated**: Marked for removal
6. **Removed**: Deleted from codebase

---

## Service Health Checklist

Use this checklist to assess service health:

### Per Service

- [ ] Specification exists and is up to date
- [ ] All methods have tests (unit + integration)
- [ ] Documentation complete (interface, error handling, examples)
- [ ] Performance meets targets (if benchmarked)
- [ ] Dependencies minimized (<3 service deps)
- [ ] No circular dependencies
- [ ] Used by at least 1 use case (or removal planned)
- [ ] Error handling comprehensive
- [ ] Monitoring configured
- [ ] Security reviewed (if handles sensitive data)

---

## Change Log

Track significant changes to services:

| Date | Service | Change | Impact | ADR |
|------|---------|--------|--------|-----|
| 2025-10-01 | AuthService | Added MFA support | UC-002 updated | ADR-015 |
| 2025-09-28 | EmailService | Switched to SendGrid | Performance improved 50% | ADR-014 |
| 2025-09-15 | UserService | Added caching layer | Latency reduced from 40ms to 20ms | ADR-013 |

---

## Service Ownership

**Purpose**: Track who is responsible for each service

| Service | Primary Owner | Secondary Owner | Team |
|---------|---------------|-----------------|------|
| AuthService | [Name/Email] | [Name/Email] | Backend |
| UserService | [Name/Email] | [Name/Email] | Backend |
| EmailService | [Name/Email] | [Name/Email] | Platform |

**Ownership Responsibilities**:
- Maintain service specification
- Review PRs for service changes
- Monitor service health
- Respond to service issues
- Conduct periodic benchmarks

---

## Open Questions & Issues

Track unresolved questions about service architecture:

- [ ] **Question 1**: Should we split UserService into UserReadService and UserWriteService (CQRS)?
  - **Impact**: Affects UC-004, UC-005, UC-009
  - **Decision by**: 2025-10-15

- [ ] **Question 2**: PaymentService external dependency (Stripe vs. PayPal)?
  - **Impact**: Affects UC-020 (Checkout)
  - **Decision by**: 2025-11-01

---

## Quick Reference: Service Extraction Workflow

When creating a new service:

1. **Identify Need**: UC requires capability not provided by existing services
2. **Check Registry**: Verify service doesn't already exist
3. **Create Spec**: Copy `.claude/templates/service-spec.md` to `services/[name]/service-spec.md`
4. **Update Registry**: Add row to Service Catalog table
5. **Design Interface**: Define Protocol with type hints
6. **Library Search**: Evaluate existing libraries (create `library-evaluation.md`)
7. **Implement**: Write code + tests
8. **Benchmark** (if performance critical): Run benchmarks, create `benchmark-report.md`
9. **Document UCs**: Update UC specifications with service references
10. **Update Traceability**: Add to Service-to-UC section

---

## Template Metadata

**Template Version**: 1.0
**Framework**: Claude Development Framework v2.0
**Purpose**: Central service registry (copy to `.claude/service-registry.md` in project)

**Instructions**:
- Replace `[PROJECT_NAME]` with actual project name
- Remove example services (AuthService, UserService, etc.)
- Update as services are added/modified/removed
- Review monthly for accuracy
