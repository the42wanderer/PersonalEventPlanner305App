package com.example.personaleventplanner305app.data

import androidx.lifecycle.LiveData
import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.Query
import androidx.room.Update

@Dao
interface EventDao {
    @Query("SELECT * FROM events WHERE dateTimeMillis >= :currentTime ORDER BY dateTimeMillis ASC")
    fun getUpcomingEvents(currentTime: Long): LiveData<List<Event>>

    @Query("SELECT * FROM events WHERE id = :id LIMIT 1")
    suspend fun getEventById(id: Long): Event?

    @Insert
    suspend fun insertEvent(event: Event)

    @Update
    suspend fun updateEvent(event: Event)

    @Delete
    suspend fun deleteEvent(event: Event)
}
