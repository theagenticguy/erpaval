# Research methods — picking the right tool per question type

Companion to `${CLAUDE_PLUGIN_ROOT}/skills/product-design-shared/references/research-design.md`. The shared reference covers the *method* (hypothesis → null → MECE questions → findings). This file covers the *techniques* you pick for each question.

## Method taxonomy

The research-design method requires you to pick a method per MECE sub-question. Questions have shapes; methods have shapes; match them.

| Question type          | What it asks                                              | Best methods                                                                      | Wrong fit                                             |
| ---------------------- | --------------------------------------------------------- | --------------------------------------------------------------------------------- | ----------------------------------------------------- |
| **Behavioral**         | What are customers doing?                                 | Funnel analytics, session replay, A/B test, event logs                            | Interviews (self-report is unreliable for behavior)   |
| **Attitudinal**        | Why are they doing it? What do they feel?                 | 1:1 interviews, open-ended surveys, support-ticket thematic coding, diary studies | Analytics alone (can't explain *why*)                 |
| **Pain-point texture** | How does the friction feel? Emotional weight?             | Ethnography, Gemba walks, empathy mapping, diary studies                          | Closed-ended surveys (flatten the texture)            |
| **Segmentation**       | Who is affected? How does behavior differ across cohorts? | Cohort analysis, persona-based research, stratified surveys                       | Interviews alone (sample too small for cohort claims) |
| **Scale**              | How common is this problem?                               | Quantitative survey (large-N), site-wide analytics, industry benchmarks           | Interviews (can show pattern but not scale)           |
| **Causal**             | Does changing X move Y?                                   | A/B test, quasi-experiment with controls, before/after with counterfactual        | Correlation from analytics (confounds; never enough)  |

**Rule of thumb**: mix at least two methods across the plan. Interviews alone produce beautiful stories that don't scale; analytics alone miss the human texture that explains the numbers.

## 1:1 interview protocol

### Recruit

- 5–8 participants per customer segment for saturation on attitudinal questions (stop earlier if you hit saturation; extend if new themes still emerge at 8).
- Screen for the segment defined in Q1 of the 5CQ. Do not interview "whoever is available."
- Compensate per your organization's user-research standards.

### Before the interview

- Pre-commit the hypothesis + null in writing (`templates/research-plan.md`).
- Write 5–8 open-ended questions. No leading questions ("Don't you agree that…?"). No multiple-choice in live interviews (save those for surveys).
- Pilot with 1 colleague; refine.

### During the interview

- Start broad ("Walk me through the last time you…"); narrow to specifics as themes emerge.
- Follow-up with "Tell me more about…" and "What did you do next?" rather than interpretation.
- Capture verbatim quotes — do not paraphrase. Record (with consent) or take typed notes.
- Save the hypothesis test to the end; ask about the current experience before describing the proposed solution.

### After the interview

- Write a 1-paragraph synthesis within 24 hours while fresh.
- Tag quotes by sub-question.
- Do not synthesize across interviews until all are complete — keeps confirmation bias out.

## Affinity clustering (synthesis across interviews)

For 5+ interviews, use affinity clustering to surface themes without imposing your hypothesis:

1. Pull every quote into its own sticky note / card. Do not yet label them.
2. Have 2-3 team members silently cluster similar quotes.
3. Name the clusters *after* they form (do not predetermine cluster names).
4. Count quotes per cluster — cluster size tells you prevalence.
5. Map clusters back to MECE sub-questions. Clusters that don't map are either (a) outside scope, or (b) a signal your sub-questions missed something.

## Survey design

For attitudinal + scale questions at N > 30:

- **Keep it short** — 5-10 questions. Longer surveys drop completion rates.
- **Mix closed + open** — closed questions for quantification, 2-3 open questions for texture.
- **No leading questions.** "How frustrating is X?" presupposes frustration; ask "How would you describe X?" instead.
- **Pre-test with 5 people** — half will misinterpret at least one question. Fix those.
- **Pre-commit the analysis plan** — what cuts will you make? Which subgroups? If you don't pre-commit, every cut becomes a fishing expedition.

## Support-ticket thematic coding

Most teams have rich support-ticket history. To use it:

1. Sample 50-100 tickets from the segment + time window of interest.
2. Define 5-10 thematic codes *a priori* from the research plan. Allow an "other" code.
3. Two coders apply codes independently. Measure inter-rater agreement (target >80%).
4. Resolve disagreements; refine codes if needed.
5. Tally frequencies per code. Pull representative quotes per theme.

Scales well; good for behavioral + attitudinal at modest cost. Weaker on questions the customer didn't think to complain about.

## Gemba walk

The Lean practice of re-experiencing the customer flow yourself. Protocol:

1. Pick a primary customer segment + a realistic scenario.
2. Execute the scenario end-to-end as a real customer would. No cheating — no internal bookmarks, no employee accounts, no "I know where to click."
3. Capture every friction: confusion, delay, dead end, missing affordance.
4. Screenshot or record.
5. Debrief within 1 hour. Rank frictions by emotional weight, not by time lost.

Cheap, fast, high signal for pain-point texture. Does not scale — you are one person. Complement with attitudinal data.

## Qualitative / Quantitative / Subjective metrics taxonomy

A useful three-way decomposition for choosing what to measure:

| Type            | What it is                                                                     | Example                                              |
| --------------- | ------------------------------------------------------------------------------ | ---------------------------------------------------- |
| **Behavioral**  | Quantitative measures of what customers do, at scale or via direct observation | Funnel drop-off at step 3 = 42%                      |
| **Qualitative** | Verbal feedback + observations of how and why                                  | "I didn't understand what 'plain white' meant" — P04 |
| **Subjective**  | Quantitative measures of the subjective experience using standardized scales   | SUS usability score = 68 (below average)             |

A good research plan uses all three. Each answers a different kind of question.

## Common VoC resource categories

This skill is methodology-first. Plug in whatever VoC resources your team has — common categories:

| Resource type             | Strongest for                                 |
| ------------------------- | --------------------------------------------- |
| Live-call listening       | Hearing real customer calls in context        |
| Feedback aggregation      | Search + visualize all customer feedback data |
| User research community   | Methods, studies, prior research              |
| Accessibility recruitment | Studies with accessibility-focused panels     |
| Diary-study platforms     | Mobile research, longitudinal observation     |
| Usability-test platforms  | Recruited testing at scale                    |
| Gemba / floor walks       | Direct observation of work in context         |
| Empathy mapping           | Collaborative empathy synthesis               |
| Past-research repository  | Re-using prior studies                        |
| Inclusive UX research     | Inclusive + accessible experience design      |
| Market research           | Market analytics + business drivers           |

## Persona development

Personas are distilled essences of real users — **built from observations of real users, not invented from assumptions**.

Beware of stereotypes. Specificity matters. A good persona:

- Names a real behavior pattern observed in research.
- Cites supporting evidence (count + source).
- Describes context, not demographics.
- States a primary job-to-be-done.
- Identifies a key pain point.

Bad persona: "Tech-savvy millennial female who loves shopping." (Stereotype. Demographic. No JTBD.)

Good persona: "Casual seller who lists 1–2 items per month, usually evenings after kids' bedtime, from mobile. JTBD: 'Get this listed fast so I can go to bed.' Pain: image-requirements step blocks completion; seller abandons 35% of the time per funnel data."

## Jobs-to-be-done (JTBD) framing

An alternative to persona-first framing. A JTBD states:

```text
When [situation], I want to [motivation], so I can [outcome].
```

Example: "When I receive a gift I need to return, I want to start the return on my phone without finding the original order, so I can dispose of the package quickly and move on with my day."

JTBD focuses on the task and outcome, not the person. Often pairs well with behavioral research and journey mapping.

## Evidence inventory handoff shape

After synthesis, produce a table that maps cleanly into Pyramid Phase 1:

| Sub-question                  | Finding (1 sentence)                                      | Evidence (sources)             | So what (1 sentence)                       | Confidence       |
| ----------------------------- | --------------------------------------------------------- | ------------------------------ | ------------------------------------------ | ---------------- |
| Q1: Where do sellers abandon? | 42% drop at the image-requirements step                   | Funnel analytics, Jan 1–Mar 31 | Image step is the dominant failure point   | High             |
| Q2: What do sellers say?      | 7 of 12 interviewed reported ambiguity about requirements | Interviews P01-P12, 9-Apr      | Ambiguity is verbalized, not just inferred | Medium (small N) |
| ...                           | ...                                                       | ...                            | ...                                        | ...              |

Each row is a Pyramid-base evidence item. Rows that cluster on a shared "so what" feed the same Pyramid-middle argument.
