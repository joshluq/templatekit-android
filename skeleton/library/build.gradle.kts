plugins {
    alias(libs.plugins.pluginkit.android.library)
    alias(libs.plugins.pluginkit.android.hilt)
    alias(libs.plugins.pluginkit.quality)
    alias(libs.plugins.pluginkit.android.testing)
}

group = "{{ cookiecutter.package_name }}"

val projectConfig = loadProjectConfig(rootProject.projectDir)
version = projectConfig.getProperty("libraryVersion", "1.0.0")

android {
    namespace = "{{ cookiecutter.package_name }}"
}

dependencies {

}
