package com.bechad.app
import com.bechad.app.domain.*
import com.bechad.app.camera.*
import org.junit.Assert.*
import org.junit.Test
class RulesTest { @Test fun levels(){ assertEquals(2, XpRules.levelForXp(100).level) }
 @Test fun plan(){ assertEquals(14, PlanGenerator.generate(Onboarding(listOf("fitness","reading"),"15-30","normal")).size) }
 @Test fun streak(){ assertTrue(StreakRules.counts(1,100,60)); assertFalse(StreakRules.counts(0,100,100)) }
 @Test fun pushups(){ val c=PushupCounter(); listOf(170.0,80.0,170.0).forEach{c.frame(it)}; assertEquals(1,c.reps) }
 @Test fun squats(){ val c=SquatCounter(); listOf(175.0,90.0,175.0).forEach{c.frame(it)}; assertEquals(1,c.reps) } }
