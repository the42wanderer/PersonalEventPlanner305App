package com.example.personaleventplanner305app.ui.list

import android.os.Bundle
import android.view.View
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.personaleventplanner305app.R
import com.example.personaleventplanner305app.data.AppDatabase
import com.example.personaleventplanner305app.data.EventRepository
import com.example.personaleventplanner305app.ui.EventViewModel
import com.example.personaleventplanner305app.ui.EventViewModelFactory

class EventListFragment : Fragment(R.layout.fragment_event_list) {

    private lateinit var eventViewModel: EventViewModel

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val repository = EventRepository(AppDatabase.getDatabase(requireContext()).eventDao())
        eventViewModel = ViewModelProvider(
            requireActivity(),
            EventViewModelFactory(repository)
        )[EventViewModel::class.java]

        val recyclerView = view.findViewById<RecyclerView>(R.id.recycler_events)
        val emptyText = view.findViewById<TextView>(R.id.text_empty_events)
        val adapter = EventAdapter { event ->
            val bundle = Bundle().apply { putLong("eventId", event.id) }
            findNavController().navigate(R.id.action_eventListFragment_to_editEventFragment, bundle)
        }

        recyclerView.layoutManager = LinearLayoutManager(requireContext())
        recyclerView.adapter = adapter

        eventViewModel.upcomingEvents.observe(viewLifecycleOwner) { events ->
            adapter.submitList(events)
            emptyText.visibility = if (events.isEmpty()) View.VISIBLE else View.GONE
        }
    }
}
