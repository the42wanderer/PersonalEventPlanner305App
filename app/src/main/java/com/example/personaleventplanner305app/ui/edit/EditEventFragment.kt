package com.example.personaleventplanner305app.ui.edit

import android.app.DatePickerDialog
import android.app.TimePickerDialog
import android.os.Bundle
import android.view.View
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.Spinner
import android.widget.TextView
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.fragment.findNavController
import com.example.personaleventplanner305app.R
import com.example.personaleventplanner305app.data.AppDatabase
import com.example.personaleventplanner305app.data.Event
import com.example.personaleventplanner305app.data.EventRepository
import com.example.personaleventplanner305app.ui.EventViewModel
import com.example.personaleventplanner305app.ui.EventViewModelFactory
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale

class EditEventFragment : Fragment(R.layout.fragment_edit_event) {

    private lateinit var eventViewModel: EventViewModel
    private var currentEvent: Event? = null
    private var selectedDateTimeMillis: Long? = null
    private val dateFormat = SimpleDateFormat("dd/MM/yyyy hh:mm a", Locale.getDefault())

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val repository = EventRepository(AppDatabase.getDatabase(requireContext()).eventDao())
        eventViewModel = ViewModelProvider(
            requireActivity(),
            EventViewModelFactory(repository)
        )[EventViewModel::class.java]

        val titleInput = view.findViewById<EditText>(R.id.input_title_edit)
        val categorySpinner = view.findViewById<Spinner>(R.id.spinner_category_edit)
        val locationInput = view.findViewById<EditText>(R.id.input_location_edit)
        val dateTimeText = view.findViewById<TextView>(R.id.text_selected_datetime_edit)
        val pickDateTimeButton = view.findViewById<Button>(R.id.button_pick_datetime_edit)
        val updateButton = view.findViewById<Button>(R.id.button_update_event)
        val deleteButton = view.findViewById<Button>(R.id.button_delete_event)

        val categoryAdapter = ArrayAdapter.createFromResource(
            requireContext(),
            R.array.event_categories,
            android.R.layout.simple_spinner_item
        ).also { it.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item) }
        categorySpinner.adapter = categoryAdapter

        val eventId = arguments?.getLong("eventId") ?: -1L
        if (eventId <= 0L) {
            Toast.makeText(requireContext(), R.string.error_event_not_found, Toast.LENGTH_SHORT).show()
            findNavController().popBackStack()
            return
        }

        eventViewModel.loadEventById(eventId)
        eventViewModel.selectedEvent.observe(viewLifecycleOwner) { event ->
            if (event == null) return@observe
            currentEvent = event
            selectedDateTimeMillis = event.dateTimeMillis

            titleInput.setText(event.title)
            locationInput.setText(event.location)
            dateTimeText.text =
                getString(R.string.selected_datetime, dateFormat.format(Date(event.dateTimeMillis)))

            val categoryIndex = resources.getStringArray(R.array.event_categories).indexOf(event.category)
            if (categoryIndex >= 0) categorySpinner.setSelection(categoryIndex)
        }

        pickDateTimeButton.setOnClickListener {
            showDateTimePicker { millis ->
                selectedDateTimeMillis = millis
                dateTimeText.text = getString(R.string.selected_datetime, dateFormat.format(Date(millis)))
            }
        }

        updateButton.setOnClickListener {
            val event = currentEvent ?: return@setOnClickListener
            val title = titleInput.text.toString().trim()
            val category = categorySpinner.selectedItem.toString()
            val location = locationInput.text.toString().trim()
            val dateTime = selectedDateTimeMillis

            if (title.isEmpty()) {
                Toast.makeText(requireContext(), R.string.error_title_empty, Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }
            if (dateTime == null) {
                Toast.makeText(requireContext(), R.string.error_datetime_empty, Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }
            if (dateTime < System.currentTimeMillis()) {
                Toast.makeText(requireContext(), R.string.error_datetime_past, Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            val updatedEvent = event.copy(
                title = title,
                category = category,
                location = location,
                dateTimeMillis = dateTime
            )

            eventViewModel.updateEvent(updatedEvent) {
                requireActivity().runOnUiThread {
                    Toast.makeText(requireContext(), R.string.message_event_updated, Toast.LENGTH_SHORT).show()
                    findNavController().popBackStack()
                }
            }
        }

        deleteButton.setOnClickListener {
            val event = currentEvent ?: return@setOnClickListener
            eventViewModel.deleteEvent(event) {
                requireActivity().runOnUiThread {
                    Toast.makeText(requireContext(), R.string.message_event_deleted, Toast.LENGTH_SHORT).show()
                    findNavController().popBackStack()
                }
            }
        }
    }

    private fun showDateTimePicker(onDateTimeSelected: (Long) -> Unit) {
        val calendar = Calendar.getInstance()
        DatePickerDialog(
            requireContext(),
            { _, year, month, dayOfMonth ->
                val timeCalendar = Calendar.getInstance().apply {
                    set(Calendar.YEAR, year)
                    set(Calendar.MONTH, month)
                    set(Calendar.DAY_OF_MONTH, dayOfMonth)
                }
                TimePickerDialog(
                    requireContext(),
                    { _, hourOfDay, minute ->
                        timeCalendar.set(Calendar.HOUR_OF_DAY, hourOfDay)
                        timeCalendar.set(Calendar.MINUTE, minute)
                        timeCalendar.set(Calendar.SECOND, 0)
                        onDateTimeSelected(timeCalendar.timeInMillis)
                    },
                    calendar.get(Calendar.HOUR_OF_DAY),
                    calendar.get(Calendar.MINUTE),
                    false
                ).show()
            },
            calendar.get(Calendar.YEAR),
            calendar.get(Calendar.MONTH),
            calendar.get(Calendar.DAY_OF_MONTH)
        ).show()
    }
}
