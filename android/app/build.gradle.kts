plugins { alias(libs.plugins.android.application); alias(libs.plugins.kotlin.android); alias(libs.plugins.kotlin.serialization) }

android { namespace="com.bechad.app"; compileSdk=35
 defaultConfig { applicationId="com.bechad.app"; minSdk=28; targetSdk=35; versionCode=1; versionName="0.1.0"; testInstrumentationRunner="androidx.test.runner.AndroidJUnitRunner" }
 buildTypes { release { isMinifyEnabled=false } }
 compileOptions { sourceCompatibility=JavaVersion.VERSION_17; targetCompatibility=JavaVersion.VERSION_17 }
 kotlinOptions { jvmTarget="17" }
 buildFeatures { compose=true }
}
dependencies { implementation(libs.androidx.core); implementation(libs.activity.compose); implementation(platform(libs.compose.bom)); implementation(libs.compose.ui); implementation(libs.compose.material3); implementation(libs.compose.tooling); implementation(libs.navigation.compose); implementation(libs.lifecycle.viewmodel); implementation(libs.coroutines); implementation(libs.serialization.json); testImplementation(libs.junit) }
