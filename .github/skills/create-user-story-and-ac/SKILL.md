---
name: create-user-story-and-ac
description: 'Use when the user asks to review a GitHub Projects Ready column and add missing User Story and Acceptance Criteria sections to its work items. Derive the content from each item title, preserve existing descriptions, and format Acceptance Criteria as a Markdown checklist.'
---

# Create User Story and AC

Review the specified GitHub Projects board and enrich only the work items in its
`Ready` status. For each item, inspect its current description before editing:

- Add a `## User Story` section only when one is missing or empty.
- Add a `## Acceptance Criteria` section only when one is missing or empty.
- Use the item title as the primary source for both sections.
- Format every acceptance criterion as an unchecked Markdown checklist item:
  `- [ ] ...`.
- Preserve all existing description text and existing non-empty sections.
- Do not modify items in other statuses.
- Do not change titles, labels, assignees, priorities, or other project fields.

## Workflow

1. Identify the target project from the user's URL, project owner, and project
   number. If the user does not provide a target, use the current repository's
   project only when it is unambiguous.
2. Read the project's fields and items through GitHub's GraphQL API. Resolve
   the `Status` single-select field and select items whose value is exactly
   `Ready`.
3. Read each Ready item's content and description. Support GitHub Issues,
   Pull Requests, and Draft Issues when the project API returns them.
4. For each item, determine whether `User Story` and `Acceptance Criteria`
   headings already contain meaningful content. Treat a heading followed only
   by whitespace, HTML comments, or empty checklist markers as missing.
5. Draft concise, title-specific text:

   ```markdown
   ## User Story
   身為<角色>，我希望<根據 title 推導的能力>，以便<使用者價值>。

   ## Acceptance Criteria
   - [ ] <主要成功情境可被驗證>
   - [ ] <輸入、計算或處理結果符合 title 的需求>
   - [ ] <結果會清楚呈現給使用者>
   - [ ] <無效或缺漏輸入會被提示並妥善處理>
   ```

   Infer the role, capability, value, and criteria from the title; do not
   invent unrelated product scope. Add or remove checklist items as needed to
   make the criteria specific and testable. Keep the criteria in the language
   used by the title or the user's request.
6. Merge the generated sections into the existing description:
   - If both sections are missing, append both with a blank line between them.
   - If one section exists and is non-empty, leave it unchanged and add only
     the missing section.
   - If a section heading exists but is empty, replace only that section's
     empty content.
7. Update the underlying GitHub content using the least-privileged API:
   - Issues: `gh api repos/OWNER/REPO/issues/NUMBER -X PATCH -f body=...`
   - Pull Requests: `gh api repos/OWNER/REPO/pulls/NUMBER -X PATCH -f body=...`
   - Draft Issues: use the GitHub GraphQL mutation for updating the draft issue
     body, preserving the returned draft issue ID.
8. Re-read every modified item and verify that the intended sections exist,
   Acceptance Criteria use `- [ ]`, and the title and unrelated body content
   are unchanged.
9. Report the modified items with links and clearly state when an item was
   skipped because it already had both sections.

## API query guidance

Use an inline fragment for `ProjectV2FieldCommon` when reading field names,
because project field configurations are unions. A query shape for the
relevant values is:

```graphql
fieldValues(first: 100) {
  nodes {
    __typename
    ... on ProjectV2ItemFieldSingleSelectValue {
      name
      field { ... on ProjectV2FieldCommon { name } }
    }
  }
}
```

Request only the fields needed to identify Ready items and update their
descriptions. Never update an item solely because it is in the project; the
exact `Ready` status and missing-section checks are required.

## Quality and safety rules

- Never overwrite a non-empty User Story or Acceptance Criteria section.
- Never replace the entire body with generated text when existing content is
  present; merge surgically.
- Keep Acceptance Criteria observable and testable, not vague goals.
- Make no assumptions about implementation details that are not in the title
  or existing description.
- If the content type cannot be updated, skip it and report the reason instead
  of silently failing.
- If the project, status field, item content, or API response is ambiguous,
  stop and ask the user rather than updating the wrong work items.
