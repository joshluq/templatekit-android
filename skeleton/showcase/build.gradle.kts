plugins {
    alias(libs.plugins.pluginkit.android.application)
    alias(libs.plugins.pluginkit.android.compose)
    alias(libs.plugins.pluginkit.android.testing)
}

android {
    namespace = "{{ cookiecutter.package_name }}.showcase"

    defaultConfig {
        applicationId = "{{ cookiecutter.package_name }}.showcase"
        versionCode = 1
        versionName = "1.0"
    }
}

dependencies {
    implementation(project(":{{ cookiecutter.library_name | lower | replace(' ', '-') }}"))
}
