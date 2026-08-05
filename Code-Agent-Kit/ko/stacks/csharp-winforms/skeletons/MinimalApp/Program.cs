using System;
using System.Windows.Forms;

namespace MinimalApp
{
    internal static class Program
    {
        /// <summary>
        /// EnableVisualStyles must be the first call in the entry point;
        /// high DPI support depends on it.
        /// </summary>
        [STAThread]
        private static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new MainForm(new GreetingService()));
        }
    }
}
