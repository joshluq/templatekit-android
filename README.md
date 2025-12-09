# Templatekit (Android)

Templatekit is a Backstage/Cookiecutter template that scaffolds Android library projects following a Consumer-Driven pattern: the generated project contains a `library/` module (the artifact) and a `showcase/` application which immediately consumes the library for development and integration testing.

Quick start
------------
1. Generate a project (Backstage will call Cookiecutter). To test locally you can run Cookiecutter directly from the `skeleton/` folder:

```powershell
# from repo root
pip install cookiecutter           # if you don't have it
cookiecutter skeleton              # follow the prompts (repo_name, library_name, package_name)
```

2. After generation, enter the generated project and build:

```powershell
cd skeleton\<generated-repo-name>
.\gradlew :library:assemble
.\gradlew :showcase:assembleDebug
```

Notes
-----
- `skeleton/` is a template folder (not a Gradle project). The generated project inside `skeleton/<repo>` is the Gradle project.
- The post-generation hook `skeleton/hooks/post_gen_project.py` moves all source files from `package_path_placeholder/` into the actual package path structure for **main**, **test**, and **androidTest** source sets in both `library/` and `showcase/` modules.
- The template relies on an external version catalog `es.joshluq.kit.pluginkit:catalog:0.0.1-SNAPSHOT`; ensure it is available in `mavenLocal` or configured repos when building the generated project.
- The generated project needs a Gradle wrapper (`gradlew`/`gradlew.bat`) to build; you can generate it locally using `gradle wrapper` if you have Gradle installed.
 - The generated project includes a `project-config.properties` file at its root. Use it to configure:
	 - `catalogVersion` — the version coordinate used by the version catalog (defaults to `es.joshluq.kit.pluginkit:catalog:0.0.1-SNAPSHOT`).
	 - `libraryVersion` — the default version for the `:library` artifact (defaults to `1.0.0`).
	Edit `project-config.properties` in the generated project to override these values without changing build scripts.

If you want additional examples, CI templates or a sample generated repository committed to this repo, tell me and I will add them.
