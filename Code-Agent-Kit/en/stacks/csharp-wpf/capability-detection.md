# Capability Detection — WPF (.NET Framework 4.7.2+)

A capability is detected from the repository, never assumed. The Unknown Rule is
what applies when detection is inconclusive, and it blocks rather than guesses —
one wrong guess costs more than the pause.

| Capability | Detection | Present Path | Absent Path | Unknown Rule |
|---|---|---|---|---|
| mvvm-framework | reference to a known MVVM package in the project file | use its base classes and commands | hand-rolled INotifyPropertyChanged plus an approved command type | block introducing a pattern the project does not already use |
| dependency-injection | container registration in `App.xaml.cs` or a bootstrapper | resolve through the container | construct explicitly at the composition root | block introducing a container |
| ui-automation | AutomationProperties in XAML, or a UI test project | assert through automation ids | assert through the view model only | block claiming UI behaviour was verified |
| localization | `*.resx` satellite resources or `x:Uid` markup | add strings to the existing resource set | keep literals with a recorded reason | block inventing a localization scheme |

Every capability a feature relies on must appear in the Project Map and be
repeated in Gate Analysis, so that a later reader can see which branch was taken
and why.
