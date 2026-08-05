using System.Windows;
using MinimalApp.ViewModels;

namespace MinimalApp
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();

            // Assigned explicitly. An unassigned DataContext is inherited from the
            // parent element, so moving this window in a visual tree would change
            // what it binds to without any error.
            DataContext = new MainViewModel();
        }
    }
}
