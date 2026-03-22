package com.travelhub.app.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.travelhub.app.data.model.Trip

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TripsScreen(onNavigateBack: () -> Unit) {
    val sampleTrips = listOf(
        Trip(id = "1", name = "Paris Adventure", destination = "Paris, France", price = 1500.0),
        Trip(id = "2", name = "Tokyo Tour", destination = "Tokyo, Japan", price = 3000.0),
        Trip(id = "3", name = "Rome Trip", destination = "Rome, Italy", price = 1200.0),
    )

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Trips") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Back",
                        )
                    }
                },
            )
        },
    ) { innerPadding ->
        LazyColumn(
            contentPadding = innerPadding,
            verticalArrangement = Arrangement.spacedBy(8.dp),
            modifier = Modifier.padding(horizontal = 16.dp),
        ) {
            items(sampleTrips) { trip ->
                TripCard(trip = trip)
            }
        }
    }
}

@Composable
fun TripCard(trip: Trip) {
    Card(
        modifier = Modifier.fillMaxWidth(),
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(text = trip.name, style = MaterialTheme.typography.titleMedium)
            Text(text = trip.destination, style = MaterialTheme.typography.bodyMedium)
            Text(text = "From $${trip.price}", style = MaterialTheme.typography.bodySmall)
        }
    }
}
