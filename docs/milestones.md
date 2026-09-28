# AskLearnly learning and milestone tracker

This tracker records learning scope, implementation work, verification, and proof-of-work checkpoints. Estimates include study, implementation, debugging, tests, and documentation. Actual hours are updated after work sessions rather than inferred from commit history.

## Working rules

- Keep only one backend and RAG milestone in progress.
- Record actual focused hours after every work session.
- End each session with one concrete next task.
- Commit coherent, working increments after relevant checks pass.
- Push completed checkpoints and milestones to `main`.
- Do not mark a milestone complete until its definition of done passes.
- Record blockers and unexpected work in the relevant milestone.
- Formal RAG evaluation, authentication, OCR, and persisted conversations remain outside the initial scope.

## Schedule

| Milestone | Status | Estimate | Actual | Target | Owner |
| --- | --- | ---: | ---: | --- | --- |
| 1. RAG and project foundation | Completed | 12 h | Not recorded | Week 1 | Yash / Shared |
| 2. AskLearnly interface | Completed | Not recorded | Not recorded | Completed | Frontend |
| 3. Document loading and Learnly synchronization | In progress | 28 h | — | Week 2 | Yash |
| 4. Chunking and metadata | Not started | 32 h | — | Week 4 | Yash / Frontend |
| 5. Embeddings and exact vector retrieval | Not started | 40 h | — | Week 6 | Yash / Frontend |
| 6. Grounded answers and streaming | Not started | 24 h | — | Week 7 | Shared |
| 7. PostgreSQL, pgvector, HNSW, and IVFFlat | Not started | 36 h | — | Week 9 | Yash / Frontend |
| 8. Advanced retrieval | Not started | 44 h | — | Week 11 | Yash / Frontend |
| 9. Embedding models and LangChain adapter | Not started | 20 h | — | Week 12 | Shared |
| 10. Complete Learnly integration | Not started | 16 h | — | Week 13 | Frontend / Yash |

Plan for approximately 20 focused hours per week and keep a two-week buffer for debugging and integration work.

## Milestone 1 — RAG and project foundation

- **Status:** Completed
- **Estimate:** 12 hours
- **Actual:** Not recorded
- **Owner:** Yash for backend; shared documentation

### Topics

- What RAG is and which problems it solves
- Hallucinations and knowledge cutoffs
- Knowledge base → retriever → generator data flow
- RAG versus fine-tuning versus prompt engineering
- Offline indexing versus online query processing
- FastAPI service architecture
- Configuration and secret management
- REST, JSON, SSE, CORS, and Pydantic schemas
- Separation between frontend, backend, and Learnly

### Completed implementation

- [x] Created the Python 3.12 backend project with a `src` layout.
- [x] Added FastAPI application configuration and environment settings.
- [x] Implemented `GET /api/v1/health`.
- [x] Configured frontend CORS behavior.
- [x] Converted the REST and streaming contract into validated Pydantic schemas.
- [x] Added environment examples without secrets.
- [x] Added backend unit and contract tests.
- [x] Documented indexing and query data flows.

### Verification

- [x] Ruff formatting passes.
- [x] Ruff linting passes.
- [x] Mypy strict checking passes.
- [x] Backend test suite passes: 41 tests.
- [x] Health, unknown-route, allowed-origin, preflight, and rejected-origin behavior are tested.
- [x] JSON fields serialize using the documented camelCase contract.

### Commit checkpoints

- `9bdc4b6 feat(backend): add health service foundation`
- `54104c7 feat(backend): add application configuration`
- `9b2c8d3 feat(backend): configure cors middleware`
- `5cd6cfd feat(backend): add shared api schema base`
- `ffcc77a feat(backend): add source api schemas`
- `da71fae feat(backend): add source synchronization schemas`
- `5cd7744 feat(backend): add chat request schemas`
- `1602cfc feat(backend): add streaming event schemas`

### Definition of done

The backend starts locally, the health endpoint passes, configuration is environment-driven, CORS permits the configured frontend, and typed schemas match the documented REST and streaming contract.

### Notes and blockers

- Actual focused hours were not recorded during this milestone.
- Two current test warnings originate from FastAPI and Starlette test-client dependencies.

## Milestone 2 — AskLearnly interface

- **Status:** Completed
- **Estimate:** Not recorded
- **Actual:** Not recorded
- **Owner:** Frontend

### Topics

- RAG application UX and source scoping
- Conversation and evidence presentation
- Streaming interface states and citation interaction
- Retrieval configuration
- Responsive layouts and mobile drawers
- Loading, empty, disconnected, retry, and error states
- Keyboard and screen-reader accessibility

### Completed implementation

- [x] Responsive three-panel workspace
- [x] Source selection and synchronization interface
- [x] Conversation workspace and evidence panel
- [x] Retrieval controls and mocked streaming transport
- [x] Dark theme, frontend tests, and production build

### Commit checkpoint

- `773181b feat(frontend): add asklearnly workspace`

### Definition of done

The responsive AskLearnly workspace presents source selection, conversation, evidence, retrieval controls, and all required interface states using mocked data.

### Notes and blockers

- Live backend integration is completed in later milestones.

## Milestone 3 — Document loading and Learnly synchronization

- **Status:** In progress
- **Estimate:** 28 hours
- **Actual:** —
- **Owner:** Yash; frontend connection support as needed

### Topics

- Document loader responsibilities
- PDF, web, and structured-data loading concepts
- PDF text extraction without LangChain
- Searchable versus scanned PDFs
- Page-level text preservation
- Source metadata, checksums, and idempotent synchronization
- Duplicate, removed, empty, corrupt, and failed documents
- API boundaries between independently deployed applications

### Implementation checklist

- [ ] Define a provider-neutral loader interface.
- [ ] Define the minimal Learnly published-document integration schema.
- [ ] Fetch published documents through the Learnly REST API.
- [ ] Download searchable PDFs without exposing storage keys.
- [ ] Extract text page by page.
- [ ] Preserve Learnly ID, title, topics, page number, preview URL, and checksum.
- [ ] Skip unchanged documents and detect updated or removed documents.
- [ ] Handle duplicate, empty, corrupt, scanned, and failed PDFs safely.
- [ ] Implement `GET /api/v1/sources`.
- [ ] Implement `POST /api/v1/sources/sync`.
- [ ] Connect frontend source and synchronization states.
- [ ] Test synchronization with representative searchable PDFs.

### Verification

- [ ] Synchronizing twice does not create duplicates.
- [ ] Changed and removed files are detected.
- [ ] Failed documents return safe errors without removing the last usable version.
- [ ] Page text and source metadata remain traceable.
- [ ] Source and synchronization responses match the frozen API contract.

### Commit checkpoints

- `feat(backend): add learnly document synchronization`
- `feat(frontend): add source synchronization experience`

### Definition of done

AskLearnly can synchronize the published Learnly collection repeatedly, preserve page-level metadata, skip unchanged files, report failures safely, and expose source state to the frontend.

### Notes and blockers

- Current task: define and test the minimal published-document contract between Learnly and AskLearnly.
- Learnly's current general document response does not expose `checksum_sha256` or `mime_type`; add them or create a dedicated published-document synchronization response.
- The integration response must provide a usable PDF download URL and must never expose `storage_key`.

## Milestone 4 — Chunking and metadata

- **Status:** Not started
- **Estimate:** 32 hours
- **Actual:** —
- **Owner:** Yash; frontend indexing-details support

### Topics

- Why chunking is required
- Character, recursive, Markdown-aware, and code-aware splitting
- Semantic splitting
- Chunk size and overlap trade-offs
- Retrieval precision versus context completeness
- Metadata management and filtering
- Stable identifiers, page and character offsets, checksums, and deterministic re-indexing

### Implementation checklist

- [ ] Define stable `Document` and `Chunk` models.
- [ ] Implement character, recursive, Markdown-aware, and isolated code-block splitting.
- [ ] Begin with an 800-character size and 120-character overlap baseline.
- [ ] Preserve source ID, page, offsets, chunk index, topics, and checksum.
- [ ] Make chunking configuration explicit.
- [ ] Inspect real chunks from different PDFs.
- [ ] Add semantic chunking after embeddings are available.
- [ ] Add boundary, overlap, empty-page, and deterministic-output tests.
- [ ] Show indexing details in the frontend.

### Verification

- [ ] Every chunk traces back to its document and page.
- [ ] Repeated chunking produces stable output.
- [ ] Each strategy has tests and documented trade-offs.

### Commit checkpoints

- `feat(backend): implement configurable chunking`
- `feat(frontend): add source indexing details`

### Definition of done

All configured splitting strategies produce deterministic, traceable chunks with production metadata and tested boundaries.

### Notes and blockers

- None recorded.

## Milestone 5 — Embeddings and exact vector retrieval

- **Status:** Not started
- **Estimate:** 40 hours
- **Actual:** —
- **Owner:** Yash; frontend evidence integration

### Topics

- Vector representations, dimensions, and semantic similarity
- Cosine similarity, dot product, and Euclidean distance
- Normalized and non-normalized vectors
- Query and document compatibility
- Batching, model identity, dimensions, and cost-quality trade-offs
- Vector-store CRUD, exact top-K search, metadata filtering, and score thresholds

### Implementation checklist

- [ ] Implement cosine similarity, dot product, and Euclidean distance with NumPy.
- [ ] Verify the metrics with manual and synthetic examples.
- [ ] Define a provider-neutral embedding interface.
- [ ] Add direct hosted embeddings with batching and retry-safe boundaries.
- [ ] Track provider, model, dimensions, and creation time.
- [ ] Reject incompatible vector dimensions.
- [ ] Build an in-memory vector store with CRUD operations.
- [ ] Implement exact cosine top-K search, filters, and thresholds.
- [ ] Add semantic chunking using embeddings.
- [ ] Show retrieved evidence in the frontend.

### Verification

- [ ] Known synthetic vectors produce the expected ranking.
- [ ] Documents can be created, read, updated, deleted, filtered, and retrieved.
- [ ] No retriever or vector-store framework abstraction is used.

### Commit checkpoints

- `feat(backend): add embedding provider and similarity metrics`
- `feat(backend): implement exact vector retrieval`
- `feat(frontend): add retrieved evidence experience`

### Definition of done

Documents can be embedded and retrieved through a tested, exact vector-search implementation whose metrics and ranking behavior can be explained from first principles.

### Notes and blockers

- None recorded.

## Milestone 6 — Grounded answers and streaming

- **Status:** Not started
- **Estimate:** 24 hours
- **Actual:** —
- **Owner:** Shared

### Topics

- Query embedding and retrieval-to-generation flow
- Top-K context construction and context-window budgeting
- Grounded prompts, citation labels, and unsupported-answer prevention
- Insufficient-context behavior
- Server-Sent Events, token streaming, cancellation, and failures
- Session-only conversation history

### Implementation checklist

- [ ] Embed each question and retrieve from the selected source scope.
- [ ] Convert retrieved chunks into citation-labelled context.
- [ ] Generate an answer using the direct model SDK.
- [ ] Implement `POST /api/v1/chat/stream`.
- [ ] Stream `retrieval`, `token`, `done`, and `error` events.
- [ ] Return an insufficient-context answer when evidence is unacceptable.
- [ ] Connect the frontend to the live stream.
- [ ] Verify cancellation, retry, citations, and PDF page links.
- [ ] Test malformed requests and interrupted streams.

### Verification

- [ ] Retrieval evidence arrives before answer tokens.
- [ ] Answers are grounded in the supplied context.
- [ ] Citations open the correct Learnly document and page.
- [ ] Stream cancellation and safe failures work.

### Commit checkpoints

- `feat(backend): stream grounded answers with citations`
- `feat(frontend): connect live asklearnly streaming`

### Definition of done

A question produces a streamed, source-grounded answer with working page-level citations and safe insufficient-context behavior.

### Notes and blockers

- None recorded.

## Milestone 7 — PostgreSQL, pgvector, HNSW, and IVFFlat

- **Status:** Not started
- **Estimate:** 36 hours
- **Actual:** —
- **Owner:** Yash; frontend index-status support

### Topics

- Vector-store internals and transactional CRUD
- Exact versus approximate nearest-neighbour search
- pgvector cosine, inner-product, and Euclidean operators
- HNSW graph indexing and IVFFlat cluster indexing
- Recall, latency, memory, build-time, and parameter trade-offs
- Metadata filtering, migrations, model compatibility, and re-indexing

### Implementation checklist

- [ ] Add PostgreSQL and pgvector with migrations.
- [ ] Persist sources, chunks, metadata, vectors, model, and dimensions.
- [ ] Implement transactional CRUD behind the vector-store interface.
- [ ] Implement exact cosine search and metadata filters first.
- [ ] Add HNSW and IVFFlat separately.
- [ ] Document when each index should be used.
- [ ] Support `VECTOR_BACKEND=memory|pgvector`.
- [ ] Require re-indexing after model or dimension changes.
- [ ] Test rollback, persistence across restarts, and backend parity.
- [ ] Show index status and safe re-index confirmation in the frontend.

### Verification

- [ ] Switching backends preserves application behavior.
- [ ] Stored vectors survive restarts.
- [ ] Both ANN indexes are implemented and their trade-offs are understood.

### Commit checkpoints

- `feat(backend): add pgvector storage backend`
- `feat(backend): add hnsw and ivfflat indexing`
- `feat(frontend): add vector index status`

### Definition of done

The durable vector backend is transactional, restart-safe, compatible with the in-memory interface, and supports exact, HNSW, and IVFFlat search.

### Notes and blockers

- None recorded.

## Milestone 8 — Advanced retrieval

- **Status:** Not started
- **Estimate:** 44 hours
- **Actual:** —
- **Owner:** Yash; frontend retrieval-control support

### Topics

- Similarity scores, thresholds, recall, and precision
- Maximal Marginal Relevance and relevance-diversity trade-offs
- BM25 term frequency and document frequency
- Dense versus sparse retrieval
- Hybrid search, Reciprocal Rank Fusion, weighted ensembles, and score normalization
- Retrieval-strategy selection

### Implementation checklist

- [ ] Finalize similarity retrieval and thresholds.
- [ ] Implement MMR directly.
- [ ] Implement BM25 without a retriever framework.
- [ ] Produce independent dense and sparse rankings.
- [ ] Fuse rankings with Reciprocal Rank Fusion.
- [ ] Implement a weighted ensemble retriever.
- [ ] Normalize public scores so higher always means more relevant.
- [ ] Apply source and metadata filters consistently.
- [ ] Expose similarity, MMR, hybrid, and ensemble strategies.
- [ ] Default to hybrid after it works.
- [ ] Compare conceptual, keyword-heavy, ambiguous, and repetitive questions.
- [ ] Connect frontend strategy controls.

### Verification

- [ ] All strategies use one interface and consistent score semantics.
- [ ] Ranking differences can be explained from first principles.
- [ ] Filters behave consistently across strategies.

### Commit checkpoints

- `feat(backend): add similarity thresholds and mmr`
- `feat(backend): add bm25 hybrid retrieval`
- `feat(backend): add ensemble retriever`
- `feat(frontend): connect retrieval strategy controls`

### Definition of done

All four retrieval strategies return filtered, consistently scored results through one interface, with understood ranking trade-offs.

### Notes and blockers

- None recorded.

## Milestone 9 — Embedding models and LangChain adapter

- **Status:** Not started
- **Estimate:** 20 hours
- **Actual:** —
- **Owner:** Shared

### Topics

- Hosted versus local embeddings
- Model size, speed, cost, privacy, quality, and dimensionality
- Sentence Transformers and local inference
- Provider-neutral architecture and adapter design
- LangChain embedding interface
- Re-indexing after provider changes

### Implementation checklist

- [ ] Add `sentence-transformers/all-MiniLM-L6-v2`.
- [ ] Compare hosted and local model trade-offs.
- [ ] Record model identity and dimensions.
- [ ] Rebuild vectors when the provider changes.
- [ ] Add a LangChain embedding adapter only.
- [ ] Keep retrievers, vector stores, chains, and orchestration independent.
- [ ] Expose provider and compatibility information in the frontend.
- [ ] Test provider switching and dimension mismatch handling.

### Verification

- [ ] The same indexing and retrieval pipeline works with hosted, local, and adapter-based embeddings.
- [ ] Incompatible indexes are detected and require rebuilding.

### Commit checkpoints

- `feat(backend): add local embedding provider`
- `feat(backend): add langchain embedding adapter`
- `feat(frontend): show embedding configuration`

### Definition of done

All three embedding paths work through the same provider interface with explicit model identity, dimensions, and index compatibility.

### Notes and blockers

- None recorded.

## Milestone 10 — Complete Learnly integration

- **Status:** Not started
- **Estimate:** 16 hours
- **Actual:** —
- **Owner:** Frontend with integration support from Yash

### Topics

- Independently deployed application integration
- Environment-based service URLs
- Deep linking and document-level RAG scope
- Page-level citation URLs
- End-to-end failure handling
- Production configuration, repository readiness, and operational documentation

### Implementation checklist

- [ ] Add AskLearnly navigation to Learnly.
- [ ] Add “Ask this note with AskLearnly” to document pages.
- [ ] Configure `NEXT_PUBLIC_ASKLEARNLY_URL`.
- [ ] Deep-link with `/ask?documentId=<learnly-document-id>`.
- [ ] Verify single-note and whole-library scopes.
- [ ] Verify unavailable, stale, failed, and re-indexing states.
- [ ] Document setup and environment variables.
- [ ] Run the complete acceptance flow.
- [ ] Review repository hygiene and commit history.

### Verification

- [ ] A searchable PDF can be published, synchronized, indexed, queried, and cited.
- [ ] Every citation opens the correct document page.
- [ ] Independent deployment configuration works without database coupling.

### Commit checkpoint

- `feat: link notes to asklearnly`

### Definition of done

A user can publish a searchable PDF in Learnly, synchronize it into AskLearnly, ask a scoped question, receive a streamed answer, and open every citation at the correct page.

### Notes and blockers

- None recorded.
