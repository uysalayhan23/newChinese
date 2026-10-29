package com.uysal23.newchinese.ui

import android.os.Bundle
import com.uysal23.newchinese.data.ContentRepository
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.material3.MaterialTheme
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

/** Debug-build-only Android runtime probe. NEVER merge into release main. */
class Hsk6ReviewProbeActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val n = intent.getStringExtra("scene")?.takeIf { it == "042" || it == "048" } ?: "042"
        val speaker = if (intent.getStringExtra("speaker") == "li") "CHAR_LI_NA_001" else "CHAR_ZHANG_WEI_001"
        val expanded = intent.getBooleanExtra("expanded", false)
        val screen = intent.getStringExtra("screen").orEmpty()
        // Exercise the actual content parser and screens, not only the visual-layer probe.
        val content = if (screen == "intro" || screen == "dialogue") {
            ContentRepository(applicationContext).loadSceneById("HSK6_SC$n")
        } else null
        setContent {
            MaterialTheme {
                when (screen) {
                    "intro" -> SceneIntroScreen(
                        scene = requireNotNull(content),
                        onStartDialogue = {}, onStudy = {}, onBack = {}
                    )
                    "dialogue" -> DialogueScreen(
                        scene = requireNotNull(content),
                        showPinyinDefault = false, showTurkishDefault = false,
                        playbackSpeed = 1f, initialLineIndex = 0,
                        onPositionChanged = { _, _ -> }, onStudy = {}, onBack = {}
                    )
                    else -> Box(Modifier.fillMaxSize()) {
                        AssetSceneStage(
                        sceneAssetBase = "hsk6/sc$n",
                        background = "assets/hsk6_sc${n}_bg.webp",
                        characterA = "assets/hsk6_sc${n}_char_zhang_wei.webp",
                        characterB = "assets/hsk6_sc${n}_char_li_na.webp",
                        foreground = "assets/hsk6_sc${n}_fg.webp",
                        preview = "assets/hsk6_sc${n}_preview.webp",
                        activeSpeakerId = speaker,
                        speechText = "你好",
                        characterAId = "CHAR_ZHANG_WEI_001",
                        characterBId = "CHAR_LI_NA_001",
                        modifier = if (expanded) Modifier.fillMaxSize() else Modifier.fillMaxWidth().height(245.dp)
                    )
                    }
                }
            }
        }
    }
}
