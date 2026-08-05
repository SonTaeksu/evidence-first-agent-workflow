using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace MinimalApp.ViewModels
{
    /// <summary>
    /// Hand-rolled, deliberately. Whether this project uses an MVVM framework is a
    /// capability decision recorded in STACK-READINESS.json; a skeleton that
    /// referenced one would be making that decision instead of starting from it.
    /// </summary>
    public abstract class ObservableObject : INotifyPropertyChanged
    {
        public event PropertyChangedEventHandler PropertyChanged;

        protected void Raise([CallerMemberName] string propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
