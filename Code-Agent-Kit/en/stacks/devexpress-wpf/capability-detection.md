# Capability Detection — DevExpress WPF (v24.2+)

A capability is detected from the repository, never assumed. The Unknown Rule is
what applies when detection is inconclusive, and it blocks rather than guesses —
one wrong guess costs more than the pause.

The plain-WPF capabilities in `../csharp-wpf/capability-detection.md` are
detected as well and are not repeated here. This table adds the DevExpress ones.

| Capability | Detection | Present Path | Absent Path | Unknown Rule |
|---|---|---|---|---|
| devexpress-version | the DevExpress version the build resolves — from the restore output, not from an installed-products list | answer within that version, and pin the documentation server to it | confirm with the owner | block every DevExpress API answer, and block choosing between dxdocs and dxdocs24_2 |
| mvvm-source | which MVVM base types the view models derive from, and whether a third-party MVVM package is also referenced | follow the framework already in use | confirm with the owner before introducing one | block introducing a second MVVM framework |
| binding-dialect | whether the XAML in scope uses DevExpress binding and command markup extensions or plain Binding and ICommand | keep the dialect that file already uses | keep plain WPF binding | block mixing dialects inside one view |
| theme-deployment | which theme is applied at startup, where that happens, and which theme assemblies are present in the published output | ship and set the theme already in use | report that the application is unthemed rather than assuming a default | block changing the theme, and block trimming any theme assembly |
| grid-view | the View element declared inside each GridControl in the XAML in scope | configure behaviour on that view type | not applicable where no grid is involved | block applying an answer written for a different view type |
| docking | a reference to DevExpress.Xpf.Docking, and whether a saved layout is restored at startup | change the layout through the docking layout and account for restored layouts | plain WPF layout, per ../csharp-wpf | block a layout change until the persistence question is answered |

Two of these deserve a note on *why* the detection is written the way it is.

`devexpress-version` is read from what the build resolved, not from what is
installed. A developer machine typically has more than one DevExpress version
present, and the installed set is not the set the build used.

`theme-deployment` is read from the published output rather than the project
file, because the theme assemblies are loaded by value at runtime and nothing in
the compiled code references them. The project file can be entirely correct while
the output is missing them, and the application will still start.

Every capability a feature relies on must appear in the Project Map and be
repeated in Gate Analysis, so that a later reader can see which branch was taken
and why.
