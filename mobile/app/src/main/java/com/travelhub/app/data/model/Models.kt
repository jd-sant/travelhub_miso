package com.travelhub.app.data.model

data class Trip(
    val id: String,
    val name: String,
    val destination: String,
    val description: String? = null,
    val startDate: String? = null,
    val endDate: String? = null,
    val price: Double,
)

data class User(
    val id: String,
    val username: String,
    val email: String,
    val fullName: String? = null,
)

data class AuthToken(
    val accessToken: String,
    val tokenType: String,
)
