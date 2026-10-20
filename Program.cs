using System;
using System.Threading.Tasks;
using ItmeArena.Tests;
public static class Program
{
    public static async Task<int> Main()
    {
        try { foreach(var result in await OnboardingChecks.RunAll()) Console.WriteLine("PASS: "+result); foreach(var result in MenuChecks.RunAll()) Console.WriteLine("PASS: "+result); foreach(var result in MovementChecks.RunAll()) Console.WriteLine("PASS: "+result); foreach(var result in PushChecks.RunAll()) Console.WriteLine("PASS: "+result); foreach(var result in GripChecks.RunAll()) Console.WriteLine("PASS: "+result); foreach(var result in MatchChecks.RunAll()) Console.WriteLine("PASS: "+result); foreach(var result in VisualChecks.RunAll()) Console.WriteLine("PASS: "+result); foreach(var result in CustomizationChecks.RunAll()) Console.WriteLine("PASS: "+result); foreach(var result in StairwellChecks.RunAll()) Console.WriteLine("PASS: "+result); foreach(var result in FactoryChecks.RunAll()) Console.WriteLine("PASS: "+result); foreach(var result in CraterChecks.RunAll()) Console.WriteLine("PASS: "+result); foreach(var result in SelectionChecks.RunAll()) Console.WriteLine("PASS: "+result); foreach(var result in BotChecks.RunAll()) Console.WriteLine("PASS: "+result); foreach(var result in UltimateChecks.RunAll()) Console.WriteLine("PASS: "+result); foreach(var result in DragChecks.RunAll()) Console.WriteLine("PASS: "+result); return 0; }
        catch(Exception e) { Console.Error.WriteLine(e); return 1; }
    }
}
