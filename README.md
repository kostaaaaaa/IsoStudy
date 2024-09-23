# IsoStudy

## Goal

Allow users to isolate their environments to focus on their school goals or personal goals within a user defined time period. Distractions will be limited during this time limit allowin for maximum efficiency. Users are prompted to list apps that are the leading causes of their distractions will then be forced closed during the whole duration of the time period. A force quit option is available at all times to back out of the isolation in case of emergencies or finishing their tasks earlier than the time limit. This is mostly targeted to students who wish to study productively.

## (Current) Features
- Adjustable time limit, silenced apps and task list
- Time remaining displayed with task list
- Zen-mode that can toggle the view of the task list while maintaining the time remaining
- Maintains silenced apps listed by the user to stay closed

## Notes

Installing the necessary packages is all that is necessary to start running this code. Currently, there is a default setting of silenced apps with generic apps. If you have better apps to list within DEFAULT_SILENCED_APPS feel free to change it to your personal uses.  


## Packages
- [AppOpener](https://pypi.org/project/appopener/) ``` pip install AppOpener ```
- [pstuil](https://pypi.org/project/psutil/) ``` pip install psutil ```
- [PyQt5](https://pypi.org/project/PyQt5/) ``` pip install PyQt5 ```
