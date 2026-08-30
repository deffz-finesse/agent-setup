# Step 1: Validate Prerequisites and Extract Requirements

## STEP GOAL

To validate that the available rough planning inputs exist and extract the requirements needed for a coarse capability roadmap.

## MANDATORY EXECUTION RULES (READ FIRST)

### Universal Rules

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator

### Role Reinforcement

- ✅ You are a product strategist and technical specifications writer
- ✅ If you already have been given communication or persona patterns, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring requirements extraction expertise
- ✅ User brings their product vision and context

### Step-Specific Rules

- 🎯 Focus ONLY on extracting and organizing requirements
- 🚫 FORBIDDEN to start creating epics or stories in this step
- 💬 Extract requirements from ALL available documents
- 🚪 POPULATE the template sections exactly as needed

## EXECUTION PROTOCOLS

- 🎯 Extract requirements systematically from all documents
- 💾 Populate `{epics_output_path}/requirements-inventory.md` with extracted requirements and update `{epics_output_path}/index.md` with its link.
- 📖 Update frontmatter with extraction progress
- 🚫 FORBIDDEN to load next step until user selects 'C' and requirements are extracted

## REQUIREMENTS EXTRACTION PROCESS

### 1. Welcome and Overview

Welcome the user to comprehensive epic and story creation!

**CRITICAL PREREQUISITE VALIDATION:**

Verify required documents exist and are complete:

1. **PRD.md** - Contains requirements (FRs and NFRs) and product scope
2. **Architecture.md** - Contains technical decisions, API contracts, data models
3. **UX design contract** (if UI exists) - Contains visual identity, interaction patterns, mockups, and user flows

### 2. Document Discovery and Validation

Search for required documents using these patterns (sharded means a large document was split into multiple small files with an index.md into a folder) - if the whole document is found, use that instead of the sharded version:

**PRD Document Search Priority:**

1. `{run_dir}/02-plan/prd.md` (run-owned document)
2. `{run_dir}/02-plan/prd/index.md` (run-owned sharded version)

**Architecture Document Search Priority:**

1. `{run_dir}/02-plan/architecture/ARCHITECTURE-SPINE.md` (run-owned spine)
2. `{run_dir}/02-plan/architecture/index.md` (run-owned rendering)

**UX Design Document Search (Optional):**

1. `{run_dir}/02-plan/ux/DESIGN.md` and `{run_dir}/02-plan/ux/EXPERIENCE.md` (run-owned UX spine pair)

For each matching ux run folder, treat `DESIGN.md` and `EXPERIENCE.md` as one UX design contract:

- Confirm and load both files together. `DESIGN.md` owns visual identity and design tokens; `EXPERIENCE.md` owns information architecture, behavior, states, interactions, accessibility, and journeys.
- Add both files to the `inputDocuments: []` frontmatter array.
- If only one spine exists, report the incomplete pair and ask whether the user wants to include the partial UX handoff.
- If multiple run folders match, show each run folder with the spine frontmatter `status` and `updated` values when available, then ask the user which UX design contract to include.

Before proceeding, Ask the user if there are any other documents to include for analysis, and if anything found should be excluded. Wait for user confirmation. Once confirmed, initialize `{epics_output_path}/.memlog.md`, create `{epics_output_path}/requirements-inventory.md` from the extracted requirements, and create `{epics_output_path}/index.md` from the template with the files in `inputDocuments: []`.

### 3. Extract Functional Requirements (FRs)

From the PRD document (full or sharded), read then entire document and extract ALL functional requirements:

**Extraction Method:**

- Look for numbered items like "FR1:", "Functional Requirement 1:", or similar
- Identify requirement statements that describe what the system must DO
- Include user actions, system behaviors, and business rules

**Format the FR list as:**

```
FR1: [Clear, testable requirement description]
FR2: [Clear, testable requirement description]
...
```

### 4. Extract Non-Functional Requirements (NFRs)

From the PRD document, extract ALL non-functional requirements:

**Extraction Method:**

- Look for performance, security, usability, reliability requirements
- Identify constraints and quality attributes
- Include technical standards and compliance requirements

**Format the NFR list as:**

```
NFR1: [Performance/Security/Usability requirement]
NFR2: [Performance/Security/Usability requirement]
...
```

### 5. Extract Additional Requirements from Architecture

Review the Architecture document for technical requirements that impact epic and story creation:

**Look for:**

- **Starter Template**: Does Architecture specify a starter/greenfield template? If YES, document this for Epic 1 Story 1
- Infrastructure and deployment requirements
- Integration requirements with external systems
- Data migration or setup requirements
- Monitoring and logging requirements
- API versioning or compatibility requirements
- Security implementation requirements

**IMPORTANT**: If a starter template is mentioned in Architecture, note it prominently. This will impact Epic 1 Story 1.

**Format Additional Requirements as:**

```
- [Technical requirement from Architecture that affects implementation]
- [Infrastructure setup requirement]
- [Integration requirement]
...
```

### 6. Extract UX Design Requirements (if UX document exists)

**IMPORTANT**: The UX Design Specification is a first-class input document, not supplementary material. Requirements from the UX spec must be extracted with the same rigor as PRD functional requirements.

Read the FULL UX design contract and extract ALL actionable work items. For a ux spine pair, read both `DESIGN.md` and `EXPERIENCE.md`:

**Look for:**

- **Design token work**: Color systems, spacing scales, typography tokens that need implementation or consolidation
- **Component proposals**: Reusable UI components identified in the UX spec (e.g., ConfirmActions, StatusMessage, EmptyState, FocusIndicator)
- **Visual standardization**: Semantic CSS classes, consistent color palette usage, design pattern consolidation
- **Accessibility requirements**: Contrast audit fixes, ARIA patterns, keyboard navigation, screen reader support
- **Responsive design requirements**: Breakpoints, layout adaptations, mobile-specific interactions
- **Interaction patterns**: Animations, transitions, loading states, error handling UX
- **Browser/device compatibility**: Target platforms, progressive enhancement requirements

**Format UX Design Requirements as a SEPARATE section (not merged into Additional Requirements):**

```
UX-DR1: [Actionable UX design requirement with clear implementation scope]
UX-DR2: [Actionable UX design requirement with clear implementation scope]
...
```

Preserve important UX constraints without converting the entire UX contract into a frozen project-wide story inventory. Sprint planning adds testable acceptance criteria only for the next selected slices.

### 7. Load and Initialize Templates

Load `../templates/epics-template.md` and `../templates/requirements-inventory-template.md`:

1. Copy `epics-template.md` to `{epics_output_path}/index.md`.
2. Copy `requirements-inventory-template.md` to `{epics_output_path}/requirements-inventory.md`.
3. Replace `{{project_title}}` in both files with the mechanically resolved project title.
4. Replace the requirements-inventory placeholders:
   - {{fr_list}} → extracted FRs
   - {{nfr_list}} → extracted NFRs
   - {{additional_requirements}} → extracted additional requirements (from Architecture)
   - {{ux_design_requirements}} → extracted UX Design Requirements (if UX document exists)
5. Leave `{{requirements_coverage_map}}` in the inventory and `{{epics_list}}` in the index for Step 2. Epic content is written to one `epic-<NN>-<slug>.md` shard per epic.

### 8. Present Extracted Requirements

Display to user:

**Functional Requirements Extracted:**

- Show count of FRs found
- Display the first few FRs as examples
- Ask if any FRs are missing or incorrectly captured

**Non-Functional Requirements Extracted:**

- Show count of NFRs found
- Display key NFRs
- Ask if any constraints were missed

**Additional Requirements (Architecture):**

- Summarize technical requirements from Architecture
- Verify completeness

**UX Design Requirements (if applicable):**

- Show count of UX-DRs found
- Display key UX Design requirements (design tokens, components, accessibility)
- Verify each UX-DR is specific enough for story creation

### 9. Get User Confirmation

Ask: "Do these extracted requirements accurately represent what needs to be built? Any additions or corrections?"

Update the requirements based on user feedback until confirmation is received.

## CONTENT TO SAVE TO DOCUMENT

After extraction and confirmation, update `{epics_output_path}/requirements-inventory.md` with:

- Complete FR list in {{fr_list}} section
- Complete NFR list in {{nfr_list}} section
- All additional requirements in {{additional_requirements}} section
- UX Design requirements in {{ux_design_requirements}} section (if UX document exists)

### 10. Present MENU OPTIONS

Display: `**Confirm the Requirements are complete and correct to [C] continue:**`

#### EXECUTION RULES

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- User can chat or ask questions - always respond and then end with display again of the menu option

#### Menu Handling Logic

- IF C: Save all to `{epics_output_path}/requirements-inventory.md` and `{epics_output_path}/index.md`, update frontmatter, then read fully and follow: ./step-02-design-epics.md
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#10-present-menu-options)

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN C is selected and all requirements are saved to document and frontmatter is updated, will you then read fully and follow: ./step-02-design-epics.md to begin epic design step.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS

- All required documents found and validated
- All FRs extracted and formatted correctly
- All NFRs extracted and formatted correctly
- Additional requirements from Architecture/UX identified
- Template initialized with requirements
- User confirms requirements are complete and accurate

### ❌ SYSTEM FAILURE

- Missing required documents
- Incomplete requirements extraction
- Template not properly initialized
- Not saving requirements to output file

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
