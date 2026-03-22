package com.travelhub.app.data.network

import com.travelhub.app.BuildConfig
import com.travelhub.app.data.model.AuthToken
import com.travelhub.app.data.model.Trip
import com.travelhub.app.data.model.User
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.*

interface TravelHubApiService {

    @GET("trips")
    suspend fun getTrips(): List<Trip>

    @GET("trips/{id}")
    suspend fun getTrip(@Path("id") id: String): Trip

    @GET("users/{id}")
    suspend fun getUser(@Path("id") id: String): User

    @FormUrlEncoded
    @POST("auth/token")
    suspend fun login(
        @Field("username") username: String,
        @Field("password") password: String,
    ): AuthToken
}

object ApiClient {
    private val loggingInterceptor = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY
    }

    private val okHttpClient = OkHttpClient.Builder()
        .addInterceptor(loggingInterceptor)
        .build()

    val service: TravelHubApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BuildConfig.API_BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(TravelHubApiService::class.java)
    }
}
