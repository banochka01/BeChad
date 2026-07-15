package com.bechad.app
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.bechad.app.domain.*
class MainActivity: ComponentActivity(){ override fun onCreate(b:Bundle?){ super.onCreate(b); setContent{ BeChadApp() } } }
@Composable fun BeChadApp(){ MaterialTheme(colorScheme=darkColorScheme(primary=androidx.compose.ui.graphics.Color(0xFFB7F34B))){ var onboarded by remember{ mutableStateOf(false)}; var quests by remember{ mutableStateOf(emptyList<Quest>())}; if(!onboarded) OnboardingScreen{ quests=PlanGenerator.generate(it).take(4); onboarded=true } else HomeScreen(quests) } }
@Composable fun OnboardingScreen(done:(Onboarding)->Unit){ Column(Modifier.padding(24.dp), verticalArrangement=Arrangement.spacedBy(12.dp)){ Text("BeChad", style=MaterialTheme.typography.headlineLarge); Text("Choose your first RPG-style growth plan. Camera processing stays local."); Button({done(Onboarding(listOf("fitness","reading"),"15-30","normal"))}){Text("Start demo plan")}; OutlinedButton({done(Onboarding(listOf("languages","productivity"),"5-10","light"))}){Text("Light language plan")} } }
@Composable fun HomeScreen(quests:List<Quest>){ var xp by remember{ mutableIntStateOf(0)}; val level=XpRules.levelForXp(xp); Column(Modifier.padding(24.dp), verticalArrangement=Arrangement.spacedBy(12.dp)){ Text("Today in BeChad", style=MaterialTheme.typography.headlineMedium); Text("Level ${level.level} • ${level.xpIntoLevel}/${level.xpToNext} XP • streak 🔥"); LinearProgressIndicator(progress={level.xpIntoLevel.toFloat()/level.xpToNext}); quests.forEach{q-> Card{ Row(Modifier.fillMaxWidth().padding(16.dp), horizontalArrangement=Arrangement.SpaceBetween){ Column{Text(q.title); Text("${q.category} • ${q.xp} XP")}; Button({xp+=q.xp}){Text("Done")} } } }; Text("AI Coach: Complete one small main quest today to protect momentum.") } }
