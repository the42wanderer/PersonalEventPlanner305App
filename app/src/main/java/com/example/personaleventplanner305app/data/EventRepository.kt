package com.example.personaleventplanner305app.data

class EventRepository(private val eventDao: EventDao) {

    fun getUpcomingEvents(currentTime: Long) = eventDao.getUpcomingEvents(currentTime)

    suspend fun getEventById(id: Long): Event? = eventDao.getEventById(id)

    suspend fun insertEvent(event: Event) = eventDao.insertEvent(event)

    suspend fun updateEvent(event: Event) = eventDao.updateEvent(event)

    suspend fun deleteEvent(event: Event) = eventDao.deleteEvent(event)
}
