package com.bechad.app.camera
import kotlin.math.*
data class Pt(val x:Double,val y:Double,val visibility:Double=1.0)
fun angle(a:Pt,b:Pt,c:Pt):Double { val abx=a.x-b.x; val aby=a.y-b.y; val cbx=c.x-b.x; val cby=c.y-b.y; val dot=abx*cbx+aby*cby; val den=hypot(abx,aby)*hypot(cbx,cby); return Math.toDegrees(acos((dot/den).coerceIn(-1.0,1.0))) }
enum class PushupPhase{UNKNOWN,UP,DOWN}; enum class SquatPhase{UNKNOWN,STANDING,DOWN}
class PushupCounter { var phase=PushupPhase.UNKNOWN; var reps=0; fun frame(elbowAngle:Double, visible:Boolean=true):Int{ if(!visible) return reps; val next= when{ elbowAngle>155 -> PushupPhase.UP; elbowAngle<95 -> PushupPhase.DOWN; else -> phase }; if(phase==PushupPhase.DOWN && next==PushupPhase.UP) reps++; phase=next; return reps } }
class SquatCounter { var phase=SquatPhase.UNKNOWN; var reps=0; fun frame(kneeAngle:Double, visible:Boolean=true):Int{ if(!visible) return reps; val next= when{ kneeAngle>160 -> SquatPhase.STANDING; kneeAngle<105 -> SquatPhase.DOWN; else -> phase }; if(phase==SquatPhase.DOWN && next==SquatPhase.STANDING) reps++; phase=next; return reps } }
