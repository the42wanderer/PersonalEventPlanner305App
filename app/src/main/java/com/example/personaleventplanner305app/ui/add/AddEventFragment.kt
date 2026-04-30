package com.example.personaleventplanner305app.ui.add

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

class AddEventFragment : Fragment(R.layout.fragment_add_event) {

    private lateinit var eventViewModel: EventViewModel
    private var selectedDateTimeMillis: Long? = null
    private val dateFormat = SimpleDateFormat("dd/MM/yyyy hh:mm a", Locale.getDefault())

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val repository = EventRepository(AppDatabase.getDatabase(requireContext()).eventDao())
        eventViewModel = ViewModelProvider(
            requireActivity(),
            EventViewModelFactory(repository)
        )[EventViewModel::class.java]

        val titleInput = view.findViewById<EditText>(R.id.input_title)
        val categorySpinner = view.findViewById<Spinner>(R.id.spinner_category)
        val locationInput = view.findViewById<EditText>(R.id.input_location)
        val dateTimeText = view.findViewById<TextView>(R.id.text_selected_datetime)
        val pickDateTimeButton = view.findViewById<Button>(R.id.button_pick_datetime)
        val saveButton = view.findViewById<Button>(R.id.button_save_event)

        val categoryAdapter = ArrayAdapter.createFromResource(
            requireContext(),
            R.array.event_categories,
            android.R.layout.simple_spinner_item
        ).also { it.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item) }
        categorySpinner.adapter = categoryAdapter

        pickDateTimeButton.setOnClickListener {
            showDateTimePicker { millis ->
                selectedDateTimeMillis = millis
                dateTimeText.text = getString(R.string.selected_datetime, dateFormat.format(Date(millis)))
            }
        }

        saveButton.setOnClickListener {
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

            val newEvent = Event(
                title = title,
                category = category,
                location = location,
                dateTimeMillis = dateTime
            )

            eventViewModel.addEvent(newEvent) {
                requireActivity().runOnUiThread {
                    Toast.makeText(requireContext(), R.string.message_event_saved, Toast.LENGTH_SHORT).show()
                    titleInput.text?.clear()
                    locationInput.text?.clear()
                    categorySpinner.setSelection(0)
                    selectedDateTimeMillis = null
                    dateTimeText.text = getString(R.string.no_datetime_selected)
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
