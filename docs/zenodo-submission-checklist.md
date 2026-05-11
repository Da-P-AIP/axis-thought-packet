# Zenodo Submission Checklist

## Before GitHub Release

- [ ] Decide the public title.
- [ ] Decide the public author/creator name.
- [ ] Decide the license.
- [ ] Add the final manuscript PDF or public research artifact.
- [ ] Update `README.md`.
- [ ] Update `CITATION.cff`.
- [ ] Update `.zenodo.json`.
- [ ] Confirm there are no private notes, tokens, emails, account IDs, or raw ChatGPT exports.
- [ ] Create a GitHub release tag, for example `v0.1.0`.

## Zenodo Route

For a GitHub-centered artifact:

1. Enable the repository in Zenodo's GitHub integration.
2. Create a GitHub release.
3. Wait for Zenodo to archive the release.
4. Copy the minted DOI into `README.md` and `CITATION.cff`.

For a paper-first deposit:

1. Create a manual Zenodo upload.
2. Select the appropriate resource type, such as publication, preprint, or technical note.
3. Reserve a DOI if the DOI needs to appear inside the PDF before publication.
4. Upload the PDF and source files.
5. Publish the record.

