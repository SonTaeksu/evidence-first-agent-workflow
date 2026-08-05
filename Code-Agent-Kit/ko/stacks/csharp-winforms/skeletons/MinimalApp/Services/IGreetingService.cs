using System.Threading.Tasks;

namespace MinimalApp
{
    /// <summary>
    /// The single entry point the form uses to reach anything outside itself.
    /// The form never calls a network, file, or database API directly.
    /// </summary>
    public interface IGreetingService
    {
        Task<string> GetGreetingAsync(string name);
    }
}
