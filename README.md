# Personal Event Planner App - SIT305 Pass Task 4.1

## Student Details
- Name: Danidu Thejas Karunarathne Hetti Muhandiramge
- Student ID: 224388526
- Unit: SIT305
- Task: Pass Task 4.1 Personal Event Planner App

## Project Overview
This is a simple Android app for managing personal events.  
It supports full CRUD (Create, Read, Update, Delete) using a local Room database and uses Fragments with Jetpack Navigation and a Bottom Navigation Bar.

## Features
- Create new events
- View upcoming events sorted by date/time (ascending)
- Edit existing events by tapping an event from the list
- Delete events
- Persist event data locally with Room
- Validate input and show Toast messages for errors and success

## Event Fields
Each event includes:
- Title
- Category (Work, Social, Travel, Study, Other)
- Location
- Date/Time

## Technologies Used
- Kotlin
- XML layouts
- Fragments
- Jetpack Navigation Component
- BottomNavigationView
- RecyclerView
- Room Database
- ViewModel + LiveData

## App Structure
- `MainActivity.kt`
- `data/Event.kt`
- `data/EventDao.kt`
- `data/AppDatabase.kt`
- `data/EventRepository.kt`
- `ui/EventViewModel.kt`
- `ui/EventViewModelFactory.kt`
- `ui/list/EventListFragment.kt`
- `ui/list/EventAdapter.kt`
- `ui/add/AddEventFragment.kt`
- `ui/edit/EditEventFragment.kt`
- `res/navigation/nav_graph.xml`
- `res/menu/bottom_nav_menu.xml`
- XML layouts for activity, fragments, and list row

## CRUD Explanation
- **Create:** Use Add Event screen, fill fields, select date/time, and tap Save.
- **Read:** Event List screen shows all upcoming events sorted by date/time.
- **Update:** Tap an event in the list, edit values, and tap Update.
- **Delete:** Tap an event in the list, then tap Delete.

## Validation Rules
- Title cannot be empty.
- Date/time cannot be empty.
- Date/time cannot be in the past.
- Toast messages are shown for:
  - Validation errors
  - Save success
  - Update success
  - Delete success

## How to Run
1. Open the project in Android Studio.
2. Let Gradle sync finish.
3. Run on emulator or physical device.

Build command from terminal:
```bash
./gradlew :app:assembleDebug
```

## LLM/AI Usage Declaration
I used AI assistance (Cursor/Codex) to support development tasks such as code generation, structure suggestions, and documentation drafting.  
I reviewed, tested, and validated the final implementation before submission.
