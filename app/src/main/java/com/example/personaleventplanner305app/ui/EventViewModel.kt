package com.example.personaleventplanner305app.ui

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.personaleventplanner305app.data.Event
import com.example.personaleventplanner305app.data.EventRepository
import kotlinx.coroutines.launch

class EventViewModel(private val repository: EventRepository) : ViewModel() {

    val upcomingEvents: LiveData<List<Event>> = repository.getUpcomingEvents(System.currentTimeMillis())

    private val _selectedEvent = MutableLiveData<Event?>()
    val selectedEvent: LiveData<Event?> = _selectedEvent

    fun loadEventById(eventId: Long) {
        viewModelScope.launch {
            _selectedEvent.postValue(repository.getEventById(eventId))
        }
    }

    fun addEvent(event: Event, onComplete: () -> Unit) {
        viewModelScope.launch {
            repository.insertEvent(event)
            onComplete()
        }
    }

    fun updateEvent(event: Event, onComplete: () -> Unit) {
        viewModelScope.launch {
            repository.updateEvent(event)
            onComplete()
        }
    }

    fun deleteEvent(event: Event, onComplete: () -> Unit) {
        viewModelScope.launch {
            repository.deleteEvent(event)
            onComplete()
        }
    }
}
