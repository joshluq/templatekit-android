# Templatekit (Android Library Template)

Templatekit is a **Backstage Scaffolder** template using **Cookiecutter** to generate Android library projects following the **Consumer-Driven** pattern. Each generated project includes:
- **`library/`** — the reusable Android library artifact (the main deliverable).
- **`showcase/`** — an internal demo app that immediately consumes the library for development, testing, and validation.

This pattern ensures your library API is always tested in a realistic consumer context, catching integration issues early in development.

## Quick Start

1. **Register this template in your Backstage instance:**
   - Go to Backstage → Catalog → **Register existing component**.
   - Paste this repo URL (e.g., `https://github.com/joshluq/templatekit`).
   - Backstage will auto-detect `catalog-info.yaml` and register the template.

2. **In Backstage**, go to **Create** and select **"Android Library Template"**.

3. **Fill in the template parameters:**
   - **Library Name** — simple name (e.g., `MyUIKit`, `Draftkit`).
   - **Package Name** — Java package (e.g., `com.example.mylib`).
   - **Description** — brief description of the library.
   - **Repository URL** — GitHub repo where the project will be published.

4. **Run the scaffolder.** Backstage will:
   - Use Cookiecutter to process `skeleton/` and replace `{{ cookiecutter.xxx }}` placeholders.
   - Create proper Java package directories.
   - Push the generated project to GitHub.

## Building Generated Projects

Once Backstage has generated and published your project to GitHub:

```bash
cd <generated-repo-name>
./gradlew :library:assemble         # Compile the library
./gradlew :library:test             # Run unit tests
./gradlew :showcase:assembleDebug   # Build the showcase app (requires Android SDK)
./gradlew :showcase:connectedAndroidTest  # Run instrumented tests (requires device/emulator)
```

## Project Structure

**Repository root (Templatekit):**

```
skeleton/                              # Template files used by Backstage Scaffolder (fetch:cookiecutter)
├── build.gradle.kts                  # Root build config
├── settings.gradle.kts               # Multi-module settings (library + showcase)
├── gradle.properties                 # Android/Gradle settings
├── project-config.properties         # Config: catalogVersion, libraryVersion
├── gradlew / gradlew.bat             # Gradle wrapper
├── gradle/
│   └── loadProjectConfig.gradle.kts  # Shared config loader for settings + build
├── buildSrc/                         # Custom plugin/extension loader
├── library/                          # THE ARTIFACT (reusable library module)
│   ├── build.gradle.kts              
│   ├── consumer-rules.pro            # ProGuard rules for consumers
│   └── src/
│       ├── main/java/{{cookiecutter.package_path}}/
│       ├── test/java/{{cookiecutter.package_path}}/
│       └── androidTest/java/{{cookiecutter.package_path}}/
├── showcase/                         # Demo/test app consuming the library
│   ├── build.gradle.kts              
│   ├── proguard-rules.pro            # App ProGuard rules
│   └── src/
│       ├── main/java/{{cookiecutter.package_path}}/showcase/
│       ├── main/res/
│       ├── test/java/{{cookiecutter.package_path}}/showcase/
│       └── androidTest/java/{{cookiecutter.package_path}}/showcase/
├── wrapper/
│   └── gradle-wrapper.properties     # Gradle wrapper version config
└── README.md                         # Instructions for generated projects

catalog-info.yaml                      # Backstage Template entity definition (uses fetch:cookiecutter action)
cookiecutter.json                      # Cookiecutter configuration with template variables
README.md                              # This file
.github/
└── copilot-instructions.md           # Guidance for AI agents
```

**Generated project structure (via Backstage Scaffolder with Cookiecutter):**

The Scaffolder creates a new project by:
1. Using `fetch:cookiecutter` to process the `skeleton/` directory with Cookiecutter templating.
2. Replacing Cookiecutter placeholders (`{{ cookiecutter.package_name }}`, `{{ cookiecutter.library_name }}`, etc.) with actual values from the form.
3. Processing `{{ cookiecutter.package_path }}/` directories and converting them to actual package paths.
4. Using `publish:github` to push the generated project to GitHub.

2. **Register in Backstage**:
   - Option A: UI method
     - In Backstage → Catalog → Register existing component.
     - Paste repo URL: `https://github.com/joshluq/templatekit-android`
     - Backstage will auto-detect `catalog-info.yaml`.
   - Option B: Programmatic (add to `app-config.yaml`):
     ```yaml
     catalog:
       locations:
         - type: url
           target: https://github.com/joshluq/templatekit-android/blob/main/catalog-info.yaml
     ```

3. **Verify integration**:
   - In Backstage Catalog, search for "Android Library Template".
   - Click to view the template entity`):
   - Token or GitHub App with repo creation permissions.

### Registration Steps

1. **Push this repo to GitHub** (if not already):
   ```powershell
   git add -A
   git commit -m "Initial commit: Android library template"
   git push origin HEAD
   ```

2. **Register in Backstage**:
   - Option A: UI method
     - In Backstage → Catalog → Register existing component.
     - Paste repo URL: `https://github.com/<org>/templatekit`
     - Backstage will auto-detect `catalog-info.yaml`.
   - Option B: Programmatic (add to `app-config.yaml`):
     ```yaml
     catalog:
       locations:
         - type: url
           target: https://github.com/<org>/templatekit/blob/main/catalog-info.yaml
     ```

3. **Verify integration**:
   - In Backstage Catalog, search for "Android Library Template".
   - Go to Templates and click "Create" to test the scaffolder flow.

### GitHub Integration in app-config.yaml

**Using a token (simple):**
```yaml
integrations:
  github:
    - host: github.com
      token: ${GITHUB_TOKEN}
```

**Using GitHub App (recommended):**
```yaml
integrations:
  github:
    - host: github.com
      apps:
        - appId: ${GITHUB_APP_ID}
          privateKey: |-
            -----BEGIN RSA PRIVATE KEY-----
            ...
            -----END RSA PRIVATE KEY-----
          installationId: ${GITHUB_INSTALLATION_ID}
```

Ensure your GitHub token/app has permissions to create repositories.

## Generated Project Features

Each generated project includes:

### Multi-module Gradle structure
- `:library` module (artifact to publish).
- `:showcase` module (demo app consuming the library).
- Shared configuration via `gradle/loadProjectConfig.gradle.kts`.

### Automatic package structure (via Scaffolder)
- Scaffolder's `fs:write` actions create proper Java package directories.
- Separate source files for `main`, `test`, and `androidTest` source sets in both modules.

### Configuration management
- **`project-config.properties`** allows overriding:
  - `catalogVersion` — external version catalog coordinate (default: `es.joshluq.kit.pluginkit:catalog:0.0.1-SNAPSHOT`).
  - `libraryVersion` — library artifact version (default: `1.0.0`).

### Gradle wrapper included
- `gradlew` (Linux/macOS) and `gradlew.bat` (Windows) are included.
- Projects build immediately without manual wrapper generation.

### Consumer-Driven Development
- The showcase app validates library API at development time.
- Tests in `library/src/androidTest/java/` can run against a real app context.
- Use the showcase to develop and test features before committing to the library.

## Development Workflow (in generated projects)

1. **Add library code** to `library/src/main/java/<package>/`.
2. **Write unit tests** in `library/src/test/java/<package>/`.
3. **Write instrumented tests** in `library/src/androidTest/java/<package>/`.
4. **Integrate in showcase** at `showcase/src/main/java/<package>/showcase/` to validate API and UX.
5. **Add showcase tests** in `showcase/src/test/java/<package>/showcase/` or `showcase/src/androidTest/...`.
6. **Build and test**:
   ```powershell
   .\gradlew :library:assemble :library:test
   .\gradlew :showcase:assembleDebug :showcase:connectedAndroidTest
   ```

## Notes & Troubleshooting

### Template Variables (defined in `catalog-info.yaml` and `cookiecutter.json`)
These are passed to Cookiecutter templating during `fetch:cookiecutter`:
- `{{ cookiecutter.library_name }}` — simple library name (used for artifact ID and GitHub repo).
- `{{ cookiecutter.package_name }}` — Java package for library and showcase base (e.g., `com.example.mylib`).
- `{{ cookiecutter.package_path }}` — package converted to directory path (e.g., `com/example/mylib`).
- `{{ cookiecutter.showcase_package }}` — showcase package (`{{ cookiecutter.package_name }}.showcase`).
- `{{ cookiecutter.showcase_package_path }}` — showcase package as path.
- `{{ cookiecutter.description }}` — library description (for GitHub and Backstage).
- `{{ cookiecutter.repoUrl }}` — GitHub repository URL where the project will be published.

### Common Issues

**"fetch:plain failed" or "fs:write failed"**
- Ensure the GitHub repo URL is accessible and points to the correct branch.
- Check that Backstage Scaffolder has network access.

**"publish:github failed to create repo"**
- Ensure GitHub token has `repo` scope or GitHub App has installation permissions.
- Token must have org-level permissions if publishing to an organization.
- Check that the `repoUrl` parameter matches GitHub org/owner expectations.

**Gradle build fails in generated project**
- Ensure Android SDK is installed on the build machine.
- Check that the external catalog `es.joshluq.kit.pluginkit:catalog:0.0.1-SNAPSHOT` is available in `mavenLocal()` or configured repositories.
- If using a custom catalog, update `project-config.properties` in the generated project.

**"fetch:cookiecutter failed"**
- Ensure Cookiecutter is installed and the skeleton directory is accessible.
- Check that all Cookiecutter variables in `cookiecutter.json` match placeholders in skeleton files.
- Verify Cookiecutter syntax is correct: use `{{ cookiecutter.variable_name }}` format.

## Additional Resources

- **Copilot Instructions** — [.github/copilot-instructions.md](.github/copilot-instructions.md) — guidance for AI agents.
- **Backstage Docs** — [Scaffolder](https://backstage.io/docs/features/software-templates/overview), [Scaffolder Built-in Actions](https://backstage.io/docs/features/software-templates/builtin-actions).
- **Android Gradle** — [Android Build System](https://developer.android.com/build).

## Contributing

Found an issue or want to improve the template? Feel free to:
1. Open an issue or PR in this repository.
2. Update `skeleton/` files to refine the template.
3. Update `catalog-info.yaml` if adding new template parameters or steps.
4. Test your changes by registering the template in a local Backstage instance before committing.
