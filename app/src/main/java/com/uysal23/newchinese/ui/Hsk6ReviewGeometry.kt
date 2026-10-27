package com.uysal23.newchinese.ui

internal object Hsk6ReviewGeometry {
    const val WIDTH = 720
    const val HEIGHT = 1280
    data class Rect(val x: Int, val y: Int, val width: Int, val height: Int)
    val zhang = Rect(6, 518, 360, 540)
    val liNa = Rect(320, 538, 390, 520)
    fun matches(assetBase: String): Boolean =
        assetBase == "hsk6/sc042" || assetBase == "hsk6/sc048"
}
