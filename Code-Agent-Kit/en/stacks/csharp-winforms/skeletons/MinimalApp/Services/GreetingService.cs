using System;
using System.Threading.Tasks;

namespace MinimalApp
{
    /// <summary>
    /// Service-layer code has no UI thread affinity, so it uses
    /// ConfigureAwait(false). Only the form resumes on the UI thread.
    /// </summary>
    public sealed class GreetingService : IGreetingService
    {
        public async Task<string> GetGreetingAsync(string name)
        {
            await Task.Delay(1).ConfigureAwait(false);

            return string.IsNullOrWhiteSpace(name)
                ? "Enter a name."
                : string.Concat("Hello, ", name.Trim(), ".");
        }
    }
}
