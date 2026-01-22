using System;
using System.Diagnostics;

class Program
{
    static void Main()
    {
        var psi = new ProcessStartInfo
        {
            FileName = "python",
            Arguments = @"C:\YOLO11\python\FireExtinguisher_.py",
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            CreateNoWindow = false
        };

        var process = Process.Start(psi);

        process.OutputDataReceived += (s, e) =>
        {
            if (e.Data != null)
                Console.WriteLine("[PY] " + e.Data);
        };

        process.BeginOutputReadLine();
        process.WaitForExit();
    }
}
