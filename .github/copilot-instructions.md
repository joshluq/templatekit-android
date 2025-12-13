# Copilot Instructions for Templatekit

## Project Overview

**Templatekit** is a Backstage Scaffolder template project for scaffolding **Android Libraries** using **Cookiecutter**. It generates new Android library projects with the **Consumer-Driven** pattern: the library artifact coupled with a showcase/demo app for immediate integration testing.

### Key Architecture
- **Two-module structure**: 
  - `library/` - The reusable Android library (the artifact)
  - `showcase/` - Internal demo app that immediately consumes the library for testing & development
- **Backstage Scaffolder with Cookiecutter**: Uses `fetch:cookiecutter` action to process templates and `publish:github` to publish
- **Consumer-Driven pattern**: The showcase app validates the library API during development, catching integration issues early
- **Gradle with version catalogs**: Uses custom pluginkit catalog (`es.joshluq.kit.pluginkit:catalog:0.0.1-SNAPSHOT`)

### Template Parameters (from `cookiecutter.json` and `catalog-info.yaml`)
- `library_name` - Simple library name for artifact ID (e.g., `MyUIKit`)
- `package_name` - Java package for both library and showcase (e.g., `com.example.mylib`)
- `description` - Library description for GitHub and Backstage
- `repoUrl` - GitHub repository URL where the project will be published

## Critical Workflows

### Building a Generated Project
```bash
cd <generated-project>
./gradlew :library:assemble  # Compile library
./gradlew :library:test      # Run JVM tests
```

### Testing Library Integration (via Showcase)
```bash
./gradlew :showcase:assembleDebug  # Build showcase consuming the library
./gradlew :showcase:connectedAndroidTest  # Instrumented tests on device
```

### Template Generation (Backstage Scaffroller with Cookiecutter)
The `catalog-info.yaml` defines the template steps using Cookiecutter:
1. `fetch:cookiecutter` — fetches the `skeleton/` directory and processes Cookiecutter placeholders
2. Template variables are passed via the `values` input:
   - `library_name` → library name
   - `package_name` → Java package (e.g., `com.example.mylib`)
   - `package_path` → package converted to path (e.g., `com/example/mylib`)
   - `repo_name` → repository name slug
   - `description` → library description
3. During fetch, all Cookiecutter variables `{{ cookiecutter.variable_name }}` are replaced with actual values
4. `{{ cookiecutter.package_path }}/` directories are processed along with other files
5. `publish:github` — publishes the generated project to GitHub

### How Template Variable Substitution Works

**In skeleton files** (Cookiecutter syntax):
- `{{ cookiecutter.package_name }}` becomes `com.example.mylib`
- `{{ cookiecutter.package_path }}` becomes `com/example/mylib`
- `{{ cookiecutter.library_name }}` becomes `MyUIKit`

**Example transformations:**
- `skeleton/library/src/main/java/{{cookiecutter.package_path}}/MyLibraryComponent.kt` → generates file with package set to actual value
- `skeleton/settings.gradle.kts` with `rootProject.name = "{{ cookiecutter.repo_name }}"` → becomes `rootProject.name = "myuikit-android"`
- Java files in `{{cookiecutter.package_path}}/` are moved to actual package paths during Cookiecutter processing
``` 
