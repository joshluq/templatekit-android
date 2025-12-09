# Copilot Instructions for Templatekit

## Project Overview

**Templatekit** is a Backstage template project for scaffolding **Android Libraries** using Cookiecutter. It generates new Android library projects with the **Consumer-Driven** pattern: the library artifact coupled with a showcase/demo app for immediate integration testing.

### Key Architecture
- **Two-module structure**: 
  - `library/` - The reusable Android library (the artifact)
  - `showcase/` - Internal demo app that immediately consumes the library for testing & development
- **Backstage + Cookiecutter integration**: Template parameters render both modules consistently
- **Consumer-Driven pattern**: The showcase app validates the library API during development, catching integration issues early
- **Gradle with version catalogs**: Uses custom pluginkit catalog (`es.joshluq.kit.pluginkit:catalog:0.0.1-SNAPSHOT`)

### Template Parameters
- `repo_name` - Repository name (e.g., `my-android-library`)
- `library_name` - Simple library name for artifact ID (e.g., `myandroidlibrary`)
- `package_name` - Java package for both library and showcase (e.g., `com.example.mylib`)

## Critical Workflows

### Building the Library
```bash
cd {{cookiecutter.repo_name}}
./gradlew :library:assemble  # Compile library
./gradlew :library:test      # Run JVM tests
```

### Testing Library Integration (via Showcase)
```bash
./gradlew :showcase:assembleDebug  # Build showcase consuming the library
./gradlew :showcase:connectedAndroidTest  # Instrumented tests on device
```

### Template Generation (Cookiecutter)
The `hooks/post_gen_project.py` script handles both modules:
1. Cookiecutter renders `{{ cookiecutter.package_name }}`, `{{ cookiecutter.library_name }}`, and `{{ cookiecutter.repo_name }}` in all files.
2. Post-hook moves Java files from `{src_set}/java/package_path_placeholder/` → `{src_set}/java/{package.path}/` for all source sets (**main**, **test**, **androidTest**) in both `library/` and `showcase/`.
3. For `library`: all source sets use `{{ cookiecutter.package_name }}`.
4. For `showcase`: all source sets use `{{ cookiecutter.package_name }}.showcase` so tests can target the right package namespace.
5. The generated project name (artifactId) for `:library` is derived from `{{ cookiecutter.library_name | lower | replace(' ', '-') }}`.
6. If the hook fails, code will be in the wrong location and imports will break.

## Project Structure & Patterns

### Module Layout
```
skeleton/
├── build.gradle.kts          # Root plugins (application, library, compose, testing)
├── settings.gradle.kts       # Modules: :library and :showcase
├── gradle.properties         # Gradle JVM settings, AndroidX, R class namespacing
├── {{cookiecutter.repo_name}}/  # Template root (ENTRY POINT for generated projects)
│   ├── build.gradle.kts      # Root build config
│   ├── settings.gradle.kts   # Includes library and showcase modules
│   ├── gradle.properties
│   │
│   ├── library/              # THE ARTIFACT (reusable component)
│   │   ├── build.gradle.kts  # Library plugin, not application
│   │   ├── consumer-rules.pro
│   │   └── src/main/java/package_path_placeholder/
│   │       └── MyLibraryComponent.kt
│   │
│   └── showcase/             # DEMO APP (consumer of library)
│       ├── build.gradle.kts  # Application plugin, depends on :library
│       └── src/main/java/package_path_placeholder/
│           └── MainActivity.kt
│
├── showcase/                 # Demo app in root showing template capabilities
│   ├── build.gradle.kts      # Uses :templatekit as dependency
│   ├── src/main/java/.../ui/theme/  # Compose Material3 theme
│   └── src/main/java/.../MainActivity.kt  # Compose with EdgeToEdge
├── templatekit/              # Library module in root
│   ├── build.gradle.kts      # Library configuration
```instructions
# Copilot Instructions for Templatekit (actual repo state)

Resumen rápido:

- `skeleton/` ahora es una carpeta de plantilla, no un proyecto Gradle. He eliminado los archivos wrapper/entrypoints de Gradle del `skeleton/` para evitar que se trate como un subproyecto.
- El template genera un proyecto multi-módulo con `library/` (artefacto) y `showcase/` (cliente demo).

Puntos clave para un agente AI que trabaje aquí:

- Estructura del template (contenida en `skeleton/{{cookiecutter.repo_name}}/`):
  - `library/` — artefacto reutilizable (Kotlin sources en `src/main/java/package_path_placeholder/`)
  - `showcase/` — app demo que implementa/consume la librería
  - `hooks/post_gen_project.py` — post-hook crítico que mueve `package_path_placeholder` → el paquete real (`{{ cookiecutter.package_name }}`) en **ambos** módulos

- Importante: NO ejecutes Gradle desde `skeleton/`. Para construir o probar, primero genera el proyecto (via Backstage/Cookiecutter) y luego entra en `skeleton/{{cookiecutter.repo_name}}/` (el proyecto generado sí es un proyecto Gradle).

Comandos habituales (después de generar el proyecto):
```powershell
cd skeleton\\<repo-name-generated>
.\\gradlew :library:assemble
.\\gradlew :showcase:assembleDebug
```

Archivos que deberías consultar cuando trabajes en el template:
- `skeleton/hooks/post_gen_project.py` — mueve archivos y crea la estructura de paquetes
- `skeleton/{{cookiecutter.repo_name}}/library/` — código de la librería y tests
- `skeleton/{{cookiecutter.repo_name}}/showcase/` — app demo que depende de `:library`
- `template.yaml` — configuración de Backstage (usa `fetch:cookiecutter` para esta carpeta)

Configuration note:
- The generated project contains a `project-config.properties` file at the project root. It exposes `catalogVersion` and `libraryVersion` so you can change the version catalog coordinate and the library artifact version without editing the Gradle scripts directly.

Notas sobre dependencias:
- El template usa un catalogo de plugins externo: `es.joshluq.kit.pluginkit:catalog:0.0.1-SNAPSHOT`. Asegúrate de tenerlo disponible en `mavenLocal` o en el repositorio configurado cuando construyas el proyecto generado.

Si algo no funciona al generar un proyecto, pasos de diagnóstico rápidos:
1. Verifica que Cookiecutter haya rellenado `{{ cookiecutter.package_name }}` correctamente en el proyecto generado.
2. Revisa `skeleton/hooks/post_gen_project.py` — puedes ejecutarlo manualmente desde la raíz del proyecto generado si la hook automática falló:
```powershell
cd <generated-project-root>
python hooks\\post_gen_project.py
```
3. Comprueba `settings.gradle.kts` dentro del proyecto generado (`:library` y `:showcase` deben aparecer).

Si quieres, actualizo este archivo con ejemplos adicionales o lo traduzco al español completo.
``` 
