using System;
using System.Windows.Input;

namespace MinimalApp.ViewModels
{
    public sealed class MainViewModel : ObservableObject
    {
        private string _greeting = "Ready.";

        public string Greeting
        {
            get { return _greeting; }
            private set { _greeting = value; Raise(); }
        }

        public ICommand GreetCommand { get; }

        public MainViewModel()
        {
            GreetCommand = new RelayCommand(() => Greeting = "Hello.");
        }
    }

    internal sealed class RelayCommand : ICommand
    {
        private readonly Action _execute;

        public RelayCommand(Action execute)
        {
            _execute = execute ?? throw new ArgumentNullException(nameof(execute));
        }

        public event EventHandler CanExecuteChanged;

        public bool CanExecute(object parameter) { return true; }

        public void Execute(object parameter) { _execute(); }
    }
}
