# Development of `streamlit-server-state`

## Set up
* Install `uv`
* Install dependencies
  ```shell
  $ uv sync
  ```
* Install pre-commit
  ```shell
  $ pre-commit install
  ```

## Release
1. Edit `CHANGELOG.md` and commit it.
2. Set the next version with the following command, which creates a new Git tag representing this release.
   ```
   $ bump-my-version bump <version> --tag --commit --commit-args='--allow-empty' --verbose
   ```
   NOTE: `patch`, `minor`, or `major` can be used as `<version>`.
3. Push the commit with the tag to GitHub. After pushing the tag, CI/CD automatically deploys the release.
   ```
   $ git push
   $ git push --tags
   ```
