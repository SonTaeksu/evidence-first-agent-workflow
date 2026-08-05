# Pitfalls — WPF (.NET Framework 4.7.2+)

Each of these is a property of the technology, verifiable independently of any
project. They are collected because they share one characteristic: **the failure
is silent, or the error message names something other than the cause.** A stack
whose failures announce themselves does not need a list like this.

## Silent binding failure

A misspelled `Path` produces no exception and no compiler error — the control renders empty. Raise `PresentationTraceSources.DataBindingSource` to Warning, or assert on the bound value in a test. Never conclude 'the binding works' from the absence of an error.

## DataContext inherited, not assigned

A control with no explicit `DataContext` inherits its parent's. Moving an element in the visual tree silently changes what it binds to.

## Collection updates off the UI thread

`ObservableCollection` raises change notifications on the calling thread; WPF requires the UI thread. Marshal through the `Dispatcher`.

## Resource lookup order

A key resolves from the element outward, then application, then theme. Two resources with the same key at different levels resolve differently depending on where the element sits.

## Framework version behaviour

4.7.2, 4.8 and 4.8.1 differ in DPI handling and some default styles. Look the version up rather than recalling it; the target framework in the project file is the authority.
