package com.example.personaleventplanner305app.ui.list

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.personaleventplanner305app.R
import com.example.personaleventplanner305app.data.Event
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class EventAdapter(
    private val onItemClick: (Event) -> Unit
) : RecyclerView.Adapter<EventAdapter.EventViewHolder>() {

    private val events = mutableListOf<Event>()
    private val dateFormat = SimpleDateFormat("dd/MM/yyyy hh:mm a", Locale.getDefault())

    fun submitList(newEvents: List<Event>) {
        events.clear()
        events.addAll(newEvents)
        notifyDataSetChanged()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): EventViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_event, parent, false)
        return EventViewHolder(view)
    }

    override fun onBindViewHolder(holder: EventViewHolder, position: Int) {
        val event = events[position]
        holder.bind(event)
        holder.itemView.setOnClickListener { onItemClick(event) }
    }

    override fun getItemCount(): Int = events.size

    inner class EventViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val titleText: TextView = itemView.findViewById(R.id.text_event_title)
        private val categoryText: TextView = itemView.findViewById(R.id.text_event_category)
        private val locationText: TextView = itemView.findViewById(R.id.text_event_location)
        private val dateTimeText: TextView = itemView.findViewById(R.id.text_event_datetime)

        fun bind(event: Event) {
            titleText.text = event.title
            categoryText.text = itemView.context.getString(R.string.category_format, event.category)
            locationText.text = itemView.context.getString(R.string.location_format, event.location)
            dateTimeText.text = itemView.context.getString(
                R.string.datetime_format,
                dateFormat.format(Date(event.dateTimeMillis))
            )
        }
    }
}
