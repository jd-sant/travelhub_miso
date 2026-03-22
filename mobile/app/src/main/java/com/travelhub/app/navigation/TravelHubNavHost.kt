package com.travelhub.app.navigation

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.travelhub.app.ui.screens.HomeScreen
import com.travelhub.app.ui.screens.TripsScreen

sealed class Screen(val route: String) {
    object Home : Screen("home")
    object Trips : Screen("trips")
}

@Composable
fun TravelHubNavHost(
    navController: NavHostController,
    modifier: Modifier = Modifier,
) {
    NavHost(
        navController = navController,
        startDestination = Screen.Home.route,
        modifier = modifier,
    ) {
        composable(Screen.Home.route) {
            HomeScreen(onNavigateToTrips = { navController.navigate(Screen.Trips.route) })
        }
        composable(Screen.Trips.route) {
            TripsScreen(onNavigateBack = { navController.popBackStack() })
        }
    }
}
