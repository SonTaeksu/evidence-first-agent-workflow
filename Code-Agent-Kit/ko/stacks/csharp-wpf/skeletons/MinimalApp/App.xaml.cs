using System.Diagnostics;
using System.Windows;

namespace MinimalApp
{
    public partial class App : Application
    {
        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);

            // A failed binding throws nothing and logs nothing at the default
            // trace level: the control simply renders empty. Raising this source
            // is the only way a binding mistake becomes observable, and it is the
            // single most useful line in a WPF skeleton.
            PresentationTraceSources.Refresh();
            PresentationTraceSources.DataBindingSource.Switch.Level = SourceLevels.Warning;
            PresentationTraceSources.DataBindingSource.Listeners.Add(
                new ConsoleTraceListener());
        }
    }
}
