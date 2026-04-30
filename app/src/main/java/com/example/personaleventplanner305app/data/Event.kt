package com.example.personaleventplanner305app.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "events")
data class Event(
    @PrimaryKey(autoGenerate = true) val id: Long = 0L,
    val title: String,
    val category: String,
    val location: String,
    val dateTimeMillis: Long
)
