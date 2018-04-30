# HCI_Productivity_App
In the 21st century, many things are constantly vying for our attention.
To compensate, people frequently set up all of these tasks to be done at once, seeing multitasking as the
only option to get through the mess of responsibilities. Although it seems intuitive to make progress in all
of these tasks at once, research has shown that it is actually counterproductive due to the cost of
switching tasks, placing a burden on the brain that takes time to recover from. To combat this, we have created
a proof of concept for a productivity application that forces the user to make a mutually agreed upon amount
of progress before being able to switch to a different task.

### Job Window
Here is where each job is contained, with the Window Manager to the left and a Task Menu to the right. Every time the ‘Start New Task’ option is selected, a new Job Window is created, and they can be navigated between by using the ‘Switch Tab’ option. You can close the current Job Window through the ‘Close Current Tab’ option.

### Window Manager
The Window Manager serves as the menu to choose which application is to be run as well as act as a container for said application. The text bar at the top allows you to search through the list of available applications. If you cannot find an application that you wish for, you can either change the directory of the link files through the settings to a folder where you keep all the shortcuts you use, such as the absolute address of the desktop (e.g. “C:/Users/user/Desktop”), or you can create a shortcut file for the desired application and place it in the default folder, “C:\ProgramData\Microsoft\Windows\Start Menu\Programs”

### Task Menu
Here you can manage the means by which progress is tracked. By typing into the text box and either clicking the ‘Add Task’ button or pressing ‘Enter,’ a task is created and shown below. Once the task is complete, you can click on the task in the Task Menu to mark it down. The text changes to have the ‘strikethrough’ decoration, and the counter above is added to. The number of tasks needed to change to a different job is determined at the intensity menu opened as soon as the application is opened. The defaults are 3 tasks for light intensity, 5 for medium intensity, and 7 for high intensity, but these can be changed in the settings menu. Once the task counter hits the number of tasks desired, a menu is brought up to determine what is to be done next. From here, you can decide to continue on the same job, switch to a different one, create a new one, or quit the application.

### Bugs
*To ensure one is never stuck at a specific tab, Options > Settings allows to switch tasks, create new tasks etc.
*Processes are not killed when the app is closed, so you must do that manually through the Task Manager
*Certain windows when grabbed do not allow for text input; to type into something such as an address bar, use the task menu, then right click copy and paste
*Certain apps have menu windows different from the actual windows; open the window where you will be working first, then use Options > Get Missing Window to grab
