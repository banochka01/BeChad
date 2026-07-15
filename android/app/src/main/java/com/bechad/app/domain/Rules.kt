package com.bechad.app.domain
import kotlin.math.max

data class Quest(val title:String,val category:String,val difficulty:String,val xp:Int,val main:Boolean=true)
data class Onboarding(val goals:List<String>, val timeBudget:String, val intensity:String)
data class Level(val level:Int,val xpIntoLevel:Int,val xpToNext:Int)
object XpRules { fun levelForXp(total:Int):Level{ var xp=total; var lvl=1; var need=100; while(xp>=need){xp-=need; lvl++; need=(need*1.25).toInt()+50}; return Level(lvl,xp,need) } }
object PlanGenerator { fun generate(o:Onboarding, completed:Int=0, skips:Int=0):List<Quest>{ val base=when(o.intensity){"light"->10;"intense"->35;else->20}; val safe=max(5, base + completed*2 - skips*3); val map=mapOf("fitness" to listOf("10 pushups","20 squats","Plank 30 seconds"),"languages" to listOf("Practice language 10 minutes","Complete one language lesson"),"reading" to listOf("Read 5 pages"),"productivity" to listOf("15 minutes focused work"),"sleep" to listOf("Prepare for bed on time"),"custom" to listOf("Complete custom habit")); return (0 until 7).flatMap{d->(o.goals.ifEmpty{listOf("fitness")}).mapIndexed{i,g-> Quest(map[g]?.get((d+i)%(map[g]?.size?:1))?:"Complete custom habit",g,o.intensity, safe + minOf(d*2,10), i<3)}} } }
object StreakRules { fun counts(mainDone:Int, plannedXp:Int, earnedXp:Int)= mainDone>0 && earnedXp*100 >= plannedXp*60 }
