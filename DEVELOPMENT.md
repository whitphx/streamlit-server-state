# Development of `streamlit-server-state`

## Release
1. Edit `CHANGELOG.md` and commit it.
2. Set the next version with the following command, which creates a new Git tag representing this release.
   ```
   $ bump-my-version bump <version> --tag
   ```
   If you want to add a commit, add `--commit --commit-args='--allow-empty'` options. This project doesn't have any files to be changed for bumping the version, so the commit is empty.
   ```
   $ bump-my-version bump <version> --tag --commit --commit-args='--allow-empty'
   ```
   NOTE: `patch`, `minor`, or `major` can be used as `<version>`.
3. Push the commit with the tag to GitHub. After pushing the tag, CI/CD automatically deploys the release.
   ```
   $ git push
   $ git push --tags
   ```
