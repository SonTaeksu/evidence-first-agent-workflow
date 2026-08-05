using System;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace MinimalApp
{
    /// <summary>
    /// Behaviour only. Layout lives in MainForm.Designer.cs, which the
    /// designer owns and rewrites.
    /// </summary>
    public partial class MainForm : Form
    {
        private readonly IGreetingService _greetingService;

        public MainForm(IGreetingService greetingService)
        {
            if (greetingService == null)
            {
                throw new ArgumentNullException(nameof(greetingService));
            }

            _greetingService = greetingService;
            InitializeComponent();
        }

        private async void OnGreetClick(object sender, EventArgs e)
        {
            btnGreet.Enabled = false;
            try
            {
                string greeting = await _greetingService
                    .GetGreetingAsync(txtName.Text)
                    .ConfigureAwait(true);

                // ConfigureAwait(true) returns to the UI thread, so no marshal
                // is needed here. Anything resumed off the UI thread must go
                // through SetStatusSafe.
                lblStatus.Text = greeting;
            }
            finally
            {
                btnGreet.Enabled = true;
            }
        }

        /// <summary>
        /// Controls are bound to the thread that created them. Calling one from
        /// another thread raises InvalidOperationException.
        /// </summary>
        public void SetStatusSafe(string text)
        {
            if (lblStatus.InvokeRequired)
            {
                lblStatus.Invoke(new Action<string>(SetStatusSafe), text);
                return;
            }

            lblStatus.Text = text;
        }
    }
}
