package com.travelhub.app.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val LightColorScheme = lightColorScheme(
    primary = Color(0xFF006874),
    onPrimary = Color.White,
    secondary = Color(0xFF4A6267),
    onSecondary = Color.White,
    background = Color(0xFFFBFCFC),
    surface = Color(0xFFFBFCFC),
)

private val DarkColorScheme = darkColorScheme(
    primary = Color(0xFF4FD8EB),
    onPrimary = Color(0xFF00363D),
    secondary = Color(0xFFB1CBD0),
    onSecondary = Color(0xFF1C3438),
    background = Color(0xFF191C1D),
    surface = Color(0xFF191C1D),
)

@Composable
fun TravelHubTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit,
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme
    MaterialTheme(
        colorScheme = colorScheme,
        content = content,
    )
}
