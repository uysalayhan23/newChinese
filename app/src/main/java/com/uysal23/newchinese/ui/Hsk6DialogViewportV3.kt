package com.uysal23.newchinese.ui

internal object Hsk6DialogViewportV3 {
    private const val ASPECT = 720f / 1280f
    const val MARKER_WIDTH_DP = 64f
    const val MARKER_MIN_HEIGHT_DP = 48f
    data class Frame(val x: Float, val y: Float, val width: Float, val height: Float)
    data class Bubble(val x: Float, val y: Float, val width: Float)
    fun fit(width: Float, height: Float): Frame {
        require(width > 0f && height > 0f)
        val imageWidth = minOf(width, height * ASPECT)
        val imageHeight = imageWidth / ASPECT
        return Frame((width-imageWidth)/2f,(height-imageHeight)/2f,imageWidth,imageHeight)
    }
    fun speakerBubble(width: Float, height: Float, speakerIsZhang: Boolean): Bubble {
        val frame = fit(width, height)
        val faceX = frame.x + frame.width * (if(speakerIsZhang) 186f else 515f) / 720f
        val mouthY = frame.y + frame.height * (if(speakerIsZhang) 600f else 605f) / 1280f
        val top = (mouthY - 26f).coerceIn(8f, maxOf(8f, height - MARKER_MIN_HEIGHT_DP - 8f))
        val widthLimit = maxOf(6f, width - MARKER_WIDTH_DP - 6f)
        val left = (if(speakerIsZhang) faceX - MARKER_WIDTH_DP - 8f else faceX + 8f)
            .coerceIn(6f,widthLimit)
        return Bubble(left,top,MARKER_WIDTH_DP)
    }
}
